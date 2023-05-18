from tkinter import *
from PIL import Image
import numpy as np
import numpy.ma as ma

def show_histogram(buffer, canal):
    image_temp = Image.fromarray(buffer.astype('uint8'))
    w = image_temp.size[0]
    h = image_temp.size[1]
    bins = np.zeros(256, dtype=int)

    for i in range(h):
        for j in range(w):
            bins[int(buffer[i, j][canal])] += 1

    size_x = np.max(bins) + 1
    gis_buffer = np.empty((size_x, 512, 3), dtype="float32")
    for i in range(size_x):
        for j in range(512):
            gis_buffer[i, j][0], gis_buffer[i, j][1], gis_buffer[i, j][2] = 255, 255, 255

    for j in range(512):
        for i in range(bins[int(j/2)]):
            gis_buffer[size_x - i - 1, j][0], gis_buffer[size_x - i - 1, j][1], gis_buffer[size_x - i - 1, j][2] = 0, 0, 0

    return gis_buffer

def do_autocorrection(buffer, coef):
    canal_0 = buffer[:, :, 0]
    canal_1 = buffer[:, :, 1]
    canal_2 = buffer[:, :, 2]

    canal_0_eq = enhance_contrast(canal_0, coef)
    canal_1_eq = enhance_contrast(canal_1, coef)
    canal_2_eq = enhance_contrast(canal_2, coef)

    buffer = np.dstack(tup=(canal_0_eq, canal_1_eq, canal_2_eq))
    return buffer

def enhance_contrast(image_matrix, coef):
    image_flattened = image_matrix.flatten()
    image_hist = np.zeros(256)
    ign_num = int(coef * 128)

    for pix in image_matrix:
        image_hist[pix] += 1

    for i in range(ign_num):
        image_hist[i] = 0
        image_hist[255-i] = 0

    cum_sum = np.cumsum(image_hist)
    cum_sum = np.array(cum_sum)
    norm = (cum_sum - cum_sum.min()) * 255
    n_ = cum_sum.max() - np.min(ma.masked_where(cum_sum == 0, cum_sum))
    uniform_norm = norm / n_
    uniform_norm = uniform_norm.astype('int')

    image_eq = uniform_norm[image_flattened]
    image_eq = np.reshape(a=image_eq, newshape=image_matrix.shape)

    return image_eq