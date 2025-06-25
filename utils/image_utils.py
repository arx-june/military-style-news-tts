import cv2
import numpy as np

def process_image_array(filepath):
    original = cv2.imread(filepath)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    binarized = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    denoised = cv2.medianBlur(binarized, 3)
    return denoised
