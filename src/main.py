# ----- imports ----- #
import cv2
import imutils
import numpy as np

# ----- To-Do-List ----- #
# TODO: add documentation, check for obsolete code pieces, check formatting => keep this until project is finished

# TODO: adjust Hough Circle detection (overlapping apples)
# TODO: add another processing step to filter / improve results

# TODO: connect this code to the GUI

# ----- class, functions, variables ----- #
COLOR_NAMES = ["redgreen", "red", "yellowgreen"]

COLOR_RANGES_HSV = {
    "redgreen": [(0, 50, 20), (20, 255, 255)],
    "red": [(170, 50, 20), (180, 255, 255)],
    "yellowgreen": [(21, 50, 20), (80, 255, 255)]
}


def get_mask(frame, color):
    """
    Creates a mask from HSV image which will later be used to check for certain colors in a ROI
    :param frame: ROI borders
    :param color: color to check for  # TODO: what is the parameter exactly?
    :return: colored mask
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
    if len(roi) != 0:
        ret, label, center = cv2.kmeans(roi, 10, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    else:
        return None

    try:
        center = np.uint8(center)
    except TypeError as error:
        print(error)
        return None
    res = center[label.flatten()]
    res2 = res.reshape(roi.shape)

    pixels_per_color = []
    for color in COLOR_NAMES:
        mask = get_mask(res2, color)
        grey_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        count = cv2.countNonZero(grey_mask)
        pixels_per_color.append(count)

    # TODO: pixel_threshold and /3 through gui?
    # Filter every circle that is not at least 1/3 red and should not be completely red so tomatoes for example are not
    # detected
    # pixel per color checks for the 2 red thresholds against the content of the circles
    thresh = pixels_per_color[0] + pixels_per_color[1] + pixels_per_color[2]
    pixel_threshold = 0.95
    red_threshold = 2

    if pixels_per_color[0] > ((roi.shape[0] * roi.shape[1]) / red_threshold) or pixels_per_color[1] > (
            (roi.shape[0] * roi.shape[1]) / red_threshold):
        if pixels_per_color[0] < ((roi.shape[0] * roi.shape[1]) / 1.2) and pixels_per_color[1] < (
                (roi.shape[0] * roi.shape[1]) / 1.2):
            if thresh > ((roi.shape[0] * roi.shape[1]) * pixel_threshold):
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

        # noise reduction
        dn_img = cv2.fastNlMeansDenoisingColored(self.hsv, None, 10, 10, 7, 21)

        # detect circles in the image
        circles = cv2.HoughCircles(dn_img[:, :, 0], cv2.HOUGH_GRADIENT, 1, 75,
                                   param1=95,
                                   param2=20,
                                   minRadius=45,
                                   maxRadius=105)

        # ensure at least some circles were found
        if circles is not None:

            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            avrg_rad = []
            for (x, y, r) in circles:
                avrg_rad.append(r)
            avrg_rad = sorted(avrg_rad)

            # Slicing 20% off of the circles to avoid exceptional bit or small circles messing up calculation
            # getting the average of all circles and accept all within a threshold
            l = round(len(avrg_rad)*0.2)
            avrg = sum(avrg_rad[l:-l]) / len(circles[l:-l])

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                roi = self.img_bgr[int(y - r / 2):int(y + r / 2), int(x - r / 2):int(x + r / 2)]
                color = get_color(roi=roi)

                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                if (avrg * 0.7) < r < (avrg * 1.3):
                    if color == "redgreen" or color == "red":
                        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                        cv2.putText(output, "Apple", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                    else:
                        continue
            # cv2.imshow("Test", output)

            return output
        else:
            print("No circles found.")
            exit()

    def main(self, path):
        """
        Main function, calls detect()-function to perform detection
        """

        result = self.detect(path)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return result
