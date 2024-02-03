import tkinter as tk
from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel, CTkFrame , CTkScrollbar , CTkTextbox
import g4f

class ChatApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("Chat App")
        self.geometry("600x400")

        # Initialize variables
        self.conversation = []
        
        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        frame = CTkFrame(master=self)
        frame.pack(side="top", fill="both", expand=True)

        scrollbar = CTkScrollbar(frame, orient="vertical", command=self.scrollbar_command)
        scrollable_area = CTkTextbox(frame, yscrollcommand=scrollbar.set, height=380)
        scrollbar.pack(side="right", fill="y")
        scrollable_area.pack(side="left", fill="both", expand=True)

        entry = CTkEntry(self, width=500)
        entry.pack(side="bottom", pady=(0, 10))

        send_button = CTkButton(self, text="Send", command=lambda: self.send_message(entry.get()))
        send_button.pack(side="bottom", padx=(10, 0), pady=(0, 10))

        # Add initial conversation history
        for line in self.conversation:
            scrollable_area.insert('end', line+"\n")

    def send_message(self, message):
        self.conversation.append(message)
        response = g4f.generate_response(message)
        self.conversation.append(response)

        scrollable_area = self.winfo_children()[1].winfo_children()[0]
        scrollable_area.insert('end', message+"\n")
        scrollable_area.insert('end', response+"\n")
        scrollbar = scrollable_area.winfo_children()[1]
        scrollbar.config(state='normal')
        scrollbar.set(scrollbar.get(), '1.0', 'end')
        scrollbar.config(state='disabled')

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()