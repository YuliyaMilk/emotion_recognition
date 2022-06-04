from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import tkinter as tk
import time
import os
from PIL import Image, ImageTk

EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised", "neutral"]

class ImageRecognition:
    def __init__(self, window, file_path):
        # Open the video source
        self.window = window
        if (file_path): 
            self.frame = cv2.imread(file_path)
            self.height, self.width, _ = self.frame.shape 
            img=Image.open(file_path)
            self.photo = ImageTk.PhotoImage(img)
        
        
        detection_model_path = './src/recognitions/cascades/haarcascade_frontalface_default.xml'
        emotion_model_path = './src/recognitions/modelall.h5'

        # hyper-parameters for bounding boxes shape
        # loading models
        self.face_detection = cv2.CascadeClassifier(detection_model_path)
        self.emotion_classifier = load_model(emotion_model_path, compile=False)
        # Get video source width and height

        
        
        
    
    def find_face(self, canvasEmotions, canvasEmotionRecognition):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detection.detectMultiScale(gray,scaleFactor=1.5, minNeighbors=5)
        if len(faces) > 0:
            faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
                        # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
                # the ROI for classification via the CNN
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            
            
            preds = self.emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]
    
            for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                if len(emotion) < 9:
                    emotion += ' ' * (9 - len(emotion))
                probPercent = prob * 100
                if (probPercent < 10):
                    probPercent = " {:.2f}".format(probPercent)
                else:
                     probPercent = "{:.2f}".format(probPercent)
                text = "{}: {}%".format(emotion, probPercent)

                w = int(prob * 300)
                canvasEmotions.create_rectangle(110, (i * 35) + 5, w + 110, (i * 35) + 35)
                canvasEmotions.create_text(103, (i * 35) + 23, font="Verdana 14", text=text, width=200, justify=tk.LEFT)
                cv2.rectangle(self.frame, (fX, fY), (fX + fW, fY + fH), (255, 0, 0), 2)
                cv2.imwrite("./ImageEmotionRecognition/image-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", self.frame)
                canvasEmotionRecognition.create_image(canvasEmotionRecognition.winfo_width() / 2 - self.photo.width() / 2, 0, image = self.photo, anchor = tk.NW)
                canvasEmotionRecognition.create_text(fX, fY - 10, font="Verdana 14", text=label)
                canvasEmotionRecognition.create_rectangle(fX+canvasEmotionRecognition.winfo_width() / 2 - self.photo.width() / 2, fY, fX + fW+canvasEmotionRecognition.winfo_width() / 2 - self.photo.width() / 2, fY + fH)
                

    
