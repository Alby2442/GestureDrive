import os
from PIL import Image, ImageDraw, ImageFont

# Settings
width, height = 480, 270
bg_color = (10, 10, 40)  # dark blue
accent_color = (80, 0, 150)  # purple
frames = []
# Use a basic font (Pillow default)
font_large = ImageFont.load_default()
font_small = ImageFont.load_default()

def draw_centered(draw, text, y, font, fill):
    # Use textbbox to measure text dimensions (compatible with Pillow >=9)
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (width - w) // 2
    draw.text((x, y), text, font=font, fill=fill)

# Fade‑in helper (simple alpha simulation by blending with background)
for i in range(10):
    img = Image.new('RGB', (width, height), bg_color)
    d = ImageDraw.Draw(img)
    alpha = i / 9.0
    # Title fade‑in
    draw_centered(d, "GestureDrive", 80, font_large, (int(255*alpha), int(255*alpha), 255))
    frames.append(img)

# Subtitle fade‑in
for i in range(10):
    img = Image.new('RGB', (width, height), bg_color)
    d = ImageDraw.Draw(img)
    draw_centered(d, "GestureDrive", 80, font_large, (255, 255, 255))
    alpha = i / 9.0
    draw_centered(d, "Hand Gesture Controlled Hill Climb Racing", 130, font_small, (int(200*alpha), int(0*alpha), int(200*alpha)))
    frames.append(img)

# Open Palm description
for i in range(10):
    img = Image.new('RGB', (width, height), bg_color)
    d = ImageDraw.Draw(img)
    draw_centered(d, "GestureDrive", 80, font_large, (255, 255, 255))
    draw_centered(d, "Hand Gesture Controlled Hill Climb Racing", 130, font_small, (200, 0, 200))
    draw_centered(d, "Open Palm → Accelerate (RIGHT arrow key)", 180, font_small, (255, 200, 0))
    frames.append(img)

# Closed Fist description
for i in range(10):
    img = Image.new('RGB', (width, height), bg_color)
    d = ImageDraw.Draw(img)
    draw_centered(d, "GestureDrive", 80, font_large, (255, 255, 255))
    draw_centered(d, "Hand Gesture Controlled Hill Climb Racing", 130, font_small, (200, 0, 200))
    draw_centered(d, "Closed Fist → Brake (LEFT arrow key)", 180, font_small, (255, 200, 0))
    frames.append(img)

# Save GIF
out_path = os.path.join('C:\\SchoolProject\\GestureDrive', 'assets', 'demo', 'gesturedrive-promo.gif')
frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=150, loop=0)
print('GIF saved to', out_path)
