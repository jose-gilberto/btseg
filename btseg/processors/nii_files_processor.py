from glob import glob
from btseg.transformers.nii_transformers import NiiToImage
from btseg.util.save_image import save_image_as_png
import os

class NiiFilesProcessor:

    def __init__(self, path: str, outpath: str) -> None:
        self.path = path
        self.transform = NiiToImage()
        self.out = outpath

    def getting_all_paths(self):
        paths = glob(self.path + '/*.nii')
        return paths

    def run(self):
        nii_paths = self.getting_all_paths()

        for index, nii_file in enumerate(nii_paths):
            os.makedirs(f'{self.out}/{index}/')
            # Transform into a img
            image_3d = self.transform(nii_file)
            path = f'{self.out}/{index}/'
            save_image_as_png(image_3d, path)

