import importlib
import sys

def get_version(pkg_name):
    try:
        mod = importlib.import_module(pkg_name)
        return getattr(mod, '__version__', 'unknown')
    except Exception as e:
        return f'error: {e}'

packages = {
    'numpy': 'numpy',
    'cv2': 'opencv-contrib-python',
    'mediapipe': 'mediapipe',
    'pyautogui': 'pyautogui',
}

print('Dependency verification:')
for import_name, pkg in packages.items():
    version = get_version(import_name)
    print(f'{pkg}: {version}')

# Ensure Python version
print('Python version:', sys.version.split()[0])
