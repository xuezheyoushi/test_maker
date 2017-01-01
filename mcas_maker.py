from PIL import Image, ImageDraw, ImageFont
from hubarcode.datamatrix import DataMatrixEncoder
import os
from random import choice


class Test:

    def __init__(self, name, test_list):
        self.test_name = name
        self.test_id = len(test_list)
        self.copies = []
        self.stats = []

    def generate_copy(self, num_copies):
        for i in range(num_copies):
            copy = Copy(len(self.copies), self)
            self.copies.append(copy)

    def enter_keys(self, keys):
        self.keys = keys
        self.stats = [0] * (len(keys) + 1)

    def mark_all(self):
        count = 0
        for copy in self.copies:
            res = copy.mark(self.keys)
            for i in range(len(res)):
                self.stats[i] += res[i]
        for i in range(len(self.stats)):
            self.stats[i] = 100 * self.stats[i] / count

    def bind_pdf(self):
        pass


class Copy:

    ans = []
    res = []

    def __init__(self, copy_id, test_obj):

        # Initialize canvas
        im = Image.open("format.png")
        helvetica = ImageFont.truetype("helvetica-bold.ttf", 80)
        scp = ImageFont.truetype("source-code-pro-regular.ttf", 30)
        draw = ImageDraw.Draw(im)

        # Draw test name
        draw.text((95, 160), test_obj.test_name, fill=0, font=helvetica)

        # Init metadata
        display_test_id = '0' * (5 - len(str(test_obj.test_id))) + \
                          str(test_obj.test_id)
        display_copy_id = '0' * (3 - len(str(copy_id))) + str(copy_id)
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.pin = ""
        for i in range(4):
            self.pin += choice(chars)

        # Write metadata
        encoder = DataMatrixEncoder(display_test_id + display_copy_id)
        encoder.save("datamatrix_temp.png", cellsize=9)
        datamatrix = Image.open("datamatrix_temp.png")
        datamatrix = datamatrix.resize((180, 180), Image.ANTIALIAS)
        datamatrix.save('temp.png', 'png')
        im.paste(datamatrix, (1490, 80, 1670, 260))
        draw.text((1160, 110), "   Test ID: %s" % display_test_id,
                  fill=0, font=scp)
        draw.text((1160, 145), "  Paper ID:   %s" % display_copy_id,
                  fill=0, font=scp)
        draw.text((1160, 180), "Access PIN:  %s" % self.pin,
                  fill=0, font=scp)

        # Save and clean-up
        parent_dir = os.getcwd()
        if not os.path.exists(str(test_obj.test_id)):
            os.makedirs(str(test_obj.test_id))
        os.chdir(str(test_obj.test_id))
        file_name = "%d_%d_mcas.jpeg" % (test_obj.test_id, copy_id)
        im.save(file_name, "jpeg", quality=50)
        os.chdir(parent_dir)
        os.remove("datamatrix_temp.png")
        print("  -> Created copy #%d for test #%d"
              % (test_obj.test_id, copy_id))

    def add_ans(self, q, a):
        self.ans[q] = a

    def mark(self, keys):
        self.res = [0] * (len(keys) + 1)
        for i in range(len(self.ans)):
            if self.ans[i] == keys[i]:
                self.res[i] = 1
        self.res[-1] = sum(self.res) / len(keys)


if __name__ == '__main__':
    test_list = []
    new_test = Test("Sample Test 1", test_list)
    new_test.generate_copy(8)
