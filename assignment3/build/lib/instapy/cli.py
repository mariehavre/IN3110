"""Command-line (script) interface to instapy"""

import argparse
import sys
from aem import con

import numpy as np
from PIL import Image

import instapy
from . import io


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
) -> None:
    """Runs the selected filter, scales the picture if the -sc flag is used.

    Args:
        file (str): filename of the image to be converted
        out_file (str): filename of the new image if it is to be saved
        implementation (str): which implementation is to be used, defaults to python
        filter (str): which filter is to be used (sepia or grayscale), default to grayscale
        scale (int): downscales the image by the given factor, defaults to 1 (no scaling)
    """
    # load the image from a file
    image = io.read_image(file)

    if scale != 1:
        image_width = int(len(image[0,:]))
        image_height = int(len(image[:,1]))
        
        im = Image.open(file)
        resized = im.resize((image_width // scale, image_height // scale))
        image = np.asarray(resized)

    # Apply the filter
    filtered = instapy.get_filter(filter, implementation)
    image_filtered = filtered(image)

    if out_file:
        io.write_image(image_filtered, out_file)
    else:
        # not asked to save, display it instead
        io.display(image_filtered)


def main(argv=None):
    """Parses the command-line arguments and call run_filter with the arguments
    Called by 'instapy file [flags]'.
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(add_help=False)

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", help="The output filename", dest="out")

    # Add required arguments
    parser.add_argument("-h", "--help", help="show this help message and exit")
    parser.add_argument("-g", "--gray", help="Select gray filter", action='store_true')
    parser.add_argument("-se", "--sepia", help="Select sepia filter", action='store_true')
    parser.add_argument("-sc", "--scale", type=int, help="Scale factor to resize image")
    parser.add_argument("-i", "--implementation", help="The implementation of the program", choices=["python", "numpy", "numba"], default="python")

    argv = parser.parse_args()

    scale = argv.scale
    implementation = argv.implementation
    out_file = argv.out

    if argv.gray: 
        run_filter(argv.file, filter='color2gray', implementation=implementation, out_file=out_file, scale=scale if scale != None else 1)

    if argv.sepia: 
        run_filter(argv.file, filter='color2sepia', implementation=implementation, out_file=out_file, scale=scale if scale != None else 1)

    if argv.sepia == False and argv.gray == False: 
        run_filter(argv.file, filter='color2gray', implementation=implementation, out_file=out_file, scale=scale if scale != None else 1)


