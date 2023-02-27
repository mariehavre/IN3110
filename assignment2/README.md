This class creates an array-like object of one or two dimensions, with functionality like
toString-method, mathematical operations, checking if the array is equal to another array,
and getting the value at a certain index.

Example:
        arrayExample1 = Array((1,), 1, 2, 3, 4)         Creates a 1D array
        arrayExample2 = Array((3,2), 1, 2, 3, 4, 5, 6)  Creates a 2D array.

Attributes:
    shape (tuple): A tuple of one or two values of type int.
    *values (int, float, bool): Values to be inserted in the array. Must be of the same type,
        and of type int, float or bool. The number of values must match the shape.
        