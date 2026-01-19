# Cloud Deployment Guide - Hosting Data Separately

## 🎯 Overview

Your app is **243MB** - mostly data. This guide shows how to host data separately and reduce deployment size to **~5MB**.

## 📊 Cost Comparison

| Option | Data Storage Cost | Bandwidth | Total/Month |
|--------|------------------|-----------|-------------|
| **GitHub Releases** | FREE | FREE | **$0** ✅ |
| AWS S3 | $0.023/GB ($0.06) | $0.09/GB | ~$0.50 |
| Google Cloud Storage | $0.020/GB ($0.05) | $0.12/GB | ~$0.80 |
| Cloudflare R2 | FREE (10GB) | FREE | **$0** ✅ |

**Recommendation:** GitHub Releases (best for hackathon/public data)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Compress Your Data

```bash
cd /home/jdsb/Desktop/BiULding/Hackathons/UIDAI
python3 upload_data_to_github.py
```

This creates `aadhaar_hackathon_data.zip` (~100-150MB compressed).

### Step 2: Upload to GitHub Release

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

2. Create a Release:
   - Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/releases/new`
   - Tag: `v1.0.0`
   - Title: `Data Release v1.0`
   - Upload: `aadhaar_hackathon_data.zip`
   - Click: **Publish release**

3. Copy the download URL (it will be):
   ```
   https://github.com/YOUR_USERNAME/YOUR_REPO/releases/download/v1.0.0/aadhaar_hackathon_data.zip
   ```

### Step 3: Update Your Code

Edit `modules/etl_pipeline_cloud.py` line 25:

```python
DATA_RELEASE_URL = "https://github.com/YOUR_USERNAME/YOUR_REPO/releases/download/v1.0.0/aadhaar_hackathon_data.zip"
```

Then run:
```bash
chmod +x prepare_cloud_deployment.sh
./prepare_cloud_deployment.sh
```

---

## 📦 Alternative Options

### Option A: Google Drive (No GitHub needed)

1. Upload `aadhaar_hackathon_data.zip` to Google Drive
2. Right-click → Share → Anyone with link
3. Get shareable link: `https://drive.google.com/file/d/FILE_ID/view`
4. Convert to direct download: 
   ```
   https://drive.google.com/uc?export=download&id=FILE_ID
   ```

### Option B: Dropbox

1. Upload to Dropbox
2. Get shareable link
3. Change `www.dropbox.com` → `dl.dropboxusercontent.com`
4. Change `?dl=0` → `?dl=1`

### Option C: AWS S3 (Best for Production)

```bash
# Install AWS CLI
pip install awscli

# Configure
aws configure

# Upload
aws s3 cp aadhaar_hackathon_data.zip s3://your-bucket/
aws s3 presign s3://your-bucket/aadhaar_hackathon_data.zip --expires-in 31536000

# Or make public
aws s3api put-object-acl --bucket your-bucket --key aadhaar_hackathon_data.zip --acl public-read
```

URL: `https://your-bucket.s3.amazonaws.com/aadhaar_hackathon_data.zip`

### Option D: Cloudflare R2 (No Egress Fees)

```bash
# Install Wrangler
npm install -g wrangler

# Login
wrangler login

# Create bucket
wrangler r2 bucket create aadhaar-data

# Upload
wrangler r2 object put aadhaar-data/aadhaar_hackathon_data.zip --file=aadhaar_hackathon_data.zip

# Make public via dashboard
```

---

## 🔄 Deployment Workflow

### Without Cloud Storage (Current)
```
Local Files (243MB)
    ↓
Git Push (243MB - SLOW)
    ↓
Streamlit Cloud (243MB - LIMITED MEMORY)
```

### With Cloud Storage (Optimized) ✅
```
Data (243MB) → GitHub Release (FREE)
Code (5MB) → Git Push (FAST)
    ↓
Streamlit Cloud (5MB - LOADS FROM CLOUD)
```

---

## ⚙️ How It Works

The updated `etl_pipeline_cloud.py` module:

1. **First Load:** Downloads ZIP from GitHub Release
2. **Caching:** Streamlit caches data in memory (TTL: 1 hour)
3. **Fallback:** If download fails, uses local files (for development)
4. **No Disk I/O:** Extracts ZIP directly to memory

### Performance

- **Initial Load:** 15-30 seconds (one-time download)
- **Subsequent Loads:** Instant (cached in memory)
- **Memory Usage:** Same as before (~243MB RAM)
- **Deployment Size:** 5MB (vs 243MB)

---

## 🎯 Deployment to Streamlit Cloud

### Before (Without Cloud Storage)
```bash
git add .
git push  # ❌ Uploads 243MB
# May fail due to memory limits
```

### After (With Cloud Storage)
```bash
# Exclude data folder
echo "data/" >> .gitignore

git add .
git commit -m "Use cloud storage for data"
git push  # ✅ Uploads only 5MB

# Deploy on Streamlit Cloud
# App downloads data from GitHub Release automatically
```

---

## 🔐 Security Considerations

### Public Data (Hackathon)
- ✅ GitHub Releases (perfect for public data)
- ✅ Google Drive public link
- ✅ S3 public bucket

### Sensitive Data (Government)
- ✅ S3 with IAM roles and presigned URLs
- ✅ Azure Blob with SAS tokens
- ✅ Private GitHub releases with token authentication
- ❌ Don't use public links

For sensitive data, update code to use authentication:

```python
import requests

response = requests.get(
    DATA_URL,
    headers={'Authorization': f'Bearer {os.getenv("DATA_TOKEN")}'}
)
```

---

## 📊 Testing Locally

Test cloud version before deployment:

```bash
# Use cloud storage
python3 -c "from modules.etl_pipeline_cloud import load_and_clean_data; load_and_clean_data(use_cloud=True)"

# Use local files
python3 -c "from modules.etl_pipeline_cloud import load_and_clean_data; load_and_clean_data(use_cloud=False)"
```

---

## 🐛 Troubleshooting

### Error: "requests module not found"
```bash
pip install requests
```

### Error: "Download failed"
Check URL is correct and publicly accessible:
```bash
curl -I YOUR_DATA_URL
# Should return: HTTP/1.1 200 OK
```

### Error: "Memory exceeded on Streamlit Cloud"
Reduce data size by sampling:
```python
# In upload_data_to_github.py, add sampling
df = pd.read_csv(file)
df_sampled = df.sample(frac=0.5, random_state=42)  # 50% sample
df_sampled.to_csv(output_file, index=False)
```

---

## ✅ Final Checklist

- [ ] Run `python3 upload_data_to_github.py`
- [ ] Upload ZIP to GitHub Release
- [ ] Copy download URL
- [ ] Update `DATA_RELEASE_URL` in `modules/etl_pipeline_cloud.py`
- [ ] Run `./prepare_cloud_deployment.sh`
- [ ] Test locally: `streamlit run app.py`
- [ ] Add `data/` to `.gitignore`
- [ ] Push to GitHub (only code, not data)
- [ ] Deploy to Streamlit Cloud
- [ ] Verify app loads data from cloud

---

## 💡 Pro Tips

1. **Version Control:** Update release tag when data changes (v1.0.0 → v1.1.0)
2. **Multiple Regions:** Host on multiple CDNs for redundancy
3. **Compression:** ZIP reduces size by ~40-60%
4. **Caching:** Set TTL higher (24 hours) for static data
5. **Monitoring:** Add logging to track download times

---

**Estimated Deployment Time:** 10 minutes  
**Cost Savings:** $0/month (vs $30-50/month for large deployments)  
**Performance:** Same or better (CDN distribution)
