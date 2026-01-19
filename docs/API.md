# API Documentation

## Overview

Jan-Gana-Drishti provides a modular architecture with well-defined interfaces for each analytical engine. This document outlines the available functions and their usage.

---

## Module 1: ETL Pipeline

### `load_and_clean_data()`

**Description**: Main entry point for data loading and cleaning pipeline.

**Returns**: 
- `merged_df` (DataFrame): Cleaned and aggregated district-month level data
- `pipeline` (AadhaarETLPipeline): Pipeline object with metadata

**Example**:
```python
from modules.etl_pipeline import load_and_clean_data

merged_data, pipeline = load_and_clean_data()
print(f"Loaded {len(merged_data)} district-month records")
```

### `AadhaarETLPipeline` Class

**Methods**:

#### `load_all_datasets()`
Loads biometric, demographic, and enrolment datasets from CSV files.

#### `clean_state_names_fuzzy(df, state_column='state')`
Standardizes state names using fuzzy matching.

**Parameters**:
- `df` (DataFrame): Input dataframe
- `state_column` (str): Column name containing state names

**Returns**: DataFrame with standardized state names

#### `aggregate_by_district_month()`
Aggregates data at district-month level.

**Returns**: DataFrame with merged biometric, demographic, and enrolment data

---

## Module 2: Fraud Detection

### `GhostHunterEngine` Class

#### `benford_law_test(df, column='total_enrolment')`

**Description**: Performs Benford's Law analysis on enrolment data.

**Parameters**:
- `df` (DataFrame): Input dataframe
- `column` (str): Column to analyze

**Returns**: DataFrame with:
- `state`, `district`
- `benford_deviation_factor`: Chi-square statistic / critical value
- `p_value`: Statistical significance
- `risk_level`: Classification (HIGH RISK, MODERATE, LOW)

**Example**:
```python
from modules.fraud_detection import GhostHunterEngine

engine = GhostHunterEngine(merged_data)
fraud_results = engine.benford_law_test()
high_risk = fraud_results[fraud_results['risk_level'] == 'HIGH RISK']
```

#### `isolation_forest_anomalies(contamination=0.05)`

**Description**: ML-based anomaly detection using Isolation Forest.

**Parameters**:
- `contamination` (float): Expected proportion of outliers (default: 0.05)

**Returns**: DataFrame with:
- `state`, `district`
- `anomaly`: -1 for anomalies, 1 for normal
- `anomaly_score`: Normalized anomaly score

#### `get_top_fraud_suspects(n=20, dual_method_only=False)`

**Description**: Get top fraud suspects combining both methods.

**Parameters**:
- `n` (int): Number of districts to return
- `dual_method_only` (bool): Only return districts flagged by both methods

**Returns**: DataFrame with combined risk scoring

---

## Module 3: Migration Tracker

### `MigrationPulseTracker` Class

#### `calculate_migration_metrics()`

**Description**: Calculates in-migration and out-migration scores.

**Returns**: DataFrame with:
- `state`, `district`
- `in_migration_score`: Demographic updates / biometric auth × 1000
- `out_migration_score`: Biometric auth / demographic updates
- `net_migration_score`: in_score - out_score
- `migration_intensity`: Combined migration activity

**Example**:
```python
from modules.migration_tracker import MigrationPulseTracker

tracker = MigrationPulseTracker(merged_data)
migration_data = tracker.calculate_migration_metrics()

# Get top in-migration districts
top_in = migration_data.nlargest(10, 'in_migration_score')
```

#### `analyze_temporal_trends(state=None, district=None)`

**Description**: Analyze migration patterns over time.

**Parameters**:
- `state` (str, optional): Filter by state
- `district` (str, optional): Filter by district

**Returns**: Time series data of migration scores

---

## Module 4: Child Welfare Analyzer

### `ChildWelfareAnalyzer` Class

#### `calculate_child_welfare_metrics()`

**Description**: Calculate child biometric update compliance metrics.

**Returns**: DataFrame with:
- `state`, `district`
- `child_mbu_rate`: Child biometric update rate (%)
- `adult_mbu_rate`: Adult biometric update rate (%)
- `mbu_gap`: Adult rate - Child rate
- `child_mbu_percentile`: National percentile ranking
- `risk_level`: CRITICAL/HIGH/MODERATE/LOW

**Example**:
```python
from modules.child_welfare import ChildWelfareAnalyzer

analyzer = ChildWelfareAnalyzer(merged_data)
welfare_data = analyzer.calculate_child_welfare_metrics()

# Get critical risk districts
critical = welfare_data[welfare_data['risk_level'] == 'CRITICAL RISK']
```

#### `get_red_districts(percentile_threshold=20)`

**Description**: Identify districts with lowest child MBU rates.

**Parameters**:
- `percentile_threshold` (int): Percentile cutoff (default: bottom 20%)

**Returns**: DataFrame of worst-performing districts

#### `identify_intervention_priorities()`

**Description**: Score districts for intervention priority.

**Returns**: DataFrame with priority scores and recommended actions

---

## Module 5: Policy Impact Engine

### `PolicyImpactEngine` Class

#### `simulate_fraud_intervention(high_risk_threshold=1.5)`

**Description**: Calculate ROI for fraud detection interventions.

**Parameters**:
- `high_risk_threshold` (float): Benford deviation threshold

**Returns**: Dict with:
- `total_high_risk_districts` (int)
- `estimated_fraud_enrolments` (int)
- `projected_annual_savings` (float)
- `audit_cost` (float)
- `net_savings` (float)
- `roi_percentage` (float)

**Example**:
```python
from modules.policy_impact import PolicyImpactEngine

engine = PolicyImpactEngine(merged_data, fraud_data, child_data, migration_data)
fraud_roi = engine.simulate_fraud_intervention()
print(f"Estimated savings: ₹{fraud_roi['projected_annual_savings']:,.0f}")
```

#### `simulate_welfare_intervention(risk_levels=['CRITICAL RISK', 'HIGH RISK'])`

**Description**: Calculate ROI for child welfare interventions.

**Parameters**:
- `risk_levels` (list): Risk levels to target

**Returns**: Dict with ROI metrics and intervention details

#### `generate_national_policy_recommendations()`

**Description**: Generate automated policy recommendations.

**Returns**: DataFrame with:
- `priority`: 1-5 ranking
- `policy_area`: Category
- `recommendation`: Action item
- `responsible_ministry`: Government department
- `timeline`: Implementation period
- `expected_impact`: Outcome description

---

## Module 6: Forecasting Engine

### `PredictiveForecastingEngine` Class

#### `forecast_state_enrolments(months_ahead=6)`

**Description**: Forecast state-level enrolments using linear regression.

**Parameters**:
- `months_ahead` (int): Forecast horizon in months

**Returns**: DataFrame with:
- `state`
- `current_avg`: Current monthly average
- `forecast_avg`: Predicted monthly average
- `growth_rate`: Percentage change
- `confidence_score`: Model R² score
- `trend`: Classification (RAPID/STEADY/SLOW/DECLINING)

**Example**:
```python
from modules.forecasting import PredictiveForecastingEngine

engine = PredictiveForecastingEngine(merged_data)
forecasts = engine.forecast_state_enrolments(months_ahead=6)
rapid_growth = forecasts[forecasts['trend'] == 'RAPID GROWTH']
```

#### `detect_seasonal_patterns()`

**Description**: Identify seasonal patterns in biometric updates.

**Returns**: DataFrame with peak months and volatility metrics

#### `identify_emerging_hotspots(growth_threshold=50, acceleration_threshold=20)`

**Description**: Detect rapidly growing districts.

**Parameters**:
- `growth_threshold` (float): Minimum growth rate (%)
- `acceleration_threshold` (float): Minimum acceleration (%)

**Returns**: DataFrame of emerging hotspot districts

---

## Module 7: Benchmarking Engine

### `BenchmarkingEngine` Class

#### `calculate_state_performance_index()`

**Description**: Calculate composite performance score (0-100).

**Returns**: DataFrame with:
- `state`
- `performance_index`: Composite score
- `national_rank`: 1-36 ranking
- `tier`: Performance classification
- Individual component scores

**Example**:
```python
from modules.benchmarking import BenchmarkingEngine

engine = BenchmarkingEngine(merged_data)
performance = engine.calculate_state_performance_index()
top_performers = performance[performance['tier'] == 'Excellent']
```

#### `identify_best_practices(top_n=10)`

**Description**: Identify exemplary districts for best practice replication.

**Parameters**:
- `top_n` (int): Number of districts to return per category

**Returns**: DataFrame with best practice examples and recommended actions

#### `identify_laggards_for_intervention(bottom_percentile=20)`

**Description**: Identify worst-performing districts needing intervention.

**Parameters**:
- `bottom_percentile` (int): Percentile threshold

**Returns**: DataFrame with intervention priorities

---

## Error Handling

All functions include error handling for common issues:

```python
try:
    merged_data, pipeline = load_and_clean_data()
except FileNotFoundError:
    print("Data files not found. Please check data/ directory structure.")
except Exception as e:
    print(f"Error loading data: {e}")
```

---

## Performance Optimization

### Caching

Streamlit caching is used for expensive operations:

```python
import streamlit as st

@st.cache_data
def load_and_clean_data():
    # Heavy processing cached
    ...
```

### Parallel Processing

For large datasets, consider parallel processing:

```python
from multiprocessing import Pool

def process_state(state_data):
    # Process individual state
    ...

with Pool() as pool:
    results = pool.map(process_state, state_groups)
```

---

## Configuration

### Environment Variables

```bash
# Optional: Set custom data directory
export UIDAI_DATA_DIR=/path/to/data

# Optional: Set cache TTL
export CACHE_TTL=3600
```

### Constants

Edit module files to adjust thresholds:

```python
# modules/fraud_detection.py
BENFORD_RISK_THRESHOLD = 1.5  # Adjust fraud sensitivity

# modules/child_welfare.py
CRITICAL_PERCENTILE = 20  # Adjust risk classification
```

---

## Testing

Unit tests for each module:

```bash
# Run all tests
python -m pytest tests/

# Test specific module
python -m pytest tests/test_fraud_detection.py
```

---

## Version History

**v1.0.0** (January 2026)
- Initial release
- 7 analytical modules
- Streamlit dashboard
- Cloud deployment support

---

## Support

For API issues or feature requests:
- GitHub Issues: [github.com/YOUR_USERNAME/jan-gana-drishti/issues]
- Email: support@nic.in
