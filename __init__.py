import json
import textwrap
import threading

import customtkinter
import keyboard
from colorize import Text_hightlighter
from keys import KeyboardHandler
import sv_ttk
from prompt import clear_chat_history, process_gpt_request
from CTkColorPicker import *
from CTkMenuBar import *
import pywinstyles
from options import Settings , Models


customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
# customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class BotBubble:
    def __init__(self, root, master, align="left"):
        self.frame = customtkinter.CTkFrame(master, fg_color="lightgreen")
        padx=20; pady=(20, 10)
        self.m = root
        if align == "left":
            self.text = customtkinter.CTkTextbox(
            self.frame, 
            wrap = "word",
            font=root.font,
            # width=1200,
            bg_color="lightgreen",
        )
            r = len(root.bubbles)
            c = 0
            # columnspan = 4
            master.grid_columnconfigure(c, weight=1)
            self.frame.grid(row=r ,column=c,padx=padx, pady=pady , sticky="w")
            customtkinter.CTkLabel(self.frame, text="Response").grid(row=r, column=c , sticky="w")
            self.text.grid(row=r+1, column=c, sticky="w")
        elif align == "right":
            self.text = customtkinter.CTkTextbox(
            self.frame, 
            wrap = "word",
            font=root.font,
            height=30,
            bg_color="lightgreen",
        )
            r = len(root.bubbles)
            c = 0
            # master.grid_columnconfigure(c, weight=1)
            self.frame.grid(row=r, column=c,padx=padx, pady=pady, sticky="e")
            customtkinter.CTkLabel(self.frame, text="Prompt").grid(row=r, column=c, sticky="w")
            self.text.grid(row=r+1, column=c, sticky="e")

    def on_text_change(self, event = None):
        # Get the current content of the textbox
        pass

  

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.is_prompting = False
        self.keyboard_handler = KeyboardHandler(self)
        self.Model = None
        self.Provider = None
        self.bubbles = []
        with open('settings.json', 'r') as f:
                data = json.load(f)
        for key , value in data.items():
            if key == "Model":
                self.Model = value
            elif key == "Provider":
                self.Provider = value

        self.title('GPT')
        self.geometry(f"{1100}x{580}")
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Chat App", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text = 'Clear Chat' , command=self.clear_chat)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.textolor_button = customtkinter.CTkButton(self.sidebar_frame, text="Select color", command=self.confi_textcolor)
        self.textolor_button.grid(row=4, column=0, padx=20, pady=(10, 10))

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
        self.option = customtkinter.CTkButton(self.sidebar_frame, text="Settings",
                                                               command=self.open_settings)
        self.option.grid(row=9, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkTextbox(self,height=40)
        # self.entry.insert(0, "Write some simple python code")# For testing
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text = 'Prompt', 
            width=20, text_color=("gray10", "#DCE4EE") , command=self.prompt)
        self.main_button_1.grid(row=3, column=3, padx=(10, 20), pady=(20, 20), sticky="nsew")
        
        # create textbox
        self.font = customtkinter.CTkFont(size = 30)

        self.textbox = customtkinter.CTkScrollableFrame(self,)                        
        self.textbox.grid(row=0, column=1,columnspan=3,rowspan = 3, padx=(10, 10), pady=( 10, 0) ,sticky="nsew")
        
        # self.textbox_1 = customtkinter.CTkTextbox(self.textbox , height = self.textbox.cget('height') ,font=self.font , bg_color='gray')
        # self.textbox_1.grid(row=0, column=1, padx=(20, 20), pady=(20, 20) ,sticky="nsew")

        # self.hightlight = Text_hightlighter(self, self.textbox)

        # self.menu = CTkTitleMenu(self , x_offset=100).add_cascade("Options" , fg_color = 'transparent' ,corner_radius = 4 , hover_color = '#bcbcbc')
        # op = CustomDropdownMenu(widget=self.menu)
        # op.add_option(option="Settings" ,command=self.open_settings)

        self.toplevel_window = None 
        # self.load_response_thread = threading.Thread(target=self.load_setup)
        # self.load_response_thread.start()


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
        if not self.is_prompting:
            self.textbox.configure(state='normal')
            self.textbox.delete('1.0', 'end')
            self.textbox.configure(state='disable')
            clear_chat_history()

    def load_setup(self):

        try:
            with open('settings.json', 'r') as f:
                data = json.load(f)
            for key , value in data.items():
                if key == "Model":
                    self.Model = value
                elif key == "Provider":
                    self.Provider = value
        except json.decoder.JSONDecodeError:
            print("No Settings Found") 
        try:
            with open('chat_history.json', 'r') as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError:
            print("No chat history")
            return
        self.textbox.configure(state='normal')
        code_index =[]
        for item in data:
            self.textbox.insert("end", f'You: {item["prompt"]}\n' , 'you') 
            self.textbox.insert("end", f'AI: ' , 'gpt') 
            is_coding = False
            end_index = None
            start_index = None


            for part in item["response"]:
                if "```python" in part or "``" in part:
                    if is_coding:
                        end_index = self.textbox.index("end")
                    else:   
                        start_index = self.textbox.index("insert")
                    is_coding = not is_coding
                    continue
                if '`\n' in part:
                    part = part.replace("`\n","\n")


                if is_coding:
                    self.hightlight.insert_code(self.textbox,part)
                else:
                    self.textbox.insert("end", part) 

                if end_index and start_index:
                    code_index.append((start_index,end_index))
                    end_index = None
                    start_index = None
            self.textbox.insert("end", '\n')
        self.hightlight.update(code_index) 
        self.textbox.configure(state='disable')

    
        
    
    def stream_gpt_response(self, chat , bubble):
        self.is_prompting = True
        hightlight = Text_hightlighter(self, bubble.text)
        code_index = []
        is_coding = False
        end_index = None
        start_index = None
        a = True
        # Call the modified process_gpt_request function and handle the streamed response
        for part in process_gpt_request(chat,self.Model,self.Provider):
            if "```python" in part or "``" in part:
                if is_coding:
                    end_index = bubble.text.index("end")
                else:
                    start_index = bubble.text.index("insert")
                is_coding = not is_coding
                continue
            if '`\n' in part:
                part = part.replace("`\n","\n")

            bubble.text.configure(state='normal')
            if is_coding:
                hightlight.insert_code(bubble.text, part)
            else:
                bubble.text.insert("end", part)

            if end_index and start_index:
                code_index.append((start_index, end_index))
                end_index = None
                start_index = None
                hightlight.update(code_index)
            
            bubble.text.configure(state='disable')
            bubble.text.see("end")
            
        bubble.on_text_change()
        self.is_prompting = False

    def prompt(self):
        if not self.is_prompting:
            chat = self.entry.get("0.0", "end")
            # self.entry.delete(0, "end")
            self.entry.delete("0.0", "end") 

            right = BotBubble(self,self.textbox,"right")
            self.bubbles.append(right)
            right.text.insert("end", f'You: {chat}\n') 


            left = BotBubble(self,self.textbox,"left")
            self.bubbles.append(left)
            left.text.insert("end", f'{self.Model}: ')

            self.stream_response_thread = threading.Thread(target=self.stream_gpt_response, args=(chat,left))
            self.stream_response_thread.start()

if __name__ == "__main__":
    app = App()
    # sv_ttk.set_theme("light")
    # pywinstyles.apply_style(app, style = 'aero')
    app.mainloop()
    keyboard.wait()
            