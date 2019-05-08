import pandas as pd
import json
import numpy as np
import imageio
from collections import defaultdict
import os


def points_from_batch(batch_csv):
    mosaic_df = pd.read_csv(batch_csv)
    segments = defaultdict(list)

    # each segment has list of responses
    # each response has list of lines (might be undone)
    # each line has data field with list of points

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
                points.append((round(point['x']), round(
                    point['y']), point['timestamp']))

        segments[segment].append(points)

    return segments


def frames_from_points(points, width, height):
    # if len(points) > 0:
    #     xs, ys, _ = zip(*points)
    #     print(img_filename)
    #     print('min width:', min(xs), 'max width:', max(xs), 'min height:', min(ys), 'max height:', max(ys))

    img_data = np.zeros((height, width), dtype=np.uint8)
    for x, y, _ in points:
        img_data[y:y + 2, x:x + 2] = 0xff  # white
    return img_data


def main():
    segments = points_from_batch('mosaic_workers.csv')
    # segments = points_from_batch('mosaic_peers.csv')

    for segment, responses in segments.items():
        # if any(x in segment for x in ['0_2', '0_3', '2_0']):
        #     points = []
        # else:
        points = [point for response in responses for point in response]
        points.sort(key=lambda x: x[2])

        frame = frames_from_points(
            points,
            604,
            481,
        )

        imageio.imwrite(os.path.join('mosaic_segments', segment), frame)

    print('successfully wrote images to file')


if __name__ == '__main__':
    main()
