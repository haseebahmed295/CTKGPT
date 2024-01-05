import tkinter as tk

root = tk.Tk()

# Create parent text widget
parent_text = tk.Text(root, height=5, width=52)

# Create subtext label widget
subtext_label = tk.Label(root, text="Subtext")
# Position the parent text widget
parent_text.place(relx=0.5, rely=0.5, anchor='center')

# Position the subtext label widget relative to the parent text widget
subtext_label.place(in_=parent_text, relx=0.5, rely=0.5, anchor='center')
root.mainloop()
