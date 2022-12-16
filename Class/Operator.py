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
        self.result = run_query(self.db, self)
        s = self.format(self.result.row)
        print(s if s is not None else "")
        return self.result


class SelfOperator(Operator):
    """
    Class for operators operating on a single relation
    """

    def __init__(self, arg, table):
        super().__init__()

        assert isinstance(table, Table) or isinstance(table, Operator)
        if isinstance(table, Operator):
            self.table = table.run_query()
        else:
            self.table = table
        self.name = f"{self.__class__.__name__}({', '.join([str(a) for a in arg])}, {table.name})"
        self.db = table.db
        self.attr = table.attr
        self.arg = arg

    def __str__(self):
        return self.name


class MultiOperator(Operator):
    """
    Class for operators operating on multiple relations
    """

    def __init__(self, rel1, rel2):
        super().__init__()

        assert isinstance(rel1, Table) or isinstance(rel1, Operator)
        if isinstance(rel1, Operator):
            self.rel1 = rel1.run_query()
        else:
            self.rel1 = rel1

        assert isinstance(rel2, Table) or isinstance(rel2, Operator)
        if isinstance(rel2, Operator):
            self.rel2 = rel2.run_query()
        else:
            self.rel2 = rel2

        self.db = rel1.db

        self.name = f"{self.__class__.__name__}({rel1}, {rel2})"

        self.attr = None
        self.query = None

    def __str__(self):
        return self.name


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

        assert isinstance(attr2, Constant) or isinstance(attr2, Attribute)
        if op not in valid_operators.keys():
            raise SyntaxException(f"{str(self)} : {op} is not a valid operator")

        # Check if the attributes are in the table
        if attr1 not in table.attr:
            raise AttributeException(f"Attribute {attr1} not in table {table.name}'s attributes.\n"
                                     + f"{table.name}'s attributes are {table.attr}")
        if isinstance(attr2, Attribute):
            if attr2 not in table.attr:
                raise AttributeException(f"Attribute {attr2} not in table {table.name}'s attributes.\n"
                                         + f"{table.name}'s attributes are {table.attr}")

        self.query = f"SELECT * FROM [{str(self.table.name)}] WHERE {attr1.a_name} {valid_operators.get(op)} " + (f"\"{attr2.name}\"" if isinstance(attr2, Constant) else f"{attr2.a_name}")

        self.commit_query = f"SELECT * FROM [{str(self.table.past_name) if self.table.past_name is not None else self.table.name}] WHERE {attr1.a_name} {valid_operators.get(op)} " + (f"\"{attr2.name}\"" if isinstance(attr2, Constant) else f"{attr2.a_name}")


class Projection(SelfOperator):

    def __init__(self, attr_list: list, table):
        super(Projection, self).__init__(attr_list, table)

        self.attr_l = attr_list

        if any(not isinstance(attr, Attribute) for attr in attr_list):
            raise TypeError(f"All attributes must be of class {Attribute.__class__}")
        # Check if all the attributes are in the table
        for attr in attr_list:
            if attr not in table.attr:
                raise AttributeException(f"Attribute {attr} is not in the table {table.name}.\n"
                                         + f"{table.name}'s attributes are : {table.attr}")

        self.query = "SELECT DISTINCT " + ", ".join([att.get_name() for att in attr_list]) + f" FROM [{self.table.name}]"

        self.commit_query = "SELECT DISTINCT " + ", ".join([att.get_name() for att in attr_list]) + f" FROM [{str(self.table.past_name) if self.table.past_name is not None else self.table.name}]"


class Rename(SelfOperator):

    def __init__(self, arg1: Attribute, arg2: Constant, table):
        args = [arg1, arg2]
        super(Rename, self).__init__(args, table)

        # Check if the first attribute is in the table
        if arg1.a_name not in table.attr:
            raise AttributeException(f"Attribute {arg1.a_name} not in the table's {table.name} attribute.\n" +
                                     f"{table.name}'s attributes are {table.attr}")
        # Check if the new name isn't already in the table
        if arg2.name in table.attr:
            raise AttributeException(f"Attribute {arg2.name} already in table's {table.name} attributes.\n" +
                                     f"{table.name}'s attributes are {table.attr}")

        # Building the query
        base_args = ", ".join(list(map(lambda x: x.replace(arg1.a_name, f"{arg1.a_name} AS {arg2.name}"), [att for att in self.table.get_attr()])))
        self.query = f"SELECT {base_args} FROM [{self.table.name}];"

        self.commit_query = f"ALTER TABLE [{str(self.table.past_name) if self.table.past_name is not None else self.table.name}] RENAME COLUMN {arg1.a_name} TO {arg2.name};"


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

