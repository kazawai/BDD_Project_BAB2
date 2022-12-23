# BAB2 Data Base Project || SPJRUD to SQL Compilation

## Introduction

Welcome to Maxime's project to the SPJRUD to SQL Compilation in python.

You can start the project by typing in the terminal
```bash
$ python3 main.py
```
Then enjoy the magic ! :D

## How to use

Once the program started, you will first be presented with something like this
```bash
Enter the name of the database you wish to use : ----------- (Enter 'exit' to quit)

$ Database : 
```
This will let you choose the database you want to use.
The database used will be the one named ``{input}.db`` with ``{input}`` being your input above.

If ``{input}.db`` already exists, you will be presented with this
```bash
The database {input}.db already exists, would you like to reset it to the predefined values ? [y/n] : 
```
Enter 'n' if you want to keep the values as they were initially. However, a test will be run on the database
to assert that at least the tables `CC`and `Cities` are present.

If the database does not exist or that you press 'y', the database will have 4 tables looking like this :

Country :

| Name | Capital    | Inhabitants | Continent     | Currency |
|------|------------|-------------|---------------|----------|
| USA  | Washington | 30000000    | North America | USD      |

Country 2 :

| Name    | Capital    | Inhabitants | Continent     | Currency |
|---------|------------|-------------|---------------|----------|
| USA     | Washington | 30000000    | North America | USD      |
| Belgium | Bruxelles  | 1           | Europe        | EUR      |

Cities :

| Name    | Country | Inhabitants |
|---------|---------|-------------|
||||

CC :

| Name    | Capital    | Inhabitants | Continent | Currency |
|---------|------------|-------------|-----------|----------|
||||||

Once the database chosen, you will be presented with the opportunity to enter your SPJRUD request :
```bash
Please enter your request below ----------- (Enter 'exit' to quit)

$ Request :
```

### List of available queries

The available requests are :
* ``Select(Attr1,op,Attr2,Rel)`` Where :
  * `Attr1` is an attribute of the Relation `Rel`
  * `op` is a valid operator, them being ``=, >=, >=, >, <, !=``
  * `Attr2` is either another attribute of `Rel` or a `Constant`
  * `Rel` is either a Table of the database, or another request
* ``Proj(Attr1,Attr2,Attr3,...,Rel)`` Where :
  * `Attr1,Attr2,Attr3,...` are all of the attributes wanted
  * `Rel` is either a Table of the database, or another request
* ``Rename(Attr1,Cst(Attr2),Rel)`` Where :
  * `Attr1` is the attribute of the relation `Rel` that wants to be renamed
  * `Cst(Attr2)` is the constant to modify `Attr1` to (has to follow the Constant naming convention)
  * `Rel` is either a Table of the database, or another request
* ``Join(Rel1,Rel2)`` Where :
  * `Rel1` is either a Table of the database or another request
  * `Rel2` is either a Table of the database or another request
* ``Union(Rel1,Rel2)`` Where :
  * `Rel1` is either a Table of the database or another request
  * `Rel2` is either a Table of the database or another request
* ``Rel(Name)`` Represents a table of the database where :
  * `Name` is the name of the table
* ``Cst(Value)`` Represents a constant, it could be a string (most used), an integer, or somthing else

Knowing that, a successful query would look like that :
```bash
Please enter your request below ----------- (Enter 'exit' to quit)

$ Request : Select(Name,=,Cst(USA),Rename(Capital,Cst(This is my capital),Rel(Country2)))
```
This particular query would output this :

| Name | This is my capital | Inhabitants | Continent     | Currency |
|------|--------------------|-------------|---------------|----------|
| USA  | Washington         | 30000000    | North America | USD      |

**Note that to represent a constant and a table of the database, the notation Cst(Value) and Rel(Name) are used.
The query will not work if the conventions listed above aren't respected.**

*Also note that the program is case-sensitive.*

You can add spaces for readability in your request if wanted. A sample request with spaces would look like this :
```bash
Please enter your request below ----------- (Enter 'exit' to quit)

$ Request : Select(Name, =, Cst(USA), Rel(Country))
```

### Useful things to know

At any point in the program, you can use the `CTRL + C` shortcut to terminate safely the program. 
Any requests that aren't committed won't be stored for the next time you launch the program.

You can commit all the queries you did since the start of the program by simply typing the command
```bash
Please enter your request below ----------- (Enter 'exit' to quit)

$ Request : commit
```

An output example with the request from last time would be :
```bash
Please enter your request below ----------- (Enter 'exit' to quit)

Request : commit


executed ALTER TABLE [Country2] RENAME COLUMN Capital TO 'This is my capital';
executed SELECT * FROM [Country2] WHERE Name = "USA"
```

Now if we simply run the command to get the integrity of the table `Country2`,
```bash
Please enter your request below ----------- (Enter 'exit' to quit)

Request : Select(Name,=,Name,Rel(Country2))
```

We get this output :

| Name    | This is my capital | Inhabitants | Continent     | Currency |
|---------|--------------------|-------------|---------------|----------|
| USA     | Washington         | 30000000    | North America | USD      |
| Belgium | Bruxelles          | 1           | Europe        | EUR      |

As you can see, the column `Capital` was successfully renamed to `This is my capital`


You can also `Insert` new rows in tables. For example, if we want to add a row in the table `Cities`, we would write :
```bash
Please enter your request below ----------- (Enter 'exit' to quit)

$ Request : Insert(Cst(Test), Cst(Test1), Cst(Test2), Rel(Cities))
```
The output would be :

```bash
executed INSERT INTO Cities (Name, Country, Inhabitants) VALUES ('Test', 'Test1', 'Test2');
Name            | Country         | Inhabitants     | 
----------------+-----------------+-----------------+
Test            | Test1           | Test2           | 
```

As you can see, the row was correctly inserted.

**Note that the row will be inserted in the specified table and directly committed, no need to enter `commit` after.**

### Exceptions

The program has a lot of useful exceptions for wrong queries.

The list of all available exceptions is :
* **SyntaxException** : Used for when there's an error in the syntax of the query
* **MissingExpressionException** : Used for when there's a missing expression in the query (for example a missing argument)
* **TableNameException** : Used when the table name isn't in the database
* **AttributeException** : Mainly used when a given attribute isn't in a given table
* **WrongDatabaseException** : Used when the given database doesn't respect all the criteria

Some example of errors :

```bash
Please enter your request below ----------- (Enter 'exit' to quit)

Request : Selec(Name,=,Name,Rel(Country2))


SyntaxException : Not a valid argument Selec
```

```bash
Please enter your request below ----------- (Enter 'exit' to quit)

Request : Select(Name,Rel(Country2))


MissingExpressionException : Select : Too little arguments, expected 4 got 2
```

```bash
Please enter your request below ----------- (Enter 'exit' to quit)

Request : Select(Name,=,Name,Rel(Country3))


TableNameException : test.db : no such table: Country3
```

```bash
Please enter your request below ----------- (Enter 'exit' to quit)

Request : Select(Wrong,=,Name,Rel(Country2))


AttributeException : Attribute Wrong not in table Country2's attributes.
Country2's attributes are ['Name', 'Capital', 'Inhabitants', 'Continent', 'Currency']
```

```bash
WrongDatabaseException : test.db should at least contain tables 'CC' and 'Cities' but doesn't.
Database's tables : ['Cities', 'Country', 'Country2']
```
```bash
Please enter your request below ----------- (Enter 'exit' to quit)

Request : select


AttributeException : select cannot be translated as an SQL query, expected one of the following :
[Select, Proj, Rename, Join, Union, Diff]
But got 'Attribute'
```

```bash
Please enter your request below ----------- (Enter 'exit' to quit)

Request : Diff(Rel(Cities),Rel(Country))


AttributeException : Difference(Cities, Country) : Cities should have the same attributes as Country.
Cities's attributes : ['Name', 'Country', 'Inhabitants']
Country's attributes : ['Name', 'Capital', 'Inhabitants', 'Continent', 'Currency']
```

#### What could raise such exceptions

Here is a list of what could raise the above exceptions for each operator :
* `SelfOperator` : if the `table` given isn't either a `Table` or a sub-query you would get an exception of the sort :
```bash
SyntaxException : {SelfOperator} : {table} is not a valid Table or Sub-query 
```
* `MultiOperator` : if the `rel1` or `rel2` given aren't either a `Table` or a sub-query. An exception of the sort would be generated :
```bash
SyntaxException : {MultiOperator} : {rel1} is not a valid Table or Sub-query
```
* `Select`
  * If `attr1` is not an attribute of `table`, you'd get an exception of the sort :
`
AttributeException : Attribute {attr1} not in table {table}'s attributes.
{table}'s attributes are ['Name', 'Country', 'Inhabitants'] 
`
  * If `attr2` is not a `Constant` or an `Attribute` of the table, you'd get :
`
SyntaxException : Select : {attr2} is not a valid Constant or Attribute
`
  * If `op` isn't a valid operator

* `Proj`
  * If there's at least one attribute of `attr_list` that isn't an `Attribute`
  * If there's at least of attribute of `attr_list` that isn't in the table

* `Rename`
  * If `arg1` isn't in the `table`
  * If `arg2` is already in the `table`

* `Insert`
  * If the length of `args` isn't the same as the number of attributes of the `table`

* `Union`
  * If the attributes of `rel1` aren't the same as those of `rel2`

* `Diff`
  * If the attributes of `rel1` aren't the same as those of `rel2`

### Unit tests
There is a series of unit tests available in the `RequestsTest.py` file.

You can run them all by putting the following command in your terminal : 
```bash
python3 RequestsTest.py
```
