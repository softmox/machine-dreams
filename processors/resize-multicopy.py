"""
Resize images to max dimension and then keep slicing squares out.
Trying this for sunset dataset
"""

import argparse
from math import ceil, floor
from os.path import join
from os import listdir
from PIL import Image

IM_DIM = 512

def resize_to_dim(img):
    x, y = img.size
    if x == y:
        # already a square image
        out_x = IM_DIM
        out_y = IM_DIM
    elif x > y:
        # use y as the IM_DIM
        # so x will be bigger than IM_DIM
        scalar = IM_DIM / y
        out_x = ceil(x * scalar)
        out_y = IM_DIM
    elif x < y:
        # use x as the IM_DIM
        # so y will be bigger than IM_DIM
        scalar = IM_DIM / x
        out_x = IM_DIM
        out_y = ceil(y * scalar)
    img = img.resize((out_x, out_y))
    return img

def multislice_squares(img):
    x, y = img.size
    images = list()
    img_offset = min(x, y) / 10

    # conditions under which we only return one image
    # because the original is square enough that it doesn't make sense
    # to generate multiple

    if x == y:
        images.append(img)

    elif abs(x - y) < floor(img_offset):
        images.append(img)

    # conditions under which we return multiple images
    # by taking multiple square slices of the original image
    
    elif x > y:
        count_crops = floor((x - y) / (img_offset))
        for i in range(0, count_crops):
            upper = 0
            lower = y
            left = i * floor(img_offset)
            right = y + left
            box = (left, upper, right, lower)
            images.append(img.crop(box=box))
    elif x < y:
        count_crops = floor((y - x) / (img_offset))
        for i in range(0, count_crops):
            upper = i * floor(img_offset)
            lower = x + upper
            left = 0
            right = x
            box = (left, upper, right, lower)
            images.append(img.crop(box=box))
    return images

def main(args):
    ###################################
    # check args and set up variables
    ###################################

    if not args.in_dir:
        print("Please specify a directory (in data dir) to pull the images.")
        return 1

    if not args.out_dir:
        print("Please specify a directory (out data dir) to store the images.")
        return 1

    ###################################
    # grab images and process
    ###################################

    def is_image(f):
        return '.jpg' in f or '.jpeg' in f or '.png' in f

    input_files = [join(args.in_dir, f) for f in listdir(args.in_dir) if is_image(f)]

    print(len(input_files))
    for i, f in enumerate(input_files):
        # open image
        img = Image.open(f)

        # do processing steps
        img = resize_to_dim(img)
        img = img.convert("RGB")
        imgs = multislice_squares(img)

        # save results

        for idx, image in enumerate(imgs):
            out_f_path = join(args.out_dir, "{}-{}.jpg".format(i, idx))
            image.save(out_f_path, "JPEG")


############################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--indir",
        dest="in_dir",
        type=str,
        default=None,
        help="specify a directory path to pull images from."
    )

    parser.add_argument(
        "--outdir",
        dest="out_dir",
        type=str,
        default=None,
        help="specify a directory path to dump images to"
    )

    args = parser.parse_args()
    main(args)