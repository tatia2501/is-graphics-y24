import numpy as np
import math

def scaling(size_x, size_y, method_var, param_b, param_c, pixels):
    if (method_var == "ближайшая точка"):
        return nearest_point(size_x, size_y, pixels)
    elif (method_var == "билинейное"):
        return bilinear(size_x, size_y, pixels)
    elif (method_var == "Lanczos3"):
        return lanczos(size_x, size_y, pixels)
    else:
        return bc_splines(size_x, size_y, param_b, param_c, pixels)

def nearest_point(size_x, size_y, pixels):
    old_size_x, old_size_y, _ = pixels.shape
    new_buffer = np.zeros((size_x, size_y, 3),dtype=np.uint8)
    for i in range(size_x):
        for j in range(size_y):
            x_coo = math.floor(i*(old_size_x/size_x))
            y_coo = math.floor(j*(old_size_y/size_y))
            new_buffer[i, j] = pixels[x_coo, y_coo]
    return new_buffer

def bilinear(size_x, size_y, pixels):
    old_size_x, old_size_y, _ = pixels.shape
    new_buffer = np.zeros((size_x, size_y, 3), dtype=np.uint8)
    x_ratio = (old_size_x - 1) / size_x
    y_ratio = (old_size_y - 1) / size_y
    for i in range(0, size_y):
        for j in range(0, size_x):
            x = int(x_ratio * j)
            y = int(y_ratio * i)
            x_diff = (x_ratio * j) - x
            y_diff = (y_ratio * i) - y

            a = pixels[x, y]
            b = pixels[x + 1, y]
            c = pixels[x, y + 1]
            d = pixels[x + 1, y + 1]

            blue = a[2] * (1 - x_diff) * (1 - y_diff) + b[2] * (x_diff) * (1 - y_diff) + c[2] * (y_diff) * (1 - x_diff) + d[2] * (x_diff * y_diff)
            green = a[1] * (1 - x_diff) * (1 - y_diff) + b[1] * (x_diff) * (1 - y_diff) + c[1] * (y_diff) * (1 - x_diff) + d[1] * (x_diff * y_diff)
            red = a[0] * (1 - x_diff) * (1 - y_diff) + b[0] * (x_diff) * (1 - y_diff) + c[0] * (y_diff) * (1 - x_diff) + d[0] * (x_diff * y_diff)

            new_buffer[j, i][0], new_buffer[j, i][1], new_buffer[j, i][2] = red, green, blue
    return new_buffer

def pixel_formula(param_b, param_c, a, b, c, d, dis):
    return (((-1/6 * param_b - param_c) * a + (-3/2 * param_b - param_c + 2) * b + (
        3/2 * param_b + param_c - 2) * c + (1/6 * param_b + param_c) * d) * dis*dis*dis + (
        (1/2 * param_b + 2 * param_c) * a + (2 * param_b + param_c - 3) * b + (
        -5/2 * param_b - 2 * param_c + 3) * c - param_c * d) * dis*dis + (
        ((-1/2 * param_b - param_c) * a + (1/2 * param_b + param_c) * c) * dis + (
        1/6 * param_b * a) + (-1/3 * param_b + 1) * b + (1/6 * param_b * c)))

def bc_splines(size_x, size_y, param_b, param_c, pixels):
    old_size_x, old_size_y, _ = pixels.shape
    new_buffer = np.zeros((size_x, size_y, 3), dtype=np.uint8)
    x_ratio = (old_size_x - 1) / size_x
    y_ratio = (old_size_y - 1) / size_y
    for i in range(0, size_y):
        for j in range(0, size_x):
            x = int(x_ratio * j)
            y = int(y_ratio * i)

            a = pixels[x - 1, y]
            b = pixels[x + 1, y]
            c = pixels[x, y - 1]
            d = pixels[x, y + 1]

            blue = pixel_formula(param_b, param_c, a[2], b[2], c[2], d[2], 1)
            green = pixel_formula(param_b, param_c, a[1], b[1], c[1], d[1], 1)
            red = pixel_formula(param_b, param_c, a[0], b[0], c[0], d[0], 1)

            new_buffer[j, i][0], new_buffer[j, i][1], new_buffer[j, i][2] = red, green, blue
    return new_buffer

def sinc(x):
    x = (x * 3.1415926)
    if ((x < 0.01) and (x > -0.01)):
        return 1.0 + x * x * (-1.0 / 6.0 + x * x * 1.0 / 120.0)
    return math.sin(x) / x

def clip(t):
    eps = 0.0000125
    if (math.fabs(t) < eps):
        return 0.0
    return float(t)

def lancos(t):
    if (t < 0.0):
        t = -t
    if (t < 3.0):
        return clip(sinc(t) * sinc(t / 3.0))
    else:
        return (0.0)

def lancos3_resample_x(arr, src_w,  src_h, y,  x, xscale):
    s = 0
    coef_sum = 0.0
    if (xscale > 1.0):
        hw = 3.0
    else:
        hw = 3.0 / xscale

    c = float(x) / xscale
    l = int(math.floor(c - hw))
    r = int(math.ceil(c + hw))

    if (y < 0):
        y = 0
    if (y >= src_h):
        y = src_h - 1
    if (xscale > 1.0):
        xscale = 1.0

    for i in range(l, r+1):
        x = i
        if (i < 0):
            x = 0
        if (i >= src_w):
            x = src_w - 1
        pix = arr[y][x]
        coef = lancos((c-i)*xscale)
        s += pix * coef
        coef_sum += coef
    s /= coef_sum
    return s

def img_resize_using_lancos3(src, dst):
    dst_cols = dst.shape[0]
    src_arr = src
    dst_arr = dst
    src_rows = src.shape[1]
    src_cols = src.shape[0]
    dst_rows = dst.shape[1]
    xratio = float(dst_cols) / float(src_cols)
    yratio = float(dst_rows) / float(src_rows)

    scale = 0.0
    if (yratio > 1.0):
        hw = 3.0
        scale = 1.0
    else:
        hw = 3.0 / yratio
        scale = yratio

    for i in range(0, dst_rows):
        for j in range(0, dst_cols):
            s = 0
            coef_sum = 0.0
            c = float(i) / yratio
            t = int(math.floor(c - hw))
            b = int(math.ceil(c + hw))

            for k in range(t, b+1):
                pix = lancos3_resample_x(src_arr, src_cols, src_rows, k, j, xratio)
                coef = lancos((c - k) * scale)
                coef_sum += coef
                pix *= coef
                s += pix
            val = int(s) / coef_sum
            if (val < 0):
                val = 0
            if (val > 255):
                val = 255
            dst_arr[i][j] = val
    return dst_arr

def lanczos(size_x, size_y, pixels):
    old_size_x, old_size_y, _ = pixels.shape
    new_buffer = np.zeros((size_x, size_y, 3), dtype=np.uint8)

    canal_0 = pixels[:, :, 0]
    canal_1 = pixels[:, :, 1]
    canal_2 = pixels[:, :, 2]

    canal_0_new = new_buffer[:, :, 0]
    canal_1_new = new_buffer[:, :, 1]
    canal_2_new = new_buffer[:, :, 2]

    canal_0_eq = img_resize_using_lancos3(canal_0, canal_0_new)
    canal_1_eq = img_resize_using_lancos3(canal_1, canal_1_new)
    canal_2_eq = img_resize_using_lancos3(canal_2, canal_2_new)

    buffer = np.dstack(tup=(canal_0_eq, canal_1_eq, canal_2_eq))

    return buffer