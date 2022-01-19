"""
Algorithm for detecting apples.

Author(s): Jan Ehreke, Franziska Niemeyer
"""

# ------ imports ------ #
import cv2
import numpy as np


# ------ algorithm ------ #
def detect(path, min_r, max_r, resize):
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
    # Resizing based on number of apples on the picture. Best results if apple is somewhat around ~100x100
    if resize == "single":
        image_bgr = cv2.resize(image_bgr, (200, 200), interpolation=cv2.INTER_AREA)
    elif resize == "multiple" and image_bgr.shape[0] > 1000:
        scale_percent = 30  # percent of original size
        width = int(image_bgr.shape[1] * scale_percent / 100)
        height = int(image_bgr.shape[0] * scale_percent / 100)
        dim = (width, height)

        image_bgr = cv2.resize(image_bgr, dim, interpolation=cv2.INTER_AREA)

    # creating a copy of the original image and converting it into HSV (Hue, Saturation, Value)
    image = image_bgr.copy()
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # The masks for both reds and a bit of green
    mask_red_low = cv2.inRange(image_hsv, lower_red_low, lower_red_high)
    mask_red_high = cv2.inRange(image_hsv, higher_red_low, higher_red_high)
    mask_red_raw = cv2.inRange(image_hsv, raw_low, raw_high)

    mask = mask_red_low + mask_red_high + mask_red_raw

    # Blur and Thresh to remove some Noise from the image
    blur = cv2.GaussianBlur(mask, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # The Kernel size which is used by erosion and closing 5x5 Matrix
    kernel = np.ones((5, 5), np.uint8)

    # Eroding some connections between the apples to get single apples not connected to other apples
    erosion = cv2.erode(thresh, kernel, iterations=2)

    # Closing to remove even more Noise and combine parts of an apple together
    closing = cv2.morphologyEx(erosion, cv2.MORPH_CLOSE, kernel)

    # cv2.RETR_EXTERNAL: We only need the external contours. Contours inside apples can be dropped
    # cv2.CHAIN_APPROX_SIMPLE: We have circles so we only need some points to get a circle and to save memory
    contours, _ = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    c_num = 0
    circles, coords = [], []
    for i, c in enumerate(contours):
        # Draw the smallest circle that still encloses the whole contour
        ((x, y), r) = cv2.minEnclosingCircle(c)
        circles.append(((x, y), r))

    for ((x, y), r) in circles:
        # min_r and max_r from GUI
        # Only accept circles between given radius
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
                # If distance too small the Algorithm detected multiple circles on a single apple
                if all(np.sqrt((coord[0] - x) ** 2 + (coord[1] - y) ** 2) > 90 for coord in coords):
                    c_num += 1
                    cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
                    cv2.putText(image, "#{}".format(c_num), (int(x) - 10, int(y)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                coords.append((x, y))
        else:
            continue
    return c_num, image
