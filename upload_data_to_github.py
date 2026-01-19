#!/usr/bin/env python3
"""
Upload Data to GitHub Release
This script compresses your data and prepares it for GitHub Release upload
"""

import os
import zipfile
from pathlib import Path

def compress_data_folder():
    """Compress data folder into a single ZIP file"""
    print("🗜️  Compressing data folder...")
    
    data_dir = Path('data')
    zip_filename = 'aadhaar_hackathon_data.zip'
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start='.')
                    zipf.write(file_path, arcname)
                    print(f"  ✓ Added: {arcname}")
    
    file_size = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"\n✅ Created {zip_filename} ({file_size:.1f} MB)")
    print(f"\nNext steps:")
    print(f"1. Go to your GitHub repo")
    print(f"2. Click 'Releases' → 'Create a new release'")
    print(f"3. Tag: v1.0.0, Title: 'Data Release v1.0'")
    print(f"4. Upload: {zip_filename}")
    print(f"5. Publish release")
    print(f"\nThen update DATA_RELEASE_URL in modules/etl_pipeline.py")

if __name__ == '__main__':
    compress_data_folder()
