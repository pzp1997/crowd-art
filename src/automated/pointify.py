import imageio
import json
import numpy as np
import pandas as pd


def circle(src, dst, x0, y0, radius):
    f = 1 - radius
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius

    dst[y0 - radius: y0 + radius, x0] = src[y0 - radius: y0 + radius, x0]
    dst[y0, x0 - radius: x0 + radius] = src[y0, x0 - radius: x0 + radius]

    while x < y:
        if f >= 0:
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x

        dst[y0 + y, x0 - x: x0 + x] = src[y0 + y, x0 - x: x0 + x]
        dst[y0 - y, x0 - x: x0 + x] = src[y0 - y, x0 - x: x0 + x]
        dst[y0 + x, x0 - y: x0 + y] = src[y0 + x, x0 - y: x0 + y]
        dst[y0 - x, x0 - y: x0 + y] = src[y0 - x, x0 - y: x0 + y]


def pointify(src):
    height, width, _ = src.shape

    spacing = 15
    radius = 5

    dst = np.full(src.shape, (0xff, 0xff, 0xff), dtype=src.dtype)
    for r in range(height // spacing):
        for c in range(width // spacing):
            circle(src, dst, c * spacing, r * spacing, radius)
    return dst


def main():
    horse_img = imageio.imread('horse_orig.jpg')
    pointillism_img = pointify(horse_img)
    imageio.imwrite('pointillism_automated.png', pointillism_img)
    print('successfully wrote image to file')


if __name__ == '__main__':
    main()
