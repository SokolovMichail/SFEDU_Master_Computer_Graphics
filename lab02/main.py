from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkcolorpicker import askcolor
from service import rgb_to_string
from windows import Show_And_Base_Color_Picker_Window, Show_Window
from color_correction import correction_basis_color, correction_grayscale


class Main_Window:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x300")
        self.master.title("Menu")

        self.image_path = None
        self.image = None
        self.width = 0
        self.height = 0
        self.basis_color_for_correction = ((255, 0, 0), '#FF0000')
        self.correction_color = ((255, 0, 0), '#FF0000')

        self.btn_load = Button(master, text="Load Image", command=self.load)
        self.btn_load.grid(row=0, column=0)

        self.btn_show = Button(master, text="Show Image", command=self.show_picture)
        self.btn_show.grid(row=1, column=0)
        self.btn_show['state'] = "disabled"

        self.btn_color_picker = Button(master, text="pick_color", command=self.pick_replacement_color)
        self.btn_color_picker.grid(row=2, column=0)

        self.btn_correct_color_on_basis = Button(master, text="Color_Correction_Basis",
                                                 command=self.exec_color_correction_basic_color)
        self.btn_correct_color_on_basis.grid(row=5, column=0)

        self.btn_grayscale_correction = Button(master, text="Color_Correction_Basis",
                                               command=self.exec_color_correction_grayscale)
        self.btn_grayscale_correction.grid(row=5, column=1)

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
        window = Show_And_Base_Color_Picker_Window(self, self.image, self.width, self.height)

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


root = Tk()
main_window = Main_Window(root)

root.mainloop()
