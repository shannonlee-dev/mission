import sys

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError('Error: Division by zero.')
    return a / b

class InvalidOperatorError(ValueError):
    pass

operator = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide
}

def parsing(row_expression: str) -> list:
    token = row_expression.split()
    if not token:
        raise ValueError('Invalid input')

    parsed_input = []
    for idx, t in enumerate(token):
        if idx % 2 == 0:  
            try:
                num = float(t)

                if num != num or num == float('inf') or num == float('-inf'):
                    raise ValueError('Invalid input')
                parsed_input.append(num)
            except ValueError:
                raise ValueError('Invalid input')
        else:           
            if t not in operator:
                raise InvalidOperatorError('Invalid input')
            parsed_input.append(t)

    if len(parsed_input) % 2 == 0:
        raise ValueError('Invalid input')

    return parsed_input

def eval_no_paren(tokens: list) -> float:

    if not tokens:
        raise ValueError('Invalid input')
    stack = [tokens[0]]  
    i = 1
    while i < len(tokens):
        op = tokens[i]
        num = tokens[i + 1]

        if op in ('*', '/'):
            prev = stack.pop()          
            stack.append(operator[op](prev, num))
        else:
            stack.append(op)
            stack.append(num)
        i += 2

    result = stack[0]
    i = 1
    while i < len(stack):
        op = stack[i]
        num = stack[i + 1]
        result = operator[op](result, num)
        i += 2

    return result

def eval_with_paren(expr: str) -> float:
    if '(' not in expr and ')' not in expr:
        return eval_no_paren(parsing(expr))

    start = expr.rfind('(')
    end = expr.find(')', start)
    if start == -1 or end == -1 or end < start:
        raise ValueError('Invalid input')

    inner = expr[start + 1:end].strip()
    inner_val = eval_no_paren(parsing(inner))

    new_expr = expr[:start] + str(inner_val) + expr[end + 1:]
    return eval_with_paren(new_expr)

def main() -> None:
    expression = input("Enter an expression: ").strip()
    if not expression:
        raise ValueError('Invalid input')

    result = eval_with_paren(expression)
    print(f"Result: {result}")

if __name__ == '__main__':
    try:
        main()
    except (ZeroDivisionError, InvalidOperatorError, ValueError) as e:
        print(e)
        sys.exit(1)
