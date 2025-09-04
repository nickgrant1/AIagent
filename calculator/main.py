# main.py

import sys
from pkg.calculator import Calculator
from pkg.render import render
#from pkg.render2 import render

def main():
    calculator = Calculator()
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    expression = " ".join(sys.argv[1:])
    try:
        result = calculator.evaluate(expression)
        to_print = render(expression, result)
        print(to_print)
    except Exception as e:
        print(f"Error: {e}. Please ensure the expression is enclosed in quotes.")


if __name__ == "__main__":
    main()
