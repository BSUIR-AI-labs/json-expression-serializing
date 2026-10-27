def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_the_highest_operation(expression: str) -> int:
    depth = 0
    fallback = -1
    for i in range(len(expression) - 1, 0, -1):
        if expression[i] == ")": depth += 1
        if expression[i] == "(": depth -= 1
        if depth == 0 and expression[i] in "+-": return i
        if depth == 0 and expression[i] in "*/" and fallback == -1: fallback = i
    return fallback


def parse_power(expression: str, depth: int = 1) -> str:
    if len(expression) == 1 or is_number(expression):
        return f'"{expression}"'
    base, exponent = expression.split("^")
    indent = '\t' * depth
    child = '\t' * (depth + 1)
    return (f'{{\n'
            f'{child}"^": [\n'
            f'{child}\t"{base}",\n'
            f'{child}\t"{exponent}"\n'
            f'{child}]\n'
            f'{indent}}}')


def parse_multiple_or_devide(expression: str, depth: int = 1) -> str:
    if is_number(expression):
        return f'"{expression}"'
    if len(expression) == 1:
        if expression == '-':
            return '"-1"'
        return f'"{expression}"'

    if expression.startswith('(') and expression.endswith(')'):
        paren_depth = 0
        for j, c in enumerate(expression):
            paren_depth += (c == '(') - (c == ')')
            if paren_depth == 0 and j < len(expression) - 1:
                break
        else:
            return parse_binary_plus_or_minus(expression[1:-1], depth)

    indent = '\t' * depth
    child = '\t' * (depth + 1)
    grand = '\t' * (depth + 2)

    if '*' in expression or '/' in expression:
        for i in range(len(expression) - 1, 0, -1):
            if expression[i] in '*/':
                left, right = expression[:i], expression[i + 1:]
                return (f'{{\n'
                        f'{child}"{expression[i]}": [\n'
                        f'{grand}{parse_multiple_or_devide(left, depth + 2)},\n'
                        f'{grand}{parse_multiple_or_devide(right, depth + 2)}\n'
                        f'{child}]\n'
                        f'{indent}}}')
    else:
        if len(expression) == 2:
            return (f'{{\n'
                    f'{child}"*": [\n'
                    f'{grand}{parse_multiple_or_devide(expression[0], depth + 2)},\n'
                    f'{grand}{parse_multiple_or_devide(expression[1], depth + 2)}\n'
                    f'{child}]\n'
                    f'{indent}}}')
        if len(expression) == 3 and expression[1] == '^':
            return parse_power(expression, depth)
        if len(expression) >= 2 and expression[1] == '^':
            return (f'{{\n'
                    f'{child}"*": [\n'
                    f'{grand}{parse_multiple_or_devide(expression[0:2], depth + 2)},\n'
                    f'{grand}{parse_multiple_or_devide(expression[3:], depth + 2)}\n'
                    f'{child}]\n'
                    f'{indent}}}')
        if len(expression) == 1:
            return f'"{expression}"'
        return (f'{{\n'
                f'{child}"*": [\n'
                f'{grand}{parse_multiple_or_devide(expression[0], depth + 2)},\n'
                f'{grand}{parse_multiple_or_devide(expression[1:], depth + 2)}\n'
                f'{child}]\n'
                f'{indent}}}')


def parse_binary_plus_or_minus(expression: str, depth: int = 1) -> str:
    indent = '\t' * depth
    child = '\t' * (depth + 1)
    grand = '\t' * (depth + 2)

    if ('+' in expression or '-' in expression) and '(' in expression:
        i = get_the_highest_operation(expression)
        if i == -1:
            return parse_multiple_or_devide(expression, depth)
        left, right = expression[:i], expression[i + 1:]
        return (f'{{\n'
                f'{child}"{expression[i]}": [\n'
                f'{grand}{parse_binary_plus_or_minus(left, depth + 2)},\n'
                f'{grand}{parse_binary_plus_or_minus(right, depth + 2)}\n'
                f'{child}]\n'
                f'{indent}}}')

    for i in range(len(expression) - 1, 0, -1):
        if expression[i] in '+-':
            left, right = expression[:i], expression[i + 1:]
            return (f'{{\n'
                    f'{child}"{expression[i]}": [\n'
                    f'{grand}{parse_binary_plus_or_minus(left, depth + 2)},\n'
                    f'{grand}{parse_binary_plus_or_minus(right, depth + 2)}\n'
                    f'{child}]\n'
                    f'{indent}}}')

    return parse_multiple_or_devide(expression, depth)


def parsing_expression(expression: str) -> str:
    left, right = expression.split('=')
    return (f'{{\n'
            f'\t"=": [\n'
            f'\t\t{parse_binary_plus_or_minus(left, 2)},\n'
            f'\t\t{parse_binary_plus_or_minus(right, 2)}\n'
            f'\t]\n'
            f'}}')