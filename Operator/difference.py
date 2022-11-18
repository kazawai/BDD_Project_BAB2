from operator import Operator

class Difference(Operator):

    name ="Difference"

    def __init__(self, Rel_A,Rel_B):
        super.__init__([Rel_A, Rel_B])
        self.Rel_A = Rel_A
        self.Rel_B = Rel_B
    
    def __str__(self):
        return f"Difference({self.Rel_A}, {self.Rel_B})"

    def __get_name__(self):
        return self.names
