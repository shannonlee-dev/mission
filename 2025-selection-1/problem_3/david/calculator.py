import sys

def add(a:int,b:int)->int:
    return a+b
def subtract(a:int,b:int)->int:
    return a-b
def multiply(a:int,b:int)->int:
    return a*b
def divide(a:int,b:int)->int:
    if b==0:
        raise ZeroDivisionError("Error: Division by zero.")
    return a/b


def interactive_mode()->None:
    try:
        number_1=int(float(input('first number:')))
        number_2=int(float(input('second number:')))
    except ValueError:
        print("Invalid number input.")
        sys.exit(1)
    
    operator={
            '+':add,
            '-':subtract,
            '*':multiply,
            '/':divide
    }
    
    op=input('operator:')

    func=operator.get(op)

    if func is None:
        print('Invalid operator.')
        sys.exit(1)
    else:
        try:
            print(f'Result: {func(number_1,number_2)}')
        except ZeroDivisionError as e:
            print(e)
    
def main():
    interactive_mode()

if __name__=='__main__':
    main()