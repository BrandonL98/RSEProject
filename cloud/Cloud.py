from flask import Flask, render_template, request, redirect, url_for, abort, session

app = Flask(__name__)

data = ''
lockState = ''
@app.route("/names", methods=["POST", "GET"])
def names():
    if (request.method == "POST"):
        global data
        data = request.form.get('name')
        return data
    else:
        global data
        return data

@app.route("/lock", methods=["GET","POST"])
def lockDoor():
    if (request.method == "POST"):
        global lockState 
        lockState = request.form.get('lock')
        return 'lock has been changed to ' + lockState
    else:
        global lockState
        return lockState

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)