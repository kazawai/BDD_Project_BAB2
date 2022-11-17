import enums_bdd


def is_constant(rq: str):
    try:
        n = enums_bdd.Constants(rq).name
        print(n)
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
    check_parentheses(rq)

    # Get the sub-query
    i = 0
    while rq[i] != '(':
        i += 1
    j = i+1
    par_c = 0
    while rq[j] != ')' or par_c != -1:
        j += 1
        if rq[j] == '(':
            par_c += 1
        elif rq[j] == ')':
            par_c -= 1
    sub_rq = rq[i+1:j]
    print(sub_rq)

    pass


if __name__ == '__main__':

    request = None

    while request != "exit":
        print("Please enter your request below ----------- (Enter 'exit' to quit)\n")
        request = input("Request :\t")

        if request == "exit":
            break

        print(process_request(request))

    print("Goodbye !")
