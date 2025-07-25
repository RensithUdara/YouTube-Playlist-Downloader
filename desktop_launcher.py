#!/usr/bin/env python3
"""
YouTube Playlist Downloader Pro - Desktop Launcher
Enhanced version with desktop-specific features and better error handling.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import subprocess
from pathlib import Path

# Add the current directory to the path so we can import our modules
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_dependencies():
    """Check if all required dependencies are available."""
    missing_deps = []
    
    try:
        import yt_dlp
    except ImportError:
        missing_deps.append("yt-dlp")
    
    try:
        import customtkinter
    except ImportError:
        missing_deps.append("customtkinter")
    
    return missing_deps

def install_dependencies(missing_deps):
    """Install missing dependencies."""
    for dep in missing_deps:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        except subprocess.CalledProcessError:
            return False
    return True

def show_dependency_error(missing_deps):
    """Show a user-friendly error dialog for missing dependencies."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    message = f"""YouTube Playlist Downloader Pro needs to install some components:

Missing: {', '.join(missing_deps)}

Would you like to install them now?
(This requires an internet connection)"""
    
    result = messagebox.askyesno(
        "Install Required Components",
        message,
        icon="question"
    )
    
    root.destroy()
    return result

def show_error_dialog(title, message):
    """Show an error dialog."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()

def main():
    """Main launcher function."""
    try:
        # Set application properties for Windows
        if sys.platform == "win32":
            try:
                import ctypes
                # Set the app model ID so Windows groups windows properly
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    "YouTubePlaylistDownloaderPro.DesktopApp.2.0"
                )
            except:
                pass
        
        # Check dependencies
        missing_deps = check_dependencies()
        
        if missing_deps:
            if show_dependency_error(missing_deps):
                # User wants to install dependencies
                root = tk.Tk()
                root.title("Installing Components")
                root.geometry("400x200")
                root.resizable(False, False)
                
                # Center the window
                root.update_idletasks()
                x = (root.winfo_screenwidth() // 2) - (400 // 2)
                y = (root.winfo_screenheight() // 2) - (200 // 2)
                root.geometry(f"400x200+{x}+{y}")
                
                label = tk.Label(
                    root, 
                    text="Installing required components...\nPlease wait...",
                    font=("Arial", 12),
                    pady=20
                )
                label.pack(expand=True)
                
                progress_label = tk.Label(root, text="", font=("Arial", 10))
                progress_label.pack(pady=10)
                
                root.update()
                
                # Install dependencies
                success = True
                for i, dep in enumerate(missing_deps):
                    progress_label.config(text=f"Installing {dep}...")
                    root.update()
                    
                    try:
                        subprocess.check_call([
                            sys.executable, "-m", "pip", "install", dep
                        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    except subprocess.CalledProcessError:
                        success = False
                        break
                
                root.destroy()
                
                if not success:
                    show_error_dialog(
                        "Installation Failed",
                        "Failed to install required components.\n\n"
                        "Please check your internet connection and try again.\n"
                        "You can also install manually using:\n"
                        "pip install yt-dlp customtkinter"
                    )
                    return
            else:
                # User declined installation
                return
        
        # Import and run the main application
        try:
            # Import the GUI module (handle different possible module names)
            gui_module = None
            possible_modules = [
                'youtube_downloader-gui',
                'youtube_downloader_gui', 
                'youtube_downloader-gui.py'
            ]
            
            for module_name in possible_modules:
                try:
                    if module_name.endswith('.py'):
                        # Import from file
                        import importlib.util
                        spec = importlib.util.spec_from_file_location(
                            "gui_module", 
                            current_dir / module_name
                        )
                        gui_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(gui_module)
                        break
                    else:
                        gui_module = __import__(module_name)
                        break
                except (ImportError, FileNotFoundError):
                    continue
            
            if gui_module is None:
                raise ImportError("Could not import GUI module")
            
            # Get the main app class
            app_class = getattr(gui_module, 'YouTubeDownloaderApp', None)
            if app_class is None:
                raise ImportError("Could not find YouTubeDownloaderApp class")
            
            # Create and run the application
            app = app_class()
            
            # Set window icon if available
            icon_path = current_dir / "icons" / "app_icon.ico"
            if icon_path.exists():
                try:
                    app.iconbitmap(str(icon_path))
                except:
                    pass
            
            # Configure for desktop use
            app.title("YouTube Playlist Downloader Pro")
            app.resizable(True, True)
            
            # Start the application
            app.mainloop()
            
        except ImportError:
            show_error_dialog(
                "Application Error",
                "Could not find the main application file.\n\n"
                "Please make sure 'youtube_downloader-gui.py' is in the same folder."
            )
        except Exception as e:
            show_error_dialog(
                "Application Error",
                f"An error occurred while starting the application:\n\n{str(e)}"
            )
    
    except Exception as e:
        # Fallback error handling
        try:
            show_error_dialog("Startup Error", f"Failed to start the application:\n\n{str(e)}")
        except:
            # Last resort - print to console
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
