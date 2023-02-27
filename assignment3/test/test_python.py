from instapy.python_filters import python_color2gray, python_color2sepia

import numpy as np




def test_color2gray(image):
    """Testing python implementation of grayscale filter.
    Converts input image to grayscale, and asserts
    equal shape, type and uniform RGB-values.

    Args:
    image (np.array)
    """
    # run color2gray
    gray_image = python_color2gray(image)
    img_width = len(gray_image[0,:])
    img_height = len(gray_image[:,1])
    
    # check that the result has the right shape, type
    assert gray_image.shape == image.shape
    assert gray_image.dtype == image.dtype
    
    # assert uniform r,g,b values
    for i in range(img_height):
        for j in range(img_width):
            assert (gray_image[i][j][0] == gray_image[i][j][1] == gray_image[i][j][2])



def test_color2sepia(image):
    """Testing python implementation of sepia filter.
    Converts input image to sepia, and asserts
    equal shape, type of array. Makes three sepia pixels
    and compares them to the same pixels in the sepia image 
    from the python_color2sepia function.

    Args:
    image (np.array)
    """
    # run color2sepia
    image_arr = np.asarray(image)
    sepia_image = python_color2sepia(image_arr)
    sepia_image_test = np.empty_like(image)

    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],]

    # check that the result has the right shape, type
    assert sepia_image.shape == image.shape
    assert sepia_image.dtype == image.dtype

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





