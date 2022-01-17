import cv2
import numpy as np
import imutils


def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters,
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001),
            rounds,
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape(image.shape)


def mask(image, clusters=8, rounds=1):
    lower_red_low = (0, 77, 115)
    lower_red_high = (5, 255, 255)
    higher_red_low = (160, 89, 128)
    higher_red_high = (180, 255, 255)
    raw_low = (28, 89, 128)
    raw_high = (35, 255, 255)

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask_lower_red = cv2.inRange(image_hsv, lower_red_low, lower_red_high)
    mask_higher_red = cv2.inRange(image_hsv, higher_red_low, higher_red_high)
    mask_raw = cv2.inRange(image_hsv, raw_low, raw_high)

    mask = mask_lower_red + mask_higher_red + mask_raw

    return mask


# Load image, resize smaller, perform kmeans, grayscale
# Apply Gaussian blur, Otsu's threshold
image = cv2.imread('../images/apples/multiple/10_apples.jpg')
# image = imutils.resize(image, width=600)
kmeans = mask(image, clusters=3)
blur = cv2.GaussianBlur(kmeans, (9, 9), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Filter out contours not circle
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) < 4:
        cv2.drawContours(thresh, [c], -1, 0, -1)

# Morph close
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Find contours and draw minimum enclosing circles 
# using contour area as filter
approximated_radius = 63
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    x, y, w, h = cv2.boundingRect(c)
    ((x, y), r) = cv2.minEnclosingCircle(c)
    cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)

    # # Large circles
    # if area > 6000 and area < 15000:
    #     ((x, y), r) = cv2.minEnclosingCircle(c)
    #     cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
    # # Small circles
    # elif area > 1000 and area < 6000:
    #     ((x, y), r) = cv2.minEnclosingCircle(c)
    #     cv2.circle(image, (int(x), int(y)), approximated_radius, (200, 255, 12), 2)

cv2.imshow('kmeans', kmeans)
cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.imshow('image', image)
cv2.waitKey()
