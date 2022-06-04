import tkinter as tk
from tkinter import ttk
from src.recognitions.real_time_video import MyVideoCapture
import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import Label, Button
from PIL import Image, ImageTk
from src.recognitions.image import ImageRecognition

class ImagePage(tk.Frame):
    def __init__(self, parent, controller, MenuPage, VideoNewPage):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#fcfcfc')
        self.img_resized = []
        self.file_path = ""
        self.image = ImageRecognition(self, self.file_path)

        img = Image.open("./custom/menu.png")
        img = img.resize((70,40), Image.ANTIALIAS)
        self.menu =  ImageTk.PhotoImage(img)
        # self.loadimage = tk.PhotoImage(file="./custom/button.png")
        menubtn = tk.Button(self, image=self.menu, width=70, command = lambda: self.back(controller,MenuPage))
        menubtn["bg"] = "white"
        menubtn["border"] = "0"
        menubtn.grid(row = 1, column = 1, padx = 20, pady = 5,sticky = 'w')

        my_font1=('Segoe UI Semibold', 18, 'bold')
     
        namePage = Label(self, text='Распознавание эмоции на изображении', anchor=CENTER, font=my_font1, bg='#fcfcfc' , fg='#006089')
        namePage.grid(row = 1, column = 2, pady = 10)
        # facebtn = Button(self, text ='Choose File', width=20, command = lambda: self.open_file()) 
        # facebtn.grid(row = 2, column = 1, padx = 5, pady = 5)
        width = 160
        height = 50
        img = Image.open("./custom/button1.png")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.loadimage =  ImageTk.PhotoImage(img)
        # self.loadimage = tk.PhotoImage(file="./custom/button.png")
        facebtn = tk.Button(self, image=self.loadimage, width=160, command = lambda: self.open_file())
        facebtn["bg"] = "white"
        facebtn["border"] = "0"
        facebtn.grid(row = 2, column = 1, padx = 20, pady = 5,sticky = 'w')


        self.canvasImage = tk.Canvas(self, width = 540, height = 460, bg='#fcfcfc')
        self.canvasEmotions = tk.Canvas(self, width = 420, height = 300, bg='#fcfcfc')
        self.canvasImage.grid(row=3, column=1, padx = 5, pady = 30)
        self.canvasEmotions.grid(row=3, column=3)
        self.canvasEmotionRecognition = tk.Canvas(self, width = 540, height = 460, bg='#fcfcfc')
        self.canvasEmotionRecognition.grid(row=3, column=2, padx = 5, pady = 30)


        img = Image.open("./custom/recognition_emotion.png")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.recImage =  ImageTk.PhotoImage(img)
        # self.loadimage = tk.PhotoImage(file="./custom/button.png")
        recognitionBtn = tk.Button(self, image=self.recImage, width=160, command = lambda: self.image.find_face( self.canvasEmotions, self.canvasEmotionRecognition))
        recognitionBtn["bg"] = "white"
        recognitionBtn["border"] = "0"
        # recognitionBtn = Button(self, text ='Распознать эмоцию', width=20, command = lambda: self.image.find_face( self.canvasEmotions, self.canvasEmotionRecognition)) 
        recognitionBtn.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'e')

    def open_file(self):
        my_str = tkinter.StringVar()

        my_str.set("")
        self.file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*jpg')])
        if self.file_path is not None:
            self.img_resized=Image.open(self.file_path)
            self.image = ImageRecognition(self, self.file_path)
            copy_img_resized = self.img_resized.copy()
            self.photo = ImageTk.PhotoImage(copy_img_resized)
            self.canvasImage.create_image(self.canvasImage.winfo_width() / 2 - self.photo.width() / 2, 0, 
                                          image = self.photo, anchor = tk.NW)
            self.canvasEmotions.delete('all')
            self.canvasEmotionRecognition.delete('all')
            # my_str.set(file_path)

            # if self.uploaded_image_label:
            #     self.uploaded_image_label.destroy()
            # self.uploaded_image_label = tkinter.Label(self.window,textvariable=my_str,fg='red' )
            # self.uploaded_image_label.pack()

            # if self.uploaded_image_button:
            #     self.uploaded_image_button.destroy()
            # self.uploaded_image_button = Button(self.window,image=img)

    def back(self, controller, MenuPage):
            controller.show_frame(MenuPage)
    