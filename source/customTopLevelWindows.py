"""
Custom Top Level Windows
- askPalette (window to ask user for new palette name)
- colorChooser

David Norman Diaz Estrada - 2023
"""
import os
import webbrowser
from PIL import Image
import customtkinter


#--------------------------------------------------
# Set paths for logo and icon:
#--------------------------------------------------
if __name__ == "__main__":
    # Get the directory path of this script:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go one level up to reach the project_folder:
    project_folder = os.path.dirname(script_dir)
    # Construct the path to the assets folder:
    assets_folder = os.path.join(project_folder, "assets")
    # Set logo and icon paths:
    icon_path = os.path.join(assets_folder, "DN.ico")
    logo_path = os.path.join(assets_folder, "DN_LogoDark.png")
else:
    icon_path = r".\assets\DN.ico"
    logo_path = r".\assets\DN_LogoDark.png"

class askPalette(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Save Palette")
        self.geometry("270x130+600+600")
        self.icon_path = icon_path
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


class colorChooser(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Color")
        self.geometry("415x300+600+600")
        self.icon_path = icon_path
        self.after(200, lambda: self.iconbitmap(self.icon_path))#delay needed due to bug in customTkinter when setting icon on TopLevel Window
        self.wm_attributes('-topmost', True)  # bring the window in front of the main app
        self.deiconify()  # show the window
        self.user_input_valid=None #initialize as none
        self.chosenColor=None
        self.defaultColors = ['#d61600', '#ff4000', '#ff5d00', '#ff7c00', '#ffa200', '#fff400', '#8ee80e',
                              '#2ad587','#00b2cb','#0064b2','#002c7c','#2b0076','#5000a8','#8700aa',
                              '#000000','#2b2b2b','#565656','#818181','#acacac','#d7d7d7','#ffffff']



        #------------------------------------------------------------------------
        #Values frame
        #------------------------------------------------------------------------
        self.values_frame = customtkinter.CTkFrame(self,fg_color="transparent")
        self.values_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NEW")

        self.button_selectColorMode = customtkinter.CTkOptionMenu(self.values_frame, values=["RGB"],width=128)
        self.button_selectColorMode.grid(row=0, column=0,columnspan=2, padx=2, pady=5, sticky="EW")

        self.sliderR = customtkinter.CTkSlider(master=self.values_frame, from_=0, to=255, number_of_steps=255,
                                               width=128,orientation="horizontal",command=self.setColor)
        self.sliderR.grid(row=1, column=0, padx=2, pady=5, sticky="w")
        self.labelR = customtkinter.CTkLabel(master=self.values_frame, text="R")
        self.labelR.grid(row=1, column=1,padx=2, pady=5, sticky="ew")

        self.sliderG = customtkinter.CTkSlider(master=self.values_frame, from_=0, to=255, number_of_steps=255,
                                               width=128,orientation="horizontal",command=self.setColor)
        self.sliderG.grid(row=2, column=0, padx=2, pady=5, sticky="w")
        self.labelG = customtkinter.CTkLabel(master=self.values_frame, text="G")
        self.labelG.grid(row=2, column=1,padx=2, pady=5, sticky="ew")

        self.sliderB = customtkinter.CTkSlider(master=self.values_frame, from_=0, to=255, number_of_steps=255,
                                               width=128,orientation="horizontal",command=self.setColor)
        self.sliderB.grid(row=3, column=0, padx=2, pady=5, sticky="w")
        self.labelB = customtkinter.CTkLabel(master=self.values_frame, text="B")
        self.labelB.grid(row=3, column=1,padx=2, pady=5, sticky="ew")


        self.hexa_label = customtkinter.CTkLabel(master=self.values_frame, text="Hexa value:",width=100)
        self.hexa_label.grid(row=4, column=0,padx=2, pady=[5,0], sticky="ew")

        self.hexa_entry = customtkinter.CTkEntry(master=self.values_frame,width=100)
        self.hexa_entry.grid(row=5, column=0,padx=5, pady=0, sticky="ew")

        self.hexa_button = customtkinter.CTkButton(master=self.values_frame,text="Set",width=40,command=self.setColor_HexaEntry)
        self.hexa_button.grid(row=5,column=1,padx=5,pady=0,sticky="ew")

        self.hexa_error = customtkinter.CTkLabel(master=self.values_frame, text="",width=100,text_color="red")
        self.hexa_error.grid(row=6, column=0,padx=2, pady=0, sticky="ew")


        #------------------------------------------------------------------------
        #Colors frame
        #------------------------------------------------------------------------
        self.colors_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.colors_frame.grid(row=0, column=1, padx=10, pady=10, sticky="NEW")

        self.mainColor = customtkinter.CTkButton(master=self.colors_frame,
                                    border_width=0,
                                    width=20*7+3*7*2,
                                    text="",
                                    state="disabled",
                                    fg_color=self.defaultColors[0])

        self.mainColor.grid(row=0, column=0,columnspan=7,padx=5, pady=5, sticky="ew")
        self.drawDefaultColors()
        self.setDefaultColor(0)#initialize sliders with same value as default color


        #------------------------------------------------------------------------
        #buttons frame
        #------------------------------------------------------------------------
        self.ok_button = customtkinter.CTkButton(master=self,
                                    width=int(250/2),
                                    border_width=0,
                                    text='Ok',
                                    command=self.ok_event)

        self.ok_button.grid(row=3, column=0,padx=5, pady=3, sticky="ew")

        self.cancel_button = customtkinter.CTkButton(master=self,
                                        width=int(250/2),
                                        border_width=0,
                                        text='Cancel',
                                        command=self.cancel_event)
        self.cancel_button.grid(row=3, column=1,padx=5, pady=3, sticky="ew")


    def setColor_HexaEntry(self):
        user_input=self.hexa_entry.get()
        if len(user_input)not in range(6,8):#allows either #ffffff or ffffff
            self.hexa_error.configure(text="Invalid Hexa value")
        else:
            try:
                rgb=self.hex_to_rgb(user_input)
                #update sliders:
                self.sliderR.set(rgb[0])
                self.sliderG.set(rgb[1])
                self.sliderB.set(rgb[2])
                #update main color:
                self.setColor()
                #ensure no error message is shown:
                self.hexa_error.configure(text="")
            except:
                self.hexa_error.configure(text="Invalid Hexa value")


    def hex_to_rgb(self,hex_color):
        if hex_color[0] == '#':
            hex_color = hex_color[1:]  # Remove the leading '#' if present
        return [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]

    def rgb_to_hexa(self, rgb):
        return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))

    def setDefaultColor(self,index):
        hex_color=self.defaultColors[index]
        self.mainColor.configure(fg_color=hex_color)
        rgb=self.hex_to_rgb(hex_color)
        self.sliderR.set(rgb[0])
        self.sliderG.set(rgb[1])
        self.sliderB.set(rgb[2])


    def setColor(self,*args):
        #print(args)
        r = self.sliderR.get()
        g = self.sliderG.get()
        b = self.sliderB.get()
        rgb=[r,g,b]
        hexColor=self.rgb_to_hexa(rgb)
        self.mainColor.configure(fg_color=hexColor)

    def drawDefaultColors(self):
        row=1
        column=0
        for i in range(len(self.defaultColors)):
            self.defaultColor=customtkinter.CTkButton(master=self.colors_frame,
                                    width=20,
                                    height=20,
                                    corner_radius=0,
                                    border_width=0,
                                    text="",
                                    fg_color=self.defaultColors[i],
                                    command=lambda index=i: self.setDefaultColor(index))
            self.defaultColor.grid(row=row, column=column, padx=3, pady=3, sticky="ew")
            column+=1
            if column>6:
                column=0
                row+=1

    def ok_event(self):
        self.chosenColor=self.mainColor.cget("fg_color")
        print("Chosen color:",self.chosenColor)
        self.grab_release()
        self.destroy()

    def on_closing(self):
        self.grab_release()
        self.destroy()

    def cancel_event(self):
        self.grab_release()
        self.destroy()

    def get_color(self):
        self.master.wait_window(self)
        if self.chosenColor!=None:
            hexa=self.chosenColor
            RGB=self.hex_to_rgb(hexa)
            return [RGB,hexa]
        else: return None


class welcomeWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version="v1.0.0"#app version
        self.title("Welcome!")
        self.geometry("530x250+350+400")
        self.icon_path=icon_path
        self.logo_path=logo_path

        self.after(200, lambda: self.iconbitmap(self.icon_path))#delay needed due to bug in customTkinter when setting icon on TopLevel Window
        self.wm_attributes('-topmost', True)  # bring the window in front of the main app
        self.deiconify()  # show the window

        pil_img = Image.open(self.logo_path)
        self.img = customtkinter.CTkImage(dark_image=pil_img, size=(int(pil_img.size[0]/3), int(pil_img.size[1]/3)))
        self.img_label = customtkinter.CTkLabel(self, image=self.img, text="")
        self.img_label.grid(row=0, column=0, columnspan=2,padx=10, pady=[10,20], sticky="EW")


        self.text_frame = customtkinter.CTkFrame(master=self,fg_color="transparent")
        self.text_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky="NEW")
        text="2023 - Made by DAVID NORMAN DIAZ ESTRADA\n"+"DN Image Editor | "+self.version
        self.appInfo_label = customtkinter.CTkLabel(self.text_frame, text=text,justify="center",font=("Roboto",15),cursor="hand2")
        self.appInfo_label.pack()
        self.appInfo_label.bind("<Button-1>", lambda event: self.open_link_linkedin())# Configure the label to act as a hyperlink

        self.github_button = customtkinter.CTkButton(master=self, text="GitHub", font=("Roboto", 15,"bold"),
                                                    cursor="hand2",fg_color="#333333",hover_color="#00cd00",
                                                    corner_radius=5,width=70,command=self.open_link_github)
        self.github_button.grid(row=2, column=0, padx=2, pady=2,sticky="e")

        self.linkedin_button = customtkinter.CTkButton(master=self, text="LinkedIn", font=("Roboto", 15,"bold"),
                                                    cursor="hand2",fg_color="#333333",hover_color="#00cd00",
                                                    corner_radius=5,width=70,command=self.open_link_linkedin)
        self.linkedin_button.grid(row=2, column=1, padx=2, pady=2,sticky="w")

    def open_link_linkedin(self):
        webbrowser.open("https://www.linkedin.com/in/dnde7")

    def open_link_github(self):
        webbrowser.open("https://github.com/DavidDZ7/DN_image_editor")

    def on_closing(self):
        self.grab_release()
        self.destroy()


#--------------------------------------------------
# Debug mode:
#--------------------------------------------------
if __name__ == "__main__":
    print("-" * 20)
    print("Debug mode")
    print("-" * 20)

    app = welcomeWindow()
    app.mainloop()

