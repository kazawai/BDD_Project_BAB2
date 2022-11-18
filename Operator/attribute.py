class Attribute:

    def __init__(self, a_name: str, a_type: str):
        self.a_name = a_name
        self.a_type = a_type

    def get_name(self):
        return self.a_name

    def get_type(self):
        return self.a_type

    def is_type(self, o_type: str):
        return o_type == self.a_type

    # String as parameter type to avoid error (called forward reference :
    # https://peps.python.org/pep-0484/#forward-references)
    def can_compare(self, o_attr: "Attribute"):
        if self.a_type != o_attr.get_type():
            return False
        return True
