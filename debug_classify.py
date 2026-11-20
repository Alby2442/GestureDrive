import sys, os
sys.path.append('C:/SchoolProject/GestureDrive')
from modules.gesture_recognition import GestureRecognizer
from tests.synthetic import closed_fist
rec = GestureRecognizer()
lm = closed_fist()
print('hand size', rec._hand_size(lm))
print('thumb_extended?', (lm[4][0] < lm[2][0]))
print('classify', rec._classify_pose(lm))
