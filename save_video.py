import cv2
import dlib
import tkinter
import numpy as np
from tqdm import tqdm
from PIL import Image,ImageTk
detector=dlib.get_frontal_face_detector()

# Set the size of the displayed image 
img_width=500
img_height=400
def TKImages(frame):
    # The camera flipped 
    # frame=cv2.flip(frame,1)
    image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)
    image=image.astype(np.uint8)
    PILimage=Image.fromarray(image)
    PILimage=PILimage.resize((img_width,img_height),Image.ANTIALIAS)
    try:
        tkImage=ImageTk.PhotoImage(image=PILimage)
    except:
        return 0
    return tkImage

def Canvas_(root):
    #  Create a canvas 
    canvas = tkinter.Canvas(root, bg='white', width=img_width, height=img_height)
    canvas.place(x=150, y=50)
    #  Create a label 
    label = tkinter.Label(root, text=' Face detection ', font=(' In black ', 14), width=15, height=1)
    # `anchor=nw` The upper left corner of the picture is used as the anchor point 
    label.place(x=300, y=20, anchor='nw')
    return canvas
#  Save the detected video 
image_path='hometown.jpg'
tkimage=''
def generate_video(input_path):
	global tkimage
    # Get the video name 
    filehead = input_path.split('/')[-1]
    # Saved in 
    output_path = 'Output_Video/'+'out_'+filehead

    print(' The video starts processing ')

    #  Get the total number of video frames 
    cap = cv2.VideoCapture(input_path)
    frame_count = 0
    while cap.isOpened():
        success, frame = cap.read()
        frame_count += 1
        if not success:
            break
    cap.release()
    # fps=cap.get(cv2.CAP_PROP_FPS)
    # frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(' Total frames of video : {}'.format(frame_count))

    cap = cv2.VideoCapture(input_path)
    # Get the height and width of the frame 
    frame_size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Get the saved video format 
    fource = cv2.VideoWriter_fourcc(*'mp4v')
    # Get video frames 
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Video preservation 
    out = cv2.VideoWriter(output_path, fource, fps, (int(frame_size[0]), int(frame_size[1])))
    margin = 0.2
    #  Set the font displayed 
    font = cv2.FONT_HERSHEY_SIMPLEX
    try:
        # Progress bar function 
        with tqdm(total=frame_count) as pbar:
            for i in range(frame_count):
                success, frame = cap.read()
                try:
                    # Get the height and width of the frame 
                    img_h, img_w, _ = np.shape(frame)
                    detected = detector(frame)
                    # If there is a face in the detected frame, frame and detect 
                    if len(detected) > 0:
                        for i, locate in enumerate(detected):
                            x1, y1, x2, y2, w, h = locate.left(), locate.top(), locate.right() + 1, locate.bottom() + 1, locate.width(), locate.height()

                            xw1 = max(int(x1 - margin * w), 0)
                            yw1 = max(int(y1 - margin * h), 0)
                            xw2 = min(int(x2 + margin * w), img_w - 1)
                            yw2 = min(int(y2 + margin * h), img_h - 1)

                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                            cv2.putText(frame, 'person', (x1, y1 - 10), font, 1.2, (0, 255, 0), 3)
                    pic=TKImages(frame)
                    canvas.create_image(0,0,anchor='nw',image=pic)
                    root.updata()
                    root.after(1)
                except Exception as e:
                    # print('error',e)
                    pass
                if success == True:
                    out.write(frame)
                    pbar.update(1)
    except:
        print(' Break in the middle ')
        pass
    img=cv2.imread(image_path)
    tkimage=TKImages(img)
    canvas.create_image(0,0,anchor='nw',image=tkimage)
    cv2.destroyAllWindows()
    out.release()
    cap.release()
    print(' The video has been saved to {}'.format(output_path))

