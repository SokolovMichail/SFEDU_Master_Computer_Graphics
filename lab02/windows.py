from tkinter import Toplevel, Canvas, NW

from PIL import ImageTk

class Show_Window:
    def __init__(self, master, image, width, height):
        # Toplevel object which will
        # be treated as a new window
        self.master = master
        self.image = image
        self.photo_image = ImageTk.PhotoImage(self.image)
        newWindow = Toplevel(self.master.master)

        # sets the title of the
        # Toplevel widget
        newWindow.title("Image")
        self.canvas = Canvas(newWindow, width=width, height=height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
        self.canvas.image = self.photo_image


class Show_And_Base_Color_Picker_Window(Show_Window):
    def __init__(self, master, image, width, height):
        Show_Window.__init__(self,master,image,width,height)
        # Toplevel object which will
        # be treated as a new window
        self.canvas.bind("<Button-1>", self.button_click_callback)


    def button_click_callback(self,event):
        rgb_im = self.image.convert('RGB')
        r, g, b = rgb_im.getpixel((event.x, event.y))
        self.master.show_basis_color(r,g,b)