import tkinter as tk

class ExpandoText(tk.Text):
    def insert(self, *args, **kwargs):
        result = tk.Text.insert(self, *args, **kwargs)
        self.reset_height()
        return result

    def reset_height(self):
        height = self.tk.call((self._w, "count", "-update", "-displaylines", "1.0", "end"))
        self.configure(height=height)
root = tk.Tk()
text = ExpandoText(root, width=20, wrap="word")
text.pack(fill="both", expand=True)

root.update_idletasks()
text.insert("1.0", "This is a line of text that will initially be wrapped.")

root.after(5000, text.insert, "end", "This is more text")

root.mainloop()
