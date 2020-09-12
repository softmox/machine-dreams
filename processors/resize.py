"""
Resize images.

You must include one command line argument:
- `imagedir`: what directory of images (in the data folder) you want to resize.

And may include two others:
- `width`: width of the resulting photo
- `height`: height of the resulting photo

TODO:
- make output director an argument so it's clearer that you have to create it
"""

import argparse
import glob
from os.path import join
from PIL import Image

IMAGE_DIR_PATH = "./data/{dirname}/"

def main(args):
    """
    Iterate through image directory, resize, and save.
    """

    if not args.image_dir:
        print("Please specify a directory (in data dir) to store the images.")
        return 1

    image_dir_path = IMAGE_DIR_PATH.format(dirname=args.image_dir)
    out_dir_name = "{dir}_processed".format(dir=args.image_dir)
    out_dir_path = IMAGE_DIR_PATH.format(dirname=out_dir_name)

    jpg_files = glob.glob(join(image_dir_path, "*jpg"))
    for f in jpg_files:
        img = Image.open(f)
        img = img.resize((args.img_width, args.img_height))
        out_f_path = f.replace(image_dir_path, out_dir_path)
        img.save(out_f_path)

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--imagedir",
        dest="image_dir",
        type=str,
        default=None,
        help="specify a directory name to pull images from."
    )
    parser.add_argument(
        "--width",
        dest="img_width",
        type=int,
        default=300,
        help="output image width in pixels."
    )
    parser.add_argument(
        "--height",
        dest="img_height",
        type=int,
        default=300,
        help="output image height in pixels."
    )
    args = parser.parse_args()
    main(args)
