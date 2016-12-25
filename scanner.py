import cv2
import numpy as np
from matplotlib import pyplot as plt
import pylab as pl

NAME = "source2"

# class RawImg:
#
#     def __init__(self, img):
#         self.cv2.imread()

im = cv2.imread(NAME+".jpeg", 0)

th = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            1, 29, 8)



# plt.subplot(1,3,1), plt.imshow(im, "gray")
plt.subplot(1,2,1), plt.imshow(th, "gray")
cv2.imwrite(NAME+"-b.jpeg", th)

contours0, hierarchy = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
h, w = im.shape[:2]
candidates = im.copy()

approximations = {}

for i in range(len(contours0)):
    # aproximate countours to polygons
    approximation = cv2.approxPolyDP(contours0[i], 4, True)

    # has the polygon 4 sides?
    if (not (len(approximation) == 4)):
        continue
    # is the polygon convex ?
    if (not cv2.isContourConvex(approximation)):
        continue

    approximations[cv2.contourArea(approximation)] = approximation

sizes = sorted(list(approximations.keys()))

NUM_PAPERS = 2

for i in range(NUM_PAPERS):
    approximation = approximations[sizes[-i-1]]
    print(approximation)
    print("$$$$$$")
    for j in range(len(approximation)):
        cv2.line(candidates,
                (approximation[(j%4)][0][0],   approximation[(j%4)][0][1]),
                (approximation[(j+1)%4][0][0], approximation[(j+1)%4][0][1]),
                (255, 255, 255), 2)



#show image
plt.subplot(1,2,2), plt.imshow(candidates, "gray")

plt.show()


    # import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# img = cv2.imread('source1-b.png',0)
# img2 = img.copy()
# template = cv2.imread('ref1.png',0)
# w, h = template.shape[::-1]
#
# # All the 6 methods for comparison in a list
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
#
# for meth in methods:
#     img = img2.copy()
#     method = eval(meth)
#
#     # Apply template Matching
#     res = cv2.matchTemplate(img,template,method)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#
#     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#         top_left = min_loc
#     else:
#         top_left = max_loc
#     bottom_right = (top_left[0] + w, top_left[1] + h)
#
#     cv2.rectangle(img,top_left, bottom_right, 255, 2)
#
#     plt.subplot(121),plt.imshow(res,cmap = 'gray')
#     plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
#     plt.subplot(122),plt.imshow(img,cmap = 'gray')
#     plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#     plt.suptitle(meth)
#
#     plt.show()