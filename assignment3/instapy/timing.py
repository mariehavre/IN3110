"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
from turtle import speed
import instapy
from . import io
from typing import Callable



def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Returns the time for one call When measuring, repeats the call `calls` times,
    and returns the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    # runs the filter function `calls` times
    # returns the _average_ time of one call
    time_total = 0

    i = 0
    while i < calls:
        t0_filter = time.time()
        filter_function(arguments[0])
        t1_filter = time.time()
        filter_time = t1_filter - t0_filter
        time_total += filter_time
        i += 1

    time_total = time_total/calls
    return time_total


def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Makes timing reports for all implementations and filters,
    runs for a given image.

    Args:
        filename (str): the image file to use
    """

    f = open("timing-report.txt", "w+")
    # load the image
    pixels = io.read_image(filename)
    f.write("Filename: " + filename + "\nWidth: " + str(len(pixels[0,:])) + "\nHeight: " + str(len(pixels[:,1])) + "\n ")
    
    # iterate through the filters
    filter_names = ["color2gray", "color2sepia"] #Lag liste med color2gray, color2sepia osv
    for filter_name in filter_names:
        # get the reference filter function
        reference_time = time_one(instapy.get_filter(filter_name), pixels)
        print(
            f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        )
        f.write(f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=}) \n")
        # iterate through the implementations
        implementations = ["numpy", "numba"] #Numpy, numba osv
        for implementation in implementations:
            filter = instapy.get_filter(filter_name, implementation)

            t0_filter = time.time()
            filter(pixels)
            t1_filter = time.time()
            filter_time = t1_filter - t0_filter

            speedup = reference_time/filter_time
            print(
                f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)"
            )
            f.write(f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x) \n")
    f.close()
        

if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()
