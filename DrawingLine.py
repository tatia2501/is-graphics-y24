import math

import numpy as np


def drawing(px, py, buffer, c1, c2, c3, visibility, thickness):
    new_pixels = buffer
    p1 = np.array([px[0], py[0]])
    p2 = np.array([px[1], py[1]])
    out = []
    p = p1
    d = p2 - p1
    N = np.max(np.abs(d))
    s = d / N
    out.append(np.rint(p))
    for i in range(0, N):
        p = p + s
        out.append(p)

    for k in range(len(out)):
        x1, y1 = int(math.floor(float(out[k][1]))), int(math.floor(float(out[k][0])))
        x2, y2 = int(math.ceil(float(out[k][1]))), int(math.ceil(float(out[k][0])))

        # x1, y1 = int(out[k][1]), int(out[k][0])
        # vis1 = visibility
        if out[k][1] - x1 > x2 - out[k][1] or out[k][0] - y1 > y2 - out[k][0]:
            temp = [x1, y1]
            x1, y1 = x2, y2
            x2, y2 = temp[0], temp[1]

        x3 = x1
        y3 = y1
        if 0 < x1 < x2:
            x2 = int(x1 + thickness / 2 - (1 - thickness % 2))
            x3 = int(x1 - thickness / 2)
        if x2 < x1 < len(buffer[0]):
            x3 = int(x1 + thickness / 2 - (1 - thickness % 2))
            x2 = int(x1 - thickness / 2)
        if 0 < y1 < y2:
            y3 = int(y1 - thickness / 2)
            y2 = int(y1 + thickness / 2 - (1 - thickness % 2))
        if y2 < y1 < len(buffer):
            y3 = int(y1 + thickness / 2 - (1 - thickness % 2))
            y2 = int(y1 - thickness / 2)


        vis1 = (abs(out[k][1] - x2) + abs(out[k][0] - y2)) * visibility
        vis2 = (abs(out[k][1] - x1) + abs(out[k][0] - y1)) * visibility
        vis3 = vis2/3

        if vis1 < 0:
            vis1 = 0
        if vis2 < 0:
            vis2 = 0
        if vis1 > 1:
            vis1 = 1
        if vis2 > 1:
            vis2 = 1
        if x1 == x2 and y1 == y2:
            vis1 = 1
            vis2 = 0

        new_pixels[x1, y1][0], \
        new_pixels[x1, y1][1], \
        new_pixels[x1, y1][2] = \
            min(c1 * vis1 + new_pixels[x1, y1][0] * (1 - vis1), 255), \
            min(c2 * vis1 + new_pixels[x1, y1][1] * (1 - vis1), 255), \
            min(c3 * vis1 + new_pixels[x1, y1][2] * (1 - vis1), 255)

        if x2 != x1 or y2 != y1:
            new_pixels[x2, y2][0], \
            new_pixels[x2, y2][1], \
            new_pixels[x2, y2][2] = \
                min(c1 * vis2 + new_pixels[x2, y2][0] * (1 - vis2), 255), \
                min(c2 * vis2 + new_pixels[x2, y2][1] * (1 - vis2), 255), \
                min(c3 * vis2 + new_pixels[x2, y2][2] * (1 - vis2), 255)

        if x1 != x3 or y1 != y3:
            new_pixels[x3, y3][0], \
            new_pixels[x3, y3][1], \
            new_pixels[x3, y3][2] = \
                min(c1 * vis3 + new_pixels[x3, y3][0] * (1 - vis3), 255), \
                min(c2 * vis3 + new_pixels[x3, y3][1] * (1 - vis3), 255), \
                min(c3 * vis3 + new_pixels[x3, y3][2] * (1 - vis3), 255)

        vis1_0 = vis1
        if x2 < x3:
            for t in range(int(x2) + 1, int(x3)):
                if (t == int(x2) + 1):
                    vis1 = (vis1_0 + vis2)/2
                elif (t == int(x3) - 1):
                    vis1 = (vis1_0 + vis3)/2
                else:
                    vis1 = vis1_0
                new_pixels[t, y1][0], \
                new_pixels[t, y1][1], \
                new_pixels[t, y1][2] = \
                    min(c1 * vis1 + new_pixels[t, y1][0] * (1 - vis1), 255), \
                    min(c2 * vis1 + new_pixels[t, y1][1] * (1 - vis1), 255), \
                    min(c3 * vis1 + new_pixels[t, y1][2] * (1 - vis1), 255)
        elif x2 > x3:
            for t in range(int(x3) + 1, int(x2)):
                if (t == int(x3) + 1):
                    vis1 = (vis1_0 + vis3) / 2
                elif (t == int(x2) - 1):
                    vis1 = (vis1_0 + vis2) / 2
                else:
                    vis1 = vis1_0
                new_pixels[t, y1][0], \
                new_pixels[t, y1][1], \
                new_pixels[t, y1][2] = \
                    min(c1 * vis1 + new_pixels[t, y1][0] * (1 - vis1), 255), \
                    min(c2 * vis1 + new_pixels[t, y1][1] * (1 - vis1), 255), \
                    min(c3 * vis1 + new_pixels[t, y1][2] * (1 - vis1), 255)

        if y2 < y3:
            for t in range(int(y2) + 1, int(y3)):
                if (t == int(y2) + 1):
                    vis1 = (vis1_0 + vis2) / 2
                elif (t == int(y3) - 1):
                    vis1 = (vis1_0 + vis3) / 2
                else:
                    vis1 = vis1_0
                new_pixels[x1, t][0], \
                new_pixels[x1, t][1], \
                new_pixels[x1, t][2] = \
                    min(c1 * vis1 + new_pixels[x1, t][0] * (1 - vis1), 255), \
                    min(c2 * vis1 + new_pixels[x1, t][1] * (1 - vis1), 255), \
                    min(c3 * vis1 + new_pixels[x1, t][2] * (1 - vis1), 255)
        elif y2 > y3:
            for t in range(int(y3) + 1, (int(y2))):
                if (t == int(y3) + 1):
                    vis1 = (vis1_0 + vis3) / 2
                elif (t == int(y2) - 1):
                    vis1 = (vis1_0 + vis2) / 2
                else:
                    vis1 = vis1_0
                new_pixels[x1, t][0], \
                new_pixels[x1, t][1], \
                new_pixels[x1, t][2] = \
                    min(c1 * vis1 + new_pixels[x1, t][0] * (1 - vis1), 255), \
                    min(c2 * vis1 + new_pixels[x1, t][1] * (1 - vis1), 255), \
                    min(c3 * vis1 + new_pixels[x1, t][2] * (1 - vis1), 255)




    return new_pixels
