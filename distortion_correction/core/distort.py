import cv2
import numpy as np

def apply_distortion(image, k1=0.1, k2=0.1, p1=0.0, p2=0.0):
    """
    Apply barrel distortion to the image.
    Args:
        image (numpy.ndarray): Input image.
        k1, k2, p1, p2 (float): Distortion coefficients.
    Returns:
        numpy.ndarray: Distorted image.
    """
    h, w = image.shape[:2]
    camera_matrix = np.array([[w, 0, w / 2],
                              [0, h, h / 2],
                              [0, 0, 1]], dtype=np.float32)
    dist_coeffs = np.array([k1, k2, p1, p2], dtype=np.float32)
    distorted = cv2.undistort(image, camera_matrix, dist_coeffs)
    return distorted
