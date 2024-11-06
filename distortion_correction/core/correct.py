import cv2
import numpy as np

def correct_distortion(image, k1, k2, p1, p2):
    """
    Corrects distortion in an image using given distortion parameters.
    
    Args:
        image (numpy.ndarray): The input distorted image.
        k1 (float): Distortion coefficient K1.
        k2 (float): Distortion coefficient K2.
        p1 (float): Distortion coefficient P1.
        p2 (float): Distortion coefficient P2.
    
    Returns:
        numpy.ndarray: The corrected image.
    """
    
    # Assuming a camera matrix and distortion coefficients
    h, w = image.shape[:2]

    # Camera matrix
    camera_matrix = np.array([[w, 0, w / 2],
                               [0, w, h / 2],
                               [0, 0, 1]], dtype=np.float32)

    # Distortion coefficients
    dist_coeffs = np.array([k1, k2, p1, p2, 0], dtype=np.float32)  # Assuming no tangential distortion for simplicity

    # Use cv2.undistort to correct the image
    corrected_image = cv2.undistort(image, camera_matrix, dist_coeffs)

    return corrected_image
