def main(base: float, exponent: int)->float:
    try: 
        base=float(input("Enter number: "))
    except:
        print('Invalid number input.')
        return 1
    try:
        exponent=int(input("Enter exponent: "))
    except:
        print('Invalid exponent input.')
        return 1
    result=1

    if base==0:
        if exponent >0:
            result = 0
        elif exponent <0:
            print('not defined')
            return 1
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