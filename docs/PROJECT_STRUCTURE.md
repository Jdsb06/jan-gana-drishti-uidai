# 📁 Jan-Gana-Drishti - Project Structure

**Team ID:** UIDAI_2401  
**Live Dashboard:** [jan-gana-drishti-uidai-02.streamlit.app](https://jan-gana-drishti-uidai-02.streamlit.app/)  
**GitHub:** [github.com/Jdsb06/jan-gana-drishti-uidai](https://github.com/Jdsb06/jan-gana-drishti-uidai)

---

## 🗂️ Directory Organization

```
jan-gana-drishti/
│
├── 📄 README.md                          # Main project documentation
├── 📄 LICENSE                            # MIT License
├── 📄 requirements.txt                   # Python dependencies
├── 📄 packages.txt                       # System packages for deployment
├── 📄 UIDAI_2401_Report.pdf              # 54-page hackathon submission (440KB)
│
├── 🐍 app.py                             # Main Streamlit dashboard (93KB)
│
├── 🔧 run_dashboard.sh                   # Quick launch script
├── 🔧 prepare_cloud_deployment.sh        # Cloud deployment preparation
│
├── 📊 modules/                           # Analytics engines (7 modules)
│   ├── __init__.py                       # Package initialization
│   ├── etl_pipeline.py                   # Data loading, cleaning, fuzzy matching
│   ├── fraud_detection.py                # Ghost Hunter (Benford + Isolation Forest)
│   ├── migration_tracker.py             # Population movement analysis
│   ├── child_welfare.py                  # MBU compliance monitoring
│   ├── policy_impact.py                  # ROI calculators
│   ├── forecasting.py                    # 6-month predictions
│   ├── benchmarking.py                   # State performance indices
│   └── __pycache__/                      # Python bytecode cache
│
├── 💾 data/                              # Aadhaar datasets (5M+ records)
│   ├── api_data_aadhar_biometric/        # 1.86M records (4 CSV files)
│   ├── api_data_aadhar_demographic/      # 2.07M records (5 CSV files)
│   └── api_data_aadhar_enrolment/        # 1.01M records (3 CSV files)
│
├── 📚 docs/                              # Comprehensive documentation
│   ├── README.md                         # Documentation index (YOU ARE HERE)
│   ├── QUICK_START.md                    # Installation and setup guide
│   ├── DATASET_ANALYSIS.md               # Data quality and structure analysis
│   ├── CLOUD_DEPLOYMENT_GUIDE.md         # Multi-cloud deployment instructions
│   ├── API.md                            # API documentation
│   ├── CONTRIBUTING.md                   # Contribution guidelines
│   ├── SUBMISSION.md                     # Hackathon submission details
│   ├── SUBMISSION_CHECKLIST.md           # Requirements verification
│   └── QUICK_REFERENCE.md                # Single-page quick reference
│
├── 📝 report/                            # Hackathon submission materials
│   ├── README.md                         # Report documentation
│   ├── submission.pdf                    # 54-page submission document (440KB)
│   ├── submission.tex                    # LaTeX source (1439 lines)
│   └── code_snippets/                    # Python module source code
│
├── 🛠️ scripts/                           # Utility and development scripts
│   ├── README.md                         # Scripts documentation
│   ├── verify_installation.py            # Installation verification
│   ├── test_fix.py                       # Module testing
│   ├── main.py                           # Data exploration script
│   ├── upload_data_to_github.py          # Git LFS helper
│   └── show_submission.sh                # Submission info display
│
└── 🔬 research/                          # Project research and planning
    ├── 1.txt                             # Strategic framework documentation
    └── 2.txt                             # Analytical methodology research

```

---

## 📋 File Categories

### Core Application Files (Root)
- `app.py` - Main Streamlit dashboard application
- `UIDAI_2401_Report.pdf` - 54-page hackathon submission document (440KB)
- `requirements.txt` - Python package dependencies
- `packages.txt` - System-level dependencies for cloud deployment
- `run_dashboard.sh` - Quick launch script for local development
- `prepare_cloud_deployment.sh` - Prepares project for cloud deployment

### Analytics Modules (`modules/`)
Seven specialized Python modules implementing the analytical engines:

1. **etl_pipeline.py** - Data loading, cleaning, fuzzy state name matching
2. **fraud_detection.py** - Benford's Law + Isolation Forest anomaly detection
3. **migration_tracker.py** - Geographic mobility analysis
4. **child_welfare.py** - Mandatory Biometric Update (MBU) compliance tracking
5. **policy_impact.py** - Policy ROI calculators and impact simulation
6. **forecasting.py** - Time series forecasting (6-month ahead predictions)
7. **benchmarking.py** - State-wise performance ranking and comparison

### Data Files (`data/`)
Aadhaar transaction datasets totaling **5,068,837 records**:

- **Biometric:** 1,861,108 records (4 files)
- **Demographic:** 2,071,700 records (5 files)
- **Enrolment:** 1,006,029 records (3 files)

**Coverage:** March 2025 - December 2025 (10 months)  
**Geographic Span:** 800+ districts across India

### Documentation (`docs/`)
Complete documentation suite organized by audience:

**For Developers:**
- QUICK_START.md - Get up and running
- CLOUD_DEPLOYMENT_GUIDE.md - Deploy to production
- API.md - API reference
- CONTRIBUTING.md - Contribution guidelines

**For Evaluators:**
- SUBMISSION.md - Hackathon submission details
- SUBMISSION_CHECKLIST.md - Requirements verification
- QUICK_REFERENCE.md - Single-page overview

**For Analysts:**
- DATASET_ANALYSIS.md - Data quality deep dive

### Submission Materials (`report/`)
Official hackathon submission package:

- `submission.pdf` - 54-page comprehensive document (440KB)
- `submission.tex` - LaTeX source code (1439 lines)
- `code_snippets/` - Full Python module implementations

**Sections:**
1. Executive Summary
2. Problem Statement
3. Datasets Documentation
4. Methodology
5. Analysis & Findings
6. Code Listings
7. References

### Utility Scripts (`scripts/`)
Development and maintenance tools:

- `verify_installation.py` - Check dependencies and data integrity
- `test_fix.py` - Test fraud detection module
- `main.py` - Quick data exploration
- `show_submission.sh` - Display submission details
- `upload_data_to_github.py` - Git LFS helper

---

## 🎯 Quick Access

### For First-Time Users
1. Read [README.md](README.md)
2. Follow [docs/QUICK_START.md](docs/QUICK_START.md)
3. Run `./run_dashboard.sh`

### For Evaluators
1. Open [UIDAI_2401_Report.pdf](../UIDAI_2401_Report.pdf)
2. Visit [Live Dashboard](https://jan-gana-drishti-uidai-02.streamlit.app/)
3. Explore the codebase and [analytics modules](../modules/)

### For Contributors
1. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)
2. Check [docs/API.md](docs/API.md)
3. Review module structure in `modules/`

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Total Records Analyzed** | 5,068,837 |
| **Python Modules** | 7 analytics engines |
| **Documentation Files** | 9 markdown files |
| **Submission PDF** | 54 pages |
| **Code Lines (app.py)** | ~2,800 lines |
| **Geographic Coverage** | 800+ districts |
| **Time Period** | 10 months (Mar-Dec 2025) |
| **Team ID** | UIDAI_2401 |

---

## 🔗 External Links

- **Live Dashboard:** [jan-gana-drishti-uidai-02.streamlit.app](https://jan-gana-drishti-uidai-02.streamlit.app/)
- **GitHub Repository:** [github.com/Jdsb06/jan-gana-drishti-uidai](https://github.com/Jdsb06/jan-gana-drishti-uidai)
- **Submission PDF:** [../UIDAI_2401_Report.pdf](../UIDAI_2401_Report.pdf)

---

## 🏆 Hackathon Details

**Challenge:** UIDAI Analytics Challenge 2026  
**Team ID:** UIDAI_2401  
**Project Name:** Jan-Gana-Drishti (*जन-गण-दृष्टि*)  
**Submission Date:** January 20, 2026  
**Status:** ✅ Complete and Submitted

---

**Jan-Gana-Drishti** (*जन-गण-दृष्टि*)  
*Predictive Governance Dashboard*  
Government of India - UIDAI Hackathon 2026

Jai Hind! 🇮🇳
