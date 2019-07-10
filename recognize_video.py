# USAGE
# python recognize_video.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
import json_operations
import requests
import lock_module

def process_video(need_to_learn, detector, embedding_model, recognizer, le, expected_confidence):

	if (need_to_learn == "True"):
		os.system("python extract_embeddings.py --dataset dataset --embeddings output/embeddings.pickle --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7")
		os.system("python train_model.py --embeddings output/embeddings.pickle --recognizer output/recognizer.pickle --le output/le.pickle")

	# load our serialized face detector from disk
	print("[INFO] loading face detector...")
	protoPath = os.path.sep.join([detector, "deploy.prototxt"])
	modelPath = os.path.sep.join([detector,
		"res10_300x300_ssd_iter_140000.caffemodel"])
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

	# load our serialized face embedding model from disk
	print("[INFO] loading face recognizer...")
	embedder = cv2.dnn.readNetFromTorch(embedding_model)

	# load the actual face recognition model along with the label encoder
	recognizer = pickle.loads(open(recognizer, "rb").read())
	le = pickle.loads(open(le, "rb").read())

	# initialize the video stream, then allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

	# start the FPS throughput estimator
	fps = FPS().start()

	# loop counters
	time_counter = 0
	name_probability = {}
	dictCounter = 0
	sentCounter = 0
	repeat = 0

	# loop over frames from the video file stream
	while True:
		# grab the frame from the threaded video stream
		frame = vs.read()

		# resize the frame to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image
		# dimensions
		frame = imutils.resize(frame, width=600)
		(h, w) = frame.shape[:2]

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(frame, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		detector.setInput(imageBlob)
		detections = detector.forward()

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections
			if confidence > expected_confidence:
				# compute the (x, y)-coordinates of the bounding box for
				# the face
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# extract the face ROI
				face = frame[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]

				# ensure the face width and height are sufficiently large
				if fW < 20 or fH < 20:
					continue

				# construct a blob for the face ROI, then pass the blob
				# through our face embedding model to obtain the 128-d
				# quantification of the face
				faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
					(96, 96), (0, 0, 0), swapRB=True, crop=False)
				embedder.setInput(faceBlob)
				vec = embedder.forward()

				# perform classification to recognize the face
				preds = recognizer.predict_proba(vec)[0]
				j = np.argmax(preds)
				proba = preds[j]
				name = le.classes_[j]

				# remember names/probability
				if time_counter % 1 == 0:
					if (name in name_probability):
						name_probability[name] += proba
					else:
						name_probability[name] = proba	
					dictCounter += 1

				# sends post after a timeframe has passed
				if time_counter % 5 == 0 and repeat == 0:
					for name in name_probability:
						name_probability[name] = name_probability[name]/dictCounter

					json_operations.writeToJSONFile('people_count', name_probability)
					name_probability.clear()
					dictCounter = 0

					door = json_operations.readFromJSONFile('people_count')

					# only takes names with probability higher than [0.x]
					actualDoor = []
					for name in door:
						if (door[name] > 0.20 and name != 'unknown'):
							actualDoor.append(name)
						elif (door[name] > 0.30):
							actualDoor.append(name)

					# check if identified names are homeowners, if so unlock door
					f = open("homeowners.txt", "r")
					for line in f:
						line = line.rstrip()
						for names in actualDoor:
							if (line == names):
								lock_module.open_lock()

					# convert list to string
					stringname = ",".join(actualDoor)
					print(stringname)
					
					sentCounter = 1
					repeat = 1

				# draw the bounding box of the face along with the
				# associated probability
				text = "{}: {:.2f}%".format(name, proba * 100)
				y = startY - 10 if startY - 10 > 10 else startY + 10
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(0, 0, 255), 2)
				cv2.putText(frame, text, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

		# no one at the door
		if sentCounter == 0 and time_counter % 20 == 0:
			print('no one')
		elif sentCounter == 1 and time_counter % 20 == 0:
			sentCounter = 0

		# update the FPS counter
		fps.update()

		# counter increase
		time_counter = time_counter + 1
		repeat = 0

		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()