# 🛠️ Utility Scripts

This folder contains development and maintenance scripts for the Jan-Gana-Drishti project.

---

## 📜 Scripts

### verify_installation.py
Verifies that all required Python packages are correctly installed and checks data file integrity.

**Usage:**
```bash
python scripts/verify_installation.py
```

**Checks:**
- Python version (3.8+)
- Required packages (pandas, streamlit, plotly, scikit-learn)
- Data file presence and structure
- Module imports

---

### test_fix.py
Tests fraud detection module fixes, specifically verifying empty result handling and proper column structure.

**Usage:**
```bash
python scripts/test_fix.py
```

**Tests:**
- Empty DataFrame handling
- Benford's Law implementation
- Isolation Forest anomaly detection
- Data preprocessing functions

---

### main.py
Simple data exploration script that loads sample CSV files and displays column information.

**Usage:**
```bash
python scripts/main.py
```

**Output:**
- Column names from each dataset
- Record counts
- Basic structure validation

---

### show_submission.sh
Displays hackathon submission information including Team ID, links, and PDF details.

**Usage:**
```bash
chmod +x scripts/show_submission.sh
./scripts/show_submission.sh
```

**Displays:**
- Team ID: UIDAI_2401
- Live dashboard URL
- GitHub repository link
- Submission PDF location and size
- Quick access commands

---

### upload_data_to_github.py
Helper script for preparing data files for GitHub upload with proper LFS configuration.

**Usage:**
```bash
python scripts/upload_data_to_github.py
```

**Note:** Large data files should use Git LFS to avoid repository bloat.

---

## 🔗 Related Documentation

- [Main README](../README.md) - Project overview
- [Quick Start Guide](../docs/QUICK_START.md) - Installation and setup
- [Documentation Index](../docs/README.md) - All documentation

---

**Jan-Gana-Drishti** (*जन-गण-दृष्टि*)  
Team ID: UIDAI_2401
