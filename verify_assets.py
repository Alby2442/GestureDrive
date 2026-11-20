import os
from PIL import Image, ImageSequence
import sys

base = r'C:\\SchoolProject\\GestureDrive'
files = [
    ('assets/icons/app_icon.png', 'PNG'),
    ('assets/branding/gesturedrive-banner.png', 'PNG'),
    ('assets/demo/gesturedrive-promo.gif', 'GIF'),
    ('assets/screenshots/dashboard.png', 'PNG'),
    ('assets/screenshots/gesture-control.png', 'PNG'),
]

for rel, expected_ext in files:
    path = os.path.join(base, rel)
    print(f'Checking {rel}')
    if not os.path.exists(path):
        print('  MISSING')
        continue
    try:
        if expected_ext == 'GIF':
            im = Image.open(path)
            im.verify()
            # reopen for size and frames
            im = Image.open(path)
            frames = sum(1 for _ in ImageSequence.Iterator(im))
            width, height = im.size
            print(f'  Format: {im.format}')
            print(f'  Dimensions: {width}x{height}')
            print(f'  Frames: {frames}')
        else:
            im = Image.open(path)
            im.verify()
            im = Image.open(path)
            print(f'  Format: {im.format}')
            print(f'  Dimensions: {im.size[0]}x{im.size[1]}')
        print(f'  File size (bytes): {os.path.getsize(path)}')
    except Exception as e:
        print('  INVALID:', e)

print('DONE')
