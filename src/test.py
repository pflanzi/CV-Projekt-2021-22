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

    # lower red range
    red1_bright_min = (0, 77, 204)
    red1_bright_max = (8, 166, 255)
    red1_middle_min = (0, 166, 179)
    red1_middle_max = (8, 230, 242)
    red1_dark_min = (0, 153, 64)
    red1_dark_max = (8, 242, 179)

    # higher red range
    red2_bright_min = (165, 46, 179)
    red2_bright_max = (180, 217, 255)
    red2_middle_min = (165, 153, 166)
    red2_middle_max = (180, 255, 230)
    red2_dark_min = (165, 143, 64)
    red2_dark_max = (180, 255, 166)

    # yellowgreen range
    yg_bright_min = (25, 26, 204)
    yg_bright_max = (38, 153, 255)
    yg_middle_min = (25, 153, 153)
    yg_middle_max = (38, 230, 217)
    yg_dark_min = (25, 128, 102)
    yg_dark_max = (38, 255, 166)


    image_bgr = cv2.imread(path)
    image = image_bgr.copy()
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # lower red range
    mask_red1_bright = cv2.inRange(image_hsv, red1_bright_min, red1_bright_max)
    mask_red1_middle = cv2.inRange(image_hsv, red1_middle_min, red1_middle_max)
    mask_red1_dark = cv2.inRange(image_hsv, red1_dark_min, red1_dark_max)

    # higher red range
    mask_red2_bright = cv2.inRange(image_hsv, red2_bright_min, red2_bright_max)
    mask_red2_middle = cv2.inRange(image_hsv, red2_middle_min, red2_middle_max)
    mask_red2_dark = cv2.inRange(image_hsv, red2_dark_min, red2_dark_max)

    # yellow green range
    mask_yg_bright = cv2.inRange(image_hsv, yg_bright_min, yg_bright_max)
    mask_yg_middle = cv2.inRange(image_hsv, yg_middle_min, yg_middle_max)
    mask_yg_dark = cv2.inRange(image_hsv, yg_dark_min, yg_dark_max)

    mask = mask_red1_bright + mask_red1_middle + mask_red1_dark + mask_red2_bright + mask_red2_middle + mask_red2_dark + mask_yg_bright + mask_yg_middle + mask_yg_dark

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
    '../images/apples/multiple/10_apples.jpg',
    '../images/apples/multiple/3_apples.jpg',
    '../images/apples/multiple/7_apples.jpg',
    '../images/apples/multiple/six_apples.jpg',
    '../images/apples/multiple/apple_test1.png',
    '../images/apples/multiple/apple_tray1.jpg',
    '../images/apples/multiple/apple_basket.jpg'
]
for image in image_path:
    detect(image)
    # cv2.imshow("HSV Image", image_hsv)
    # cv2.imshow("Mask image", mask)
    cv2.waitKey(0)
