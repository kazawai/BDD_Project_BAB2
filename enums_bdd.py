from enum import Enum


class SPJRUDRequest(Enum):
    SELECT = "Select"
    PROJECTION = "Proj"
    JOIN = "Join"
    RENAME = "Rename"
    UNION = "Union"
    DIFFERENCE = "Diff"
    INSERT = "Insert"
    SHOWTABLES = "showtables"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Constants(Enum):
    ATTRIBUTE = ""
    TABLE = "Rel"
    CONSTANTS = "Cst"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
