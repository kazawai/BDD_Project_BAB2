from SQL import *


class Operator:
    """
    Abstract class for the operators
    Should never be called alone
    """

    attr = None

    def format(self, query):
        s = ""
        try:
            length = max(max(len(str(element)) for row in query for element in row), max(len(str(attr[0])) for attr in self.attr)) + 2
        except ValueError:
            raise ValueError("Your query returned an empty table")
        s += "".join(str(attr[0]).ljust(length) + "| " for attr in self.attr) + "\n"
        s += "+-".join("-"*length for i in range(len(self.attr))) + "+\n"
        for row in query:
            s += "".join(str(el).ljust(length)+"| " for el in row) + "\n"
        return s


class SelfOperator(Operator):

    query = ""

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
        self.query = ""


valid_operators = ["=", ">=", "<=", "<", ">", "!="]


class Select(SelfOperator):

    def __init__(self, attr1: Attribute, op: str, attr2, table: Table):
        attr = [attr1, op, attr2]
        super(Select, self).__init__(attr, table)

        assert isinstance(attr1, Attribute)
        assert isinstance(attr2, Constant) or isinstance(attr2, Attribute)
        assert op in valid_operators
        # TODO : check if attr1 and attr2 are in the table (if attr2 is an Attribute)


class Projection(SelfOperator):

    def __init__(self, attr_list, table: Table):
        super(Projection, self).__init__(attr_list, table)

        if any(not isinstance(attr, Attribute) for attr in attr_list):
            raise TypeError("All attributes must be of class 'Attribute'")
        # TODO : check if attributes in table


class Rename(SelfOperator):

    def __init__(self, arg1: Attribute, arg2, table: Table):
        args = [arg1, arg2]
        super(Rename, self).__init__(args, table)

        assert isinstance(arg1, Attribute)
        assert isinstance(arg2, Constant)
        # TODO : check if arg1 in the table and arg2 not already in the table


class Join(MultiOperator):

    def __init__(self, rel1, rel2):
        super(Join, self).__init__(rel1, rel2)

        assert rel1.attr == rel2.attr
        # TODO : the query


class Union(MultiOperator):

    def __init__(self, rel1, rel2):
        super(Union, self).__init__(rel1, rel2)

        assert rel1.attr == rel2.attr
        # TODO : the query

