# RSEProject - Smart Door Unlock
Developed by Brandon Le, Zhou Cindy, Winston Darmawan, James Zhang, Ann LMing
## Face Detection 
### To install opencv 3 on Windows
Link to step-to-step instructions: 
https://solarianprogrammer.com/2016/09/17/install-opencv-3-with-python-3-on-windows/


The following sections assume python3 and opencv was correctly installed


When encountering error about the package not being recognized do:
```
python -m pip install <package name>
```

### Install dependencies
Install all of these packages through the user command line.


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

### Simplified Usage
The following step will create a local host webpage that has access to all the features that the offline version of the Smart Door Unlock offers. This version will use the default webcam for your laptop or monitor. 
```
python routes.py --relearn <True/False>
```

relearn False -> will skip the learning image process. This will be the normal setting for booting up the program.

relearn True -> will run the learning image process when the camera loads up. Used for when photos are manually added to the dataset rather than through the user interface.

The webpage loaded can be accessed through this URL
```
http://127.0.0.1:8000
```

