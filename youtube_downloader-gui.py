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

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Main application class
class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("YouTube Playlist Downloader Pro")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # Center window on screen
        self.center_window()
        
        # --- Variables ---
        self.download_processes = {}
        self.video_widgets = {}
        self.is_fetching = False
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.total_videos = 0
        self.completed_downloads = 0
        self.failed_downloads = 0
        
        # --- Styling ---
        self.setup_styles()
        
        # --- GUI Elements ---
        self.create_widgets()
        
        # --- Start monitoring downloads ---
        self.after(100, self.monitor_downloads)

    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        """Setup custom styling for the application."""
        # Custom colors
        self.colors = {
            'primary': "#1f538d",
            'secondary': "#14375e", 
            'success': "#2d5016",
            'warning': "#8b4513",
            'danger': "#8b1538",
            'background': "#212121",
            'surface': "#2b2b2b"
        }

    def create_widgets(self):
        # Main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section with title and logo
        self.create_header(main_container)
        
        # URL input section
        self.create_url_section(main_container)
        
        # Download path section
        self.create_path_section(main_container)
        
        # Options section
        self.create_options_section(main_container)
        
        # Status section
        self.create_status_section(main_container)
        
        # Video list section
        self.create_video_list_section(main_container)
        
        # Control buttons section
        self.create_control_buttons(main_container)
        
        # Footer section
        self.create_footer(main_container)
        
        # Initialize context menu
        self.create_context_menu()

    def create_header(self, parent):
        """Create the header section with title and description."""
        header_frame = ctk.CTkFrame(parent, height=80, fg_color=self.colors['primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🎵 YouTube Playlist Downloader Pro",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=(15, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Professional grade YouTube playlist downloading with advanced features",
            font=ctk.CTkFont(size=12),
            text_color="#E0E0E0"
        )
        subtitle_label.pack()

    def create_url_section(self, parent):
        """Create the URL input section."""
        url_frame = ctk.CTkFrame(parent, fg_color=self.colors['surface'])
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        url_label = ctk.CTkLabel(
            url_frame, 
            text="📎 Playlist URL:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        url_label.pack(anchor="w", padx=15, pady=(15, 5))

        # URL input with button in same row
        input_frame = ctk.CTkFrame(url_frame, fg_color="transparent")
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.url_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="https://www.youtube.com/playlist?list=...",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.load_button = ctk.CTkButton(
            input_frame,
            text="🔍 Load Playlist",
            command=self.start_fetch_thread,
            height=40,
            width=150,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.colors['primary']
        )
        self.load_button.pack(side=tk.RIGHT)

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

    def fetch_playlist_titles(self, url):
        """Fetches video titles and URLs from a playlist using yt-dlp with enhanced error handling."""
        try:
            command = [
                "yt-dlp", 
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
                "yt-dlp is not installed or not in your system's PATH.\n\nPlease install it using:\npip install yt-dlp"
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
            command = ["yt-dlp", "--newline"]
            
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


if __name__ == "__main__":
    try:
        app = YouTubeDownloaderApp()
        app.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Application Error", f"Failed to start application:\n{e}")
