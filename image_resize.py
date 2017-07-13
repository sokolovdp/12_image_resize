import argparse
import sys
import os
from collections import namedtuple
from PIL import Image

picture_size = namedtuple('size', ['width', 'height'])


def check_size_format(size: "str") -> "tuple":
    try:
        width, height = tuple(map(int, size.lower().split('x')))
    except (ValueError, IndexError):
        raise argparse.ArgumentTypeError("invalid value {}, should be like this: 200x300".format(size))
    else:
        if width <= 0 or height <= 0:
            raise argparse.ArgumentTypeError("invalid value {}, should be like this: 200x300".format(size))
        else:
            return picture_size(width, height)


def check_image_file(image_file: "str") -> "str":
    try:
        picture = Image.open(image_file)
    except OSError:
        raise argparse.ArgumentTypeError("{} wrong path to file or invalid image format".format(image_file))
    else:
        if picture.format not in ['JPEG', 'PNG']:
            raise argparse.ArgumentTypeError("{} image must be JPEG or PNG format".format(image_file))
        else:
            picture.close()
            return image_file


def resize_image(old_image: "class 'PIL.JpegImagePlugin.JpegImageFile'", width: "int", height: "int", size: "tuple",
                 scale: "float") -> "tuple":
    old_width, old_height = old_image.size
    aspect_ratio = round(old_width / old_height, 2)
    if scale:
        new_width = int(old_width * scale)
        new_height = int(old_height * scale)
    elif width:
        new_width = width
        new_height = int(new_width / aspect_ratio)
    elif height:
        new_height = height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width, new_height = size
    new_size = picture_size(new_width, new_height)
    return old_image.resize(new_size, Image.ANTIALIAS), new_size


def main(image_file_name: "str", new_path: "str", width: "int", height: "int", size: "tuple", scale: "float"):
    with Image.open(image_file_name) as old_image:
        new_image, new_size = resize_image(old_image, width, height, size, scale)
        new_file_ext = old_image.format.lower()
    if not new_path:
        new_path, _ = os.path.split(image_file_name)
        if not new_path:
            new_path = os.getcwd()
    _, image_file_name = os.path.split(image_file_name)
    new_image_file_name = "{}_{}x{}.{}".format(image_file_name.split('.')[0], new_size.width, new_size.height,
                                               new_file_ext)
    new_image_file_full_path = os.path.join(new_path, new_image_file_name)
    new_image.save(new_image_file_full_path)
    print("re-sized imaged saved to {}".format(new_image_file_full_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='resize .jpg and .png images')
    parser.add_argument("image_file", type=check_image_file, help="path to .jpg or .png image file")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--width", dest="width", action="store", type=int, help="width of re-sized picture")
    group.add_argument("--height", dest="height", action="store", type=int, help="height of re-sized picture")
    group.add_argument("--new_size", dest="new_size", action="store", type=check_size_format,
                       help="new aspect, format: 200x300")
    group.add_argument("--scale", dest="scale", action="store", type=float, help="scale of picture resizing")
    parser.add_argument("--output", dest="out_path", action="store", help="folder where to put re-sized picture")
    args = parser.parse_args(sys.argv[1:])
    if args.out_path and not os.path.isdir(args.out_path):
        print("{} is not a valid output path".format(args.out_path))
    else:
        main(args.image_file, args.out_path, args.width, args.height, args.new_size, args.scale)
