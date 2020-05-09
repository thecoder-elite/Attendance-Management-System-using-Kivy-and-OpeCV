''' 
THIS FILE TAKES IMAGES STORED IN THE DATA FOLDER AND CREATES A NUMPY ARRAY FOR EACH FACE STORED IN EACH SUB FOLDER.
THE ARRAY IS STORED IN THE trainer.yml FILE.
WE ALSO ASSIGN AN ID TO EACH FOLDER INSIDE THE DATA FOLDER SO THAT IT CAN BE USED TO RECOGNIZE THE PERSON.
WE STORE THE ID IN labels.pickle FILE

'''
import os # importing module 
import numpy as np   # import numpy library
from PIL import Image   # importing Image class from pillow module which is a python module for image processing
import cv2  # importing opencv library
import pickle
'''
“Pickling” is the process whereby a Python object hierarchy is converted into a byte stream.
pickle has two main methods.
The first one is dump, which dumps an object to a file object 
and the second one is load, which loads an object from a file object.
'''

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # finding where the current file is saved
image_dir = os.path.join(BASE_DIR,"images") # going into the images folder where this current file is saved

face_cascade = cv2.CascadeClassifier('data\haarcascade_frontalface_default.xml')   # explained in faces.py
recognizer = cv2.face.LBPHFaceRecognizer_create()

'''
for each label that we create we need to associate a id with it
so current keeps a track of that id for each label we increment current_id
and the label and the current_id value to the label_ids dictionary
'''
current_id = 0
label_ids = {}

x_train = []    # verify the image and turn it into a grayscaled numpy array
y_labels = []   # we need to store the labels as some number

for root,dirs,files in os.walk(image_dir): # walking through each file present in the images folder
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root,file)
            label = os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
       #     print(label,path)
            
            # checking if id associated with label is present in dictionary
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
       #     print(label_ids)

            pil_image = Image.open(path).convert("L")   # convert image into grayscale
            
            # resizing image for accuracy
            size = (550,550)
            final_img =pil_image.resize(size, Image.ANTIALIAS)
            
            
            image_array = np.array(final_img, "uint8")  # convert each image into an equivalent numpy array
       #     print(image_array)
            faces = face_cascade.detectMultiScale(image_array, scaleFactor=2, minNeighbors=5)

            # for each face we store the numpy array for it and its id 
            for(x,y,w,h) in faces:
                roi = image_array[y:y+h,x:x+w]
                x_train.append(roi)
                y_labels.append(id_)


#print(y_labels) # printing the labels for each named-directory 
#print(x_train)  # printing the numpy array for each image in that directory


with open("labels.pickle",'wb') as f:   # wb stands for writing in bits
    pickle.dump(label_ids,f) # storing label_ids in the pickle file

# we use the recognizer to store the numpy array of each face and the associated labels
recognizer.train(x_train,np.array(y_labels))
recognizer.save("trainer.yml") # we store into a file called trainer.yml
