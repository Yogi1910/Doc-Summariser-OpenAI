


def square(user_input):
    import numpy
    try:
        num = float(user_input)
        squared = num ** 2
        return squared
    except ValueError:
        return "Please enter a valid number"
    

def square_root(number):
    try:
        num = float(number)
        sqrt = num ** 0.5
        return sqrt
    except ValueError:
        return "Please enter a valid number for square root calculation"

def cube(number):
    try:
        num = float(number)
        cubed = num ** 3
        return cubed
    except ValueError:
        return "Please enter a valid number for cube calculation"