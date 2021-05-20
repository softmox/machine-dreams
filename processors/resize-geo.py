"""
Code to resize images for geometric-forms dataset
"""

import argparse
from math import ceil
from os.path import join
from os import listdir
from PIL import Image


def is_square(img):
    return img.size[0] == img.size[1]

def square_by_tile(img):
    w = img.size[0]
    h = img.size[1]
    square_size = max(w, h)
    new_img = Image.new('RGB', (square_size, square_size), (0,0,0))

    if w > h:
        iterations = ceil(w / h)
        for i in range(0, iterations):
            new_img.paste(img, (0, i * h))
            img = img.transpose(method=Image.FLIP_TOP_BOTTOM)

    else:
        iterations = ceil(h / w)
        for i in range(0, iterations):
            new_img.paste(img, (i * w, 0))
            img = img.transpose(method=Image.FLIP_LEFT_RIGHT)

    return new_img

def square_by_crop(img):
    square_size = min(img.size[0], img.size[1])
    return img.crop(box=(0, 0, square_size, square_size))

def aspect_ratio(img):
    return img.size[0] / img.size[1]


def reshape_to_square(img):
    if is_square(img):
        # no need to adjust shape
        return img
    elif aspect_ratio(img) >= 0.75 and aspect_ratio(img) <= 1/0.75:
        # if picture is nearly square, just crop it
        return square_by_crop(img)
    else:
        # picture is not close to square, so tile it
        return square_by_tile(img)



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
    for f in input_files:
        # open image
        img = Image.open(f)

        # do processing steps
        img = reshape_to_square(img)
        img = img.resize((512, 512))
        img = img.convert("RGB")

        # save result
        out_f_path = f.replace(args.in_dir, args.out_dir).replace(".png", ".jpg")
        img.save(out_f_path, "JPEG")

        
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
