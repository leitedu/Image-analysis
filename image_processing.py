import os
import numpy as np
from PIL import Image

# Reads image from path and returns image and corresponding array
def read_image(path):
    im = Image.open(path)
    im_array = np.array(im).astype(np.int16)
    return im, im_array

# Verifies technique used based on characteristic magnitude of RGB channels (fluorescence is "darker")
def technique_identifier(img):
    verify = Image.open(img)
    verify_array = np.array(verify).astype(np.int16)
    avg = np.average(verify_array)
    if avg < 50:
        return 1
    else:
        return 0

# Takes average of pictures from a specified folder and returns it and corresponding array
def average_images(path):

    files = os.listdir(path)
    arrays = []

    for photo in files:
        img_path = path / photo
        img = Image.open(img_path)
        img_array = np.array(img).astype(np.int16)
        arrays.append(img_array)

    avg_array = np.average(arrays, axis=0)
    avg_image = Image.fromarray(np.round(avg_array).astype(np.uint8))

    return avg_image, avg_array

# Applies LUMA conversion to generate brightness map from RGB image diference
def luma(img, param_luma):           
    img_dif = np.zeros((img.shape[0], img.shape[1]))
    for i in range(3):
        img_dif[:, :] += param_luma[i]*np.clip(img[:, :, i], a_min=0, a_max=None)

    return img_dif
