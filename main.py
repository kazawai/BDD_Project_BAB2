import enums_bdd


def is_constant(rq: str):
    try:
        n = enums_bdd.Constants(rq).name
        return True
    except Exception:
        return False


def get_request_content(rq: str):

    pass


def check_parentheses(rq: str):
    stack = []
    for char in rq:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    if stack:
        raise SyntaxError("There was an error in your parentheses count")
    return True


def process_request(rq: str):
    # Get the sub-query
    i = 0
    while rq[i] != '(':
        i += 1
    query = rq[:i]
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
    max_index = []
    stack = []
    base_i = 0
    for i in range(len(args)):
        if args[i] == '(':
            stack.append(args[i])
        if args[i] == ')':
            # We assume that the expression is balanced since we checked it earlier
            stack.pop()
            if not stack:
                max_index.append((base_i, i+1))
                base_i = i + 2

    args_l = [args[i:j] for (i,j) in max_index] + args[max_index.pop()[-1] + 1:].split(',') if len(max_index) != 0 else args.split(',')
    
    q = enums_bdd.Query(query, args_l)
    if is_constant(query):
        print(f"Constant found ! : {q.query} || {q.arg_list}")
        return None
    print(f"There was not any sub-request to {rq}" if args is None else f"{rq} : {q.query} || {q.arg_list}")

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
