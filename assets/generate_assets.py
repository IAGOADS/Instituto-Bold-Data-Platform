# assets/generate_assets.py
import os
from PIL import Image, ImageDraw, ImageFont

def create_styled_image(filename, width, height, bg_color, text, accent_color=None, text_size=20):
    """Generates a premium PNG image using Pillow with custom styling and text."""
    # Ensure parent folders exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Create image canvas
    img = Image.new('RGBA', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw simple corporate accent line or block if accent color provided
    if accent_color:
        draw.rectangle([0, height-6, width, height], fill=accent_color)
        draw.ellipse([width-15, 10, width-5, 20], fill=accent_color)
        
    # Draw high-fidelity textual representation (since fonts vary, we draw simple shapes and load default)
    try:
        font = ImageFont.load_default()
    except:
        font = None
        
    # Draw clean central text
    # Pillow draw.text uses simple rendering, we split lines to center
    words = text.split()
    y_text = height // 2 - 10
    
    for word in words:
        draw.text((width // 2 - len(word)*4, y_text), word, fill=(255, 255, 255, 255))
        y_text += 12
        
    # Save image
    img.save(filename, 'PNG')
    print(f"Created asset file: {filename}")

if __name__ == "__main__":
    # Get current script parent directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    logo_dir = os.path.join(base_dir, "assets", "logos")
    fav_dir = os.path.join(base_dir, "assets", "favicon")
    
    # Roxo Bold: #522f8b (RGB: 82, 47, 139)
    # Dourado Bold: #fb9e21 (RGB: 251, 158, 33)
    # Azul ADM: #004B87 (RGB: 0, 75, 135)
    
    # 1. Generate Instituto Bold logo
    create_styled_image(
        filename=os.path.join(logo_dir, "instituto_bold.png"),
        width=250,
        height=80,
        bg_color=(82, 47, 139, 255),
        text="INSTITUTO BOLD",
        accent_color=(251, 158, 33, 255)
    )
    
    # 2. Generate ADM logo
    create_styled_image(
        filename=os.path.join(logo_dir, "adm.png"),
        width=250,
        height=80,
        bg_color=(0, 75, 135, 255),
        text="ADM",
        accent_color=(251, 158, 33, 255)
    )
    
    # 3. Generate Favicon
    create_styled_image(
        filename=os.path.join(fav_dir, "favicon.png"),
        width=32,
        height=32,
        bg_color=(82, 47, 139, 255),
        text="IB",
        accent_color=(251, 158, 33, 255)
    )
    print("All branding assets generated successfully!")
