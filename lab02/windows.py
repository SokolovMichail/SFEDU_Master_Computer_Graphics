from tkinter import Toplevel, Canvas, NW
from PIL import ImageTk
from PIL import Image as ImagePIL
from tkinter import *
import numpy as np
from service import permutate_array
from math import floor
from color_correction import brightness_prep
import keyboard
from scipy import interpolate

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
        self.button_hist_clr = Button(newWindow, text="Show_Histogram_Color",
                                  command=self.show_color_histogram)
        self.button_hist_clr.pack()

        self.button_hist_gray = Button(newWindow, text="Show_Histogram_Grey",
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

class Brighness_Correction_Advanced_Window_Line:
    def __init__(self,master,image,width,height):
        self.width = width
        self.height = height
        self.master = master
        self.points = {}
        self.points[0.] = 0.
        self.points[1.] = 1.
        self.image = image
        self.show_window = Show_Window(self.master.master,image,width,height)
        self.newWindow = Toplevel(self.master.master)
        self.newWindow.title("Create_function")
        self.canvas = Canvas(self.newWindow, width=300, height=300)
        self.canvas.grid(row = 1, column =1)
        self.bezier = None
        #self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
        self.canvas.bind("<Button-1>", self.mouse_click_callback)
        self.draw_function()
        self.button_reset = Button(self.newWindow, text="Reset Function",
                                                 command=self.reset)
        self.button_reset.grid(row =2, column = 1)
        self.button_correct = Button(self.newWindow, text="Correct",
                                   command=self.correct)
        self.button_correct.grid(row =3, column = 1)
        label = Label(self.newWindow,text = '11')
        label.grid(row = 0,column = 0)


    def mouse_click_callback(self, event):
        x = event.x
        y = event.y
        x = max(22,min(x,278))
        y = max(22,min(y,278))
        if keyboard.is_pressed("z"):
            x = 22
        if keyboard.is_pressed("o"):
            x = 278
        x -= 22
        y -= 22
        self.points[1-x/256.0] = y /256.0
        self.draw_function()

    def interpolate(self,x):
        ord_x = self.points.keys()
        ord_x = sorted(ord_x)
        ord_y = []
        for i in ord_x:
            ord_y.append(self.points[i])
        res = np.interp(x,ord_x,ord_y)
        return res

    def correct(self):
        image = brightness_prep(self.image)
        image_new = self.interpolate(image)
        image_new *= 255
        image_fin = ImagePIL.fromarray(image_new.astype('uint8'), 'RGB')
        show_window = Show_Window(self.master.master, image_fin, self.width, self.height)


    def draw_function(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, 300, 300, fill='red')
        self.canvas.create_rectangle(22,22,278,278,fill = 'white')
        ord = self.points.keys()
        if len(ord) >= 2:
            ord = sorted(ord)
            prev = ord[0]
            for i in ord:
                self.canvas.create_line((256-prev*256)+22,(self.points[prev]*256)+22,256-i*256+22,self.points[i]*256+22)
                prev = i
        for i in ord:
            self.canvas.create_oval(256-(i*256-2)+22,self.points[i]*256 - 2+22,256-(i*256+2)+22,self.points[i]*256 +2+22,fill = 'green')

    def reset(self):
        self.points = {}
        self.points[0.] = 0.
        self.points[1.] = 1.
        self.draw_function()

class Brightness_Correction_Advanced_Bezier(Brighness_Correction_Advanced_Window_Line):

    def interpolate(self,x):
        ord_x = self.points.keys()
        ord_x = sorted(ord_x)
        ord_y = []
        for i in ord_x:
            ord_y.append(self.points[i])
        ord_x = np.array(ord_x)*256.
        ord_y = np.array(ord_y)*256.
        self.spline = interpolate.CubicSpline(ord_x,ord_y)
        return self.spline(x)


    def correct(self):
        image_bin = np.array(self.image)[:, :, :3]
        image_new = self.interpolate(image_bin)
        image_fin = ImagePIL.fromarray(image_new.astype('uint8'), 'RGB')
        show_window = Show_Window(self.master.master, image_fin, self.width, self.height)

    def draw_function(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, 300, 300, fill='red')
        self.canvas.create_rectangle(22, 22, 278, 278, fill='white')
        ord_x = np.arange(0,256)
        ord_y = self.interpolate(ord_x)
        ord_x_m = ord_x# * 255
        ord_y_m = ord_y# * 255
        for i in range(1,256):
            self.canvas.create_line((256 - ord_x_m[i-1]) + 22, (ord_y_m[i-1]) + 22, 256 - ord_x_m[i] + 22,
                                    ord_y_m[i] + 22)
        for i in self.points.keys():
            self.canvas.create_oval(256 - (i * 256 - 2) + 22, self.points[i] * 256 - 2 + 22, 256 - (i * 256 + 2) + 22,
                                    self.points[i] * 256 + 2 + 22, fill='green')



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





