from os import listdir
from os.path import isfile, join
from PIL import Image

output_size = 512,512

def make_square(im, size=512, fill_color=(0, 0, 0)):
    x, y = im.size
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im)
    return new_im


input_folder = '/Users/annepope/ai-art/brush-paintings/brush-paintings-resized'


def is_image(f):
    return '.jpg' in f or '.jpeg' in f

input_files = [f for f in listdir(input_folder) if is_image(f)]

for idx, image_path in enumerate(input_files):
    try:
        img = Image.open(join(input_folder, image_path))
        assert img.mode == "RGB"
        assert img.size == (512, 512)
    except AssertionError as e:
        print(image_path, img.size)
    # try:
    #     img = Image.open(join(input_folder, image_path))
    #     img.thumbnail(output_size)
    #     new_img = make_square(img)
    #     new_img.save(join(output_folder, str(idx)) + ".jpg")
    # except Exception as e:
    #     print(e, image_path)