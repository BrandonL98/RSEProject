from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
import lock_module
import time

app = Flask(__name__)

data = ''
lockState = ''
@app.route("/names", methods=["POST", "GET"])
def names():
    if (request.method == "POST"):
        global data
        data = request.args.get('name')
        return data
    else:
        global data
        return jsonify({"name":data})

@app.route("/lock", methods=["GET","POST"])
def lockDoor():
    if (request.method == "POST"):
        global lockState 
        lockState = request.args.get('lock')
        if lockState == 'true':
            print(lockState)
            lock_module.lock_lock()
        elif lockState == 'false':
            print(lockState)
            lock_module.open_lock()
        return lockState
    else:
        state = lock_module.check_lock_status()
        if state == 'Locked':
            return jsonify({"state":"true"})
        elif state == 'Unlocked':
            return jsonify({"state":"false"})

@app.route("/status", methods=["GET"])
def status():
    state = lock_module.check_lock_status()
    return jsonify({"lock":state})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)