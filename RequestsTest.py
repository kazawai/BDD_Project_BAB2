import unittest

import main
from main import *
from Class.Operator import *
from Class.SQL import *
from Class.Errors import *


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        create_db("unit_test", test=True)
        self.db = Database("unit_test")
        main.db = "unit_test"

    def test_wrongParentheses(self):
        input1 = "Select((Name, =, Name, Rel(Country))"
        with self.assertRaises(SyntaxException):
            check_parentheses(input1)

    def test_select(self):
        input1 = "Select(Name, =, Name, Rel(Country))"
        rq = process_request(input1)
        self.assertTrue(isinstance(rq, Select))

    def test_wrongOperator(self):
        input1 = "Select(Name,eq,Name,Rel(Country))"
        with self.assertRaises(SyntaxException):
            process_request(input1)

    def test_wrongAttribute(self):
        input1 = "Select(Test,=,Name,Rel(Country))"
        with self.assertRaises(AttributeException):
            process_request(input1)

    def test_wrongTable(self):
        input1 = "Select(Name,=,Name,Rel(Test))"
        with self.assertRaises(TableNameException):
            process_request(input1)

    def test_wrongRequest(self):
        input1 = "Sel(Name,=,Name,Rel(Test))"
        with self.assertRaises(SyntaxException):
            process_request(input1)

    def test_proj(self):
        input1 = "Proj(Name,Rel(Country))"
        rq = process_request(input1)
        self.assertTrue(isinstance(rq, Projection))

        input2 = "Proj(Name, Capital, Currency, Rel(Country))"
        rq2 = process_request(input2)
        self.assertTrue(isinstance(rq2, Projection))

    def test_rename(self):
        input1 = "Rename(Name,Cst(Test),Rel(Country))"
        rq = process_request(input1)
        self.assertTrue(isinstance(rq, Rename))

    def test_renameToAttr(self):
        input1 = "Rename(Name,Test,Rel(Country))"
        with self.assertRaises(SyntaxException):
            process_request(input1)

    def test_renameCstToCst(self):
        input1 = "Rename(Cst(Name),Cst(Test),Rel(Country))"
        with self.assertRaises(SyntaxException):
            process_request(input1)

    def test_renameToAlreadyExisting(self):
        input1 = "Rename(Name,Cst(Capital),Rel(Country))"
        with self.assertRaises(AttributeException):
            process_request(input1)

    def test_renameNotExisting(self):
        input1 = "Rename(Test,Cst(Capital),Rel(Country))"
        with self.assertRaises(AttributeException):
            process_request(input1)

    def test_join(self):
        input1 = "Join(Rel(Country), Rel(Country2))"
        rq = process_request(input1)
        self.assertTrue(isinstance(rq, Join))

    def test_union(self):
        input1 = "Union(Rel(Country), Rel(Country2))"
        rq = process_request(input1)
        self.assertTrue(isinstance(rq, Union))

    def test_difference(self):
        input1 = "Diff(Rel(Country), Rel(Country2))"
        rq = process_request(input1)
        self.assertTrue(isinstance(rq, Difference))

    def test_diffAttr(self):
        input1 = "Diff(Rel(Country), Rel(Cities))"
        with self.assertRaises(AttributeException):
            process_request(input1)

        input2 = "Union(Rel(Country), Rel(Cities))"
        with self.assertRaises(AttributeException):
            process_request(input2)

    def test_subQueries(self):
        input1 = "Select(Test,=,Test,Rename(Name,Cst(Test),Rel(Country)))"
        rq = process_request(input1)
        self.assertTrue(isinstance(rq, Select))
        self.assertTrue(rq.table.attr == ["Test", "Capital", "Inhabitants", "Continent", "Currency"])

    def test_tooManyArgs(self):
        input1 = "Rename(Name,Capital,Cst(Test1),Cst(Test2),Rel(Country))"
        with self.assertRaises(SyntaxException):
            process_request(input1)

    def test_notEnoughArgs(self):
        input1 = "Select(Name,Rel(Country))"
        with self.assertRaises(MissingExpressionException):
            process_request(input1)


if __name__ == '__main__':
    unittest.main()
