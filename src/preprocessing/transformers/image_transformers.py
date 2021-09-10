import cv2
import numpy as np


class MinimumBoundingBox:

    def __init__(self, padding: int):
        self.p = padding # TODO: implement padding

    def __call__(self, image):
        rows = np.any(image, axis=1)
        cols = np.any(image, axis=0)

        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]

        return image[y_min:y_max+1, x_min:x_max+1]


class Resize:

    def __init__(self, proportion_scale: bool, g_measure: int):
        self.proportion_scale = proportion_scale
        self.g_measure = g_measure
    
    def __call__(self, image):
        y, x = image.shape

        if self.proportion_scale:
            if x < y:
                y_i = self.g_measure
                x_i = (self.g_measure * x) / y
                return cv2.resize(image, (x_i, y_i))
            
            if x > y:
                x_i = self.g_measure
                y_i = (self.g_measure * y) / x
                return cv2.resize(image, (x_i, y_i))

        return cv2.resize(image, (self.g_measure, self.g_measure)) 