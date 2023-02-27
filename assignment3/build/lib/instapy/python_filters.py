"""pure Python implementation of image filters"""
import time


import numpy as np
from PIL import Image #Usikker på om jeg får bruke denne her?


def python_color2gray(image: np.array) -> np.array:
    """Converts RGB pixel array to grayscale by multiplying
    the elements in the RGB array by certain weights and
    adding them together, creating a uniform grayscale pixel.

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)    
    img_width = len(gray_image[0,:])
    img_height = len(gray_image[:,1])

    for i in range(img_height):
            for j in range(img_width):
                for k in range(3):
                    gray_image[i,j,k] = 0.21*image[i,j,0] + 0.72*image[i,j,1] + 0.07*image[i,j,2]

    #grayscale_image = Image.fromarray(gray_image)
    #grayscale_image.save("rain_grayscale.jpg")
    
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Converts rgb pixel array to sepia by multiplying
    the sepia matrix to the RGB vector.

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """

    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],]

    sepia_image = np.empty_like(image)
    img_width = len(sepia_image[0,:])
    img_height = len(sepia_image[:,1])
                 
    for i in range(img_height):
        for j in range(img_width):
            R_temp = 0
            G_temp = 0
            B_temp = 0  
            for k in range(3):
                R_temp += image[i][j][k]*sepia_matrix[0][k]
                G_temp += image[i][j][k]*sepia_matrix[1][k]
                B_temp += image[i][j][k]*sepia_matrix[2][k]
            R = min(255, R_temp)
            G = min(255, G_temp)
            B = min(255, B_temp)
            sepia_image[i][j][:] = [R, G, B]

    sepia_image = sepia_image.astype("uint8")
    return sepia_image