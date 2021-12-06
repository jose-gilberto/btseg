import os
import math
from typing import List
from glob import glob

import pandas as pd
import numpy as np
import cv2
import btseg.transformers as t


class TimeSeriesProcessor:

    def __init__(
        self,
        path: str,
        region: int = 1,
        angles: int = 720) -> None:
        self.path = path
        self.region = region
        self.angles = angles

    def slice_selection(self) -> pd.DataFrame:
        paths = glob(self.path + '/*/')
        ids = list(range(1, len(paths) + 1, 1))

        initial_dataframe = pd.DataFrame({
            'id': ids,
            'path': paths
        })

        transforms = t.Compose([
            t.ConvertColor(conversion_code=cv2.COLOR_BGR2GRAY),
            t.RegionSelection(region=self.region),
            t.GaussianBlur(kernel_size=(7, 7), sigma_x=0),
            t.CannyEdge(threshold_1=50, threshold_2=100),
            t.Dilate(kernel=None, iterations=1),
            t.Erode(kernel=None, iterations=1)
        ])

        # array with all paths to correct slices for each tumor
        max_slice = []

        for value in initial_dataframe.values:
            id, path = value
            images = glob(f'{path}/*')
            max_area = 0
            max_slice_path = None

            for image_path in images:
                image = cv2.imread(image_path)
                transformed_image = transforms(image)
                cnts, _ = cv2.findContours(transformed_image.copy(),
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
                cnts_areas = [(cv2.contourArea(c), c) for c in cnts]
                # Take care of slices without tumor segments
                maximum_contour = max(cnts_areas, key=lambda x: x[0]) if cnts_areas != [] else (0, None)

                if maximum_contour[0] >= max_area:
                    max_area = maximum_contour[0]
                    max_slice_path = image_path

            max_slice.append(max_slice_path)

        initial_dataframe['slice_path'] = max_slice
        return initial_dataframe

    def generating_time_series(self, dataframe: pd.DataFrame):
        new_dataframe = pd.DataFrame()
        new_dataframe['id'] = dataframe['id']

        for i in range(self.angles):
            new_dataframe[f'a_{i}'] = None

        transforms = t.Compose([
            t.ConvertColor(conversion_code=cv2.COLOR_BGR2GRAY),
            t.RegionSelection(region=self.region),
            t.Resize(proportion_scale=True, g_measure=700),
            t.GaussianBlur(kernel_size=(7, 7), sigma_x=0),
            t.CannyEdge(threshold_1=50, threshold_2=100),
            t.Dilate(kernel=None, iterations=1),
            t.Erode(kernel=None, iterations=1),
            t.MinimumBoundingBox(),
        ])

        for value in dataframe.values:
            id, path = value[0], value[2]
            image = cv2.imread(path)
            image_transformed = transforms(image)

            contours, _ = cv2.findContours(image_transformed,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
            contours_areas = [(cv2.contourArea(c), c) for c in contours]
            maximum_contour = max(contours_areas, key=lambda x: x[0])

            ref = np.zeros_like(image_transformed)
            cv2.drawContours(ref, [maximum_contour[1]], 0, 255, 1)

            M = cv2.moments(ref)
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])

            width = image_transformed.shape[1]
            height = image_transformed.shape[0]

            distances = []
            N = self.angles

            for i in np.arange(0, N, 1):
                tmp = np.zeros_like(image_transformed)
                theta = i * (360 / N)
                theta *= np.pi / 180 
                cv2.line(
                    tmp,
                    (centroid_x, centroid_y),
                    (int(centroid_x + np.cos(theta) * width),
                     int(centroid_y - np.sin(theta) * height)), 255, 5
                )

                (row, col) = np.nonzero(np.logical_and(tmp, ref))
                try:
                    distance = math.sqrt(
                        (col[0] - centroid_x)**2 +
                        (row[0] - centroid_y)**2
                    ) 
                    distances.append(distance)
                except:
                    distances.append(distance)

            for index, distance in enumerate(distances):
                new_dataframe.loc[new_dataframe['id'] == id, f'a_{index}'] = distance

        return new_dataframe

    def run(self) -> pd.DataFrame:
        initial_dataframe = self.slice_selection()
        final_dataframe = self.generating_time_series(initial_dataframe)

        return final_dataframe

