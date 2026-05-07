def convert_to_float(str_numbers:str)->list:
    token = str_numbers.split()
    if not token:
        raise EmptyError('Enter one more number')
    return [float(i) for i in token]



a = ''
b = a.split()
print(b)
