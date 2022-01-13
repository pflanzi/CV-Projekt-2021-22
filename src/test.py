import cv2
import numpy as np
import imutils


def detect(path):
    # Defining the color ranges to be filtered.
    # The following ranges should be used on HSV domain image.
    # lower_red_low = (0, 145, 163)
    # lower_red_high = (8, 255, 255)
    # higher_red_low = (175, 145, 163)
    # higher_red_high = (180, 255, 255)
    # raw_low = (25, 115, 128)
    # raw_high = (38, 255, 255)

    lower_red_low = (0, 77, 115)
    lower_red_high = (5, 255, 255)
    higher_red_low = (160, 89, 128)
    higher_red_high = (180, 255, 255)
    raw_low = (28, 89, 128)
    raw_high = (35, 255, 255)

    image_bgr = cv2.imread(path)
    image = image_bgr.copy()
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    mask_lower_red = cv2.inRange(image_hsv, lower_red_low, lower_red_high)
    mask_higher_red = cv2.inRange(image_hsv, higher_red_low, higher_red_high)
    mask_raw = cv2.inRange(image_hsv, raw_low, raw_high)

    mask = mask_lower_red + mask_higher_red + mask_raw

    blur = cv2.GaussianBlur(mask, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations=3)
    dilation = cv2.dilate(erosion, kernel, iterations=2)

    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

    cnts, _ = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
    c_num = 0
    circles = []
    for i, c in enumerate(cnts):
        # draw a circle enclosing the object
        ((x, y), r) = cv2.minEnclosingCircle(c)
        circles.append(((x, y), r))

    for ((x, y), r) in circles:
        if 50 < r < 100:
            c_num += 1
            cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
            cv2.putText(image, "#{}".format(c_num), (int(x) - 10, int(y)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        else:
            continue
    cv2.imshow("Mask", mask)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Erosion", erosion)
    cv2.imshow("Dilation", dilation)
    cv2.imshow("Detected Apples", image)


image_path = [
    '../images/test/10_apples.jpg',
    '../images/test/3_apples.jpg',
    '../images/test/7_apples.jpg',
    '../images/test/six_apples.jpg',
    '../images/test/apple_test1.png',
    '../images/test/apple_tray1.jpg',
    '../images/test/apple_basket.jpg'
]
for image in image_path:
    detect(image)
    # cv2.imshow("HSV Image", image_hsv)
    # cv2.imshow("Mask image", mask)
    cv2.waitKey(0)
