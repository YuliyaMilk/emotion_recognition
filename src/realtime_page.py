import tkinter as tk
from tkinter import ttk
import tkinter
from tkinter import *
from tkinter.ttk import *
from src.recognitions.real_time_video import MyVideoCapture
from PIL import Image, ImageTk

class RealtimePage(tk.Frame):
    def __init__(self, parent, controller, MenuPage,VideoNewPage,video_source=0 ):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#fcfcfc')
        self.video_source = video_source
        self.vid = MyVideoCapture(self, self.video_source)
        # Create a canvas that can fit the above video source size
        self.canvasVideo = tk.Canvas(self, width = self.vid.width, height = self.vid.height, bg='#fcfcfc')
        self.canvasEmotions = tk.Canvas(self, width = 420, height = 300, bg='#fcfcfc')
        self.canvasVideo.grid(row=2, column=1, padx = 10, pady = 50)
        self.canvasEmotions.grid(row=2, column=2)

        my_font1=('Segoe UI Semibold', 18, 'bold')

        img = Image.open("./custom/menu.png")
        img = img.resize((70,40), Image.ANTIALIAS)
        self.menu =  ImageTk.PhotoImage(img)
        # self.loadimage = tk.PhotoImage(file="./custom/button.png")
        menubtn = tk.Button(self, image=self.menu, width=70, command = lambda: self.back(controller,MenuPage))
        menubtn["bg"] = "white"
        menubtn["border"] = "0"
        menubtn.grid(row = 1, column = 1, padx = 20, pady = 5,sticky = 'w')
     
        namePage = tk.Label(self, text='Распознавание эмоции в реальном времени', anchor=CENTER, font=my_font1, bg='#fcfcfc' , fg='#006089')
        namePage.grid(row = 1, column = 1, pady = 10, columnspan=2)

        self.delay = 30
        self.update()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
 
        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvasVideo.create_image(0, 0, image = self.photo, anchor = tk.NW)
            self.canvasEmotions.delete('all')
            self.vid.recognition(frame, self.canvasVideo, self.canvasEmotions)
 
        self.after(self.delay, self.update)

    def back(self, controller, MenuPage):
            controller.show_frame(MenuPage)