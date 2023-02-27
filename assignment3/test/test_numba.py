from asyncio import run_coroutine_threadsafe
from instapy.numba_filters import numba_color2gray, numba_color2sepia

import numpy.testing as nt
import numpy as np


def test_color2gray(image, reference_gray):
    """Testing numba implementation of grayscale filter.
    Asserting equal shape, type and three randomly selected pixels.
    Asserting uniform RGB-values.

    Args:
    image (np.array)
    reference_gray (np.array)
    """
    gray_image = numba_color2gray(image)
    img_width = len(gray_image[0,:])
    img_height = len(gray_image[:,1])

    # check that the result has the right shape, type
    assert gray_image.shape == reference_gray.shape
    assert gray_image.dtype == image.dtype

    # assert uniform r,g,b values
    for i in range(img_height):
        for j in range(img_width):
            assert (gray_image[i][j][0] == gray_image[i][j][1] == gray_image[i][j][2])

    #Choosing three pixels to test
    img_height = [0, 55, 100]
    img_width = [0, 55, 100] 
    for i in img_height:
        for j in img_width:
            assert np.allclose(gray_image[i][j][0], reference_gray[i][j][0], rtol=1e-5)
            assert np.allclose(gray_image[i][j][1], reference_gray[i][j][1], rtol=1e-5)
            assert np.allclose(gray_image[i][j][2], reference_gray[i][j][2], rtol=1e-5)


def test_color2sepia(image, reference_sepia):
    """Testing numba implementation of sepia filter.
    Asserting equal shape, type and three randomly selected pixels.

    Args:
    image (np.array)
    reference_gray (np.array)
    """
    sepia_image = numba_color2sepia(image)
    assert sepia_image.shape == reference_sepia.shape
    assert sepia_image.dtype == image.dtype

    sepia_image_test = np.empty_like(image)

    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],]

    #Choosing three pixels to test
    img_height = [0, 55, 100]
    img_width = [0, 55, 100] 

    for i in img_height:
            for j in img_width:
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
                sepia_image_test[i][j][:] = [R, G, B]
                assert np.allclose(sepia_image_test[i][j][:], sepia_image[i][j][:])

