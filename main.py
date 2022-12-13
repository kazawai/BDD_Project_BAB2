from Class.Operator import *
from enums_bdd import Constants, SPJRUDRequest
from sql_query import *


global db


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

    return constants + sub_queries


def process_request(rq: str) -> Operator:
    """
    Recursive function that process the request.
    Meaning that it ultimately converts the request in a "Query" object and runs a bunch of tests.

    :param rq: The request to process
    :return: The last letter index
    """

    # Get the sub-query
    i = 0
    while i < len(rq) and rq[i] != '(':
        i += 1
    if i == len(rq):
        print(f"Constant found : {rq}")
        return create_obj(rq)
    j = i
    while j >= 0 and rq[j] != ',':
        j -= 1
    q = rq[j + 1:i] if j <= i else rq[:i]
    j = i + 1
    par_c = 0

    while rq[j] != ')' or par_c != -1:
        if rq[j] == '(':
            par_c += 1
        elif rq[j] == ')':
            par_c -= 1
            if par_c == -1:
                break
        j += 1

    args = rq[i+1:j]

    # Find sub-queries in arguments (that have to not be separated)
    args_l = parse_arguments(args)

    if is_constant(q):
        print(f"Constant found ! : {q} || {args_l}")
    print(f"There was not any sub-request to {rq}" if args is None else f"{rq} : {q} || {args_l}")

    return create_obj(q, [process_request(arg) for arg in args_l] if not is_constant(q) else args_l)


def create_obj(q: str, args: list = None) -> Operator:

    a = Operator
    print(args)

    match q:
        case SPJRUDRequest.SELECT.value:
            a = Select(args[0], args[1], args[2], args[3])

        case SPJRUDRequest.PROJECTION.value:
            a = Projection([arg for arg in args if isinstance(arg, Attribute)], args[-1])

        case SPJRUDRequest.JOIN.value:
            a = Join(args[0], args[1])

        case SPJRUDRequest.RENAME.value:
            a = Rename(args[0], args[1], args[2])

        case SPJRUDRequest.UNION.value:
            a = Union(args[0], args[1])

        case Constants.TABLE.value:
            a = Table(db, args[0])

        case Constants.CONSTANTS.value:
            a = Constant(args[0])

        case _:
            a = Attribute(q)

    print(f"{q} |||| {a}")

    return a


if __name__ == '__main__':

    request = None

    while request != "exit":
        print("Enter the name of the database you wish to use : ----------- (Enter 'exit' to quit)\n")

        request = input("Database :\t")
        print("\n")

        if request == "exit":
            break

        db = request

        create_db(db)

        while request != "exit" and request != "db_change":
            print("Please enter your request below ----------- (Enter 'exit' to quit)\n")
            request = input("Request :\t")
            print("\n")

            if request == "exit" or request == "db_change":
                break

            check_parentheses(request)
            query = process_request(request)

            run_query(db, query)


    print("Goodbye !")
