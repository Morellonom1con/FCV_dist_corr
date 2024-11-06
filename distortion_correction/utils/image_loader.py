import cv2

def load_image(image_path):
    """
    Load an image from a file.
    Args:
        image_path (str): Path to the image file.
    Returns:
        numpy.ndarray: Loaded image.
    """
    return cv2.imread(image_path)

def save_image(image, save_path):
    """
    Save an image to a file.
    Args:
        image (numpy.ndarray): Image to be saved.
        save_path (str): File path to save the image.
    """
    cv2.imwrite(save_path, image)
