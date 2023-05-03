"""
    ECE 592 - Autonomous Bomber
    Matt Parker

    Note that this is an updated version of the previous team's "detection.py" code. This code will take an input picture rather than a video
    then provide the GPS coordinates for where the target is
"""

from header import *
import numpy as np
from tarpdetector import *
from newgcs import *
from copter import *

#Standard Dimensions (Taken from Previous Group)
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# Get the current image to be processed (640x480p)
def Check_Picture_Find_Coords(image, altitude:int, coords:tuple, count):
    ''' 
        The purpose of this funciton is to take a picture as an input, identify the blue tarp, 
        output the gps coords of the center of the tarp

        image - str Filepath to an image
        altitude - int height in meters
        coords - tuple coordinates where drone is at time of picture (lon, lat)
        count - how to save the mask with a unique num
    '''
    # Define the lower and upper boundaries for blue color in BGR format
    lower_blue = np.array([0, 80, 0])
    upper_blue = np.array([255, 250, 45])
    img = cv2.imread(image)
    center = detect_blue_cluster(img, lower_blue, upper_blue, count)

    if center is not None:
        print(f"The center of the blue cluster is at pixel coordinates: {center}")
        Target_Coords = get_lat_long_of_target(center, coords, altitude)
        return Target_Coords
    else:
        print("No blue cluster detected.")
        return None
    
    

