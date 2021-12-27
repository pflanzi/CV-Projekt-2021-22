# ----- import ----- #
import cv2
import imutils
import numpy as np

# ----- To-Do-List ----- #
# TODO: add documentation
# TODO: check for obsolete code pieces
# TODO: check formatting
# TODO: adjust Hough Circle detection (overlapping apples)
# TODO: get more test images
# TODO: add another processing step to filter / improve results
# TODO: connect this code to the GUI

# ----- class, functions, variables ----- #
COLOR_NAMES = ["redgreen", "red"]

COLOR_RANGES_HSV = {
    "redgreen": [(0, 50, 10), (60, 255, 255)],
    "red": [(170, 50, 10), (180, 255, 255)]
}


def get_mask(frame, color):
    """

    :param frame:
    :param color:
    :return:
    """
    blurred_frame = cv2.GaussianBlur(frame, (3, 3), 0)
    hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    color_range = COLOR_RANGES_HSV[color]
    lower = np.array(color_range[0])
    upper = np.array(color_range[1])

    color_mask = cv2.inRange(hsv_frame, lower, upper)
    color_mask = cv2.bitwise_and(blurred_frame, blurred_frame, mask=color_mask)

    return color_mask


def get_color(roi):
    """
    Finds the dominant color in a ROI
    :param roi: given ROI (region of interest)
    :return: dominant colour
    """
    roi = np.float32(roi)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(roi, 4, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape(roi.shape)

    pixels_per_color = []
    for color in COLOR_NAMES:
        mask = get_mask(res2, color)
        grey_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        count = cv2.countNonZero(grey_mask)
        pixels_per_color.append(count)

    print(f"roi {roi.shape}")
    # TODO: Change Threshold to be dynamic
    if pixels_per_color[0] > ((roi.shape[0] * roi.shape[1]) / 3) or \
            pixels_per_color[1] > ((roi.shape[0] * roi.shape[1]) / 3):
        return COLOR_NAMES[pixels_per_color.index(max(pixels_per_color))]
    else:
        return None


class DetectionAlgorithm:
    """
    Detection Algorithm class containing functions
    for detecting and counting objects in a given image
    """

    def __init__(self):
        """
        Class constructor initializing the following class attributes:
            img_bgr : numpy.ndarray
                stores a colored image (channels are in BGR order)
            hsv : numpy.ndarray
                stores a colored HSV image
            dim : tuple
                dimensions of the BGR image: (rows, columns, channels)
        """

        self.img_bgr = None
        self.hsv = None
        self.dim = (0, 0, 0)

    def read_img(self, path):
        """
        Reads the image from a given path and resizes it if necessary.
        :param path: system path to the image
        """
        if type(path) is not str:
            print('The given path must be of type str!')

        self.img_bgr = cv2.imread(path)

        self.dim = self.img_bgr.shape  # dim = rows, columns, channels

        while self.dim[1] > 1000 or self.dim[0] > 1000:
            new_width = int(self.dim[1] * 0.9)

            self.img_bgr = imutils.resize(self.img_bgr, width=new_width)

            self.dim = self.img_bgr.shape

        self.hsv = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2HSV)

    def detect(self, path):
        """
        Function that performs the actual detection of circles inside a given image.
        :param path: image path
        """

        try:
            self.read_img(path)

        except AttributeError as a:
            print(f'{a}. Please enter a valid image path.')
            exit()

        except TypeError as t:
            print(f'{t}. Please enter a valid image path.')
            exit()

        output = self.img_bgr.copy()
        # detect circles in the image
        circles = cv2.HoughCircles(self.hsv[:, :, 0], cv2.HOUGH_GRADIENT, 1, 75,
                                   param1=25,
                                   param2=35,
                                   minRadius=30,
                                   maxRadius=105)

        # ensure at least some circles were found
        if circles is not None:

            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:

                roi = self.img_bgr[int(y - r / 2):int(y + r / 2), int(x - r / 2):int(x + r / 2)]
                color = get_color(roi=roi)

                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                if color == "redgreen" or color == "red":
                    cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    cv2.putText(output, "Apple", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                else:
                    print("Not red")
            cv2.imshow("Test", output)

    def main(self):
        """
        Main function, calls detect()-function to perform detection
        """

        image_path = 'test'

        self.detect(image_path)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


program = DetectionAlgorithm()
program.main()
