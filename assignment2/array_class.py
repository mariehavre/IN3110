"""
Array class for assignment 2.
"""

from audioop import mul
from os import stat
from struct import pack
from itertools import chain


class Array:

    def __init__(self, shape, *values):
        """Initializes an array of 1- or 2-dimensionality. Creates a flat array used for elementwise operations.
        Elements can only be of type:

        - int
        - float
        - bool

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """
        
        self.values = values
        self.shape = shape

        for i in range(len(values)):
            it = type(values[0])
            if type(values[i]) != it:
                raise ValueError 

        for val in values:
            if type(val) not in (float, int, bool):
                raise TypeError

        if type(shape) is not tuple:
            raise TypeError

        init_num = 1
        for num in shape:
            init_num *= num
        
        if init_num != len(values):
            raise ValueError


        if len(shape) > 1:
            self.array = Array.create_2D_array(shape, values)
        else:
            self.array = Array.create_1D_array(values)

        self.flat_array = self.flat_array(self)

    def __getitem__(self, index):
        """Returns the value at the given index.

        Args:
            index: Must be of type integer.

        Returns:
            int, float or boolean value.

        Raises:
            TypeError: If index is not an integer.
        """
        if index.isinstance(int):
            return self.array[index]
        else:
            raise TypeError
            

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        return str(self.array)

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        #Om man sender inn en array må shape og type stemme
        if isinstance(other, Array):
            self.check_int_float_shape(other)
            sum_array = [i+j for i, j in zip(self.flat_array, other.flat_array)]
        elif isinstance(other, (int, float)):
            #Sjekker først om verdien som sendes inn er av riktig type om det ikke er en array
            sum_array = []
            for i in range (len(self.flat_array)):
                sum_array.append(self.flat_array[i] + other)

        return Array(self.shape, *sum_array)
        


    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self.__add__(other)


    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        if isinstance(other, Array):
            self.check_int_float_shape(other)
            sub_array = [i-j for i, j in zip(self.flat_array, other.flat_array)]
        elif isinstance(other, int) or isinstance(other, float):
            sub_array = []
            for i in range (len(self.flat_array)):
                sub_array.append(self.flat_array[i] - other)
        
        return Array(self.shape, *sub_array)


    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        return -(self.__sub__(other))

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        mul_array = []
        if isinstance(other, Array):
            self.check_int_float_shape(other)
            mul_array = [i*j for i, j in zip(self.flat_array, other.flat_array)]
        elif isinstance(other, int) or isinstance(other, float):
            for i in range (len(self.flat_array)):
                mul_array.append(self.flat_array[i]*other)
        return Array(self.shape, *mul_array)

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it returns NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it returns False.
        If `other` is an unexpected type, it returns False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        if self.shape != other.shape or type(other) != type(self):
            return False

        return self.array==other.array

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method raises ValueError.
        If `other` is not an array or a number, it returns TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        if other.shape != self.shape:
            raise ValueError

        if type(other.values[0]) not in (float, int):
            return TypeError

        bool_array = [i==j for i, j in zip(self.flat_array, other.flat_array)]
        return Array(self.shape, *bool_array)

    def min_element(self):
        """Returns the smallest value of the array.

        Returns NotImplemented if values is not of type int or float.

        Returns:
            float: The value of the smallest element in the array.

        """
        self.check_int_float_other(self)

        sorted_arr = sorted(self.flat_array)
        return sorted_arr[0]


    def mean_element(self):
        """Returns the mean value of an array. 
        
        Returns NotImplemented if values is not of type int or float.

        Returns:
            float: the mean value
        """
        self.check_int_float_other(self)
        return sum(self.flat_array)/len(self.flat_array)
    
    @staticmethod
    def create_2D_array(shape, values):
        """Creates a 2D array based on the given shape and values given in the constructor.

        Args:
            shape (tuple): Tuple of ints determining the shape of the array.
            values (list): List of values of type bool, int or float.
        
        Returns:
            list: A 2D list of the values given.
        """
        elementsInEachList = shape[1]
        numberOfList= shape[0]
        parentList = []

        for i in range(numberOfList):
            childList = []
            k = i * elementsInEachList
            val = k + elementsInEachList
            while k < val:
                childList.append(values[k])
                k += 1
            
            if numberOfList > 1:
                parentList.append(childList)
            else:
                parentList = childList
        return parentList

    @staticmethod
    def create_1D_array(values):
        """Creates a 1D array of the values given in the constructor.

        Args:
            values (list): List of values of type bool, int or float.
        
        Returns:
            list: List of shape (1,)
        """
        return list(values)

    def flat_array(self, other):
        """Flattens the N-dimensional array of values into a 1-dimensional array.

         Args:
            other (Array): The array that is to be flattened. 

        Returns:
            list: flat list of array values.
        """
        flat_array = other.array
        for _ in range(len(other.shape[1:])):
            flat_array = list(chain(*flat_array))
        return flat_array

    def check_int_float_shape(self, other):
        """Checks if the values are int or float, and that the shape of the arrays that are to be 
            compared matches. Returns NotImplemented if not.

        Args:
            other (Array): The array to be checked.
        """
        if type(other.values[0]) not in (float, int) or other.shape != self.shape:
            return NotImplemented

    def check_int_float_other(self, other):
        """Checks if the values are int or float.

        Args:
            other (Array): The array to be checked.

        Raises:
            ValueError: If the values are not of type int or float.
        """
        if type(other.values[0]) not in (int, float):
            raise ValueError