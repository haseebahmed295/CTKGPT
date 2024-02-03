import json
from  pathlib import Path
import threading
import time
import customtkinter
from animations import Loading , settings_img , trash_img , send_img
from keys import KeyboardHandler
from Preferences import Prefrences, Models
from Settings import Settings
from responses import check_part, clear_chat_history, insert_text, process_gpt_request
from CTkColorPicker import *
from CTkMenuBar import *
from bubbles import BotBubble
from PIL import Image
import pywinstyles

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.is_prompting = False
        self.keyboard_handler = KeyboardHandler(self)
        self.settings = Settings(self)
        self.set_scaling_event(self.settings.scaling)

        self.title('GPT')
        
        self.geometry(f"{1100}x{580}")
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)


        self.clear_chat_button = customtkinter.CTkButton(self.sidebar_frame, width=20,text = '' ,fg_color='transparent', command=self.clear_chat , image=trash_img)
        self.clear_chat_button.grid(row=1, column=0, sticky = 'w',padx=5, pady=(10, 20))
        # self.textolor_button = customtkinter.CTkButton(self.sidebar_frame,width=20, text="",fg_color='transparent',command=self.confi_textcolor, image=send_img)
        # self.textolor_button.grid(row=4, column=0, sticky = 'w',padx=10, pady=(10, 20))

        self.option = customtkinter.CTkButton(self.sidebar_frame, text="",fg_color='transparent'
                                              ,image=settings_img,width=20,command=self.open_settings)
        self.option.grid(row=8, column=0,
                         sticky = 'w',padx=5, pady=(10, 20)
                         )
        # pywinstyles.set_opacity(self.option,value=0.1, color="#000001")

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self,height=45,border_width=1,corner_radius=15, placeholder_text="Type Here",)
        self.entry.grid(row=3, column=1, columnspan=2, padx=(10, 10), pady=(15, 15), sticky="nswe")
        

        self.main_button_1 = customtkinter.CTkButton(self.entry, text = '', command=self.prompt ,width=20, fg_color='transparent',image=send_img)
        self.main_button_1.place(relx=1.0, x= -10, rely=0.8, anchor="se")
        
        # create font
        self.font = customtkinter.CTkFont(size = 15)
        
        # self.attributes('-alpha', 0.9)
        self.chat_frame = customtkinter.CTkScrollableFrame(self , fg_color=self.settings.frame_color)                        
        self.chat_frame.grid(row=0, column=1,columnspan=3,rowspan = 3, padx=(10, 10), pady=( 10, 0) ,sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)
        

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
 
    def set_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    def confi_textcolor(self):  
        pick_color = AskColor()
        color = pick_color.get()
        for i in BotBubble.bubbles:
            i.frame.configure(fg_color = color)

    def clear_chat(self):
        if not self.is_prompting:
            for buble in BotBubble.bubbles:
                for i in buble.text_boxes:
                    i.destroy()
                buble.frame.destroy()
            clear_chat_history()

    def load_setup(self) -> None:
        """
        Load setup from settings.json and chat_history.json files.
        """
        self.is_prompting = True
        chat_history_file_path = Path('prefs/chat_history.json')

        try:
            with chat_history_file_path.open('r') as file:
                data = json.load(file)
            if not data:
                self.is_prompting = False
                return
        except json.decoder.JSONDecodeError:
            self.is_prompting = False
            return

        loading_animation = self.loading_animation()
        next(loading_animation)
        for item in data:
            insert_text(self, item)
        next(loading_animation, None)
        self.is_prompting = False

    def loading_animation(self):
        self.dummy = customtkinter.CTkFrame(self)                        
        self.dummy.grid(row=0, column=1,columnspan=3,rowspan = 3, padx=(10, 10), pady=( 10, 0) ,sticky="nsew")
        app.chat_frame.lower(app.dummy)
        L = Loading(app, app.dummy)
        L.start_thread()
        yield
        L.stop_thread()
        app.chat_frame.lift(app.dummy)
        del L
        del self.dummy
        
    def stream_gpt_response(self,chat):
        self.is_prompting = True
        right = BotBubble(app, app.chat_frame, "right")
        r = right.add_text_box()
        right.text_boxes[r].insert("end", f'{chat}')
        right.adjust_text_box(right.text_boxes[r])
        left = BotBubble(app, app.chat_frame, "left")
        is_coding = False
        index=left.add_text_box()
        for part in process_gpt_request(chat,self.settings.model):
            time.sleep(0.05)
            if "``" in part or '```python' in part:
                if is_coding:
                    index = left.add_text_box()
                else:
                    index = left.add_code_box()
                is_coding = not is_coding
                continue
            part = check_part(part , is_coding)
            left.text_boxes[index].configure(state='normal')
            left.text_boxes[index].insert("end", part)
            left.text_boxes[index].configure(state='disable')
            left.adjust_text_box(left.text_boxes[index] , code=True if is_coding else False)
        for keys , values in BotBubble.colorizers.items():
            values.update()
            self.is_prompting = False

    def prompt(self , event = None):
        if not self.is_prompting:
            chat = self.entry.get()
            self.entry.delete('0' ,"end") 
            self.chat_frame._parent_canvas.yview_moveto(1.0)
            self.stream_response_thread = threading.Thread(target=self.stream_gpt_response, args=(chat,))
            self.stream_response_thread.start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
            