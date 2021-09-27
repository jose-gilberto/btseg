import numpy as np
import cv2


def get_contours(img_path):
    img = cv2.imread(img_path)
    # map all tumor
    # TODO: map all segmentations separately
    img = np.where(img > 0, 64, img)
    # black and white
    img_bw = img > 63
    img_bw = 255 * img_bw.astype('uint8')

    # detect the outer most contour
    contours, _ = cv2.findContours(img_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    out = img.copy()
    ref = np.zeros_like(img_bw)
    cv2.drawContours(ref, contours, 0, 255, 1)

    return ref, out