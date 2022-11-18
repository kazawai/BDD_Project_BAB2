from enum import Enum


class SPJRUDRequest(Enum):
    SELECT = "Select"
    PROJECTION = "Proj"
    JOIN = "Join"
    RENAME = "Rename"
    UNION = "Union"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Constants(Enum):
    RELATION = "Rel"
    CONSTANTS = "Cst"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Query:

    def __init__(self, query: str, arg_list: list):
        self.query = query
        self.arg_list = arg_list
        if not self.check_query():
            raise SyntaxError(f"Query \"{self.query}\" not recognized")
        self.check_args()

    def check_query(self):
        return Constants.has_value(self.query) or SPJRUDRequest.has_value(self.query)

    def check_args(self):
        # TODO : Check the arguments (number and form)
        match self.query:
            case SPJRUDRequest.SELECT.value:
                pass
            case SPJRUDRequest.PROJECTION.value:
                pass
            case SPJRUDRequest.JOIN.value:
                pass
            case SPJRUDRequest.RENAME.value:
                pass
            case SPJRUDRequest.UNION.value:
                pass
            case Constants.RELATION.value:
                pass
            case Constants.CONSTANTS.value:
                pass
