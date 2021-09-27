import glob
import os
from btseg.transformers import Compose, NiiToImage
from btseg.util.save_image import save_image_as_png


class BratsPreprocessor:

    def __init__(self, data_dir: str, out_dir: str) -> None:
        self.data_dir = data_dir
        self.out_dir = out_dir

    def run(self):
        files = glob.glob(os.path.join(
            self.data_dir, '*.nii'
        )) # find all files with nii extension

        # generating the transformers
        pre_transformers = Compose([
            NiiToImage()
        ])

        for f in files:
            img = pre_transformers(f)

            ffolder = f.split('\\')[-1].replace('_seg.nii', '')
            ffolder = os.path.join(
                self.out_dir, ffolder
            ) 
            os.mkdir(ffolder)

            save_image_as_png(img, ffolder)

        

        # get all directories files
        # get all .seg files
        # extract each one

        # extract the survival rate, age and extent of resection in csv
        # extract the grade in csv