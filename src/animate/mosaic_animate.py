import pandas as pd
import json
import numpy as np
import imageio
from collections import defaultdict
import os

mosaic_df = pd.read_csv('mosaic_peers.csv')

segments = defaultdict(list)

# each segment has list of responses
# each response has list of lines (might be undone)
# each line has data field with list of points

THICK_LINES = True

undo_usage = 0

for _, row in mosaic_df.iterrows():
    segment = row['Input.image']
    response = row['Answer.response']
    response = json.loads(response)
    points = []

    for line in response:
        if line['undoTimestamp'] is not None:
            undo_usage += 1
            continue

        for point in line['data']:
            points.append((round(point['x']), round(point['y']), point['timestamp']))

    segments[segment].append(points)

def create_image_from_points(img_filename, points, width, height):
    if any(x in img_filename for x in ['0_2', '0_3', '2_0']):
        points = []
    if len(points) > 0:
        xs, ys, _ = zip(*points)
        print(img_filename)
        print('min width:', min(xs), 'max width:', max(xs), 'min height:', min(ys), 'max height:', max(ys))
    img_data = np.zeros((height, width))
    for x, y, _ in points:
        img_data[y, x] = 1
        if THICK_LINES:
            img_data[y + 1, x] = 1
            img_data[y, x + 1] = 1
            img_data[y + 1, x + 1] = 1
    imageio.imwrite(img_filename, img_data)

for segment, responses in segments.items():
    points = [point for response in responses for point in response]
    points.sorted(key=lambda x: x[2])

    create_image_from_points(
        os.path.join('mosaic_segments', segment),
        points,
        604,
        481,
    )
