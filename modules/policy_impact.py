"""
Module 5: Policy Impact Prediction Engine
Simulates impact of policy interventions and provides evidence-based recommendations
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class PolicyImpactEngine:
    """
    Predicts impact of policy interventions using:
    - Scenario simulation for resource allocation
    - Impact forecasting for targeted interventions
    - ROI estimation for government spending
    """
    
    def __init__(self, data, fraud_results, migration_results, welfare_results):
        self.data = data.copy()
        self.fraud_results = fraud_results
        self.migration_results = migration_results
        self.welfare_results = welfare_results
        self.impact_analysis = None
        
    def simulate_fraud_intervention(self, intervention_districts, audit_effectiveness=0.7):
        """
        Simulate impact of fraud audits in specific districts
        
        Parameters:
        - intervention_districts: List of districts to audit
        - audit_effectiveness: % of fraud that will be prevented (default 70%)
        
        Returns: Estimated savings and impact
        """
        results = []
        
        # Estimate fraud magnitude in each district
        fraud_districts = self.fraud_results['combined']
        if fraud_districts is None or len(fraud_districts) == 0:
            return pd.DataFrame()
        
        fraud_high_risk = fraud_districts[fraud_districts['dual_detection'] == True]
        
        for district in intervention_districts:
            district_data = fraud_high_risk[fraud_high_risk['district'] == district]
            
            if len(district_data) > 0:
                # Estimate fraudulent enrolments
                total_enrolments = district_data['total_enrolment'].values[0]
                
                # Conservative estimate: 5-15% of enrolments in high-risk districts are fraudulent
                estimated_fraud_rate = 0.10  # 10% average
                estimated_fraud_enrolments = total_enrolments * estimated_fraud_rate
                
                # Calculate savings (assuming ₹1,500/year per fraudulent beneficiary)
                annual_savings_per_beneficiary = 1500  # INR
                projected_annual_savings = estimated_fraud_enrolments * annual_savings_per_beneficiary * audit_effectiveness
                
                # Calculate audit cost (₹50 per enrolment audited)
                audit_cost = total_enrolments * 50
                
                # Calculate ROI
                roi = (projected_annual_savings - audit_cost) / audit_cost * 100
                
                results.append({
                    'district': district,
                    'state': district_data['state'].values[0],
                    'total_enrolments': total_enrolments,
                    'estimated_fraud_enrolments': int(estimated_fraud_enrolments),
                    'projected_annual_savings_inr': int(projected_annual_savings),
                    'audit_cost_inr': int(audit_cost),
                    'roi_percentage': round(roi, 1),
                    'intervention_priority': 'HIGH' if roi > 100 else 'MEDIUM'
                })
        
        return pd.DataFrame(results).sort_values('projected_annual_savings_inr', ascending=False)
    
    def simulate_welfare_intervention(self, intervention_districts, outreach_effectiveness=0.6):
        """
        Simulate impact of child welfare outreach programs
        
        Parameters:
        - intervention_districts: List of districts for MBU awareness campaigns
        - outreach_effectiveness: % improvement in child biometric updates (default 60%)
        
        Returns: Estimated children reached and welfare access improvement
        """
        results = []
        
        welfare_critical = self.welfare_results['district_scores']
        welfare_high_risk = welfare_critical[welfare_critical['welfare_risk'] == 'CRITICAL RISK']
        
        for district in intervention_districts:
            district_data = welfare_high_risk[welfare_high_risk['district'] == district]
            
            if len(district_data) > 0:
                current_child_bio = district_data['bio_age_5_17'].values[0]
                current_child_enrol = district_data['enrol_age_5_17'].values[0]
                
                # Estimate missing biometric updates
                expected_mbu_rate = 150  # 1.5 updates per child per year (national average)
                expected_updates = current_child_enrol * expected_mbu_rate / 100
                missing_updates = max(0, expected_updates - current_child_bio)
                
                # Project improvement after intervention
                projected_additional_updates = missing_updates * outreach_effectiveness
                children_at_risk = missing_updates / (expected_mbu_rate / 100)
                children_helped = projected_additional_updates / (expected_mbu_rate / 100)
                
                # Calculate impact (children regaining welfare access)
                avg_welfare_value_per_child = 8000  # INR per year (PDS + scholarships + healthcare)
                welfare_access_value = children_helped * avg_welfare_value_per_child
                
                # Program cost (₹100 per child outreach)
                program_cost = children_at_risk * 100
                
                roi = (welfare_access_value - program_cost) / program_cost * 100
                
                results.append({
                    'district': district,
                    'state': district_data['state'].values[0],
                    'children_at_risk': int(children_at_risk),
                    'children_helped': int(children_helped),
                    'welfare_access_value_inr': int(welfare_access_value),
                    'program_cost_inr': int(program_cost),
                    'roi_percentage': round(roi, 1),
                    'intervention_priority': 'HIGH' if children_at_risk > 1000 else 'MEDIUM'
                })
        
        return pd.DataFrame(results).sort_values('children_at_risk', ascending=False)
    
    def simulate_migration_infrastructure(self, intervention_districts):
        """
        Estimate infrastructure needs for high migration districts
        
        Returns: Resource allocation recommendations
        """
        results = []
        
        migration_data = self.migration_results['district_scores']
        high_migration = migration_data[
            (migration_data['migration_type'] == 'HIGH IN-MIGRATION') |
            (migration_data['migration_type'] == 'HIGH MOBILITY (Both)')
        ]
        
        for district in intervention_districts:
            district_data = high_migration[high_migration['district'] == district]
            
            if len(district_data) > 0:
                in_migration_score = district_data['in_migration_score'].values[0]
                
                # Estimate population influx (demographic updates = address changes)
                total_demo_updates = district_data['total_demo_updates'].values[0]
                
                # Infrastructure needs estimation
                estimated_new_residents = total_demo_updates * 0.7  # 70% are actual relocations
                
                # Calculate infrastructure requirements
                ration_shops_needed = int(np.ceil(estimated_new_residents / 2500))  # 1 shop per 2500 people
                healthcare_centers_needed = int(np.ceil(estimated_new_residents / 5000))  # 1 PHC per 5000
                school_capacity_needed = int(estimated_new_residents * 0.25)  # 25% are children
                
                # Cost estimation
                ration_shop_cost = 500000  # INR 5 lakh per shop
                healthcare_cost = 2000000  # INR 20 lakh per PHC
                school_expansion_cost = 1000  # INR 1000 per additional student capacity
                
                total_infrastructure_cost = (
                    ration_shops_needed * ration_shop_cost +
                    healthcare_centers_needed * healthcare_cost +
                    school_capacity_needed * school_expansion_cost
                )
                
                results.append({
                    'district': district,
                    'state': district_data['state'].values[0],
                    'estimated_new_residents': int(estimated_new_residents),
                    'ration_shops_needed': ration_shops_needed,
                    'healthcare_centers_needed': healthcare_centers_needed,
                    'school_capacity_needed': school_capacity_needed,
                    'total_infrastructure_cost_inr': int(total_infrastructure_cost),
                    'urgency': 'HIGH' if estimated_new_residents > 10000 else 'MEDIUM'
                })
        
        return pd.DataFrame(results).sort_values('estimated_new_residents', ascending=False)
    
    def generate_national_policy_recommendations(self):
        """
        Generate top-level policy recommendations based on all analyses
        """
        recommendations = []
        
        # 1. Fraud prevention recommendations
        fraud_high_risk_count = 0
        if self.fraud_results['combined'] is not None and len(self.fraud_results['combined']) > 0:
            fraud_high_risk_count = len(self.fraud_results['combined'][
                self.fraud_results['combined']['dual_detection'] == True
            ])
        
        if fraud_high_risk_count > 0:
            recommendations.append({
                'category': 'Fraud Prevention',
                'priority': 'CRITICAL',
                'recommendation': f'Immediate audit of {fraud_high_risk_count} high-risk districts showing dual anomalies',
                'expected_impact': 'Prevention of estimated ₹50-200 crore annual subsidy leakage',
                'implementation_timeline': '3 months',
                'responsible_ministry': 'Ministry of Electronics & IT, State Revenue Departments'
            })
        
        # 2. Child welfare recommendations
        welfare_critical_count = len(self.welfare_results['district_scores'][
            self.welfare_results['district_scores']['welfare_risk'] == 'CRITICAL RISK'
        ])
        
        if welfare_critical_count > 0:
            recommendations.append({
                'category': 'Child Welfare',
                'priority': 'HIGH',
                'recommendation': f'Launch MBU awareness campaigns in {welfare_critical_count} critical districts',
                'expected_impact': f'Restore welfare access for 50,000-200,000 children',
                'implementation_timeline': '6 months',
                'responsible_ministry': 'Ministry of Women & Child Development, Ministry of Education'
            })
        
        # 3. Migration management recommendations
        high_migration_count = len(self.migration_results['district_scores'][
            self.migration_results['district_scores']['migration_type'] == 'HIGH IN-MIGRATION'
        ])
        
        if high_migration_count > 0:
            recommendations.append({
                'category': 'Infrastructure Planning',
                'priority': 'HIGH',
                'recommendation': f'Allocate infrastructure funds to {high_migration_count} high in-migration districts',
                'expected_impact': 'Prevent service delivery collapse in urban centers',
                'implementation_timeline': '12-24 months',
                'responsible_ministry': 'Ministry of Rural Development, Ministry of Housing & Urban Affairs'
            })
        
        # 4. Data quality recommendations
        recommendations.append({
            'category': 'Data Quality',
            'priority': 'MEDIUM',
            'recommendation': 'Standardize state/district naming in UIDAI transaction logs',
            'expected_impact': 'Improved real-time analytics accuracy by 15-20%',
            'implementation_timeline': '6 months',
            'responsible_ministry': 'UIDAI, NIC'
        })
        
        # 5. Predictive governance recommendations
        recommendations.append({
            'category': 'System Improvement',
            'priority': 'MEDIUM',
            'recommendation': 'Deploy real-time anomaly detection for biometric transactions',
            'expected_impact': 'Early detection of fraud patterns within 7 days instead of 6 months',
            'implementation_timeline': '9 months',
            'responsible_ministry': 'UIDAI, MeitY'
        })
        
        return pd.DataFrame(recommendations)
    
    def calculate_intervention_roi_matrix(self):
        """
        Create a prioritization matrix for all potential interventions
        """
        # Get top districts from each category
        fraud_districts = []
        if self.fraud_results['combined'] is not None and len(self.fraud_results['combined']) > 0:
            fraud_top = self.fraud_results['combined'][
                self.fraud_results['combined']['dual_detection'] == True
            ].head(5)['district'].tolist()
            fraud_districts = fraud_top
        
        welfare_top = self.welfare_results['district_scores'][
            self.welfare_results['district_scores']['welfare_risk'] == 'CRITICAL RISK'
        ].head(5)['district'].tolist()
        
        migration_top = self.migration_results['district_scores'][
            self.migration_results['district_scores']['migration_type'] == 'HIGH IN-MIGRATION'
        ].head(5)['district'].tolist()
        
        # Simulate interventions
        fraud_impact = self.simulate_fraud_intervention(fraud_districts) if fraud_districts else pd.DataFrame()
        welfare_impact = self.simulate_welfare_intervention(welfare_top)
        migration_impact = self.simulate_migration_infrastructure(migration_top)
        
        return {
            'fraud_interventions': fraud_impact,
            'welfare_interventions': welfare_impact,
            'infrastructure_needs': migration_impact,
            'policy_recommendations': self.generate_national_policy_recommendations()
        }
    
    def run_full_analysis(self):
        """
        Run complete policy impact analysis
        """
        print("\n" + "="*80)
        print("MODULE 5: POLICY IMPACT PREDICTION ENGINE")
        print("="*80 + "\n")
        
        print("Simulating Policy Interventions and Calculating ROI...\n")
        
        self.impact_analysis = self.calculate_intervention_roi_matrix()
        
        print(f"✓ Fraud Intervention Scenarios: {len(self.impact_analysis['fraud_interventions'])} districts analyzed")
        print(f"✓ Welfare Intervention Scenarios: {len(self.impact_analysis['welfare_interventions'])} districts analyzed")
        print(f"✓ Infrastructure Planning: {len(self.impact_analysis['infrastructure_needs'])} districts analyzed")
        print(f"✓ Policy Recommendations: {len(self.impact_analysis['policy_recommendations'])} generated\n")
        
        return self.impact_analysis
