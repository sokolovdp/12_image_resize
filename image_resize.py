import argparse
import sys
import os
from PIL import Image


def resize_image(old_image_path: "str", new_size: "tuple", new_dir: "str") -> "str":
    with Image.open(old_image_path) as image:
        new_image = image.resize(new_size, Image.ANTIALIAS)
        new_file_ext = image.format.lower()
    _, file_name = os.path.split(old_image_path)
    new_file_name = "{}_{}x{}.{}".format(file_name.split('.')[0], new_width, new_height, new_file_ext)
    new_file_path = os.path.join(new_dir, new_file_name)
    new_image.save(new_file_path)
    return new_file_path


def check_wxh_format(wxh: "str") -> "tuple of ints":
    pars = wxh.lower().split('x')
    try:
        width = int(pars[0])
        height = int(pars[1])
    except (ValueError, IndexError):
        raise argparse.ArgumentTypeError("invalid value {}, should be like this: 200x300".format(wxh))
    else:
        return width, height


def check_image_file(image_file: "str") -> "str":
    try:
        with Image.open(image_file) as im:
            if im.format not in ['JPEG', 'PNG']:
                raise argparse.ArgumentTypeError("{} image must be JPEG or PNG type".format(image_file))
    except OSError:
        raise argparse.ArgumentTypeError("{} wrong path to file or invalid image format".format(image_file))
    else:
        return image_file


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='resize .jpg and .png images')
    ap.add_argument("image_file", type=check_image_file, help="path to .jpg or .png image file")
    resize = ap.add_mutually_exclusive_group(required=True)
    resize.add_argument("--width", dest="width", action="store", type=int, help="width of resized picture")
    resize.add_argument("--height", dest="height", action="store", type=int, help="height of resized picture")
    resize.add_argument("--wxh", dest="wxh", action="store", type=check_wxh_format, help="new aspect, format: 200x300")
    resize.add_argument("--scale", dest="scale", action="store", type=float, help="scale of picture resizing")
    ap.add_argument("--output", dest="out_path", action="store", help="folder where to put resized picture")
    args = ap.parse_args(sys.argv[1:])

    with Image.open(args.image_file) as old_image:
        old_width, old_height = old_image.size
        old_format = old_image.format

    aspect_ratio = round(old_width / old_height, 2)
    # set output directory path
    new_path, _ = os.path.split(args.image_file)
    if not new_path:
        new_path = os.getcwd()
    if args.out_path:
        if not os.path.isdir(args.out_path):
            print("{} is not a valid output path".format(args.out_path))
            exit()
        else:
            new_path = args.out_path
    # define new image size
    if args.scale:
        new_width = int(old_width * args.scale)
        new_height = int(old_height * args.scale)
    elif args.width:
        new_width = args.width
        new_height = int(new_width / aspect_ratio)
    elif args.height:
        new_height = args.height
        new_width = int(new_height * aspect_ratio)
    else:  # new ratio wxh
        new_width, new_height = args.wxh

    print("re-sized imaged saved to {}".format(resize_image(args.image_file, (new_width, new_height), new_path)))
