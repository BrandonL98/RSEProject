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

### Install dependencies
Essentials for facial recognition
```
python -m pip install --upgrade imutils
```
```
python -m pip install scikit-learn
```
Essentials for server backend requests
```
python -m pip install Flask
```
```
python -m pip install requests
```

### Simplified Usage
The following step will create a local host webpage that has access to the rest of the features below.
```
python routes.py --relearn <True/False>
```

relearn True -> will run the learning image process

relearn False -> will skip the learning image process

The webpage loaded can be accessed through this URL
```
http://127.0.0.1:8000
```
