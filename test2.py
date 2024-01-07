import customtkinter


class SettingsView(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        # sourcery skip: merge-list-append, move-assign-in-block
        super().__init__( *args, **kwargs)

        # As each frame is created, it is added to this list
        widget_list = []

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.grid(row=0, column=0, padx=20, pady=20)
        widget_list.append(self.label)

        # === Create widgets ===
        # Keybind Changer
        self.frame_1 = customtkinter.CTkFrame(master=self)
        self.frame_1.columnconfigure(0, weight=1)  # lbl label
        self.frame_1.columnconfigure(1, weight=0)  # lbl keybind
        self.frame_1.columnconfigure(2, weight=0)  # btn set
        self.label_1 = customtkinter.CTkLabel(master=self.frame_1, text="Bot start/stop keybind: ")
        self.label_1.grid(row=1, column=0, padx=20, pady=20)
        self.entry_keybinds = customtkinter.CTkLabel(master=self.frame_1,)
        self.entry_keybinds.grid(row=1, column=1, padx=20, pady=20)
        self.button_1 = customtkinter.CTkButton(master=self.frame_1, text="Hello", command=self.__modify_keybind)
        self.button_1.grid(row=1, column=2, padx=20, pady=20)
        widget_list.append(self.frame_1)

        self.frame_2 = customtkinter.CTkFrame(master=self)
        self.frame_2.columnconfigure(0, weight=1)  # lbl label
        self.frame_2.columnconfigure(1, weight=0)  # lbl keybind
        self.frame_2.columnconfigure(2, weight=0)  # btn set
        self.label_2 = customtkinter.CTkLabel(master=self.frame_2, text="Bot start/stop keybind: ")
        self.label_2.grid(row=2, column=0, padx=20, pady=20)
        self.entr = customtkinter.CTkLabel(master=self.frame_2)
        self.entr.grid(row=2, column=1, padx=20, pady=20)
        self.btn = customtkinter.CTkButton(master=self.frame_2, text="Hello", command=self.__modify_keybind)
        self.btn.grid(row=2, column=2, padx=20, pady=20)
        widget_list.append(self.frame_2)







        # Keybind Note
        self.note = (
            "Use the `EDIT` button to unlock keyboard input. Press `ESC` to clear input. The new keybind will not be saved until you click the Save button &"
            " restart OSBC."
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
        self.btn_save = customtkinter.CTkButton(master=self, text="Save")
        self.btn_save.grid(row=self.num_of_widgets + 2, column=0, columnspan=2, pady=20, padx=20)

    def __modify_keybind(self):
        print("Modify keybind")
        pass

    def on_closing(self):
        self.stop_keyboard_listener()
        self.parent.destroy()

app = SettingsView()
    # sv_ttk.set_theme("light")
    # pywinstyles.apply_style(app, style = 'aero')
app.mainloop()