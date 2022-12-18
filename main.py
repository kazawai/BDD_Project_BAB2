from Class.Operator import *
from enums_bdd import Constants, SPJRUDRequest
from sql_query import *
from Class.Errors import *
import traceback
import os
import readline


global db


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
                raise SyntaxException("There was an error in your parentheses count : Too many closing brackets")
            l_char = stack.pop()
            if char == ']' and l_char != '[':
                raise SyntaxException("There was an error in your parentheses count : Missing opening [")
            if char == ')' and l_char != '(':
                raise SyntaxException("There was an error in your parentheses count : Missing opening (")
    if stack:
        raise SyntaxException("There was an error in your parentheses count : Missing closing brackets")
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
    Recursive function that processes the request.
    Meaning that it ultimately converts the request in a "Query" object and runs a bunch of tests.

    :param rq: The request to process
    :return: The last letter index
    """

    # Get the sub-query
    i = 0
    while i < len(rq) and rq[i] != '(':
        i += 1
    if i == len(rq):
        return create_obj(rq)
    j = i
    while j >= 0 and rq[j] != ',':
        j -= 1
    q = rq[j + 1:i] if j <= i else rq[:i]
    if not SPJRUDRequest.has_value(q) and not Constants.has_value(q):
        raise SyntaxException(f"Not a valid argument {q}")
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

    return create_obj(q, [process_request(arg) for arg in args_l] if not Constants.has_value(q) else args_l)


def create_obj(q: str, args: list = None) -> Operator:

    a = Operator

    match q:
        case SPJRUDRequest.SELECT.value:
            if len(args) > 4:
                raise SyntaxException(f"{q} : Too many arguments, expected 4 got {len(args)}")
            elif len(args) < 4:
                raise MissingExpressionException(f"{q} : Too little arguments, expected 4 got {len(args)}")
            a = Select(args[0], args[1], args[2], args[3])

        case SPJRUDRequest.PROJECTION.value:
            a = Projection([arg for arg in args if isinstance(arg, Attribute)], args[-1])

        case SPJRUDRequest.JOIN.value:
            if len(args) > 2:
                raise SyntaxException(f"{q} : Too many arguments, expected 2 got {len(args)}")
            elif len(args) < 2:
                raise MissingExpressionException(f"{q} : Too little arguments, expected 2 got {len(args)}")
            a = Join(args[0], args[1])

        case SPJRUDRequest.RENAME.value:
            if len(args) > 3:
                raise SyntaxException(f"{q} : Too many arguments, expected 3 got {len(args)}")
            elif len(args) < 3:
                raise MissingExpressionException(f"{q} : Too little arguments, expected 3 got {len(args)}")
            a = Rename(args[0], args[1], args[2])

        case SPJRUDRequest.UNION.value:
            if len(args) > 2:
                raise SyntaxException(f"{q} : Too many arguments, expected 2 got {len(args)}")
            elif len(args) < 2:
                raise MissingExpressionException(f"{q} : Too little arguments, expected 2 got {len(args)}")
            a = Union(args[0], args[1])

        case Constants.TABLE.value:
            if len(args) > 1:
                raise SyntaxException(f"{q} : Too many arguments, expected 1 got {len(args)}")
            elif len(args) < 1:
                raise MissingExpressionException(f"{q} : Too little arguments, expected 1 got {len(args)}")
            a = Table(db, args[0])

        case Constants.CONSTANTS.value:
            if len(args) > 1:
                raise SyntaxException(f"{q} : Too many arguments, expected 1 got {len(args)}")
            elif len(args) < 1:
                raise MissingExpressionException(f"{q} : Too little arguments, expected 1 got {len(args)}")
            a = Constant(args[0])

        case _:
            if q in valid_operators:
                return q
            a = Attribute(q)

    return a


if __name__ == '__main__':

    request = None
    try:
        while request != "exit":
            print("Enter the name of the database you wish to use : ----------- (Enter 'exit' to quit)\n")

            request = input("Database : ")
            print("\n")

            if request == "exit":
                exit(0)

            db = request

            create_db(db)

            while request != "exit" and request != "db_change":
                    print("Please enter your request below ----------- (Enter 'exit' to quit)\n")
                    request = input("Request : ")
                    print("\n")

                    if request == "exit" or request == "db_change":
                        break

                    if request == "commit":
                        commit_queries()
                        continue

                    check_parentheses(request)
                    query = process_request(request)

                    query.run_query()

                    delete_tables(db)
    except KeyboardInterrupt:
        exit(0)
    except SError as e:
        print(f"\033[91m{str(e)}\033[0m")
    finally:
        print("Goodbye !")
        delete_tables(db)
