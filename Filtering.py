import math

import numpy as np
from PIL import Image

def do_threshold_filtering(buffer, threshold):
    image_temp = Image.fromarray(buffer.astype('uint8'))
    W = image_temp.size[0]
    H = image_temp.size[1]
    C = 3

    for i in range(H):
        for j in range(W):
            for k in range(C):
                if (buffer[i,j][k] > threshold):
                    buffer[i, j][k] = 255
                else:
                    buffer[i, j][k] = 0
    return buffer

def square_matrix(square, coef):
    num = coef * 2 + 1
    tot_sum = 0

    for i in range(num):
        for j in range(num):
            tot_sum += square[i][j]
    return tot_sum // (num * num)

def boxBlur(image, coef):
    num = coef * 2 + 1
    square = []
    square_row = []
    blur_row = []
    blur_img = []
    n_rows = len(image)
    n_col = len(image[0])
    rp, cp = 0, 0
    while rp <= n_rows - num:
        while cp <= n_col - num:
            for i in range(rp, rp + num):
                for j in range(cp, cp + num):
                    square_row.append(image[i][j])
                square.append(square_row)
                square_row = []
            blur_row.append(square_matrix(square, coef))
            square = []
            cp = cp + 1
        blur_img.append(blur_row)
        blur_row = []
        rp = rp + 1
        cp = 0
    return blur_img

def do_averaging_filtering(buffer, coef):
    canal_0 = buffer[:, :, 0]
    canal_1 = buffer[:, :, 1]
    canal_2 = buffer[:, :, 2]

    canal_0_eq = boxBlur(canal_0, coef)
    canal_1_eq = boxBlur(canal_1, coef)
    canal_2_eq = boxBlur(canal_2, coef)

    buffer = np.dstack(tup=(canal_0_eq, canal_1_eq, canal_2_eq))
    return buffer

def do_gauss_filtering(buffer, coef):
    K_size = int(3 * coef)
    image_temp = Image.fromarray(buffer.astype('uint8'))
    W = image_temp.size[0]
    H = image_temp.size[1]
    C = 3

    pad = K_size // 2
    out = np.zeros((H + pad * 2, W + pad * 2, C), dtype=np.float)
    out[pad: pad + H, pad: pad + W] = buffer.copy().astype(np.float)

    K = np.zeros((K_size, K_size), dtype=np.float)
    for x in range(-pad, -pad + K_size):
        for y in range(-pad, -pad + K_size):
            K[y + pad, x + pad] = np.exp(-(x ** 2 + y ** 2) / (2 * (coef ** 2)))
    K /= (2 * np.pi * coef * coef)
    K /= K.sum()
    tmp = out.copy()

    for y in range(H):
        for x in range(W):
            for c in range(C):
                out[pad + y, pad + x, c] = np.sum(K * tmp[y: y + K_size, x: x + K_size, c])
    out = np.clip(out, 0, 255)
    out = out[pad: pad + H, pad: pad + W].astype(np.uint8)
    return out

def square_matrix_for_med(square, coef):
    num = coef * 2 + 1
    square = np.array(square)
    square = np.reshape(square, num * num)
    square = np.sort(square)

    return square[int(square.shape[0] / 2)]

def median(image, coef):
    num = coef * 2 + 1
    square = []
    square_row = []
    blur_row = []
    blur_img = []
    n_rows = len(image)
    n_col = len(image[0])
    rp, cp = 0, 0
    while rp <= n_rows - num:
        while cp <= n_col - num:
            for i in range(rp, rp + num):
                for j in range(cp, cp + num):
                    square_row.append(image[i][j])
                square.append(square_row)
                square_row = []
            blur_row.append(square_matrix_for_med(square, coef))
            square = []
            cp = cp + 1
        blur_img.append(blur_row)
        blur_row = []
        rp = rp + 1
        cp = 0
    return blur_img

def do_median_filtering(buffer, coef):
    canal_0 = buffer[:, :, 0]
    canal_1 = buffer[:, :, 1]
    canal_2 = buffer[:, :, 2]

    canal_0_eq = median(canal_0, coef)
    canal_1_eq = median(canal_1, coef)
    canal_2_eq = median(canal_2, coef)

    buffer = np.dstack(tup=(canal_0_eq, canal_1_eq, canal_2_eq))
    return buffer

def do_sobel_filtering(buffer):
    G_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    G_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    rows = np.size(buffer, 0)
    columns = np.size(buffer, 1)
    mag = np.zeros(buffer.shape)
    for i in range(0, rows - 2):
        for j in range(0, columns - 2):
            v = sum(sum(G_x * buffer[i:i + 3, j:j + 3][0]))
            h = sum(sum(G_y * buffer[i:i + 3, j:j + 3][0]))
            mag[i + 1, j + 1] = np.sqrt((v ** 2) + (h ** 2))

    for p in range(0, rows):
        for q in range(0, columns):
            if mag[p, q] < 70:
                mag[p, q] = 0
    return mag

def osu_count_threshold(buff, w, h):
    min = np.min(buff)
    max = np.max(buff)

    histSize = max - min + 1
    hist = np.zeros(histSize)

    for i in range(h):
        for j in range(w):
            hist[buff[i][j] - min] += 1

    m = 0
    n = 0

    for i in range(max - min + 1):
        m += i * hist[i]
        n += hist[i]

    maxSigma = -1.0
    threshold = 0
    alpha1 = 0
    beta1 = 0

    for i in range(max - min):
        alpha1 += i * hist[i]
        beta1 += hist[i]

        w1 = beta1 / n
        a = alpha1 / beta1 - (float)(m - alpha1) / (n - beta1)

        sigma = w1 * (1 - w1) * a * a

        if (sigma > maxSigma):
            maxSigma = sigma
            threshold = i

    threshold += min
    return threshold

def do_ocu_filtering(buffer):
    image_temp = Image.fromarray(buffer.astype('uint8'))
    W = image_temp.size[0]
    H = image_temp.size[1]
    C = 3
    threshold = osu_count_threshold(buffer[:, :, 0], W, H)

    for i in range(H):
        for j in range(W):
            for k in range(C):
                if (buffer[i,j][k] > threshold):
                    buffer[i, j][k] = 255
                else:
                    buffer[i, j][k] = 0
    return buffer

def lerp(a, b, t):
    return (1 - t) * a + t * b

def do_sharpening_filtering(buffer, coef):
    weights = np.copy(buffer)
    image_temp = Image.fromarray(buffer.astype('uint8'))
    W = image_temp.size[0]
    H = image_temp.size[1]
    for i in range(1, H-1):
        for j in range(1, W-1):
            min_g = min(weights[i][j][1], weights[i - 1][j][1], weights[i + 1][j][1], weights[i][j - 1][1], weights[i][j + 1][1]) / 255
            max_g = max(weights[i][j][1], weights[i - 1][j][1], weights[i + 1][j][1], weights[i][j - 1][1], weights[i][j + 1][1]) / 255
            d_min_g = 0 + min_g
            d_max_g = 1 - max_g

            if (d_max_g > d_min_g):
                if (min_g == 0):
                    a = 0
                else:
                    a = d_min_g / max_g
            else:
                a = d_max_g / max_g

            a = math.sqrt(a) # ?

            dev_max = lerp(-0.125, -0.2, coef)
            w = a * dev_max
            for k in range(3):
                pix = (w * weights[i-1][j][k] + w * weights[i][j-1][k] + weights[i][j][k] + w * weights[i][j+1][k] + w * weights[i+1][j][k]) / (w * 4 + 1)
                if (pix < 0):
                    # pix = 0
                    pix = buffer[i,j][k]
                if (pix > 255):
                    # pix = 255
                    pix = buffer[i, j][k]
                buffer[i,j][k] = pix
    return buffer