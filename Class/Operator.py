import sqlite3

from Class.SQL import *
from sql_query import *
from Class.Errors import *


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
        self.table = None
        self.printable_query = ""

    def format(self, query):
        """
        A simple nicely formatted table
        :param query: the query needing to be formatted
        :return: the nicely formatted string
        """
        if len(self.result.attr) == 0 or len(self.result.row) == 0:
            print("\033[91mYour query has returned an empty sequence\033[0m")
            return
        length = max(max(len(str(element)) for element in self.result.attr), max(len(str(a)) for attr in self.result.row for a in attr)) + 5

        s = "".join(str(att).ljust(length) + "| " for att in self.result.attr) + "\n" + "+-".join("-"*length for i in range(len(self.result.attr))) + "+\n" + \
            "".join(["".join(str(el).ljust(length) + "| " for el in row) + "\n" for row in query])
        return s

    def __str__(self):
        return str(self.__class__.__name__)

    def run_query(self):
        try:
            self.result = run_query(self.db, self)
        except sqlite3.OperationalError as e:
            raise TableNameException(f"{str(self)} : {e}")
        s = self.format(self.result.row)
        print(s if s is not None else "")
        return self.result


class SelfOperator(Operator):
    """
    Class for operators operating on a single relation
    """

    def __init__(self, arg, table):
        super().__init__()

        if not isinstance(table, Table) and not isinstance(table, Operator):
            raise SyntaxException(f"{str(self)} : {str(table)} is not a valid Table or Sub-query")
        if isinstance(table, Operator):
            self.table = table.run_query()
        else:
            self.table = table
        self.name = f"{self.__class__.__name__}({', '.join([str(a) for a in arg])}, {table.name})"
        self.db = table.db
        self.attr = table.attr
        self.arg = arg

    def __str__(self):
        return self.__class__.__name__


class MultiOperator(Operator):
    """
    Class for operators operating on multiple relations
    """

    def __init__(self, rel1, rel2):
        super().__init__()

        if not isinstance(rel1, Table) and not isinstance(rel1, Operator):
            raise SyntaxException(f"{str(self)} : {str(rel1)} is not a valid Table or Sub-query")
        if isinstance(rel1, Operator):
            self.rel1 = rel1.run_query()
        else:
            self.rel1 = rel1

        if not isinstance(rel2, Table) and not isinstance(rel2, Operator):
            raise SyntaxException(f"{str(self)} : {str(rel2)} is not a valid Table or Sub-query")
        if isinstance(rel2, Operator):
            self.rel2 = rel2.run_query()
        else:
            self.rel2 = rel2

        self.db = rel1.db

        self.name = f"{self.__class__.__name__}({rel1}, {rel2})"

        self.attr = None
        self.query = None

    def __str__(self):
        return self.__class__.__name__


# All the SPJRUD's valid operators and their SQL equals
valid_operators = {
    "=": "=",
    ">=": ">=",
    "<=": "<=",
    "<": ">",
    ">": ">",
    "!=": "<>"
}


class Select(SelfOperator):

    def __init__(self, attr1: Attribute, op: str, attr2, table):
        attr = [attr1, op, attr2]
        super(Select, self).__init__(attr, table)

        if not isinstance(attr2, Constant) and not isinstance(attr2, Attribute):
            raise SyntaxException(f"{str(self)} : {str(attr2)} is not a valid Constant or Attribute")
        if op not in valid_operators.keys():
            raise SyntaxException(f"{str(self)} : {op} is not a valid operator")

        # Check if the attributes are in the table
        if attr1.a_name not in self.table.attr:
            raise AttributeException(f"Attribute {attr1} not in table {table.name}'s attributes.\n"
                                     + f"{table.name}'s attributes are {self.table.attr}")
        if isinstance(attr2, Attribute):
            if attr2.a_name not in self.table.attr:
                raise AttributeException(f"Attribute {attr2} not in table {table.name}'s attributes.\n"
                                         + f"{table.name}'s attributes are {self.table.attr}")

        self.query = f"SELECT * FROM [{str(self.table.name)}] WHERE {attr1.a_name} {valid_operators.get(op)} " + (f"\"{attr2.name}\"" if isinstance(attr2, Constant) else f"{attr2.a_name}") + ";"

        self.printable_query = f"SELECT * FROM [{str(table.name)}] WHERE {attr1.a_name} {valid_operators.get(op)} " + (f"\"{attr2.name}\"" if isinstance(attr2, Constant) else f"{attr2.a_name}") + ";"

        self.commit_query = f"SELECT * FROM [{str(self.table.past_name) if self.table.past_name is not None else self.table.name}] WHERE {attr1.a_name} {valid_operators.get(op)} " + (f"\"{attr2.name}\"" if isinstance(attr2, Constant) else f"{attr2.a_name}") + ";"


class Projection(SelfOperator):

    def __init__(self, attr_list: list, table):
        super(Projection, self).__init__(attr_list, table)

        self.attr_l = attr_list

        if any(not isinstance(attr, Attribute) for attr in attr_list):
            raise TypeError(f"All attributes must be of class {Attribute.__class__}")
        # Check if all the attributes are in the table
        for attr in attr_list:
            if str(attr) not in self.table.attr:
                raise AttributeException(f"Attribute {attr} is not in the table {table.name}.\n"
                                         + f"{table.name}'s attributes are : {self.table.attr}")

        self.query = "SELECT DISTINCT " + ", ".join([att.get_name() for att in attr_list]) + f" FROM [{self.table.name}];"

        self.printable_query = "SELECT DISTINCT " + ", ".join([att.get_name() for att in attr_list]) + f" FROM [{table.name}];"

        self.commit_query = "SELECT DISTINCT " + ", ".join([att.get_name() for att in attr_list]) + f" FROM [{str(self.table.past_name) if self.table.past_name is not None else self.table.name}];"


class Rename(SelfOperator):

    def __init__(self, arg1: Attribute, arg2: Constant, table):
        args = [arg1, arg2]
        super(Rename, self).__init__(args, table)

        # Check if the first attribute is in the table
        if arg1.a_name not in self.table.attr:
            raise AttributeException(f"Attribute {arg1.a_name} not in the table's {table.name} attribute.\n" +
                                     f"{table.name}'s attributes are {self.table.attr}")
        # Check if the new name isn't already in the table
        if arg2.name in self.table.attr:
            raise AttributeException(f"Attribute {arg2.name} already in table's {table.name} attributes.\n" +
                                     f"{table.name}'s attributes are {self.table.attr}")

        # Building the query
        base_args = ", ".join(list(map(lambda x: x.replace(arg1.a_name, f"{arg1.a_name} AS '{arg2.name}'"), [att for att in self.table.get_attr()])))
        self.query = f"SELECT {base_args} FROM [{self.table.name}];"

        self.printable_query = self.query = f"SELECT {base_args} FROM [{table.name}];"

        self.commit_query = f"ALTER TABLE [{str(self.table.past_name) if self.table.past_name is not None else self.table.name}] RENAME COLUMN {arg1.a_name} TO '{arg2.name}';"


class Insert(SelfOperator):

    def __init__(self, args: list, table):
        super(Insert, self).__init__(args, table)

        if not len(args) == len(table.attr):
            raise SyntaxException(f"{str(self)} : To insert a new row, you have to provide a value for every column.\n" +
                                  f"Table {table.name}'s attributes : {self.table.attr}")

        values = ', '.join([("'" + arg.name + "'") for arg in args])

        self.query = f"INSERT INTO {self.table.name} ({', '.join(self.table.attr)}) VALUES ({values});"
        self.printable_query = f"INSERT INTO {table.name} ({', '.join(self.table.attr)}) VALUES ({values});"

    def run_query(self):
        try:
            self.result = commit_query(self)
        except sqlite3.OperationalError as e:
            raise TableNameException(f"{str(self)} : {e}")
        s = self.format(self.result.row)
        print(s if s is not None else "")
        return self.result


class Join(MultiOperator):

    def __init__(self, rel1, rel2):
        super(Join, self).__init__(rel1, rel2)

        self.query = f"SELECT DISTINCT * FROM [{str(rel1)}] NATURAL JOIN [{str(rel2)}];"


class Union(MultiOperator):

    def __init__(self, rel1, rel2):
        super(Union, self).__init__(rel1, rel2)

        if not rel1.attr == rel2.attr:
            raise AttributeException(f"{str(self)} : {str(rel1)} should have the same attributes as {str(rel2)}.\n" +
                                     f"{str(rel1)}'s attributes : {rel1.attr}\n{str(rel2)}'s attributes : {rel2.attr}")

        self.query = f"SELECT DISTINCT * FROM [{rel1}] UNION SELECT DISTINCT * FROM [{rel2}];"


class Difference(MultiOperator):

    def __init__(self, rel1, rel2):
        super(Difference, self).__init__(rel1, rel2)

        if not rel1.attr == rel2.attr:
            raise AttributeException(f"{str(self)} : {str(rel1)} should have the same attributes as {str(rel2)}.\n" +
                                     f"{str(rel1)}'s attributes : {rel1.attr}\n{str(rel2)}'s attributes : {rel2.attr}")

        self.query = f"SELECT DISTINCT * FROM [{rel1}] MINUS SELECT DISTINCT * FROM [{rel2}];"
