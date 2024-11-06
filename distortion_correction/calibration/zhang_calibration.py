import cv2
import numpy as np

def calibrate_camera(images, chessboard_size=(9, 6)):
    """
    Performs camera calibration using multiple images of a chessboard pattern.

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

    for i, img in enumerate(images):
        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Try to find the chessboard corners
        ret, corners = cv2.findChessboardCorners(
            gray,
            chessboard_size,
            flags=cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE
        )

        if ret:
            # Refine corner detection for better accuracy
            corners_refined = cv2.cornerSubPix(
                gray,
                corners,
                (11, 11),
                (-1, -1),
                (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)
            )
            imgpoints.append(corners_refined)
            objpoints.append(objp)
        else:
            print(f"Warning: No checkerboard found in image {i + 1}. Please ensure the pattern is visible.")

    if len(objpoints) == 0 or len(imgpoints) == 0:
        raise ValueError("No valid chessboard patterns were detected in any of the images.")

    # Calibrate the camera
    ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    if not ret:
        raise ValueError("Camera calibration failed.")

    return {'camera_matrix': camera_matrix, 'dist_coeffs': dist_coeffs}

# Example usage:
# images = [cv2.imread(file_path) for file_path in list_of_image_paths]
# calibration_data = calibrate_camera(images)
# print("Camera Matrix:\n", calibration_data['camera_matrix'])
# print("Distortion Coefficients:\n", calibration_data['dist_coeffs'])
