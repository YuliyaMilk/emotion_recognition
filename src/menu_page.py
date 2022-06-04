import tkinter as tk
from tkinter import CENTER, Label, Button, Frame

from src.realtime_page import RealtimePage
from src.image_page import ImagePage
from src.video_page import VideoPage
from PIL import Image, ImageTk


class MenuPage(tk.Frame):
    def __init__(self, parent, controller, MenuPage,VideoNewPage):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#fcfcfc')
        
        frame = Frame(self,  bg='#fcfcfc')
        frame.place(relx=0.5, rely=0.4, anchor="c")
        
        # label of frame Layout 2
        my_font1=('Segoe UI Semibold', 18, 'bold')
     
        label = Label(frame, text ="Меню", font = my_font1, bg='#fcfcfc',fg='#006089', anchor=CENTER)
         
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan=4, sticky='ew')


        img = Image.open("./custom/page1.png")
        img = img.resize((270,50), Image.ANTIALIAS)
        self.recReal =  ImageTk.PhotoImage(img)
        button1 = tk.Button(frame, image=self.recReal, width=280, command = lambda: controller.show_frame(RealtimePage))
        button1["bg"] = "white"
        button1["border"] = "0"
        # button1 = Button(frame, text ="Real Time Emotion Recognition",
        # command = lambda : controller.show_frame(RealtimePage))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        ## button to show frame 2 with text layout2
        img = Image.open("./custom/page2.png")
        img = img.resize((270,50), Image.ANTIALIAS)
        self.recImage =  ImageTk.PhotoImage(img)
        button2 = tk.Button(frame, image=self.recImage, width=280, command = lambda: controller.show_frame(ImagePage))
        button2["bg"] = "white"
        button2["border"] = "0"
        # button2 = Button(frame, text ="Image Emotion Recognition",
        # command = lambda : controller.show_frame(ImagePage))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

         ## button to show frame 2 with text layout2
        img = Image.open("./custom/page3.png")
        img = img.resize((270,50), Image.ANTIALIAS)
        self.recVideo =  ImageTk.PhotoImage(img)
        button3 = tk.Button(frame, image=self.recVideo, width=280, command = lambda: controller.show_frame(VideoPage))
        button3["bg"] = "white"
        button3["border"] = "0"
        # button2 = Button(frame, text ="Image Emotion Recognition",
        # command = lambda : controller.show_frame(ImagePage))
     
        # putting the button in its place by
        # using grid
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)