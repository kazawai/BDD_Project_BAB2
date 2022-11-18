from enums_bdd import SPJRUDRequest, Constants


class Operator:

    def __init__(self, attr_list):
        self.a_list = attr_list

    def __get_name__(self):
        return ""


def check_query(query: Operator) -> bool:
    # TODO : Check the arguments (number and form)
    match query.__get_name__():
        case SPJRUDRequest.SELECT.value:
            if not isinstance(query.a_list[0], str):
                raise SyntaxError("First attribute of \"Select\" has to be of type : \'str\'")
            if not query.a_list[1] == "=" or query.a_list[1] =="!=":
                raise SyntaxError("Second attribute of \"Select\" has to be = or !=")
            if not isinstance(query.a_list[2], str):
                raise SyntaxError("Third attribute of \"Select\" has to be of type : \'str\'")
            if not isinstance(query.a_list[3], Constants.CONSTANTS):
                raise SyntaxError("Fourth attribute of \"Select\" has to be an Constants")
            return True

        case SPJRUDRequest.PROJECTION.value:
            if not isinstance(query.a_list[0], str):
                raise SyntaxError("First attribute of \"Projection\" has to be of type : \'str\'")
            if not isinstance(query.a_list[1], Constants.CONSTANTS ):
                raise SyntaxError("Second attribute of \"Projection\" has to be of type : \'str\'")
            return True

        case SPJRUDRequest.JOIN.value:
            if not isinstance(query.a_list[0], str):
                raise SyntaxError("First attribute of \"Join\" has to be of type : \'str\'")
            if not isinstance(query.a_list[1], str):
                raise SyntaxError("Second attribute of \"Join\" has to be of type : \'str\'")
            return True

        case SPJRUDRequest.RENAME.value:
            if not isinstance(query.a_list[0], str):
                raise SyntaxError("First attribute of \"Rename\" has to be of type : \'str\'")
            if not isinstance(query.a_list[1], str):
                raise SyntaxError("Second attribute of \"Rename\" has to be of type : \'str\'")
            if not isinstance(query.a_list[2], Constants.CONSTANTS ):
                raise SyntaxError("Third attribute of \"Rename\" has to be of type : \'str\'")

            # TODO : Check if the first name is in the relation
            return True

        case SPJRUDRequest.UNION.value:
            if not isinstance(query.a_list[0], str):
                raise SyntaxError("First attribute of \"Union\" has to be of type : \'str\'")
            if not isinstance(query.a_list[1], str):
                raise SyntaxError("Second attribute of \"Union\" has to be of type : \'str\'")
            return True
        
        case SPJRUDRequest.DIFFERENCE.value:
            if not isinstance(query.a_list[0], str):
                raise SyntaxError("First attribute of \"Difference\" has to be of type : \'str\'")
            if not isinstance(query.a_list[1], str):
                raise SyntaxError("Second attribute of \"Difference\" has to be of type : \'str\'")
            return True

        case Constants.RELATION.value:
            if not Constants.RELATION.has_value == type(str):
                raise SyntaxError("The attibute of \" Relation\" has to be of type : \'str\'")
            return True

        case Constants.CONSTANTS.value:
            if not Constants.CONSTANTS.has_value == type(str):
                raise SyntaxError("The attibute of \" Cconstants\" has to be of type : \'str\'")
            return True
