"""numpy implementation of image filters"""
from asyncore import read
import imp

from typing import Optional
import numpy as np

from PIL import Image


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image)
    for i in range(3):
        gray_image[:,:,i] = 0.21*image[:,:,0] + 0.72*image[:,:,1] + 0.07*image[:,:,2]

    return gray_image


def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """

    # define sepia matrix (optional: with `k` tuning parameter for bonus task 13)
    sepia_matrix = np.array([
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],])

    # Apply the matrix filter
    sepia_image = np.empty_like(image)
    sepia_image = np.matmul(image, np.transpose(sepia_matrix))
 
    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    sepia_image[sepia_image > 255] = 255
    sepia_image = sepia_image.astype("uint8")

    return sepia_image



