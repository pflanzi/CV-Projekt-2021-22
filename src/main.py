import cv2
import numpy as np
from scipy import ndimage
from tqdm import tqdm
import glob


class DetectionAlgorithm:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.img_rgb = cv2.imread('images/six_apples.jpg')
        self.image_list = []
        for picture in glob.glob('images/single_apples/*'):
            image = cv2.imread(picture)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.image_list.append(image)

    def detect(self, img_template):
        for scale_percent in tqdm(range(20, 150, 10)):
            self.width = int(img_template.shape[1] * scale_percent / 100)
            self.height = int(img_template.shape[0] * scale_percent / 100)
            dim = (self.width, self.height)

            # resize image
            template = cv2.resize(img_template, dim, interpolation=cv2.INTER_AREA)

            # grayscale
            img_gray = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2GRAY)

            th, tw = template.shape
            ih, iw = img_gray.shape

            # Template bigger than original Picture -> exit
            if th >= ih or tw >= iw:
                break

            output = self.img_rgb.copy()
            # detect circles in the image
            circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 60,
                                       param1=90,
                                       param2=40,
                                       minRadius=65,
                                       maxRadius=100)
            # ensure at least some circles were found
            if circles is not None:
                # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
                # loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                cv2.imshow("Test", output)
                cv2.imshow("Gray", img_gray)
                break

    def main(self):
        # for image in self.image_list:
        #     self.detect(image)
        self.detect(self.image_list[0])
        # cv2.imshow("Apple Detection", self.img_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


program = DetectionAlgorithm()
program.main()

# cv2.imwrite('images/apples_found.jpg', self.img_rgb)
