import tkinter as tk
from tkinter import ttk
import base64
root = tk.Tk()
style = ttk.Style()

borderImageData = '''R0lGODlh...''' # Truncated for brevity, use the full string from the example
focusBorderImageData = '''R0lGODlh...''' # Truncated for brevity, use the full string from the example

# Decode the base64-encoded image data
borderImageData = base64.b64decode(borderImageData)
focusBorderImageData = base64.b64decode(focusBorderImageData)

# Create PhotoImage objects from the decoded image data
borderImage = tk.PhotoImage(data=borderImageData)
focusBorderImage = tk.PhotoImage(data=focusBorderImageData)
style.element_create("RoundedFrame", "image", borderImage,
                     ("focus", focusBorderImage), border=16, sticky="nsew")
style.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])
frame1 = ttk.Frame(style="RoundedFrame", padding=10)
text1 = tk.Text(frame1, borderwidth=0, highlightthickness=0, wrap="word",
                width=40, height=4)
text1.pack(fill="both", expand=True)
text1.bind("<FocusIn>", lambda event: frame1.state(["focus"]))
text1.bind("<FocusOut>", lambda event: frame1.state(["!focus"]))
root.configure(background="white")
frame1.pack(side="top", fill="both", expand=True, padx=20, pady=20)
root.mainloop()
