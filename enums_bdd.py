from enum import Enum


class SPJRUDRequest(Enum):
    SELECT = "Select"
    PROJECTION = "Proj"
    JOIN = "Join"
    RENAME = "Rename"
    UNION = "Union"


class Constants(Enum):
    RELATION = "Rel"
    CONSTANTS = "Cst"


class Query:

    def __init__(self, query: str, arg_list: list):
        self.query = query
        self.arg_list = arg_list
        self.check_args()

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
