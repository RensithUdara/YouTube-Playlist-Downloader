#!/usr/bin/env python3
"""
Desktop Application Builder for YouTube Playlist Downloader Pro
Creates a standalone desktop application using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Application configuration
APP_CONFIG = {
    'name': 'YouTube Playlist Downloader Pro',
    'version': '2.0.0',
    'description': 'Professional YouTube playlist downloader with modern GUI',
    'author': 'YouTube Playlist Downloader Team',
    'icon': 'icons/app_icon.ico',
    'main_script': 'youtube_downloader-gui.py',
    'console': False,  # Set to True if you want console window
    'onefile': True,   # Create single executable file
}

def check_requirements():
    """Check if all required tools and files are available."""
    print("🔍 Checking requirements...")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found")
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed")
    
    # Check if main script exists
    if not os.path.exists(APP_CONFIG['main_script']):
        print(f"❌ Main script not found: {APP_CONFIG['main_script']}")
        return False
    print(f"✅ Main script found: {APP_CONFIG['main_script']}")
    
    # Check if icon exists
    if not os.path.exists(APP_CONFIG['icon']):
        print(f"⚠️ Icon not found: {APP_CONFIG['icon']}")
        print("🎨 Creating icons...")
        try:
            subprocess.check_call([sys.executable, "create_icon.py"])
        except Exception as e:
            print(f"❌ Failed to create icons: {e}")
            return False
    print(f"✅ Icon found: {APP_CONFIG['icon']}")
    
    return True

def create_spec_file():
    """Create PyInstaller spec file for advanced configuration."""
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{APP_CONFIG['main_script']}'],
    pathex=[],
    binaries=[],
    datas=[
        ('icons/', 'icons/'),
        ('README.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'yt_dlp',
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_CONFIG['name'].replace(' ', '_')}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={str(APP_CONFIG['console']).lower()},
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{APP_CONFIG['icon']}',
    version_file='version_info.txt',
)
'''
    
    spec_filename = f"{APP_CONFIG['name'].replace(' ', '_')}.spec"
    with open(spec_filename, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✅ Created spec file: {spec_filename}")
    return spec_filename

def create_version_info():
    """Create version information file for Windows executable."""
    version_info = f'''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=(2,0,0,0),
prodvers=(2,0,0,0),
# Contains a bitmask that specifies the valid bits 'flags'r
mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
OS=0x4,
# The general type of file.
# 0x1 - the file is an application.
fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
subtype=0x0,
# Creation date and time stamp.
date=(0, 0)
),
  kids=[
StringFileInfo(
  [
  StringTable(
    u'040904B0',
    [StringStruct(u'CompanyName', u'{APP_CONFIG['author']}'),
    StringStruct(u'FileDescription', u'{APP_CONFIG['description']}'),
    StringStruct(u'FileVersion', u'{APP_CONFIG['version']}'),
    StringStruct(u'InternalName', u'{APP_CONFIG['name']}'),
    StringStruct(u'LegalCopyright', u'© 2025 {APP_CONFIG['author']}'),
    StringStruct(u'OriginalFilename', u'{APP_CONFIG['name'].replace(' ', '_')}.exe'),
    StringStruct(u'ProductName', u'{APP_CONFIG['name']}'),
    StringStruct(u'ProductVersion', u'{APP_CONFIG['version']}')])
  ]), 
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("✅ Created version_info.txt")

def build_application():
    """Build the desktop application using PyInstaller."""
    print("\n🚀 Building desktop application...")
    print("=" * 50)
    
    # Create spec file
    spec_file = create_spec_file()
    
    # Create version info
    create_version_info()
    
    # Build command
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        spec_file
    ]
    
    print(f"🔨 Running: {' '.join(build_cmd)}")
    
    try:
        # Run PyInstaller
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build completed successfully!")
            
            # Find the executable
            exe_name = f"{APP_CONFIG['name'].replace(' ', '_')}.exe"
            exe_path = Path("dist") / exe_name
            
            if exe_path.exists():
                print(f"🎉 Executable created: {exe_path}")
                print(f"📏 File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
                
                # Create a more user-friendly name
                friendly_name = f"{APP_CONFIG['name']}.exe"
                friendly_path = Path("dist") / friendly_name
                
                if friendly_path != exe_path:
                    shutil.copy2(exe_path, friendly_path)
                    print(f"📋 Also created: {friendly_path}")
                
                return True
            else:
                print(f"❌ Executable not found at expected location: {exe_path}")
                return False
        else:
            print("❌ Build failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def create_desktop_shortcut():
    """Create a desktop shortcut (Windows only)."""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        exe_path = Path("dist") / f"{APP_CONFIG['name']}.exe"
        
        if exe_path.exists():
            shortcut_path = Path(desktop) / f"{APP_CONFIG['name']}.lnk"
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(exe_path.absolute())
            shortcut.WorkingDirectory = str(exe_path.parent.absolute())
            shortcut.IconLocation = str(exe_path.absolute())
            shortcut.Description = APP_CONFIG['description']
            shortcut.save()
            
            print(f"✅ Desktop shortcut created: {shortcut_path}")
            return True
            
    except ImportError:
        print("⚠️ winshell not available - skipping desktop shortcut")
        print("📦 Install with: pip install winshell pywin32")
    except Exception as e:
        print(f"⚠️ Could not create desktop shortcut: {e}")
    
    return False

def cleanup_build_files():
    """Clean up temporary build files."""
    print("\n🧹 Cleaning up build files...")
    
    cleanup_items = [
        "build",
        "__pycache__",
        "*.spec",
        "version_info.txt"
    ]
    
    for item in cleanup_items:
        if "*" in item:
            # Handle wildcards
            import glob
            for file in glob.glob(item):
                try:
                    os.remove(file)
                    print(f"🗑️ Removed: {file}")
                except Exception:
                    pass
        else:
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f"🗑️ Removed directory: {item}")
                elif os.path.exists(item):
                    os.remove(item)
                    print(f"🗑️ Removed file: {item}")
            except Exception:
                pass

def main():
    """Main build process."""
    print("🖥️ YouTube Playlist Downloader Pro - Desktop App Builder")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed!")
        input("Press Enter to exit...")
        return
    
    print("\n📋 Application Configuration:")
    print(f"   Name: {APP_CONFIG['name']}")
    print(f"   Version: {APP_CONFIG['version']}")
    print(f"   Main Script: {APP_CONFIG['main_script']}")
    print(f"   Icon: {APP_CONFIG['icon']}")
    print(f"   Single File: {APP_CONFIG['onefile']}")
    
    # Confirm build
    response = input(f"\n🤔 Build desktop application? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ Build cancelled.")
        return
    
    # Build application
    if build_application():
        print("\n🎉 Desktop application built successfully!")
        
        # Create desktop shortcut
        create_desktop_shortcut()
        
        # Show results
        print("\n📋 Build Results:")
        dist_dir = Path("dist")
        if dist_dir.exists():
            for file in dist_dir.glob("*.exe"):
                size_mb = file.stat().st_size / (1024*1024)
                print(f"   📁 {file.name} ({size_mb:.1f} MB)")
        
        print(f"\n📁 Files are located in: {dist_dir.absolute()}")
        print("\n🚀 You can now distribute the executable file!")
        print("   • No Python installation required on target machines")
        print("   • All dependencies are included")
        print("   • Professional desktop application ready to use")
        
        # Ask about cleanup
        cleanup_response = input(f"\n🧹 Clean up build files? (Y/n): ").strip().lower()
        if cleanup_response not in ['n', 'no']:
            cleanup_build_files()
        
    else:
        print("❌ Build failed! Check the error messages above.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
