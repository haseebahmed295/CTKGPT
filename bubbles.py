import customtkinter
from colorize import Text_highlighter

class BotBubble:
    def __init__(self, root, master, align="left"):
        # Initialize attributes
        self.settings = root.settings
        self.master = master
        self.row = len(root.bubbles)
        self.column = 0
        self.padx = 10
        self.pady = (10, 10)
        self.font = root.font
        self.text_boxes = []
        self.colorizers = {}
        # Create a frame with custom corner radius and foreground color
        self.frame = customtkinter.CTkFrame(master, corner_radius=5, fg_color=self.settings.bubble_color)
        if align == "left":
            # If align is left, create a label with "Response" text and grid it
            customtkinter.CTkLabel(self.frame, text="Response").grid(sticky="w", padx=10)
            # Grid the frame and add left bubble
            self.frame.grid(row=self.row, column=self.column, padx=self.padx, pady=self.pady, sticky="w")
        elif align == "right":
            # Grid the frame and add right bubble
            self.frame.grid(row=self.row, column=self.column, padx=self.padx, pady=self.pady, sticky="e")
        root.bubbles.append(self)

    def add_text_box(self):
        """
        Add a left bubble to the frame and return its index in the text_boxes list.
        """
        # Create a custom text box
        text = customtkinter.CTkTextbox(
            self.frame, 
            wrap="word",
            font=self.font,
            activate_scrollbars=False,
            fg_color='transparent'
        )
        text.is_code_block = False
        # Add the text box to the grid
        text.grid(row=len(self.text_boxes) + 1, pady=self.pady, padx=self.padx, sticky="w")
        # Append the text box to the text_boxes list
        self.text_boxes.append(text)
        # Return the index of the text box in the text_boxes list
        return len(self.text_boxes) - 1
    
    def add_code_box(self, label=""):
        """
        Add a left bubble to the frame and return its index in the text_boxes list.
        """
        code_box = customtkinter.CTkFrame(self.frame, fg_color=self.settings.code_lable, corner_radius=0)
        customtkinter.CTkLabel(code_box, text=label, height=30).grid(sticky="w", padx=20)
        text = customtkinter.CTkTextbox(
            code_box, 
            wrap="word",
            font=self.font,
            activate_scrollbars=False,
            fg_color=self.settings.code_color,
            border_spacing=10, 
            corner_radius=0
        )
        text.is_code_block = True
        code_box.grid(row=len(self.text_boxes) + 1, padx=20, pady=self.pady)
        text.grid(row=1, sticky="w")
        self.text_boxes.append(text)
        code_color = Text_highlighter(text)
        self.colorizers[len(self.text_boxes) - 1] = code_color
        return len(self.text_boxes) - 1
                
    def adjust_text_box(self, text_box):
        """
        Update the text box dimensions based on the length of the text.
        """

        text = text_box.get('1.0', 'end')
        # modified_text = text.strip('\n')
        # text_box.delete("1.0", "end")
        # text_box.insert("end", modified_text)

        total_char = len(text)
        if not text_box.cget('width')>=800:
            if text_box.is_code_block or total_char > 116:
                max_width = 800
            else:
                max_width = (total_char * self.font.cget("size")) / 2 + 15
            text_box.configure(width=max_width)

        # Update the text box height
        text_box.configure(height=0)
        while text_box._textbox.yview() != (0.0, 1.0) and not text_box._y_scrollbar.winfo_ismapped():
            text_box.configure(height=text_box.cget('height') + 25)
            # self.master._parent_canvas.yview_moveto(0.1)
        text_box._draw()