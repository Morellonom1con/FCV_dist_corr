import cv2
import numpy as np

def calibrate_camera(images, chessboard_size=(9, 6)):
    """
    Performs camera calibration using multiple images of a chessboard pattern with color segmentation.

    Args:
        images (list): List of images loaded using OpenCV.
        chessboard_size (tuple): Inner corners per chessboard dimension (width, height).

    Returns:
        dict: A dictionary containing the camera matrix and distortion coefficients.
    """
    # Prepare object points for a chessboard pattern
    objp = np.zeros((chessboard_size[1] * chessboard_size[0], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points
    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane

    # Define HSV range for color segmentation
    lower_hsv = np.array([0, 0, 143])
    upper_hsv = np.array([179, 61, 252])

    for i, img in enumerate(images):
        # Convert image to HSV color space for color segmentation
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

        # Apply morphological operations to clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 30))
        dilated_mask = cv2.dilate(mask, kernel, iterations=5)
        processed_img = 255 - cv2.bitwise_and(dilated_mask, mask)

        # Convert the processed image to grayscale
        processed_img = np.uint8(processed_img)

        # Try to find the chessboard corners
        ret, corners = cv2.findChessboardCorners(
            processed_img,
            chessboard_size,
            flags=cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
        )

        if ret:
            objpoints.append(objp)
            corners_refined = cv2.cornerSubPix(
                cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                corners,
                (11, 11),
                (-1, -1),
                (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)
            )
            imgpoints.append(corners_refined)
        else:
            print(f"Warning: No checkerboard found in image {i + 1}. Please ensure the pattern is visible.")

    if len(objpoints) == 0 or len(imgpoints) == 0:
        raise ValueError("No valid chessboard patterns were detected in any of the images.")

    # Calibrate the camera
    ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1::-1], None, None)
    if not ret:
        raise ValueError("Camera calibration failed.")

    return {'camera_matrix': camera_matrix, 'dist_coeffs': dist_coeffs}
