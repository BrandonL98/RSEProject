# RSEProject - Smart Door Unlock

## Face Detection :trollface:
### To install opencv 3 on Windows
Link to step-to-step instructions: 
https://solarianprogrammer.com/2016/09/17/install-opencv-3-with-python-3-on-windows/


The following sections assume python3 and opencv was correctly installed


When encountering error about the package not being recognized do:
```
python -m pip install <package name>
```


### To add faces to dataset
The following steps allow the homeowner to add new pictures of faces to dataset:
```
python build_face_dataset.py --cascade haarcascade_frontalface_default.xml --output dataset/<name of faces to be added> --homeowner <True/False>
```

Press K to capture faces

Press Q to quit


If ran successfully, the program should assure that the folder with the name of faces exist in dataset directory. If the person is the homeowner, the name will also be written to "homeowners.txt"


### To identify faces from camera
The following step will open the camera and output the names of people recognized

```
python recognize_video.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle
```


This will train the computer to recognize faces and open up a web page: **127.0.0.1:8000** , which is the home page

To continue: click start button, this will take you to demo page

The camera should then open and start facial recognition

press Q to quit

Once you quit, check the web page again, it should have the heading demo and the information about who's at the door

There are 3 possible outcomes:

```
The person at the door is a stranger
```

```
The home owner <name> is at the door
```

```
The visitor {{name}} is at the door
```

There should also be a button "Home" which will bring you back to home page