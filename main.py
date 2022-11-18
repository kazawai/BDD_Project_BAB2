from enums_bdd import Constants, SPJRUDRequest
from Operator.operator import Operator


def is_constant(rq: str) -> bool:
    """
    Check if the query "rq" is a constant or not.

    :param rq: The query
    :return: True if the query is a constant, False if not
    """
    return Constants.has_value(rq)


def get_request_content(rq: str):

    pass


def check_parentheses(rq: str) -> bool:
    """
    Check the parentheses of a query.

    :param rq: The query/request to check
    :return: True if success
    :raise SyntaxError: If there was a parentheses problem
    """
    stack = []
    for char in rq:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                raise SyntaxError("There was an error in your parentheses count")
            stack.pop()
    if stack:
        raise SyntaxError("There was an error in your parentheses count")
    return True


def parse_arguments(args: str) -> list:
    """
    Parse the arguments. Separate the normal arguments from sub-queries

    :param args: The arguments
    :return: A list of the separated arguments
    """

    max_index = []
    stack = []
    comma_c = 0
    base_i = 0
    for i in range(len(args)):
        if args[i] == ',':
            comma_c += 1
            if not stack:
                base_i = i + 1
        if args[i] == '(':
            stack.append(args[i])
        if args[i] == ')':
            # We assume that the expression is balanced since we checked it earlier
            stack.pop()
            if not stack:
                max_index.append((base_i, i + 1, comma_c))
                base_i = i + 2

    # TODO : Check the order and re-arrange the element
    return [args[i:j] for (i, j, k) in max_index] + [args.split(',')[k] for k in range(comma_c) if k not in [c for (i, j, c) in max_index]]


def create_query(query, args_l) -> Operator:
    """
    Instantiate the query to the right type

    :param query: The query
    :param args_l: The arguments
    :return: An Operator object
    """

    # TODO : implement
    pass


def process_request(rq: str) -> int:
    """
    Recursive function that process the request.
    Meaning that it ultimately converts the request in a "Query" object and runs a bunch of tests.

    :param rq: The request to process
    :return: The last letter index
    """
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
    
    q = create_query(query, args_l)
    if is_constant(query):
        #print(f"Constant found ! : {q.query} || {q.arg_list}")
        return None
    #print(f"There was not any sub-request to {rq}" if args is None else f"{rq} : {q.query} || {q.arg_list}")

    return j


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
