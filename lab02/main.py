from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import floor
from tkcolorpicker import askcolor
import numpy as np

class Main_Window:
    def __init__(self,master):
        self.master = master
        self.master.geometry("400x300")
        self.master.title("Menu")

        self.file_path = None
        self.image = None
        self.width = 0
        self.height = 0
        self.basis_color_for_correction = ((255, 0, 0),'#FF0000')

        self.btn_load = Button(master,text = "Load Image",command = self.load)
        self.btn_load.pack()

        self.btn_show = Button(master, text = "Show Image", command = self.show_picture)
        self.btn_show.pack()
        self.btn_show['state'] = "disabled"

        self.btn_color_picker = Button(master, text="pick_color",command = self.pick_color)
        self.btn_color_picker.pack()

        self.canvas =  Canvas(self.master, width = 20, height = 20)
        self.canvas.create_rectangle(0, 0, 20, 20, fill = "#FF0000")
        self.canvas.pack()

    def load(self):
        self.file_path = filedialog.askopenfilename()
        self.width, self.height = Image.open(self.file_path).size
        self.image = ImageTk.PhotoImage(Image.open(self.file_path))
        #self.btn_hist['state'] = "normal"
        self.btn_show['state'] = "normal"

    def show_picture(self):
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(self.master)

        # sets the title of the
        # Toplevel widget
        newWindow.title("Image")
        canvas = Canvas(newWindow, width=self.width, height=self.height)
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=self.image)
        canvas.image = self.image

    def pick_color(self):
        self.basis_color_for_correction = askcolor(color="red", parent=None, title= ("Color Chooser"), alpha=False)
        self.canvas.create_rectangle(0,0,20,20,fill = self.basis_color_for_correction[1])


root = Tk()
main_window = Main_Window(root)

root.mainloop()
