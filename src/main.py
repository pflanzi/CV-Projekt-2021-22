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
                    w, h = template.shape[::-1]
                    result = cv2.matchTemplate(img_gray, img_template, cv2.TM_CCOEFF_NORMED)

                    # ----- get all the coordinates where the matching result is >= threshold
                    threshold = 0.7
                    (yCoords, xCoords) = np.where(result >= threshold)
                    clone = self.img_rgb.copy()

                    # print("[INFO] {} matched locations *before* NMS".format(len(yCoords)))

                    # ----- loop over the x- and y-coordinates and draw the bounding boxes
                    for (x, y) in zip(xCoords, yCoords):
                        cv2.rectangle(clone, (x, y), (x + w, y + h), (255, 0, 0), 3)

                    cv2.imshow("Before NMS", clone)

                    '''
                    w, h = template.shape[::-1]
                    result = cv2.matchTemplate(img_gray, ndimage.rotate(template, angle), cv2.TM_CCOEFF_NORMED)
                    match_thresh = 0.9

                    # TODO: Check for color in an area around Object + Template
                    loc = np.where(result >= match_thresh)

                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(self.img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), 1)
                    '''
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
