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
Enter 'n' if you want to keep the values as they were initially.

If the database does not exist or that you press 'y', the database will have 3 tables looking like this :

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

*Also note that the program is case-sensitive and doesn't work if any spacing are put between anything in the query.*

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
