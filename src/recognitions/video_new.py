from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


import tkinter as tk

EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised", "neutral"]

def convertMillis(millis):
    seconds, millis = divmod(millis, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return seconds, minutes, hours

df = pd.DataFrame(columns=['Person', 'Time', 'Emotion', 'Probability', 'Other emotion'])

class NewVideoCapture:
    def __init__(self, window, name, surname, data_values, video_source=0):
        # Open the video source
        self.window = window
        self.vid = cv2.VideoCapture(video_source)
        self.last_emotion = ''
        self.name = name + " " +  surname
        self.j = 0
        self.count = 0
        self.data_values = data_values
        
        self.millis=0
        fps = self.vid.get(cv2.CAP_PROP_FPS)
        frame_count = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration = frame_count/fps

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        # parameters for loading data and images
        detection_model_path = './src/recognitions/cascades/haarcascade_frontalface_default.xml'
        emotion_model_path = './src/recognitions/modelall.h5'

        # hyper-parameters for bounding boxes shape
        # loading models
        self.face_detection = cv2.CascadeClassifier(detection_model_path)
        self.emotion_classifier = load_model(emotion_model_path, compile=False)
        # Get video source width and height
        
    
    def recognition(self, frame, data_values):
        frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
            
            
            self.millis = self.vid.get(cv2.CAP_PROP_POS_MSEC)

            if self.last_emotion:
                data_values[self.last_emotion] += 1
            if self.last_emotion != label:
                self.last_emotion = label
                canvas = []
                

                for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                    text = "{}: {:.2f}%".format(emotion, prob * 100)
                    canvas.append(text)
                    
                
                con_sec, con_min, con_hour = convertMillis(int(self.millis))
                time = "{0}:{1}:{2}".format(con_hour, con_min, con_sec)
                df.loc[self.j] = [self.name , time , label, round(emotion_probability*100, 2), canvas]
                self.j += 1

            return data_values
                

           

    def createResults(self, data_values):
        labels = []
        sizes = []
        for x, y in data_values.items():
            labels.append(x)
            sizes.append(y)

        # Plot
        patches, text = plt.pie(sizes)

        plt.legend(patches, labels, loc='best')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('emotion_diagram.png')

        with pd.ExcelWriter('detection.xlsx', engine='xlsxwriter') as wb:
            df.to_excel(wb, sheet_name='Emotion', index=False)
            sheet = wb.sheets['Emotion']
            sheet.autofilter(0, 0, df.shape[0], 2)
            sheet.set_column('A:D', 10)
            sheet.set_column('E:E', 100)
            sheet.insert_image('G1', 'emotion_diagram.png')
        

    def get_time_video(self):
        res = (self.duration * 1000) - self.millis
        con_sec, con_min, con_hour = convertMillis(int(res))
        time = "{0}:{1}:{2}".format(con_hour, con_min, con_sec)
        return time

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.mainloop()