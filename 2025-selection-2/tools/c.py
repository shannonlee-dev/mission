import sys

def parsing(row_expression: str) -> list[float, str, float]:
    token = row_expression.split()
    if len(token) !=3:
        print('Invalid input. 수식이 완벽하지 않습니다. 숫자와 연산자 사이 space를 잊으셨나요?')
        raise MissingDoubleSpaceError
    
    remove_parentheses_token=[]

    for i in token:
        print(i)
        if i.startswith('(') and i.endswith(')'):
            print('여기가 문제임',i)
            remove_parentheses_token.append(i[1:-1])
            
        else:
            remove_parentheses_token.append(i)

    return remove_parentheses_token

def main():
    #type(expression):str
    expression = input("Enter expression. Use parenthesses for negatives.e.g., (-4)*5\n"
          + "Put a space between each number and operator.\n" 
          + "or press enter if you want to use interactive mode"
          + "\n---->>> : ")
    if not expression :
        expression = interactive()
    try:
        parsed_expression = parsing(expression)
    except MissingDoubleSpaceError as e:
        print(e)
        sys.exit(1)

    print(parsed_expression)
    
main()