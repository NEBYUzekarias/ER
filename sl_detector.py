

# import the necessary packages

import argparse
import datetime
import imutils
import time
import cv2

# construct the argument parser and parse the arguments
# 
ap = argparse.ArgumentParser()
#if there is no external video we can remove the next one line of code 
#ap.add_argument("-v", "--video", help="videos/example_01.mp4") 
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam

camera = cv2.VideoCapture(0)
time.sleep(0.25)
# the following if else also can be removed

#if args.get("video", None) is None:
#	camera = cv2.VideoCapture(0)
#	time.sleep(0.25)

# otherwise, we are reading from a video file
##	camera = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
# this frame also has to update it's value in afixed time of range
firstFrame = None 
numOfFrame = 100
count = numOfFrame

# loop over the frames of the video
# insted of using while loop we can try to do with interupet




#think other way of implementing while loop 
#how can i change this to interrupt 
while True:

	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "no motion"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	# of the 
	if not grabbed:
		break
	
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it


	#this is the main thing i have to focues 
	if firstFrame is None :
		firstFrame = gray

		continue


	# compute the absolute difference between the current frame and
	# first frame
	#this is the place for comparision
	frameDelta = cv2.absdiff(firstFrame, gray)
	cv2.imshow("firstFrame", frameDelta)

	# the second argument must to lerate the value we need
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text 

		(x, y, w, h) = cv2.boundingRect(c)
		print str(w) + "the value of w"
		print str(h) + "the value of h"
		if w > 100 and h > 100 :
		
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			text = "Occupied"
	count = count - 1
	
	if count == 0 :
		firstFrame = gray 
		count = numOfFrame
	# draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
	
	#if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()