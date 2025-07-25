# 🎵 YouTube Playlist Downloader Pro

A professional-grade YouTube playlist downloader with both CLI and GUI interfaces. Features a modern, clean design with advanced download options and real-time progress tracking.

## ✨ Features

### 🖥️ CLI Version (`youtube_Download-cli.py`)
- **Professional UI**: Clean, colorized terminal interface with progress bars
- **Smart Selection**: Download all videos or select specific ranges (e.g., 1-5, 8, 10-15)
- **Quality Options**: Choose from best quality, audio-only, or custom formats
- **Enhanced Progress**: Real-time download progress with speed and ETA
- **Error Handling**: Robust error handling with detailed feedback
- **Directory Selection**: Choose download location (current, Downloads, or custom)
- **Download Summary**: Complete statistics after download completion

### 🎨 GUI Version (`youtube_downloader-gui.py`)
- **Modern Dark Theme**: Professional dark interface using CustomTkinter
- **Enhanced Video Cards**: Rich video information display with thumbnails metadata
- **Individual Controls**: Per-video download options and quality settings
- **Real-time Progress**: Live progress bars with speed and ETA for each video
- **Batch Operations**: Download all videos with staggered start times
- **Smart Status**: Color-coded status indicators and progress tracking
- **Global Options**: Set quality and format preferences for all downloads
- **Context Menus**: Right-click functionality for improved usability

### 📋 Common Features
- **Multiple Formats**: MP4 video downloads and MP3 audio extraction
- **Quality Selection**: Best, 1080p, 720p, 480p, and audio-only options
- **Robust Downloads**: Resume capability and error recovery
- **Path Management**: Customizable download directories
- **Progress Tracking**: Real-time download progress and statistics
- **Error Handling**: Comprehensive error reporting and recovery

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### 🎯 Easy Setup (Recommended)

#### Option 1: Automatic Setup Script
1. **Download** this repository
2. **Run the setup script**:
   
   **Windows:**
   ```batch
   # Double-click setup.bat OR run in Command Prompt:
   setup.bat
   ```
   
   **All Platforms:**
   ```bash
   python setup.py
   ```

#### Option 2: Manual Installation
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install yt-dlp customtkinter
   ```

### 🔧 Alternative Installation
If you prefer to install dependencies separately:
```bash
# Core dependency for downloading
pip install yt-dlp

# GUI dependency (only needed for GUI version)
pip install customtkinter
```

### ⚡ Quick Fix for "yt-dlp Not Found" Error
If you see the error "yt-dlp is not installed or not in your system's PATH":

1. **Run this command**:
   ```bash
   pip install yt-dlp
   ```

2. **Or use the setup script**:
   ```bash
   python setup.py
   ```

3. **Verify installation**:
   ```bash
   yt-dlp --version
   ```

## 📖 Usage

### 🖥️ CLI Version
```bash
python youtube_Download-cli.py
```

**Features:**
- Enter YouTube playlist URL
- Choose download directory
- Select video quality and format
- Pick specific videos or download all
- Monitor real-time progress

**Example Usage:**
1. Run the script
2. Choose download location (current, Downloads, or custom path)
3. Paste playlist URL
4. Select download options (Best Quality, Audio Only, or Custom)
5. Choose videos to download:
   - Type `all` for all videos
   - Type `1,3,5` for specific videos
   - Type `1-10` for a range
   - Type `1,3-5,8` for mixed selection

### 🎨 GUI Version
```bash
python youtube_downloader-gui.py
```

**Features:**
- Modern dark theme interface
- Paste playlist URL in the input field
- Set global download options
- View detailed video information
- Individual video controls
- Real-time progress monitoring
- Batch download management

**Usage Steps:**
1. Launch the GUI application
2. Set download path using "Change Folder" button
3. Configure global download options (quality, audio-only)
4. Paste YouTube playlist URL
5. Click "Load Playlist" to fetch video information
6. Choose individual video settings or use global settings
7. Download individual videos or use "Download All"

## ⚙️ Configuration Options

### Quality Settings
- **Best Quality**: Downloads the highest available quality (usually 1080p+ MP4)
- **1080p**: Maximum 1080p resolution
- **720p**: Maximum 720p resolution  
- **480p**: Maximum 480p resolution
- **Audio Only**: Extracts MP3 audio at 192kbps

### Download Paths
- **Current Directory**: Downloads to the script's location
- **Downloads Folder**: Uses system Downloads folder
- **Custom Path**: Specify any directory

### File Naming
Files are saved with the original video title as the filename, with special characters sanitized for filesystem compatibility.

## 🛠️ Advanced Features

### CLI Advanced Usage
- **Keyboard Interruption**: Press Ctrl+C to safely cancel downloads
- **Resume Downloads**: Automatically resumes interrupted downloads
- **Error Recovery**: Skips failed videos and continues with the next

### GUI Advanced Features
- **Staggered Downloads**: Batch downloads start with 500ms delays to prevent overwhelming
- **Visual Feedback**: Color-coded borders show download status
- **Context Menus**: Right-click URL field for copy/paste operations
- **Auto-validation**: Automatic URL validation with visual feedback

## 🐛 Troubleshooting

### ⚠️ Common Issues & Quick Fixes

#### 1. **"yt-dlp not found" or "yt-dlp is not installed" error**
This is the most common issue. Here are the solutions:

**Quick Fix:**
```bash
pip install yt-dlp
```

**If that doesn't work, try:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Then install yt-dlp
python -m pip install yt-dlp
```

**Windows users can also:**
- Double-click `setup.bat` in the project folder
- Or run `python setup.py`

#### 2. **GUI not working or CustomTkinter errors**:
```bash
pip install --upgrade customtkinter
```

#### 3. **"pip is not recognized" error (Windows)**:
- Make sure Python is installed with "Add to PATH" option checked
- Or use: `python -m pip install yt-dlp customtkinter`

#### 4. **Download failures**:
- Check internet connection
- Verify the playlist URL is public
- Try updating yt-dlp: `pip install --upgrade yt-dlp`
- Some videos may be region-restricted or private

#### 5. **Permission errors**:
- Choose a different download directory
- Run Command Prompt/Terminal as administrator
- Ensure you have write permissions to the download folder

#### 6. **Python version issues**:
- Ensure Python 3.7 or higher is installed
- Check version: `python --version`
- Update Python if needed from [python.org](https://www.python.org/)

### System Requirements
- **Windows**: Windows 10 or higher
- **macOS**: macOS 10.14 or higher  
- **Linux**: Any modern distribution
- **Python**: 3.7 or higher
- **Internet**: Stable connection for downloading

## 📝 Notes

- **Playlist Privacy**: Only public playlists can be downloaded
- **Video Availability**: Some videos may be region-restricted or private
- **File Sizes**: High-quality videos can be large; ensure adequate storage space
- **Rate Limiting**: The tool respects YouTube's rate limits to prevent blocking

## 🔧 Technical Details

### Dependencies
- **yt-dlp**: Core downloading functionality
- **customtkinter**: Modern GUI framework
- **tkinter**: Built-in GUI library (included with Python)
- **subprocess**: Process management
- **threading**: Concurrent operations
- **json**: Data parsing
- **re**: Regular expressions for progress parsing

### Architecture
- **Modular Design**: Separate CLI and GUI implementations
- **Thread Safety**: Background downloads don't block the UI
- **Error Resilience**: Comprehensive exception handling
- **Resource Management**: Proper cleanup of processes and resources

## 📄 License

This project is provided as-is for educational and personal use. Please respect YouTube's Terms of Service and only download content you have permission to download.

## 🤝 Contributing

Feel free to submit issues, feature requests, or improvements. This is a community-driven project focused on providing a professional YouTube downloading experience.

## 🎯 Version History

### v2.0 (Current)
- ✨ Complete UI redesign with professional dark theme
- 🚀 Enhanced progress tracking with speed and ETA
- 🎵 Improved audio extraction with quality options
- 📊 Real-time statistics and batch operation support
- 🛠️ Advanced error handling and recovery
- 🎨 Modern CustomTkinter GUI with enhanced UX

### v1.0 (Previous)
- Basic CLI and GUI functionality
- Simple download options
- Basic progress tracking

---

**Enjoy downloading your favorite YouTube playlists with style! 🎵✨**
