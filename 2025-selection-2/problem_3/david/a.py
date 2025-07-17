def add(a: int, b: int) -> int:
    """Return a + b."""
    return a + b


def subtract(a: int, b: int) -> int:
    """Return a - b."""
    return a - b


def multiply(a: int, b: int) -> int:
    """Return a * b."""
    return a * b


def divide(a: int, b: int):
    """Return a / b or print error if b is zero."""
    if b == 0:
        print("Error: Division by zero.")
        return None
    return a / b

oppa=input()

a = {add:'2',
     '2':subtract,
     '4': multiply}

function = a.get(oppa)

print(function(3,5))