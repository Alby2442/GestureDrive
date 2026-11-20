import os
from PIL import Image

path = r'C:\\SchoolProject\\GestureDrive\\assets\\demo\\gesturedrive-promo.gif'
if not os.path.exists(path):
    print('GIF not found')
    exit(1)

im = Image.open(path)
print('Format:', im.format)
print('Size (W x H):', im.size)
frames = 0
durations = []
while True:
    frames += 1
    durations.append(im.info.get('duration', 0))
    try:
        im.seek(im.tell() + 1)
    except EOFError:
        break
print('Frames:', frames)
print('Durations (ms per frame):', durations)
print('Total duration (ms):', sum(durations))
print('File size (bytes):', os.path.getsize(path))
print('Loop count (0=forever):', im.info.get('loop', 0))
