from operator import Operator


class Join(Operator):

    name = "Join"

    def __init__(self, rel1, rel2):
        super().__init__([rel1, rel2])
        self.f_relation = rel1
        self.s_relation = rel2

    def __str__(self):
        return f"Join({self.f_relation}, {self.s_relation})"

    def __get_name__(self):
        return self.name
