from Class.SQL import *
from sql_query import *


class Operator:
    """
    Abstract class for the operators
    Should never be called alone
    """

    def __init__(self):
        self.attr = None
        self.query = ""
        self.result = None
        self.db = None
        self.commit_query = ""

    def format(self, query):
        try:
            length = max(max(len(str(element)) for element in self.result.attr), max(len(str(attr[0])) for attr in self.attr)) + 2
        except ValueError:
            raise ValueError("Your query returned an empty table")
        s = "".join(str(att[0]).ljust(length) + "| " for att in self.attr) + "\n" + "+-".join("-"*length for i in range(len(self.attr))) + "+\n" + \
            "".join(["".join(str(el).ljust(length) + "| " for el in row) + "\n" for row in query])
        return s

    def __str__(self):
        return str(self.__class__.__name__)

    def run_query(self):
        self.result = run_query(self.db, self)
        print(self.format(self.result.row))
        return self.result


class SelfOperator(Operator):

    def __init__(self, arg, table):
        super().__init__()

        assert isinstance(table, Table) or isinstance(table, SelfOperator) or isinstance(table, MultiOperator)

        self.table = table
        self.name = table.name
        self.db = table.db
        self.attr = table.attr
        self.arg = arg

    def __str__(self):
        return super().__str__() + self.name


class MultiOperator(Operator):

    def __init__(self, rel1, rel2):
        super().__init__()

        assert isinstance(rel1, Table) or isinstance(rel1, SelfOperator) or isinstance(rel1, MultiOperator)

        assert isinstance(rel2, Table) or isinstance(rel2, SelfOperator) or isinstance(rel2, MultiOperator)

        self.rel1 = rel1
        self.rel2 = rel2
        self.db = rel1.db

        self.name = f"({rel1}, {rel2})"

        self.attr = None
        self.query = None

    def __str__(self):
        return super().__str__() + self.name


valid_operators = ["=", ">=", "<=", "<", ">", "!="]


class Select(SelfOperator):

    def __init__(self, attr1: Attribute, op: str, attr2, table):
        attr = [attr1, op, attr2]
        super(Select, self).__init__(attr, table)

        assert isinstance(attr1, Attribute)
        assert isinstance(attr2, Constant) or isinstance(attr2, Attribute)
        assert op in valid_operators
        assert isinstance(table, Table) or isinstance(table, Operator)
        # TODO : check if attr1 and attr2 are in the table (if attr2 is an Attribute)
        if isinstance(table, Operator):
            table = table.run_query()

        # TODO : build the query
        self.query = f"SELECT * FROM [{str(table.name)}] WHERE {attr1.a_name} {op} " + (f"\"{attr2.name}\"" if isinstance(attr2, Constant) else f"{attr2.a_name}")

        self.commit_query = self.query


class Projection(SelfOperator):

    def __init__(self, attr_list: list, table):
        super(Projection, self).__init__(attr_list, table)

        self.attr_l = attr_list

        if any(not isinstance(attr, Attribute) for attr in attr_list):
            raise TypeError("All attributes must be of class 'Attribute'")

        assert isinstance(table, Table) or isinstance(table, Operator)
        if isinstance(table, Operator):
            table = table.run_query()
        # TODO : check if attributes in table

        self.query = "SELECT DISTINCT " + ", ".join([att.get_name() for att in attr_list]) + f" FROM {table.name}"

        self.commit_query = self.query

    def format(self, query):
        try:
            length = max(max(len(str(element)) for row in query for element in row), max(len(str(attr[0])) for attr in self.attr)) + 2
        except ValueError:
            raise ValueError("Your query returned an empty table")
        s = "".join(str(att.get_name()).ljust(length) + "| " for att in self.attr_l) + "\n" + "+-".join("-" * length for i in range(len(self.attr_l))) + "+\n" + \
            "".join(["".join(str(el).ljust(length) + "| " for el in row) + "\n" for row in query])
        return s


class Rename(SelfOperator):

    def __init__(self, arg1: Attribute, arg2: Constant, table):
        args = [arg1, arg2]
        super(Rename, self).__init__(args, table)

        self.arg2 = arg2

        assert isinstance(arg1, Attribute)
        assert isinstance(arg2, Constant)
        assert isinstance(table, Table) or isinstance(table, Operator)
        if isinstance(table, Operator):
            table = table.run_query()
        # TODO : check if arg1 in the table and arg2 not already in the table

        # Building the query
        self.query = f"SELECT {arg1.a_name} AS {arg2.name} FROM {table.name};"

        self.commit_query = f"ALTER TABLE {self.table.name} RENAME COLUMN {arg1.a_name} TO {arg2.name};"

    def format(self, query):
        try:
            length = max(max(len(str(element)) for element in self.result.attr), max(len(str(attr[0])) for attr in self.attr)) + 2
        except ValueError:
            raise ValueError("Your query returned an empty table")
        s = "".join(str(self.arg2.name).ljust(length) + "| ") + "\n" + "+-".join("-" * (length // 2)) + "+\n" + \
            "".join(["".join(str(el).ljust(length) + "| " for el in row) + "\n" for row in query])
        return s


class Join(MultiOperator):

    def __init__(self, rel1, rel2):
        super(Join, self).__init__(rel1, rel2)

        assert isinstance(rel1, Table) or isinstance(rel1, Operator)
        if isinstance(rel1, Operator):
            rel1 = rel1.run_query()
        assert isinstance(rel2, Table) or isinstance(rel2, Operator)
        if isinstance(rel2, Operator):
            rel2 = rel2.run_query()

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

        assert isinstance(rel1, Table) or isinstance(rel1, Operator)
        if isinstance(rel1, Operator):
            rel1 = rel1.run_query()
        assert isinstance(rel2, Table) or isinstance(rel2, Operator)
        if isinstance(rel2, Operator):
            rel2 = rel2.run_query()

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
