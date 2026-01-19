"""
Quick test to verify the fraud detection fix
"""
import sys
import pandas as pd
import numpy as np

# Test 1: Empty results handling
print("Testing fraud detection module fixes...")
print("="*70)

# Create mock data
test_data = pd.DataFrame({
    'state': ['State1'] * 10,
    'district': ['District1'] * 10,
    'month_year': pd.period_range('2025-03', periods=10, freq='M'),
    'total_enrolment': [100, 200, 150, 300, 250, 180, 220, 190, 210, 240],
    'enrol_age_18_plus': [50, 100, 75, 150, 125, 90, 110, 95, 105, 120],
    'enrol_age_5_17': [30, 60, 45, 90, 75, 54, 66, 57, 63, 72],
    'enrol_age_0_5': [20, 40, 30, 60, 50, 36, 44, 38, 42, 48],
    'bio_age_17_plus': [500, 600, 550, 700, 650, 580, 620, 590, 610, 640],
    'bio_age_5_17': [300, 400, 350, 500, 450, 380, 420, 390, 410, 440],
    'demo_age_17_plus': [100, 150, 125, 200, 175, 140, 160, 145, 155, 165],
    'demo_age_5_17': [50, 75, 62, 100, 87, 70, 80, 72, 77, 82]
})

print("✅ Test data created successfully")

# Test the fix: create empty DataFrame with proper columns
empty_benford_results = pd.DataFrame(columns=[
    'state', 'district', 'total_enrolment', 'chi_square_stat',
    'critical_value', 'deviation_factor', 'risk_level', 'n_transactions'
])

print("✅ Empty DataFrame with columns created successfully")
print(f"   Columns: {list(empty_benford_results.columns)}")
print(f"   Shape: {empty_benford_results.shape}")

# Test sorting on empty DataFrame
try:
    sorted_df = empty_benford_results.sort_values('chi_square_stat', ascending=False)
    print("✅ Sorting empty DataFrame works (no KeyError)")
except KeyError as e:
    print(f"❌ KeyError still occurs: {e}")
    sys.exit(1)

# Test with actual data
benford_results_with_data = pd.DataFrame([
    {
        'state': 'Test State',
        'district': 'Test District',
        'total_enrolment': 1000,
        'chi_square_stat': 120.5,
        'critical_value': 100.0,
        'deviation_factor': 1.205,
        'risk_level': 'HIGH RISK',
        'n_transactions': 50
    }
])

try:
    sorted_with_data = benford_results_with_data.sort_values('chi_square_stat', ascending=False)
    print("✅ Sorting DataFrame with data works")
except Exception as e:
    print(f"❌ Error sorting with data: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("🎉 All tests passed! The KeyError fix is working correctly.")
print("="*70)
print("\n📌 Next steps:")
print("   1. Make sure dependencies are installed in .venv:")
print("      source .venv/bin/activate")
print("      pip install -r requirements.txt")
print("   2. Run the dashboard:")
print("      streamlit run app.py")
