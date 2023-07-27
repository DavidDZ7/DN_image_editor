"""
Custom Top Level Windows
- askPalette: window to ask user for new palette name

David Norman Diaz Estrada - 2023
"""
import customtkinter

class askPalette(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Save Palette")
        self.geometry("270x130+600+600")
        self.icon_path = r".\assets\DN.ico"
        self.after(200, lambda: self.iconbitmap(self.icon_path))#delay needed due to bug in customTkinter when setting icon on TopLevel Window
        self.wm_attributes('-topmost', True)  # bring the window in front of the main app
        self.deiconify()  # show the window
        self.user_input_valid=None #initialize as none

        self.label = customtkinter.CTkLabel(master=self, text="Enter name for new palette:")
        self.label.grid(row=0, column=0,columnspan=2,padx=5, pady=3, sticky="ew")

        self.entry = customtkinter.CTkEntry(self)
        self.entry.grid(row=1, column=0,columnspan=2,padx=5, pady=3, sticky="ew")

        self.ok_button = customtkinter.CTkButton(master=self,
                                    width=int(250/2),
                                    border_width=0,
                                    text='Ok',
                                    command=self.ok_event)

        self.ok_button.grid(row=2, column=0,padx=5, pady=3, sticky="ew")

        self.cancel_button = customtkinter.CTkButton(master=self,
                                        width=int(250/2),
                                        border_width=0,
                                        text='Cancel',
                                        command=self.cancel_event)
        self.cancel_button.grid(row=2, column=1,padx=5, pady=3, sticky="ew")

        self.errorMessage = customtkinter.CTkLabel(master=self, text="",text_color="red")
        self.errorMessage.grid(row=3, column=0, columnspan=2, padx=0, pady=0, sticky="ew")


    def ok_event(self):
        current_entry=self.entry.get()
        #print("Current Entry:",current_entry)
        #print(len(current_entry))
        if len(current_entry) not in range(1,14):
            if len(current_entry)>13: errorMessage="Name too long"
            else: errorMessage="Error: empty name"
            self.errorMessage.configure(text=errorMessage)

        else:
            self.user_input_valid = current_entry
            self.grab_release()
            self.destroy()

    def on_closing(self):
        self.grab_release()
        self.destroy()

    def cancel_event(self):
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self.user_input_valid


