import imageio
import json
import numpy as np
import pandas as pd


def points_from_batch(batch_csv):
    heatmap_df = pd.read_csv(batch_csv)
    clicks = sorted(
        (
            click
            for response in heatmap_df['Answer.response']
            for click in json.loads(response)
        ),
        key=lambda click: click['timestamp'],
    )
    return [(round(click['x']), round(click['y'])) for click in clicks]


def frames_from_points(points, width, height, points_per_frame):
    frames = []
    point_count = 0
    img_data = np.zeros((height, width), dtype=np.uint8)

    for x, y in points:
        if point_count % points_per_frame == 0:
            frames.append(np.copy(img_data))
        img_data[y:y + 2, x:x + 2] = 0xff  # white
        point_count += 1

    frames.append(img_data)

    return frames


def main():
    # points = points_from_batch('heatmap_workers.csv')
    points = points_from_batch('heatmap_peers.csv')
    frames = frames_from_points(
        points, width=600, height=477, points_per_frame=20)

    imageio.mimsave('heatmap.gif', frames)
    imageio.imwrite('heatmap_static.png', frames[-1])

    print('successfully wrote image to file')


if __name__ == '__main__':
    main()
