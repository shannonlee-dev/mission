import sys

def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
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
    """list[float, str, float, str, ...] 형태로 변환"""
    token = row_expression.split()
    if not token:
        raise ValueError('Invalid input')

    parsed_input = []


    for idx, t in enumerate(token):
        if idx % 2 == 0:
            # 숫자 자리
            try:
                num = float(t)
                # NaN 체크 (math 없이 가능)
                if num != num or num == float('inf') or num == float('-inf'):
                    raise ValueError('Invalid input')
                parsed_input.append(num)
            except ValueError:
                raise ValueError('Invalid input')
        else:

            if t not in operator:
                raise InvalidOperatorError('Invalid input')
            parsed_input.append(t)

    # >>> FIX: 짝수 길이면 "숫자 연산자 숫자 ..." 형태가 아님
    if len(parsed_input) % 2 == 0:
        raise ValueError('Invalid input')

    return parsed_input

def calculate_expression(exp: list) -> float:
    """*, / 먼저 처리 후 +, - 처리"""
    if not exp:
        raise ValueError('Invalid input')

    # >>> FIX: 원본은 리스트를 직접 수정하며 인덱스가 꼬였음.
    # 1차 패스: * / 처리
    out = [exp[0]]
    i = 1
    while i < len(exp):
        op = exp[i]
        num = exp[i + 1]
        if op in ('*', '/'):
            out[-1] = operator[op](out[-1], num)
        else:
            out.extend([op, num])
        i += 2

    # 2차 패스: + - 처리
    result = out[0]
    i = 1
    while i < len(out):
        op = out[i]
        num = out[i + 1]
        result = operator[op](result, num)
        i += 2

    return result

# >>> FIX: 괄호를 재귀적으로 푸는 함수 추가
def eval_with_paren(expr: str) -> float:
    # 괄호가 없으면 바로 계산
    if '(' not in expr and ')' not in expr:
        return calculate_expression(parsing(expr))

    # 가장 안쪽 '(' 찾기
    start = expr.rfind('(')
    end = expr.find(')', start)
    if start == -1 or end == -1 or end < start:
        raise ValueError('Invalid input')  # 괄호 짝 오류

    inner = expr[start + 1:end].strip()
    # 내부 식 계산
    inner_val = calculate_expression(parsing(inner))

    # 계산 결과로 치환 후 다시 재귀 호출
    new_expr = expr[:start] + str(inner_val) + expr[end + 1:]
    return eval_with_paren(new_expr)

def main() -> None:
    # expression = input("Enter expression.\nPut a space between each number and operator.\n\n---->>> : ")
    expression = '( 4 + 5 ) * ( 3 - 2 )'
    if not expression:
        raise ValueError('Invalid input')
    if expression.count('(') != expression.count(')'):
        raise ValueError('Invalid input')

    # >>> FIX: while 루프 제거, 재귀 함수로 괄호 처리
    result = eval_with_paren(expression)
    print(f"Result: {result}")

if __name__ == '__main__':
    try:
        main()
    except (ZeroDivisionError, InvalidOperatorError, ValueError) as e:
        print(e)
        sys.exit(1)
