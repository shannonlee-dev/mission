import sys

def power(base: float, exponent: int) -> float:
    if exponent == 0:
        return 1.0
    if base == 0:
        if exponent < 0:
            raise ZeroDivisionError("0 cannot be raised to a negative exponent.")
        else:
            return 0.0
    result = 1.0
    for _ in range(abs(exponent)):
        result *= base
    if exponent < 0:
        result = 1.0 / result
    return result

def run_power_calculation(base_str: str, exponent_str: str) -> float:
    try:
        base = float(base_str)
    except ValueError:
        raise ValueError("Invalid number input.")
    try:
        exponent = int(exponent_str)
    except ValueError:
        raise ValueError("Invalid exponent input.")
    return power(base, exponent)

def main() -> None:
    base_str = input("Enter number: ")
    exponent_str = input("Enter exponent: ")
    try:
        result = run_power_calculation(base_str, exponent_str)
        print(f"Result: {result}")
    except (ValueError, ZeroDivisionError) as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
