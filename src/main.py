import cv2
import numpy as np
from scipy import ndimage
from tqdm import tqdm
import glob


COLOR_NAMES = ["red", "red "]

COLOR_RANGES_HSV = {
    "red": [(0, 50, 10), (10, 255, 255)],
    "red ": [(170, 50, 10), (180, 255, 255)]
}


def getMask(frame, color):
    blurred_frame = cv2.GaussianBlur(frame, (3, 3), 0)
    hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    color_range = COLOR_RANGES_HSV[color]
    lower = np.array(color_range[0])
    upper = np.array(color_range[1])

    color_mask = cv2.inRange(hsv_frame, lower, upper)
    color_mask = cv2.bitwise_and(blurred_frame, blurred_frame, mask=color_mask)

    return color_mask


def getDominantColor(roi):
    roi = np.float32(roi)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(roi, 4, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape(roi.shape)

    pixels_per_color = []
    for color in COLOR_NAMES:
        mask = getMask(res2, color)
        grey_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        count = cv2.countNonZero(grey_mask)
        pixels_per_color.append(count)

    if pixels_per_color[0] > 3000 or pixels_per_color[1] > 3000:
        return COLOR_NAMES[pixels_per_color.index(max(pixels_per_color))]
    else:
        return None


class DetectionAlgorithm:

    def __init__(self):
        self.img_rgb = cv2.imread('images/six_apples.jpg')
        # self.img_rgb = cv2.imread('images/3_apples.jpg')
        # self.img_rgb = cv2.imread('images/multiple_apples.jpg')
        # self.img_rgb = cv2.imread('images/fruit-vocabulary-words.jpg')
        self.hsv = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2HSV)

    def detect(self):

        output = self.img_rgb.copy()
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

                roi = self.img_rgb[int(y - r / 2):int(y + r / 2), int(x - r / 2):int(x + r / 2)]
                color = getDominantColor(roi=roi)

                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                if color == "red" or color == "red ":
                    cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    cv2.putText(output, "Apple", (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                else:
                    print("Not red")
            cv2.imshow("Test", output)

    def main(self):
        self.detect()
        cv2.waitKey(0)
        cv2.destroyAllWindows()


program = DetectionAlgorithm()
program.main()

# cv2.imwrite('images/apples_found.jpg', self.img_rgb)
