# import the necessary packages
import numpy as np
import argparse
import cv2
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(args["image"])
height, width, _ = image.shape
radiusUpperBound = min(height, width)/2
radiusLowerBound = 0
output = image.copy()
cv2.imshow("original_image",image)
image = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
cv2.imshow("denoised.jpg",image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray_image.jpg", gray)
# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.3, 100)

# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
 
	# loop over the (x, y) coordinates and radius of the circles
	maxAreaCircle = None
	maxRadius = 0
	for (x, y, r) in circles:
		print("Diameter = %d" %(2*r))	
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
		cv2.putText(output, "Diameter = %d" %(2*r),
		(int(x-100), int(y-40)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 255, 0), 2)
		# show the output image
		cv2.imshow("output",output)
		cv2.imwrite("output.jpg",output)
		cv2.waitKey(0)

