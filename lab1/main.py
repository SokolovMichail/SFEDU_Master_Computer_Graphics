from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import floor
import numpy as np

def permutate_array(y_x):
    intensities = y_x[0]
    counts = y_x[1]
    counts = y_x[1]
    max = np.amax(counts)
    counts = counts/max
    counts *= 100
    return dict(zip(intensities,counts))


class Main_Window:
    def __init__(self,master):
        self.master = master
        self.master.geometry("400x300")
        self.master.title("Menu")
        self.file_path = None
        self.image = None
        self.width = 0
        self.height = 0
        btn_load = Button(master,text = "Load Image",command = self.load)
        btn_load.pack()
        self.btn_show = Button(master,text = "Show Image",command = self.show_window)
        self.btn_show.pack()
        self.btn_hist = Button(master, text="Show Histograms",command = self.show_histograms)
        self.btn_hist.pack()
        self.btn_hist['state'] = "disabled"
        self.btn_show['state'] = "disabled"

    def load(self):
        self.file_path = filedialog.askopenfilename()
        self.width, self.height = Image.open(self.file_path).size
        self.image = ImageTk.PhotoImage(Image.open(self.file_path))
        self.btn_hist['state'] = "normal"
        self.btn_show['state'] = "normal"

    def show_window(self):
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

    def show_histograms(self):
        newWindow = Toplevel(self.master)
        img = Image.open(self.file_path)
        data = np.array(img)
        data = data.reshape((data.shape[0]*data.shape[1],data.shape[2]))

        # Suppress specific bands (e.g. (255, 120, 65) -> (0, 120, 0) for g)
        r = [(d[0]) for d in data]
        g = [(d[1]) for d in data]
        b = [(d[2]) for d in data]
        y_r = permutate_array(np.unique(r, return_counts=True))
        y_g = permutate_array(np.unique(g, return_counts=True))
        y_b = permutate_array(np.unique(b, return_counts=True))
        newWindow.title("Histograms")
        canvas = Canvas(newWindow, width=256*3 + 70, height=540)
        canvas.pack()
        for i in range(256):
            canvas.create_rectangle(30 + 3 * i, 110, 33 + 3*i, int(floor(110-y_r.get(i,0))), fill='red')
            canvas.create_rectangle(30 + 3 * i, 290, 33 + 3 * i, int(floor(290-y_g.get(i,0))), fill='green')
            canvas.create_rectangle(30 + 3 * i, 440, 33 + 3 * i, int(floor(440-y_b.get(i,0))), fill='blue')
            if (i % 20 == 0) | (i == 255):
                canvas.create_text(30 + 3 *i,130,text = i.__str__())
                canvas.create_text(30 + 3 * i, 310, text=i.__str__())
                canvas.create_text(30 + 3 * i, 470, text=i.__str__())

root = Tk()
main_window = Main_Window(root)

root.mainloop()
