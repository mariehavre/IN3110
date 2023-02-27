from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia

import numpy.testing as nt
import numpy as np


"""Testing numpy implementation of grayscale and sepia filter.
    Asserting equal shape and values.

    Args:
    image (np.array)
    reference_gray/reference_sepia: (np.array)
"""


def test_color2gray(image, reference_gray):
    assert numpy_color2gray(image).shape == reference_gray.shape
    assert np.allclose(numpy_color2gray(image), reference_gray)    


def test_color2sepia(image, reference_sepia):
    sepia_image = numpy_color2sepia(image)
    assert sepia_image.shape == reference_sepia.shape
    assert np.allclose(numpy_color2sepia(image), reference_sepia)
    
