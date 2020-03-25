import numpy as np # importing numpy library
import cv2  # importing opencv library
import pickle

def face():
     # getting haar classifier
     face_cascade = cv2.CascadeClassifier('data\haarcascade_frontalface_default.xml') # there are different types of classifiers we are using the specified one
     recognizer = cv2.face.LBPHFaceRecognizer_create()
     recognizer.read("trainer.yml")


     labels = {}
     # we import the created pickle file to get the value of the label from the id that we get from the recognizer
     with open("labels.pickle",'rb') as f:   # wb stands for read in bits
          og_labels = pickle.load(f) # storing label_ids in the pickle file
          labels = {v:k for k,v in og_labels.items()}
     # enabling the camera 
     cap = cv2.VideoCapture(0)

     while(True):
          # capture frame by frame
          ret,frame = cap.read()
          
          # converting the image to gray scale
          gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

          # scaling the image 
          faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) # incr scaleFactor increases accuracy but too high and accuracy decreases
          
          # printing the coordinates of faces detected by the camera 
          for(x, y, w, h) in faces:
               print(x,y,w,h)
               


               # getting the region of interest (roi i.e the face) from the gray frame  
               roi_gray = gray[y:y+h,x:x+w]

               # getting the region of interest (roi i.e the face) from the colored frame
          #     roi_color = frame[y:y+h,x:x+w]
          
               #creating a file to save the roi
          #     img_item = "my-image.png"
          
               # actually saving the image
          #     cv2.imwrite(img_item,roi_gray)

               # drawing a rectangle around roi
               color = (255,0,0)   # BGR color code not RGB
               stroke = 2  # width of the border of rectangle
               width = x + w   # defining width of rectangle
               height = y + h  # defining height of rectangle
               cv2.rectangle(frame, (x,y) , (width ,height), color, stroke )   # calling actual rectangle generation function

               # we use the roi gray to feed it to our predictor 
               id_, conf = recognizer.predict(roi_gray) # we take the id of the predicted image and a confidence score related to it
               if conf>=85:
                    print("id id = "+str(id_))
                    print("conf is = "+str(conf))
                    print(labels[id_])
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    name = labels[id_]
                    color = (255,0,0)
                    stroke = 2
                    cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)


          # display resulting frame
          cv2.imshow('frame',frame)
          if cv2.waitKey(20) & 0xFF == ord('q'):
               break 

     # when everything is done release capture 
     cap.release()
     cv2.destroyAllWindows()

     #return the name of recognized face
     return labels[id_]


'''
-> to detect a face we have used a opencv class
known as the "haar classifier"

-> to draw the rectangle around the face we have used opencv method called rectangle

-> to recognize a face we can use
1. deep learning model
2. keras
3. tensorflow
4. pytorch
5. scikit learn
but we are using lbph face recognizer

'''