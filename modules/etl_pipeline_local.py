"""
Module 1: Clean & Merge Pipeline (ETL)
Handles data loading, state name cleaning using fuzzy matching, and aggregation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from fuzzywuzzy import process, fuzz
import warnings
warnings.filterwarnings('ignore')


# Official LGD (Local Government Directory) State Names
OFFICIAL_STATE_NAMES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]


class AadhaarETLPipeline:
    """ETL Pipeline for Aadhaar datasets with fuzzy matching state name cleaning"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)
        self.biometric_df = None
        self.demographic_df = None
        self.enrolment_df = None
        self.merged_df = None
        self.state_mapping = {}
        
    def load_csv_files(self, pattern, dataset_name):
        """Load and concatenate multiple CSV files matching a pattern"""
        folder_path = self.data_dir / pattern
        csv_files = sorted(folder_path.glob('*.csv'))
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {folder_path}")
        
        print(f"Loading {dataset_name}: {len(csv_files)} file(s)")
        df_list = []
        
        for file in csv_files:
            df = pd.read_csv(file)
            df_list.append(df)
            print(f"  ✓ {file.name}: {len(df):,} records")
        
        combined_df = pd.concat(df_list, ignore_index=True)
        print(f"  Total {dataset_name} records: {len(combined_df):,}\n")
        
        return combined_df
    
    def clean_state_names_fuzzy(self, df, state_column='state'):
        """
        Clean state names using fuzzy matching (Levenshtein distance)
        Maps variations to official LGD names
        """
        print("🔧 Cleaning State Names with Fuzzy Matching...")
        
        unique_states = df[state_column].unique()
        print(f"  Found {len(unique_states)} unique state values (should be ≤36)")
        
        # Build mapping dictionary
        for dirty_state in unique_states:
            # Skip if already official
            if dirty_state in OFFICIAL_STATE_NAMES:
                self.state_mapping[dirty_state] = dirty_state
                continue
            
            # Handle obvious errors
            if str(dirty_state).isdigit() or dirty_state in ['100000']:
                self.state_mapping[dirty_state] = 'INVALID_ENTRY'
                continue
            
            # Find best match using fuzzy matching
            best_match, score = process.extractOne(
                str(dirty_state), 
                OFFICIAL_STATE_NAMES, 
                scorer=fuzz.token_sort_ratio
            )
            
            # Only accept matches with score > 75
            if score > 75:
                self.state_mapping[dirty_state] = best_match
            else:
                self.state_mapping[dirty_state] = 'UNKNOWN_STATE'
        
        # Apply mapping
        df[state_column] = df[state_column].map(self.state_mapping)
        
        # Remove invalid entries
        original_count = len(df)
        df = df[~df[state_column].isin(['INVALID_ENTRY', 'UNKNOWN_STATE'])]
        cleaned_count = len(df)
        
        print(f"  ✓ Standardized to {df[state_column].nunique()} states")
        print(f"  ✓ Removed {original_count - cleaned_count} invalid records\n")
        
        return df
    
    def clean_district_names(self, df, district_column='district'):
        """Standardize district names (title case, strip whitespace)"""
        df[district_column] = df[district_column].str.strip().str.title()
        return df
    
    def load_all_datasets(self):
        """Load all three datasets"""
        print("="*80)
        print("MODULE 1: CLEAN & MERGE PIPELINE (ETL)")
        print("="*80 + "\n")
        
        # Load datasets
        self.biometric_df = self.load_csv_files('api_data_aadhar_biometric', 'Biometric')
        self.demographic_df = self.load_csv_files('api_data_aadhar_demographic', 'Demographic')
        self.enrolment_df = self.load_csv_files('api_data_aadhar_enrolment', 'Enrolment')
        
        # Parse dates
        for df in [self.biometric_df, self.demographic_df, self.enrolment_df]:
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['month_year'] = df['date'].dt.to_period('M')
        
        return self
    
    def clean_all_datasets(self):
        """Clean state and district names in all datasets"""
        print("🧹 Cleaning State & District Names...")
        
        for name, df in [('Biometric', self.biometric_df), 
                         ('Demographic', self.demographic_df),
                         ('Enrolment', self.enrolment_df)]:
            print(f"\n{name} Dataset:")
            if df is not None:
                df = self.clean_state_names_fuzzy(df)
                df = self.clean_district_names(df)
                
                # Update the dataframe
                if name == 'Biometric':
                    self.biometric_df = df
                elif name == 'Demographic':
                    self.demographic_df = df
                else:
                    self.enrolment_df = df
        
        return self
    
    def aggregate_by_district_month(self):
        """Aggregate data at District-Month level"""
        print("\n📊 Aggregating Data at District-Month Level...\n")
        
        # Aggregate Biometric
        bio_agg = self.biometric_df.groupby(['state', 'district', 'month_year']).agg({
            'bio_age_5_17': 'sum',
            'bio_age_17_': 'sum'
        }).reset_index()
        bio_agg.columns = ['state', 'district', 'month_year', 'bio_age_5_17', 'bio_age_17_plus']
        print(f"  ✓ Biometric: {len(bio_agg):,} district-month records")
        
        # Aggregate Demographic
        demo_agg = self.demographic_df.groupby(['state', 'district', 'month_year']).agg({
            'demo_age_5_17': 'sum',
            'demo_age_17_': 'sum'
        }).reset_index()
        demo_agg.columns = ['state', 'district', 'month_year', 'demo_age_5_17', 'demo_age_17_plus']
        print(f"  ✓ Demographic: {len(demo_agg):,} district-month records")
        
        # Aggregate Enrolment
        enrol_agg = self.enrolment_df.groupby(['state', 'district', 'month_year']).agg({
            'age_0_5': 'sum',
            'age_5_17': 'sum',
            'age_18_greater': 'sum'
        }).reset_index()
        enrol_agg.columns = ['state', 'district', 'month_year', 
                            'enrol_age_0_5', 'enrol_age_5_17', 'enrol_age_18_plus']
        print(f"  ✓ Enrolment: {len(enrol_agg):,} district-month records")
        
        # Merge all datasets
        merged = bio_agg.merge(demo_agg, on=['state', 'district', 'month_year'], how='outer')
        merged = merged.merge(enrol_agg, on=['state', 'district', 'month_year'], how='outer')
        
        # Fill NaN with 0 (districts may not have all types of transactions)
        merged = merged.fillna(0)
        
        # Add total enrolment column
        merged['total_enrolment'] = (merged['enrol_age_0_5'] + 
                                     merged['enrol_age_5_17'] + 
                                     merged['enrol_age_18_plus'])
        
        self.merged_df = merged
        print(f"\n  ✓ MERGED Dataset: {len(merged):,} records")
        print(f"  ✓ States: {merged['state'].nunique()}")
        print(f"  ✓ Districts: {merged['district'].nunique()}")
        print(f"  ✓ Time Range: {merged['month_year'].min()} to {merged['month_year'].max()}\n")
        
        return merged
    
    def run_pipeline(self):
        """Execute the complete ETL pipeline"""
        self.load_all_datasets()
        self.clean_all_datasets()
        merged_data = self.aggregate_by_district_month()
        
        print("="*80)
        print("✅ MODULE 1 COMPLETE: Clean & Aggregated Data Ready")
        print("="*80 + "\n")
        
        return merged_data
    
    def get_state_mapping(self):
        """Return the state name mapping for reference"""
        return self.state_mapping


def load_and_clean_data():
    """
    Main entry point for ETL pipeline
    Returns cleaned and merged district-month level data
    """
    pipeline = AadhaarETLPipeline()
    return pipeline.run_pipeline(), pipeline
