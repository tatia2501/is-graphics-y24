import numpy as np

def RGB_CMY(R, G, B):
    C = 1.0 - (R / 255.0)
    M = 1.0 - (G / 255.0)
    Y = 1.0 - (B / 255.0)
    return C, M, Y

def CMY_RGB(C, M, Y):
    R = 255.0 * (1.0 - C)
    G = 255.0 * (1.0 - M)
    B = 255.0 * (1.0 - Y)
    return R, G, B

def RGB_YCoCg(R, G, B):
    matrix = np.array([[1/4, 1/2, 1/4], [1/2, 0, -1/2], [-1/4, 1/2, -1/4]])
    rgb = np.array([R, G, B])
    res = matrix.dot(rgb)
    return res[0], res[1], res[2]

def YCoCg_RGB(Y, Co, Cg):
    tmp = Y - Cg
    R = tmp + Co
    G = Y + Cg
    B = tmp - Co
    return R, G, B

def RGB_YCbCr601(R, G, B):
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    Cb = (B - Y) / 1.772
    Cr = (R - Y) / 1.402
    return Y, Cb, Cr

def YCbCr601_RGB(Y, Cb, Cr):
    R = Y + 1.402 * Cr
    G = Y - (0.299 * 1.402 / 0.587) * Cr - (0.114 * 1.772 / 0.587) * Cb
    B = Y + 1.772 * Cb
    return R, G, B

def RGB_YCbCr709(R, G, B):
    Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
    Cb = (B - Y) / 1.8556
    Cr = (R - Y) / 1.5748
    return Y, Cb, Cr

def YCbCr709_RGB(Y, Cb, Cr):
    R = Y + 1.5748 * Cr
    G = Y - (0.2126 * 1.5748 / 0.7152) * Cr - (0.0722 * 1.8556 / 0.7152) * Cb
    B = Y + 1.8556 * Cb
    return R, G, B

def RGB_HSV(R, G, B):
    R, G, B = R / 255.0, G / 255.0, B / 255.0
    Cmax = max(R, G, B)
    Cmin = min(R, G, B)
    Cdelta = Cmax-Cmin

    if Cdelta == 0:
        H = 0
    elif Cmax == R:
        H = 60 * (((G - B) / Cdelta) % 6)
    elif Cmax == G:
        H = 60 * ((B - R) / Cdelta + 2)
    elif Cmax == B:
        H = 60 * ((R - G) / Cdelta + 4)

    if Cmax == 0:
        S = 0
    else:
        S = Cdelta/Cmax

    V = Cmax

    return H, S, V

def HSV_RGB(H, S, V):
    C = V*S
    X = C * (1 - abs((H/60) % 2 - 1))
    m = V - C
    if H >= 0 and H < 60:
        R = (C + m) * 255
        G = (X + m) * 255
        B = m * 255
    elif H >= 60 and H < 120:
        R = (X + m) * 255
        G = (C + m) * 255
        B = m * 255
    elif H >= 120 and H < 180:
        R = m * 255
        G = (C + m) * 255
        B = (X + m) * 255
    elif H >= 180 and H < 240:
        R = m * 255
        G = (X + m) * 255
        B = (C + m) * 255
    elif H >= 240 and H < 300:
        R = (X + m) * 255
        G = m * 255
        B = (C + m) * 255
    elif H >= 300 and H < 360:
        R = (C + m) * 255
        G = m * 255
        B = (X + m) * 255

    return R, G, B

def RGB_HSL(R, G, B):
    R, G, B = R / 255.0, G / 255.0, B / 255.0
    Cmax = max(R, G, B)
    Cmin = min(R, G, B)
    Cdelta = Cmax-Cmin

    if Cdelta == 0:
        H = 0
    elif Cmax == R:
        H = 60 * (((G - B) / Cdelta) % 6)
    elif Cmax == G:
        H = 60 * ((B - R) / Cdelta + 2)
    elif Cmax == B:
        H = 60 * ((R - G) / Cdelta + 4)

    L = (Cmax + Cmin)/2

    if Cdelta == 0:
        S = 0
    else:
        S = Cdelta/(1 - abs(2 * L - 1))

    return H, S, L

def HSL_RGB(H, S, L):
    C = (1 - abs(2 * L - 1)) * S
    X = C * (1 - abs((H/60) % 2 - 1))
    m = L - C/2
    if H >= 0 and H < 60:
        R = (C + m) * 255
        G = (X + m) * 255
        B = m * 255
    elif H >= 60 and H < 120:
        R = (X + m) * 255
        G = (C + m) * 255
        B = m * 255
    elif H >= 120 and H < 180:
        R = m * 255
        G = (C + m) * 255
        B = (X + m) * 255
    elif H >= 180 and H < 240:
        R = m * 255
        G = (X + m) * 255
        B = (C + m) * 255
    elif H >= 240 and H < 300:
        R = (X + m) * 255
        G = m * 255
        B = (C + m) * 255
    elif H >= 300 and H < 360:
        R = (C + m) * 255
        G = m * 255
        B = (X + m) * 255

    return R, G, B

def to_RGB(space, buffer):
    new_buffer = np.empty((len(buffer[0]), len(buffer[0]), 3), dtype="float32")
    match space:
        case "HSL":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = HSL_RGB(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
        case "HSV":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = HSV_RGB(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
        case "YCbCr601":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = YCbCr601_RGB(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
        case "YCbCr709":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = YCbCr709_RGB(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
        case "YCoCg":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = YCoCg_RGB(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
        case "CMY":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = CMY_RGB(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
    return new_buffer

def from_RGB(space, buffer):
    new_buffer = np.empty((len(buffer[0]), len(buffer[0]), 3), dtype="float32")
    match space:
        case "HSL":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = RGB_HSL(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
        case "HSV":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = RGB_HSV(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
        case "YCbCr601":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = RGB_YCbCr601(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
        case "YCbCr709":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = RGB_YCbCr709(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
        case "YCoCg":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = RGB_YCoCg(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
        case "CMY":
            for i in range(len(buffer)):
                for j in range(len(buffer[i])):
                    new_buffer[i, j][0], new_buffer[i, j][1], new_buffer[i, j][2] = RGB_CMY(buffer[i, j][0], buffer[i, j][1], buffer[i, j][2])
    return new_buffer