"""
Module 7: Comparative Benchmarking Engine
Compares districts/states to identify best practices and laggards
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class BenchmarkingEngine:
    """
    Provides comparative analysis for:
    - State vs national average performance
    - District performance within states
    - Best practice identification
    - Laggard detection for targeted interventions
    """
    
    def __init__(self, data, fraud_results, migration_results, welfare_results):
        self.data = data.copy()
        self.fraud_results = fraud_results
        self.migration_results = migration_results
        self.welfare_results = welfare_results
        self.benchmarks = None
        
    def calculate_state_performance_index(self):
        """
        Create a composite performance index for each state
        """
        state_metrics = self.data.groupby('state').agg({
            'bio_age_17_plus': 'sum',
            'bio_age_5_17': 'sum',
            'demo_age_17_plus': 'sum',
            'demo_age_5_17': 'sum',
            'total_enrolment': 'sum',
            'enrol_age_18_plus': 'sum',
            'enrol_age_5_17': 'sum'
        }).reset_index()
        
        # Calculate performance metrics
        
        # 1. Biometric Update Rate (higher is better)
        state_metrics['bio_update_rate'] = (
            (state_metrics['bio_age_17_plus'] + state_metrics['bio_age_5_17']) /
            (state_metrics['total_enrolment'] + 1) * 100
        )
        
        # 2. Child Biometric Compliance (higher is better)
        state_metrics['child_bio_compliance'] = (
            state_metrics['bio_age_5_17'] /
            (state_metrics['enrol_age_5_17'] + 1) * 100
        )
        
        # 3. Demographic Update Activity (normalized)
        state_metrics['demo_activity_score'] = (
            (state_metrics['demo_age_17_plus'] + state_metrics['demo_age_5_17']) /
            (state_metrics['total_enrolment'] + 1) * 100
        )
        
        # 4. Adult Enrolment Ratio (should be moderate - not too high)
        state_metrics['adult_enrol_ratio'] = (
            state_metrics['enrol_age_18_plus'] /
            (state_metrics['total_enrolment'] + 1)
        )
        
        # Normalize scores (0-100 scale)
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler(feature_range=(0, 100))
        
        state_metrics['bio_score'] = scaler.fit_transform(state_metrics[['bio_update_rate']])
        state_metrics['child_score'] = scaler.fit_transform(state_metrics[['child_bio_compliance']])
        state_metrics['demo_score'] = scaler.fit_transform(state_metrics[['demo_activity_score']])
        
        # Adult ratio score (penalize extreme values)
        # Optimal ratio is around 0.6-0.7
        state_metrics['adult_ratio_deviation'] = np.abs(state_metrics['adult_enrol_ratio'] - 0.65)
        state_metrics['adult_score'] = 100 - scaler.fit_transform(state_metrics[['adult_ratio_deviation']])
        
        # Calculate composite index (weighted average)
        state_metrics['composite_index'] = (
            state_metrics['bio_score'] * 0.35 +
            state_metrics['child_score'] * 0.30 +
            state_metrics['demo_score'] * 0.20 +
            state_metrics['adult_score'] * 0.15
        ).round(1)
        
        # Rank states
        state_metrics['national_rank'] = state_metrics['composite_index'].rank(ascending=False, method='min')
        
        # Classify performance
        state_metrics['performance_tier'] = pd.cut(
            state_metrics['composite_index'],
            bins=[0, 40, 60, 80, 100],
            labels=['NEEDS IMPROVEMENT', 'AVERAGE', 'GOOD', 'EXCELLENT']
        )
        
        # Calculate national average
        national_avg = state_metrics['composite_index'].mean()
        state_metrics['vs_national_avg'] = (state_metrics['composite_index'] - national_avg).round(1)
        
        return state_metrics.sort_values('composite_index', ascending=False)
    
    def identify_best_practices(self):
        """
        Identify states/districts with exemplary performance
        """
        best_practices = []
        
        # 1. Best in Child Welfare
        welfare_scores = self.welfare_results['district_scores'].copy()
        # Use child_mbu_percentile as the score (already 0-100)
        welfare_scores['child_welfare_score'] = welfare_scores['child_mbu_percentile']
        
        top_child_welfare = welfare_scores.nlargest(5, 'child_welfare_score')
        
        for _, row in top_child_welfare.iterrows():
            best_practices.append({
                'category': 'Child Biometric Updates',
                'state': row['state'],
                'district': row['district'],
                'metric_value': round(row['child_mbu_rate'], 1),
                'metric_name': 'Child MBU Rate (%)',
                'why_exemplary': 'High child biometric update rates ensuring welfare access',
                'replicable_action': 'Mobile biometric update camps + school awareness programs'
            })
        
        # 2. Best in Migration Management
        migration_scores = self.migration_results['district_scores'].copy()
        stable_districts = migration_scores[migration_scores['migration_type'] == 'STABLE']
        
        # Find stable high-population districts
        # Check if 'total_enrolment' is already in migration_scores, otherwise merge
        if 'total_enrolment' in stable_districts.columns:
            top_stable = stable_districts.nlargest(3, 'total_enrolment')
        elif len(stable_districts) > 0:
            stable_with_data = stable_districts.merge(
                self.data.groupby(['state', 'district'])['total_enrolment'].sum().reset_index(),
                on=['state', 'district'],
                how='left'
            )
            top_stable = stable_with_data.nlargest(3, 'total_enrolment')
        else:
            top_stable = pd.DataFrame()  # No stable districts
        
        for _, row in top_stable.iterrows():
            best_practices.append({
                'category': 'Population Stability',
                'state': row['state'],
                'district': row['district'],
                'metric_value': round(row['migration_intensity'], 1),
                'metric_name': 'Migration Intensity Score',
                'why_exemplary': 'Low migration despite high population - good retention',
                'replicable_action': 'Study local economic/social factors for replication'
            })
        
        # 3. Best in Fraud Prevention (districts with clean patterns)
        fraud_clean = self.fraud_results['benford'][
            self.fraud_results['benford']['risk_level'] == 'LOW RISK'
        ]
        
        # Get high-enrolment clean districts
        if len(fraud_clean) > 0:
            fraud_clean_with_enrol = fraud_clean.merge(
                self.data.groupby(['state', 'district'])['total_enrolment'].sum().reset_index(),
                on=['state', 'district'],
                how='left'
            )
            
            top_clean = fraud_clean_with_enrol.nlargest(3, 'total_enrolment')
        else:
            top_clean = pd.DataFrame()  # No clean districts
        
        for _, row in top_clean.iterrows():
            best_practices.append({
                'category': 'Clean Enrolment Practices',
                'state': row['state'],
                'district': row['district'],
                'metric_value': round(row['benford_p_value'], 3),
                'metric_name': 'Benford P-Value',
                'why_exemplary': 'Natural enrolment patterns with no statistical anomalies',
                'replicable_action': 'Study enrolment verification processes and oversight mechanisms'
            })
        
        return pd.DataFrame(best_practices)
    
    def identify_laggards_for_intervention(self):
        """
        Identify states/districts needing urgent intervention
        """
        laggards = []
        
        # 1. Worst performers in state index
        state_index = self.calculate_state_performance_index()
        worst_states = state_index.nsmallest(5, 'composite_index')
        
        for _, row in worst_states.iterrows():
            laggards.append({
                'level': 'State',
                'state': row['state'],
                'district': 'All Districts',
                'issue': 'Overall Low Performance',
                'metric': 'Composite Index',
                'value': round(row['composite_index'], 1),
                'national_avg': round(state_index['composite_index'].mean(), 1),
                'gap': round(row['vs_national_avg'], 1),
                'recommended_action': 'Comprehensive system audit and capacity building'
            })
        
        # 2. Critical welfare laggards
        welfare_critical = self.welfare_results['district_scores'][
            self.welfare_results['district_scores']['welfare_risk'] == 'CRITICAL RISK'
        ].nsmallest(10, 'child_mbu_rate')
        
        for _, row in welfare_critical.iterrows():
            laggards.append({
                'level': 'District',
                'state': row['state'],
                'district': row['district'],
                'issue': 'Child Welfare Risk',
                'metric': 'Child MBU Rate (%)',
                'value': round(row['child_mbu_rate'], 1),
                'national_avg': 150.0,  # Expected rate
                'gap': round(row['child_mbu_rate'] - 150, 1),
                'recommended_action': 'Immediate MBU awareness campaign + mobile biometric camps'
            })
        
        # 3. Fraud high-risk districts
        if self.fraud_results['combined'] is not None and len(self.fraud_results['combined']) > 0:
            fraud_critical = self.fraud_results['combined'][
                self.fraud_results['combined']['dual_detection'] == True
            ].head(10)
            
            for _, row in fraud_critical.iterrows():
                laggards.append({
                    'level': 'District',
                    'state': row['state'],
                    'district': row['district'],
                    'issue': 'Fraud Risk',
                    'metric': 'Dual Anomaly Detection',
                    'value': 'POSITIVE',
                    'national_avg': 'NEGATIVE',
                    'gap': 'N/A',
                    'recommended_action': 'Urgent audit of enrolment processes and records'
                })
        
        return pd.DataFrame(laggards)
    
    def generate_peer_comparison_matrix(self, state_name):
        """
        Compare a specific state with its peers (similar population/geography)
        """
        state_index = self.calculate_state_performance_index()
        
        target_state = state_index[state_index['state'] == state_name]
        
        if len(target_state) == 0:
            return None
        
        # Find peer states (similar total enrolment)
        target_enrolment = target_state['total_enrolment'].values[0]
        
        # Get states within 30% of target enrolment
        state_index['enrolment_diff_pct'] = (
            np.abs(state_index['total_enrolment'] - target_enrolment) / target_enrolment * 100
        )
        
        peers = state_index[
            (state_index['enrolment_diff_pct'] < 30) &
            (state_index['state'] != state_name)
        ].nsmallest(5, 'enrolment_diff_pct')
        
        # Add target state to comparison
        comparison = pd.concat([target_state, peers])
        
        comparison['relative_position'] = comparison['composite_index'].rank(ascending=False, method='min')
        
        return comparison[['state', 'composite_index', 'bio_update_rate', 'child_bio_compliance',
                          'demo_activity_score', 'performance_tier', 'relative_position']]
    
    def calculate_district_rankings_within_state(self, state_name):
        """
        Rank all districts within a specific state
        """
        state_data = self.data[self.data['state'] == state_name]
        
        district_metrics = state_data.groupby('district').agg({
            'bio_age_17_plus': 'sum',
            'bio_age_5_17': 'sum',
            'demo_age_17_plus': 'sum',
            'total_enrolment': 'sum',
            'enrol_age_5_17': 'sum'
        }).reset_index()
        
        # Calculate metrics
        district_metrics['bio_rate'] = (
            (district_metrics['bio_age_17_plus'] + district_metrics['bio_age_5_17']) /
            (district_metrics['total_enrolment'] + 1) * 100
        )
        
        district_metrics['child_mbu_rate'] = (
            district_metrics['bio_age_5_17'] /
            (district_metrics['enrol_age_5_17'] + 1) * 100
        )
        
        district_metrics['demo_activity'] = (
            district_metrics['demo_age_17_plus'] /
            (district_metrics['total_enrolment'] + 1) * 100
        )
        
        # Simple composite score
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler(feature_range=(0, 100))
        
        district_metrics['composite_score'] = (
            scaler.fit_transform(district_metrics[['bio_rate']]) * 0.4 +
            scaler.fit_transform(district_metrics[['child_mbu_rate']]) * 0.4 +
            scaler.fit_transform(district_metrics[['demo_activity']]) * 0.2
        ).round(1)
        
        district_metrics['rank_in_state'] = district_metrics['composite_score'].rank(
            ascending=False, method='min'
        )
        
        return district_metrics.sort_values('composite_score', ascending=False)
    
    def run_full_analysis(self):
        """
        Run complete benchmarking analysis
        """
        print("\n" + "="*80)
        print("MODULE 7: COMPARATIVE BENCHMARKING ENGINE")
        print("="*80 + "\n")
        
        print("Generating Performance Benchmarks and Comparisons...\n")
        
        # Run all benchmarking components
        state_performance = self.calculate_state_performance_index()
        best_practices = self.identify_best_practices()
        laggards = self.identify_laggards_for_intervention()
        
        self.benchmarks = {
            'state_performance': state_performance,
            'best_practices': best_practices,
            'laggards': laggards
        }
        
        print(f"✓ State Performance Index: Calculated for {len(state_performance)} states")
        print(f"✓ Best Practices: Identified {len(best_practices)} exemplary cases")
        print(f"✓ Laggards: Flagged {len(laggards)} areas needing intervention\n")
        
        return self.benchmarks
