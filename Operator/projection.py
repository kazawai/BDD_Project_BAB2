from operator import Operator


class Projection(Operator):

    name = "Proj"

    def __int__(self, col, rel):
        super([col, rel])
        self.column = col
        self.relation = rel

    def __str__(self):
        return f"Proj({self.column}, {self.relation})"

    def get_name(self):
        return self.name
