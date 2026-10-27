def all_brackets_are_closed(expression: str) -> bool:
    stack = []
    for c in expression:
        if c == '(': stack.append('(')
        elif c == ')':
            if not stack: return False
            stack.pop()
    return not stack


def brackets_are_not_null(expression: str) -> bool:
    return '()' not in expression and ')(' not in expression


def is_letter(expression: str) -> bool:
    return expression in "qwertyuiopasdfghjklzxcvbnm"


def is_digit(expression: str) -> bool:
    return expression in '0123456789'


def is_bracket(expression: str) -> bool:
    return expression in "()"


def is_operand(expression: str) -> bool:
    return expression in '+-*/^'


def operands_are_binary(expression: str) -> bool:
    for i in range(len(expression)):
        if expression[i] == '-' and (i == 0 or expression[i - 1] in '(*/=+-^'):
            continue
        if expression[i] in "+-*/^":
            if i == 0: return False
            if i == len(expression) - 1: return False
            if (
                expression[i - 1] != ')' and
                not is_letter(expression[i - 1]) and
                not is_digit(expression[i - 1])
            ): return False
            if (
                expression[i + 1] != '(' and
                not is_letter(expression[i + 1]) and
                not is_digit(expression[i + 1]) and
                expression[i + 1] != '-'
            ): return False
    return True


def is_valid_equal(expression: str) -> bool:
    if expression.count('=') != 1: return False
    i = expression.index('=')
    if i == 0 or i == len(expression) - 1: return False
    left = expression[i - 1]
    right = expression[i + 1]
    if left != ')' and not is_letter(left) and not is_digit(left): return False
    if right != '(' and not is_letter(right) and not is_digit(right) and right != '-': return False
    return True


def has_invalid_symbols(expression: str) -> bool:
    for i in range(len(expression)):
        if expression[i] == '=':
            continue
        if expression[i] == '.':
            if i == 0 or i == len(expression) - 1: return False
            if not is_digit(expression[i - 1]) or not is_digit(expression[i + 1]): return False
            continue
        if (
            not is_letter(expression[i]) and
            not is_digit(expression[i]) and
            not is_bracket(expression[i]) and
            not is_operand(expression[i])
        ): return False
    return True


def dots_are_sane(expression: str) -> bool:
    dots = 0
    for c in expression:
        if c == '.':
            dots += 1
            if dots > 1: return False
        elif c in "+-*/^()=":
            dots = 0
    return True


def remove_unary_plus(expression: str) -> str:
    result = ''
    for i in range(len(expression)):
        if expression[i] == "+":
            if i == 0 or expression[i - 1] == '(' or is_operand(expression[i - 1]): continue
        result += expression[i]
    return result


def is_valid_expression(expression: str) -> bool:
    expression = expression.replace(" ", '')
    return (
        is_valid_equal(expression) and
        operands_are_binary(expression) and
        all_brackets_are_closed(expression) and
        brackets_are_not_null(expression) and
        has_invalid_symbols(expression) and
        dots_are_sane(expression)
    )