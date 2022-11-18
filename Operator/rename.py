from operator import Operator


class Rename(Operator):

    name = "Rename"

    def __init__(self, p_name, n_name, rel):
        super().__init__([p_name, n_name, rel])
        self.p_name = p_name
        self.n_name = n_name
        self.relation = rel

    def __str__(self):
        return f"Rename({self.p_name} -> {self.n_name}, de {self.relation}"

    def __get_name__(self):
        return self.name
