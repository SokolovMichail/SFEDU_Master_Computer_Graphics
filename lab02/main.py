from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkcolorpicker import askcolor
from service import rgb_to_string
from windows import Color_Picker_Window, Show_Window, ColorsHistogramWindow, \
    Brighness_Correction_Advanced_Window_Line,Brightness_Correction_Advanced_Bezier
from color_correction import correction_basis_color, \
    correction_grayscale,color_correction_sqr,normalize_histogram_2,normalize_histogram,equalize_histogram,color_correction_square


class Main_Window:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x300")
        self.master.title("Menu")

        self.image_path = None
        self.image = None
        self.width = 0
        self.height = 0
        self.basis_color_for_correction = ([255, 0, 0], '#FF0000')
        self.correction_color = ((255, 0, 0), '#FF0000')

        self.btn_load = Button(master, text="Load Image", command=self.load)
        self.btn_load.grid(row=0, column=0)

        self.btn_show = Button(master, text="Show Image", command=self.show_picture)
        self.btn_show.grid(row=1, column=0)
        self.btn_show['state'] = "disabled"

        self.btn_color_picker = Button(master, text="Pickk  Color", command=self.pick_replacement_color)
        self.btn_color_picker.grid(row=2, column=0)

        self.btn_correct_color_on_basis = Button(master, text="Color Correction on Basic Color",
                                                 command=self.exec_color_correction_basic_color)
        self.btn_correct_color_on_basis.grid(row=5, column=0)

        self.btn_grayscale_correction = Button(master, text="Grayscale Correction",
                                               command=self.exec_color_correction_grayscale)
        self.btn_grayscale_correction.grid(row=5, column=1)

        self.btn_sinus_correction = Button(master, text="Sqrt Correction",
                                           command=self.exec_color_correction_sqrt)
        self.btn_sinus_correction.grid(row=5, column=2)

        self.btn_sqr_correction = Button(master, text="Square Correction",
                                           command=self.exec_color_correction_sqr)
        self.btn_sqr_correction.grid(row=7, column=1)

        self.btn_normalize_histogram = Button(master, text="Normalize_Histogram",
                                           command=self.normalize_histogram)
        self.btn_normalize_histogram.grid(row=6, column=0)

        self.btn_equalize_histogram = Button(master, text="Equalize_Histogram",
                                              command=self.equalize_histogram)
        self.btn_equalize_histogram.grid(row=6, column=1)

        self.btn_brightness_correction_advance_line = Button(master, text="Advanced_brightness_Histogram",
                                                             command=self.advanced_color_correction_line)
        self.btn_brightness_correction_advance_line.grid(row=6, column=2)

        self.btn_brightness_correction_advance_curve = Button(master, text="Advanced_brightness_Histogram_Bez",
                                                              command=self.advanced_color_correction_bezier)
        self.btn_brightness_correction_advance_curve.grid(row=7, column=0)

        self.canvas_default = Canvas(self.master, width=20, height=20)
        self.canvas_default.create_rectangle(0, 0, 20, 20, fill="#FF0000")
        self.canvas_default.grid(row=0, column=2)

        self.label_default = Label(self.master, text="Default color")
        self.label_default.grid(row=0, column=1)

        self.canvas_replacement = Canvas(self.master, width=20, height=20)
        self.canvas_replacement.create_rectangle(0, 0, 20, 20, fill="#FF0000")
        self.canvas_replacement.grid(row=1, column=2)

        self.label_replacement = Label(self.master, text="Replace color")
        self.label_replacement.grid(row=1, column=1)

    def load(self):
        self.image_path = filedialog.askopenfilename()
        self.width, self.height = Image.open(self.image_path).size
        self.image = Image.open(self.image_path)
        # self.btn_hist['state'] = "normal"
        self.btn_show['state'] = "normal"

    def show_picture(self):
        window = Color_Picker_Window(self, self.image, self.width, self.height)

    def show_basis_color(self, r, g, b):
        self.basis_color_for_correction = ((r, g, b), rgb_to_string(r, g, b))
        self.canvas_default.create_rectangle(0, 0, 20, 20, fill=self.basis_color_for_correction[1])

    def pick_replacement_color(self):
        self.correction_color = askcolor(color="red", parent=None, title=("Color Chooser"), alpha=False)
        self.canvas_replacement.create_rectangle(0, 0, 20, 20, fill=self.correction_color[1])

    def exec_color_correction_basic_color(self):
        image_corrected = correction_basis_color(self.image, self.basis_color_for_correction, self.correction_color)
        window = Show_Window(self, image_corrected, self.width, self.height)

    def exec_color_correction_grayscale(self):
        image_corrected = correction_grayscale(self.image)
        window = Show_Window(self, image_corrected, self.width, self.height)

    def exec_color_correction_sqrt(self):
        image_corrected = color_correction_sqr(self.image)
        window = Show_Window(self, image_corrected, self.width, self.height)

    def exec_color_correction_sqr(self):
        image_corrected = color_correction_square(self.image)
        window = Show_Window(self, image_corrected, self.width, self.height)

    def normalize_histogram(self):
        image_normalized = normalize_histogram_2(self.image)
        window = Show_Window(self, image_normalized, self.width, self.height)

    def equalize_histogram(self):
        image_eq = equalize_histogram(self.image)
        window = Show_Window(self, image_eq, self.width, self.height)

    def advanced_color_correction_line(self):
        window = Brighness_Correction_Advanced_Window_Line(self, self.image, self.width, self.height)

    def advanced_color_correction_bezier(self):
        window = Brightness_Correction_Advanced_Bezier(self, self.image, self.width, self.height)


root = Tk()
main_window = Main_Window(root)

root.mainloop()
