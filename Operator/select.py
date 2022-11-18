from operator import Operator


class Select(Operator):

    name = "Select"

    def __int__(self, op, rel):
        super([op, rel])
        self.op = op
        self.relation = rel

    def __str__(self):
        return f"Select({self.op}, {self.relation})"

    def get_name(self):
        return self.name
