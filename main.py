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
    parentheses = 0
    for i in range(len(rq)):
        if rq[i] == '(':
            parentheses += 1
        elif rq[i] == ')':
            parentheses -= 1
    if parentheses != 0:
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
    q = enums_bdd.Query(query, args.split(','))
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
