import os
from PIL import Image

src_path = r'C:\\SchoolProject\\GestureDrive\\assets\\screenshots\\dashboard.png'

if not os.path.exists(src_path):
    print('FAIL: source file missing')
    exit(1)

try:
    # Open original (JPEG data)
    img = Image.open(src_path)
    img.load()
    # Preserve dimensions and quality (no resizing). Convert to RGBA if needed.
    if img.mode in ('RGBA', 'RGB'):
        out_img = img
    else:
        out_img = img.convert('RGBA')
    # Save as PNG overwriting same path
    out_img.save(src_path, format='PNG')
    # Verify
    verify_img = Image.open(src_path)
    fmt = verify_img.format
    size = verify_img.size
    fsize = os.path.getsize(src_path)
    print('PASS')
    print('Format:', fmt)
    print('Dimensions:', size)
    print('File size (bytes):', fsize)
except Exception as e:
    print('FAIL')
    print('Error:', e)
