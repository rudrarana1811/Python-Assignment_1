import re


class ExpressionParser:
    def __init__(self, tokens, get_variable):
        self.tokens = tokens
        self.position = 0
        self.get_variable = get_variable

    def parse(self):
        value = self.parse_expression()

        if self.position != len(self.tokens):
            raise ValueError

        return value

    def parse_expression(self):
        value = self.parse_term()

        while self.position < len(self.tokens):
            operator = self.tokens[self.position]

            if operator not in ("+", "-"):
                break

            self.position += 1
            right = self.parse_term()

            if operator == "+":
                value += right
            else:
                value -= right

        return value

    def parse_term(self):
        value = self.parse_factor()

        while self.position < len(self.tokens):
            if self.tokens[self.position] != "*":
                break

            self.position += 1
            value *= self.parse_factor()

        return value

    def parse_factor(self):
        if self.position >= len(self.tokens):
            raise ValueError

        token = self.tokens[self.position]
        self.position += 1

        if token.isdigit():
            return int(token)

        if token == "(":
            value = self.parse_expression()

            if self.position >= len(self.tokens):
                raise ValueError

            if self.tokens[self.position] != ")":
                raise ValueError

            self.position += 1
            return value

        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            return self.get_variable(token)

        raise ValueError


def tokenize(expression):
    # Convert the expression into numbers, names and operators
    tokens = re.findall(
        r"[A-Za-z_][A-Za-z0-9_]*|\d+|[()+\-*]",
        expression
    )

    if "".join(tokens) != re.sub(r"\s+", "", expression):
        raise ValueError

    return tokens


print("Recursive Expression Engine")
print("Enter number of variables:")
v = int(input())

variables = {}

print("Enter variable definitions:")
for i in range(v):
    print(f"Definition {i + 1}:")
    line = input()

    if "=" not in line:
        print("INVALID")
        raise SystemExit

    name, expression = line.split("=", 1)
    name = name.strip()

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        print("INVALID")
        raise SystemExit

    variables[name] = expression.strip()

print("Enter expression to evaluate:")
target = input()

state = {}
memo = {}


def evaluate_variable(name):
    if name in memo:
        return memo[name]

    if name not in variables:
        raise ValueError

    if state.get(name) == 1:
        raise RuntimeError

    state[name] = 1

    tokens = tokenize(variables[name])

    parser = ExpressionParser(tokens, evaluate_variable)
    value = parser.parse()

    state[name] = 2
    memo[name] = value

    return value


try:
    result = ExpressionParser(
        tokenize(target),
        evaluate_variable
    ).parse()

    print(result)

except RuntimeError:
    print("CYCLE")

except Exception:
    print("INVALID")
