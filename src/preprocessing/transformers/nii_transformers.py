import nibabel as nib


def read_nii_file(nii_file):
    img = nib.load(nii_file)
    img_fdata = img.get_fdata()
    return img_fdata
