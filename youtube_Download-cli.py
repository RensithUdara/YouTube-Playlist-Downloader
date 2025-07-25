import subprocess
import json
import sys
import os
import re
import time
from datetime import datetime
import shutil

# ANSI Color codes for better UI
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display an attractive banner."""
    banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            🎵 YouTube Playlist Downloader CLI 🎵            ║
║                                                              ║
║                    Professional Edition                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
{Colors.OKCYAN}Welcome to the most advanced YouTube playlist downloader!{Colors.ENDC}
{Colors.WARNING}Version 2.0 | Built with ❤️  | {datetime.now().strftime('%Y')}{Colors.ENDC}
"""
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed."""
    print(f"{Colors.OKCYAN}🔍 Checking dependencies...{Colors.ENDC}")
    
    try:
        # First try to import yt_dlp module
        import yt_dlp
        version = yt_dlp.version.__version__
        print(f"{Colors.OKGREEN}✅ yt-dlp found: {version}{Colors.ENDC}")
        return True
    except ImportError:
        # If import fails, try command line
        try:
            result = subprocess.run(["yt-dlp", "--version"], 
                                  check=True, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, 
                                  text=True)
            version = result.stdout.strip()
            print(f"{Colors.OKGREEN}✅ yt-dlp found: {version}{Colors.ENDC}")
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"{Colors.FAIL}❌ Error: yt-dlp is not installed or not in your system's PATH.{Colors.ENDC}")
            print(f"{Colors.WARNING}📦 Please install it by running: pip install yt-dlp{Colors.ENDC}")
            print(f"{Colors.WARNING}📦 Or run the setup script: python setup.py{Colors.ENDC}")
            return False

def get_download_directory():
    """Get and validate download directory."""
    while True:
        print(f"\n{Colors.OKBLUE}📁 Download Directory Options:{Colors.ENDC}")
        print("1. Current directory (default)")
        print("2. Downloads folder")
        print("3. Custom path")
        
        choice = input(f"\n{Colors.BOLD}Choose option (1-3) [1]: {Colors.ENDC}").strip()
        
        if choice == '' or choice == '1':
            return os.getcwd()
        elif choice == '2':
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            if os.path.exists(downloads_path):
                return downloads_path
            else:
                print(f"{Colors.WARNING}⚠️  Downloads folder not found, using current directory.{Colors.ENDC}")
                return os.getcwd()
        elif choice == '3':
            custom_path = input(f"{Colors.BOLD}Enter custom path: {Colors.ENDC}").strip()
            if os.path.exists(custom_path) and os.path.isdir(custom_path):
                return custom_path
            else:
                print(f"{Colors.FAIL}❌ Invalid path. Please try again.{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}❌ Invalid choice. Please try again.{Colors.ENDC}")

def main():
    """Main function to run the command-line interface."""
    
    clear_screen()
    print_banner()
    
    if not check_dependencies():
        input(f"\n{Colors.WARNING}Press Enter to exit...{Colors.ENDC}")
        sys.exit(1)
    
    download_dir = get_download_directory()
    print(f"{Colors.OKGREEN}📂 Downloads will be saved to: {download_dir}{Colors.ENDC}")
    
    while True:
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        playlist_url = input(f"\n{Colors.BOLD}🔗 Enter YouTube Playlist URL (or 'exit' to quit): {Colors.ENDC}")
        
        if playlist_url.lower() in ['exit', 'quit', 'q']:
            print(f"\n{Colors.OKCYAN}👋 Thank you for using YouTube Playlist Downloader!{Colors.ENDC}")
            break

        if not playlist_url.strip():
            print(f"{Colors.WARNING}⚠️  Please enter a valid URL.{Colors.ENDC}")
            continue

        print(f"\n{Colors.OKCYAN}🔍 Fetching playlist information...{Colors.ENDC}")
        videos = fetch_playlist_info(playlist_url)

        if videos:
            print(f"{Colors.OKGREEN}✅ Successfully found {len(videos)} videos!{Colors.ENDC}")
            selected_videos = prompt_for_selection(videos)
            if selected_videos:
                download_videos(selected_videos, download_dir)
        else:
            print(f"{Colors.FAIL}❌ Could not find any videos at that URL. Please try again.{Colors.ENDC}")

def get_ytdlp_command():
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

def fetch_playlist_info(url):
    """Fetches video titles and URLs from a playlist with enhanced error handling."""
    try:
        print(f"{Colors.OKCYAN}⏳ Analyzing playlist structure...{Colors.ENDC}")
        
        ytdlp_cmd = get_ytdlp_command()
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

        video_info_list = []
        error_count = 0
        
        for line in iter(process.stdout.readline, ''):
            if line.strip():
                try:
                    video_json = json.loads(line)
                    if 'title' in video_json and 'url' in video_json:
                        video_info_list.append({
                            'title': video_json['title'],
                            'url': video_json['url'],
                            'duration': video_json.get('duration', 'Unknown'),
                            'uploader': video_json.get('uploader', 'Unknown')
                        })
                except json.JSONDecodeError:
                    error_count += 1
                    continue
        
        process.wait()
        
        if error_count > 0:
            print(f"{Colors.WARNING}⚠️  Skipped {error_count} invalid entries{Colors.ENDC}")
        
        return video_info_list

    except Exception as e:
        print(f"{Colors.FAIL}❌ An error occurred while fetching info: {e}{Colors.ENDC}")
        return []

def format_duration(duration):
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

def prompt_for_selection(video_list):
    """Displays videos and prompts user for selection with enhanced UI."""
    print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}📹 VIDEOS FOUND IN PLAYLIST{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
    
    # Display header
    print(f"{Colors.BOLD}{'No.':<4} {'Title':<50} {'Duration':<10} {'Uploader':<15}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'-'*80}{Colors.ENDC}")
    
    for i, video in enumerate(video_list, 1):
        title = video['title'][:47] + "..." if len(video['title']) > 50 else video['title']
        duration = format_duration(video.get('duration', 'Unknown'))
        uploader = video.get('uploader', 'Unknown')[:12] + "..." if len(video.get('uploader', 'Unknown')) > 15 else video.get('uploader', 'Unknown')
        
        print(f"{Colors.OKCYAN}{i:<4}{Colors.ENDC} {title:<50} {duration:<10} {uploader:<15}")
    
    print(f"{Colors.OKBLUE}{'-'*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}Total videos: {len(video_list)}{Colors.ENDC}")
    
    # Selection options
    print(f"\n{Colors.OKGREEN}📋 Selection Options:{Colors.ENDC}")
    print("• Enter 'all' to download all videos")
    print("• Enter numbers: 1, 3, 5")
    print("• Enter ranges: 1-5, 10-15")
    print("• Combine: 1, 3-5, 8, 10-12")
    print("• Enter 'exit' to return to main menu")
    
    while True:
        selection_input = input(f"\n{Colors.BOLD}🎯 Your selection: {Colors.ENDC}").strip()
        
        if selection_input.lower() in ['exit', 'quit', 'back']:
            return None
        
        if selection_input.lower() == 'all':
            print(f"{Colors.OKGREEN}✅ Selected all {len(video_list)} videos{Colors.ENDC}")
            return video_list

        selected_indices = set()
        
        # Parse ranges and individual numbers
        parts = re.split(r'[,\s]+', selection_input)
        
        valid_input = True
        for part in parts:
            if not part:
                continue
            
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    if 1 <= start <= end <= len(video_list):
                        selected_indices.update(range(start, end + 1))
                    else:
                        print(f"{Colors.FAIL}❌ Invalid range: {part}. Please enter valid numbers (1-{len(video_list)}).{Colors.ENDC}")
                        valid_input = False
                        break
                except ValueError:
                    print(f"{Colors.FAIL}❌ Invalid range format: {part}. Use format like '5-8'.{Colors.ENDC}")
                    valid_input = False
                    break
            else:
                try:
                    index = int(part)
                    if 1 <= index <= len(video_list):
                        selected_indices.add(index)
                    else:
                        print(f"{Colors.FAIL}❌ Invalid number: {index}. Please enter a number between 1 and {len(video_list)}.{Colors.ENDC}")
                        valid_input = False
                        break
                except ValueError:
                    print(f"{Colors.FAIL}❌ Invalid input: {part}. Please use numbers, ranges, or 'all'.{Colors.ENDC}")
                    valid_input = False
                    break
        
        if valid_input and selected_indices:
            selected_videos = [video_list[i-1] for i in sorted(selected_indices)]
            print(f"{Colors.OKGREEN}✅ Selected {len(selected_videos)} videos{Colors.ENDC}")
            return selected_videos
        elif valid_input:
            print(f"{Colors.WARNING}⚠️  No videos selected. Please try again.{Colors.ENDC}")

def get_download_options():
    """Get user preferences for download quality and format."""
    print(f"\n{Colors.OKBLUE}⚙️  Download Options:{Colors.ENDC}")
    print("1. Best Quality (MP4)")
    print("2. Audio Only (MP3)")
    print("3. Custom Quality")
    
    while True:
        choice = input(f"\n{Colors.BOLD}Choose download option (1-3) [1]: {Colors.ENDC}").strip()
        
        if choice == '' or choice == '1':
            return {'format': 'best[ext=mp4]', 'audio_only': False, 'description': 'Best Quality MP4'}
        elif choice == '2':
            return {'format': 'bestaudio[ext=m4a]', 'audio_only': True, 'description': 'Audio Only MP3'}
        elif choice == '3':
            print("\nCustom Quality Options:")
            print("• 1080p: best[height<=1080]")
            print("• 720p: best[height<=720]")
            print("• 480p: best[height<=480]")
            custom = input("Enter custom format: ").strip()
            if custom:
                return {'format': custom, 'audio_only': False, 'description': f'Custom: {custom}'}
        
        print(f"{Colors.FAIL}❌ Invalid choice. Please try again.{Colors.ENDC}")

def progress_bar(current, total, bar_length=40):
    """Create a visual progress bar."""
    percent = float(current) / total
    arrow = '█' * int(round(percent * bar_length))
    spaces = '░' * (bar_length - len(arrow))
    return f"{Colors.OKGREEN}[{arrow}{spaces}] {percent*100:.1f}%{Colors.ENDC}"

def download_videos(videos_to_download, download_dir):
    """Downloads the selected videos with enhanced progress tracking."""
    if not videos_to_download:
        return
    
    # Get download options
    options = get_download_options()
    
    print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}🚀 STARTING DOWNLOADS{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}📂 Download Directory: {download_dir}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}🎯 Format: {options['description']}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}📊 Total Videos: {len(videos_to_download)}{Colors.ENDC}")
    
    successful_downloads = 0
    failed_downloads = 0
    start_time = time.time()
    
    ytdlp_cmd = get_ytdlp_command()
    
    for i, video in enumerate(videos_to_download, 1):
        print(f"\n{Colors.OKCYAN}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}📥 [{i}/{len(videos_to_download)}] Downloading:{Colors.ENDC}")
        print(f"{Colors.OKCYAN}🎵 {video['title'][:70]}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}{'='*80}{Colors.ENDC}")
        
        try:
            # Prepare command
            command = ytdlp_cmd + ["--newline"]
            
            # Add output template
            output_template = os.path.join(download_dir, "%(title)s.%(ext)s")
            command.extend(["-o", output_template])
            
            # Add format selection
            command.extend(["-f", options['format']])
            
            # Add audio extraction if needed
            if options['audio_only']:
                command.extend(["--extract-audio", "--audio-format", "mp3"])
            
            command.append(video['url'])
            
            # Execute download
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Track progress
            last_progress = 0
            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if line:
                    # Extract progress from yt-dlp output
                    if '[download]' in line and '%' in line:
                        try:
                            # Extract percentage
                            percent_match = re.search(r'(\d+(?:\.\d+)?)%', line)
                            if percent_match:
                                percent = float(percent_match.group(1))
                                if percent > last_progress:
                                    bar = progress_bar(percent, 100)
                                    print(f"\r{bar} {percent:.1f}%", end='', flush=True)
                                    last_progress = percent
                        except ValueError:
                            pass
                    elif any(keyword in line.lower() for keyword in ['error', 'failed', 'unable']):
                        print(f"\n{Colors.WARNING}⚠️  {line}{Colors.ENDC}")
            
            process.wait()
            
            if process.returncode == 0:
                print(f"\n{Colors.OKGREEN}✅ Download completed successfully!{Colors.ENDC}")
                successful_downloads += 1
            else:
                print(f"\n{Colors.FAIL}❌ Download failed (Exit Code: {process.returncode}){Colors.ENDC}")
                failed_downloads += 1
                
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}⚠️  Download interrupted by user{Colors.ENDC}")
            break
        except Exception as e:
            print(f"\n{Colors.FAIL}❌ An error occurred during download: {e}{Colors.ENDC}")
            failed_downloads += 1
    
    # Summary
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}📊 DOWNLOAD SUMMARY{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✅ Successful: {successful_downloads}{Colors.ENDC}")
    print(f"{Colors.FAIL}❌ Failed: {failed_downloads}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}⏱️  Total Time: {total_time:.1f} seconds{Colors.ENDC}")
    print(f"{Colors.OKBLUE}📂 Files saved to: {download_dir}{Colors.ENDC}")
    
    input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

if __name__ == "__main__":
    main()