"""
This code contains functions used to manipulate images in OpenCV 
"""
import cv2
import numpy as np


from PIL import Image


def image_as_nparray(image):
    """
    Converts PIL's Image to numpy's array.
    image: PIL's Image object.
    """
    return np.asarray(image) # returns Numpy's array of the image


def nparray_as_image(nparray, mode='RGB'):
    """
    Converts numpy's array of image to PIL's Image.
    nparray: Numpy's array of image.
    mode: mode of the conversion.
    """
    return Image.fromarray(np.asarray(np.clip(nparray, 0, 255), dtype='uint8'), mode) # returns PIL's Image containing the image.


def load_image(source_path):
    """
    Loads RGB image and converts it to grayscale.
    source_path: image's source path.
    """
    source_image = cv2.imread(source_path)
    return cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY) # returns image loaded from the path and converted to grayscale.


def draw_with_alpha(source_image, image_to_draw, coordinates):
    """
    Draws a partially transparent image over another image.
    source_image: Image to draw over.
    image_to_draw: Image to draw.
    coordinates: coordinates to draw an image at. Tuple of x, y, width and height.
    """
    x, y, w, h = coordinates
    image_to_draw = image_to_draw.resize((h, w), Image.ANTIALIAS)
    image_array = image_as_nparray(image_to_draw)
    for c in range(0, 3):
        source_image[y:y + h, x:x + w, c] = image_array[:, :, c] * (image_array[:, :, 3] / 255.0) \
                                            + source_image[y:y + h, x:x + w, c] * (1.0 - image_array[:, :, 3] / 255.0)
