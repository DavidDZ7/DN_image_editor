"""
Python GUI for DN Image Editor

Filter 1: pixelate with triangles
Filter 2: Color mapping

David Norman Diaz Estrada - 2023
"""
import webbrowser
import os
import json
#external libraries:
import cv2
import customtkinter
import tkinter
from customtkinter import filedialog
from tkinter import colorchooser
from PIL import Image #we use PIL to open jpg,png images.
#custom libraries:
import source.filter_triangle as filter_triangle
import source.colorMapping as colorMapping
import source.LinearGradient as LinearGradient
import source.Kmeans_tones as Kmeans_tones
import source.customTopLevelWindows as customTopLevelWindows

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #------------------------------------------------------------------------
        #Global variables
        #------------------------------------------------------------------------
        self.title("DN Image Editor")
        self.geometry("1250x1000+0+0")# Set the width,height of the window, and x and y coordinates
        self.iconbitmap("assets/DN.ico")# Set DN image editor icon
        customtkinter.set_appearance_mode("dark")#sets the window/App in dark mode
        self.toplevel_window = None #initialize as None

        self.input_image_path = "assets\oslo2021.png"  # global input_image_path
        self.new_output_image=None# global output image, this one is not resized, which does occur with the output displayed

        # initialize the global variables for storing the 8 tones to be used for color mapping:
        self.Rtones = [0, 0, 0, 0, 0, 0, 0, 0]
        self.Gtones = [0, 0, 0, 0, 0, 0, 0, 0]
        self.Btones = [0, 0, 0, 0, 0, 0, 0, 0]

        #initialize amplitudes for fuzzy color mapping:
        self.amplitudes=[5,5,5,5,5,5,5,5]

        #Default filter that will show on bottom frame at program initialization:
        self.default_filter="Color Mapping"# options: "Color Mapping","Pixelate Triangles"
        #------------------------------------------------------------------------
        #Frames configuration
        #------------------------------------------------------------------------
        self.grid_columnconfigure(0, weight=1) # configure to expand columns horizontally
        self.grid_rowconfigure(0, weight=0)  # Set weight for the first row (First frame: Images frame)
        self.grid_rowconfigure(1, weight=0)  # Set weight for the second row (Second frame: Menu frame)
        self.grid_rowconfigure(2, weight=1)  # Set weight for the third row (Third frame: Bottom frame)
        self.grid_rowconfigure(3, weight=0)  # Set weight for the fourth row (Fourth frame: Author frame)
        # we will only allow the Bottom frame to expand, while the Images, Menu and Author frame will be fixed
        # The rows 0,1,3, will maintain their initial sizes,
        # while the  row 2 will expand to fill any available extra space.

        #------------------------------------------------------------------------
        #Images frame (where input and output images are displayed)
        #------------------------------------------------------------------------
        self.images_frame = customtkinter.CTkFrame(self)
        self.images_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NEW")
        self.images_frame.pack_propagate(False)#prevent from expanding
        self.images_frame.configure(height=600)# Configure the row to have a constant height


        img1 = self.resizeIMG(self.input_image_path)  # call resize function to display default image resized
        self.input_img = customtkinter.CTkImage(dark_image=img1, size=(img1.size[0], img1.size[1]))
        self.input_img_label = customtkinter.CTkLabel(self.images_frame, image=self.input_img, text="")
        self.input_img_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        self.input_img_label.pack_propagate(False)#prevent from expanding
        self.input_img_label.configure(height=600)# Configure the row to have a constant height

        self.output_img_label = customtkinter.CTkLabel(self.images_frame, image=None, text="")
        self.output_img_label.grid(row=0, column=1, padx=10, pady=10, sticky="W")
        self.output_img_label.pack_propagate(False)#prevent from expanding
        self.output_img_label.configure(height=600)# Configure the row to have a constant height


        #------------------------------------------------------------------------
        #Menu frame
        #------------------------------------------------------------------------
        self.menu_frame = customtkinter.CTkFrame(self)
        self.menu_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NEW")

        self.button_load = customtkinter.CTkButton(self.menu_frame, text="Load image", command=self.load_image)
        self.button_load.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        self.button_run = customtkinter.CTkButton(self.menu_frame, text="Run Filter", command=lambda:self.run_filter(self.default_filter))
        self.button_run.grid(row=0, column=1, padx=10, pady=10, sticky="W")

        self.button_selectFilter = customtkinter.CTkOptionMenu(self.menu_frame, values=["Color Mapping","Pixelate Triangles"], command=self.selectFilter_callback)
        self.button_selectFilter.grid(row=0, column=2, padx=10, pady=10, sticky="W")

        self.button_saveIMG = customtkinter.CTkButton(self.menu_frame, text="Save Output", command=self.saveIMG)
        self.button_saveIMG.grid(row=0, column=3, padx=10, pady=10, sticky="W")


        #------------------------------------------------------------------------
        #Bottom frame (where the image filters and options are displayed)
        #------------------------------------------------------------------------
        self.bottom_frame = customtkinter.CTkFrame(self)
        self.bottom_frame.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")

        self.selectFilter_callback(choice=self.default_filter)#show default filter when initializing

        #------------------------------------------------------------------------
        #Author frame
        #------------------------------------------------------------------------
        def open_link():
            webbrowser.open("https://www.linkedin.com/in/dnde7")
        self.author_frame = customtkinter.CTkFrame(self,fg_color="transparent")
        self.author_frame.grid(row=3, column=0, padx=0, pady=0, sticky="NEW")
        self.author_label = customtkinter.CTkLabel(self.author_frame, text="2023 - Made by DAVID NORMAN DIAZ ESTRADA",justify="center",font=("Roboto",10),cursor="hand2")
        self.author_label.pack()
        self.author_label.bind("<Button-1>", lambda event: open_link())# Configure the label to act as a hyperlink

    def load_image(self):
        # Define the file types
        filetypes = (("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg"))
        answer = filedialog.askopenfilename(parent=self, title="Select File", filetypes=filetypes)
        print("file_path: ", self.input_image_path)
        if answer == "":
            pass  # don't do anything if filedialog returns empty value (happens when user cancels selecting a file)
        else:
            self.input_image_path=answer
            self.img = self.resizeIMG(self.input_image_path)  # resize image for display
            self.input_img = customtkinter.CTkImage(dark_image=self.img, size=(self.img.size[0], self.img.size[1]))
            self.input_img_label.configure(image=self.input_img)  # update the input image
            self.output_img_label.configure(image=None)  # erase previous output image from GUI
            self.new_output_image = None #erase previous output image

    def saveIMG(self):
        # ask user for filename for new image:
        filetypes = (("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg"))
        path = filedialog.asksaveasfilename(filetypes=filetypes)
        if path != "" and self.new_output_image is not None and self.new_output_image.any():  # to avoid error when user cancels saving image or empty image
            print(path)
            fileName = os.path.basename(path)
            # print(fileName)
            directory = os.path.dirname(path)
            # print(directory)
            # Change the current directory to specified directory:
            os.chdir(directory)

            #global newImage
            print("saving New Image")
            cv2.imwrite(fileName, self.new_output_image)

    def resizeIMG(self, path):
        """
        :param path: input image path or PIL image
        :return: img - a PIL image resized where max width = 600, max height = 600
        """
        try:
            img = Image.open(path)  # try to read image as filename (this is valid when user imports an image)
        except:
            img = path  # in case it's not possible, it means we are passing a PIL image (the processed image)
        # using pillow to resize IMG:
        baseW = 600  # max allowed Width
        baseH = 600  # max allowed Height
        imgWidth = img.size[0]
        imgHeight = img.size[1]
        if imgWidth > baseW:  # we resize the image in case its width exceeds 600 pixels
            wpercent = (float(baseW / imgWidth))
            hsize = int((float(imgHeight) * float(wpercent)))
            img = img.resize((baseW, hsize), Image.ANTIALIAS)
        imgWidth = img.size[0]
        imgHeight = img.size[1]
        if imgHeight > baseH:  # we resize the image in case its height exceeds 600 pixels
            hpercent = (float(baseH / imgHeight))
            wsize = int((float(imgWidth) * float(hpercent)))
            img = img.resize((wsize, baseH), Image.ANTIALIAS)
        # note that there will be cases in which we will have to resize by width and then by height

        # img = ImageTk.PhotoImage(img)
        return img

    def run_filter(self, filter_ID):
        print("input_image_path: ", self.input_image_path)

        if filter_ID=="Pixelate Triangles":
            print("Running Pixelate Triangles")
            size = int(self.slider.get())  # get value of size from slider
            flipX = int(self.switch_flipX.get())  # get value of size from slider
            flipY = int(self.switch_flipY.get())  # get value of size from slider
            print("Size: ", size)
            self.new_output_image = filter_triangle.filter_triangle(self.input_image_path, size, flipX, flipY)

            # convert newImage from OpenCV image to PIL image in order to display in GUI:
            im_pil = cv2.cvtColor(self.new_output_image,
                                  cv2.COLOR_BGR2RGB)  # convert from BGR to RGB in order to correctly create a PIL image
            im_pil = Image.fromarray(im_pil)  # create PIL image from array
            # Show processed Image on GUI
            img2 = self.resizeIMG(im_pil)  # we resize IMG in case it's one of its dimentions exceeds 650 pixels

            output_img = customtkinter.CTkImage(dark_image=img2, size=(img2.size[0], img2.size[1]))
            self.output_img_label.configure(image=output_img)
        elif filter_ID=="Color Mapping":
            print("Running Color Mapping")
            amplitudes=self.getAmplitudes()
            selectedMode=self.colorMappingType_var.get()#get value from radio button: fuzzy, euclidean, or linear
            print("Selected Color Mappping mode: ",selectedMode)
            self.new_output_image = colorMapping.main(self.input_image_path, self.Rtones, self.Gtones, self.Btones,
                                                      amplitudes,colorMode="RGB", mappingMode=selectedMode, visualize=False)
            # print(newImage)

            # convert newImage from OpenCV image to PIL image in order to display in GUI:
            im_pil = cv2.cvtColor(self.new_output_image,
                                  cv2.COLOR_BGR2RGB)  # convert from BGR to RGB in order to correctly create a PIL image
            im_pil = Image.fromarray(im_pil)  # create PIL image from array
            # Show processed Image on GUI
            img2 = self.resizeIMG(im_pil)  # we resize IMG in case it's one of its dimentions exceeds 650 pixels
            output_img = customtkinter.CTkImage(dark_image=img2, size=(img2.size[0], img2.size[1]))
            self.output_img_label.configure(image=output_img)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def setColor(self, ID):
        colorChooser = customTopLevelWindows.colorChooser()#create colorChooser top level window
        color=colorChooser.get_color()
        print(color)
        # print(color[0]) print RGB value
        # print(color[1]) print hexa value
        #global Rtones, Gtones, Btones

        if color != None:
            if ID == 0: self.color_button1.configure(fg_color=color[1])
            if ID == 1: self.color_button2.configure(fg_color=color[1])
            if ID == 2: self.color_button3.configure(fg_color=color[1])
            if ID == 3: self.color_button4.configure(fg_color=color[1])
            if ID == 4: self.color_button5.configure(fg_color=color[1])
            if ID == 5: self.color_button6.configure(fg_color=color[1])
            if ID == 6: self.color_button7.configure(fg_color=color[1])
            if ID == 7: self.color_button8.configure(fg_color=color[1])

            self.Rtones[ID] = int(color[0][0])#update global variable value for R channel of tones
            self.Gtones[ID] = int(color[0][1])#update global variable value for G channel of tones
            self.Btones[ID] = int(color[0][2])#update global variable value for B channel of tones

        print("Rtones = " + str(self.Rtones))
        print("Gtones = " + str(self.Gtones))
        print("Btones = " + str(self.Btones))

    def linearGradient(self,RUN, ID):

        if RUN == False:
            colorChooser = customTopLevelWindows.colorChooser()  # create colorChooser top level window
            color = colorChooser.get_color()
            print(color)
            # print(color[0]) print RGB value
            # print(color[1]) print hexa value

            if color != None:
                if ID == 1:
                    self.linearGradient_color1_button.configure(fg_color=color[1])  # assign color in hexadecimal
                    self.linearGradient_color1 = [int(color[0][0]), int(color[0][1]), int(color[0][2])]  # assign RBG values
                if ID == 2:
                    self.linearGradient_color2_button.configure(fg_color=color[1])  # assign color in hexadecimal
                    self.linearGradient_color2 = [int(color[0][0]), int(color[0][1]), int(color[0][2])]  # assign RBG values

        if RUN == True:
                R, G, B = LinearGradient.getGradient(self.linearGradient_color1, self.linearGradient_color2)
                print(R, G, B)

                # load the tones to the palette in GUI:
                palette=[R, G, B]
                self.setPalette(palette,mode="From Linear Gradient")

                #LinearGradient.plotGradient(R, G, B)# to visualize the linear gradient in 3D

    def readPalettes(self):
        # Ensure to read palettes from the directory of the main script being run
        directory = os.path.dirname(os.path.abspath(__file__))
        # Change the current directory to directory of the main script being run
        os.chdir(directory)

        # Opening JSON file in read mode
        with open('assets\colorPalettes.json', 'r') as json_file:
            data = json.load(json_file)
            return data

    def rgb_to_hexa(self, rgb):
        return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))

    def setPalette(self, palette,mode):
        if mode=="From json":
            data = self.readPalettes()  # call function to read json file with palettes

            paleta = palette  # select palette according to user

            R = data[paleta]["R"]
            G = data[paleta]["G"]
            B = data[paleta]["B"]
        else: #From Linear Gradient or from k-means result
            R = palette[0]
            G = palette[1]
            B = palette[2]

        labels = [self.color_button1, self.color_button2, self.color_button3, self.color_button4,self.color_button5,self.color_button6,self.color_button7,self.color_button8]
        for a in range(0, len(labels)):
            rgb = [R[a], G[a], B[a]]

            tone = self.rgb_to_hexa(rgb)
            labels[a].configure(fg_color=tone)

            self.Rtones[a] = R[a]
            self.Gtones[a] = G[a]
            self.Btones[a] = B[a]

        print("Rtones = " + str(self.Rtones))
        print("Gtones = " + str(self.Gtones))
        print("Btones = " + str(self.Btones))

    def button_selectPalette_callback(self, *args):
        print("args:",args)
        self.setPalette(self.button_selectPalette.get(),mode="From json")

    def button_savePalette_callback(self):
        # Display a TopLevel window to ask user the name of new palette:
        dialog = customTopLevelWindows.askPalette()
        paletteName = dialog.get_input()  # waits for input

        if paletteName != None:
            self.data = self.readPalettes()  # always read palette database first, avoid bug of overwriting previosly saved values
            #global data  # data is the current dictionary for palettes
            # modify the dictionary:
            self.data["names"].append(paletteName)
            #global Rtones, Gtones, Btones  # global variables that store the current colors in palette
            self.data[paletteName] = {
                "R": self.Rtones,
                "G": self.Gtones,
                "B": self.Btones}
            #pprint.pprint(self.data)

            # Opening JSON file in write mode
            with open('assets/colorPalettes.json', 'w') as json_file:
                json.dump(self.data, json_file, indent=4)  # indent defines # of spaces for indentation
            print("New palette saved: ",paletteName)

            # Update palettes in GUI:
            # After adding the new pallete to dictionary, we update the option list in GUI
            NewOptionList = self.data["names"]
            self.button_selectPalette.configure(values=NewOptionList)
            self.button_selectPalette.set(paletteName)#show new paletteName on menu

    def getAmplitudes(self):
        a1 = self.slider_c1.get()/10
        a2 = self.slider_c2.get()/10
        a3 = self.slider_c3.get()/10
        a4 = self.slider_c4.get()/10
        a5 = self.slider_c5.get()/10
        a6 = self.slider_c6.get()/10
        a7 = self.slider_c7.get()/10
        a8 = self.slider_c8.get()/10
        self.amplitudes = [a1, a2, a3, a4, a5, a6, a7, a8]
        print("Amplitudes:" + str(self.amplitudes))
        return self.amplitudes

    def setAmplitudes(self, *args):
        value=self.slider_master.get()
        self.slider_c1.set(value)
        self.slider_c2.set(value)
        self.slider_c3.set(value)
        self.slider_c4.set(value)
        self.slider_c5.set(value)
        self.slider_c6.set(value)
        self.slider_c7.set(value)
        self.slider_c8.set(value)
        #masterAmp.set(value)

    def Kmeans(self):
        # ask image to get tones from:
        filetypes = (("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg"))
        answer = filedialog.askopenfilename(parent=self, title="Select File", filetypes=filetypes)
        if answer == "":
            pass  # don't do anything if filedialog returns empty value (happens when user cancels selecting a file)
        else:

            print("Getting Tones from Image")
            img = answer
            R, G, B = Kmeans_tones.main(img, clusters=8)

            self.setPalette([R,G,B],mode="from kmeans")

    def selectFilter_callback(self, choice):
        print("Selected Filter:", choice)
        if choice=="Pixelate Triangles":
            #Set min and max sizes allowed for pixelation:
            currentImage=Image.open(self.input_image_path)#read full size input image
            inputWidth=currentImage.size[0]
            inputHeight=currentImage.size[1]
            min_size=int(min(inputWidth,inputHeight)*0.01)#set min size for triangle filter as 1% of image's lowest dimention
            max_size=int(max(inputWidth,inputHeight)*0.10)#set max size for triangle filter as 10% of image's highest dimention
            # ------------------------------------------------------------------------
            # Bottom frame
            # ------------------------------------------------------------------------
            self.button_run.configure(command=lambda: self.run_filter("Pixelate Triangles"))

            self.clear_frame(self.bottom_frame)#ensure the bottom_frame is clean before adding widgets, buttons, etc

            self.slider_text = customtkinter.CTkLabel(self.bottom_frame, text="Size")
            self.slider_text.grid(row=0, column=1, padx=0, pady=10, sticky="w")

            self.slider = customtkinter.CTkSlider(self.bottom_frame, from_=min_size, to=max_size, number_of_steps=99)
            self.slider.grid(row=0, column=0, padx=0, pady=10, sticky="w")

            self.switch_flipX = customtkinter.CTkSwitch(self.bottom_frame, text="Flip X", onvalue=True, offvalue=False)
            self.switch_flipX.grid(row=1, column=0, padx=0, pady=10, sticky="w")

            self.switch_flipY = customtkinter.CTkSwitch(self.bottom_frame, text="Flip Y", onvalue=True, offvalue=False)
            self.switch_flipY.grid(row=2, column=0, padx=0, pady=10, sticky="w")


        elif choice == "Color Mapping":
            # ------------------------------------------------------------------------
            # Bottom frame
            # ------------------------------------------------------------------------
            self.button_run.configure(command=lambda:self.run_filter("Color Mapping"))

            self.clear_frame(self.bottom_frame) #ensure the bottom_frame is clean before adding widgets, buttons, etc

            # ------------------------------------------------------------------------
            # Make color palette:
            # ------------------------------------------------------------------------
            #Make 8 buttons one for each color in the palette:
            self.color_button1 = customtkinter.CTkButton(self.bottom_frame, text="",width=30, height=30, command=lambda: self.setColor(0))
            self.color_button1.grid(row=0, column=0, padx=1, pady=10, sticky="W")

            self.color_button2 = customtkinter.CTkButton(self.bottom_frame, text="",width=30, height=30, command=lambda: self.setColor(1))
            self.color_button2.grid(row=0, column=1, padx=1, pady=10, sticky="W")

            self.color_button3 = customtkinter.CTkButton(self.bottom_frame, text="",width=30, height=30, command=lambda: self.setColor(2))
            self.color_button3.grid(row=0, column=2, padx=1, pady=10, sticky="W")

            self.color_button4 = customtkinter.CTkButton(self.bottom_frame, text="",width=30, height=30, command=lambda: self.setColor(3))
            self.color_button4.grid(row=0, column=3, padx=1, pady=10, sticky="W")

            self.color_button5 = customtkinter.CTkButton(self.bottom_frame, text="",width=30, height=30, command=lambda: self.setColor(4))
            self.color_button5.grid(row=0, column=4, padx=1, pady=10, sticky="W")

            self.color_button6 = customtkinter.CTkButton(self.bottom_frame, text="",width=30, height=30, command=lambda: self.setColor(5))
            self.color_button6.grid(row=0, column=5, padx=1, pady=10, sticky="W")

            self.color_button7 = customtkinter.CTkButton(self.bottom_frame, text="",width=30, height=30, command=lambda: self.setColor(6))
            self.color_button7.grid(row=0, column=6, padx=1, pady=10, sticky="W")

            self.color_button8 = customtkinter.CTkButton(self.bottom_frame, text="",width=30, height=30, command=lambda: self.setColor(7))
            self.color_button8.grid(row=0, column=7, padx=1, pady=10, sticky="W")

            #Make sliders for each color weight/amplitude
            sliders_height = 100
            sliders_width = 15
            min_amp=1
            max_amp=99
            steps=100  #steps for amplitude, this is later divided by 100 when colorMapping, CTkSlider does not allow float

            self.slider_c1 = customtkinter.CTkSlider(self.bottom_frame, from_=min_amp, to=max_amp, number_of_steps=steps, orientation="vertical",height=sliders_height,width=sliders_width)
            self.slider_c1.grid(row=1, column=0, padx=0, pady=0, sticky="")
            self.slider_c2 = customtkinter.CTkSlider(self.bottom_frame, from_=min_amp, to=max_amp, number_of_steps=steps, orientation="vertical",height=sliders_height,width=sliders_width)
            self.slider_c2.grid(row=1, column=1, padx=0, pady=0, sticky="")
            self.slider_c3 = customtkinter.CTkSlider(self.bottom_frame, from_=min_amp, to=max_amp, number_of_steps=steps, orientation="vertical",height=sliders_height,width=sliders_width)
            self.slider_c3.grid(row=1, column=2, padx=0, pady=0, sticky="")
            self.slider_c4 = customtkinter.CTkSlider(self.bottom_frame, from_=min_amp, to=max_amp, number_of_steps=steps, orientation="vertical",height=sliders_height,width=sliders_width)
            self.slider_c4.grid(row=1, column=3, padx=0, pady=0, sticky="")
            self.slider_c5 = customtkinter.CTkSlider(self.bottom_frame, from_=min_amp, to=max_amp, number_of_steps=steps, orientation="vertical",height=sliders_height,width=sliders_width)
            self.slider_c5.grid(row=1, column=4, padx=0, pady=0, sticky="")
            self.slider_c6 = customtkinter.CTkSlider(self.bottom_frame, from_=min_amp, to=max_amp, number_of_steps=steps, orientation="vertical",height=sliders_height,width=sliders_width)
            self.slider_c6.grid(row=1, column=5, padx=0, pady=0, sticky="")
            self.slider_c7 = customtkinter.CTkSlider(self.bottom_frame, from_=min_amp, to=max_amp, number_of_steps=steps, orientation="vertical",height=sliders_height,width=sliders_width)
            self.slider_c7.grid(row=1, column=6, padx=0, pady=0, sticky="")
            self.slider_c8 = customtkinter.CTkSlider(self.bottom_frame, from_=min_amp, to=max_amp, number_of_steps=steps, orientation="vertical",height=sliders_height,width=sliders_width)
            self.slider_c8.grid(row=1, column=7, padx=0, pady=0, sticky="")
            #text for color sliders:
            self.sliders_text = customtkinter.CTkLabel(self.bottom_frame, text="Color Weights", fg_color="transparent",anchor="center")
            self.sliders_text.grid(row=2, column=0, padx=0, pady=0,columnspan=8,sticky="nsew")

            #Master slider:
            self.slider_master = customtkinter.CTkSlider(self.bottom_frame, from_=min_amp, to=max_amp, number_of_steps=steps, orientation="vertical",height=sliders_height,width=sliders_width,command=self.setAmplitudes)
            self.slider_master.grid(row=1, column=8, padx=0, pady=0, sticky="")
            #Master slider text:
            self.slider_master_text = customtkinter.CTkLabel(self.bottom_frame, text="Master Weight", fg_color="transparent",anchor="center")
            self.slider_master_text.grid(row=2, column=8, padx=0, pady=0,sticky="nsew")


            # Get list to store color palette names:
            self.data = self.readPalettes()  # call function to read json file with palettes

            # set default color palette:
            self.setPalette(self.data["names"][0],mode="From json")

            # ------------------------------------------------------------------------
            # Make palette menu button:
            # ------------------------------------------------------------------------
            OptionList = self.data["names"]# list of options for palettes
            self.button_selectPalette = customtkinter.CTkOptionMenu(self.bottom_frame,
                                                                   values=OptionList,
                                                                   command=self.button_selectPalette_callback)
            self.button_selectPalette.grid(row=0, column=8, padx=10, pady=10, sticky="W")

            # ------------------------------------------------------------------------
            # Make button to save current palette:
            # ------------------------------------------------------------------------
            self.savePalette_button = customtkinter.CTkButton(self.bottom_frame, text="Save new palette",width=30,
                                                                      height=30,
                                                                      command=self.button_savePalette_callback)
            self.savePalette_button.grid(row=0, column=9, padx=10, pady=10, sticky="W")


            # ------------------------------------------------------------------------
            # Make Generate Palette frame (sub-frame of bottom_frame):
            # ------------------------------------------------------------------------
            self.generatePalette_frame = customtkinter.CTkFrame(self.bottom_frame)#make bottom_frame its parent
            self.generatePalette_frame.grid(row=1, column=9, padx=10, pady=0, sticky="NSENW")

            #generate palette text:
            self.generatePalette_text = customtkinter.CTkLabel(self.generatePalette_frame, text="Generate palette", fg_color="transparent",anchor="center")
            self.generatePalette_text.grid(row=0, column=0, padx=0, pady=0,columnspan=4,sticky="nsew")

            # ------------------------------------------------------------------------
            #Linear gradient:
            # ------------------------------------------------------------------------
            self.linearGradient_color1= [0, 0, 0] #default values for color 1
            self.linearGradient_color2= [255, 255, 255] #default values for color 2

            self.linearGradient_color1_button = customtkinter.CTkButton(self.generatePalette_frame,fg_color="#000000", text="",width=30, height=30, command=lambda: self.linearGradient(RUN=False,ID=1))
            self.linearGradient_color1_button.grid(row=1, column=1, padx=1, pady=10, sticky="W")
            self.linearGradient_color2_button = customtkinter.CTkButton(self.generatePalette_frame,fg_color="#FFFFFF", text="",width=30, height=30, command=lambda: self.linearGradient(RUN=False,ID=2))
            self.linearGradient_color2_button.grid(row=1, column=2, padx=1, pady=10, sticky="W")
            self.load_linearGradient_button = customtkinter.CTkButton(self.generatePalette_frame, text="Load linear gradient",width=30, height=30, command=lambda: self.linearGradient(RUN=True,ID=None))
            self.load_linearGradient_button.grid(row=1, column=0, padx=1, pady=10, sticky="W")


            # ------------------------------------------------------------------------
            # Button for k-means tones from image
            # ------------------------------------------------------------------------
            self.kmeans_button = customtkinter.CTkButton(self.generatePalette_frame, text="Tones from image",width=30, height=30, command=self.Kmeans)
            self.kmeans_button.grid(row=2, column=0, padx=1, pady=10, sticky="W")

            # ------------------------------------------------------------------------
            # Make Color Mapping frame (sub-frame of bottom_frame):
            # ------------------------------------------------------------------------
            self.colorMapping_frame = customtkinter.CTkFrame(self.bottom_frame)  # make bottom_frame its parent
            self.colorMapping_frame.grid(row=1, column=10, padx=10, pady=0, sticky="NSENW")

            #text:
            self.colorMapping_text = customtkinter.CTkLabel(self.colorMapping_frame, text="Color Mapping type", fg_color="transparent",anchor="center")
            self.colorMapping_text.grid(row=0, column=0, padx=0, pady=0,sticky="nsew")

            #Make 3 radio buttons to select the color mapping type:
            self.colorMappingType_var = tkinter.StringVar(value="fuzzy")#variable to track the selected type of color mapping

            self.radiobutton_1 = customtkinter.CTkRadioButton(self.colorMapping_frame, text="Fuzzy", variable=self.colorMappingType_var, value="fuzzy")
            self.radiobutton_1.grid(row=1, column=0, padx=1, pady=2, sticky="W")

            self.radiobutton_2 = customtkinter.CTkRadioButton(self.colorMapping_frame, text="Euclidean", variable=self.colorMappingType_var, value="euclidean")
            self.radiobutton_2.grid(row=2, column=0, padx=1, pady=2, sticky="W")

            self.radiobutton_3 = customtkinter.CTkRadioButton(self.colorMapping_frame, text="Light", variable=self.colorMappingType_var, value="light")
            self.radiobutton_3.grid(row=3, column=0, padx=1, pady=2, sticky="W")



app = App()
app.mainloop()
