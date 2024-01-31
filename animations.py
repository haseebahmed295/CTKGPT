import customtkinter
from PIL import Image
import tkinter

class Loading:
    file = r"assets\spinner.gif"
    def __init__(self,root , master) -> None:
        self.photoimage_objects = []
        self.root = root

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(2, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(2, weight=1)
        self.gif_label = customtkinter.CTkLabel(master, text="Loading \nChat History", image="")
        self.gif_label.grid(row=1 , column=1)
        
        info = Image.open(Loading.file)
        self.frames = info.n_frames # number of frames
        
        for i in range(self.frames):
            obj = tkinter.PhotoImage(file=Loading.file, format=f"gif -index {i}")
            self.photoimage_objects.append(obj)

    
    def animation(self,current_frame=0):
        image = self.photoimage_objects[current_frame]
        self.gif_label.configure(image=image)
        current_frame = current_frame + 1
        if current_frame == self.frames:
            current_frame = 0 # reset the current_frame to 0 when end is reached
        self.loop = self.root.after(50, lambda: self.animation(current_frame))

    def stop_animation(self):
        self.root.after_cancel(self.loop)