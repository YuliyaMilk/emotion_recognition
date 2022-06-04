import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from PIL import Image, ImageTk

from src.menu_page import MenuPage
from src.realtime_page import RealtimePage
from src.image_page import ImagePage
from src.video_page import VideoPage
from src.video_without_demo import VideoNewPage

class GUI(tkinter.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.uploaded_image_button = None
        self.uploaded_image_label = None

        container = tkinter.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {} 
        self.file_path=None
  
        for F in (MenuPage, RealtimePage, ImagePage, VideoPage, VideoNewPage):
  
            frame = F(container, self,MenuPage,VideoNewPage)
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(MenuPage)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def start(self):
        self.title("Emotion Recognition")
        width= self.winfo_screenwidth()               
        height= self.winfo_screenheight()               

        self.geometry("%dx%d" % (width, height))
        self.mainloop()

    def open_file(self):
        global img, file_path
        my_str = tkinter.StringVar()

        my_str.set("")
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*jpg')])
        if file_path is not None:
            self.img_resized=Image.open(file_path)
            copy_img_resized = self.img_resized.copy()
            copy_img_resized = copy_img_resized.resize(IMG_SIZE)
            img=ImageTk.PhotoImage(copy_img_resized)
            my_str.set(file_path)

            if self.uploaded_image_label:
                self.uploaded_image_label.destroy()
            self.uploaded_image_label = tkinter.Label(self.window,textvariable=my_str,fg='red' )
            self.uploaded_image_label.pack()

            if self.uploaded_image_button:
                self.uploaded_image_button.destroy()
            self.uploaded_image_button = Button(self.window,image=img)
            self.uploaded_image_button.pack()
            
    
    def uploadButton(self):
        my_font1=('times', 18, 'bold')
     
        face = Label(self.window, text='Выберите фото ', anchor=CENTER, width=30,font=my_font1 )
        face.pack()
        facebtn = Button(self.window, text ='Choose File', width=20, command = lambda: gui.open_file()) 
        facebtn.pack()

    
    

gui = GUI()
gui['background']='#856ff8'

# gui.uploadButton()

gui.start()