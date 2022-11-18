from enums_bdd import SPJRUDRequest, Constants


class Operator:

    def __init__(self, attr_list):
        self.a_list = attr_list

    def get_name(self):
        return ""


def check_query(query: Operator) -> bool:
    # TODO : Check the arguments (number and form)
    match query.get_name():
        case SPJRUDRequest.SELECT.value:
            return True

        case SPJRUDRequest.PROJECTION.value:
            return True

        case SPJRUDRequest.JOIN.value:
            return True

        case SPJRUDRequest.RENAME.value:
            if not isinstance(query.a_list[0], str):
                raise SyntaxError("First attribute of \"Rename\" has to be of type : \'str\'")
            if not isinstance(query.a_list[1], str):
                raise SyntaxError("Second attribute of \"Rename\" has to be of type : \'str\'")

            # TODO : Check if the first name is in the relation
            return True

        case SPJRUDRequest.UNION.value:
            return True

        case Constants.RELATION.value:
            return True

        case Constants.CONSTANTS.value:
            return True
