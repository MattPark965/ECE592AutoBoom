import cv2

cam=cv2.VideoCapture(0)

while True:
	ret, image=cam.read()
	cv2.imshow('test',image)
	k=cv2.waitKey(1)
	if k!= -1:
		break
		
cv2.imwrite('/home/raspberrypi/test.jpg', image)
cam.release()
