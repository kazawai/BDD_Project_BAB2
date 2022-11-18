from operator import Operator
from attribute import Attribute


class Relation(Operator):

    name = "Rel"

    def __init__(self, r_name: str, l_attr: list = None, create: bool = False):
        super().__init__([r_name, l_attr])
        self.r_name = r_name
        if create:
            self.create_table()
        else:
            self.r_check()
        self.l_attr = None
        self.check_attr(l_attr)

    def check_attr(self, l_attr: list):
        """
        Will check the attributes given, if none were given, we will take those from the database

        :param l_attr:
        :return:
        """
        if l_attr is None:
            # TODO : retrieve them from the database
            return
        for a in l_attr:
            if not isinstance(a, Attribute):
                raise TypeError(f"Attribute {a} isn't of type \'Attribute\'")
        self.l_attr = l_attr

    def r_check(self) -> bool:
        """
        Check if the relation is a table from the database

        :return: True or False
        """
        pass

    def create_table(self):
        pass

    def __get_name__(self):
        return self.name

    def __str__(self):
        return f"Rel({self.r_name})"
