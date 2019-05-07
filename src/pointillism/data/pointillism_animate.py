import json
import imageio
import numpy as np

RADIUS = 3
OPACITY = 0xa0


def points_from_batch(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)


def circle(img_data, x0, y0, radius, color):
    f = 1 - radius
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius

    img_data[y0 - radius: y0 + radius, x0] = color
    img_data[y0, x0 - radius: x0 + radius] = color

    while x < y:
        if f >= 0:
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x

        img_data[y0 + y, x0 - x: x0 + x] = color
        img_data[y0 - y, x0 - x: x0 + x] = color
        img_data[y0 + x, x0 - y: x0 + y] = color
        img_data[y0 - x, x0 - y: x0 + y] = color


def points_to_frame(points):
    color2pixel = {
        'black':  (0x00, 0x00, 0x00, OPACITY),
        'white':  (0xff, 0xff, 0xff, OPACITY),
        'red':    (0xff, 0x00, 0x00, OPACITY),
        'green':  (0x00, 0x80, 0x00, OPACITY),
        'blue':   (0x00, 0x00, 0xff, OPACITY),
        'purple': (0x80, 0x00, 0x80, OPACITY),
        'orange': (0xff, 0xa5, 0x00, OPACITY),
        'yellow': (0xff, 0xff, 0x00, OPACITY),
        'brown':  (0xa5, 0x2a, 0x2a, OPACITY),
    }

    img_data = np.full((401, 600, 4), color2pixel['white'], dtype=np.uint8)
    for c, r, color, timestamp in points:
        circle(img_data, 10 * c, 10 * r, RADIUS, color2pixel[color])
    return img_data


def main():
    instances = points_from_batch('pointillism-peers.json')
    for i, instance in enumerate(instances):
        frame = points_to_frame(instance)
        imageio.imwrite('pointillism_{}.png'.format(i), frame)

    combined = [point for instance in instances for point in instance]
    frame = points_to_frame(combined)
    imageio.imwrite('pointillism_combined.png', frame)

    print('successfully wrote images to file')


if __name__ == '__main__':
    main()
