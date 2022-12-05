from enums_bdd import Constants, SPJRUDRequest
from Class.Operator import *


def is_constant(rq: str) -> bool:
    """
    Check if the query "rq" is a constant or not.

    :param rq: The query
    :return: True if the query is a constant, False if not
    """
    return Constants.has_value(rq)


def check_parentheses(rq: str) -> bool:
    """
    Check the parentheses of a query.

    :param rq: The query/request to check
    :return: True if success
    :raise SyntaxError: If there was a parentheses problem
    """
    stack = []
    front_char = ['(', '[']
    back_char = [')', ']']
    for char in rq:
        if char in front_char:
            stack.append(char)
        elif char in back_char:
            if not stack:
                raise SyntaxError("There was an error in your parentheses count")
            l_char = stack.pop()
            if char == ']' and l_char != '[':
                raise SyntaxError("There was an error in your parentheses count")
            if char == ')' and l_char != '(':
                raise SyntaxError("There was an error in your parentheses count")
    if stack:
        raise SyntaxError("There was an error in your parentheses count")
    return True


def parse_arguments(args: str) -> list:
    """
    Parse the arguments. Separate the normal arguments from sub-queries

    :param args: The arguments
    :return: A list of the separated arguments
    """

    # Proj(Rel(a, b), c) || Proj(c, Rel(a, b), d) || Proj(c, Rel(a))
    max_index = []
    stack = []
    comma_c = 0
    comma_i = 0
    base_i = 0
    for i in range(len(args)):
        if args[i] == ',':
            comma_c += 1
            if stack:
                comma_i += 1
            if not stack:
                base_i = i + 1
        if args[i] == '(' or args[i] == '[':
            stack.append(args[i])
        if args[i] == ')' or args[i] == ']':
            # We assume that the expression is balanced since we checked it earlier
            stack.pop()
            if not stack and args[i] == ')':
                max_index.append((base_i, i + 1, comma_c, comma_i))
                base_i = i + 1
                comma_i = 0

    sub_queries = [args[i:j] for (i, j, k, l) in max_index]
    constants = [args.split(',')[k] for k in range(comma_c + 1) if (not any(k in a for a in [(a for a in range(c - l, c + 1)) for (i, j, c, l) in max_index]))]

    # TODO : Check the order and re-arrange the element
    return sub_queries + constants


def process_request(rq: str) -> int:
    """
    Recursive function that process the request.
    Meaning that it ultimately converts the request in a "Query" object and runs a bunch of tests.

    :param rq: The request to process
    :return: The last letter index
    """

    # TODO : Recursion problem when typing 'Proj(Proj(Rel(a,b),b),Proj(c,Rel(a,b),d)'

    # Get the sub-query
    i = 0
    while rq[i] != '(':
        i += 1
    j = i
    while j >= 0 and rq[j] != ',':
        j -= 1
    query = rq[j+1:i] if j <= i else rq[:i]
    j = i
    par_c = 0
    while rq[j] != ')' or par_c != -1:
        j += 1
        if rq[j] == '(':
            par_c += 1
            k = process_request(rq[i + 1:])
            if k is not None:
                j = k + len(query)
        elif rq[j] == ')':
            par_c -= 1

    args = rq[i+1:j]

    # Find sub-queries in arguments (that have to not be separated)
    args_l = parse_arguments(args)



    if is_constant(query):
        print(f"Constant found ! : {query} || {args_l}")
        return None
    print(f"There was not any sub-request to {rq}" if args is None else f"{rq} : {query} || {args_l}")

    return j


def create_obj(query: str, args: list) -> Operator:

    a = Operator()

    match query:
        case SPJRUDRequest.SELECT.value:
            a = Select(args[0], args[1])

        case SPJRUDRequest.PROJECTION.value:
            a = Projection(args[0], args[1])

        case SPJRUDRequest.JOIN.value:
            a = Join(args[0], args[1])

        case SPJRUDRequest.RENAME.value:
            a = Rename(args[0], args[1])

        case SPJRUDRequest.UNION.value:
            a = Union(args[0], args[1])

        case Constants.ATTRIBUTE.value:
            a = Attribute(args[0])

        case Constants.CONSTANTS.value:
            a = Constants(args[0])

    return a


if __name__ == '__main__':

    request = None

    while request != "exit":
        print("Please enter your request below ----------- (Enter 'exit' to quit)\n")
        request = input("Request :\t")

        if request == "exit":
            break

        check_parentheses(request)
        process_request(request)

    print("Goodbye !")
