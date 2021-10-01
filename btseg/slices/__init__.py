import glob
import os
import btseg.transformers as t
import cv2
import numpy as np
from imutils import perspective
from scipy.spatial import distance as dist

def midpoint(pt_a, pt_b):
    return ((pt_a[0] + pt_b[0]) * 0.5, (pt_a[1] + pt_b[1]) * 0.5)

def calculate_slice_area(path, transforms) -> str:
    image = cv2.imread(path)
    transformed_image = transforms(image)

    contours = cv2.findContours(transformed_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    areas = []

    for c in contours:
        if cv2.contourArea(c) < 100:
            continue

        orig = image.copy()

        box = cv2.minAreaRect(c)

        box = cv2.boxPoints(box)
        box = np.array(box, dtype='int')

        x_sorted = box[np.argsort(box[:, 0]), :]
        left_most = x_sorted[:2, :]
        right_most = x_sorted[2:, :]

        left_most = left_most[np.argsort(left_most[:, 1]), :]
        (tl, bl) = left_most

        d = dist.cdist(tl[np.newaxis], right_most, 'euclidean')[0]
        (br, tr) = right_most[np.argsort(d)[::-1], :]

        box = np.array([tl, tr, br, bl], dtype='float32')
        
        # box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        # for (x, y) in box:
        #     cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
        
        (tl, tr, br, bl) = box
        (tltr_x, tltr_y) = midpoint(tl, tr)
        (blbr_x, blbr_y) = midpoint(bl, br)

        (tlbl_x, tlbl_y) = midpoint(tl, bl)
        (trbr_x, trbr_y) = midpoint(tr, br)

        d_a = dist.euclidean((tltr_x, tltr_y), (blbr_x, blbr_y))
        d_b = dist.euclidean((tlbl_x, tlbl_y), (trbr_x, trbr_y))

        areas.append(d_a * d_b)

    return max(areas, default=0)


def selecting_slice(dir_path: str) -> str:
    files = glob.glob(os.path.join(
        dir_path, '*.png'
    ))
    
    transforms = t.Compose([
        t.ConvertColor(conversion_code=cv2.COLOR_BGR2GRAY),
        t.RegionSelection(region=1),
        t.GaussianBlur(kernel_size=(7, 7), sigma_x=0),
        t.CannyEdge(threshold_1=50, threshold_2=100),
        t.Dilate(kernel=None, iterations=1),
        t.Erode(kernel=None, iterations=1)
    ])

    slice_path = ''
    slice_area = -1

    for f in files:
        area = calculate_slice_area(f, transforms)
        if area > slice_area:
            slice_area = area
            slice_path = f 

    return slice_path if slice_path != '' else None