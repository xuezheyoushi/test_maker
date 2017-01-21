import cv2
import numpy as np
from matplotlib import pyplot as plt
import pylab as pl
from pylibdmtx.pylibdmtx import decode


NUM_OPTIONS = 5
MARKED_THRESH = 1.5


class RawPhoto:

    img = None
    th = None
    paper_objs = []

    def __init__(self, raw_img):
        self.img = raw_img

    def get_papers(self, num_paper, num_questions=60):
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
            if len(approximation) != 4:
                continue
            if not cv2.isContourConvex(approximation):
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
            trans_matrix = cv2.getPerspectiveTransform(ref_pts, key_pts)
            paper = cv2.warpPerspective(self.img, trans_matrix, (875, 1240))
            self.paper_objs.append(PaperScan(paper, num_questions))
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
                transform[(r_id + 2) % 4], transform[(r_id + 3) % 4])


class PaperScan:

    '''
    This is the preprocessed single image for one test paper.
    '''

    img = None
    th = None
    th_inv = None
    test_id = None
    paper_id = None
    ans_imgs = []
    num_questions = 60
    name_img = None
    class_img = None
    marked_ans = None


    def __init__(self, paper_img, num_questions=60):
        self.img = paper_img
        self.num_questions = num_questions
        self.th_inv = cv2.adaptiveThreshold(paper_img, 255,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            1, 29, 8)
        self.th = 255 - self.th_inv
        self.read_datamatrix()
        self.name_img = self.th[122:180, 120:480]
        self.class_img = self.th[122:180, 570:670]

    def read_datamatrix(self):
        datamatrix_region = self.th[40:140, 740:840]
        content = decode(datamatrix_region, timeout=3)[0][0]
        self.test_id = content[:5]
        self.paper_id = content[5:]

    def read_answers(self):
        pass

    def remove_edges(self):
        scan_times = 22
        threshold = 0.5
        count = 0
        ans_img_trim = []
        for ans_img in self.ans_imgs:

            # cv2.imwrite("ans-img-trim-%d.png" % count, ans_img)

            h, w = ans_img.shape[:2]

            # TODO: reconstruct shitty code below

            # Top
            flag = False
            for t in range(scan_times):
                if sum(ans_img[t]) > threshold * w * 255:
                    flag = True
                else:
                    if flag:
                        break
            if t == scan_times - 1:
                t = 0

            # Bottom
            flag = False
            for b in range(scan_times):
                if sum(ans_img[- (b + 1)]) > threshold * w * 255:
                    flag = True
                else:
                    if flag:
                        break
            if b == scan_times - 1:
                b = 0

            # Left
            flag = False
            for l in range(scan_times):
                if sum(ans_img[:, l]) > threshold * h * 255:
                    flag = True
                else:
                    if flag:
                        break
            if l == scan_times - 1:
                l = 0

            # Right
            flag = False
            for r in range(scan_times):
                if sum(ans_img[:, - (r + 1)]) > threshold * h * 255:
                    flag = True
                else:
                    if flag:
                        break
            if r == scan_times - 1:
                r = 0

            trimmed = ans_img[t:h - b, l:w - r]
            kernel = np.ones((2, 2), np.uint8)
            # erosion = cv2.erode(trimmed, kernel, iterations=1)
            opening = cv2.morphologyEx(trimmed, cv2.MORPH_OPEN, kernel)

            # TODO: delete this
            cv2.imwrite("ans-img-trim-%d.png" % count, opening)
            count += 1
            ans_img_trim.append(ans_img[t:h - b, l:w - r])

        self.ans_imgs = ans_img_trim

    def segment(self):
        offset = 12
        col_keys = {0: [87, 227], 1: [266, 406], 2: [446, 586], 3: [624, 764]}
        for i in range(self.num_questions):
            col = int(i / 15)
            row = i % 15
            up = int(306 + row * ((1126 - 306) / (15 * 1.0))) - offset
            down = int(306 + (row + 1) * ((1126 - 306) / 15)) + offset
            left = col_keys[col][0] - offset
            right = col_keys[col][1] + offset
            ans_img = self.th_inv[up:down, left:right]
            self.ans_imgs.append(ans_img)
            cv2.imwrite("ans-img-%d.png" % i, ans_img)


    def read_filled_answers(self):
        for curr_img in self.ans_imgs:
            h, w = curr_img.shape[:2]
            partition_len = int(w / NUM_OPTIONS);
            brightnesses = [0] * NUM_OPTIONS
            for i in range(NUM_OPTIONS):
                for j in range(h):
                    begin_partition = partition_len * i
                    end_partition = partition_len * (i + 1)
                    for k in range(begin_partition, end_partition):
                        for row in range(h):
                            for col in range(partition_len):
                                brightnesses[i] += curr_img[row][col]
            min = min(brightnesses)
            res = []
            for i in range(NUM_OPTIONS):
                if brightnesses[i] > MARKED_THRESH * min:
                    res.append(i)
            if len(res) == 0:
                res = None
            elif len(res) == 1:
                res = res[0]






if __name__ == "__main__":

    test_img = cv2.imread("source7.jpeg", 0)
    rp = RawPhoto(test_img)
    rp.get_papers(4, 22)
    rp.paper_objs[1].segment()
    rp.paper_objs[1].remove_edges()
