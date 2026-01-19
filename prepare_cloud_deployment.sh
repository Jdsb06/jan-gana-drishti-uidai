#!/bin/bash
# Deployment script for cloud-based data hosting
# This reduces app size from 243MB to ~5MB

echo "🚀 Preparing for cloud deployment..."
echo ""

# Step 1: Compress data
echo "Step 1: Compressing data..."
python3 upload_data_to_github.py
echo ""

# Step 2: Backup original ETL pipeline
echo "Step 2: Backing up original ETL pipeline..."
cp modules/etl_pipeline.py modules/etl_pipeline_local.py
echo "  ✓ Backup saved to modules/etl_pipeline_local.py"
echo ""

# Step 3: Switch to cloud version
echo "Step 3: Switching to cloud-based data loading..."
cp modules/etl_pipeline_cloud.py modules/etl_pipeline.py
echo "  ✓ Updated modules/etl_pipeline.py to use cloud storage"
echo ""

# Step 4: Create .gitignore for data folder
echo "Step 4: Creating .gitignore to exclude data folder..."
cat > .gitignore << 'EOF'
# Data folder (hosted separately)
data/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
ENV/
.venv
*.log

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Compiled/Build
*.pkl
*.joblib
dist/
build/
*.egg-info/

# Deployment
aadhaar_hackathon_data.zip
EOF
echo "  ✓ Created .gitignore (data/ folder will be excluded)"
echo ""

echo "✅ Setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Upload aadhaar_hackathon_data.zip to GitHub Release"
echo "2. Update DATA_RELEASE_URL in modules/etl_pipeline.py"
echo "3. Push code to GitHub (only ~5MB without data)"
echo "4. Deploy to Streamlit Cloud/Render"
echo ""
echo "📁 Your app size is now: $(du -sh . 2>/dev/null | cut -f1) (excluding data/)"
