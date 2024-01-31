import tkinter as tk

root = tk.Tk()

# Configure the grid to expand equally
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# Create a widget, for example a Label
label = tk.Label(root, text="I am centered!")
# Place the widget in the center cell of the grid
label.grid(row=1, column=1)

# Run the main loop
root.mainloop()