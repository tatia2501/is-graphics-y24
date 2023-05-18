import numpy as np
from PIL import Image
import random
import math

def make_matrix(m):
    a = int(m/2)
    mul_m = np.arange(a*a).reshape(a, a)
    if m > 2:
        pred_m = make_matrix(a)
    else:
        return [[2, 0], [1, 3]]
    for i in range(a):
        for j in range(a):
            mul_m[i][j] = pred_m[i][j] * 4
    m_1 = np.arange(a * a).reshape(a, a)
    m_2 = np.arange(a * a).reshape(a, a)
    m_3 = np.arange(a * a).reshape(a, a)
    m_4 = np.arange(a * a).reshape(a, a)
    for i in range(a):
        for j in range(a):
            m_1[i][j] = mul_m[i][j] + 2
    for i in range(a):
        for j in range(a):
            m_2[i][j] = mul_m[i][j]
    for i in range(a):
        for j in range(a):
            m_3[i][j] = mul_m[i][j] + 1
    for i in range(a):
        for j in range(a):
            m_4[i][j] = mul_m[i][j] + 3
    return np.vstack([np.hstack([m_1, m_2]), np.hstack([m_3, m_4])])

def ordered(buffer, bt):
    image_temp = Image.fromarray(buffer.astype('uint8'))
    w = image_temp.size[0]
    h = image_temp.size[1]
    indexMatrix = make_matrix(8)
    arr = np.array(buffer, dtype=float) / 255
    nc = pow(2, bt)
    coef = 1/(nc-1)

    for i in range(h):
        for j in range(w):
            old_val = arr[i, j].copy()
            new_val = np.round(old_val * (nc - 1)) / (nc - 1)
            arr[i, j] = new_val
            err = old_val - new_val

            diff = (indexMatrix[i % 8][j % 8] / 64 ) * coef
            c0 = err[0] + diff
            c1 = err[1] + diff
            c2 = err[2] + diff
            if (c0 > coef):
                if (err[0] > 0):
                    arr[i, j][0] += coef
            if (c0 < 0):
                if (err[0] < 0):
                    arr[i,j][0] -= coef
            if (c1 > coef):
                if (err[1] > 0):
                    arr[i, j][1] += coef
            if (c1 < 0):
                if (err[1] < 0):
                    arr[i, j][1] -= coef
            if (c2 > coef):
                if (err[2] > 0):
                    arr[i, j][2] += coef
            if (c2 < 0):
                if (err[2] < 0):
                    arr[i,j][2] -= coef
    return np.array(arr/np.max(arr, axis=(0,1)) * 255)

def random_func(buffer, bt):
    arr = np.array(buffer, dtype=float) / 255
    nc = pow(2, bt)
    coef = 1/(nc-1)
    image_temp = Image.fromarray(buffer.astype('uint8'))
    w = image_temp.size[0]
    h = image_temp.size[1]

    for i in range(h):
        for j in range(w):
            old_val = arr[i, j].copy()
            new_val = np.round(old_val * (nc - 1)) / (nc - 1)
            arr[i, j] = new_val
            err = old_val - new_val

            rnd = random.random() * coef
            c0 = err[0] + rnd
            c1 = err[1] + rnd
            c2 = err[2] + rnd
            if (c0 > coef):
                if (err[0] > 0):
                    arr[i, j][0] += coef
            if (c0 < 0):
                if (err[0] < 0):
                    arr[i,j][0] -= coef
            if (c1 > coef):
                if (err[1] > 0):
                    arr[i, j][1] += coef
            if (c1 < 0):
                if (err[1] < 0):
                    arr[i, j][1] -= coef
            if (c2 > coef):
                if (err[2] > 0):
                    arr[i, j][2] += coef
            if (c2 < 0):
                if (err[2] < 0):
                    arr[i,j][2] -= coef
    return np.array(arr/np.max(arr, axis=(0,1)) * 255)

def atkinson(buffer, bt):
    arr = np.array(buffer, dtype=float) / 255
    nc = pow(2, bt)
    image_temp = Image.fromarray(buffer.astype('uint8'))
    w = image_temp.size[0]
    h = image_temp.size[1]

    for i in range(h):
        for j in range(w):
            old_val = arr[i, j].copy()
            new_val = np.round(old_val * (nc - 1)) / (nc - 1)
            arr[i, j] = new_val
            err = old_val - new_val

            if (j + 1 < w):
                arr[i, j + 1] += err / 8
            if (j + 1 < w and i + 1 < h):
                arr[i + 1, j + 1] += err / 8
            if (i + 1 < h):
                arr[i + 1, j] += err / 8
            if (i + 1 < h and j > 0):
                arr[i + 1, j - 1] += err / 8
            if (i + 2 < h):
                arr[i + 2, j] += err / 8
            if (j + 2 < w):
                arr[i, j + 2] += err / 8
    return np.array(arr/np.max(arr, axis=(0,1)) * 255)

def floyd_steinberg(buffer, bt):
    arr = np.array(buffer, dtype=float) / 255
    nc = pow(2, bt)
    image_temp = Image.fromarray(buffer.astype('uint8'))
    w = image_temp.size[0]
    h = image_temp.size[1]

    for i in range(h):
        for j in range(w):
            old_val = arr[i, j].copy()
            new_val = np.round(old_val * (nc - 1)) / (nc - 1)
            arr[i, j] = new_val
            err = old_val - new_val

            if (j + 1 < w):
                arr[i, j + 1] += err * 7 / 16
            if (j + 1 < w and i + 1 < h):
                arr[i + 1, j + 1] += err / 16
            if (i + 1 < h):
                arr[i + 1, j] += err * 5 / 16
            if (i + 1 < h and j > 0):
                arr[i + 1, j - 1] += err * 3 / 16
    return np.array(arr/np.max(arr, axis=(0,1)) * 255)

def gradient(x, y):
    buffer = np.empty((y, x, 3), dtype="float32")
    diff = 255/(x-1)
    for i in range(x):
        for j in range(y):
            buffer[j,i][0], buffer[j,i][1], buffer[j,i][2] = diff * i, diff * i, diff * i

    return buffer