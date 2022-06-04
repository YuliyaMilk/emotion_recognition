import tkinter as tk
from tkinter import Label, CENTER, filedialog, Entry, StringVar
from PIL import Image, ImageTk
from src.recognitions.video import LoadVideoCapture
import imutils
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

FRAME_SIZE = (640, 360)

class VideoPage(tk.Frame):
    def __init__(self, parent, controller, MenuPage, VideoNewPage):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#fcfcfc')
        self.vid = None
        # self.vid = MyVideoCapture(self, self.video_source)
        # Create a canvas that can fit the above video source size
        self.file_path = None
        top_frame = tk.Frame(self, bg='#fcfcfc')
        top_frame.pack(side=tk.TOP, fill=tk.BOTH)
        bottom_frame = tk.Frame(self, bg='#fcfcfc')
        bottom_frame.pack(side=tk.TOP, fill=tk.BOTH)  


        my_font1=('Segoe UI Semibold', 18, 'bold')
        my_font2=('Segoe UI Semibold', 14)

        img = Image.open("./custom/menu.png")
        img = img.resize((70,40), Image.ANTIALIAS)
        self.menu =  ImageTk.PhotoImage(img)
        # self.loadimage = tk.PhotoImage(file="./custom/button.png")
        menubtn = tk.Button(top_frame, image=self.menu, width=70, command = lambda: self.back(controller,MenuPage))
        menubtn["bg"] = "white"
        menubtn["border"] = "0"
        menubtn.grid(row = 1, column = 1, padx = 20, pady = 5, sticky = 'w')
     
        namePage = tk.Label(top_frame, text='Распознавание эмоции в видео', anchor=CENTER, font=my_font1, bg='#fcfcfc' , fg='#006089')
        namePage.grid(row = 1, column = 4, pady = 10, padx = 30)
        

        img = Image.open("./custom/button2.png")
        img = img.resize((135, 50), Image.ANTIALIAS)
        self.loadimage =  ImageTk.PhotoImage(img)
        facebtn = tk.Button(top_frame, image=self.loadimage, width=135, command = lambda: self.open_file())
        facebtn["bg"] = "white"
        facebtn["border"] = "0"
        facebtn.grid(row = 2, column = 3, padx = 35, pady = 5,sticky = 'w', rowspan=2)

        img = Image.open("./custom/rec_em_without_demo.png")
        img = img.resize((200, 50), Image.ANTIALIAS)
        self.new_page =  ImageTk.PhotoImage(img)
        without_demo = tk.Button(top_frame, image=self.new_page, width=200, command = lambda: self.open_page(controller, VideoNewPage, self.file_path))
        without_demo["bg"] = "white"
        without_demo["border"] = "0"
        without_demo.grid(row = 2, column = 4, padx = 10, pady = 5,sticky = 'w', rowspan=2)

        name = StringVar()
        surname = StringVar()
        
        name_label = tk.Label(top_frame, text="Введите имя:", font=my_font2, bg='#fcfcfc' , fg='#006089')
        surname_label = tk.Label(top_frame, text="Введите фамилию:", font=my_font2, bg='#fcfcfc' , fg='#006089')
        
        name_label.grid(row=2, column=1, sticky="w")
        surname_label.grid(row=3, column=1, sticky="w")
        
        self.name_entry = Entry(top_frame, textvariable=name)
        self.surname_entry = Entry(top_frame, textvariable=surname)
        
        self.name_entry.grid(row=2,column=2, padx=5, pady=5)
        self.surname_entry.grid(row=3,column=2, padx=5, pady=5)

        self.canvasVideo = tk.Canvas(bottom_frame, width = FRAME_SIZE[0], height = FRAME_SIZE[1], bg='#fcfcfc')
        self.canvasVideo.grid(row=0, column=0, padx = 10, pady = 45, sticky='w')

        self.canvasDiagram = tk.Canvas(bottom_frame, width = 1000, height = 200, bg='#fcfcfc')
        self.f = Figure(figsize=(15, 2))
        self.canvasDiagram.grid(row=1, column=0, columnspan=2)
        self.ax = self.f.add_subplot(111)
        self.ax.plot([], [])
        self.ax.set(xlim=[0, 200], ylim=[0, 100], title='Диаграмма',
        ylabel='Вероятность эмоции', xlabel='Время')
        
        self.canvas = FigureCanvasTkAgg(self.f, self.canvasDiagram)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT)

        self.delay = 30
        self.update()

    def open_file(self):
        my_str = StringVar()

        my_str.set("")
        self.file_path = filedialog.askopenfilename(filetypes=[('Video Files', '*mp4')])
        if self.file_path is not None:
            self.vid = LoadVideoCapture(self, self.file_path)


    def update(self):
        # Get a frame from the video source
        if not self.vid:
            self.after(self.delay, self.update)
            return

        ret, frame = self.vid.get_frame()
        if ret:
            frame = imutils.resize(frame, width=FRAME_SIZE[0])
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvasVideo.create_image(0, 0, image = self.photo, anchor = tk.NW)
            self.vid.recognition(frame, self.canvasVideo, self.canvas, self.ax)
        self.after(self.delay, self.update)

    def back(self, controller, MenuPage):
            controller.show_frame(MenuPage)

    def open_page(self,controller, VideoNewPage, file_path):
        controller.file_path = file_path
        controller.show_frame(VideoNewPage)