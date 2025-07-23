import sys

def add(a,b):
    return a+b
def subtract(a,b):
    return a-b
def multiply(a,b):
    return a*b
def divide(a,b):
    if b==0:
        raise ZeroDivisionError('Error: Division by zero.')
    return a/b

class InvalidOperatorError(ValueError):
    pass

class MissingDoubleSpaceError(ValueError):
    pass

operator={
    '+' : add,
    '-' : subtract,
    '*' : multiply,
    '/' : divide
}

def interactive() -> str:
    first_number_input = input('first number: ')
    second_number_input = input('second number: ')
    operator_input = input('operator: ')

    expression = first_number_input + ' '+ operator_input + ' ' + second_number_input 
    return expression

def parsing(row_expression: str) -> list: #list[float, str, float] 
    token = row_expression.split()
    if len(token) !=3:
        raise MissingDoubleSpaceError('Invalid input. forgot double space?')
    
    remove_parentheses_token=[]

    for i in token:
        if i.startswith('(') and i.endswith(')'):
            remove_parentheses_token.append(i[1:-1])
            
        else:
            remove_parentheses_token.append(i)
    
    parsed_input = []

    for index,value in enumerate(remove_parentheses_token):
        if index%2 == 0:
            try:
                float_number=float(value)
            except ValueError:
                raise ValueError('Invalid number')
            parsed_input.append(float_number)    
        else:
            if value not in operator:
                raise InvalidOperatorError('Invalid operator.')
            parsed_input.append(value)

    return parsed_input       

def calculate_expression(exp: list) -> float:  # list[float, str, float] -> float
    
    func = operator.get(exp[1])   
    try:
        result = func(exp[0],exp[2])
    except ZeroDivisionError:
        raise ZeroDivisionError('Error: Division by zero.')    
    return result

def evaluate(exp:str)->float :
    parsed_expression = parsing(exp)
    return calculate_expression(parsed_expression)

def main()-> None :
    #type(expression):str
    expression = input("Enter expression. Use parenthesses for negatives.e.g., (-4)*5\n"
          + "Put a space between each number and operator.\n" 
          + "or press enter if you want to use interactive mode"
          + "\n---->>> : ")
    if not expression :
        expression = interactive()

    try:
        result = evaluate(expression)
    except (MissingDoubleSpaceError,ValueError,InvalidOperatorError,ZeroDivisionError) as e:
        print(e)
        sys.exit(1) 

    print(f"Result: {result}")


if __name__ == '__main__':
    main()