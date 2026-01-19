"""
Installation Verification Script for Jan-Gana-Drishti
Checks if all dependencies and data files are properly set up
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("="*70)
    print("🐍 Checking Python Version...")
    version = sys.version_info
    print(f"   Current version: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python version OK")
        return True
    else:
        print("   ❌ Python 3.8+ required")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    print("\n" + "="*70)
    print("📦 Checking Dependencies...")
    
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'streamlit': 'streamlit',
        'plotly': 'plotly',
        'fuzzywuzzy': 'fuzzywuzzy',
        'sklearn': 'scikit-learn',
        'scipy': 'scipy'
    }
    
    all_ok = True
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} NOT FOUND")
            all_ok = False
    
    if not all_ok:
        print("\n   ⚠️  Install missing packages with: pip install -r requirements.txt")
    
    return all_ok


def check_data_structure():
    """Check if data directories and files exist"""
    print("\n" + "="*70)
    print("📂 Checking Data Structure...")
    
    base_dir = Path.cwd()
    data_dir = base_dir / 'data'
    
    if not data_dir.exists():
        print(f"   ❌ Data directory not found: {data_dir}")
        return False
    
    print(f"   ✅ Data directory found: {data_dir}")
    
    required_folders = [
        'api_data_aadhar_biometric',
        'api_data_aadhar_demographic',
        'api_data_aadhar_enrolment'
    ]
    
    all_ok = True
    total_files = 0
    
    for folder in required_folders:
        folder_path = data_dir / folder
        if not folder_path.exists():
            print(f"   ❌ Missing folder: {folder}")
            all_ok = False
        else:
            csv_files = list(folder_path.glob('*.csv'))
            total_files += len(csv_files)
            if len(csv_files) == 0:
                print(f"   ⚠️  {folder}: No CSV files found")
                all_ok = False
            else:
                print(f"   ✅ {folder}: {len(csv_files)} CSV file(s)")
    
    print(f"\n   📊 Total CSV files: {total_files}")
    
    return all_ok


def check_module_structure():
    """Check if all custom modules exist"""
    print("\n" + "="*70)
    print("🔧 Checking Module Structure...")
    
    base_dir = Path.cwd()
    modules_dir = base_dir / 'modules'
    
    if not modules_dir.exists():
        print(f"   ❌ Modules directory not found: {modules_dir}")
        return False
    
    print(f"   ✅ Modules directory found")
    
    required_modules = [
        '__init__.py',
        'etl_pipeline.py',
        'fraud_detection.py',
        'migration_tracker.py',
        'child_welfare.py'
    ]
    
    all_ok = True
    for module_file in required_modules:
        module_path = modules_dir / module_file
        if not module_path.exists():
            print(f"   ❌ Missing module: {module_file}")
            all_ok = False
        else:
            print(f"   ✅ {module_file}")
    
    return all_ok


def check_main_files():
    """Check if main application files exist"""
    print("\n" + "="*70)
    print("📄 Checking Main Application Files...")
    
    base_dir = Path.cwd()
    
    required_files = {
        'app.py': 'Main Streamlit application',
        'requirements.txt': 'Dependencies list',
        'README.md': 'Documentation',
        'QUICK_START.md': 'Quick start guide'
    }
    
    all_ok = True
    for file_name, description in required_files.items():
        file_path = base_dir / file_name
        if not file_path.exists():
            print(f"   ❌ {file_name} ({description})")
            all_ok = False
        else:
            print(f"   ✅ {file_name}")
    
    return all_ok


def test_import_modules():
    """Test if custom modules can be imported"""
    print("\n" + "="*70)
    print("🧪 Testing Module Imports...")
    
    all_ok = True
    
    try:
        from modules.etl_pipeline import AadhaarETLPipeline
        print("   ✅ ETL Pipeline module")
    except Exception as e:
        print(f"   ❌ ETL Pipeline module: {str(e)}")
        all_ok = False
    
    try:
        from modules.fraud_detection import GhostHunterEngine
        print("   ✅ Fraud Detection module")
    except Exception as e:
        print(f"   ❌ Fraud Detection module: {str(e)}")
        all_ok = False
    
    try:
        from modules.migration_tracker import MigrationPulseTracker
        print("   ✅ Migration Tracker module")
    except Exception as e:
        print(f"   ❌ Migration Tracker module: {str(e)}")
        all_ok = False
    
    try:
        from modules.child_welfare import ChildWelfareAnalyzer
        print("   ✅ Child Welfare module")
    except Exception as e:
        print(f"   ❌ Child Welfare module: {str(e)}")
        all_ok = False
    
    return all_ok


def main():
    """Run all verification checks"""
    print("\n" + "="*70)
    print("🇮🇳 Jan-Gana-Drishti Installation Verification")
    print("Government of India - UIDAI Hackathon 2026")
    print("="*70)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Data Structure", check_data_structure),
        ("Module Structure", check_module_structure),
        ("Main Files", check_main_files),
        ("Module Imports", test_import_modules)
    ]
    
    results = {}
    for check_name, check_func in checks:
        results[check_name] = check_func()
    
    # Summary
    print("\n" + "="*70)
    print("📊 VERIFICATION SUMMARY")
    print("="*70)
    
    all_passed = True
    for check_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status}: {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*70)
    
    if all_passed:
        print("🎉 All checks passed! You're ready to launch the dashboard.")
        print("\n📌 Next steps:")
        print("   1. Run: streamlit run app.py")
        print("   2. Or: ./run_dashboard.sh")
        print("   3. Open browser: http://localhost:8501")
        print("="*70)
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n📌 Common fixes:")
        print("   • Install dependencies: pip install -r requirements.txt")
        print("   • Verify data directory structure")
        print("   • Check file permissions")
        print("="*70)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
