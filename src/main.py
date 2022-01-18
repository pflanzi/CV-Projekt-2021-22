"""
Algorithm for detecting apples.

Author(s): Jan Ehreke, Franziska Niemeyer
"""

# ------ imports ------ #
import cv2
import numpy as np
import imutils
from PIL import Image
import glob


# ------ algorithm ------ #
def detect(path, min_r, max_r, resize='single'):
    """
    The detection algorithm. Counts apples.
    :param path: image path
    :param min_r: min radius for enclosing circles
    :param max_r: max radius for enclosing circles
    :param resize: resizing method for single or multiple apples
    :return image with enclosing circles
    """

    # Defining the color ranges to be filtered.
    # The following ranges should be used on HSV domain image.
    lower_red_low = (0, 145, 163)
    lower_red_high = (8, 255, 255)
    higher_red_low = (175, 145, 26)
    higher_red_high = (180, 255, 255)
    raw_low = (25, 115, 128)
    raw_high = (38, 255, 255)

    image_bgr = cv2.imread(path)
    if resize == "single":
        image_bgr = cv2.resize(image_bgr, (200, 200), interpolation=cv2.INTER_AREA)
    elif resize == "multiple" and image_bgr.shape[0] > 1000:
        scale_percent = 30  # percent of original size
        width = int(image_bgr.shape[1] * scale_percent / 100)
        height = int(image_bgr.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        image_bgr = cv2.resize(image_bgr, dim, interpolation=cv2.INTER_AREA)

    image = image_bgr.copy()
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    mask_red_low = cv2.inRange(image_hsv, lower_red_low, lower_red_high)
    mask_red_high = cv2.inRange(image_hsv, higher_red_low, higher_red_high)
    mask_red_raw = cv2.inRange(image_hsv, raw_low, raw_high)

    mask = mask_red_low + mask_red_high + mask_red_raw

    blur = cv2.GaussianBlur(mask, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations=2)
    closing = cv2.morphologyEx(erosion, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    c_num = 0
    circles, coords = [], []
    for i, c in enumerate(contours):
        # draw a circle enclosing the object
        ((x, y), r) = cv2.minEnclosingCircle(c)
        circles.append(((x, y), r))

    for ((x, y), r) in circles:
        if min_r < r < max_r:
            # First iteration on empty list
            if not coords:
                c_num += 1
                coords.append((x, y))
                cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
                cv2.putText(image, "#{}".format(c_num), (int(x) - 10, int(y)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            else:
                # Check for distance to center point to center of every other circle
                if all(np.sqrt((coord[0] - x) ** 2 + (coord[1] - y) ** 2) > 90 for coord in coords):
                    c_num += 1
                    cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
                    cv2.putText(image, "#{}".format(c_num), (int(x) - 10, int(y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                coords.append((x, y))

        else:
            continue

    # cv2.imshow("thresh", thresh)
    # cv2.imshow("dil", dilation)
    # cv2.imshow("Detected Apples", image)

    return c_num, image


# image_list = []
# resize = "single"
# for filename in glob.glob('../images/apples/single/other/*.jpg'):
#     image_list.append(filename)

# resize = "multiple"
# for filename in glob.glob('images/apples/multiple/*.jpg'):
#     image_list.append(filename)
#
# for image in image_list:
#     detect(image)
#     # cv2.imshow("HSV Image", image_hsv)
#     # cv2.imshow("Mask image", mask)
#     cv2.waitKey(0)
