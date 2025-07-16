def main()->None:
    try: 
        base=float(input("Enter number: "))
    except ValueError:
        print('Invalid number input.')
        return
    try:
        exponent=int(input("Enter exponent: "))
    except ValueError:
        print('Invalid exponent input.')
        return
    result=1

    if base==0:
        if exponent >0:
            result = 0
        elif exponent <0:
            print('not defined')
            return
        elif exponent == 0:
            result=1
    else:
        for _ in range(abs(exponent)):
            result*=base

        if exponent<0:  
            result=1.0/result


    print(f"Result: {result}")


if __name__ == "__main__":
    main()