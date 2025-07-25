#!/usr/bin/env python3
"""
YouTube Playlist Downloader Pro - Setup Script
Automatically installs required dependencies and checks system compatibility.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please update Python and try again.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_package(package_name, display_name=None):
    """Install a Python package using pip."""
    if display_name is None:
        display_name = package_name
    
    print(f"📦 Installing {display_name}...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", package_name
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {display_name} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {display_name}")
        return False

def check_package_installation(package_name, import_name=None):
    """Check if a package is properly installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False

def main():
    """Main setup function."""
    print("🎵 YouTube Playlist Downloader Pro - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("\n📋 Installing required dependencies...")
    
    # Install dependencies
    dependencies = [
        ("yt-dlp", "YouTube Downloader (yt-dlp)"),
        ("customtkinter", "Modern GUI Framework (CustomTkinter)")
    ]
    
    failed_packages = []
    
    for package, display_name in dependencies:
        if not install_package(package, display_name):
            failed_packages.append(display_name)
    
    print("\n🔍 Verifying installations...")
    
    # Verify installations
    verification_checks = [
        ("yt_dlp", "yt-dlp"),
        ("customtkinter", "CustomTkinter")
    ]
    
    all_verified = True
    for import_name, display_name in verification_checks:
        if check_package_installation(import_name, import_name):
            print(f"✅ {display_name} - Working")
        else:
            print(f"❌ {display_name} - Not working")
            all_verified = False
    
    print("\n" + "=" * 50)
    
    if all_verified and not failed_packages:
        print("🎉 Setup completed successfully!")
        print("\n📖 You can now run:")
        print("   • CLI Version: python youtube_Download-cli.py")
        print("   • GUI Version: python youtube_downloader-gui.py")
        
        # Check if script files exist
        cli_file = Path("youtube_Download-cli.py")
        gui_file = Path("youtube_downloader-gui.py")
        
        if cli_file.exists() and gui_file.exists():
            print("\n✅ All application files found!")
        else:
            print("\n⚠️  Some application files may be missing:")
            if not cli_file.exists():
                print("   - youtube_Download-cli.py not found")
            if not gui_file.exists():
                print("   - youtube_downloader-gui.py not found")
    else:
        print("❌ Setup encountered issues:")
        if failed_packages:
            print("   Failed to install:", ", ".join(failed_packages))
        if not all_verified:
            print("   Some packages are not working properly")
        print("\n🔧 Try running this script again or install manually:")
        print("   pip install yt-dlp customtkinter")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
