# Image Resizer

```
usage: image_resize.py [-h]
                       (--width WIDTH | --height HEIGHT | --wxh WXH | --scale SCALE)
                       [--output OUT_PATH]
                       image_file

resize .jpg and .png images

positional arguments:
  image_file         path to .jpg or .png image file

optional arguments:
  -h, --help         show this help message and exit
  --width WIDTH      width of resized picture
  --height HEIGHT    height of resized picture
  --wxh WXH          new aspect, format: 200x300
  --scale SCALE      scale of picture resizing
  --output OUT_PATH  folder where to put resized picture
```



# Sample usage
```
python.exe image_resize.py test.png --wxh 500x200 --output D:\
re-sized imaged saved to D:\test_500x200.png

Process finished with exit code 0
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
