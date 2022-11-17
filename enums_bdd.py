import enum


class SPJRUDRequest(enum.Enum):
    SELECT = "Select"
    PROJECTION = "Proj"
    JOIN = "Join"
    RENAME = "Rename"
    UNION = "Union"


class Constants(enum.Enum):
    RELATION = "Rel"
    CONSTANTS = "Cst"
