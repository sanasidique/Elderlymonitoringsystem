# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

# import the necessary packages
import smtplib
from email.mime.text import MIMEText


import re


import numpy as np
import subprocess
import time
import cv2
import os
# from src.dbconnection import *

labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream, pointer to output video file, and
# frame dimensions




vs = cv2.VideoCapture("video.mp4")
# vs = cv2.VideoCapture(0)
writer = None
(W, H) = (None, None)



# loop over frames from the video file

listop=[]
listra=[]
counti=0
aspect_list=[]
while True:

	counti=counti+1
	# read the next frame from the file

	(grabbed, frame) = vs.read()
	_, frame = vs.read()

	print("==> ",counti)
	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break

	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	# construct a blob from the input frame and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes
	# and associated probabilities
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()

	# initialize our lists of detected bounding boxes, confidences,
	# and class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []

	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability)
			# of the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > 0.5:
				# scale the bounding box coordinates back relative to
				# the size of the image, keeping in mind that YOLO
				# actually returns the center (x, y)-coordinates of
				# the bounding box followed by the boxes' width and
				# height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# use the center (x, y)-coordinates to derive the top
				# and and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates,
				# confidences, and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4,
		0.5)

	carlist=[]
	bikelist=[]
	plist=[]

	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])


			if LABELS[classIDs[i]]=="person"  :
				# draw a bounding box rectangle and label on the frame
				color = [int(c) for c in COLORS[classIDs[i]]]
				cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
				text = "{}: {:.4f}".format(LABELS[classIDs[i]],
					confidences[i])
				print(LABELS[classIDs[i]])
				plist.append([(x, y), (x + w, y + h)])
				if len(aspect_list)>=10:
					aspect_list=aspect_list[len(aspect_list)-9:]
				aspect_list.append(h/w)



			# iud(qry, 3)
	if len(aspect_list)>=10:
		print (aspect_list)
		dif_list=[]
		item_list=[]
		for i in range(1,len(aspect_list)):
			dif=abs(aspect_list[i-1]-aspect_list[i])
			dif_list.append(dif)
			if dif>0.15:
				item_list.append(1)
			else:
				item_list.append(0)

		print (dif_list)
		print (sum(item_list))
		print (sum(dif_list))
		if sum(item_list)>3:

			print (item_list)
			max_count = 0
			current_count = 0

			for x in item_list:
				if x == 1:
					current_count += 1
					max_count = max(max_count, current_count)
				else:
					current_count = 0

			print("max_count",max_count)
			if max_count>=3:
				cv2.imwrite("photo.jpg",frame)
				import requests

				url = "http://localhost:8000/myapp/upload/"

				data = {
					"pid": "1",
				}

				files = {
					"image": ("photo.jpg", open("photo.jpg", "rb"), "image/jpeg")
				}

				response = requests.post(url, data=data, files=files)

				print(response.status_code)
				print(response.text)

				print ("fall detected")
				aspect_list = []
		# if sum(dif_list)>1.5:
		# 	aspect_list=[]
		# 	print ("fall detected")

	cv2.imshow('video', frame)

	if cv2.waitKey(33) == 27:
		break


# release the file pointers
print("[INFO] cleaning up...")

vs.release()

# KL23111755069873 Received Rs.13542/- against new registration fee vide receipt no KL77D23110000546 dated 18-Nov-2023. Thanks PERAMBRA SRTO. MoRTH.