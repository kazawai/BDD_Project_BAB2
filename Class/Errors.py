class SError(Exception):
    def __init__(self, name: str, description: str = None):
        self.err = f"{name}" + (f" : {description}" if description is not None else "")
        super().__init__(self.err)

    def __str__(self):
        return self.err


class SyntaxException(SError):
    def __init__(self, description: str = None):
        super().__init__(self.__class__.__name__, description)


class MissingExpressionException(SError):
    def __init__(self, description: str = None):
        super().__init__(self.__class__.__name__, description)


class TableNameException(SError):
    def __init__(self, description: str = None):
        super().__init__(self.__class__.__name__, description)


class AttributeException(SError):
    def __init__(self, description: str = None):
        super().__init__(self.__class__.__name__, description)
