import sys 

class EmptyError(ValueError):
    pass

def find_max_min(float_numbers:list[float])-> tuple[float,float]:
    
    if not float_numbers:
        raise EmptyError('Empty one more number')

    max_x=float_numbers[0]
    min_y=float_numbers[0]

    for i in float_numbers:
        if i > max_x:
            max_x = i
        if i < min_y:
            min_y = i

    return max_x,min_y

def convert_to_float(str_numbers:str)->list:
    token = str_numbers.split()
    if not token:
        raise EmptyError('Enter one more number')
    return [float(i) for i in token]

def main():
    input_str = input("Enter numbers separted by spaces: ")
    try:
        input_float = convert_to_float(input_str)
        max_value,min_value = find_max_min(input_float)
        print(f"Max: {max_value}, Min: {min_value}")
    
    except EmptyError as e:
        print(e)
        sys.exit(1)

    except ValueError:
        print('Invalid input.')
        sys.exit(1)

if __name__ == '__main__':
    main()