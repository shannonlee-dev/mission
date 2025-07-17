import sys

def main():
    try:
        number_1=float(input('first number:'))
        number_2=float(input('second number:'))
    except ValueError:
        print("Invalid number input.")
        sys.exit(1)
    
    operator=['+','-','*','/']
    
    op=input('operator:')

    try:
        if op == operator[0]:
            print(f'result: {add(number_1,number_2)}')

        elif op == operator[1]:
            print(f'result: {subtract(number_1,number_2)}')

        elif op == operator[2]:
            print(f'result: {multiply(number_1,number_2)}')

        elif op == operator[3]:
            print(f'result: {divide(number_1,number_2)}')
        else:
            print("Invalid operator.")
            sys.exit(1)
    except ZeroDivisionError as e:
        print(e)
        sys.exit(1)     

def add(a,b):
    return a+b
def subtract(a,b):
    return a-b
def multiply(a,b):
    return a*b
def divide(a,b):
    if b==0:
        raise ZeroDivisionError("Error: Division by zero.")
        sys.exit(1)
    return a/b

if __name__=='__main__':
    main()