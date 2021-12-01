import cv2
import numpy as np
from scipy import ndimage
from tqdm import tqdm

img_rgb = cv2.imread('images/six_apples.jpg')
img_template = cv2.imread('images/test_apple.jpg', 0)
for i in tqdm(range(20, 100)):
    template = img_template
    scale_percent = i  # percent of original size
    width = int(template.shape[1] * scale_percent / 100)
    height = int(template.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    template = cv2.resize(template, dim, interpolation=cv2.INTER_AREA)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    temp_height, temp_width = template.shape
    img_height, img_width = img_gray.shape

    if temp_height >= img_height or temp_width >= img_width:
        break

    for angle in range(0, 360, 10):
        try:
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray, ndimage.rotate(template, angle), cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 3)
        except cv2.error as error:
            continue
            # Some rotation exceeds the height/width of the image but doesn't break the program
            # random comment

cv2.imshow("test", img_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imwrite('images/apples_found.jpg', img_rgb)
