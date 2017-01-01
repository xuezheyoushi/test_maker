import cv2
import numpy as np
# from matplotlib import pyplot as plt
import pylab as pl
from pylibdmtx.pylibdmtx import decode


img = cv2.imread("ans-img-53.png", 0)

h, w = img.shape[:2]

# Top
flag = False
for t in range(10):
    if sum(img[t]) > 0.7 * w * 255:
        flag = True
    else:
        if flag:
            break
if t == 9:
    t = 0

print(t)