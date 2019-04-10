from PIL import Image
import argparse
import os.path as path

def main():
    parser = argparse.ArgumentParser(
        description='Combine "sub-images" back into full image')
    parser.add_argument(
        'filename',
        help='filename of the combined output image'
    )
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

    sub_im = Image.open('{}_0_0{}'.format(filename, extension))
    sub_width, sub_height = sub_im.size
    mode = sub_im.mode

    width, height = sub_width * args.cols, sub_height * args.rows

    im = Image.new(mode, (width, height))

    for r in range(args.rows):
        upper = (r / args.rows) * height
        # lower = ((r + 1) / args.rows) * height
        for c in range(args.cols):
            left = (c / args.cols) * width
            # right = ((c + 1) / args.cols) * width
            if r != 0 or c != 0:
                sub_im = Image.open(
                    '{}_{}_{}{}'.format(filename, r, c, extension))
            im.paste(sub_im, (int(left), int(upper)))

    im.save(args.filename)

if __name__ == '__main__':
    main()
