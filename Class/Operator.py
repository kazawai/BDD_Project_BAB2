from Class.SQL import *
from sql_query import run_query


class Operator:
    """
    Abstract class for the operators
    Should never be called alone
    """

    attr = None
    query = ""
    result = None
    db = None

    def format(self, query):
        try:
            length = max(max(len(str(element)) for row in self.result for element in row), max(len(str(attr[0])) for attr in self.attr)) + 2
        except ValueError:
            raise ValueError("Your query returned an empty table")
        s = "".join(str(att[0]).ljust(length) + "| " for att in self.attr) + "\n" + "+-".join("-"*length for i in range(len(self.attr))) + "+\n" + \
            "".join(["".join(str(el).ljust(length) + "| " for el in row) + "\n" for row in query])
        return s

    def __str__(self):
        return str(self.__class__)

    def run_query(self):
        self.result = run_query(self.db, self.query)
        print(self.format(self.result))


class SelfOperator(Operator):

    def __init__(self, arg, table):

        assert isinstance(table, Table) or isinstance(table, SelfOperator) or isinstance(table, MultiOperator)

        self.table = table
        self.name = table.name
        self.db = table.db
        self.attr = table.attr
        self.arg = arg


class MultiOperator(Operator):

    def __init__(self, rel1, rel2):

        assert isinstance(rel1, Table) or isinstance(rel1, SelfOperator) or isinstance(rel1, MultiOperator)

        assert isinstance(rel2, Table) or isinstance(rel2, SelfOperator) or isinstance(rel2, MultiOperator)

        self.rel1 = rel1
        self.rel2 = rel2
        self.db = rel1.db

        self.name = f"({rel1}, {rel2})"

        self.attr = None
        self.query = None


valid_operators = ["=", ">=", "<=", "<", ">", "!="]


class Select(SelfOperator):

    def __init__(self, attr1: Attribute, op: str, attr2, table: Table):
        attr = [attr1, op, attr2]
        super(Select, self).__init__(attr, table)

        assert isinstance(attr1, Attribute)
        assert isinstance(attr2, Constant) or isinstance(attr2, Attribute)
        assert op in valid_operators
        # TODO : check if attr1 and attr2 are in the table (if attr2 is an Attribute)

        # TODO : build the query
        self.query = f"SELECT DISTINCT * FROM {str(table)} WHERE {str(attr1)} {op} " + f"\"{str(attr2)}\"" if isinstance(attr2, Constant) else f"{str(attr2)}"


class Projection(SelfOperator):

    def __init__(self, attr_list: list, table: Table):
        super(Projection, self).__init__(attr_list, table)

        self.attr_l = attr_list

        if any(not isinstance(attr, Attribute) for attr in attr_list):
            raise TypeError("All attributes must be of class 'Attribute'")
        # TODO : check if attributes in table

        self.query = "SELECT DISTINCT " + ", ".join([att.get_name() for att in attr_list]) + f" FROM {table.name}"

    def format(self, query):
        try:
            length = max(max(len(str(element)) for row in query for element in row), max(len(str(attr[0])) for attr in self.attr)) + 2
        except ValueError:
            raise ValueError("Your query returned an empty table")
        s = "".join(str(att.get_name()).ljust(length) + "| " for att in self.attr_l) + "\n" + "+-".join("-" * length for i in range(len(self.attr_l))) + "+\n" + \
            "".join(["".join(str(el).ljust(length) + "| " for el in row) + "\n" for row in query])
        return s


class Rename(SelfOperator):

    def __init__(self, arg1: Attribute, arg2: Constant, table: Table):
        args = [arg1, arg2]
        super(Rename, self).__init__(args, table)

        self.arg2 = arg2

        assert isinstance(arg1, Attribute)
        assert isinstance(arg2, Constant)
        # TODO : check if arg1 in the table and arg2 not already in the table

        # Building the query
        self.query = f"SELECT {arg1.a_name} AS {arg2.name} FROM {table.name};"

    def format(self, query):
        try:
            length = max(max(len(str(element)) for row in self.result for element in row), max(len(str(attr[0])) for attr in self.attr)) + 2
        except ValueError:
            raise ValueError("Your query returned an empty table")
        s = "".join(str(self.arg2.name).ljust(length) + "| ") + "\n" + "+-".join("-" * (length // 2)) + "+\n" + \
            "".join(["".join(str(el).ljust(length) + "| " for el in row) + "\n" for row in query])
        return s


class Join(MultiOperator):

    def __init__(self, rel1, rel2):
        super(Join, self).__init__(rel1, rel2)

        assert rel1.attr == rel2.attr

        self.query = f"SELECT DISTINCT FROM {str(rel1)} JOIN {str(rel2)}"

    def format(self, query):
        try:
            length = max(max(len(str(element)) for row in query for element in row), max(len(str(attr[0])) for attr in self.attr)) + 2
        except ValueError:
            raise ValueError("Your query returned an empty table")
        s = "".join(str(self.arg2.name).ljust(length) + "| ") + "\n" + "+-".join("-" * (length // 2)) + "+\n" + \
            "".join(["".join(str(el).ljust(length) + "| " for el in row) + "\n" for row in query])
        return s


class Union(MultiOperator):

    def __init__(self, rel1, rel2):
        super(Union, self).__init__(rel1, rel2)

        assert rel1.attr == rel2.attr

        self.query = f"SELECT DISTINCT * FROM {rel1} UNION SELECT DISTINCT * FROM {rel2}"

    def format(self, query):
        try:
            length = max(max(len(str(element)) for row in query for element in row), max(len(str(attr[0])) for attr in self.attr)) + 2
        except ValueError:
            raise ValueError("Your query returned an empty table")
        s = "".join(str(self.arg2.name).ljust(length) + "| ") + "\n" + "+-".join("-" * (length // 2)) + "+\n" + \
            "".join(["".join(str(el).ljust(length) + "| " for el in row) + "\n" for row in query])
        return s
