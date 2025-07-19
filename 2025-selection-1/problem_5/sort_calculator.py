import sys

class EmptyInputError(ValueError):
    pass

def find_min(numbers:list[float])->float:
    if not numbers:
        raise EmptyInputError('Invalid input.')

    min_num=numbers[0]
    
    for i in numbers:
        if i < min_num:
            min_num = i

    return min_num



# list 내부에서만 sort 하는 함수
def sort(numbers:list[float])->list[float]:
    
    result = numbers[:]

    for i in range(len(result)):
        temp = result.index(find_min(result[i:]))
        result[i],result[temp] = result[temp],result[i]
    return result    

def parsed(str_numbers:str)->list:
    token = str_numbers.split()
    if not token:
        raise EmptyInputError('Invalid input.')
    
    float_numbers = [float(i) for i in token]

    POS_inf = float('+inf')
    NEG_inf = float('-inf')

    for i in float_numbers:
        if i == POS_inf or i == NEG_inf:
            raise ValueError("Invalid input.")
        if i != i:
            raise ValueError("Invalid input.")    
    try:
        return float_numbers
    except ValueError:
        raise ValueError('Invalid input.')
    
def list_to_str(sorted_list:list)->str:
    str_list=[str(nums) for nums in sorted_list] 
    return (' '.join(str_list))

def main():
    try:
        str_numbers = input('Enter numbers: ')
        float_numbers = parsed(str_numbers)
        sorted_numbers = sort(float_numbers)
        result = list_to_str(sorted_numbers)
        print(result)
    except (EmptyInputError,ValueError) as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()