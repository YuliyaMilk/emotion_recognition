import tkinter as tk
from tkinter import Label, CENTER, filedialog, Entry, StringVar
from PIL import Image, ImageTk
from src.recognitions.video_new import NewVideoCapture
import imutils
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

FRAME_SIZE = (640, 360)

class VideoNewPage(tk.Frame):
    def __init__(self, parent, controller, MenuPage,VideoNewPage):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#fcfcfc')
        self.vid = None
        self.file_path = controller.file_path
        self.time_video = 0

        self.data_values = {
            "angry": 0,
            "disgust": 0,
            "scared": 0, 
            "happy": 0, 
            "sad": 0, 
            "surprised": 0, 
            "neutral": 0,
        }
        # self.vid = MyVideoCapture(self, self.video_source)
        # Create a canvas that can fit the above video source size

        top_frame = tk.Frame(self, bg='#fcfcfc')
        top_frame.pack(side=tk.TOP, fill=tk.BOTH)
        


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

        video_label = tk.Label(top_frame, text="Видео: ", font=my_font2, bg='#fcfcfc' , fg='#006089')
        self.video_path = tk.Label(top_frame, text="", font=my_font2, bg='#fcfcfc' , fg='red')
        video_label.grid(row=4, column=1, sticky="w")
        self.video_path.grid(row=4, column=2, sticky="w", columnspan=3)

        time_label = tk.Label(top_frame, text="Оставшееся время: ", font=my_font2, bg='#fcfcfc' , fg='#006089')
        self.time_name = tk.Label(top_frame, text="", font=my_font2, bg='#fcfcfc' , fg='#006089')
        time_label.grid(row=5, column=1, sticky="w")
        self.time_name.grid(row=5, column=2, sticky="w", columnspan=3)

        self.delay = 30
        self.update()

    def open_file(self):
        my_str = StringVar()

        my_str.set("")
        self.file_path = filedialog.askopenfilename(filetypes=[('Video Files', '*mp4')])
        if self.file_path is None:
            self.video_path["text"] = "Выберите видео!"
        else:
            self.video_path["text"] = self.file_path
            self.vid = NewVideoCapture(self,  self.name_entry.get(), self.surname_entry.get(), self.data_values, self.file_path)


    def update(self):
        # Get a frame from the video source
        if not self.vid:
            self.after(self.delay, self.update)
            return

        ret, frame = self.vid.get_frame()
        if ret:
            self.vid.recognition(frame, self.data_values)
            self.time_name["text"] = self.vid.get_time_video()
            if self.data_values['angry'] == 0 and self.data_values['disgust'] == 0 and self.data_values['scared'] == 0 and self.data_values['happy'] == 0 and self.data_values['sad'] == 0 and self.data_values['surprised'] == 0 and self.data_values['neutral'] == 0:
                pass
            else:
                self.vid.createResults(self.data_values)
        else: 
            self.time_name["text"] = "Готово"
        self.after(self.delay, self.update)

    def back(self, controller, MenuPage):
            controller.show_frame(MenuPage)