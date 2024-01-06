from tkinter import *
from datetime import datetime
import random
import re
from tkinter import messagebox
from tkinter.font import Font
import textwrap
import customtkinter

root = customtkinter.CTk()
# root.config(bg="lightblue")
root.geometry('410x600+400+100')

#ana ekran
canvas = customtkinter.CTkCanvas(root , bg="white")
canvas.grid(row=0,column=0,columnspan=2 ,padx=(10, 10), pady=( 10, 0) ,sticky="nsew")
canvas.place(x=10, y=10, width=390, height=530)

bubbles = []

class BotBubble:
    def __init__(self,master,message=""):
        self.master = master
        self.frame = customtkinter.CTkFrame(master , bg_color="transparent", fg_color="light green")
        self.i = self.master.create_window(70,490,window=self.frame , anchor="w")       
        customtkinter.CTkLabel(self.frame,text=datetime.now().strftime("%d-%m-%Y %X"),bg_color="light green").grid(row=0,column=0,sticky="w",padx=5) #tarih saat        
        customtkinter.CTkLabel(self.frame, text=textwrap.fill(message, 25),bg_color="light green").grid(row=1, column=0,sticky="w",padx=5,pady=3)
        root.update_idletasks()



    def draw_triangle(self,widget):
        x1, y1, x2, y2 = self.master.bbox(widget)
        return x1, y2 - 10, x1 - 15, y2 + 10, x1, y2

def send_message():
    if bubbles:
        canvas.move(ALL, 0, -80) #balonlar arasındaki mesafe
    a = BotBubble(canvas,message=entry.get())
    bubbles.append(a)

#mesaj yazma alanı
entry = customtkinter.CTkEntry(root,width=26, font=("Helvetica", 10))
entry.place(x=10, y=550)


#buton
buton = customtkinter.CTkButton(root,command=send_message , text='GÖNDER', bg_color='lightblue')
buton.grid(row=5, column=3, padx=(10, 20), pady=(20, 20), sticky="nsew")

root.mainloop()