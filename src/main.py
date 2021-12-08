import cv2
import numpy as np
from scipy import ndimage
from tqdm import tqdm
import glob


class DetectionAlgorithm:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.img_rgb = cv2.imread('images/six_apples.jpg')
        self.image_list = []
        for picture in glob.glob('images/single_apples/*'):
            image = cv2.imread(picture)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.image_list.append(image)

    def detect(self, img_template):
        for scale_percent in tqdm(range(20, 150, 10)):
            template = img_template
            self.width = int(template.shape[1] * scale_percent / 100)
            self.height = int(template.shape[0] * scale_percent / 100)
            dim = (self.width, self.height)

            # resize image
            template = cv2.resize(template, dim, interpolation=cv2.INTER_AREA)

            # grayscale
            img_gray = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2GRAY)

            th, tw = template.shape
            ih, iw = img_gray.shape

            # Template bigger than original Picture -> exit
            if th >= ih or tw >= iw:
                break

            for angle in range(0, 360, 20):
                # TODO: more precise try catch
                try:
                    # Template matching
                    # TODO: Check multi-template matching
                    # below an example code of how multi-template matching could work
                    # result = cv2.matchTemplate(imageGray, templateGray, cv2.TM_CCOEFF_NORMED)
                    #
                    # # ----- get all the coordinates where the matching result is >= threshold
                    # threshold = 0.7
                    # (yCoords, xCoords) = np.where(result >= threshold)
                    # clone = image.copy()
                    #
                    # print("[INFO] {} matched locations *before* NMS".format(len(yCoords)))
                    #
                    # # ----- loop over the x- and y-coordinates and draw the bounding boxes
                    # for (x, y) in zip(xCoords, yCoords):
                    #     cv2.rectangle(clone, (x, y), (x + tW, y + tH), (255, 0, 0), 3)
                    #
                    # cv2.imshow("Before NMS", clone)

                    w, h = template.shape[::-1]
                    res = cv2.matchTemplate(img_gray, ndimage.rotate(template, angle), cv2.TM_CCOEFF_NORMED)
                    threshold_template = 0.9

                    # TODO: Check for color in an area around Object + Template
                    loc = np.where(res >= threshold_template)

                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(self.img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), 1)

                    # Shape matching

                    '''
                    ret, thresh = cv2.threshold(img_gray, 127, 255, 0)
                    ret, thresh2 = cv2.threshold(img_template, 127, 255, 0)
                    contour, hierarchy = cv2.findContours(thresh, 2, 1)
                    cnt1 = contour[0]
                    contour, hierarchy = cv2.findContours(thresh2, 2, 1)
                    cnt2 = contour[0]
                    ret = cv2.matchShapes(cnt1, cnt2, 1, 0.0)
                    
                    threshold_shape = 0.3
                    loc = np.where(ret <= threshold_shape)
                    '''

                    _, threshold = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
                    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    i = 0
                    for contour in contours:
                        if i == 0:
                            i = 1
                            continue

                        # cv2.approxPloyDP() function to approximate the shape
                        # TODO: fine tuning maybe
                        approx = cv2.approxPolyDP(
                            contour, 0.01 * cv2.arcLength(contour, True), True)

                        # using drawContours() function
                        cv2.drawContours(self.img_rgb, [contour], 0, (0, 0, 0), 1)

                        # finding center point of shape
                        m = cv2.moments(contour)
                        if m['m00'] != 0.0:
                            x = int(m['m10'] / m['m00'])
                            y = int(m['m01'] / m['m00'])

                        if len(approx) >= 100:
                            cv2.putText(self.img_rgb, 'apple',
                                        (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(self.img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), 1)
                except cv2.error as error:
                    continue
                    # Some rotation exceeds the height/width of the image but doesn't break the program

    def main(self):
        for image in self.image_list:
            self.detect(image)
        cv2.imshow("Apple Detection", self.img_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


program = DetectionAlgorithm()
program.main()

# cv2.imwrite('images/apples_found.jpg', self.img_rgb)