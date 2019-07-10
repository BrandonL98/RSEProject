from flask import Flask, render_template, request, redirect, url_for, abort, session
import recognize_video
import build_face_dataset
import json_operations
import home_owner_operation
import lock_module
import requests
import argparse

app = Flask(__name__)

@app.route("/")
def start():
	return redirect(url_for('home'))

@app.route("/home", methods=["GET", "POST"])
def home():
	if request.method == "POST":
		if request.form["button"] == "start":
			return redirect(url_for('user'))
	else:
		return render_template('home.html')

@app.route("/camera", methods=["GET", "POST"])
def camera():
    
    if request.method == "POST":
        if request.form["button"] == "back":
            return redirect(url_for('user'))
    else:
        ap = argparse.ArgumentParser()

        ap.add_argument("-rl", "--relearn", required=True,
            help="if there is photo to be relearned")
        args = vars(ap.parse_args())

        need_to_learn = args["relearn"]

        recognize_video.process_video(need_to_learn,"face_detection_model",
            "openface_nn4.small2.v1.t7","output/recognizer.pickle","output/le.pickle",0.5)

    door = json_operations.readFromJSONFile('people_count')

    # only takes names with probability higher than [0.x]
    actualDoor = []
    for name in door:
        if (door[name] > 0.05):
            actualDoor.append(name)

    # convert list to string
    stringname = ", ".join(actualDoor)

    # check man at door and if he/she is home owner
    return render_template('demo.html', name=stringname)

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        if request.form["button"] == "lock":
            lock_module.lock_lock()
            return redirect(url_for('user'))
        elif request.form["button"] == "unlock":
            lock_module.open_lock()
            return redirect(url_for('user'))
        elif request.form["button"] == 'camera':
            return redirect(url_for('camera'))
        elif request.form["button"] == 'back':
            return redirect(url_for('home'))
        elif request.form["button"] == 'add':
            return redirect(url_for('add'))
        elif request.form["button"] == 'remove':
            return redirect(url_for('homeowner'))
    else: 
        state = lock_module.check_lock_status()
        return render_template('lock.html', lock_status = state)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        if request.form["button"] == 'add':
            text = request.form['name']
            low_text = text.lower()
            names = "dataset/" + low_text
            build_face_dataset.add_user("haarcascade_frontalface_default.xml", names, "False")
        elif request.form["button"] == 'add2':
            text = request.form['name']
            low_text = text.lower()
            names = "dataset/" + low_text
            build_face_dataset.add_user("haarcascade_frontalface_default.xml", names, "True")
        elif request.form["button"] == 'back':
            return redirect(url_for('user'))
		
    return render_template('add.html')

@app.route('/homeowner', methods=['GET','POST'])
def homeowner():
    # return a list of homeowners
    p_list = home_owner_operation.print_owners()
    if request.method == "GET":
        f = open("homeowners.txt", "r")
        f = map(lambda s: s.strip(), f)
        return render_template('homeowner.html', homeowners = p_list, lines = f)
    if request.method == "POST":
        if request.form["button"] == 'add':
            text = request.form['name']
            low_text = text.lower()
            home_owner_operation.add_owner(low_text)
            return redirect(url_for('homeowner'))
        elif request.form["button"] == 'delete':
            # delete the name input into the field
            del_name = request.form['owner']
            print(del_name)
            home_owner_operation.delete_owner(del_name)
            f = open("homeowners.txt", "r")
            f = map(lambda s: s.strip(), f)
            return redirect(url_for('homeowner'))
        elif request.form["button"] == 'back':
            return redirect(url_for('user'))
    
if __name__ == '__main__':
        app.run(debug=True, port = 8000)
