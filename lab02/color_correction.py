from PIL import Image
import numpy as np

def my_func(a,axis):
    print(0)
    return a

def correction_basis_color(image, basis_color,replacement_color):
    for i in range(3):
        if basis_color[0][i] == 0:
            basis_color[i] = 1
    coef_r = (replacement_color[0][0] / (basis_color[0][0] * 1.0))
    coef_g = (replacement_color[0][1] / (basis_color[0][1] * 1.0))
    coef_b = (replacement_color[0][2] / (basis_color[0][2] * 1.0))
    coefs = (coef_r,coef_g,coef_b)
    image_bin = np.array(image)[:,:,:3]
    res = np.clip(np.multiply(image_bin,coefs),0,255)
    return Image.fromarray(res.astype('uint8'), 'RGB')
