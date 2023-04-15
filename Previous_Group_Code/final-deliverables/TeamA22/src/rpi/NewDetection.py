"""
    ECE 592 - Autonomous Bomber
    Matt Parker

    Note that this is an updated version of the previous team's "detection.py" code. This code will take an input picture rather than a video
    then provide the GPS coordinates for where the target is
"""

from header import *
import numpy as np
from TarpDetector import *

# Only looking to identify the blue tarp in a picture
lower_blue = np.array([90, 50, 50])  # Lower bound of the blue color range in HSV
upper_blue = np.array([150, 255, 255])  # Upper bound of the blue color range in HSV

#Standard Dimensions (Taken from Previous Group)
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# Get the current image to be processed (640x480p)
def Check_Picture(image):
    ''' image input should be a path to the image '''
    img = cv2.imread(image)
    center = detect_blue_cluster(img, lower_blue, upper_blue)

    if center is not None:
        print(f"The center of the blue cluster is at pixel coordinates: {center}")
    else:
        print("No blue cluster detected.")
    
    

