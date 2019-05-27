# RSEProject - Smart Door Unlock

## Face Detection
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

### To train machine for recognizing faces

The steps follow do the training for face recognizing:
```
python extract_embeddings.py --dataset dataset --
embeddings output/embeddings.pickle --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7
```

After this is ran successfully run:
```
python train_model.py --embeddings output/embeddings.pickle --recognizer output/recognizer.pickle --le output/le.pickle
```

### To identify faces from camera
The following step will open the camera and output the names of people recognized

**!!! OUTPUT IS STILL TO BE IMPLEMENTED !!!**

```
python recognize_video.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle
```