"""
Module 3: Migration Pulse Tracker
Analyzes demographic and biometric patterns to detect migration flows
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


class MigrationPulseTracker:
    """
    Tracks inter-district migration patterns using:
    - Demographic Updates (Address changes) = In-Migration signal
    - Biometric Updates + Low Address Changes = Out-Migration signal
    """
    
    def __init__(self, data):
        self.data = data.copy()
        self.migration_scores = None
        
    def calculate_migration_metrics(self):
        """
        Calculate migration indicators for each district
        """
        print("\n" + "="*80)
        print("MODULE 3: MIGRATION PULSE TRACKER")
        print("="*80 + "\n")
        
        print("Analyzing Migration Patterns...\n")
        
        # Aggregate by district (sum across all months)
        district_summary = self.data.groupby(['state', 'district']).agg({
            'demo_age_17_plus': 'sum',      # Adult address changes
            'demo_age_5_17': 'sum',          # Child address changes
            'bio_age_17_plus': 'sum',        # Adult biometric auth
            'bio_age_5_17': 'sum',           # Child biometric auth
            'total_enrolment': 'sum'
        }).reset_index()
        
        # Calculate total demographic updates (address changes)
        district_summary['total_demo_updates'] = (
            district_summary['demo_age_17_plus'] + 
            district_summary['demo_age_5_17']
        )
        
        # Calculate total biometric authentications
        district_summary['total_bio_auth'] = (
            district_summary['bio_age_17_plus'] + 
            district_summary['bio_age_5_17']
        )
        
        # Migration Indicators
        
        # 1. In-Migration Score (High address updates = arrivals)
        # Normalized per 1000 biometric authentications
        district_summary['in_migration_score'] = (
            district_summary['total_demo_updates'] / 
            (district_summary['total_bio_auth'] + 1) * 1000
        )
        
        # 2. Out-Migration Score (High bio auth, low demo updates = departures)
        # Ratio of biometric to demographic
        district_summary['out_migration_score'] = (
            district_summary['total_bio_auth'] / 
            (district_summary['total_demo_updates'] + 1)
        )
        
        # Normalize out-migration score (cap at reasonable value)
        district_summary['out_migration_score'] = district_summary['out_migration_score'].clip(upper=10)
        
        # 3. Net Migration Score (Combined indicator)
        # Positive = In-Migration dominant, Negative = Out-Migration dominant
        district_summary['net_migration_score'] = (
            district_summary['in_migration_score'] - 
            district_summary['out_migration_score']
        )
        
        # 4. Migration Intensity (Total movement)
        district_summary['migration_intensity'] = (
            district_summary['in_migration_score'] + 
            district_summary['out_migration_score']
        )
        
        # Classify migration type
        def classify_migration(row):
            if row['in_migration_score'] > 20 and row['net_migration_score'] > 5:
                return "HIGH IN-MIGRATION"
            elif row['out_migration_score'] > 5 and row['net_migration_score'] < -2:
                return "HIGH OUT-MIGRATION"
            elif row['migration_intensity'] > 15:
                return "HIGH MOBILITY (Both)"
            else:
                return "STABLE"
        
        district_summary['migration_type'] = district_summary.apply(classify_migration, axis=1)
        
        # Sort by migration intensity
        district_summary = district_summary.sort_values('migration_intensity', ascending=False)
        
        self.migration_scores = district_summary
        
        # Summary Statistics
        in_migration = len(district_summary[district_summary['migration_type'] == 'HIGH IN-MIGRATION'])
        out_migration = len(district_summary[district_summary['migration_type'] == 'HIGH OUT-MIGRATION'])
        high_mobility = len(district_summary[district_summary['migration_type'] == 'HIGH MOBILITY (Both)'])
        stable = len(district_summary[district_summary['migration_type'] == 'STABLE'])
        
        print(f"📊 Migration Analysis Results:")
        print(f"  ✓ Districts Analyzed: {len(district_summary)}")
        print(f"  📈 HIGH IN-MIGRATION: {in_migration} districts")
        print(f"  📉 HIGH OUT-MIGRATION: {out_migration} districts")
        print(f"  🔄 HIGH MOBILITY: {high_mobility} districts")
        print(f"  ⚖️  STABLE: {stable} districts\n")
        
        return district_summary
    
    def get_top_migration_districts(self, migration_type='in', n=15):
        """
        Get top districts by migration type
        migration_type: 'in', 'out', or 'intensity'
        """
        if self.migration_scores is None:
            print("⚠️  Run calculate_migration_metrics() first!")
            return None
        
        if migration_type == 'in':
            top = self.migration_scores.nlargest(n, 'in_migration_score')
            print(f"\n🌍 TOP {n} IN-MIGRATION HOTSPOTS (People Arriving):\n")
            print("-" * 80)
            for idx, row in top.iterrows():
                print(f"📍 {row['district']}, {row['state']}")
                print(f"   In-Migration Score: {row['in_migration_score']:.1f}")
                print(f"   Address Updates: {row['total_demo_updates']:,}")
                print(f"   Type: {row['migration_type']}\n")
        
        elif migration_type == 'out':
            top = self.migration_scores.nlargest(n, 'out_migration_score')
            print(f"\n🌍 TOP {n} OUT-MIGRATION DISTRICTS (People Leaving):\n")
            print("-" * 80)
            for idx, row in top.iterrows():
                print(f"📍 {row['district']}, {row['state']}")
                print(f"   Out-Migration Score: {row['out_migration_score']:.1f}")
                print(f"   Biometric Auth: {row['total_bio_auth']:,}")
                print(f"   Type: {row['migration_type']}\n")
        
        else:  # intensity
            top = self.migration_scores.nlargest(n, 'migration_intensity')
            print(f"\n🌍 TOP {n} HIGH MOBILITY DISTRICTS (Most Movement):\n")
            print("-" * 80)
            for idx, row in top.iterrows():
                print(f"📍 {row['district']}, {row['state']}")
                print(f"   Migration Intensity: {row['migration_intensity']:.1f}")
                print(f"   Net Score: {row['net_migration_score']:.1f}")
                print(f"   Type: {row['migration_type']}\n")
        
        return top
    
    def get_migration_corridors(self):
        """
        Identify potential migration corridors (pairs of in/out districts in same state)
        """
        if self.migration_scores is None:
            print("⚠️  Run calculate_migration_metrics() first!")
            return None
        
        print("\n" + "="*80)
        print("🛤️  MIGRATION CORRIDORS (Within-State Flows)")
        print("="*80 + "\n")
        
        corridors = []
        
        for state in self.migration_scores['state'].unique():
            state_data = self.migration_scores[self.migration_scores['state'] == state]
            
            # Get top in-migration and out-migration districts in this state
            in_districts = state_data[state_data['migration_type'] == 'HIGH IN-MIGRATION']
            out_districts = state_data[state_data['migration_type'] == 'HIGH OUT-MIGRATION']
            
            if len(in_districts) > 0 and len(out_districts) > 0:
                corridors.append({
                    'state': state,
                    'in_districts': in_districts['district'].tolist(),
                    'out_districts': out_districts['district'].tolist(),
                    'n_in': len(in_districts),
                    'n_out': len(out_districts)
                })
        
        # Display corridors
        for corridor in corridors[:10]:  # Top 10 states
            print(f"🏛️  {corridor['state']}:")
            print(f"   ➡️  {corridor['n_out']} districts losing population: {', '.join(corridor['out_districts'][:3])}")
            print(f"   ⬅️  {corridor['n_in']} districts gaining population: {', '.join(corridor['in_districts'][:3])}\n")
        
        return corridors
    
    def analyze_temporal_trends(self):
        """
        Analyze migration trends over time (month by month)
        """
        print("\n" + "="*80)
        print("📅 TEMPORAL MIGRATION TRENDS")
        print("="*80 + "\n")
        
        # Monthly aggregation
        monthly_trends = self.data.groupby('month_year').agg({
            'demo_age_17_plus': 'sum',
            'demo_age_5_17': 'sum',
            'bio_age_17_plus': 'sum',
            'bio_age_5_17': 'sum'
        }).reset_index()
        
        monthly_trends['total_address_changes'] = (
            monthly_trends['demo_age_17_plus'] + 
            monthly_trends['demo_age_5_17']
        )
        
        monthly_trends['total_bio_auth'] = (
            monthly_trends['bio_age_17_plus'] + 
            monthly_trends['bio_age_5_17']
        )
        
        monthly_trends['mobility_ratio'] = (
            monthly_trends['total_address_changes'] / 
            (monthly_trends['total_bio_auth'] + 1) * 100
        )
        
        print("Month-wise Migration Activity:\n")
        for idx, row in monthly_trends.iterrows():
            print(f"{row['month_year']}: {row['total_address_changes']:>10,} address changes "
                  f"| Mobility Ratio: {row['mobility_ratio']:>6.2f}%")
        
        return monthly_trends
    
    def run_full_analysis(self):
        """Execute complete migration analysis pipeline"""
        migration_df = self.calculate_migration_metrics()
        
        # Get top districts
        self.get_top_migration_districts('in', n=10)
        self.get_top_migration_districts('out', n=10)
        
        # Get corridors
        self.get_migration_corridors()
        
        # Temporal trends
        temporal_df = self.analyze_temporal_trends()
        
        print("\n" + "="*80)
        print("✅ MODULE 3 COMPLETE: Migration Analysis Done")
        print("="*80 + "\n")
        
        return {
            'district_scores': migration_df,
            'temporal_trends': temporal_df
        }
