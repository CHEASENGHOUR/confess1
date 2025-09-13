import qrcode
from PIL import Image, ImageDraw
import numpy as np
import math

def create_heart_mask(size):
    """Create a heart-shaped mask"""
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    
    # Heart shape parameters
    center_x, center_y = size // 2, size // 2
    scale = size / 400  # Scale factor based on image size
    
    # Create heart shape using mathematical formula
    points = []
    for angle in range(0, 360, 2):
        t = math.radians(angle)
        # Parametric heart equation
        x = 16 * (math.sin(t) ** 3)
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        
        # Scale and center the heart
        x = int(center_x + x * scale * 8)
        y = int(center_y - y * scale * 8)  # Negative because image Y is flipped
        points.append((x, y))
    
    # Draw filled heart
    draw.polygon(points, fill=255)
    return mask

def create_heart_qr(url, filename="heart_qr.png", fill_color="red", back_color="white"):
    """Generate a heart-shaped QR code"""
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for better masking
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color='black', back_color='white')
    
    # Resize to standard size
    size = 400
    qr_img = qr_img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Create heart mask
    heart_mask = create_heart_mask(size)
    
    # Create colored background
    background = Image.new('RGB', (size, size), back_color)
    
    # Create heart-colored layer
    heart_layer = Image.new('RGB', (size, size), fill_color)
    
    # Apply QR code pattern to heart layer
    qr_array = np.array(qr_img)
    heart_array = np.array(heart_layer)
    
    # Where QR is black (0), make heart darker
    dark_areas = qr_array < 128
    heart_array[dark_areas] = heart_array[dark_areas] * 0.3  # Make QR areas darker
    
    heart_layer = Image.fromarray(heart_array.astype('uint8'))
    
    # Composite the layers using the heart mask
    result = Image.composite(heart_layer, background, heart_mask)
    
    # Add a decorative border
    border_size = 20
    final_size = size + 2 * border_size
    final_img = Image.new('RGB', (final_size, final_size), back_color)
    final_img.paste(result, (border_size, border_size))
    
    # Add small hearts around the border
    draw = ImageDraw.Draw(final_img)
    
    # Save the image
    final_img.save(filename, dpi=(300, 300))  # High resolution
    print(f"Heart-shaped QR code saved as '{filename}'")
    return final_img

def create_simple_heart_qr(url, filename="simple_heart_qr.png"):
    """Create a simpler heart QR code with better readability"""
    
    # Generate QR code with maximum error correction
    qr = qrcode.QRCode(
        version=3,  # Larger version for better error correction
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color='#FF1493', back_color='white')  # Pink QR code
    
    # Resize
    size = 400
    qr_img = qr_img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Create heart overlay (semi-transparent)
    heart_overlay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(heart_overlay)
    
    # Draw heart outline
    center_x, center_y = size // 2, size // 2
    scale = size / 400
    
    points = []
    for angle in range(0, 360, 1):
        t = math.radians(angle)
        x = 16 * (math.sin(t) ** 3)
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        x = int(center_x + x * scale * 8)
        y = int(center_y - y * scale * 8)
        points.append((x, y))
    
    # Draw thick heart outline
    for i in range(len(points)):
        next_i = (i + 1) % len(points)
        draw.line([points[i], points[next_i]], fill=(255, 20, 147, 180), width=8)
    
    # Convert QR to RGBA and composite with heart outline
    qr_rgba = qr_img.convert('RGBA')
    result = Image.alpha_composite(qr_rgba, heart_overlay)
    
    # Convert back to RGB
    final_img = Image.new('RGB', result.size, 'white')
    final_img.paste(result, mask=result.split()[-1])
    
    final_img.save(filename, dpi=(300, 300))
    print(f"Heart-outlined QR code saved as '{filename}'")
    return final_img

# Example usage
if __name__ == "__main__":
    # Your URL
    url = "https://confess1-amber.vercel.app/"
    
    print("Generating heart-shaped QR codes...")
    
    # Method 1: Heart-shaped QR (artistic but may be harder to scan)
    create_heart_qr(url, "heart_shaped_qr.png", fill_color="#FF69B4", back_color="white")
    
    # Method 2: Regular QR with heart outline (better scanning reliability)
    create_simple_heart_qr(url, "heart_outline_qr.png")
    
    # Method 3: Different color variations
    create_heart_qr(url, "red_heart_qr.png", fill_color="#FF0000", back_color="#FFE4E6")
    create_heart_qr(url, "pink_heart_qr.png", fill_color="#FF1493", back_color="#FFF0F5")
    
    print("\n✨ All QR codes generated successfully!")
    print("\nFiles created:")
    print("1. heart_shaped_qr.png - Full heart shape (artistic)")
    print("2. heart_outline_qr.png - QR with heart outline (reliable)")
    print("3. red_heart_qr.png - Red heart variation")
    print("4. pink_heart_qr.png - Pink heart variation")
    print("\n💡 Tip: Test all versions to see which scans best on your devices!")