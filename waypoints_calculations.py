#Calculate coords
#Taking 9 pictures of 80.978403x45.550352 (w*l)

#Size of the rectangles that we will be taking pictures of 
rect_width = 80.978403
rect_height = 45.550352

#General latitude/longitude to m conversions
latitude = 111000 #1 degree of latitude = 111 km
longitude = 87870 #1 degree of longitude = 87.87 km 

#Top right hand corner of box
start = [35.726688, -78.694846]  

start[0] = start[0] - (rect_height/2)/latitude
#take picture

for y in range (3):
    print(start)
    #take picture
    for x in range(2):
        start[0] = start[0] - (rect_height)/latitude
        print(start)
        #take picture
    start[0] = start[0] + (rect_height*2)/latitude
    start[1] = start[1] + rect_width/longitude