from flask import Flask, render_template, request, redirect, url_for, abort, session
import recognize_video
import lock_module
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os

app = Flask(__name__)

@app.route("/camera", methods=["POST","GET"])
def camera():

    ap = argparse.ArgumentParser()

    ap.add_argument("-d", "--detector", required=True,
		help="path to OpenCV's deep learning face detector")
    ap.add_argument("-m", "--embedding-model", required=True,
		help="path to OpenCV's deep learning face embedding model")
    ap.add_argument("-r", "--recognizer", required=True,
		help="path to model trained to recognize faces")
    ap.add_argument("-l", "--le", required=True,
		help="path to label encoder")
    ap.add_argument("-c", "--confidence", type=float, default=0.5,
		help="minimum probability to filter weak detections")
    ap.add_argument("-rl", "--relearn", required=True,
		help="if there is photo to be relearned")
    args = vars(ap.parse_args())

    need_to_learn = args["relearn"]

    identified_record = recognize_video.process_video(need_to_learn,args["detector"],args["embedding_model"],args["recognizer"],args["le"],args["confidence"])

    # check man at door and if he/she is home owner
    door = "unknown"
    biggest_val = -1
    for key,val in identified_record.items():
        if val > biggest_val:
            door = key
            biggest_val = val

    f = open("homeowners.txt", "r")
    for line in f:
        line = line.rstrip()
        if line == door:
            return render_template('demo.html', name=door, homeowner="True")
        elif line == '':
            return render_template('demo.html', name=door)
	
    return render_template('demo.html', name=door)

@app.route("/lock")
def lock():
	state = lock_module.check_lock_status()
	return state

@app.route('/update_lock/<state>', methods=["PUT"])
def update_lock(state):
    if (state == "open"):
        lock_module.open_lock()
    if (state == "lock"):
        lock_module.lock_lock()

if __name__ == '__main__':
    app.run(debug=True, port = 8000)