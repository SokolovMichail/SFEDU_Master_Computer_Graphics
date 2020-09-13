from PIL import Image
import numpy as np
from math import sin,cos,tan
from service import permutate_array_2

def correction_basis_color(image, basis_color, replacement_color):
    for i in range(3):
        if basis_color[0][i] == 0:
            basis_color[i] = 1
    coef_r = (replacement_color[0][0] / (basis_color[0][0] * 1.0))
    coef_g = (replacement_color[0][1] / (basis_color[0][1] * 1.0))
    coef_b = (replacement_color[0][2] / (basis_color[0][2] * 1.0))
    coefs = (coef_r, coef_g, coef_b)
    image_bin = np.array(image)[:, :, :3]
    res = np.clip(np.multiply(image_bin, coefs), 0, 255)
    return Image.fromarray(res.astype('uint8'), 'RGB')


def correction_grayscale(image):
    image_bin = np.array(image)[:, :, :3]
    rgb_sums = np.sum(image_bin, axis=(0, 1))
    avg = np.sum(rgb_sums) / 3.0
    coef_r = (avg / (rgb_sums[0] * 1.))
    coef_g = (avg / (rgb_sums[1] * 1.))
    coef_b = (avg / (rgb_sums[2] * 1.))
    coefs = (coef_r, coef_g, coef_b)
    res = np.clip(np.multiply(image_bin, coefs), 0, 255)
    return Image.fromarray(res.astype('uint8'), 'RGB')

def normalize_sinus(x):
    return abs(1-x)

def color_correction_sinus(image):
    image_bin = np.array(image)[:, :, :3]
    image_new = image_bin / 255.0
    res = (1+np.sin((image_new)))/2.
    res *= 255
    res = res.astype(int)
    return Image.fromarray(res.astype('uint8'), 'RGB')

def normalize_histogram(image):
    image_bin = np.array(image)[:, :, :3]
    # Suppress specific bands (e.g. (255, 120, 65) -> (0, 120, 0) for g)
    grayness = np.sum(image_bin, axis=2)
    grayness = grayness / 3.
    grayness = grayness.astype(int)
    grayness_ready = np.unique(grayness)
    min_v = np.min(grayness_ready)
    max_v = np.max(grayness_ready)
    res = np.clip((image_bin-min_v)*(255/max(1,max_v-min_v)),0,255)
    return Image.fromarray(res.astype('uint8'), 'RGB')

def calculate_new_value_norm(x,axis):
    pass

def normalize_histogram_2(image):
    image_bin = np.array(image)[:, :, :3]
    mins = np.min(image_bin,axis=(1,0))
    maxs = np.max(image_bin,axis=(1,0))
    image_new = np.copy(image_bin)
    #min_v = mins[i]
    #max_v = maxs[i]
    image_new = np.subtract(image_new,mins)
    tmp = 255 / (maxs - mins)
    image_new = np.multiply(image_new,tmp)
    #res = np.clip((image_bin-min_v)*(255/max(1,max_v-min_v)),0,255)
    return Image.fromarray(image_new.astype('uint8'), 'RGB')

def equalize_histogram(image):
    image_bin = np.array(image)[:, :, :3]
    pixel_amount = image_bin.shape[0] * image_bin.shape[1] * 1.
    r = image_bin[:, :, 0]
    g = image_bin[:, :, 1]
    b = image_bin[:, :, 2]
    r_normed = permutate_array_2(np.unique(r,return_counts=True))
    g_normed = permutate_array_2(np.unique(g,return_counts=True))
    b_normed = permutate_array_2(np.unique(b,return_counts=True))
    r_normed = r_normed / 2#55
    b_normed = b_normed / 2#55
    g_normed = g_normed / 2#55
    shr = np.roll(r_normed,1)
    shr[0] = 0
    r_normed = r_normed + shr
    shg = np.roll(g_normed,1)
    shg[0] = 0
    g_normed = g_normed + shg
    shb = np.roll(b_normed,1)
    shr[0] = 0
    b_normed = b_normed + shb
    image_new = np.copy(image_bin)
    for i in range(image_new.shape[0]):
        for j in  range(image_new.shape[1]):
            image_new[i,j,0] = r_normed[image_new[i,j,0]]
            image_new[i, j, 1] = g_normed[image_new[i, j, 1]]
            image_new[i, j, 2] = b_normed[image_new[i, j, 2]]
    #res = np.clip((image_bin-min_v)*(255/max(1,max_v-min_v)),0,255)
    return Image.fromarray(image_new.astype('uint8'), 'RGB')


