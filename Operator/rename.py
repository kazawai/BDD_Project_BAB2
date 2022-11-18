from operator import Operator


class Rename(Operator):

    name = "Rename"

    def __int__(self, p_name, n_name, rel):
        super([p_name, n_name, rel])
        self.p_name = p_name
        self.n_name = n_name
        self.relation = rel

    def __str__(self):
        return f"Rename({self.p_name} -> {self.n_name}, de {self.relation}"

    def get_name(self):
        return self.name
