import json
import imageio
import numpy as np

RADIUS = 8
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


def color2pixel(color, opacity=0xff):
    if color == 'black':
        return (0x00, 0x00, 0x00, opacity)
    elif color == 'white':
        return (0xff, 0xff, 0xff, opacity)
    elif color == 'red':
        return (0xff, 0x00, 0x00, opacity)
    elif color == 'green':
        return (0x00, 0x80, 0x00, opacity)
    elif color == 'blue':
        return (0x00, 0x00, 0xff, opacity)
    elif color == 'purple':
        return (0x80, 0x00, 0x80, opacity)
    elif color == 'orange':
        return (0xff, 0xa5, 0x00, opacity)
    elif color == 'yellow':
        return (0xff, 0xff, 0x00, opacity)
    elif color == 'brown':
        return (0xa5, 0x2a, 0x2a, opacity)
    else:
        print('unkown color:', color)
        return (np.nan, np.nan, np.nan, np.nan)


def points_to_frame(points):
    img_data = np.full((410, 600, 4), color2pixel('white'), dtype=np.uint8)
    for c, r, color, timestamp in points:
        circle(img_data, 10 * c, 10 * r, RADIUS, color2pixel(color))
    return img_data


def normalize_timestamps(points):
    print('normalize_timestamps')
    min_timestamp = min(timestamp for _, _, _, timestamp in points)
    max_timestamp = max(timestamp for _, _, _, timestamp in points)
    print(min_timestamp, max_timestamp)

    print(len([1 for _, _, _, timestamp in points if timestamp is None]))

    return [
        (c, r, color, (timestamp - min_timestamp) / (max_timestamp - min_timestamp))
        for c, r, color, timestamp in points
    ]


def main():
    instances = points_from_batch('pointillism-peers.json')
    for i, instance in enumerate(instances):
        frame = points_to_frame(instance)
        imageio.imwrite('pointillism_{}.png'.format(i), frame)

    combined = [point for instance in instances for point in instance]
    # combined = normalize_timestamps(combined)

    frame = points_to_frame(combined)
    imageio.imwrite('pointillism_combined.png', frame)

    print('successfully wrote images to file')


if __name__ == '__main__':
    main()
