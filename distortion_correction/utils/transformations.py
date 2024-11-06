import cv2
import numpy as np

def resize_image(image, width=None, height=None):
    """
    Resize an image to the specified width or height while maintaining aspect ratio.
    Args:
        image (numpy.ndarray): Input image.
        width (int): Desired width (optional).
        height (int): Desired height (optional).
    Returns:
        numpy.ndarray: Resized image.
    """
    h, w = image.shape[:2]
    
    if width is None and height is None:
        return image
    
    if width is None:
        ratio = height / float(h)
        width = int(w * ratio)
    else:
        ratio = width / float(w)
        height = int(h * ratio)
    
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
