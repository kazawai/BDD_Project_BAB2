from operator import Operator


class Projection(Operator):

    name = "Proj"

    def __init__(self, col, rel):
        super().__init__([col, rel])
        self.column = col
        self.relation = rel

    def __str__(self):
        return f"Proj({self.column}, {self.relation})"

    def __get_name__(self):
        return self.name
