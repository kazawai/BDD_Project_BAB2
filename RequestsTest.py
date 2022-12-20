import unittest

from main import *
from Class.Operator import *
from Class.SQL import *
from Class.Errors import *


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        create_db("unit_test", test=True)
        self.db = Database("unit_test")

    def parenthesesTest(self):
        input1 = "Select((Name, =, Name, Rel(Country))"
        self.assertRaises(SyntaxException, check_parentheses(input1))

    def selectTest(self):
        input1 = "Select(Name, =, Name, Rel(Country))"



if __name__ == '__main__':
    unittest.main()
