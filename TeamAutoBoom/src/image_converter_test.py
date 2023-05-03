import cv2

# Load an RGB image
img = cv2.imread('test_0.jpg')

# Convert the RGB image to HSV
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Display the original and HSV images side by side
cv2.imshow('Original', img)
cv2.imshow('HSV', hsv_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
