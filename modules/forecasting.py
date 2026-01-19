"""
Module 6: Predictive Forecasting Engine
Time-series forecasting and trend analysis for proactive governance
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class PredictiveForecastingEngine:
    """
    Forecasts future trends using:
    - Linear regression for trend analysis
    - Seasonal decomposition for patterns
    - Growth rate projections
    """
    
    def __init__(self, data):
        self.data = data.copy()
        self.forecasts = None
        
    def forecast_state_enrolments(self, months_ahead=6):
        """
        Forecast enrolments for each state for the next N months
        """
        results = []
        
        # Group by state and month
        monthly_data = self.data.groupby(['state', 'month_year']).agg({
            'total_enrolment': 'sum'
        }).reset_index()
        
        for state in monthly_data['state'].unique():
            state_data = monthly_data[monthly_data['state'] == state].copy()
            state_data = state_data.sort_values('month_year')
            
            if len(state_data) < 3:  # Need at least 3 months for forecasting
                continue
            
            # Prepare time-series data
            state_data['time_index'] = np.arange(len(state_data))
            X = state_data[['time_index']].values
            y = state_data['total_enrolment'].values
            
            # Fit linear regression model
            model = LinearRegression()
            model.fit(X, y)
            
            # Calculate trend metrics
            slope = model.coef_[0]
            r_squared = model.score(X, y)
            
            # Calculate growth rate
            avg_enrolment = y.mean()
            growth_rate_per_month = (slope / avg_enrolment) * 100 if avg_enrolment > 0 else 0
            
            # Forecast future months
            last_time_index = state_data['time_index'].max()
            future_indices = np.arange(last_time_index + 1, last_time_index + 1 + months_ahead).reshape(-1, 1)
            future_predictions = model.predict(future_indices)
            
            # Calculate confidence intervals (95%)
            residuals = y - model.predict(X)
            std_error = np.std(residuals)
            confidence_interval = 1.96 * std_error
            
            # Determine trend direction
            if growth_rate_per_month > 2:
                trend = "RAPID GROWTH"
            elif growth_rate_per_month > 0.5:
                trend = "STEADY GROWTH"
            elif growth_rate_per_month > -0.5:
                trend = "STABLE"
            elif growth_rate_per_month > -2:
                trend = "DECLINING"
            else:
                trend = "RAPID DECLINE"
            
            # Sum total forecasted enrolments
            total_forecast = np.sum(future_predictions)
            
            results.append({
                'state': state,
                'current_monthly_avg': int(avg_enrolment),
                'growth_rate_pct_per_month': round(growth_rate_per_month, 2),
                'trend_direction': trend,
                'forecast_6m_total': int(total_forecast),
                'confidence_score': round(r_squared * 100, 1),
                'std_error': int(std_error),
                'policy_implication': self._get_policy_implication(trend, growth_rate_per_month)
            })
        
        return pd.DataFrame(results).sort_values('growth_rate_pct_per_month', ascending=False)
    
    def _get_policy_implication(self, trend, growth_rate):
        """Generate policy implication based on trend"""
        if trend == "RAPID GROWTH":
            return "Scale up enrolment centers and staff immediately"
        elif trend == "STEADY GROWTH":
            return "Plan gradual infrastructure expansion"
        elif trend == "STABLE":
            return "Maintain current capacity"
        elif trend == "DECLINING":
            return "Investigate causes - market saturation or service issues"
        else:
            return "ALERT: Investigate system problems or demographic changes"
    
    def detect_seasonal_patterns(self):
        """
        Detect seasonal patterns in biometric and demographic updates
        """
        # Aggregate by month across all locations
        monthly_totals = self.data.groupby('month_year').agg({
            'bio_age_17_plus': 'sum',
            'bio_age_5_17': 'sum',
            'demo_age_17_plus': 'sum',
            'demo_age_5_17': 'sum',
            'total_enrolment': 'sum'
        }).reset_index()
        
        monthly_totals = monthly_totals.sort_values('month_year')
        
        # Calculate month-over-month changes
        monthly_totals['bio_adult_mom_change'] = monthly_totals['bio_age_17_plus'].pct_change() * 100
        monthly_totals['bio_child_mom_change'] = monthly_totals['bio_age_5_17'].pct_change() * 100
        monthly_totals['enrolment_mom_change'] = monthly_totals['total_enrolment'].pct_change() * 100
        
        # Identify peak months
        peak_bio_adult = monthly_totals.loc[monthly_totals['bio_age_17_plus'].idxmax()]
        peak_enrolment = monthly_totals.loc[monthly_totals['total_enrolment'].idxmax()]
        low_enrolment = monthly_totals.loc[monthly_totals['total_enrolment'].idxmin()]
        
        # Calculate volatility
        enrolment_volatility = monthly_totals['total_enrolment'].std() / monthly_totals['total_enrolment'].mean() * 100
        
        patterns = {
            'monthly_data': monthly_totals,
            'peak_bio_month': str(peak_bio_adult['month_year']),
            'peak_bio_value': int(peak_bio_adult['bio_age_17_plus']),
            'peak_enrolment_month': str(peak_enrolment['month_year']),
            'peak_enrolment_value': int(peak_enrolment['total_enrolment']),
            'lowest_enrolment_month': str(low_enrolment['month_year']),
            'lowest_enrolment_value': int(low_enrolment['total_enrolment']),
            'enrolment_volatility_pct': round(enrolment_volatility, 1)
        }
        
        return patterns
    
    def identify_emerging_hotspots(self, top_n=10):
        """
        Identify districts with rapidly increasing activity (emerging hotspots)
        """
        # Calculate growth rates by district
        district_growth = []
        
        for state in self.data['state'].unique():
            for district in self.data[self.data['state'] == state]['district'].unique():
                district_data = self.data[
                    (self.data['state'] == state) & 
                    (self.data['district'] == district)
                ].sort_values('month_year')
                
                if len(district_data) < 3:
                    continue
                
                # Calculate total activity trend
                district_data['time_index'] = np.arange(len(district_data))
                district_data['total_activity'] = (
                    district_data['bio_age_17_plus'] + 
                    district_data['bio_age_5_17'] +
                    district_data['demo_age_17_plus'] + 
                    district_data['demo_age_5_17'] +
                    district_data['total_enrolment']
                )
                
                X = district_data[['time_index']].values
                y = district_data['total_activity'].values
                
                if len(y) > 0 and y.mean() > 0:
                    # Fit linear model
                    model = LinearRegression()
                    model.fit(X, y)
                    
                    slope = model.coef_[0]
                    avg_activity = y.mean()
                    growth_rate = (slope / avg_activity) * 100 if avg_activity > 0 else 0
                    
                    # Calculate acceleration (second derivative approximation)
                    if len(y) >= 3:
                        first_half_avg = y[:len(y)//2].mean()
                        second_half_avg = y[len(y)//2:].mean()
                        acceleration = ((second_half_avg - first_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0
                    else:
                        acceleration = 0
                    
                    district_growth.append({
                        'state': state,
                        'district': district,
                        'avg_monthly_activity': int(avg_activity),
                        'growth_rate_pct': round(growth_rate, 2),
                        'acceleration_pct': round(acceleration, 1),
                        'emerging_status': 'RAPID EMERGENCE' if growth_rate > 10 and acceleration > 20 else 'STEADY GROWTH' if growth_rate > 5 else 'STABLE'
                    })
        
        df_growth = pd.DataFrame(district_growth)
        df_growth = df_growth.sort_values('growth_rate_pct', ascending=False).head(top_n)
        
        return df_growth
    
    def predict_future_fraud_risk(self):
        """
        Predict which districts are at risk of developing fraud patterns
        """
        # Group by district
        district_summary = self.data.groupby(['state', 'district']).agg({
            'enrol_age_18_plus': 'sum',
            'enrol_age_5_17': 'sum',
            'enrol_age_0_5': 'sum',
            'bio_age_17_plus': 'sum',
            'bio_age_5_17': 'sum',
            'demo_age_17_plus': 'sum',
            'total_enrolment': 'sum'
        }).reset_index()
        
        # Calculate risk indicators
        district_summary['adult_enrol_ratio'] = (
            district_summary['enrol_age_18_plus'] / 
            (district_summary['total_enrolment'] + 1)
        )
        
        district_summary['bio_to_enrol_ratio'] = (
            district_summary['bio_age_17_plus'] / 
            (district_summary['enrol_age_18_plus'] + 1)
        )
        
        district_summary['demo_to_bio_ratio'] = (
            district_summary['demo_age_17_plus'] / 
            (district_summary['bio_age_17_plus'] + 1)
        )
        
        # Risk scoring
        risk_score = (
            (district_summary['adult_enrol_ratio'] > 0.9).astype(int) * 30 +  # Abnormally high adult ratio
            (district_summary['bio_to_enrol_ratio'] < 0.5).astype(int) * 40 +  # Low bio usage after enrolment
            (district_summary['demo_to_bio_ratio'] < 0.1).astype(int) * 30     # Very low updates
        )
        
        district_summary['fraud_risk_score'] = risk_score
        district_summary['predicted_risk'] = pd.cut(
            risk_score,
            bins=[-1, 30, 60, 100],
            labels=['LOW', 'MODERATE', 'HIGH']
        )
        
        high_risk = district_summary[district_summary['predicted_risk'] == 'HIGH'].sort_values(
            'fraud_risk_score', ascending=False
        )
        
        return high_risk[['state', 'district', 'fraud_risk_score', 'predicted_risk', 
                          'adult_enrol_ratio', 'bio_to_enrol_ratio', 'demo_to_bio_ratio', 
                          'total_enrolment']]
    
    def run_full_analysis(self):
        """
        Run complete forecasting analysis
        """
        print("\n" + "="*80)
        print("MODULE 6: PREDICTIVE FORECASTING ENGINE")
        print("="*80 + "\n")
        
        print("Generating Forecasts and Trend Analysis...\n")
        
        # Run all forecasting components
        state_forecasts = self.forecast_state_enrolments(months_ahead=6)
        seasonal_patterns = self.detect_seasonal_patterns()
        emerging_hotspots = self.identify_emerging_hotspots(top_n=10)
        future_fraud_risks = self.predict_future_fraud_risk()
        
        self.forecasts = {
            'state_forecasts': state_forecasts,
            'seasonal_patterns': seasonal_patterns,
            'emerging_hotspots': emerging_hotspots,
            'future_fraud_risks': future_fraud_risks
        }
        
        print(f"✓ State Forecasts: Generated for {len(state_forecasts)} states")
        print(f"✓ Seasonal Patterns: Analyzed {len(seasonal_patterns['monthly_data'])} months")
        print(f"✓ Emerging Hotspots: Identified {len(emerging_hotspots)} rapidly growing districts")
        print(f"✓ Future Fraud Risks: Flagged {len(future_fraud_risks)} high-risk districts\n")
        
        return self.forecasts
