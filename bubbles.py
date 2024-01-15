import customtkinter
import math
from chlorophyll import CodeView
import pygments


class BotBubble:
    def __init__(self, root, master, align="left"):
        r = len(root.bubbles)
        c = 0
        padx=20; pady=(20, 10)
        self.m = root

        self.frame = customtkinter.CTkFrame(master , width=800 , corner_radius=5
        ,height=400,fg_color='white',
        )
        if align == "left":
            self.text = customtkinter.CTkTextbox(self.frame, wrap = "word",font=root.font,
            activate_scrollbars=False,
            
        )

            self.frame.grid(row=r, column=c,padx=padx, pady=pady ,sticky="w")
            customtkinter.CTkLabel(self.frame, text="Response").grid(column =c+1 ,sticky="w" , padx=10)
            self.text.grid(column =c+1, padx=10, pady=(5, 10))

        elif align == "right":
            self.text = customtkinter.CTkTextbox(self.frame,wrap = "word",font=root.font,
            activate_scrollbars=False
        )
            
            self.frame.grid(row=r, column=c,padx=padx, pady=pady, sticky="e")
            customtkinter.CTkLabel(self.frame, text="Prompt").grid(column =c+1 , sticky="w" , padx=10)
            self.text.grid(column =c+1 , padx=10, pady=(5, 10))

    def on_text_change(self, textbox):
        """
        Update the text box dimensions based on the length of the text.
        """

        # Get the text from the text box
        text = self.text.get('1.0', 'end')

        # Calculate the total number of characters in the text box
        total_chars = len(text)

        # Define the maximum width of the text box
        max_width = 1050

        # Calculate the size of the text based on the number of characters
        text_size = total_chars * self.m.font.actual("size")

        # Calculate the size of a single line of text
        single_line_size = self.m.font.cget('size') + self.m.font.actual("size")+5

        # Check if the text exceeds the maximum width
        if text_size > max_width:
            # Calculate the number of lines required to display the text
            num_lines = (math.ceil(text_size / max_width) + text.count('\n')) / 2

            # Adjust the width of the text box
            self.text.configure(width=max_width)

            # Adjust the height of the text box based on the number of lines
            if num_lines > 1:
                self.text.configure(height=num_lines * single_line_size)
            else:
                self.text.configure(height=single_line_size)
        else:
            # Adjust the height and width of the text box
            self.text.configure(height=single_line_size, width=text_size)

        # Remove trailing newline character from the text
        modified_text = text.rstrip('\n')

        # Clear the text box
        self.text.delete("1.0", "end")

        # Insert the modified text into the text box
        self.text.insert("end", modified_text)