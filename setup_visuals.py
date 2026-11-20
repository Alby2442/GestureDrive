import os
from PIL import Image, ImageSequence

base = r'C:\\SchoolProject\\GestureDrive'

# Uploaded source files
src_banner = r'C:\\Users\\albin\\.gemini\\antigravity\\brain\\a0fd2a32-a535-4f6c-af31-79a338f7f886\\.user_uploaded\\media_1795201048597_5cbfe0c2.jpg'
src_demo = r'C:\\Users\\albin\\.gemini\\antigravity\\brain\\a0fd2a32-a535-4f6c-af31-79a338f7f886\\.user_uploaded\\media_1795201068450_dc295e7d.png'
src_gesture = r'C:\\Users\\albin\\.gemini\\antigravity\\brain\\a0fd2a32-a535-4f6c-af31-79a338f7f886\\.user_uploaded\\media_1795201091226_09fdf05b.jpg'

# Destination paths
banner_dest = os.path.join(base, 'assets', 'branding', 'gesturedrive-banner.png')
demo_dest = os.path.join(base, 'assets', 'demo', 'gesturedrive-promo.gif')
gesture_dest = os.path.join(base, 'assets', 'screenshots', 'gesture-control.png')

# Ensure directories exist
os.makedirs(os.path.dirname(banner_dest), exist_ok=True)
os.makedirs(os.path.dirname(demo_dest), exist_ok=True)
os.makedirs(os.path.dirname(gesture_dest), exist_ok=True)

# 1. Convert banner JPEG to PNG
im = Image.open(src_banner)
im.save(banner_dest, format='PNG')
print('Banner saved as PNG')

# 2. Convert demo PNG to GIF (single‑frame)
im_demo = Image.open(src_demo)
# Ensure RGB (GIF does not support RGBA)
im_demo = im_demo.convert('RGB')
im_demo.save(demo_dest, format='GIF')
print('Demo saved as GIF')

# 3. Convert gesture JPEG to PNG
im_gesture = Image.open(src_gesture)
im_gesture.save(gesture_dest, format='PNG')
print('Gesture screenshot saved as PNG')
