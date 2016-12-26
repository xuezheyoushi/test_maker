import cv2
import numpy as np
from matplotlib import pyplot as plt
import pylab as pl
from pylibdmtx.pylibdmtx import decode


class RawPhoto:

    img = None
    th = None
    paper_objs = []

    def __init__(self, raw_img):
        self.img = raw_img

    def get_papers(self, num_paper):
        # Take threshold of the image
        self.th = cv2.adaptiveThreshold(self.img, 255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        1, 29, 8)
        # Find contours
        contours0, hir = cv2.findContours(self.th, cv2.RETR_LIST,
                                          cv2.CHAIN_APPROX_SIMPLE)
        # Approximate all rectangles
        approximations = {}
        for i in range(len(contours0)):
            # Approximate contours to polygons
            approximation = cv2.approxPolyDP(contours0[i], 4, True)
            # Has 4 sides? Convex?
            if (len(approximation) != 4):
                continue
            if (not cv2.isContourConvex(approximation)):
                continue
            approximations[cv2.contourArea(approximation)] = approximation
        # Get largest rectangles
        sizes = sorted(list(approximations.keys()))
        for i in range(num_paper):
            # Break if rectangle clearly not big enough
            if sizes[-i-1] < 0.7 * sizes[-1]:
                break
            approximation = approximations[sizes[-i-1]]
            raw_refs = self.get_refs(approximation)
            ref_pts = np.float32([[raw_refs[0][0], raw_refs[0][1]],
                                  [raw_refs[1][0], raw_refs[1][1]],
                                  [raw_refs[2][0], raw_refs[2][1]],
                                  [raw_refs[3][0], raw_refs[3][1]]])
            key_pts = np.float32([[764, 307], [49, 307],
                                  [49, 1128], [764, 1128]])
            M = cv2.getPerspectiveTransform(ref_pts, key_pts)
            paper = cv2.warpPerspective(self.img, M, (875, 1240))
            self.paper_objs.append(PaperScan(paper, i))
        # Print warning if not all detected
        if i != (num_paper - 1):
            print("WARNING: %d papers not detected." % (num_paper - 1 - i))

    def get_refs(self, approx):
        # Define cornor points
        A = approx[0][0]
        B = approx[1][0]
        C = approx[2][0]
        D = approx[3][0]
        # Define center points of edges
        E = (int((A[0] + B[0]) / 2), int((A[1] + B[1]) / 2))
        F = (int((B[0] + C[0]) / 2), int((B[1] + C[1]) / 2))
        G = (int((C[0] + D[0]) / 2), int((C[1] + D[1]) / 2))
        H = (int((D[0] + A[0]) / 2), int((D[1] + A[1]) / 2))
        # Define ref points
        I = int(G[0] + 1.053 * (E[0] - G[0])), int(G[1] + 1.053 * (E[1] - G[1]))
        J = int(H[0] + 1.053 * (F[0] - H[0])), int(H[1] + 1.053 * (F[1] - H[1]))
        K = int(E[0] + 1.053 * (G[0] - E[0])), int(E[1] + 1.053 * (G[1] - E[1]))
        L = int(F[0] + 1.053 * (H[0] - F[0])), int(F[1] + 1.053 * (H[1] - F[1]))
        # Check brightnesses
        brightnesses = []
        offset = int(0.012 * ((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2) ** 0.5)
        for pt in [I, J, K, L]:
            i_base = pt[0] - offset
            j_base = pt[1] - offset
            brightness = 0
            for i in range(offset * 2):
                for j in range(offset * 2):
                    brightness += self.img[j_base + j][i_base + i]
            brightnesses.append(brightness)
        # Orientate rectangle
        r_id = brightnesses.index(min(brightnesses))
        transform = {0: B, 1: C, 2: D, 3: A}
        return (transform[r_id], transform[(r_id + 1) % 4],
                transform[(r_id + 2) %4], transform[(r_id + 3) % 4])


class PaperScan:

    img = None
    th = None
    th_inv = None
    test_id = None
    paper_id = None
    answers = []

    def __init__(self, paper_img, i):
        self.img = paper_img
        cv2.imwrite("test%d.png" % i, paper_img)
        self.th_inv = cv2.adaptiveThreshold(paper_img, 255,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            1, 29, 8)
        self.th = 255 - self.th_inv
        self.read_datamatrix(i)

    def read_datamatrix(self, i):
        datamatrix_region = self.th[40:140, 740:840]
        content = decode(datamatrix_region, timeout=1)[0][0]
        self.test_id = content[:5]
        self.paper_id = content[5:]

    def read_answer(self, num_questions):
        pass


test_img = cv2.imread("source6.jpeg", 0)
rp = RawPhoto(test_img)
rp.get_papers(8)