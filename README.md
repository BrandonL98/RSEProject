# RSEProject - Smart Door Unlock
Developed by Brandon Le, Zhou Cindy, Winston Darmawan, James Zhang, Ann LMing

# Face Detection 
## To install opencv 3 on Windows
Link to step-to-step instructions: 
https://solarianprogrammer.com/2016/09/17/install-opencv-3-with-python-3-on-windows/


The following sections assume python3 and opencv was correctly installed


When encountering error about the package not being recognized do:
```
python -m pip install <package name>
```

## Install dependencies
Install these packages through the user command line.

Essentials for facial recognition:
```
python -m pip install --upgrade imutils
```
```
python -m pip install scikit-learn
```
Essentials for server backend requests:
```
python -m pip install Flask
```
```
python -m pip install requests
```

## Setting up server
Copy the python file from the cloud folder to a cloud server with an elastic IP address. Make sure that cloud.py is running to ensure that the Smart Door Unlock will run. The IP address will need to be changed for post/get requests on both recognise_video.py and routes.py to the correct address for the cloud server. 

## Setting up Google Home (optional)
### Setting up firebase
Follow the tutorial on how to set up a firebase account on your laptop.
https://codelabs.developers.google.com/codelabs/actions-2/index.html?index=..%2F..index#1


### Setting up the working directory

If the current directory is not set up with firebase yet, the following steps will help initialise the directory for you. In the directory you want to work in, type
```
firebase init
select functions
select the firebase project (actions-lockagent-ea0fb (actions-lockagent))
javascript
yes
yes
```
Following the above commands should initialise the directory with a firebase.json and functions directory. Go into the functions directory.
```
cd functions
```
Functions folder contains an index.js file file, package.json file and a node-modules folder. The node-modules folder contains all the npm dependicies required for the program. Index.js is the primary file we will be working on. 

### Running the program
We first need to declare which agent we are working with.
```
firebase use --project actions-lockagent-ea0fb
```
After this, run the following steps to compile and deploy our files into the google cloud.
```
npm install
firebase deploy --project actions-lockagent-ea0fb
```
The file is now updated on the firebase server. On dialogflow, the intents should reply with the updated conversation responses declared in the index.js file. 


## Program Usage
The following step will create a local host webpage, it will assume that you have the cloud server up and running. This version will access the secondary webcam or camera (not the default webcam) connected to the computer. It will run independently to whether or not Google Home application is functioning.

```
python routes.py --relearn <True/False>
```

--relearn False -> will skip the learning image process. This will be the normal setting for booting up the program.

--relearn True -> will run the learning image process when the camera loads up. Used for when photos are manually added to the dataset rather than through the user interface.

The webpage loaded can be accessed through this URL
```
http://127.0.0.1:8000
```
