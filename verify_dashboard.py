import os
from PIL import Image

path = r'C:\\SchoolProject\\GestureDrive\\assets\\screenshots\\dashboard.png'

exists = os.path.exists(path)
print('Exists:', exists)
if not exists:
    exit(0)

try:
    im = Image.open(path)
    im.verify()  # verify integrity
    fmt = im.format
    # Need to reopen to get size after verify
    im = Image.open(path)
    size = im.size
    print('Format:', fmt)
    print('Dimensions:', size)
    print('File size (bytes):', os.path.getsize(path))
    print('PASS')
except Exception as e:
    print('Error:', e)
    print('FAIL')
