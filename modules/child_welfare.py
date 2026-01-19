"""
Module 4: Missing Middle (Child Welfare Analysis)
Identifies districts where children are not updating biometrics
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


class ChildWelfareAnalyzer:
    """
    Analyzes child biometric update patterns to identify:
    - Districts with low Mandatory Biometric Updates (MBU) for children
    - "Red Districts" where children may lose access to welfare schemes
    """
    
    def __init__(self, data):
        self.data = data.copy()
        self.district_scores = None
        
    def calculate_child_welfare_metrics(self):
        """
        Calculate child biometric update metrics for each district
        """
        print("\n" + "="*80)
        print("MODULE 4: MISSING MIDDLE (Child Welfare Analysis)")
        print("="*80 + "\n")
        
        print("Analyzing Child Biometric Update Patterns...\n")
        
        # Aggregate by district
        district_summary = self.data.groupby(['state', 'district']).agg({
            'bio_age_5_17': 'sum',           # Actual biometric updates (5-17 years)
            'enrol_age_5_17': 'sum',         # New enrolments (5-17 years)
            'demo_age_5_17': 'sum',          # Demographic updates (5-17 years)
            'bio_age_17_plus': 'sum',        # Adult biometric (for comparison)
            'enrol_age_18_plus': 'sum',      # Adult enrolment (for comparison)
            'total_enrolment': 'sum'
        }).reset_index()
        
        # Calculate metrics
        
        # 1. Child MBU Rate (Mandatory Biometric Updates - as percentage of total child activity)
        # Formula: Child biometric updates / (Child bio + child demo + child enrolments) * 100
        # This shows what percentage of child interactions are biometric updates
        district_summary['total_child_activity'] = (
            district_summary['bio_age_5_17'] + 
            district_summary['demo_age_5_17'] + 
            district_summary['enrol_age_5_17']
        )
        
        district_summary['child_mbu_rate'] = (
            district_summary['bio_age_5_17'] / 
            (district_summary['total_child_activity'] + 1) * 100
        )
        
        # 2. Adult MBU Rate (for comparison - adults should have higher rates)
        district_summary['total_adult_activity'] = (
            district_summary['bio_age_17_plus'] + 
            district_summary['enrol_age_18_plus']
        )
        
        district_summary['adult_mbu_rate'] = (
            district_summary['bio_age_17_plus'] / 
            (district_summary['total_adult_activity'] + 1) * 100
        )
        
        # 3. MBU Gap (Adult - Child rate)
        # Large positive gap = children lagging behind adults
        district_summary['mbu_gap'] = (
            district_summary['adult_mbu_rate'] - 
            district_summary['child_mbu_rate']
        )
        
        # 4. Child Engagement Score (Total child interactions)
        district_summary['child_engagement'] = (
            district_summary['bio_age_5_17'] + 
            district_summary['demo_age_5_17']
        )
        
        # 5. Expected vs Actual MBU
        # Use median child MBU rate as baseline "expected" rate
        median_mbu = district_summary['child_mbu_rate'].median()
        district_summary['expected_child_mbu'] = (
            district_summary['total_child_activity'] * (median_mbu / 100)
        )
        
        district_summary['mbu_shortfall'] = (
            district_summary['expected_child_mbu'] - 
            district_summary['bio_age_5_17']
        )
        
        # Calculate percentile rank (lower rank = worse performance)
        # For districts with same child_mbu_rate, use mbu_shortfall as tiebreaker
        # Sort by child_mbu_rate (ascending), then by mbu_shortfall (descending)
        district_summary = district_summary.sort_values(['child_mbu_rate', 'mbu_shortfall'], 
                                                        ascending=[True, False])
        # Assign rank based on this sorted order
        district_summary['child_mbu_percentile'] = (
            pd.Series(range(1, len(district_summary) + 1), index=district_summary.index) / 
            len(district_summary) * 100
        )
        
        # Risk Classification
        def classify_risk(row):
            if row['child_mbu_percentile'] < 20 and row['mbu_shortfall'] > 100:
                return "CRITICAL RISK"
            elif row['child_mbu_percentile'] < 40:
                return "HIGH RISK"
            elif row['child_mbu_percentile'] < 60:
                return "MODERATE RISK"
            else:
                return "LOW RISK"
        
        district_summary['welfare_risk'] = district_summary.apply(classify_risk, axis=1)
        
        # Sort by risk (worst first)
        district_summary = district_summary.sort_values('child_mbu_percentile')
        
        self.district_scores = district_summary
        
        # Summary Statistics
        critical = len(district_summary[district_summary['welfare_risk'] == 'CRITICAL RISK'])
        high = len(district_summary[district_summary['welfare_risk'] == 'HIGH RISK'])
        moderate = len(district_summary[district_summary['welfare_risk'] == 'MODERATE RISK'])
        low = len(district_summary[district_summary['welfare_risk'] == 'LOW RISK'])
        
        print(f"📊 Child Welfare Analysis Results:")
        print(f"  ✓ Districts Analyzed: {len(district_summary)}")
        print(f"  🚨 CRITICAL RISK: {critical} districts")
        print(f"  ⚠️  HIGH RISK: {high} districts")
        print(f"  ⚡ MODERATE RISK: {moderate} districts")
        print(f"  ✅ LOW RISK: {low} districts")
        print(f"\n  📌 Median Child MBU Rate: {median_mbu:.1f}%")
        print(f"  📌 Total Children at Risk: {district_summary[district_summary['welfare_risk'].isin(['CRITICAL RISK', 'HIGH RISK'])]['mbu_shortfall'].sum():,.0f}\n")
        
        return district_summary
    
    def get_red_districts(self, n=20):
        """
        Identify "Red Districts" with lowest child MBU rates
        """
        if self.district_scores is None:
            print("⚠️  Run calculate_child_welfare_metrics() first!")
            return None
        
        print("\n" + "="*80)
        print(f"🚨 TOP {n} RED DISTRICTS (Lowest Child Biometric Updates)")
        print("="*80)
        print("These districts have children at risk of losing access to:")
        print("  • School Mid-Day Meals (MDM)")
        print("  • Scholarship Programs")
        print("  • Healthcare Benefits")
        print("  • PDS Rations\n")
        print("-" * 80 + "\n")
        
        red_districts = self.district_scores.head(n)
        
        for idx, row in red_districts.iterrows():
            risk_icon = "🔴" if row['welfare_risk'] == "CRITICAL RISK" else "🟠"
            print(f"{risk_icon} {row['district']}, {row['state']}")
            print(f"   Child MBU Rate: {row['child_mbu_rate']:.1f}% (Percentile: {row['child_mbu_percentile']:.0f})")
            print(f"   Missing Updates: {row['mbu_shortfall']:,.0f} children")
            print(f"   Adult MBU Rate: {row['adult_mbu_rate']:.1f}% (Gap: {row['mbu_gap']:.1f}%)")
            print(f"   Risk Level: {row['welfare_risk']}\n")
        
        return red_districts
    
    def compare_child_adult_patterns(self):
        """
        Compare child vs adult biometric update patterns
        """
        print("\n" + "="*80)
        print("👶 vs 👨 CHILD-ADULT COMPARISON")
        print("="*80 + "\n")
        
        if self.district_scores is None:
            print("⚠️  Run calculate_child_welfare_metrics() first!")
            return None
        
        # Overall statistics
        total_child_mbu = self.district_scores['bio_age_5_17'].sum()
        total_adult_mbu = self.district_scores['bio_age_17_plus'].sum()
        
        avg_child_rate = self.district_scores['child_mbu_rate'].mean()
        avg_adult_rate = self.district_scores['adult_mbu_rate'].mean()
        
        print(f"National Level Statistics:")
        print(f"  👶 Total Child MBUs (5-17 years): {total_child_mbu:,}")
        print(f"  👨 Total Adult MBUs (17+ years): {total_adult_mbu:,}")
        print(f"\n  📊 Average Child MBU Rate: {avg_child_rate:.1f}%")
        print(f"  📊 Average Adult MBU Rate: {avg_adult_rate:.1f}%")
        print(f"  📊 Gap (Adult - Child): {avg_adult_rate - avg_child_rate:.1f}%\n")
        
        # Districts with largest gap
        large_gap = self.district_scores.nlargest(10, 'mbu_gap')
        
        print(f"Top 10 Districts with Largest Adult-Child MBU Gap:")
        print("(Children severely lagging behind adults)\n")
        
        for idx, row in large_gap.iterrows():
            print(f"📍 {row['district']}, {row['state']}")
            print(f"   Child: {row['child_mbu_rate']:.1f}% | Adult: {row['adult_mbu_rate']:.1f}% | Gap: {row['mbu_gap']:.1f}%\n")
        
        return large_gap
    
    def identify_intervention_priorities(self):
        """
        Prioritize districts for immediate intervention
        """
        print("\n" + "="*80)
        print("🎯 INTERVENTION PRIORITY MATRIX")
        print("="*80 + "\n")
        
        if self.district_scores is None:
            print("⚠️  Run calculate_child_welfare_metrics() first!")
            return None
        
        # Priority score = Risk severity + Scale of impact
        self.district_scores['intervention_priority'] = (
            (100 - self.district_scores['child_mbu_percentile']) * 0.5 +  # Risk severity
            (self.district_scores['mbu_shortfall'] / 
             self.district_scores['mbu_shortfall'].max() * 100) * 0.5  # Scale
        )
        
        priority_districts = self.district_scores.nlargest(15, 'intervention_priority')
        
        print("Top 15 Districts Requiring IMMEDIATE Intervention:\n")
        print("-" * 80 + "\n")
        
        for rank, (idx, row) in enumerate(priority_districts.iterrows(), 1):
            print(f"#{rank} | {row['district']}, {row['state']}")
            print(f"     Priority Score: {row['intervention_priority']:.1f}")
            print(f"     Risk: {row['welfare_risk']}")
            print(f"     Children Affected: {row['mbu_shortfall']:,.0f}")
            print(f"     Recommended Action: Mobile Biometric Camp + Awareness Drive\n")
        
        return priority_districts
    
    def analyze_temporal_trends(self):
        """
        Analyze child MBU trends over time
        """
        print("\n" + "="*80)
        print("📅 TEMPORAL TRENDS (Child Welfare)")
        print("="*80 + "\n")
        
        # Monthly aggregation
        monthly = self.data.groupby('month_year').agg({
            'bio_age_5_17': 'sum',
            'enrol_age_5_17': 'sum'
        }).reset_index()
        
        monthly['child_mbu_rate'] = (
            monthly['bio_age_5_17'] / 
            (monthly['enrol_age_5_17'] + 1) * 100
        )
        
        print("Month-wise Child MBU Activity:\n")
        for idx, row in monthly.iterrows():
            print(f"{row['month_year']}: {row['bio_age_5_17']:>10,} updates "
                  f"| MBU Rate: {row['child_mbu_rate']:>6.1f}%")
        
        # Identify concerning trends
        if monthly['child_mbu_rate'].iloc[-1] < monthly['child_mbu_rate'].iloc[0]:
            print(f"\n⚠️  WARNING: Child MBU rate DECLINING over time!")
            print(f"   March: {monthly['child_mbu_rate'].iloc[0]:.1f}% → December: {monthly['child_mbu_rate'].iloc[-1]:.1f}%")
        else:
            print(f"\n✅ POSITIVE: Child MBU rate improving over time")
        
        return monthly
    
    def run_full_analysis(self):
        """Execute complete child welfare analysis pipeline"""
        welfare_df = self.calculate_child_welfare_metrics()
        red_districts = self.get_red_districts(n=20)
        comparison = self.compare_child_adult_patterns()
        priorities = self.identify_intervention_priorities()
        temporal = self.analyze_temporal_trends()
        
        print("\n" + "="*80)
        print("✅ MODULE 4 COMPLETE: Child Welfare Analysis Done")
        print("="*80 + "\n")
        
        return {
            'district_scores': welfare_df,
            'red_districts': red_districts,
            'priorities': priorities,
            'temporal': temporal
        }
