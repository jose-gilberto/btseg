import nibabel as nib


class NiiToImage:

    def __init__(self) -> None:
        pass

    def __call__(self, nii_file: str):
        img = nib.load(nii_file)
        img_fdata = img.get_fdata()
        return img_fdata
