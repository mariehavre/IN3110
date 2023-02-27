# Instapy

## Description
This Python package can be used to convert an image to grayscale or sepia. The image will either be displayed or saved to a new file.

## Instructions on installing
To install the package, write `python3 -m pip install .` in the terminal while in the `assignment3` directory.

## Instructions on running
To run the package, write `instapy -h` to get instruction on which flags to use. Example usage:

`instapy rain.jpg -o rain_gs.jpg -i numba -g`

This will convert `rain.jpg` to grayscale using numba and save the picture as `rain_gs.jpg`.

Available flags:

```
positional arguments:
  file                              The filename to apply filter to, required input

options:
  -h                                Shows help message and exit
  -o FILENAME                       The output filename, optional input. Picture will be displayed if no input is given
  -g                                Select gray filter
  -se                               Select sepia filter
  -sc SCALE                         Scale factor to resize image, input must be an int. Will default to scale = 1
  -i {python,numba,numpy,cython}    Choose which implementation to use, will default to python
```