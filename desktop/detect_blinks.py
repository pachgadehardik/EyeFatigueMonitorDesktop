
# python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat
import wx
from tkinter import messagebox
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time	
import datetime
import timeit
import dlib
# from dlib import fhog_object_detector
# from dlib import shape_predictor
import cv2
import winsound
frequency = 2500
duration = 2000 

app =wx.App()
list_a=[] #for storing the session wise blinks
list_b=[] #for storing the session numbers
# def countdown_timer(x):
# 	while x>=0:
# 		x-=1
# 		print("{} remaining".format(str(datetime.timedelta(seconds=x))))
# 		print("\n")
# 		time.sleep(1)
		
# def timer():
# 	now = time.localtime(time.time())
# 	return now[5]
# run = True


def eye_aspect_ratio(eye):
	
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	
	C = dist.euclidean(eye[0], eye[3])

	#eye aspect ratio
	ear = (A + B)/(2.0 * C)

	
	return ear

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")

args = vars(ap.parse_args())
 

# EYE_AR_THRESH = 0.3
EYE_AR_THRESH = 0.24
EYE_AR_CONSEC_FRAMES =4 

# initialize the frame counters and the total number of blinks
COUNTER = 0
TOTAL = 0
count_of_sessions = 0
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("loading facial landmark predictor...")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("Starting video...")

vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
fileStream = False
time.sleep(1.0)
# now = time.time()
# future = now+10
# print("Now",now)
# print("Future",future)
# loop over frames from the video stream
while (True) :
	
	
	# minutes = 0
	
	
	
	# print("Timer Started")
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)
	
	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		
		shape = face_utils.shape_to_np(shape)

		
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)

		
		ear = (leftEAR + rightEAR) / 2.0

		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		
		if ear < EYE_AR_THRESH:
			COUNTER += 1
			
		
		else:
			
		
			if COUNTER >= EYE_AR_CONSEC_FRAMES:

				TOTAL += 1
				start = 0
				if TOTAL == 1:
					now = time.time()
					future = now+10
					print("Now",now)
					print("Future",future)
				print("BLINK COUNT: ",TOTAL)
				# print("Counter: ",COUNTER)
				if(time.time() >= future):
					print("Current time is :",time.time())
					if(TOTAL<=20):

						list_a.append(TOTAL)
						winsound.Beep(frequency,duration)
						cv2.putText(frame,"ALERT!!", (200,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
						wx.MessageBox('Close your eyes!!', 'Warning', wx.OK | wx.ICON_WARNING)
						TOTAL = 0
						now = time.time()
						future = now+10
						count_of_sessions += 1
						list_b.append(count_of_sessions)
					# messagebox.showinfo("Title", "a Tk MessageBox")
				# print("Blinks are: ",TOTAL)
				
				print("List of blinks: ",list_a)
				print("List of Sessions: ",list_b)



				
				
			
			COUNTER = 0

		# draw the total number of blinks on the frame along with
		# the computed eye aspect ratio for the frame
		cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
	# show the frame
	# 
	# cv2.resizeWindow("Frame", 50, 50)
	#cv2.imshow("Frame", frame)
	# cv2.imshow("Gray",gray)
	key = cv2.waitKey(1) & 0xFF
	
	# plt.plot(list_a,list_b)
	# # plt.scatter(list_a,list_b,color='darkgreen',marker='^')
	# plt.show()
	if key == ord("q"):
		break
cv2.destroyAllWindows()
vs.stop()
# print(list_a)
# print(list_b)
plt.plot(list_b,list_a, color='green', linestyle='dashed', linewidth = 3, 
         marker='o', markerfacecolor='blue', markersize=12)
plt.show()
