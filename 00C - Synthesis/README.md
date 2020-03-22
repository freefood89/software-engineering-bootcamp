# 00C - Synthesis

Now that you have written a program that can generate thumbnails given any filename and a program that stores a mapping from the original image to the thumbnail, it's time to put them together. The goal of this step is to combine the logic from the previous steps to create a system that, given a image filename, generates a thumbnail and stores a reference to that in a database

## Specification

- The program should not crash if an image with the provided filename does not exist.
- The program should not crash if the provided filename is for a file that is not an image
- The program should overwrite thumbnails of images that have already been processed if it's run multiple times