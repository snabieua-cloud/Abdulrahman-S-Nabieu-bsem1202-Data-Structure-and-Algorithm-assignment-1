# DCOMP320 - Data Structures and Algorithms
# Stack-Based Mathematical Expression Evaluator

class Stack:
    """A simple stack implementation using a Python list."""

    def __init__(self):
        self.items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item."""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        """Return the top item without removing it."""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        """Check whether the stack is empty."""
        return len(self.items) == 0


def precedence(operator):
    """Return the precedence level of an operator."""
    if operator in ("+", "-"):
        return 1
    elif operator in ("*", "/"):
        return 2
    return 0


def apply_operator(a, b, operator):
    """Perform a mathematical operation."""
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b

    raise ValueError("Invalid operator: " + operator)


def evaluate_expression(expression):
    """Evaluate a mathematical expression using stacks."""

    values = Stack()
    operators = Stack()

    # Add spaces around parentheses so they become separate tokens
    expression = expression.replace("(", " ( ")
    expression = expression.replace(")", " ) ")

    tokens = expression.split()

    for token in tokens:

        # If the token is a number
        if token.isdigit():
            values.push(float(token))

        # Opening parenthesis
        elif token == "(":
            operators.push(token)

        # Closing parenthesis
        elif token == ")":

            while not operators.is_empty() and operators.peek() != "(":
                operator = operators.pop()
                b = values.pop()
                a = values.pop()

                result = apply_operator(a, b, operator)
                values.push(result)

            # Remove the opening parenthesis
            if not operators.is_empty():
                operators.pop()

        # Operator
        elif token in ("+", "-", "*", "/"):

            while (
                not operators.is_empty()
                and operators.peek() != "("
                and precedence(operators.peek()) >= precedence(token)
            ):
                operator = operators.pop()
                b = values.pop()
                a = values.pop()

                result = apply_operator(a, b, operator)
                values.push(result)

            operators.push(token)

        else:
            raise ValueError("Invalid token: " + token)

    # Apply remaining operators
    while not operators.is_empty():

        operator = operators.pop()

        if operator == "(":
            raise ValueError("Unmatched parenthesis.")

        b = values.pop()
        a = values.pop()

        result = apply_operator(a, b, operator)
        values.push(result)

    return values.pop()


def read_input_file(filename):
    """Read expressions from the input file."""

    with open(filename, "r") as file:
        lines = file.readlines()

    return lines


def process_expressions(lines):
    """Evaluate all expressions from the input file."""

    results = []

    for line in lines:
        line = line.strip()

        # Ignore empty lines
        if not line:
            continue

        # Ignore separator lines
        if line == "-----":
            continue

        result = evaluate_expression(line)
        results.append(result)

    return results


def format_result(result):
    """Remove .0 from whole-number results."""

    if result == int(result):
        return str(int(result))

    return str(result)


def write_output_file(filename, results):
    """Write calculated results to the output file."""

    with open(filename, "w") as file:

        for i, result in enumerate(results):

            file.write(format_result(result))

            if i < len(results) - 1:
                file.write("\n-----\n")


def main():
    """Main program."""

    input_file = "input.txt"
    output_file = "output.txt"

    try:
        # Read input
        lines = read_input_file(input_file)

        # Evaluate expressions
        results = process_expressions(lines)

        # Write results
        write_output_file(output_file, results)

        print("Expression evaluation completed successfully.")
        print("Results have been written to output.txt.")

    except FileNotFoundError:
        print("Error: input.txt was not found.")

    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()