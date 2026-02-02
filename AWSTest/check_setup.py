import os
import sys
import re
from pathlib import Path

# --- Configuration ---
REQUIRED_FILES = [
    "apprunner.yaml",
    "manage.py",
    "requirements/base.txt",
    "requirements/dev.txt",
    "config/settings.py",  # Adjust if your settings are elsewhere
]

FORBIDDEN_DEPS = [
    "paypalrestsdk",      # Security risk
    "django-debug-toolbar", # Should not be in base.txt
]

REQUIRED_DEPS = [
    "psycopg",            # Prod database adapter
    "gunicorn",           # Prod web server
    "whitenoise",         # Static files
    "django-environ",     # Config
    "paypal-server-sdk",  # Modern PayPal SDK
]

def check_file_exists(path):
    if not os.path.exists(path):
        print(f"❌ MISSING: {path}")
        return False
    print(f"✅ FOUND:   {path}")
    return True

def check_apprunner_yaml():
    """Validates specific Python 3.11 syntax for App Runner."""
    path = "apprunner.yaml"
    if not os.path.exists(path):
        return False

    with open(path, "r") as f:
        content = f.read()

    errors = []
    
    # Check 1: Runtime MUST be python311 for this version
    if "runtime: python311" not in content:
        errors.append("   - Runtime must be 'python311' (Found something else)")

    # Check 2: Build commands must use pip3/python3
    if "pip install" in content:
        errors.append("   - Build command uses 'pip install'. Must use 'pip3 install' for Python 3.11")
    
    # Check 3: Collectstatic presence
    if "collectstatic" not in content:
        errors.append("   - Missing 'collectstatic' command")

    if errors:
        print(f"❌ ISSUE:   {path}")
        for e in errors:
            print(e)
        return False
    
    print(f"✅ VALID:   {path} (Python 3.11 syntax correct)")
    return True

def check_requirements():
    """Scans requirements/base.txt for safety and completeness."""
    path = "requirements/base.txt"
    if not os.path.exists(path):
        return False

    with open(path, "r") as f:
        content = f.read()

    success = True
    
    # Check for forbidden
    for dep in FORBIDDEN_DEPS:
        if dep in content:
            print(f"❌ DANGER:  {dep} found in {path}. Remove it!")
            success = False

    # Check for required
    for dep in REQUIRED_DEPS:
        if dep not in content:
            print(f"❌ MISSING: {dep} not found in {path}")
            success = False

    # Check for binary psycopg
    if "psycopg[binary]" in content:
        print(f"⚠️  WARNING: 'psycopg[binary]' found. Use 'psycopg' for better prod stability.")
    
    if success:
        print(f"✅ VALID:   {path}")
    return success

def main():
    print("--- 🚀 App Runner Pre-Flight Check ---\n")
    all_passed = True

    # 1. File Structure
    print("Checking File Structure...")
    for f in REQUIRED_FILES:
        if not check_file_exists(f):
            all_passed = False
    print("")

    # 2. App Runner Config
    print("Checking App Runner Config...")
    if not check_apprunner_yaml():
        all_passed = False
    print("")

    # 3. Dependencies
    print("Checking Dependencies...")
    if not check_requirements():
        all_passed = False
    print("")

    if all_passed:
        print("🎉 READY FOR TAKEOFF! You can push to Git.")
        sys.exit(0)
    else:
        print("🛑 FIX ERRORS BEFORE PUSHING.")
        sys.exit(1)

if __name__ == "__main__":
    main()