"""
Tests for our array class. Write 'pytest' in the command line to run the tests.
"""

from array_class import Array

# 1D tests (Task 4)
oneD_1 = Array((4,), 1, 2, 3, 4)
oneD_2 = Array((4,), 1, 1, 1, 1)

def test_str_1d():
    assert str(oneD_1) == '[1, 2, 3, 4]'


def test_add_1d_arr():
    assert (oneD_1 + oneD_2).is_equal(Array((4,), 2, 3, 4, 5)) == Array((4,), True, True, True, True)

def test_add_1d_int():
    assert (oneD_1 + 10).is_equal(Array((4,), 11, 12, 13, 14)) == Array((4,), True, True, True, True)

def test_add_1d_float():
    assert (oneD_1 + 0.5).is_equal(Array((4,), 1.5, 2.5, 3.5, 4.5)) == Array((4,), True, True, True, True)


def test_sub_1d_arr():
    assert (oneD_1 - oneD_2).is_equal(Array((4,), 0, 1, 2, 3)) == Array((4,), True, True, True, True)

def test_sub_1d_int():
    assert (oneD_1 - 2).is_equal(Array((4,), -1, 0, 1, 2)) == Array((4,), True, True, True, True)

def test_sub_1d_float():
    assert (oneD_1 - 0.5).is_equal(Array((4,), 0.5, 1.5, 2.5, 3.5)) == Array((4,), True, True, True, True)


def test_mul_1d_arr():
    assert (oneD_1*oneD_2).is_equal(Array((4,), 1, 2, 3, 4)) == Array((4,), True, True, True, True)

def test_mul_1d_int():
    assert (oneD_1*10).is_equal(Array((4,), 10, 20, 30, 40)) == Array((4,), True, True, True, True)

def test_mul_1d_float():
    (oneD_1*0.1).is_equal(Array((4,), 0.1, 0.2, 0.3, 0.4)) == Array((4,), True, True, True, True)


def test_eq_1d():
    assert oneD_1 == Array((4,), 1, 2, 3, 4)

def test_same_1d():
    assert oneD_1.is_equal(Array((4,), 1, 2, 3, 4)) == Array((4,), True, True, True, True)


def test_smallest_1d():
    assert oneD_1.min_element() == 1


def test_mean_1d():
    assert oneD_1.mean_element() == 2.5


# 2D tests (Task 6)

twoD_1 = Array((3, 2), 1, 2, 3, 4, 5, 6)
twoD_2 = Array((3, 2), 2, 2, 2, 2, 2, 2)


def test_add_2d_arr():
    assert (twoD_1 + twoD_2).is_equal(Array((3,2), 3, 4, 5, 6, 7, 8)) == Array((3,2), True, True, True, True, True, True)

def test_add_2d_int():
    assert (twoD_1 + 10).is_equal(Array((3, 2), 11, 12, 13, 14, 15, 16)) == Array((3,2), True, True, True, True, True, True)

def test_add_2d_float():
    assert (twoD_1 + 0.5).is_equal(Array((3, 2), 1.5, 2.5, 3.5, 4.5, 5.5, 6.5)) == Array((3,2), True, True, True, True, True, True)


def test_sub_2d_arr():
    assert (twoD_1 - twoD_2).is_equal(Array((3, 2), -1, 0, 1, 2, 3, 4)) == Array((3,2), True, True, True, True, True, True)

def test_sub_2d_int():
    assert (twoD_1 - 1).is_equal(Array((3,2), 0, 1, 2, 3, 4, 5)) == Array((3,2), True, True, True, True, True, True)

def test_sub_2d_float():
    assert (twoD_1 - 0.5).is_equal(Array((3,2), 0.5, 1.5, 2.5, 3.5, 4.5, 5.5)) == Array((3,2), True, True, True, True, True, True)


def test_mul_2d_arr():
    assert (twoD_1*twoD_2).is_equal(Array((3,2), 2, 4, 6, 8, 10, 12)) == Array((3,2), True, True, True, True, True, True)

def test_mul_2d_int():
    assert (twoD_1*10).is_equal(Array((3,2), 10, 20, 30, 40, 50, 60)) == Array((3,2), True, True, True, True, True, True)

def test_mul_2d_float():
    assert (twoD_1*0.5).is_equal(Array((3,2), 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)) == Array((3,2), True, True, True, True, True, True)
    

def test_same_2d():
    assert twoD_1.is_equal(Array((3, 2), 1, 2, 3, 4, 5, 6)) == Array((3,2), True, True, True, True, True, True)

def test_eq_2d():
    assert twoD_1 == Array((3, 2), 1, 2, 3, 4, 5, 6)

def test_mean_2d():
    assert twoD_1.mean_element() == 3.5


if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """


    # Task 4: 1d tests
    test_add_1d_arr()
    test_add_1d_int()
    test_add_1d_float()


    test_sub_1d_arr()
    test_sub_1d_int()
    test_sub_1d_float()

    test_mul_1d_arr()
    test_mul_1d_int()
    test_mul_1d_float()

    test_str_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d_arr()
    test_add_2d_int()
    test_add_2d_float()

    test_sub_2d_arr()
    test_sub_2d_int()
    test_sub_2d_float()

    test_mul_2d_arr()
    test_mul_2d_int()
    test_mul_2d_float()

    test_same_2d()
    test_mean_2d()