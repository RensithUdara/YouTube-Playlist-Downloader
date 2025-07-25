#!/usr/bin/env python3
"""
Test script to validate YouTube Playlist Downloader installation
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import yt_dlp
        print("✅ yt-dlp import successful")
        print(f"   Version: {yt_dlp.version.__version__}")
    except ImportError as e:
        print(f"❌ yt-dlp import failed: {e}")
        return False
    
    try:
        import customtkinter as ctk
        print("✅ customtkinter import successful")
    except ImportError as e:
        print(f"❌ customtkinter import failed: {e}")
        return False
    
    try:
        import tkinter as tk
        print("✅ tkinter import successful")
    except ImportError as e:
        print(f"❌ tkinter import failed: {e}")
        return False
    
    return True

def test_files():
    """Test if application files exist."""
    print("\n📁 Testing application files...")
    
    files = [
        "youtube_Download-cli.py",
        "youtube_downloader-gui.py",
        "requirements.txt",
        "README.md"
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def test_syntax():
    """Test syntax of main application files."""
    print("\n🔍 Testing syntax...")
    
    files_to_test = [
        "youtube_Download-cli.py",
        "youtube_downloader-gui.py"
    ]
    
    all_valid = True
    for file in files_to_test:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                compile(content, file, 'exec')
                print(f"✅ {file} syntax valid")
            except SyntaxError as e:
                print(f"❌ {file} syntax error: {e}")
                all_valid = False
        else:
            print(f"⚠️ {file} not found for syntax check")
            all_valid = False
    
    return all_valid

def main():
    """Run all tests."""
    print("🎵 YouTube Playlist Downloader Pro - Validation Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test imports
    if test_imports():
        tests_passed += 1
    
    # Test files
    if test_files():
        tests_passed += 1
    
    # Test syntax
    if test_syntax():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your installation is ready to use.")
        print("\n📖 You can now run:")
        print("   • CLI Version: python youtube_Download-cli.py")
        print("   • GUI Version: python youtube_downloader-gui.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("💡 Try running: python setup.py")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
