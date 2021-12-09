# ----- imports ----- #
import cv2
import numpy as np
from tqdm import tqdm
import glob


# ----- To-Do-List ----- #
# TODO: add documentation
# TODO: check for obsolete code pieces
# TODO: check formatting
# TODO: adjust Hough Circle detection (overlapping apples)
# TODO: get more test images
# TODO: add another processing step to filter / improve results
# TODO: connect this code to the GUI

# ----- class, functions, variables ----- #
class DetectionAlgorithm:
    """
    Detection Algorithm class containing functions
    for detecting and counting objects in a given image
    """

    def __init__(self):
        """
        Class constructor initializing the following class attributes:
            width : int
                template image width
            height : int
                template image height
            img_rgb : numpy.ndarray
                stores a colored image (channels are in BGR order)
        """
        self.img_rgb = cv2.imread('../images/multiple_apples.jpg')

        if self.img_rgb is not None:
            self.width = self.img_rgb.shape[1]
            self.height = self.img_rgb.shape[0]
        else:
            print(f"[INFO] Could not load image")

    def detect(self):
        """
        Function that performs the actual detection of circles inside a given image.
        """
        # grayscale
        img_gray = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2GRAY)

        self.height, self.width = img_gray.shape

        output = self.img_rgb.copy()

        # detect circles in the image
        circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1,
                                   minDist=58,
                                   param1=90,
                                   param2=45,
                                   minRadius=65,
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

            cv2.imshow("Test", output)
            # cv2.imshow("Gray", img_gray)

    def main(self):
        """
        TODO: add some description here
        :return:
        """
        self.detect()
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# ----- main program ----- #
program = DetectionAlgorithm()
program.main()

# cv2.imwrite('images/apples_found.jpg', self.img_rgb)
