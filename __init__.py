import json
from  pathlib import Path
import threading
import customtkinter
import keyboard
from keys import KeyboardHandler
from Preferences import Prefrences, Models
from Settings import Settings
from prompt import clear_chat_history, insert_text, process_gpt_request
from CTkColorPicker import *
from CTkMenuBar import *
from bubbles import BotBubble

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.is_prompting = False
        self.keyboard_handler = KeyboardHandler(self)
        self.bubbles = []
        self.settings = Settings(self)

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
        self.entry = customtkinter.CTkEntry(self,height=40)
        # self.entry.insert(0, "Write some simple python code")# For testing
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.entry.bind('<Return>', self.prompt)

        self.main_button_1 = customtkinter.CTkButton(master=self, text = 'Prompt', 
            width=20, text_color=("gray10", "#DCE4EE") , command=self.prompt)
        self.main_button_1.grid(row=3, column=3, padx=(10, 20), pady=(20, 20), sticky="nsew")
        
        # create textbox
        self.font = customtkinter.CTkFont(size = 15)
        
        self.chat_frame = customtkinter.CTkScrollableFrame(self,)                        
        self.chat_frame.grid(row=0, column=1,columnspan=3,rowspan = 3, padx=(10, 10), pady=( 10, 0) ,sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # self.chat_frame_1 = customtkinter.CTkTextbox(self.chat_frame , height = self.chat_frame.cget('height') ,font=self.font , bg_color='gray')
        # self.chat_frame_1.grid(row=0, column=1, padx=(20, 20), pady=(20, 20) ,sticky="nsew")

        # self.hightlight = Text_highlighter(self, self.chat_frame)

        # self.menu = CTkTitleMenu(self , x_offset=100).add_cascade("Options" , fg_color = 'transparent' ,corner_radius = 4 , hover_color = '#bcbcbc')
        # op = CustomDropdownMenu(widget=self.menu)
        # op.add_option(option="Settings" ,command=self.open_settings)

        self.toplevel_window = None 
        self.load_response_thread = threading.Thread(target=self.load_setup)
        self.load_response_thread.start()

    def open_settings(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Prefrences(self)
        else:
            self.toplevel_window.focus()
 
    def confi_textcolor(self):  
        pick_color = AskColor() # open the color picker
        color = pick_color.get()
        for i in self.bubbles:
            i.frame.configure(fg_color = color)
        # self.chat_frame.configure(text_color = color)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def clear_chat(self):
        if not self.is_prompting:
            for buble in self.bubbles:
                for i in buble.text_boxes:
                    i.destroy()
                buble.frame.destroy()
            clear_chat_history()

    def load_setup(self) -> None:
        """
        Load setup from settings.json and chat_history.json files.
        """
        chat_history_file = Path('prefs/chat_history.json')

        try:
            with chat_history_file.open('r') as f:
                data = json.load(f)
            if not data:
                return
        except json.decoder.JSONDecodeError:
            print("No chat history")
            return

        for item in data:
            insert_text(self, item)

    def stream_gpt_response(self,chat):
        self.is_prompting = True
        right = BotBubble(app, app.chat_frame, "right")
        r = right.add_text_box()
        right.text_boxes[r].insert("end", f'{chat}')
        right.adjust_text_box(right.text_boxes[r])
        left = BotBubble(app, app.chat_frame, "left")
        is_coding = False
        index=left.add_text_box()
        parts = []
        for part in process_gpt_request(chat,self.settings.model):
            parts.append(part)
            if "```python" in part or "``" in part:
                if is_coding:
                    index = left.add_text_box()
                else:
                    index = left.add_code_box()

                is_coding = not is_coding
                continue
            if '`\n' in part or '`' in part:
                continue
            left.text_boxes[index].configure(state='normal')
            left.text_boxes[index].insert("end", part)
            left.text_boxes[index].configure(state='disable')
            left.adjust_text_box(left.text_boxes[index])
            # if left.text_boxes[index].is_code_block:
            #     left.colorizers[index].update()
            self.is_prompting = False
        print(parts)

    def prompt(self):
        if not self.is_prompting:
            chat = self.entry.get()
            self.entry.delete('0' ,"end") 
            self.chat_frame._parent_canvas.yview_moveto(1.0)
            self.stream_response_thread = threading.Thread(target=self.stream_gpt_response, args=(chat,))
            self.stream_response_thread.start()

if __name__ == "__main__":
    app = App()
    
    app.mainloop()
    # threading.Thread(target=keyboard.wait()).start()
            