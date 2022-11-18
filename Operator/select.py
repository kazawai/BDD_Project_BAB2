from operator import Operator


class Select(Operator):

    name = "Select"

    def __init__(self, op, rel):
        super().__init__([op, rel])
        self.op = op
        self.relation = rel

    def __str__(self):
        return f"Select({self.op}, {self.relation})"

    def __get_name__(self):
        return self.name
