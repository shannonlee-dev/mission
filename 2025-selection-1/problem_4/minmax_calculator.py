import sys 

class EmptyInputError(ValueError):
    pass

def find_min_max(float_numbers:list[float])-> tuple[float,float]:
    
    if not float_numbers:
        raise EmptyInputError('Enter one more number')

    first=float_numbers[0]

    max_num=first
    min_num=first
    POS_inf = float('+inf')
    NEG_inf = float('-inf')

    for i in float_numbers:
        if i == POS_inf or i == NEG_inf:
            raise ValueError("Infinity not allowed")
        if i != i:
            raise ValueError("NaN not allowed")
    
    for i in float_numbers:
        if i > max_num:
            max_num = i
        if i < min_num:
            min_num = i

    return min_num,max_num

def convert_to_float(str_numbers:str)->list[float]:
    token = str_numbers.split()
    if not token:
        raise EmptyInputError('Enter one more number')
    return [float(i) for i in token]

def main():
    input_str = input("Enter numbers separated by spaces: ")
    try:
        input_float = convert_to_float(input_str)
        min_value,max_value = find_min_max(input_float)
        print(f"Min: {min_value},Max: {max_value}")
    
    except EmptyInputError as e:
        print(e)
        sys.exit(1)

    except ValueError as e:
        print('Invalid input.')
        sys.exit(1)

if __name__ == '__main__':
    main()