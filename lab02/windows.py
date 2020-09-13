from tkinter import Toplevel, Canvas, NW
from PIL import ImageTk
from tkinter import *
import numpy as np
from service import permutate_array
from math import floor

class Show_Window:
    def __init__(self, master, image, width, height,name="Image"):
        # Toplevel object which will
        # be treated as a new window
        self.name = name
        self.master = master
        self.image = image
        self.photo_image = ImageTk.PhotoImage(self.image)
        newWindow = Toplevel(self.master.master)

        # sets the title of the
        # Toplevel widget
        newWindow.title(name)
        self.canvas = Canvas(newWindow, width=width, height=height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
        self.canvas.image = self.photo_image
        self.button_hist_clr = Button(newWindow, text="Show_Histogram",
                                  command=self.show_color_histogram)
        self.button_hist_clr.pack()

        self.button_hist_gray = Button(newWindow, text="Show_Histogram",
                                  command=self.show_brightness_histogram)
        self.button_hist_gray.pack()

    def show_color_histogram(self):
        histogram = ColorsHistogramWindow(self.master, self.image, self.name+" Histogram")

    def show_brightness_histogram(self):
        histogram = BrightnessHistogramWindow(self.master, self.image, self.name+" Histogram")



class Color_Picker_Window(Show_Window):
    def __init__(self, master, image, width, height):
        Show_Window.__init__(self,master,image,width,height)
        # Toplevel object which will
        # be treated as a new window
        self.canvas.bind("<Button-1>", self.button_click_callback)
        self.rgb_im = self.image.convert('RGB')


    def button_click_callback(self,event):

        r, g, b = self.rgb_im.getpixel((event.x, event.y))
        self.master.show_basis_color(r,g,b)

class Brighness_Correction:
    def __init__(self,master,image,width,height):
        self.master = master
        self.points = {}
        self.points[0.] = 0.
        self.points[1.] = 1.
        self.show_window = Show_Window(self,master,width,height)
        newWindow = Toplevel(self.master.master)
        newWindow.title("Create_function")
        self.canvas = Canvas(newWindow, width=256, height=256)
        self.canvas.pack()
        self.button_reset = Button(master, text="Reset Function",
                                                 command=self.reset)


    def mouse_click_callback(self, event):
        self.points[event.x/255.0] = event.y /255.0

    def draw_function(self):
        pass

    def reset(self):
        pass

class ColorsHistogramWindow:
    def __init__(self,master,image, name):
        self.master = master
        newWindow = Toplevel(self.master.master)
        image_bin = np.array(image)[:, :, :3]

        # Suppress specific bands (e.g. (255, 120, 65) -> (0, 120, 0) for g)
        r = image_bin[:,:,0]
        g = image_bin[:,:,1]
        b = image_bin[:,:,2]
        y_r = permutate_array(np.unique(r, return_counts=True))
        y_g = permutate_array(np.unique(g, return_counts=True))
        y_b = permutate_array(np.unique(b, return_counts=True))
        newWindow.title(name)
        canvas = Canvas(newWindow, width=256*3 + 70, height=540)
        canvas.pack()
        for i in range(256):
            canvas.create_rectangle(30 + 3 * i, 110, 33 + 3 * i, int(floor(110 - y_r.get(i, 0))), fill='red')
            canvas.create_rectangle(30 + 3 * i, 290, 33 + 3 * i, int(floor(290 - y_g.get(i, 0))), fill='green')
            canvas.create_rectangle(30 + 3 * i, 440, 33 + 3 * i, int(floor(440 - y_b.get(i, 0))), fill='blue')
            if (i % 20 == 0) | (i == 255):
                canvas.create_text(30 + 3 * i, 130, text=i.__str__())
                canvas.create_text(30 + 3 * i, 310, text=i.__str__())
                canvas.create_text(30 + 3 * i, 470, text=i.__str__())

class BrightnessHistogramWindow:
    def __init__(self,master,image, name):
        self.master = master
        newWindow = Toplevel(self.master.master)
        image_bin = np.array(image)[:, :, :3]

        # Suppress specific bands (e.g. (255, 120, 65) -> (0, 120, 0) for g)
        grayness = np.sum(image_bin,axis=2)
        grayness = grayness / 3.
        grayness = grayness.astype(int)
        grayness_rd = permutate_array(np.unique(grayness, return_counts=True))
        newWindow.title(name)
        canvas = Canvas(newWindow, width=256*3 + 70, height=300)
        canvas.pack()
        for i in range(256):
            canvas.create_rectangle(30 + 3 * i, 110, 33 + 3 * i, int(floor(110 - grayness_rd.get(i, 0))), fill='black')
            if (i % 20 == 0) | (i == 255):
                canvas.create_text(30 + 3 * i, 130, text=i.__str__())





