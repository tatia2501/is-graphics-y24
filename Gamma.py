import numpy as np

def to_new_gamma(buffer, gamma):
    if gamma == -1:
        return to_sRGB(buffer)
    if gamma == 0:
        return from_sRGB(buffer)

    return np.array(255 * (buffer / 255) ** gamma, dtype='uint8')

def to_sRGB(buffer):
    new_buffer = np.zeros((len(buffer[0]), len(buffer[0]), 3), dtype="float32")
    for i in range(len(buffer)):
        for j in range(len(buffer[0])):
            for k in range(3):
                if buffer[i, j][k]/255 <= 0.0031308:
                    new_buffer[i, j][k] = 12.92 * buffer[i, j][k]
                else:
                    new_buffer[i, j][k] = 255 * (1.055 * (buffer[i, j][k] / 255) ** (1/2.4) - 0.055)

    return new_buffer

def from_sRGB(buffer):
    new_buffer = np.zeros((len(buffer[0]), len(buffer[0]), 3), dtype="float32")
    for i in range(len(buffer)):
        for j in range(len(buffer[0])):
            for k in range(3):
                if (buffer[i, j][k] / 255) <= 0.04045:
                    new_buffer[i, j][k] = buffer[i, j][k] / 12.92
                else:
                    new_buffer[i, j][k] = 255 * ((buffer[i, j][k] / 255 + 0.055) / 1.055) ** 2.4

    return new_buffer
