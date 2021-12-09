import cv2
import numpy as np
from scipy import ndimage
from tqdm import tqdm
import glob


class DetectionAlgorithm:

    def __init__(self):
        # self.img_rgb = cv2.imread('images/six_apples.jpg')
        # self.img_rgb = cv2.imread('images/3_apples.jpg')
        # self.img_rgb = cv2.imread('images/multiple_apples.jpg')
        self.img_rgb = cv2.imread('images/fruit-vocabulary-words.jpg')
        self.hsv = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2HSV)

    def detect(self):

        output = self.img_rgb.copy()
        # detect circles in the image
        circles = cv2.HoughCircles(self.hsv[:, :, 0], cv2.HOUGH_GRADIENT, 1, 75,
                                   param1=15,
                                   param2=22,
                                   minRadius=80,
                                   maxRadius=105)
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
                cv2.putText(output, "Apple", (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.imshow("Test", output)

    def main(self):
        self.detect()
        cv2.waitKey(0)
        cv2.destroyAllWindows()


program = DetectionAlgorithm()
program.main()

# cv2.imwrite('images/apples_found.jpg', self.img_rgb)
