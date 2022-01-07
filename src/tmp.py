import cv2
import numpy as np
import imutils
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage.segmentation import watershed

img = cv2.imread('../images/test/100_apples.jpg')
img = imutils.resize(img, width=640)
# img = cv2.pyrMeanShiftFiltering(img, 21, 51)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_1 = np.array([0, 50, 20])
upper_1 = np.array([80, 255, 255])
mask1 = cv2.inRange(hsv, lower_1, upper_1)

lower_2 = np.array([160, 50, 20])
upper_2 = np.array([179, 255, 255])
mask2 = cv2.inRange(hsv, lower_2, upper_2)

thresh = mask1 + mask2
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
thresh = cv2.erode(thresh, kernel)

D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices=False, min_distance=20,
                          labels=thresh)

markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=thresh)
print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

circles = []
circles_r = []

for label in np.unique(labels):
    if label == 0:
        continue
    average = 0

    mask = np.zeros(gray.shape, dtype="uint8")
    mask[labels == label] = 255

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    # TODO: Check for color threshold like in main
    ((x, y), r) = cv2.minEnclosingCircle(c)
    circles.append(((x, y), r))
    circles_r.append(r)

'''r = sum(circles_r)/(len(np.unique(labels)) - 1)
print(sorted(circles_r))'''
for (x, y), r in circles:
    if 20 < r < 200:
        cv2.circle(img, (int(x), int(y)), int(r), (0, 255, 0), 2)
        cv2.putText(img, "{}".format(round(r)), (int(x) - 10, int(y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

cv2.imshow('thresh', thresh)
# cv2.imshow('gray', gray)
cv2.imshow('img', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
