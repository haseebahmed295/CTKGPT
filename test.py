from tkinter import ALL
import textwrap
import customtkinter

root = customtkinter.CTk()
root.geometry('800x600')

frame = customtkinter.CTkScrollableFrame(root ,height=600,width = 800, bg_color='white', fg_color="white")
frame.grid(row=0, column=0 ,rowspan=2)  # Fill and expand the frame

canvas = customtkinter.CTkCanvas(frame ,height=600 , width = 800)
canvas.grid(row=1, column=0)  # Fill and expand the canvas

bubbles = []


class BotBubble:
    def __init__(self, master, message=""):
        self.master = master
        self.frame = customtkinter.CTkFrame(master, bg_color="transparent", fg_color="light green")
        self.i = self.master.create_window(70, 490, window=self.frame , anchor="nw")
        master.configure(height = int(master.cget("height")) + 300)
        self.scroll_height = master.winfo_height()  
        self.frame.place(x=50, y=self.scroll_height-300)
        customtkinter.CTkLabel(self.frame, text='       Hello          ', bg_color="light green").grid(row=0, column=0, sticky="w", padx=5)  # tarih saat
        self.c =customtkinter.CTkTextbox(self.frame, activate_scrollbars=False, bg_color="light green" )
        self.c.grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.c.insert('end' ,textwrap.fill(message, 25) , )
        self.c.bind("<Configure>", self.update_height)
        root.update_idletasks()

    def update_height(self, event):

        num_lines = len(self.c.get(1.0, "end").split("\n"))
        line_height = self.c.cget("font").metrics("linespace")  

        self.c.configure(height=num_lines*line_height)
        self.frame.configure(height=num_lines*line_height)

        

def send_message():

    if bubbles:
        canvas.move(ALL, 0, -80)  # balloons distance
    a = BotBubble(canvas, message=entry.get())
    bubbles.append(a)
    print(canvas.cget("height"))
    root.update_idletasks()
    canvas.yview_moveto(1)


# message entry area
entry = customtkinter.CTkEntry(root, width=26, font=("Helvetica", 10))
entry.place(x=10, y=550)

# button
button = customtkinter.CTkButton(root, command=send_message, text='GÖNDER', bg_color='lightblue')
button.grid(row=1, column=1, sticky="e")  # Place the button at the bottom

root.mainloop()