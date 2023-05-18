import re
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def convert(img, title=None):
    img_name = 'test.png'
    if title is not None:
        plt.title(title)
        img_name = title + '.png'
    plt.imsave(img_name, img)


def catch_error(expression, exception_type=RuntimeError):
    if not expression:
        raise exception_type()


def read(filespec):
    valid_extensions = [".pnm", ".ppm", ".pgm", ".PNM", ".PPM", ".PGM"]
    catch_error(isinstance(filespec, str) and len(filespec) >= 5)
    catch_error(filespec[-4:] in valid_extensions)
    with open(filespec, "rb") as f:
        buf = f.read()
        regex_pnm_header = b"(^(P[56])\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s)"
        match = re.search(regex_pnm_header, buf)
        if match is not None:
            header, typestr, width, height, maxval = match.groups()
            width, height, maxval = int(width), int(height), int(maxval)
            if typestr == b"P6": numch = 3
            else: numch = 1
            if typestr == b"P6": shape = (height, width, numch)
            else: shape = (height, width)
            if maxval > 255:
                dtype = ">u2"
            else:
                dtype = np.uint8
            pixels = np.frombuffer(buf, dtype, count=width * height * numch, offset=len(header))
            if maxval <= 255:
                pixels = pixels.reshape(shape).astype(np.uint8)
            else:
                pixels = pixels.reshape(shape).astype(np.uint16)
            return header, pixels, maxval
        raise RuntimeError()


def write(filespec, image, maxval, p=""):
    valid_extensions = [".pnm", ".ppm", ".PNM", ".PPM"]
    catch_error(isinstance(filespec, str) and len(filespec) >= 5)
    catch_error(filespec[-4:] in valid_extensions or image.ndim == 2 or image.ndim == 3)
    height, width = image.shape[:2]
    if image.ndim == 3:
        numch = 3
    else:
        numch = 1
    if maxval > 255:
        image = image.byteswap()
    if (p == "P5"):
        numch = 1
    with open(filespec, "wb") as f:
        typestr = "P6" if numch == 3 else "P5"
        f.write(("%s %d %d %d\n"%(typestr, width, height, maxval)).encode("utf-8"))
        f.write(image)