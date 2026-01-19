# Jan-Gana-Drishti Documentation

Welcome to the comprehensive documentation for **Jan-Gana-Drishti** (जन-गण-दृष्टि) - Predictive Governance Dashboard.

---

## 📚 Documentation Index

### Getting Started
- **[QUICK_START.md](QUICK_START.md)** - Installation, setup, and first steps
- **[DATASET_ANALYSIS.md](DATASET_ANALYSIS.md)** - Understanding the data structure and quality

### Deployment
- **[CLOUD_DEPLOYMENT_GUIDE.md](CLOUD_DEPLOYMENT_GUIDE.md)** - Deploy to Streamlit Cloud, AWS, Azure, and other platforms

### Development
- **[API.md](API.md)** - Complete API reference for all modules and functions
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributors

### Legal
- **[../LICENSE](../LICENSE)** - License terms and data protection policies

---

## 🎯 Quick Links

### For End Users
1. Start with [QUICK_START.md](QUICK_START.md) for installation
2. Review [DATASET_ANALYSIS.md](DATASET_ANALYSIS.md) to understand the data
3. Access the dashboard at `http://localhost:8501`

### For Developers
1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
2. Check [API.md](API.md) for function references
3. Follow code standards and testing requirements

### For DevOps/Deployment
1. Follow [CLOUD_DEPLOYMENT_GUIDE.md](CLOUD_DEPLOYMENT_GUIDE.md)
2. Choose deployment platform (Streamlit Cloud, AWS, Azure)
3. Set up CI/CD pipeline

---

## 📖 Documentation Structure

```
docs/
├── README.md                      # This file (documentation index)
├── QUICK_START.md                 # Installation and basic usage
├── DATASET_ANALYSIS.md            # Data structure and quality
├── CLOUD_DEPLOYMENT_GUIDE.md      # Deployment instructions
├── API.md                         # API reference
└── CONTRIBUTING.md                # Contribution guidelines
```

---

## 🔧 Module Documentation

### Core Modules

Each analytical module has detailed documentation within the code:

| Module | File | Purpose |
|--------|------|---------|
| **ETL Pipeline** | `modules/etl_pipeline.py` | Data loading, cleaning, and aggregation |
| **Fraud Detection** | `modules/fraud_detection.py` | Ghost Hunter Engine with Benford's Law and ML |
| **Migration Tracker** | `modules/migration_tracker.py` | Population movement analysis |
| **Child Welfare** | `modules/child_welfare.py` | MBU compliance monitoring |
| **Policy Impact** | `modules/policy_impact.py` | ROI simulation and recommendations |
| **Forecasting** | `modules/forecasting.py` | Predictive analytics |
| **Benchmarking** | `modules/benchmarking.py` | Performance comparison |

See [API.md](API.md) for detailed function signatures and usage examples.

---

## 🎓 Tutorials

### Tutorial 1: Running Your First Analysis

```python
# Load data
from modules.etl_pipeline import load_and_clean_data
merged_data, pipeline = load_and_clean_data()

# Run fraud detection
from modules.fraud_detection import GhostHunterEngine
engine = GhostHunterEngine(merged_data)
fraud_results = engine.benford_law_test()

# View high-risk districts
high_risk = fraud_results[fraud_results['risk_level'] == 'HIGH RISK']
print(high_risk[['state', 'district', 'benford_deviation_factor']])
```

### Tutorial 2: Migration Analysis

```python
# Load data
merged_data, pipeline = load_and_clean_data()

# Calculate migration metrics
from modules.migration_tracker import MigrationPulseTracker
tracker = MigrationPulseTracker(merged_data)
migration_data = tracker.calculate_migration_metrics()

# Find top in-migration districts
top_in_migration = migration_data.nlargest(10, 'in_migration_score')
print(top_in_migration[['state', 'district', 'in_migration_score']])
```

### Tutorial 3: Policy ROI Simulation

```python
# Load all data
merged_data, pipeline = load_and_clean_data()

# Run fraud and child welfare analysis first
from modules.fraud_detection import GhostHunterEngine
from modules.child_welfare import ChildWelfareAnalyzer

fraud_engine = GhostHunterEngine(merged_data)
fraud_data = fraud_engine.benford_law_test()

child_analyzer = ChildWelfareAnalyzer(merged_data)
child_data = child_analyzer.calculate_child_welfare_metrics()

# Calculate policy ROI
from modules.policy_impact import PolicyImpactEngine
policy_engine = PolicyImpactEngine(merged_data, fraud_data, child_data, None)
fraud_roi = policy_engine.simulate_fraud_intervention()

print(f"Projected annual savings: ₹{fraud_roi['projected_annual_savings']:,.0f}")
print(f"ROI: {fraud_roi['roi_percentage']:.1f}%")
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: "No module named 'modules'"
**Solution**: Ensure you're running from the project root directory.

```bash
cd /path/to/jan-gana-drishti
streamlit run app.py
```

#### Issue: "Data files not found"
**Solution**: Verify data directory structure:

```bash
ls -R data/
```

Should show:
- `data/api_data_aadhar_biometric/`
- `data/api_data_aadhar_demographic/`
- `data/api_data_aadhar_enrolment/`

#### Issue: "Memory error during data loading"
**Solution**: Reduce data size or increase system RAM. For testing, sample the data:

```python
# In modules/etl_pipeline.py, add sampling:
df = pd.read_csv(file).sample(frac=0.5, random_state=42)
```

#### Issue: "Streamlit won't start"
**Solution**: Check if port 8501 is available:

```bash
lsof -i :8501
streamlit run app.py --server.port=8502  # Use different port
```

---

## 📊 Performance Optimization

### Tips for Large Datasets

1. **Enable Caching**: Streamlit caching is already implemented
2. **Parallel Processing**: Use multiprocessing for heavy computations
3. **Data Sampling**: For development, use subset of data
4. **Database Backend**: For production, consider PostgreSQL/MongoDB

### Memory Management

```python
# Clear memory after heavy operations
import gc
gc.collect()

# Use categorical data types
df['state'] = df['state'].astype('category')
```

---

## 🔐 Security Best Practices

### Data Protection

1. **Never commit sensitive data** to version control
2. **Use environment variables** for credentials
3. **Enable HTTPS** in production
4. **Implement authentication** for public deployments
5. **Regular security audits** of dependencies

### Configuration

```bash
# .streamlit/secrets.toml (never commit this file)
[database]
user = "admin"
password = "secure_password"

# Access in code:
import streamlit as st
db_password = st.secrets["database"]["password"]
```

---

## 📧 Support

### Getting Help

- **Technical Issues**: Open a [GitHub Issue](https://github.com/YOUR_USERNAME/jan-gana-drishti/issues)
- **Feature Requests**: Use GitHub Discussions
- **Security Concerns**: Email security@nic.in
- **General Questions**: Check existing documentation first

### Community

- **GitHub Discussions**: Ask questions and share ideas
- **Issue Tracker**: Report bugs and track fixes
- **Pull Requests**: Contribute improvements

---

## 📝 Changelog

See project releases for detailed changelog:
- **v1.0.0** (January 2026): Initial release

---

## 🎯 Roadmap

Future enhancements planned:
- Real-time data integration
- Advanced ML models (LSTM, Prophet)
- Mobile responsive design
- Multi-language support (Hindi, regional languages)
- PDF report generation
- RESTful API endpoints

---

## 📚 External Resources

### Government References
- [UIDAI Official Website](https://uidai.gov.in/)
- [National Informatics Centre](https://www.nic.in/)
- [Digital India Portal](https://digitalindia.gov.in/)

### Technical Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [scikit-learn Documentation](https://scikit-learn.org/)

### Research Papers
- Benford's Law in Fraud Detection
- Isolation Forest for Anomaly Detection
- Time Series Forecasting Methods

---

## 🤝 Acknowledgments

This project would not be possible without:
- **UIDAI** for data access
- **NIC** for infrastructure support
- **Open Source Community** for amazing tools
- **Government Officials** for domain expertise

---

<div align="center">

### 🇮🇳 Documentation maintained with pride for Digital India 🇮🇳

[⬆ Back to Top](#jan-gana-drishti-documentation)

</div>
