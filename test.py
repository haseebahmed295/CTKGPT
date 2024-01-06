from tkinter import *
from datetime import datetime
import random
import re
from tkinter import messagebox
from tkinter.font import Font
import textwrap

root = Tk()
root.config(bg="lightblue")
root.geometry('410x600+400+100')

#ana ekran
canvas = Canvas(root, width=200, height=200,bg="white")
canvas.grid(row=0,column=0,columnspan=2)
canvas.place(x=10, y=10, width=390, height=530)

bubbles = []

class BotBubble:
    def __init__(self,master,message=""):
        self.master = master
        self.frame = Frame(master,bg="light green")
        self.i = self.master.create_window(70,490,window=self.frame )       
        Label(self.frame,text=datetime.now().strftime("%d-%m-%Y %X"),font=("Helvetica", 7),bg="light green").grid(row=0,column=0,sticky="w",padx=5) #tarih saat        
        Label(self.frame, text=textwrap.fill(message, 25), font=("Helvetica", 9),bg="light green").grid(row=1, column=0,sticky="w",padx=5,pady=3)
        root.update_idletasks()
        self.master.create_polygon(self.draw_triangle(self.i), fill="light green", outline="light green")



    def draw_triangle(self,widget):
        x1, y1, x2, y2 = self.master.bbox(widget)
        return x1, y2 - 10, x1 - 15, y2 + 10, x1, y2

def send_message():
    if bubbles:
        canvas.move(ALL, 0, -80) #balonlar arasındaki mesafe
    a = BotBubble(canvas,message=entry.get())
    bubbles.append(a)

#mesaj yazma alanı
entry = Entry(root,width=26, font=("Helvetica", 10))
entry.place(x=10, y=550, width=290, height=40)


#buton
buton = Button(root, width=10, height=2, 
relief='raised',state='active',command=send_message)
buton.config(text='GÖNDER', bg='lightblue', font='Verdana 8 bold')
buton.place(x=310, y=550)

root.mainloop()