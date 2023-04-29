
# HashConsing & Expression Parser in Python


## Goals of the project
The main code is an implementation of an optimization technique called "hash consing". The main purpose of the project is to evaluate arithmetic expressions represented as a tree data structure in a more efficient way by reusing identical sub-expressions.
The program takes an arithmetic expression as input, which is a tree-like structure consisting of constant values, variables, and operations such as addition and subtraction. It then evaluates the expression by traversing the tree and performing the necessary calculations. To improve the performance of the evaluation, we used hash consing to identify identical sub-expressions and reuse their previously calculated results instead of recalculating them. This reduces the number of calculations needed to evaluate the expression, and may lead to faster execution times in large expressions.

## Methodolgy
We define a hierarchy of classes that represent mathematical expressions. There are three types of expressions: constants, variables, and binary operators (Add and Sub). Each expression class has an eval method that evaluates the expression with a given environment (a dictionary of variable values).
The get_exprs_hash function takes an expression and a hash table (a dictionary that maps expressions to their hashed versions) and returns a tuple containing the hashed expression, the updated hash table, and the number of expressions that were hashed. The function works by recursively calling itself on sub-expressions until it reaches a constant or a variable. When it encounters a binary operator expression, it checks if the expression has already been hashed. If it has, it returns the hashed version from the hash table. If not, it hashes its left and right sub-expressions, creates a new hashed expression using the same operator, and stores it in the hash table.


## Outputs
Example #1 <br />
In this example the input expression is :  <b>  (((7 + 2) - (7 + 2)) + ((7 + 2) - (5 + 2))) <\b> <br />
As you can see the number of calculation using hash consing is lower than computation with normal method. <br />

![Output Screenshot](https://github.com/shahrambashokian/HashConsing/blob/main/images/Screenshot1.png?raw=true)


