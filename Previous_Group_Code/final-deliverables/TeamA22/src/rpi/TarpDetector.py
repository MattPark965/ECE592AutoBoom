# -*- coding: utf-8 -*-
"""TarpDetector.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cuvZuzoVHKZSe-SauL9NXJvo23-6sQVB
"""

import cv2  # Import OpenCV for image processing
import numpy as np # Import NumPy for np array processing

# The below is a function that returns the center of a cluster of blue pixels
# If there is no blue in the image then it returns None

def detect_blue_cluster(img, lower_blue, upper_blue):  # NOTE: The color ranges are in HSV
    #img Must be read in as cv2.imread(image_path) before this function is called

    # Convert the image from BGR to HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create a binary mask using the specified blue color range
    mask = cv2.inRange(hsv_img, lower_blue, upper_blue)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to store blue cluster center and max contour area
    blue_cluster_center = None
    max_area = 0

    for contour in contours: # Iterate through every contour found
        area = cv2.contourArea(contour) # Calculate the area of the first contour
        if area > max_area: # Checks if the area is max area found so far if so the below executes
            max_area = area # Updates max area of contour
            M = cv2.moments(contour) # Moments returns the 
            if M["m00"] != 0: # If the area of the contour is not zero
                cX = int(M["m10"] / M["m00"]) # Calculate the center of the shape in X coordinates
                cY = int(M["m01"] / M["m00"]) # Calculate the center of the shape in Y coordinates
                blue_cluster_center = (cX, cY) # returns tuple of x and y pixel coordinates

    return blue_cluster_center