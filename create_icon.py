#!/usr/bin/env python3
"""
Icon Creator for YouTube Playlist Downloader Pro
Creates application icons in multiple sizes and formats.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_youtube_icon():
    """Create a professional YouTube-style icon for the application."""
    
    # Create icons directory
    os.makedirs("icons", exist_ok=True)
    
    # Icon sizes to create
    sizes = [16, 32, 48, 64, 128, 256]
    
    for size in sizes:
        # Create a new image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background circle with gradient effect
        # Red background (YouTube style)
        bg_color = (255, 0, 0, 255)  # YouTube red
        shadow_color = (200, 0, 0, 180)
        
        # Draw shadow
        shadow_size = int(size * 0.9)
        shadow_pos = ((size - shadow_size) // 2 + 2, (size - shadow_size) // 2 + 2)
        draw.ellipse([shadow_pos[0], shadow_pos[1], 
                     shadow_pos[0] + shadow_size, shadow_pos[1] + shadow_size], 
                    fill=shadow_color)
        
        # Draw main circle
        circle_size = int(size * 0.85)
        circle_pos = ((size - circle_size) // 2, (size - circle_size) // 2)
        draw.ellipse([circle_pos[0], circle_pos[1], 
                     circle_pos[0] + circle_size, circle_pos[1] + circle_size], 
                    fill=bg_color)
        
        # Draw play button triangle (white)
        play_color = (255, 255, 255, 255)
        center_x, center_y = size // 2, size // 2
        triangle_size = int(size * 0.25)
        
        # Triangle points (play button)
        triangle_points = [
            (center_x - triangle_size//2, center_y - triangle_size//2),
            (center_x - triangle_size//2, center_y + triangle_size//2),
            (center_x + triangle_size//2, center_y)
        ]
        draw.polygon(triangle_points, fill=play_color)
        
        # Add download arrow overlay
        arrow_color = (255, 255, 255, 200)
        arrow_size = int(size * 0.15)
        arrow_x = center_x + int(size * 0.2)
        arrow_y = center_y + int(size * 0.2)
        
        # Draw download arrow
        arrow_points = [
            (arrow_x, arrow_y - arrow_size//2),
            (arrow_x - arrow_size//2, arrow_y),
            (arrow_x + arrow_size//2, arrow_y),
        ]
        draw.polygon(arrow_points, fill=arrow_color)
        
        # Draw arrow stem
        stem_width = max(2, arrow_size // 4)
        draw.rectangle([arrow_x - stem_width//2, arrow_y - arrow_size, 
                       arrow_x + stem_width//2, arrow_y], fill=arrow_color)
        
        # Save icon
        img.save(f"icons/icon_{size}x{size}.png", "PNG")
        print(f"✅ Created icon_{size}x{size}.png")
    
    # Create ICO file for Windows
    try:
        # Load the largest icon
        large_icon = Image.open("icons/icon_256x256.png")
        
        # Create multi-size ICO file
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        icons = []
        
        for icon_size in icon_sizes:
            icon = large_icon.resize(icon_size, Image.Resampling.LANCZOS)
            icons.append(icon)
        
        # Save as ICO file
        icons[0].save("icons/app_icon.ico", format='ICO', sizes=icon_sizes)
        print("✅ Created app_icon.ico")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not create ICO file: {e}")
    
    print("\n🎨 Icon creation completed!")
    print("📁 Icons saved in 'icons/' directory")

def create_banner_image():
    """Create a banner image for the application."""
    
    # Create banner
    width, height = 800, 200
    img = Image.new('RGB', (width, height), (45, 45, 45))  # Dark background
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Draw gradient background
    for y in range(height):
        color_value = int(45 + (y / height) * 30)
        color = (color_value, color_value, color_value + 20)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Draw title text
    title = "YouTube Playlist Downloader Pro"
    subtitle = "Professional Edition • Desktop Application"
    
    # Get text dimensions
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    
    title_width = title_bbox[2] - title_bbox[0]
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    
    # Center text
    title_x = (width - title_width) // 2
    title_y = height // 2 - 40
    
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = height // 2 + 10
    
    # Draw text with shadow
    shadow_offset = 2
    draw.text((title_x + shadow_offset, title_y + shadow_offset), title, 
              fill=(0, 0, 0), font=title_font)
    draw.text((title_x, title_y), title, fill=(255, 255, 255), font=title_font)
    
    draw.text((subtitle_x + shadow_offset, subtitle_y + shadow_offset), subtitle, 
              fill=(0, 0, 0), font=subtitle_font)
    draw.text((subtitle_x, subtitle_y), subtitle, fill=(200, 200, 200), font=subtitle_font)
    
    # Add decorative elements
    # Draw some YouTube-style elements
    accent_color = (255, 0, 0)  # YouTube red
    
    # Left accent
    draw.rectangle([50, height//2 - 30, 70, height//2 + 30], fill=accent_color)
    
    # Right accent  
    draw.rectangle([width - 70, height//2 - 30, width - 50, height//2 + 30], fill=accent_color)
    
    # Save banner
    img.save("icons/banner.png", "PNG")
    print("✅ Created banner.png")

if __name__ == "__main__":
    print("🎨 Creating application icons...")
    print("=" * 50)
    
    try:
        create_youtube_icon()
        create_banner_image()
        
        print("\n🎉 All icons created successfully!")
        print("\n📋 Files created:")
        print("   • icons/icon_*x*.png - Various icon sizes")
        print("   • icons/app_icon.ico - Windows icon file")
        print("   • icons/banner.png - Application banner")
        
    except ImportError:
        print("❌ Error: PIL (Pillow) is required to create icons")
        print("📦 Install it with: pip install Pillow")
    except Exception as e:
        print(f"❌ Error creating icons: {e}")
    
    input("\nPress Enter to continue...")
