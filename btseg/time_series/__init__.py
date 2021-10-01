import cv2
import btseg.transformers as t
import numpy as np
import math


def generate_time_series(path):
    img = cv2.imread(path)

    transforms = t.Compose([
        t.ConvertColor(conversion_code=cv2.COLOR_BGR2GRAY),
        t.Resize(proportion_scale=True, g_measure=700),
        t.RegionSelection(region=1),
        t.GaussianBlur(kernel_size=(7, 7), sigma_x=0),
        t.CannyEdge(threshold_1=50, threshold_2=100),
        t.Dilate(kernel=None, iterations=1),
        t.Erode(kernel=None, iterations=1),
        t.MinimumBoundingBox()
    ])

    transformed_img = transforms(img)
    ref = np.zeros_like(transformed_img)

    contours, _ = cv2.findContours(transformed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(ref, contours, 0, 255, 1)

    M = cv2.moments(ref)
    centroid_x = int(M['m10'] / M['m00'])
    centroid_y = int(M['m01'] / M['m00'])

    height, width = transformed_img.shape
    N = 360
    distances = []
    out = transformed_img.copy()

    for i in np.arange(0, N, 1):
        tmp = np.zeros_like(transformed_img)

        theta = i * (360 / N)
        theta *= np.pi / 180.0

        cv2.line(tmp, (centroid_x, centroid_y), (int(centroid_x + np.cos(theta) * width), int(centroid_y - np.sin(theta) * height)), 255, 5)

        (row, col) = np.nonzero(np.logical_and(tmp, ref))
        cv2.line(out, (centroid_x, centroid_y), (col[0], row[0]), 0, 1)

        distance = math.sqrt(
            ((col[0] - centroid_x) ** 2) + ((row[0] - centroid_y) ** 2)
        )
        distances.append(distance)
    
    return distances

def save_time_series(values, fname):
    values = np.array(values)
    np.savetxt(fname, values)