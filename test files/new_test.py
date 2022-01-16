# Name: approach_2.py
# By Dr. S. S. Gajbhar
import cv2

# Defining the color ranges to be filtered.
# The following ranges should be used on HSV domain image.

# default color range (almost very good)
# lower_red_low = (0, 150, 150)
# lower_red_high = (8, 255, 255)
# higher_red_low = (160, 150, 150)
# higher_red_high = (180, 255, 255)
# raw_low = (25, 115, 128)
# raw_high = (38, 255, 255)

# custom color range 1 (no, just no)
# lower_red_low = (0, 77, 102)
# lower_red_high = (8, 255, 255)
# higher_red_low = (160, 77, 102)
# higher_red_high = (180, 255, 255)
# raw_low = (25, 115, 128)
# raw_high = (38, 255, 255)

# custom color range 2 (almost very good)
# lower_red_low = (0, 64, 128)
# lower_red_high = (8, 255, 255)
# higher_red_low = (165, 64, 128)
# higher_red_high = (180, 255, 255)
# raw_low = (25, 115, 128)
# raw_high = (38, 255, 255)

# custom color range 3 (very good)
# lower_red_low = (0, 77, 115)
# lower_red_high = (5, 255, 255)
# # higher_red_low = (160, 89, 128)
# higher_red_high = (180, 255, 255)
# raw_low = (28, 89, 128)
# raw_high = (35, 255, 255)

# custom color range 4 (no, just no)
# lower_red_low = (0, 112, 135)
# lower_red_high = (5, 255, 255)
# higher_red_low = (175, 79, 115)
# higher_red_high = (180, 255, 255)
# raw_low = (25, 115, 128)
# raw_high = (38, 255, 255)

# custom color range 5 (von gestern, almost good)
# lower_red_low = (0, 145, 163)
# lower_red_high = (8, 255, 255)
# higher_red_low = (175, 145, 163)
# higher_red_high = (180, 255, 255)
# raw_low = (25, 115, 128)
# raw_high = (38, 255, 255)

image_bgr = cv2.imread('../images/apples/multiple/3_apples.jpg')
image = image_bgr.copy()
image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

mask_lower_red = cv2.inRange(image_hsv, lower_red_low, lower_red_high)
mask_higher_red = cv2.inRange(image_hsv, higher_red_low, higher_red_high)
mask_raw = cv2.inRange(image_hsv, raw_low, raw_high)

mask = mask_lower_red + mask_higher_red + mask_raw

cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                           cv2.CHAIN_APPROX_SIMPLE)
c_num = 0
for i, c in enumerate(cnts):
    # draw a circle enclosing the object
    ((x, y), r) = cv2.minEnclosingCircle(c)
    if r > 34:
        c_num += 1
        cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
        cv2.putText(image, "#{}".format(c_num), (int(x) - 10, int(y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    else:
        continue

cv2.imshow("Original image", image_bgr)
cv2.imshow("Detected Apples", image)
# cv2.imshow("HSV Image", image_hsv)
# cv2.imshow("Mask image", mask)
cv2.waitKey(0)
