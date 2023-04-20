#Calculate coords
#Taking 9 pictures (3x3 box) of 80.978403x45.550352 (WxL)

#Size of the rectangles that we will be taking pictures of (in meters)
rect_width = 80.978403
rect_height = 45.550352

#General latitude/longitude to m conversions
latitude = 111000 #1 degree of latitude = 111 km
longitude = 87870 #1 degree of longitude = 87.87 km 

#Top right hand corner of box
#start = [35.726688, -78.694846]  
start = [35.726688, -78.695573] 

#Set start coordinates to be in the middle of the first box
start[0] = start[0] - (rect_height/2)/latitude 
start[1] = start[1] + (rect_width/2)/longitude

for y in range (3):
    print(start)
    #take picture code
    for x in range(2): 
        start[0] = start[0] - (rect_height)/latitude #Move down the 3 boxes in the column
        print(start)
        #take picture code
    start[0] = start[0] + (rect_height*2)/latitude #Move up 2 boxes 
    start[1] = start[1] + rect_width/longitude #Move to the left to start at the top of next column