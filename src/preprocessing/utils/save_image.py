import os
import imageio


def save_image_as_png(data, path, filename):
    fdata = data
    (_, _, z) = fdata.shape
    for k in range(z):
        slice = fdata[k, :, :]
        imageio.imwrite(os.path.join(path, '{}.png'.format(filename)), slice)