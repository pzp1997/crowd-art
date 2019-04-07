from PIL import Image
import argparse
import os.path as path

def main():
    parser = argparse.ArgumentParser(
        description='Divide an image into equally sized "sub-images"')
    parser.add_argument('filename', help='image file to divide')
    parser.add_argument(
        '--rows', '-r',
        type=int, default=2,
        help='number of vertical divisions'
    )
    parser.add_argument(
        '--cols', '-c',
        type=int, default=3,
        help='number of horizontal divisions'
    )
    args = parser.parse_args()

    filename, extension = path.splitext(args.filename)

    im = Image.open(args.filename)
    width, height = im.size

    for r in range(args.rows):
        upper = (r / args.rows) * height
        lower = ((r + 1) / args.rows) * height
        for c in range(args.cols):
            left = (c / args.cols) * width
            right = ((c + 1) / args.cols) * width
            sub_im = im.crop((left, upper, right, lower))
            sub_im.save('{}_{}_{}.{}'.format(filename, r, c, extension))

if __name__ == '__main__':
    main()
