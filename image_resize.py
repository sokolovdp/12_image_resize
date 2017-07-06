import argparse
import sys
import os
from PIL import Image


def check_wxh_format(wxh: "str") -> "tuple":
    pars = wxh.lower().split('x')
    try:
        width = int(pars[0])
        height = int(pars[1])
        if width <= 0 or height <= 0:
            raise argparse.ArgumentTypeError("invalid value {}, should be like this: 200x300".format(wxh))
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


def resize_image(old_image: "class 'PIL.JpegImagePlugin.JpegImageFile'", width: "int", height: "int", wxh: "tuple",
                 scale: "float") -> "tuple":
    old_width, old_height = old_image.size
    aspect_ratio = round(old_width / old_height, 2)
    if scale:  # one of these arguments must be set
        new_width = int(old_width * scale)
        new_height = int(old_height * scale)
    elif width:
        new_width = width
        new_height = int(new_width / aspect_ratio)
    elif height:
        new_height = height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width, new_height = wxh
    new_size = (new_width, new_height)
    return old_image.resize(new_size, Image.ANTIALIAS), new_size


def main(image_file_name: "str", new_path: "str", width: "int", height: "int", wxh: "tuple", scale: "float"):
    with Image.open(image_file_name) as old_image:
        new_image, new_size = resize_image(old_image, width, height, wxh, scale)
        new_file_ext = old_image.format.lower()
    if not new_path:  # use path given in the image file name
        new_path, _ = os.path.split(image_file_name)
        if not new_path:
            new_path = os.getcwd()
    _, image_file_name = os.path.split(image_file_name)
    new_image_file_name = "{}_{}x{}.{}".format(image_file_name.split('.')[0], new_size[0], new_size[1], new_file_ext)
    new_image_file_full_path = os.path.join(new_path, new_image_file_name)
    new_image.save(new_image_file_full_path)
    print("re-sized imaged saved to {}".format(new_image_file_full_path))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='resize .jpg and .png images')
    ap.add_argument("image_file", type=check_image_file, help="path to .jpg or .png image file")
    meg = ap.add_mutually_exclusive_group(required=True)
    meg.add_argument("--width", dest="width", action="store", type=int, help="width of re-sized picture")
    meg.add_argument("--height", dest="height", action="store", type=int, help="height of re-sized picture")
    meg.add_argument("--wxh", dest="wxh", action="store", type=check_wxh_format, help="new aspect, format: 200x300")
    meg.add_argument("--scale", dest="scale", action="store", type=float, help="scale of picture resizing")
    ap.add_argument("--output", dest="out_path", action="store", help="folder where to put re-sized picture")
    args = ap.parse_args(sys.argv[1:])
    if args.out_path and not os.path.isdir(args.out_path):
        print("{} is not a valid output path".format(args.out_path))
    else:
        main(args.image_file, args.out_path, args.width, args.height, args.wxh, args.scale)
