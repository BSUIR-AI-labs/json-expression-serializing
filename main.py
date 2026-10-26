def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def parse_power(expression: str) -> dict:
    if len(expression) == 1 or is_number(expression): return expression
    base, exponent = expression.split("^")
    return {"^": [base, exponent]}


def get_the_highest_operation(expression: str) -> int:
    depth = 0
    fallback = -1
    for i in range(len(expression) - 1, 0, -1):
        if expression[i] == ")": depth += 1
        if expression[i] == "(": depth -= 1
        if depth == 0 and expression[i] in "+-": return i
        if depth == 0 and expression[i] in "*/" and fallback == -1: fallback = i
    return fallback


def parse_multiple_or_devide(expression: str) -> any:
    if is_number(expression): return expression
    if len(expression) == 1:
        if expression == '-': return "-1"
        return expression
    if expression.startswith('(') and expression.endswith(')'):
        depth = 0
        for j, c in enumerate(expression):
            depth += (c == '(') - (c == ')')
            if depth == 0 and j < len(expression) - 1: break
        else:
            return parse_binary_plus_or_minus(expression[1:-1])
    if '*' in expression or '/' in expression:
        for i in range(len(expression) - 1, 0, -1):
            if expression[i] in '*/':
                left, right = expression[:i], expression[i + 1:]
                return {expression[i]: [parse_multiple_or_devide(left), parse_multiple_or_devide(right)]}
    else:
        if len(expression) == 2: return {"*": [parse_multiple_or_devide(expression[0]), parse_multiple_or_devide(expression[1])]}
        if len(expression) == 3 and expression[1] == '^': return parse_power(expression)
        if len(expression) >= 2 and expression[1] == '^': return {"*": [parse_multiple_or_devide(expression[0:2]), parse_multiple_or_devide(expression[3:])]}
        if len(expression) == 1: return expression
        return {"*": [parse_multiple_or_devide(expression[0]), parse_multiple_or_devide(expression[1:])]}


def parse_binary_plus_or_minus(expression: str) -> any:
    if ('+' in expression or '-' in expression) and '(' in expression:
        i = get_the_highest_operation(expression)
        if i == -1: return parse_multiple_or_devide(expression)
        left, right = expression[:i], expression[i + 1:]
        return {expression[i]: [parse_binary_plus_or_minus(left), parse_binary_plus_or_minus(right)]}
    for i in range(len(expression) - 1, 0, -1):
        if expression[i] in '+-':
            left, right = expression[:i], expression[i + 1:]
            return {expression[i]: [parse_binary_plus_or_minus(left), parse_binary_plus_or_minus(right)]}
    return parse_multiple_or_devide(expression)


def expression_serializing(expression: str) -> dict:
    left, right = expression.split("=")
    return {'=': [parse_binary_plus_or_minus(left), parse_binary_plus_or_minus(right)]}