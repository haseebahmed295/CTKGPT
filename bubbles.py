import customtkinter
from colorize import Text_highlighter

class BotBubble:
    spacer = None
    bubbles = []
    colorizers = {}
    code_lable = None

    def __init__(self, root, master, align="left"):
        # Initialize attributes
        self.settings = root.settings
        self.master = master
        self.row = len(BotBubble.bubbles)
        self.column = 0
        self.padx = 10
        self.pady = (10, 10)
        self.font = root.font
        self.text_boxes = []
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
        BotBubble.bubbles.append(self)

        if not BotBubble.spacer:
            BotBubble.spacer = customtkinter.CTkFrame(master,height=80,fg_color='transparent')
        BotBubble.spacer.grid(row=self.row+1)


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
            fg_color='transparent',
            height=0
        )
        text.is_code_block = False
        # Add the text box to the grid
        text.grid(row=len(self.text_boxes) + 1, pady=self.pady, padx=self.padx, sticky="w")
        # Append the text box to the text_boxes list
        self.text_boxes.append(text)
        # Return the index of the text box in the text_boxes list
        return len(self.text_boxes) - 1
    
    def add_code_box(self):
        """
        Add a left bubble to the frame and return its index in the text_boxes list.
        """
        text = customtkinter.CTkTextbox(
            self.frame,
            wrap="word",
            font=self.font,
            activate_scrollbars=False,
            fg_color=self.settings.code_color,
            height=0,
            border_spacing=10, 
        )
        text.is_code_block = True
        text.grid(row=len(self.text_boxes) + 1, padx=20, pady=self.pady)
        self.text_boxes.append(text)
        code_color = Text_highlighter(text)
        BotBubble.colorizers[len(self.text_boxes) - 1] = code_color
        return len(self.text_boxes) - 1
                
    def format_text(self, text_box):
        text = text_box.get('1.0', 'end')
        modified_text = text.strip('\n')
        text_box.delete("1.0", "end")
        text_box.insert("end", modified_text)

    def adjust_text_box(self, text_box , code = False):
        """
        Update the text box dimensions based on the length of the text.
        """
        text = text_box.get('1.0', 'end')
        if text.endswith('\n') or text.startswith('\n'):
            self.format_text(text_box)

        total_char = len(text)
        if not text_box.cget('width')>=800:
            if text_box.is_code_block or total_char > 116:
                max_width = 800
            else:
                max_width = (total_char * self.font.cget("size")) / 2 + 15
            text_box.configure(width=max_width)

        while text_box._textbox.yview() != (0.0, 1.0) and not text_box._y_scrollbar.winfo_ismapped():
            text_box.configure(height=text_box.cget('height') + 25)
            self.master._parent_canvas.yview_moveto(1.0)
        if code:
            text_box._draw()