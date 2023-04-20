#Calculate field of view dimensions at 50 m altitude

import math

takeoff_alt = 50 #Altitude of 50 m for the drone

#Camera resolution 
render_width = 1920 
render_height = 1080 
aspect = render_width/render_height

#Horizontal Field of View
HFOV_degrees = 78 #FOV given by Logitech in degrees
HFOV_radians = math.radians(78) #Horizontal FOV in radians (converted to degrees later)

#Vertical Field of View - calculation for aspect ratio greater than 1
VFOV = math.degrees(2 * math.atan((0.5 * render_height) / (0.5 * render_width / math.tan(HFOV_radians / 2))))
# print("HFOV:", HFOV_degrees, "degrees")
# print("VFOV:", VFOV, "degrees")

#Calculate length and width of field
field_width = 2*takeoff_alt*math.tan(HFOV_radians/2) #Trig to find half of camera view, then multiply by 2 to get full view  
print("Field Width:", field_width, "m")

field_height = field_width*1/aspect #Multiply field width by aspect ratio to get field height
print("Field Height:", field_height, "m")
