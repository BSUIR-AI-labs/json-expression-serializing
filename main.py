import validation
import parsing
import saving



#TODO visual interface
def main(expression: str):
    expression = validation.remove_unary_plus(expression)
    if validation.is_valid_expression(expression):
        parsed_expression = parsing.parsing_expression(expression)
        saving.save_json(parsed_expression)

    else:
        print("There is some problems with parsing. Please, check your expression.")