import json
import customtkinter

import g4f
Models = {
        # gpt-3.5
        'gpt-3.5-turbo'          : g4f.models.gpt_35_turbo,
        'gpt-3.5-turbo-0613'     : g4f.models.gpt_35_turbo_0613,
        'gpt-3.5-turbo-16k'      : g4f.models.gpt_35_turbo_16k,
        'gpt-3.5-long':  g4f.models.gpt_35_long,

        'gpt-4'          :  g4f.models.gpt_4,
        'gpt-4-turbo'    :  g4f.models.gpt_4_turbo,


        'llama2-7b' :  g4f.models.llama2_7b,
        'llama2-13b':  g4f.models.llama2_13b,
        'llama2-70b':  g4f.models.llama2_70b,
        
        # Mistral
        'mixtral-8x7b':  g4f.models.mixtral_8x7b,
        'mistral-7b':  g4f.models.mistral_7b,
        'openchat_3.5':  g4f.models.openchat_35,
    
    
    }

class Prefrences(customtkinter.CTkToplevel):
    def __init__(self, master , *args, **kwargs):
        # sourcery skip: merge-list-append, move-assign-in-block
        super().__init__(master,*args, **kwargs)
        self.title('Prefrences')
        self.master = master
        # As each frame is created, it is added to this list
        widget_list = []

        self.label = customtkinter.CTkLabel(self, text="Prefrences" , font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)
        widget_list.append(self.label)

        # === Create widgets ===
        # Keybind Changer
        self.frame_1 = customtkinter.CTkFrame(master=self)
        self.frame_1.columnconfigure(0, weight=1)  # lbl label
        self.frame_1.columnconfigure(1, weight=0)  # lbl keybind
        self.frame_1.columnconfigure(2, weight=0)  # btn set
        self.label_1 = customtkinter.CTkLabel(master=self.frame_1, text="Chat Model: ")
        self.label_1.grid(row=1, column=0, padx=20, pady=20)
        self.entry_keybinds = customtkinter.CTkLabel(master=self.frame_1, text="")
        self.entry_keybinds.grid(row=1, column=1, padx=20, pady=20)
        self.option_1 = customtkinter.CTkOptionMenu(self.frame_1, values=list(Models.keys()), )
        self.option_1.grid(row=1, column=2, padx=20, pady=20)
        widget_list.append(self.frame_1)

        self.option_1.set(self.master.settings.model)

        # Keybind Note
        self.note = (
            "To apply and save changes click on save"
        )
        self.lbl_keybind_note = customtkinter.CTkLabel(master=self, text=self.note)
        self.lbl_keybind_note.bind(
            "<Configure>",
            lambda e: self.lbl_keybind_note.configure(wraplength=self.lbl_keybind_note.winfo_width() - 10),
        )
        widget_list.append(self.lbl_keybind_note)

        # Grid layout
        self.num_of_widgets = len(widget_list)
        for i in range(self.num_of_widgets):
            self.rowconfigure(i, weight=0)
        self.rowconfigure(self.num_of_widgets + 1, weight=1)  # Spacing between Save btn and options
        self.rowconfigure(self.num_of_widgets + 2, weight=0)  # Save btn
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Add widgets to grid
        for i in range(self.num_of_widgets):
            widget_list[i].grid(row=i, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)

        # Save button
        self.btn_save = customtkinter.CTkButton(master=self, text="Save" , command=self.save_settings)
        self.btn_save.grid(row=self.num_of_widgets + 2, column=0, columnspan=2, pady=20, padx=20)

        self.focus()
     
    
    def save_settings(self):
            # A function to save the value of the model
            settings_file_path = 'prefs/settings.json'
            
            # Load the current settings
            with open(settings_file_path, 'r') as file:
                data = json.load(file)
            
            # Update the settings (assuming self.model_value contains the new model value)
            data['Model'] = self.model_value  # Replace with the actual attribute that stores the model value
            
            # Save the updated settings
            with open(settings_file_path, 'w') as file:
                json.dump(data, file, indent=4)



