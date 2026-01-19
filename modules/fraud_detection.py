"""
Module 2: Ghost Hunter Engine (Fraud Detection)
Implements Benford's Law and Isolation Forest for fraud detection
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class GhostHunterEngine:
    """
    Fraud Detection Module using:
    1. Benford's Law (First Two Digits test)
    2. Isolation Forest (Anomaly Detection)
    """
    
    def __init__(self, data):
        self.data = data.copy()
        self.benford_results = None
        self.isolation_results = None
        
    @staticmethod
    def get_benfords_distribution():
        """
        Expected distribution for first two digits according to Benford's Law
        """
        digits = range(10, 100)
        expected = [np.log10(1 + 1/d) for d in digits]
        return digits, expected
    
    def calculate_first_two_digits(self, series):
        """Extract first two significant digits from a number"""
        def extract_digits(num):
            if pd.isna(num) or num <= 0:
                return None
            # Convert to string and extract first two digits
            str_num = str(int(num))
            if len(str_num) >= 2:
                return int(str_num[:2])
            elif len(str_num) == 1:
                return int(str_num[0] + '0')  # Pad single digit
            return None
        
        return series.apply(extract_digits)
    
    def benford_law_test(self, column='total_enrolment', group_by='district'):
        """
        Apply Benford's Law test on enrolment counts by district
        Returns districts with significant deviations (potential fraud)
        """
        print("\n" + "="*80)
        print("MODULE 2A: BENFORD'S LAW ANALYSIS (Ghost Enrolments)")
        print("="*80 + "\n")
        
        # Get expected Benford distribution
        expected_digits, expected_probs = self.get_benfords_distribution()
        
        results = []
        
        # Group by district and aggregate total enrolments
        district_totals = self.data.groupby(['state', group_by])[column].sum().reset_index()
        district_totals = district_totals[district_totals[column] > 0]
        
        print(f"Analyzing {len(district_totals)} districts for Benford's Law compliance...\n")
        
        for idx, row in district_totals.iterrows():
            state = row['state']
            district = row[group_by]
            total = row[column]
            
            # Get all transactions for this district
            district_data = self.data[
                (self.data['state'] == state) & 
                (self.data[group_by] == district)
            ][column]
            
            # Extract first two digits
            first_two = self.calculate_first_two_digits(district_data)
            first_two = first_two.dropna()
            
            # Need at least 5 data points (reduced from 10 for monthly aggregated data)
            if len(first_two) < 5:
                continue
            
            # Calculate observed distribution
            observed_counts = first_two.value_counts()
            observed_probs = observed_counts / len(first_two)
            
            # Chi-square test
            expected_counts = {}
            observed_aligned = {}
            
            for digit in expected_digits:
                expected_count = expected_probs[expected_digits.index(digit)] * len(first_two)
                expected_counts[digit] = expected_count
                observed_aligned[digit] = observed_counts.get(digit, 0)
            
            obs_array = np.array([observed_aligned[d] for d in expected_digits])
            exp_array = np.array([expected_counts[d] for d in expected_digits])
            
            # Chi-square statistic
            chi_square = np.sum((obs_array - exp_array)**2 / (exp_array + 1e-10))
            
            # Critical value at 95% confidence (df = 89 for 90 categories)
            critical_value = stats.chi2.ppf(0.95, df=89)
            
            # Determine risk level
            if chi_square > critical_value * 1.5:
                risk_level = "HIGH RISK"
            elif chi_square > critical_value:
                risk_level = "MODERATE RISK"
            else:
                risk_level = "COMPLIANT"
            
            results.append({
                'state': state,
                'district': district,
                'total_enrolment': total,
                'chi_square_stat': chi_square,
                'critical_value': critical_value,
                'deviation_factor': chi_square / critical_value,
                'risk_level': risk_level,
                'n_transactions': len(first_two)
            })
        
        # Create DataFrame with proper columns even if empty
        if results:
            self.benford_results = pd.DataFrame(results)
            self.benford_results = self.benford_results.sort_values('chi_square_stat', ascending=False)
        else:
            # Create empty DataFrame with expected columns
            self.benford_results = pd.DataFrame(columns=[
                'state', 'district', 'total_enrolment', 'chi_square_stat',
                'critical_value', 'deviation_factor', 'risk_level', 'n_transactions'
            ])
        
        # Summary statistics
        high_risk = len(self.benford_results[self.benford_results['risk_level'] == 'HIGH RISK'])
        moderate_risk = len(self.benford_results[self.benford_results['risk_level'] == 'MODERATE RISK'])
        
        print(f"📊 Benford's Law Results:")
        print(f"  ✓ Total Districts Analyzed: {len(self.benford_results)}")
        print(f"  ⚠️  HIGH RISK Districts: {high_risk} (Potential Ghost Enrolments)")
        print(f"  ⚡ MODERATE RISK Districts: {moderate_risk}")
        print(f"  ✅ COMPLIANT Districts: {len(self.benford_results) - high_risk - moderate_risk}\n")
        
        return self.benford_results
    
    def isolation_forest_anomalies(self, contamination=0.05):
        """
        Use Isolation Forest to detect anomalous adult enrolment patterns
        Adult enrolment should be rare (saturation >99%)
        """
        print("\n" + "="*80)
        print("MODULE 2B: ISOLATION FOREST ANALYSIS (Anomalous Adult Enrolments)")
        print("="*80 + "\n")
        
        # Aggregate by district (total across all months)
        district_summary = self.data.groupby(['state', 'district']).agg({
            'enrol_age_18_plus': 'sum',
            'enrol_age_5_17': 'sum',
            'enrol_age_0_5': 'sum',
            'bio_age_17_plus': 'sum',
            'demo_age_17_plus': 'sum'
        }).reset_index()
        
        # Calculate features
        district_summary['total_enrol'] = (district_summary['enrol_age_18_plus'] + 
                                           district_summary['enrol_age_5_17'] + 
                                           district_summary['enrol_age_0_5'])
        
        district_summary['adult_enrol_ratio'] = (
            district_summary['enrol_age_18_plus'] / 
            (district_summary['total_enrol'] + 1)
        )
        
        district_summary['adult_per_bio_update'] = (
            district_summary['enrol_age_18_plus'] / 
            (district_summary['bio_age_17_plus'] + 1)
        )
        
        # Features for anomaly detection
        features = ['enrol_age_18_plus', 'adult_enrol_ratio', 'adult_per_bio_update']
        X = district_summary[features].fillna(0)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train Isolation Forest
        print(f"Training Isolation Forest (contamination={contamination})...\n")
        iso_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        
        district_summary['anomaly'] = iso_forest.fit_predict(X_scaled)
        district_summary['anomaly_score'] = iso_forest.score_samples(X_scaled)
        
        # -1 = anomaly, 1 = normal
        district_summary['is_anomaly'] = district_summary['anomaly'] == -1
        
        # Sort by anomaly score (most anomalous first)
        district_summary = district_summary.sort_values('anomaly_score')
        
        self.isolation_results = district_summary
        
        # Summary
        anomalies = district_summary[district_summary['is_anomaly']]
        print(f"📊 Isolation Forest Results:")
        print(f"  ✓ Districts Analyzed: {len(district_summary)}")
        print(f"  ⚠️  ANOMALIES DETECTED: {len(anomalies)}")
        print(f"  💡 These districts show suspicious adult enrolment patterns")
        print(f"     (High adult enrolments despite 99%+ saturation)\n")
        
        return district_summary
    
    def get_top_fraud_suspects(self, n=20):
        """
        Combine both methods to identify top fraud suspects
        """
        print("\n" + "="*80)
        print("🎯 TOP FRAUD SUSPECTS (Combined Analysis)")
        print("="*80 + "\n")
        
        if self.benford_results is None or self.isolation_results is None:
            print("⚠️  Run both detection methods first!")
            return None
        
        # Check if we have results to merge
        if len(self.benford_results) == 0 or len(self.isolation_results) == 0:
            print("⚠️  No fraud suspects found (insufficient data for analysis)")
            # Return empty DataFrame with expected columns
            return pd.DataFrame(columns=[
                'state', 'district', 'total_enrolment', 'chi_square_stat',
                'critical_value', 'deviation_factor', 'risk_level', 'n_transactions',
                'is_anomaly', 'anomaly_score', 'risk_score', 'dual_detection'
            ])
        
        # Merge results
        merged = self.benford_results.merge(
            self.isolation_results[['state', 'district', 'is_anomaly', 'anomaly_score']],
            on=['state', 'district'],
            how='inner'
        )
        
        # Calculate composite risk score
        merged['risk_score'] = (
            merged['deviation_factor'] * 0.6 +  # Benford weight
            (1 - merged['anomaly_score']) * 0.4  # Isolation Forest weight (inverted)
        )
        
        # Add flag for dual detection
        merged['dual_detection'] = (
            (merged['risk_level'].isin(['HIGH RISK', 'MODERATE RISK'])) & 
            (merged['is_anomaly'])
        )
        
        top_suspects = merged.sort_values('risk_score', ascending=False).head(n)
        
        if len(top_suspects) > 0:
            print(f"Top {n} Districts with HIGHEST Fraud Risk:\n")
            for idx, row in top_suspects.iterrows():
                flag = "🔴 CRITICAL" if row['dual_detection'] else "⚠️  WARNING"
                print(f"{flag} | {row['district']}, {row['state']}")
                print(f"         Benford Risk: {row['risk_level']}")
                print(f"         Isolation Forest: {'ANOMALY' if row['is_anomaly'] else 'Normal'}")
                print(f"         Risk Score: {row['risk_score']:.2f}\n")
        else:
            print("No fraud suspects found after merging results.\n")
        
        return merged
    
    def run_full_analysis(self):
        """Execute complete fraud detection pipeline"""
        benford_df = self.benford_law_test()
        isolation_df = self.isolation_forest_anomalies()
        combined_df = self.get_top_fraud_suspects()
        
        print("="*80)
        print("✅ MODULE 2 COMPLETE: Fraud Detection Analysis Done")
        print("="*80 + "\n")
        
        return {
            'benford': benford_df,
            'isolation': isolation_df,
            'combined': combined_df
        }
