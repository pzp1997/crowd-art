import pandas as pd
import json
import numpy as np
import imageio

heatmap_df = pd.read_csv('heatmap_peers.csv')

points = []
for response in heatmap_df['Answer.response']:
    response = json.loads(response)
    for click in response:
        points.append((round(click['x']), round(click['y'])))

img_data = np.zeros((600, 477))
for x, y in points:
    img_data[x, y] = 1

img_data = np.transpose(img_data)

print('writing image to file')
imageio.imwrite('heatmap_static.png', img_data)
print('successfully wrote image to file')


# print('imageio is installed')


# imageio.imwrite
# imageio.get_writer(uri, format=None, mode='?', **kwargs)

# import os
# import imageio
#
# png_dir = '../saves/png/'
# images = []
#
# imageio.mimsave('heatmap.gif', images)
