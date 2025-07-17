import sys

def power(base:float, exponent:int) -> float:
    if exponent==0:
        return 1.0
    
    elif base==0:
        if exponent <0:
            raise ZeroDivisionError("0 cannot be raised to a negative exponent.")
        else:
            return 0.0    
    
    result = 1.0
    
    for _ in range(abs(exponent)):
        result*=base
    
    if exponent < 0 :
        result=1/result

    return result

def main()->None:
    try:
        base=float(input("Enter number: "))
    except ValueError:
        print("Invalid number input.")
        sys.exit(1)   
    try:
        exponent=int(input("Enter exponent: "))
    except ValueError :
        print("Invalid exponent input.")
        sys.exit(1)
    
    try:
        print(f"Result: {power(base,exponent)}")
    except ZeroDivisionError as e:
        print("Error",e)
        sys.exit(1)

if __name__ == "__main__":
    main()