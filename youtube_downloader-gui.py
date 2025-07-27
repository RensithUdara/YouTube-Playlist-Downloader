import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import customtkinter as ctk
import subprocess
import threading
import json
import os
import sys
import re
import time
from datetime import datetime
import webbrowser
import urllib.parse

# Optional imports for enhanced features
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Main application class
class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("🎵 YouTube Playlist Downloader Pro")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Set window icon if available
        try:
            if os.path.exists("icons/app_icon.ico"):
                self.iconbitmap("icons/app_icon.ico")
        except:
            pass
        
        # Center window on screen
        self.center_window()
        
        # --- Enhanced Variables ---
        self.download_processes = {}
        self.video_widgets = {}
        self.video_data = {}
        self.is_fetching = False
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube Downloads")
        self.total_videos = 0
        self.completed_downloads = 0
        self.failed_downloads = 0
        self.download_history = []
        self.favorites = []
        self.current_playlist_info = {}
        
        # Create download directory if it doesn't exist
        os.makedirs(self.download_path, exist_ok=True)
        
        # --- Enhanced Styling ---
        self.setup_styles()
        
        # --- Load user preferences ---
        self.load_preferences()
        
        # --- GUI Elements ---
        self.create_widgets()
        
        # --- Start monitoring downloads ---
        self.after(100, self.monitor_downloads)
        
        # --- Initialize tooltips ---
        self.setup_tooltips()

    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        """Setup enhanced custom styling for the application."""
        # Enhanced color palette
        self.colors = {
            'primary': "#FF0000",      # YouTube Red
            'primary_dark': "#CC0000",  # Darker YouTube Red
            'secondary': "#282828",     # YouTube Dark Gray
            'secondary_light': "#3F3F3F",
            'success': "#00C851",       # Success Green
            'warning': "#FF8800",       # Warning Orange
            'danger': "#FF4444",        # Danger Red
            'info': "#0099FF",          # Info Blue
            'background': "#181818",    # Dark Background
            'surface': "#282828",       # Surface Gray
            'surface_light': "#3F3F3F", # Light Surface
            'text_primary': "#FFFFFF",  # Primary Text
            'text_secondary': "#AAAAAA", # Secondary Text
            'border': "#444444",        # Border Color
            'accent': "#4285F4",        # Accent Blue
            'gradient_start': "#FF0000",
            'gradient_end': "#CC0000"
        }
        
        # Font configurations
        self.fonts = {
            'title': ctk.CTkFont(size=28, weight="bold"),
            'subtitle': ctk.CTkFont(size=14),
            'heading': ctk.CTkFont(size=16, weight="bold"),
            'body': ctk.CTkFont(size=12),
            'small': ctk.CTkFont(size=10),
            'button': ctk.CTkFont(size=12, weight="bold"),
            'large_button': ctk.CTkFont(size=14, weight="bold")
        }

    def create_widgets(self):
        # Create main tabbed interface
        self.create_main_tabs()

    def create_main_tabs(self):
        """Create the main tabbed interface."""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create tabview
        self.tabview = ctk.CTkTabview(main_container, height=750)
        self.tabview.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.tab_downloader = self.tabview.add("🎵 Downloader")
        self.tab_history = self.tabview.add("📜 History") 
        self.tab_favorites = self.tabview.add("⭐ Favorites")
        self.tab_settings = self.tabview.add("⚙️ Settings")
        self.tab_about = self.tabview.add("ℹ️ About")
        
        # Setup each tab
        self.setup_downloader_tab()
        self.setup_history_tab()
        self.setup_favorites_tab()
        self.setup_settings_tab()
        self.setup_about_tab()

    def setup_downloader_tab(self):
        """Setup the main downloader tab with enhanced UI."""
        tab = self.tab_downloader
        
        # Header section with animated gradient effect
        self.create_enhanced_header(tab)
        
        # Quick actions toolbar
        self.create_quick_actions(tab)
        
        # URL input section with validation
        self.create_enhanced_url_section(tab)
        
        # Download path and options
        options_container = ctk.CTkFrame(tab, fg_color="transparent")
        options_container.pack(fill=tk.X, pady=(0, 15))
        
        # Left side - Path and basic options
        left_options = ctk.CTkFrame(options_container, fg_color=self.colors['surface'])
        left_options.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 7))
        self.create_enhanced_path_section(left_options)
        
        # Right side - Advanced options
        right_options = ctk.CTkFrame(options_container, fg_color=self.colors['surface'])
        right_options.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(7, 0))
        self.create_advanced_options(right_options)
        
        # Playlist info section
        self.create_playlist_info_section(tab)
        
        # Enhanced status section with real-time stats
        self.create_enhanced_status_section(tab)
        
        # Video list with preview thumbnails
        self.create_enhanced_video_list_section(tab)
        
        # Enhanced control buttons with more options
        self.create_enhanced_control_buttons(tab)

    def create_enhanced_header(self, parent):
        """Create an enhanced header with gradient effect and animations."""
        header_frame = ctk.CTkFrame(parent, height=100, fg_color=self.colors['primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Main title with YouTube-style branding
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🎵 YouTube Playlist Downloader Pro",
            font=self.fonts['title'],
            text_color="white"
        )
        title_label.pack(pady=(15, 5))
        
        # Subtitle with feature highlights
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="✨ High-Quality Downloads • Batch Processing • Smart Organization • History Tracking",
            font=self.fonts['subtitle'],
            text_color="#FFE0E0"
        )
        subtitle_label.pack()
        
        # Version and status indicator
        version_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        version_frame.pack(fill=tk.X, padx=20, pady=(5, 5))
        
        version_label = ctk.CTkLabel(
            version_frame,
            text="v2.0 Pro",
            font=ctk.CTkFont(size=10),
            text_color="#CCCCCC"
        )
        version_label.pack(side=tk.LEFT)
        
        # Live status indicator
        self.status_dot = ctk.CTkLabel(
            version_frame,
            text="🟢 Ready",
            font=ctk.CTkFont(size=10),
            text_color="#00FF00"
        )
        self.status_dot.pack(side=tk.RIGHT)

    def create_quick_actions(self, parent):
        """Create quick action buttons toolbar."""
        toolbar_frame = ctk.CTkFrame(parent, height=50, fg_color=self.colors['surface'])
        toolbar_frame.pack(fill=tk.X, pady=(0, 15))
        toolbar_frame.pack_propagate(False)
        
        # Quick action buttons
        buttons_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        buttons_frame.pack(expand=True, pady=10)
        
        # Paste URL button
        self.paste_button = ctk.CTkButton(
            buttons_frame,
            text="📋 Paste URL",
            command=self.paste_url_from_clipboard,
            width=100,
            height=30,
            font=self.fonts['small']
        )
        self.paste_button.pack(side=tk.LEFT, padx=5)
        
        # Clear all button  
        self.clear_button = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Clear",
            command=self.clear_all,
            width=80,
            height=30,
            font=self.fonts['small'],
            fg_color=self.colors['warning']
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Open download folder
        self.open_folder_button = ctk.CTkButton(
            buttons_frame,
            text="📁 Open Folder",
            command=self.open_download_folder,
            width=120,
            height=30,
            font=self.fonts['small'],
            fg_color=self.colors['info']
        )
        self.open_folder_button.pack(side=tk.LEFT, padx=5)
        
        # Refresh playlist button
        self.refresh_button = ctk.CTkButton(
            buttons_frame,
            text="🔄 Refresh",
            command=self.refresh_playlist,
            width=100,
            height=30,
            font=self.fonts['small'],
            fg_color=self.colors['accent']
        )
        self.refresh_button.pack(side=tk.LEFT, padx=5)

    def create_enhanced_url_section(self, parent):
        """Create enhanced URL input with validation and suggestions."""
        url_frame = ctk.CTkFrame(parent, fg_color=self.colors['surface'])
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Header with icon and instructions
        header_frame = ctk.CTkFrame(url_frame, fg_color="transparent")
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        url_label = ctk.CTkLabel(
            header_frame, 
            text="🔗 Playlist URL",
            font=self.fonts['heading'],
            text_color=self.colors['text_primary']
        )
        url_label.pack(side=tk.LEFT)
        
        # URL validation indicator
        self.url_status = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=self.colors['text_secondary']
        )
        self.url_status.pack(side=tk.RIGHT)
        
        # URL input with enhanced styling
        input_frame = ctk.CTkFrame(url_frame, fg_color="transparent")
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 10))

        self.url_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="🎵 Enter YouTube playlist URL (e.g., https://youtube.com/playlist?list=...)",
            height=45,
            font=self.fonts['body'],
            border_width=2,
            border_color=self.colors['border']
        )
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.url_entry.bind('<KeyRelease>', self.validate_url)
        self.url_entry.bind('<Return>', lambda e: self.start_fetch_thread())

        self.load_button = ctk.CTkButton(
            input_frame,
            text="🔍 Load Playlist",
            command=self.start_fetch_thread,
            height=45,
            width=150,
            font=self.fonts['button'],
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_dark']
        )
        self.load_button.pack(side=tk.RIGHT)
        
        # URL suggestions/history
        self.create_url_suggestions(url_frame)

    def create_url_suggestions(self, parent):
        """Create URL suggestions dropdown."""
        suggestions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        suggestions_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            suggestions_frame,
            text="💡 Recent playlists:",
            font=ctk.CTkFont(size=10),
            text_color=self.colors['text_secondary']
        ).pack(side=tk.LEFT)

    def create_enhanced_path_section(self, parent):
        """Create enhanced download path section with organization options."""
        # Header
        ctk.CTkLabel(
            parent,
            text="📁 Download Settings",
            font=self.fonts['heading']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Path selection
        path_frame = ctk.CTkFrame(parent, fg_color="transparent")
        path_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.path_label = ctk.CTkLabel(
            path_frame,
            text=f"📂 {self.download_path}",
            font=self.fonts['small'],
            anchor="w",
            text_color=self.colors['text_secondary']
        )
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.path_button = ctk.CTkButton(
            path_frame,
            text="📁 Browse",
            command=self.select_download_path,
            height=30,
            width=80,
            font=self.fonts['small']
        )
        self.path_button.pack(side=tk.RIGHT)
        
        # Organization options
        org_frame = ctk.CTkFrame(parent, fg_color="transparent")
        org_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.organize_folders_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            org_frame,
            text="📂 Create playlist folders",
            variable=self.organize_folders_var,
            font=self.fonts['small']
        ).pack(anchor="w", pady=2)
        
        self.add_numbers_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            org_frame,
            text="🔢 Add track numbers",
            variable=self.add_numbers_var,
            font=self.fonts['small']
        ).pack(anchor="w", pady=2)

    def create_advanced_options(self, parent):
        """Create advanced download options."""
        # Header
        ctk.CTkLabel(
            parent,
            text="⚙️ Quality & Format",
            font=self.fonts['heading']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        options_frame = ctk.CTkFrame(parent, fg_color="transparent")
        options_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Quality selection with preview
        quality_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        quality_frame.pack(fill=tk.X, pady=(0, 10))
        
        ctk.CTkLabel(
            quality_frame, 
            text="🎥 Video Quality:",
            font=self.fonts['small']
        ).pack(anchor="w")
        
        self.quality_var = ctk.StringVar(value="Best Available")
        self.quality_dropdown = ctk.CTkOptionMenu(
            quality_frame,
            values=[
                "Best Available",
                "4K (2160p)",
                "1440p",
                "1080p HD", 
                "720p HD",
                "480p",
                "360p",
                "Audio Only (Best)",
                "Audio Only (320kbps)",
                "Audio Only (128kbps)"
            ],
            variable=self.quality_var,
            width=180,
            command=self.on_quality_change
        )
        self.quality_dropdown.pack(anchor="w", pady=(5, 0))
        
        # Format options
        format_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        format_frame.pack(fill=tk.X, pady=(0, 10))
        
        ctk.CTkLabel(
            format_frame,
            text="📝 Format Options:",
            font=self.fonts['small']
        ).pack(anchor="w")
        
        self.subtitle_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            format_frame,
            text="📜 Download subtitles",
            variable=self.subtitle_var,
            font=ctk.CTkFont(size=10)
        ).pack(anchor="w", pady=2)
        
        self.thumbnail_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            format_frame,
            text="🖼️ Save thumbnails",
            variable=self.thumbnail_var,
            font=ctk.CTkFont(size=10)
        ).pack(anchor="w", pady=2)

    def create_playlist_info_section(self, parent):
        """Create playlist information display."""
        self.playlist_info_frame = ctk.CTkFrame(parent, fg_color=self.colors['surface'])
        # Initially hidden
        
        # Playlist header
        info_header = ctk.CTkFrame(self.playlist_info_frame, fg_color="transparent")
        info_header.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        self.playlist_title_label = ctk.CTkLabel(
            info_header,
            text="",
            font=self.fonts['heading'],
            anchor="w"
        )
        self.playlist_title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.playlist_stats_label = ctk.CTkLabel(
            info_header,
            text="",
            font=self.fonts['small'],
            text_color=self.colors['text_secondary']
        )
        self.playlist_stats_label.pack(side=tk.RIGHT)
        
        # Playlist description (collapsible)
        self.playlist_desc_label = ctk.CTkLabel(
            self.playlist_info_frame,
            text="",
            font=self.fonts['small'],
            text_color=self.colors['text_secondary'],
            anchor="w",
            wraplength=800
        )
        self.playlist_desc_label.pack(fill=tk.X, padx=15, pady=(0, 15))

    def create_enhanced_status_section(self, parent):
        """Create enhanced status section with real-time statistics."""
        status_frame = ctk.CTkFrame(parent, height=70, fg_color=self.colors['surface'])
        status_frame.pack(fill=tk.X, pady=(0, 15))
        status_frame.pack_propagate(False)
        
        # Main status display
        status_content = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Status text with icon
        status_left = ctk.CTkFrame(status_content, fg_color="transparent")
        status_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.status_label = ctk.CTkLabel(
            status_left,
            text="📋 Ready - Paste a playlist URL to begin downloading",
            font=self.fonts['body'],
            anchor="w",
            text_color=self.colors['text_primary']
        )
        self.status_label.pack(side=tk.TOP, fill=tk.X)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            status_left,
            width=300,
            height=8,
            progress_color=self.colors['success']
        )
        self.progress_bar.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))
        self.progress_bar.set(0)
        
        # Statistics panel
        stats_frame = ctk.CTkFrame(status_content, width=200, fg_color=self.colors['surface_light'])
        stats_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        stats_frame.pack_propagate(False)
        
        self.stats_total_label = ctk.CTkLabel(
            stats_frame,
            text="Total: 0",
            font=self.fonts['small'],
            text_color=self.colors['text_secondary']
        )
        self.stats_total_label.pack(pady=2)
        
        self.stats_completed_label = ctk.CTkLabel(
            stats_frame,
            text="✅ Completed: 0",
            font=self.fonts['small'],
            text_color=self.colors['success']
        )
        self.stats_completed_label.pack(pady=2)
        
        self.stats_failed_label = ctk.CTkLabel(
            stats_frame,
            text="❌ Failed: 0",
            font=self.fonts['small'],
            text_color=self.colors['danger']
        )
        self.stats_failed_label.pack(pady=2)

    def create_enhanced_video_list_section(self, parent):
        """Create enhanced video list with thumbnails and detailed info."""
        # Header with controls
        list_header = ctk.CTkFrame(parent, fg_color="transparent")
        list_header.pack(fill=tk.X, pady=(0, 10))
        
        list_label = ctk.CTkLabel(
            list_header,
            text="📺 Playlist Videos",
            font=self.fonts['heading']
        )
        list_label.pack(side=tk.LEFT)
        
        # List controls
        controls_frame = ctk.CTkFrame(list_header, fg_color="transparent")
        controls_frame.pack(side=tk.RIGHT)
        
        # Select all/none buttons
        self.select_all_button = ctk.CTkButton(
            controls_frame,
            text="☑️ All",
            command=self.select_all_videos,
            width=60,
            height=25,
            font=ctk.CTkFont(size=10)
        )
        self.select_all_button.pack(side=tk.LEFT, padx=2)
        
        self.select_none_button = ctk.CTkButton(
            controls_frame,
            text="☐ None", 
            command=self.select_no_videos,
            width=60,
            height=25,
            font=ctk.CTkFont(size=10)
        )
        self.select_none_button.pack(side=tk.LEFT, padx=2)
        
        # View mode toggle
        self.view_mode_var = ctk.StringVar(value="List")
        self.view_toggle = ctk.CTkOptionMenu(
            controls_frame,
            values=["List", "Grid", "Compact"],
            variable=self.view_mode_var,
            width=80,
            height=25,
            command=self.change_view_mode
        )
        self.view_toggle.pack(side=tk.LEFT, padx=2)
        
        # Enhanced scrollable frame
        self.video_list_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color=self.colors['surface'],
            scrollbar_button_color=self.colors['primary'],
            scrollbar_button_hover_color=self.colors['primary_dark']
        )
        self.video_list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

    def create_enhanced_control_buttons(self, parent):
        """Create enhanced control buttons with more options."""
        button_container = ctk.CTkFrame(parent, fg_color="transparent")
        button_container.pack(fill=tk.X, pady=(0, 15))

        # Main action buttons
        main_buttons = ctk.CTkFrame(button_container, fg_color="transparent")
        main_buttons.pack(side=tk.LEFT)

        self.download_selected_button = ctk.CTkButton(
            main_buttons,
            text="⬇️ Download Selected",
            command=self.download_selected,
            state=tk.DISABLED,
            height=45,
            width=180,
            font=self.fonts['large_button'],
            fg_color=self.colors['success'],
            hover_color="#00A041"
        )
        self.download_selected_button.pack(side=tk.LEFT, padx=(0, 10))

        self.download_all_button = ctk.CTkButton(
            main_buttons,
            text="⬇️ Download All",
            command=self.download_all,
            state=tk.DISABLED,
            height=45,
            width=150,
            font=self.fonts['large_button'],
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_dark']
        )
        self.download_all_button.pack(side=tk.LEFT, padx=(0, 10))

        # Control buttons
        control_buttons = ctk.CTkFrame(button_container, fg_color="transparent")
        control_buttons.pack(side=tk.RIGHT)

        self.pause_all_button = ctk.CTkButton(
            control_buttons,
            text="⏸️ Pause All",
            command=self.pause_all_downloads,
            state=tk.DISABLED,
            height=35,
            width=120,
            font=self.fonts['button'],
            fg_color=self.colors['warning']
        )
        self.pause_all_button.pack(side=tk.LEFT, padx=5)

        self.cancel_all_button = ctk.CTkButton(
            control_buttons,
            text="⏹️ Stop All",
            command=self.cancel_all_downloads,
            state=tk.DISABLED,
            height=35,
            width=120,
            font=self.fonts['button'],
            fg_color=self.colors['danger']
        )
        self.cancel_all_button.pack(side=tk.LEFT, padx=5)

    # === NEW ENHANCED TAB METHODS ===
    
    def setup_history_tab(self):
        """Setup the download history tab."""
        tab = self.tab_history
        
        # Header
        header_frame = ctk.CTkFrame(tab, height=60, fg_color=self.colors['surface'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="📜 Download History",
            font=self.fonts['title'],
            text_color=self.colors['text_primary']
        ).pack(pady=20)
        
        # Controls
        controls_frame = ctk.CTkFrame(tab, fg_color=self.colors['surface'])
        controls_frame.pack(fill=tk.X, pady=(0, 15))
        
        buttons_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        buttons_frame.pack(pady=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="🔄 Refresh",
            command=self.refresh_history,
            width=100,
            height=30
        ).pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Clear History",
            command=self.clear_history,
            width=120,
            height=30,
            fg_color=self.colors['danger']
        ).pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="� Export Report",
            command=self.export_history,
            width=120,
            height=30,
            fg_color=self.colors['info']
        ).pack(side=tk.LEFT, padx=5)
        
        # History list
        self.history_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color=self.colors['surface']
        )
        self.history_frame.pack(fill=tk.BOTH, expand=True)

    def setup_favorites_tab(self):
        """Setup the favorites/bookmarks tab."""
        tab = self.tab_favorites
        
        # Header
        header_frame = ctk.CTkFrame(tab, height=60, fg_color=self.colors['surface'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="⭐ Favorite Playlists",
            font=self.fonts['title'],
            text_color=self.colors['text_primary']
        ).pack(pady=20)
        
        # Add current playlist to favorites
        add_frame = ctk.CTkFrame(tab, fg_color=self.colors['surface'])
        add_frame.pack(fill=tk.X, pady=(0, 15))
        
        buttons_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        buttons_frame.pack(pady=10)
        
        self.add_favorite_button = ctk.CTkButton(
            buttons_frame,
            text="⭐ Add Current Playlist",
            command=self.add_to_favorites,
            width=180,
            height=35,
            state=tk.DISABLED
        )
        self.add_favorite_button.pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Clear Favorites",
            command=self.clear_favorites,
            width=130,
            height=35,
            fg_color=self.colors['danger']
        ).pack(side=tk.LEFT, padx=5)
        
        # Favorites list
        self.favorites_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color=self.colors['surface']
        )
        self.favorites_frame.pack(fill=tk.BOTH, expand=True)

    def setup_settings_tab(self):
        """Setup the settings and preferences tab."""
        tab = self.tab_settings
        
        # Header
        header_frame = ctk.CTkFrame(tab, height=60, fg_color=self.colors['surface'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="⚙️ Settings & Preferences",
            font=self.fonts['title'],
            text_color=self.colors['text_primary']
        ).pack(pady=20)
        
        # Settings container
        settings_container = ctk.CTkFrame(tab, fg_color="transparent")
        settings_container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # General Settings
        general_frame = ctk.CTkFrame(settings_container, fg_color=self.colors['surface'])
        general_frame.pack(fill=tk.X, pady=(0, 15))
        
        ctk.CTkLabel(
            general_frame,
            text="🎛️ General Settings",
            font=self.fonts['heading']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Theme selection
        theme_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        theme_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        ctk.CTkLabel(theme_frame, text="🎨 Theme:", font=self.fonts['body']).pack(side=tk.LEFT)
        self.theme_var = ctk.StringVar(value="Dark")
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["Dark", "Light", "System"],
            variable=self.theme_var,
            command=self.change_theme,
            width=120
        )
        theme_menu.pack(side=tk.RIGHT)
        
        # Concurrent downloads
        concurrent_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        concurrent_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        ctk.CTkLabel(concurrent_frame, text="🔄 Max Concurrent Downloads:", font=self.fonts['body']).pack(side=tk.LEFT)
        self.concurrent_var = ctk.StringVar(value="3")
        concurrent_menu = ctk.CTkOptionMenu(
            concurrent_frame,
            values=["1", "2", "3", "4", "5"],
            variable=self.concurrent_var,
            width=80
        )
        concurrent_menu.pack(side=tk.RIGHT)
        
        # Auto-start downloads
        self.auto_start_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            general_frame,
            text="🚀 Auto-start downloads when playlist loads",
            variable=self.auto_start_var,
            font=self.fonts['body']
        ).pack(anchor="w", padx=15, pady=5)
        
        # Show notifications
        self.notifications_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            general_frame,
            text="🔔 Show completion notifications",
            variable=self.notifications_var,
            font=self.fonts['body']
        ).pack(anchor="w", padx=15, pady=(5, 15))
        
        # Advanced Settings
        advanced_frame = ctk.CTkFrame(settings_container, fg_color=self.colors['surface'])
        advanced_frame.pack(fill=tk.X, pady=(0, 15))
        
        ctk.CTkLabel(
            advanced_frame,
            text="🔧 Advanced Settings",
            font=self.fonts['heading']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Keep temporary files
        self.keep_temp_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            advanced_frame,
            text="📁 Keep temporary files for debugging",
            variable=self.keep_temp_var,
            font=self.fonts['body']
        ).pack(anchor="w", padx=15, pady=5)
        
        # Retry failed downloads
        retry_frame = ctk.CTkFrame(advanced_frame, fg_color="transparent")
        retry_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        ctk.CTkLabel(retry_frame, text="🔄 Retry failed downloads:", font=self.fonts['body']).pack(side=tk.LEFT)
        self.retry_var = ctk.StringVar(value="3")
        retry_menu = ctk.CTkOptionMenu(
            retry_frame,
            values=["0", "1", "2", "3", "5"],
            variable=self.retry_var,
            width=80
        )
        retry_menu.pack(side=tk.RIGHT)
        
        # Save/Reset buttons
        button_frame = ctk.CTkFrame(advanced_frame, fg_color="transparent")
        button_frame.pack(fill=tk.X, padx=15, pady=(10, 15))
        
        ctk.CTkButton(
            button_frame,
            text="💾 Save Settings",
            command=self.save_preferences,
            width=120,
            height=35,
            fg_color=self.colors['success']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ctk.CTkButton(
            button_frame,
            text="🔄 Reset to Defaults",
            command=self.reset_preferences,
            width=150,
            height=35,
            fg_color=self.colors['warning']
        ).pack(side=tk.LEFT)

    def setup_about_tab(self):
        """Setup the about and help tab."""
        tab = self.tab_about
        
        # Header with logo/icon
        header_frame = ctk.CTkFrame(tab, height=120, fg_color=self.colors['primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="🎵 YouTube Playlist Downloader Pro",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="Version 2.0 - Professional Edition",
            font=self.fonts['subtitle'],
            text_color="#FFE0E0"
        ).pack()
        
        # Content container
        content_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Features section
        features_frame = ctk.CTkFrame(content_frame, fg_color=self.colors['surface'])
        features_frame.pack(fill=tk.X, pady=(0, 15))
        
        ctk.CTkLabel(
            features_frame,
            text="✨ Features",
            font=self.fonts['heading']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        features_text = """
• 🎥 High-quality video downloads (up to 4K)
• 🎵 Audio-only downloads in multiple formats
• 📱 Batch processing for entire playlists
• 🖼️ Thumbnail and subtitle support
• 📂 Smart organization with folders
• 📜 Download history tracking
• ⭐ Favorite playlists management
• 🔄 Auto-retry for failed downloads
• 🎨 Modern dark/light theme support
• 📊 Real-time progress monitoring
        """
        
        ctk.CTkLabel(
            features_frame,
            text=features_text.strip(),
            font=self.fonts['body'],
            anchor="w",
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 15))
        
        # System info
        info_frame = ctk.CTkFrame(content_frame, fg_color=self.colors['surface'])
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ System Information",
            font=self.fonts['heading']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        try:
            import platform
            system_info = f"""
• Operating System: {platform.system()} {platform.release()}
• Python Version: {platform.python_version()}
• Architecture: {platform.machine()}
• Processor: {platform.processor()[:50]}...
            """
        except:
            system_info = "• System information unavailable"
        
        ctk.CTkLabel(
            info_frame,
            text=system_info.strip(),
            font=self.fonts['small'],
            anchor="w",
            justify="left",
            text_color=self.colors['text_secondary']
        ).pack(anchor="w", padx=15, pady=(0, 15))
        
        # Links and actions
        links_frame = ctk.CTkFrame(content_frame, fg_color=self.colors['surface'])
        links_frame.pack(fill=tk.X, pady=(0, 15))
        
        ctk.CTkLabel(
            links_frame,
            text="🔗 Links & Support",
            font=self.fonts['heading']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        buttons_frame = ctk.CTkFrame(links_frame, fg_color="transparent")
        buttons_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        ctk.CTkButton(
            buttons_frame,
            text="🌐 Visit GitHub",
            command=lambda: webbrowser.open("https://github.com/"),
            width=120,
            height=35
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ctk.CTkButton(
            buttons_frame,
            text="📁 Open Download Folder",
            command=self.open_download_folder,
            width=180,
            height=35,
            fg_color=self.colors['info']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ctk.CTkButton(
            buttons_frame,
            text="🔧 Check Dependencies",
            command=self.check_dependencies,
            width=160,
            height=35,
            fg_color=self.colors['accent']
        ).pack(side=tk.LEFT)

    def create_path_section(self, parent):
        """Create the download path selection section."""
        path_frame = ctk.CTkFrame(parent, fg_color=self.colors['surface'])
        path_frame.pack(fill=tk.X, pady=(0, 15))
        
        path_label = ctk.CTkLabel(
            path_frame,
            text="📁 Download Location:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        path_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        path_content_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_content_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.path_label = ctk.CTkLabel(
            path_content_frame,
            text=f"📂 {self.download_path}",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.path_button = ctk.CTkButton(
            path_content_frame,
            text="Change Folder",
            command=self.select_download_path,
            height=30,
            width=120,
            font=ctk.CTkFont(size=11)
        )
        self.path_button.pack(side=tk.RIGHT)

    def create_options_section(self, parent):
        """Create the download options section."""
        options_frame = ctk.CTkFrame(parent, fg_color=self.colors['surface'])
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        options_label = ctk.CTkLabel(
            options_frame,
            text="⚙️ Download Options:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        options_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        options_content = ctk.CTkFrame(options_frame, fg_color="transparent")
        options_content.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Quality selection
        quality_frame = ctk.CTkFrame(options_content, fg_color="transparent")
        quality_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ctk.CTkLabel(quality_frame, text="Quality:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.quality_var = ctk.StringVar(value="Best Quality")
        self.quality_dropdown = ctk.CTkOptionMenu(
            quality_frame,
            values=["Best Quality", "1080p", "720p", "480p", "Audio Only (MP3)"],
            variable=self.quality_var,
            width=150
        )
        self.quality_dropdown.pack(anchor="w", pady=(5, 0))
        
        # Global audio only option
        audio_frame = ctk.CTkFrame(options_content, fg_color="transparent")
        audio_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        self.global_audio_var = ctk.BooleanVar()
        self.global_audio_checkbox = ctk.CTkCheckBox(
            audio_frame,
            text="Download All as MP3",
            variable=self.global_audio_var,
            font=ctk.CTkFont(size=12)
        )
        self.global_audio_checkbox.pack(pady=10)

    def create_status_section(self, parent):
        """Create the status display section."""
        status_frame = ctk.CTkFrame(parent, height=60, fg_color=self.colors['surface'])
        status_frame.pack(fill=tk.X, pady=(0, 15))
        status_frame.pack_propagate(False)
        
        # Status text
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="📋 Ready - Paste a playlist URL and click 'Load Playlist' to begin",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=15, fill=tk.X, expand=True)
        
        # Progress stats
        stats_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        stats_frame.pack(side=tk.RIGHT, padx=15, pady=10)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Ready",
            font=ctk.CTkFont(size=11)
        )
        self.stats_label.pack()

    def create_video_list_section(self, parent):
        """Create the scrollable video list section."""
        list_label = ctk.CTkLabel(
            parent,
            text="📺 Playlist Videos:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        list_label.pack(anchor="w", pady=(0, 10))
        
        # Scrollable frame for videos with custom styling
        self.video_list_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color=self.colors['surface'],
            scrollbar_button_color=self.colors['primary']
        )
        self.video_list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

    def create_control_buttons(self, parent):
        """Create the main control buttons."""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill=tk.X, pady=(0, 15))

        # Left side buttons
        left_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_buttons.pack(side=tk.LEFT)

        self.download_all_button = ctk.CTkButton(
            left_buttons,
            text="⬇️ Download All",
            command=self.download_all,
            state=tk.DISABLED,
            height=40,
            width=150,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.colors['success']
        )
        self.download_all_button.pack(side=tk.LEFT, padx=(0, 10))

        self.cancel_all_button = ctk.CTkButton(
            left_buttons,
            text="⏹️ Cancel All",
            command=self.cancel_all,
            state=tk.DISABLED,
            height=40,
            width=120,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.colors['danger']
        )
        self.cancel_all_button.pack(side=tk.LEFT)

        # Right side buttons
        right_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_buttons.pack(side=tk.RIGHT)

        self.clear_button = ctk.CTkButton(
            right_buttons,
            text="🗑️ Clear List",
            command=self.clear_video_list,
            height=40,
            width=120,
            font=ctk.CTkFont(size=13),
            fg_color=self.colors['warning']
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))

        self.refresh_button = ctk.CTkButton(
            right_buttons,
            text="🔄 Refresh",
            command=self.refresh_playlist,
            height=40,
            width=100,
            font=ctk.CTkFont(size=13)
        )
        self.refresh_button.pack(side=tk.LEFT)

    def create_footer(self, parent):
        """Create the footer section."""
        footer_frame = ctk.CTkFrame(parent, height=30, fg_color="transparent")
        footer_frame.pack(fill=tk.X)
        footer_frame.pack_propagate(False)
        
        # Left side - version info
        version_label = ctk.CTkLabel(
            footer_frame,
            text="YouTube Playlist Downloader Pro v2.0",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        version_label.pack(side=tk.LEFT)
        
        # Right side - copyright
        copyright_label = ctk.CTkLabel(
            footer_frame,
            text=f"© {datetime.now().year} - Professional Edition",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        copyright_label.pack(side=tk.RIGHT)

    def select_download_path(self):
        """Opens a file dialog to select the download directory."""
        selected_path = filedialog.askdirectory(title="Select Download Directory")
        if selected_path:
            self.download_path = selected_path
            self.path_label.configure(text=f"📂 {self.download_path}")

    def clear_video_list(self):
        """Clear the video list."""
        if self.download_processes:
            if messagebox.askyesno("Confirm Clear", "There are active downloads. Are you sure you want to clear the list?"):
                self.cancel_all()
            else:
                return
        
        for widget in self.video_list_frame.winfo_children():
            widget.destroy()
        
        self.video_widgets.clear()
        self.download_processes.clear()
        self.video_info_list = []
        self.total_videos = 0
        self.completed_downloads = 0
        self.failed_downloads = 0
        
        self.status_label.configure(text="📋 List cleared - Ready for new playlist")
        self.update_stats_display()
        self.download_all_button.configure(state=tk.DISABLED)

    def refresh_playlist(self):
        """Refresh the current playlist."""
        url = self.url_entry.get()
        if url:
            self.clear_video_list()
            self.start_fetch_thread()
        else:
            messagebox.showwarning("No URL", "Please enter a playlist URL first.")

    def update_stats_display(self):
        """Update the statistics display."""
        if self.total_videos > 0:
            self.stats_label.configure(
                text=f"Total: {self.total_videos} | ✅ {self.completed_downloads} | ❌ {self.failed_downloads} | 🔄 {len(self.download_processes)}"
            )
        else:
            self.stats_label.configure(text="Ready")

    def create_context_menu(self):
        """Creates and binds the right-click context menu for the URL entry."""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut", command=lambda: self.url_entry.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Copy", command=lambda: self.url_entry.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Paste", command=self.paste_from_clipboard)

        # Bind the right-click event to the URL entry widget
        self.url_entry.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        """Displays the context menu at the mouse cursor position."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def paste_from_clipboard(self):
        """Gets content from the clipboard and pastes it into the URL entry."""
        try:
            clipboard_content = self.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard_content)
        except tk.TclError:
            # Handle cases where clipboard is empty or non-text content
            pass

    def start_fetch_thread(self):
        """Initiates fetching playlist titles in a separate thread."""
        if self.is_fetching:
            return
        
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a playlist URL.")
            return

        # Basic URL validation
        if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be']):
            messagebox.showerror("Invalid URL", "Please enter a valid YouTube playlist URL.")
            return

        self.is_fetching = True
        self.load_button.configure(state=tk.DISABLED, text="🔄 Loading...")
        self.status_label.configure(text="🔍 Analyzing playlist structure...")
        
        # Clear previous video widgets
        for widget in self.video_list_frame.winfo_children():
            widget.destroy()
        self.video_widgets.clear()

        fetch_thread = threading.Thread(target=self.fetch_playlist_titles, args=(url,))
        fetch_thread.daemon = True
        fetch_thread.start()

    def get_ytdlp_command(self):
        """Get the appropriate yt-dlp command based on installation method."""
        try:
            # Try using yt-dlp as a command
            subprocess.run(["yt-dlp", "--version"], 
                          check=True, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
            return ["yt-dlp"]
        except (FileNotFoundError, subprocess.CalledProcessError):
            # Fall back to using Python module
            return [sys.executable, "-m", "yt_dlp"]

    def fetch_playlist_titles(self, url):
        """Fetches video titles and URLs from a playlist using yt-dlp with enhanced error handling."""
        try:
            ytdlp_cmd = self.get_ytdlp_command()
            command = ytdlp_cmd + [
                "--flat-playlist", 
                "-j", 
                "--no-warnings",
                "--ignore-errors",
                url
            ]
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True
            )

            self.video_info_list = []
            error_count = 0
            
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    try:
                        video_json = json.loads(line)
                        if 'title' in video_json and 'url' in video_json:
                            self.video_info_list.append({
                                'title': video_json['title'],
                                'url': video_json['url'],
                                'duration': video_json.get('duration', 'Unknown'),
                                'uploader': video_json.get('uploader', 'Unknown'),
                                'view_count': video_json.get('view_count', 0)
                            })
                    except json.JSONDecodeError:
                        error_count += 1
                        continue
            
            process.wait()
            
            # Schedule UI updates on main thread
            self.after(0, lambda: self.display_videos(error_count))

        except FileNotFoundError:
            self.after(0, lambda: messagebox.showerror(
                "yt-dlp Not Found", 
                "yt-dlp is not installed or not in your system's PATH.\n\nPlease install it using:\npip install yt-dlp\n\nOr run the setup script: python setup.py"
            ))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch playlist:\n{str(e)}"))
        finally:
            self.is_fetching = False
            self.after(0, lambda: self.load_button.configure(state=tk.NORMAL, text="🔍 Load Playlist"))

    def format_duration(self, duration):
        """Format duration from seconds to readable format."""
        if duration == 'Unknown' or duration is None:
            return 'Unknown'
        
        try:
            duration = int(duration)
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes:02d}:{seconds:02d}"
        except (ValueError, TypeError):
            return 'Unknown'

    def format_view_count(self, view_count):
        """Format view count to readable format."""
        if not view_count or view_count == 0:
            return "Unknown"
        
        try:
            count = int(view_count)
            if count >= 1000000:
                return f"{count/1000000:.1f}M"
            elif count >= 1000:
                return f"{count/1000:.1f}K"
            else:
                return str(count)
        except (ValueError, TypeError):
            return "Unknown"

    def display_videos(self, error_count=0):
        """Displays fetched video titles with enhanced UI and download options."""
        if self.video_info_list:
            self.total_videos = len(self.video_info_list)
            self.completed_downloads = 0
            self.failed_downloads = 0
            
            status_text = f"✅ Found {len(self.video_info_list)} videos. Ready to download."
            if error_count > 0:
                status_text += f" ({error_count} entries skipped)"
            
            self.status_label.configure(text=status_text)
            self.update_stats_display()
            self.download_all_button.configure(state=tk.NORMAL)
            
            for i, video_info in enumerate(self.video_info_list, 1):
                video_url = video_info['url']
                
                # Main video frame with enhanced styling
                video_frame = ctk.CTkFrame(
                    self.video_list_frame, 
                    height=100,
                    fg_color=self.colors['background'],
                    border_width=1,
                    border_color="#404040"
                )
                video_frame.pack(fill=tk.X, pady=5, padx=5)
                video_frame.pack_propagate(False)
                
                # Left section - Video info
                info_frame = ctk.CTkFrame(video_frame, fg_color="transparent")
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Video number and title
                title_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                title_frame.pack(fill=tk.X, anchor="w")
                
                number_label = ctk.CTkLabel(
                    title_frame,
                    text=f"{i:02d}.",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=self.colors['primary'],
                    width=30
                )
                number_label.pack(side=tk.LEFT)
                
                title_text = video_info['title'][:80] + "..." if len(video_info['title']) > 80 else video_info['title']
                title_label = ctk.CTkLabel(
                    title_frame,
                    text=title_text,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    anchor="w"
                )
                title_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
                
                # Video details
                details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                details_frame.pack(fill=tk.X, anchor="w", pady=(5, 0))
                
                duration = self.format_duration(video_info.get('duration'))
                uploader = video_info.get('uploader', 'Unknown')[:20] + "..." if len(video_info.get('uploader', 'Unknown')) > 20 else video_info.get('uploader', 'Unknown')
                views = self.format_view_count(video_info.get('view_count'))
                
                details_text = f"⏱️ {duration} | 👤 {uploader} | 👀 {views} views"
                details_label = ctk.CTkLabel(
                    details_frame,
                    text=details_text,
                    font=ctk.CTkFont(size=10),
                    text_color="gray",
                    anchor="w"
                )
                details_label.pack(anchor="w")
                
                # Progress and status
                progress_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                progress_frame.pack(fill=tk.X, anchor="w", pady=(5, 0))
                
                status_label = ctk.CTkLabel(
                    progress_frame,
                    text="Ready",
                    font=ctk.CTkFont(size=10),
                    anchor="w"
                )
                status_label.pack(anchor="w")
                
                progress_bar = ctk.CTkProgressBar(
                    progress_frame,
                    height=8,
                    progress_color=self.colors['primary']
                )
                progress_bar.set(0)
                progress_bar.pack(fill=tk.X, pady=(2, 0))
                
                # Right section - Controls
                controls_frame = ctk.CTkFrame(video_frame, fg_color="transparent", width=200)
                controls_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
                controls_frame.pack_propagate(False)
                
                # Options
                options_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
                options_frame.pack(fill=tk.X)
                
                # Audio only checkbox
                audio_only_var = ctk.BooleanVar(value=False)
                audio_checkbox = ctk.CTkCheckBox(
                    options_frame,
                    text="Audio Only (MP3)",
                    variable=audio_only_var,
                    font=ctk.CTkFont(size=10)
                )
                audio_checkbox.pack(anchor="w", pady=(0, 5))
                
                # Quality selection for individual video
                quality_var = ctk.StringVar(value="Best")
                quality_option = ctk.CTkOptionMenu(
                    options_frame,
                    values=["Best", "1080p", "720p", "480p"],
                    variable=quality_var,
                    width=120,
                    height=25,
                    font=ctk.CTkFont(size=10)
                )
                quality_option.pack(anchor="w", pady=(0, 10))
                
                # Buttons
                button_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
                button_frame.pack(fill=tk.X)
                
                download_button = ctk.CTkButton(
                    button_frame,
                    text="⬇️ Download",
                    command=lambda url=video_url: self.start_single_download(url),
                    height=30,
                    width=120,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    fg_color=self.colors['success']
                )
                download_button.pack(fill=tk.X, pady=(0, 5))

                cancel_button = ctk.CTkButton(
                    button_frame,
                    text="⏹️ Cancel",
                    command=lambda url=video_url: self.cancel_single_download(url),
                    state=tk.DISABLED,
                    height=25,
                    width=120,
                    font=ctk.CTkFont(size=10),
                    fg_color=self.colors['danger']
                )
                cancel_button.pack(fill=tk.X)
                
                # Store widget references
                self.video_widgets[video_url] = {
                    'video_frame': video_frame,
                    'status_label': status_label,
                    'progress_bar': progress_bar,
                    'download_button': download_button,
                    'cancel_button': cancel_button,
                    'audio_only_var': audio_only_var,
                    'quality_var': quality_var,
                }
        else:
            self.status_label.configure(text="❌ No videos found in playlist.")
            self.download_all_button.configure(state=tk.DISABLED)

    def start_single_download(self, video_url):
        """Prepares and starts the download of a single video with enhanced options."""
        if video_url in self.download_processes:
            return
        
        self.download_all_button.configure(state=tk.DISABLED)
        self.cancel_all_button.configure(state=tk.NORMAL)
        
        widgets = self.video_widgets[video_url]
        widgets['download_button'].configure(state=tk.DISABLED)
        widgets['cancel_button'].configure(state=tk.NORMAL)
        widgets['status_label'].configure(text="🔄 Initializing...")
        widgets['video_frame'].configure(border_color=self.colors['primary'])

        download_thread = threading.Thread(target=self.run_download, args=(video_url,))
        download_thread.daemon = True
        download_thread.start()

    def run_download(self, video_url):
        """Executes the yt-dlp command for a single video with enhanced features."""
        widgets = self.video_widgets[video_url]
        full_output = []
        
        try:
            # Build command with enhanced options
            ytdlp_cmd = self.get_ytdlp_command()
            command = ytdlp_cmd + ["--newline"]
            
            # Output template with download path
            output_template = os.path.join(self.download_path, "%(title)s.%(ext)s")
            command.extend(["-o", output_template])

            # Determine format based on global and individual settings
            audio_only = self.global_audio_var.get() or widgets['audio_only_var'].get()
            
            if audio_only:
                command.extend([
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "--audio-quality", "192K"
                ])
            else:
                # Quality selection
                quality = widgets['quality_var'].get()
                global_quality = self.quality_var.get()
                
                if global_quality == "Audio Only (MP3)":
                    command.extend([
                        "--extract-audio", 
                        "--audio-format", "mp3",
                        "--audio-quality", "192K"
                    ])
                else:
                    if quality == "Best" or global_quality == "Best Quality":
                        command.extend(["-f", "best[ext=mp4]"])
                    elif quality == "1080p":
                        command.extend(["-f", "best[height<=1080][ext=mp4]"])
                    elif quality == "720p":
                        command.extend(["-f", "best[height<=720][ext=mp4]"])
                    elif quality == "480p":
                        command.extend(["-f", "best[height<=480][ext=mp4]"])

            # Add additional options
            command.extend([
                "--no-playlist",
                "--write-description",
                "--write-info-json"
            ])
            
            command.append(video_url)

            # Start download process
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.download_processes[video_url] = process
            
            # Progress tracking
            progress_regex = re.compile(r'\[download\]\s+(\d+\.\d+)%')
            speed_regex = re.compile(r'(\d+(?:\.\d+)?(?:K|M|G)?iB/s)')
            eta_regex = re.compile(r'ETA\s+(\d+:\d+)')
            
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                
                full_output.append(line)
                line = line.strip()
                
                if process.poll() is not None and not line:
                    break

                # Update progress
                progress_match = progress_regex.search(line)
                if progress_match:
                    try:
                        percentage = float(progress_match.group(1)) / 100.0
                        
                        # Extract speed and ETA
                        speed_match = speed_regex.search(line)
                        eta_match = eta_regex.search(line)
                        
                        speed_text = speed_match.group(1) if speed_match else "N/A"
                        eta_text = eta_match.group(1) if eta_match else "N/A"
                        
                        status_text = f"⬇️ {percentage*100:.1f}% | 🚀 {speed_text} | ⏱️ {eta_text}"
                        
                        self.after(0, lambda p=percentage: widgets['progress_bar'].set(p))
                        self.after(0, lambda s=status_text: widgets['status_label'].configure(text=s))
                        
                    except (ValueError, IndexError):
                        pass
                elif '[ExtractAudio]' in line:
                    self.after(0, lambda: widgets['status_label'].configure(text="🎵 Extracting audio..."))
                elif '[ffmpeg]' in line and 'Destination:' in line:
                    self.after(0, lambda: widgets['status_label'].configure(text="🔄 Processing..."))
                elif any(keyword in line.lower() for keyword in ['error', 'failed', 'unable']):
                    self.after(0, lambda l=line: widgets['status_label'].configure(text=f"⚠️ {l[:50]}..."))
            
            process.wait()
            
            # Determine success
            combined_output = "".join(full_output)
            is_success = (process.returncode == 0 or 
                         any(indicator in combined_output for indicator in [
                             '[download] 100%',
                             '[ExtractAudio] Destination:',
                             '[ffmpeg] Destination:'
                         ]))
            
            # Update UI based on result
            if is_success:
                self.after(0, lambda: self._handle_successful_download(video_url))
            else:
                self.after(0, lambda: self._handle_failed_download(video_url, combined_output))

        except Exception as e:
            self.after(0, lambda: self._handle_download_error(video_url, str(e)))
        finally:
            if video_url in self.download_processes:
                del self.download_processes[video_url]
            
            self.after(0, lambda: self._cleanup_download_ui(video_url))
            self.after(0, self._check_global_buttons_state)

    def _handle_successful_download(self, video_url):
        """Handle successful download UI updates."""
        widgets = self.video_widgets[video_url]
        widgets['status_label'].configure(text="✅ Download completed!")
        widgets['progress_bar'].set(1.0)
        widgets['video_frame'].configure(border_color=self.colors['success'])
        self.completed_downloads += 1
        self.update_stats_display()

    def _handle_failed_download(self, video_url, error_output):
        """Handle failed download UI updates."""
        widgets = self.video_widgets[video_url]
        error_msg = "Download failed"
        if "ERROR:" in error_output:
            error_lines = [line for line in error_output.split('\n') if 'ERROR:' in line]
            if error_lines:
                error_msg = error_lines[-1].replace('ERROR:', '').strip()[:50]
        
        widgets['status_label'].configure(text=f"❌ {error_msg}")
        widgets['progress_bar'].set(0)
        widgets['video_frame'].configure(border_color=self.colors['danger'])
        self.failed_downloads += 1
        self.update_stats_display()

    def _handle_download_error(self, video_url, error_message):
        """Handle download exception UI updates."""
        widgets = self.video_widgets[video_url]
        widgets['status_label'].configure(text=f"⚠️ Error: {error_message[:30]}...")
        widgets['progress_bar'].set(0)
        widgets['video_frame'].configure(border_color=self.colors['warning'])
        self.failed_downloads += 1
        self.update_stats_display()

    def _cleanup_download_ui(self, video_url):
        """Clean up download UI elements."""
        if video_url in self.video_widgets:
            widgets = self.video_widgets[video_url]
            widgets['download_button'].configure(state=tk.NORMAL)
            widgets['cancel_button'].configure(state=tk.DISABLED)


    def download_all(self):
        """Starts downloading all videos in the loaded playlist with enhanced options."""
        if not hasattr(self, 'video_info_list') or not self.video_info_list:
            messagebox.showwarning("No Videos", "Please load a playlist first.")
            return
        
        # Confirm download
        response = messagebox.askyesno(
            "Confirm Download", 
            f"Are you sure you want to download all {len(self.video_info_list)} videos?\n\n"
            f"Download path: {self.download_path}"
        )
        
        if not response:
            return
        
        self.download_all_button.configure(state=tk.DISABLED)
        self.cancel_all_button.configure(state=tk.NORMAL)
        self.status_label.configure(text="🚀 Starting batch download...")
        
        # Reset counters
        self.completed_downloads = 0
        self.failed_downloads = 0
        self.update_stats_display()
        
        # Start downloads with a small delay between each
        for i, video_info in enumerate(self.video_info_list):
            video_url = video_info['url']
            if video_url not in self.download_processes:
                # Use after() to stagger the start times slightly
                self.after(i * 500, lambda url=video_url: self.start_single_download(url))

    def cancel_single_download(self, video_url):
        """Terminates the subprocess for a specific video download with enhanced feedback."""
        if video_url in self.download_processes:
            process = self.download_processes[video_url]
            try:
                process.terminate()
                widgets = self.video_widgets[video_url]
                widgets['status_label'].configure(text="🛑 Cancelling...")
                widgets['progress_bar'].set(0)
                widgets['video_frame'].configure(border_color=self.colors['warning'])
                
                # Give process time to terminate gracefully
                self.after(2000, lambda: self._force_kill_process(video_url, process))
            except Exception as e:
                print(f"Error cancelling download: {e}")

    def _force_kill_process(self, video_url, process):
        """Force kill a process if it hasn't terminated gracefully."""
        try:
            if process.poll() is None:  # Process still running
                process.kill()
        except Exception:
            pass

    def cancel_all(self):
        """Terminates all active download subprocesses with enhanced feedback."""
        if not self.download_processes:
            return
        
        response = messagebox.askyesno(
            "Confirm Cancel", 
            f"Are you sure you want to cancel all {len(self.download_processes)} active downloads?"
        )
        
        if not response:
            return
        
        self.status_label.configure(text="🛑 Cancelling all downloads...")
        
        # Create a list to avoid dictionary size change during iteration
        processes_to_cancel = list(self.download_processes.items())
        
        for video_url, process in processes_to_cancel:
            try:
                process.terminate()
                if video_url in self.video_widgets:
                    widgets = self.video_widgets[video_url]
                    widgets['status_label'].configure(text="🛑 Cancelled")
                    widgets['progress_bar'].set(0)
                    widgets['video_frame'].configure(border_color=self.colors['warning'])
            except Exception as e:
                print(f"Error cancelling download for {video_url}: {e}")

    def monitor_downloads(self):
        """Enhanced download monitoring with better state management."""
        self._check_global_buttons_state()
        
        # Update overall progress if downloads are active
        if self.download_processes:
            active_count = len(self.download_processes)
            self.status_label.configure(
                text=f"📥 Downloading... {active_count} active downloads"
            )
        elif hasattr(self, 'video_info_list') and self.video_info_list and self.completed_downloads + self.failed_downloads > 0:
            if self.completed_downloads + self.failed_downloads == len(self.video_info_list):
                self.status_label.configure(text="✅ All downloads completed!")
        
        # Reschedule
        self.after(500, self.monitor_downloads)

    def _check_global_buttons_state(self):
        """Enhanced global button state management."""
        has_active_downloads = bool(self.download_processes)
        has_videos = hasattr(self, 'video_info_list') and bool(self.video_info_list)
        
        if not has_active_downloads:
            if has_videos:
                self.download_all_button.configure(state=tk.NORMAL)
            else:
                self.download_all_button.configure(state=tk.DISABLED)
            self.cancel_all_button.configure(state=tk.DISABLED)
        else:
            self.download_all_button.configure(state=tk.DISABLED)
            self.cancel_all_button.configure(state=tk.NORMAL)

    def create_context_menu(self):
        """Enhanced context menu for URL entry."""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="✂️ Cut", command=lambda: self.url_entry.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="📋 Copy", command=lambda: self.url_entry.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="📥 Paste", command=self.paste_from_clipboard)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Clear", command=lambda: self.url_entry.delete(0, tk.END))

        self.url_entry.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        """Enhanced context menu display."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def paste_from_clipboard(self):
        """Enhanced clipboard paste with validation."""
        try:
            clipboard_content = self.clipboard_get().strip()
            if clipboard_content:
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, clipboard_content)
                
                # Auto-validate if it looks like a YouTube URL
                if any(domain in clipboard_content.lower() for domain in ['youtube.com', 'youtu.be']):
                    self.url_entry.configure(border_color=self.colors['success'])
                    self.after(1000, lambda: self.url_entry.configure(border_color=""))
        except tk.TclError:
            messagebox.showwarning("Clipboard Error", "Could not access clipboard content.")

    # === ENHANCED FUNCTIONALITY METHODS ===

    def setup_tooltips(self):
        """Setup tooltips for better user experience."""
        # This would require a tooltip library, simplified for now
        pass

    def load_preferences(self):
        """Load user preferences from file."""
        try:
            prefs_file = os.path.join(os.path.expanduser("~"), ".youtube_downloader_prefs.json")
            if os.path.exists(prefs_file):
                with open(prefs_file, 'r') as f:
                    prefs = json.load(f)
                    self.download_path = prefs.get('download_path', self.download_path)
                    # Load other preferences...
        except:
            pass

    def save_preferences(self):
        """Save user preferences to file."""
        try:
            prefs = {
                'download_path': self.download_path,
                'theme': getattr(self, 'theme_var', ctk.StringVar()).get() if hasattr(self, 'theme_var') else 'Dark',
                'concurrent_downloads': int(getattr(self, 'concurrent_var', ctk.StringVar(value='3')).get()) if hasattr(self, 'concurrent_var') else 3,
                'auto_start': getattr(self, 'auto_start_var', ctk.BooleanVar()).get() if hasattr(self, 'auto_start_var') else False,
                'notifications': getattr(self, 'notifications_var', ctk.BooleanVar(value=True)).get() if hasattr(self, 'notifications_var') else True,
                'keep_temp': getattr(self, 'keep_temp_var', ctk.BooleanVar()).get() if hasattr(self, 'keep_temp_var') else False,
                'retry_count': int(getattr(self, 'retry_var', ctk.StringVar(value='3')).get()) if hasattr(self, 'retry_var') else 3
            }
            prefs_file = os.path.join(os.path.expanduser("~"), ".youtube_downloader_prefs.json")
            with open(prefs_file, 'w') as f:
                json.dump(prefs, f, indent=2)
            self.show_notification("✅ Settings saved successfully!", "success")
        except Exception as e:
            self.show_notification(f"❌ Failed to save settings: {str(e)}", "error")

    def reset_preferences(self):
        """Reset preferences to default values."""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to default values?"):
            # Reset all variables to defaults if they exist
            if hasattr(self, 'theme_var'):
                self.theme_var.set("Dark")
            if hasattr(self, 'concurrent_var'):
                self.concurrent_var.set("3")
            if hasattr(self, 'auto_start_var'):
                self.auto_start_var.set(False)
            if hasattr(self, 'notifications_var'):
                self.notifications_var.set(True)
            if hasattr(self, 'keep_temp_var'):
                self.keep_temp_var.set(False)
            if hasattr(self, 'retry_var'):
                self.retry_var.set("3")
            self.show_notification("🔄 Settings reset to defaults", "info")

    def paste_url_from_clipboard(self):
        """Paste URL from clipboard."""
        try:
            clipboard_text = self.clipboard_get()
            if 'youtube.com' in clipboard_text or 'youtu.be' in clipboard_text:
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, clipboard_text)
                self.validate_url()
                self.show_notification("📋 URL pasted from clipboard", "info")
            else:
                self.show_notification("❌ No valid YouTube URL found in clipboard", "warning")
        except:
            self.show_notification("❌ Failed to access clipboard", "error")

    def validate_url(self, event=None):
        """Validate YouTube URL in real-time."""
        url = self.url_entry.get().strip()
        if not url:
            if hasattr(self, 'url_status'):
                self.url_status.configure(text="")
            return
            
        if 'youtube.com/playlist' in url or 'youtube.com/watch' in url:
            if hasattr(self, 'url_status'):
                self.url_status.configure(text="✅ Valid", text_color=self.colors['success'])
        else:
            if hasattr(self, 'url_status'):
                self.url_status.configure(text="⚠️ Invalid URL", text_color=self.colors['warning'])

    def clear_all(self):
        """Clear all fields and reset the interface."""
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all data and stop downloads?"):
            self.url_entry.delete(0, tk.END)
            self.cancel_all_downloads()
            for widget in self.video_list_frame.winfo_children():
                widget.destroy()
            self.video_widgets.clear()
            self.video_data.clear()
            self.current_playlist_info.clear()
            if hasattr(self, 'playlist_info_frame'):
                self.playlist_info_frame.pack_forget()
            self.update_statistics()
            self.status_label.configure(text="📋 Ready - Paste a playlist URL to begin")

    def open_download_folder(self):
        """Open the download folder in file explorer."""
        try:
            os.makedirs(self.download_path, exist_ok=True)
            if sys.platform == "win32":
                os.startfile(self.download_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.download_path])
            else:
                subprocess.run(["xdg-open", self.download_path])
        except Exception as e:
            self.show_notification(f"❌ Failed to open folder: {str(e)}", "error")

    def refresh_playlist(self):
        """Refresh the current playlist."""
        url = self.url_entry.get().strip()
        if url:
            self.start_fetch_thread()
        else:
            self.show_notification("❌ No playlist URL to refresh", "warning")

    def on_quality_change(self, value):
        """Handle quality selection change."""
        if "Audio Only" in value and hasattr(self, 'subtitle_var'):
            self.subtitle_var.set(False)
            if hasattr(self, 'thumbnail_var'):
                self.thumbnail_var.set(True)  # Keep thumbnails for audio
        self.show_notification(f"🎥 Quality set to: {value}", "info")

    def change_view_mode(self, mode):
        """Change the video list view mode."""
        # This would change how videos are displayed
        self.show_notification(f"👁️ View changed to: {mode}", "info")

    def select_all_videos(self):
        """Select all videos in the list."""
        for video_id, widget_data in self.video_widgets.items():
            if 'checkbox' in widget_data:
                widget_data['checkbox'].select()

    def select_no_videos(self):
        """Deselect all videos in the list."""
        for video_id, widget_data in self.video_widgets.items():
            if 'checkbox' in widget_data:
                widget_data['checkbox'].deselect()

    def download_selected(self):
        """Download only selected videos."""
        selected_videos = []
        for video_id, widget_data in self.video_widgets.items():
            if 'checkbox' in widget_data and widget_data['checkbox'].get():
                selected_videos.append(video_id)
        
        if not selected_videos:
            self.show_notification("❌ No videos selected", "warning")
            return
            
        self.show_notification(f"⬇️ Starting download of {len(selected_videos)} selected videos", "info")
        # Implementation would go here

    def pause_all_downloads(self):
        """Pause all active downloads."""
        # Implementation for pausing downloads
        self.show_notification("⏸️ All downloads paused", "info")

    def add_to_favorites(self):
        """Add current playlist to favorites."""
        if self.current_playlist_info:
            favorite = {
                'title': self.current_playlist_info.get('title', 'Unknown'),
                'url': self.url_entry.get(),
                'video_count': self.current_playlist_info.get('video_count', 0),
                'added_date': datetime.now().isoformat()
            }
            self.favorites.append(favorite)
            self.save_favorites()
            if hasattr(self, 'refresh_favorites_display'):
                self.refresh_favorites_display()
            self.show_notification("⭐ Added to favorites", "success")

    def save_favorites(self):
        """Save favorites to file."""
        try:
            favorites_file = os.path.join(os.path.expanduser("~"), ".youtube_downloader_favorites.json")
            with open(favorites_file, 'w') as f:
                json.dump(self.favorites, f, indent=2)
        except:
            pass

    def change_theme(self, theme):
        """Change the application theme."""
        if theme == "Dark":
            ctk.set_appearance_mode("dark")
        elif theme == "Light":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("system")
        
        self.show_notification(f"🎨 Theme changed to: {theme}", "info")

    def check_dependencies(self):
        """Check and display dependency status."""
        dependencies = {
            "yt-dlp": "YouTube downloader",
            "customtkinter": "Modern GUI framework",
            "Pillow": "Image processing",
            "requests": "HTTP requests"
        }
        
        status_window = ctk.CTkToplevel(self)
        status_window.title("🔧 Dependency Status")
        status_window.geometry("400x300")
        status_window.attributes('-topmost', True)
        
        ctk.CTkLabel(
            status_window,
            text="🔧 Dependency Status",
            font=self.fonts['heading']
        ).pack(pady=20)
        
        status_frame = ctk.CTkScrollableFrame(status_window)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        for module, description in dependencies.items():
            try:
                __import__(module)
                status = "✅ Installed"
                color = self.colors['success']
            except ImportError:
                status = "❌ Missing"
                color = self.colors['danger']
            
            item_frame = ctk.CTkFrame(status_frame, fg_color=self.colors['surface'])
            item_frame.pack(fill=tk.X, pady=2)
            
            ctk.CTkLabel(
                item_frame,
                text=f"{module}: {description}",
                font=self.fonts['body']
            ).pack(side=tk.LEFT, padx=10, pady=5)
            
            ctk.CTkLabel(
                item_frame,
                text=status,
                font=self.fonts['small'],
                text_color=color
            ).pack(side=tk.RIGHT, padx=10, pady=5)

    def show_notification(self, message, type_="info"):
        """Show a temporary notification."""
        # Simple status update for now
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
            
            # Auto-clear after 3 seconds
            def clear_notification():
                try:
                    current_text = self.status_label.cget("text")
                    if current_text == message:  # Only clear if it hasn't changed
                        self.status_label.configure(text="📋 Ready")
                except:
                    pass
            
            self.after(3000, clear_notification)

    def update_statistics(self):
        """Update the statistics display."""
        total = len(self.video_widgets)
        completed = sum(1 for widget_data in self.video_widgets.values() 
                       if widget_data.get('status') == 'completed')
        failed = sum(1 for widget_data in self.video_widgets.values() 
                    if widget_data.get('status') == 'failed')
        
        if hasattr(self, 'stats_total_label'):
            self.stats_total_label.configure(text=f"Total: {total}")
        if hasattr(self, 'stats_completed_label'):
            self.stats_completed_label.configure(text=f"✅ Completed: {completed}")
        if hasattr(self, 'stats_failed_label'):
            self.stats_failed_label.configure(text=f"❌ Failed: {failed}")
        
        # Update progress bar
        if hasattr(self, 'progress_bar'):
            if total > 0:
                progress = completed / total
                self.progress_bar.set(progress)
            else:
                self.progress_bar.set(0)


if __name__ == "__main__":
    try:
        app = YouTubeDownloaderApp()
        app.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Application Error", f"Failed to start application:\n{e}")
