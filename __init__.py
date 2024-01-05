import threading
import tkinter
import customtkinter
import keyboard
from colorize import Text_hightlighter
from keys import KeyboardHandler
import sv_ttk
from prompt import process_gpt_request
from CTkColorPicker import *
from CTkMenuBar import *
import pywinstyles
from options import Settings

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.is_prompting = False
        self.keyboard_handler = KeyboardHandler(self)

        self.title('GPT Tempslate')
        self.geometry(f"{1100}x{580}")
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="GPT", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = tkinter.ttk.Button(self.sidebar_frame, text = 'Clear Chat' , command=self.clear_chat)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.color_button = customtkinter.CTkButton(self.sidebar_frame, text="Select color", command=self.confi_textcolor)
        self.color_button.grid(row=4, column=0, padx=20, pady=(10, 10))

        # self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Type Here")
        self.entry.insert(0, "Write some simple python code")# For testing
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text = 'Prompt', 
            width=20, text_color=("gray10", "#DCE4EE") , command=self.prompt)
        self.main_button_1.grid(row=3, column=3, padx=(10, 20), pady=(20, 20), sticky="nsew")
        
        # create textbox
        self.font = customtkinter.CTkFont(size = 15)
        self.textbox = customtkinter.CTkTextbox(self ,font=self.font , state = 'disable' , wrap = 'word')                        
        self.textbox.grid(row=0, column=1,columnspan=3,rowspan = 3, padx=(10, 10), pady=( 10, 0) ,sticky="nsew")
        # self.textbox_1 = customtkinter.CTkTextbox(self.textbox , height = self.textbox.cget('height') ,font=font , fg_color = 'green')
        # self.textbox_1.grid(row=1, column=0, padx=(10, 10), pady=(10, 0) ,sticky="nsew")

        self.hightlight = Text_hightlighter(self, self.textbox)

        self.menu = CTkTitleMenu(self).add_cascade("Options")
        op = CustomDropdownMenu(widget=self.menu)
        op.add_option(option="Settings" ,command=self.open_settings)

        self.toplevel_window = None 

    def open_settings(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Settings(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()
 
    def confi_textcolor(self):  
        pick_color = AskColor() # open the color picker
        color = pick_color.get()
        self.textbox.configure(text_color = color)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def clear_chat(self):
        self.textbox.configure(state = 'normal')
        self.textbox.delete('1.0', 'end')
        self.textbox.configure(state = 'disable')
    

    def stream_gpt_response(self, chat):
        self.is_prompting = True
        self.textbox.configure(state='normal')
        self.textbox.insert("end",'GPT:')
        self.textbox.configure(state='disable')
        is_coding = False
        # Call the modified process_gpt_request function and handle the streamed response
        for part in process_gpt_request(chat):
            if "```" in part:
                is_coding = not is_coding
                continue

            if not is_coding:
                self.textbox.configure(state='normal') 
                self.textbox.insert("end", part) 
                self.textbox.configure(state='disable') 
                self.textbox.see("end") # Auto-scroll to the end of the text box self.textbox_1.see("end") # Auto-scroll to the end of the textbox_1 self.update_idletasks() 
            else:
                self.textbox.configure(state='normal') 
                self.textbox.insert("end", part) 
                self.hightlight.update()
                self.textbox.configure(state='disable') 
                self.textbox.see("end")
        
        self.is_prompting = False


    def prompt(self):
        if not self.is_prompting:
            chat = self.entry.get()
            self.entry.delete(0, "end")
            self.textbox.configure(state='normal')
            self.textbox.insert("end", f'\nYou: {chat}\n')
            self.textbox.configure(state='disable')
            # Start the streaming in a separate thread to keep the GUI responsive
            threading.Thread(target=self.stream_gpt_response, args=(chat,)).start()
        

if __name__ == "__main__":
    app = App()
    # sv_ttk.set_theme("light")
    # pywinstyles.apply_style(app, style = 'aero')
    app.mainloop()
    keyboard.wait()
            