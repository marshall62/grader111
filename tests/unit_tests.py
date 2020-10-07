def test_add (student_function):

    return 22 == student_function(10, 12)


def test_sub (student_function):

    a =  -2 == student_function(10, 12)
    b =  1.0 == student_function(1.5, .5)
    return a and b

def test_div (student_function):

    a =  5 == student_function(10, 2)
    return a

def test_div2 (student_function):

    a =  -2 == student_function(10, 0)
    return a

def test_mul (student_function):

    a =  0 == student_function(10, 0)
    return a
