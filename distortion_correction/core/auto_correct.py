import cv2
import numpy as np

def undistort_image(image, camera_matrix, dist_coeffs):
    """
    Corrects the distortion in a single image using the provided camera matrix and distortion coefficients.

    Args:
        image (np.array): Input distorted image.
        camera_matrix (np.array): Camera matrix from calibration.
        dist_coeffs (np.array): Distortion coefficients from calibration.

    Returns:
        np.array: The corrected image.
    """
    # Apply undistortion
    corrected_image = cv2.undistort(image, camera_matrix, dist_coeffs)
    return corrected_image

def perform_batch_correction(folder_path, calibration_data):
    """
    Corrects distortion in all images in the given folder using the provided calibration data.

    Args:
        folder_path (str): Path to the folder containing images to process.
        calibration_data (dict): Calibration data including camera matrix and distortion coefficients.
    """
    camera_matrix = calibration_data.get('camera_matrix')
    dist_coeffs = calibration_data.get('dist_coeffs')
    
    if camera_matrix is None or dist_coeffs is None:
        print("Invalid calibration data.")
        return

    # Process all images in the specified folder
    import os  # Inline import to comply with your restrictions
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            image_path = os.path.join(folder_path, file_name)
            img = cv2.imread(image_path)
            if img is not None:
                corrected_img = undistort_image(img, camera_matrix, dist_coeffs)
                # Save the corrected image with a prefix
                save_path = os.path.join(folder_path, "corrected_" + file_name)
                cv2.imwrite(save_path, corrected_img)
                print(f"Saved corrected image to {save_path}")
