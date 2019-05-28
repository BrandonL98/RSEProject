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

@app.route("/camera")
def camera():

    ap = argparse.ArgumentParser()

    ap.add_argument("-rl", "--relearn", required=True,
		help="if there is photo to be relearned")
    args = vars(ap.parse_args())

    need_to_learn = args["relearn"]

    identified_record = recognize_video.process_video(need_to_learn,"face_detection_model",
        "openface_nn4.small2.v1.t7","output/recognizer.pickle","output/le.pickle",0.5)

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
	return render_template('lock.html', lock_status = state)

@app.route('/update_lock/<state>', methods=["PUT"])
def update_lock(state):
    if (state == "open"):
        lock_module.open_lock()
    if (state == "lock"):
        lock_module.lock_lock()

if __name__ == '__main__':
    app.run(debug=True, port = 8000)