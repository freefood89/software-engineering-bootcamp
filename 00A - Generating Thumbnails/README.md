# 00A - Generating Thumbnails

Python is a powerful language in that it allows you to accomplish a lot with little code (in most use-cases). In this step you'll write an interactive program that can create thumbnail images from photos.

## Parts

The buildtin `input()` function ([docs](https://docs.python.org/3/library/functions.html#input)) will be used to tell the program which file you want to generate a thumbnail for.

The python module `pillow` ([docs](https://python-pillow.org/)) will be used to generate the thumbnails from images.

## Specification

Your project folder structure should look something like the following:

```
/project-root
  /uploads
    lolcats.jpg
  /thumbnails
    lolcats.thumbnail.jpg
  generate_thumbnail.py
```

- The program should not crash if an image with the provided filename does not exist.
- The program should not crash if the provided filename is for a file that is not an image
- The program should overwrite thumbnails of images that have already been processed if it's run multiple times

## Appendix

Starter code:

```python
from PIL import Image

def generate_thumbnail(image, filename, size=(128, 128)):
	image.thumbnail(size)
	image.save(filename, "JPEG")

im = Image.open('lolcats.jpg')
generate_thumbnail(im, 'lolcats.thumbnail.jpg')
```