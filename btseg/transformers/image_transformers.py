import cv2
import numpy as np


class SegmentExtraction:
    
    def __init__(self, segment_number: int):
        pass

    def __call__(self, img):
        pass


class MinimumBoundingBox:

    def __init__(self, padding: int = 0):
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
                return cv2.resize(image, dsize=(int(x_i), int(y_i)))
            
            if x > y:
                x_i = self.g_measure
                y_i = (self.g_measure * y) / x
                return cv2.resize(image, dsize=(int(x_i), int(y_i)))

        return cv2.resize(image, (self.g_measure, self.g_measure))


class ConvertColor:

    def __init__(self, conversion_code) -> None:
        self.conversion_code = conversion_code
    
    def __call__(self, image):
        return cv2.cvtColor(image, self.conversion_code)


class GaussianBlur:

    def __init__(self, kernel_size, sigma_x) -> None:
        self.ksize = kernel_size
        self.sigma_x = sigma_x

    def __call__(self, image):
        return cv2.GaussianBlur(image, self.ksize, self.sigma_x)


class CannyEdge:

    def __init__(self, threshold_1, threshold_2) -> None:
        self.t1 = threshold_1
        self.t2 = threshold_2

    def __call__(self, image):
        return cv2.Canny(image, self.t1, self.t2)


class Dilate:

    def __init__(self, kernel, iterations) -> None:
        self.kernel = kernel
        self.iterations = iterations

    def __call__(self, image):
        return cv2.dilate(image, self.kernel, iterations=self.iterations)


class Erode:

    def __init__(self, kernel, iterations) -> None:
        self.kernel = kernel
        self.iterations = iterations

    def __call__(self, image):
        return cv2.erode(image, self.kernel, self.iterations)


class RegionSelection:

    def __init__(self, region) -> None:
        self.r = region
    
    def __call__(self, image):
        if self.r == 1:
            return np.where(image > 0, 64, image)
