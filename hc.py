from typing import Dict, Tuple
import timeit


class Expr:
    num_calc = 0
    def eval(self, env: Dict[str, float]) -> float:
        Expr.num_calc += 1
        raise NotImplementedError

    def __eq__(self, other):
        return type(self) == type(other) and self.args == other.args

    def __hash__(self):
        return hash((type(self),) + self.args)


class Const(Expr):
    def __init__(self, value: float):
        self.value = value
        self.args = (value,)

    def eval(self, env: Dict[str, float]) -> float:
        Expr.num_calc += 1
        return self.value

    def __repr__(self):
        return f"{self.value}"


class Var(Expr):
    def __init__(self, name: str):
        self.name = name
        self.args = (name,)

    def eval(self, env: Dict[str, float]) -> float:
        Expr.num_calc += 1
        return env[self.name]

    def __repr__(self):
        return self.name


class Add(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right
        self.args = (left, right)

    def eval(self, env: Dict[str, float]) -> float:
        Expr.num_calc += 1
        return self.left.eval(env) + self.right.eval(env)

    def __repr__(self):
        return f"({self.left} + {self.right})"



class Sub(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right
        self.args = (left, right)

    def eval(self, env: Dict[str, float]) -> float:
        Expr.num_calc += 1
        return self.left.eval(env) - self.right.eval(env)

    def __repr__(self):
        return f"({self.left} - {self.right})"


def get_exprs_hash(exprs: Expr, hash_table: Dict[str, Expr], count: int = 0) -> Tuple[Expr, Dict[str, Expr], int]:
    if isinstance(exprs, Const):
        return exprs, hash_table, count

    if isinstance(exprs, Var):
        if exprs.name not in hash_table:
            hash_table[exprs.name] = exprs
        return hash_table[exprs.name], hash_table, count

    if isinstance(exprs, Add) or isinstance(exprs, Sub):
        if exprs in hash_table:
            return hash_table[exprs], hash_table, count + 1
        else:
            hashed_left, hash_table, count = get_exprs_hash(exprs.left, hash_table, count)
            hashed_right, hash_table, count = get_exprs_hash(exprs.right, hash_table, count)
            hashed = exprs.__class__(hashed_left, hashed_right)
            hash_table[hashed] = hashed
            return hashed, hash_table, count + 1

    raise ValueError(f"Unsupported expression type: {type(exprs)}")




# Test the hash consing
print("\n********************* RESULTS *********************\n")
env = {}
exprs = Add(Sub(Add(Const(7), Const(2)), Add(Const(7), Const(2))), Sub(Add(Const(7), Const(2)), Add(Const(5), Const(2))))



# Evaluation without HashConsing
print("********************* EVALUATON *********************")
result = exprs.eval(env)
print(f"Evaluation without HashConsing: {result}")

# Evaluation with HashConsing
hashed_exprs, hash_table, count = get_exprs_hash(exprs, {})
result = hashed_exprs.eval(env)
print(f"Evaluation with HashConsing: {result}")


print("\n********************* #CALCULATIONS *********************")
# Compare the number of calculations with and without HashConsing
hashed_exprs, hash_table, count = get_exprs_hash(exprs, {})
print(f"Number of calculations without HashConsing: {count}")

num_calculations_without_hashconsing = len(hash_table) if hash_table else 0
num_calculations_with_hashconsing = len(hash_table)
print(f"Number of calculations with HashConsing: {num_calculations_without_hashconsing}")


# Printing the final expression
print("\n********************* FINAL EXPRS *********************")
print(f"Final expression: {hashed_exprs}")


print("\n********************* TIME *********************")
# Time performance without hash consing
time_no_hashconsing = timeit.timeit(
    stmt="exprs.eval(env)",
    globals=globals(),
    number=10000,
)
print(f"Time without HashConsing: {time_no_hashconsing}")


# Time performance with hash consing
hashconsing_time = timeit.timeit(
    stmt="get_exprs_hash(exprs, {}, 0)",
    globals=globals(),
    number=10000,
)
_, _, hashconsing_calcs = get_exprs_hash(exprs, {}, 0)
print(f"Time with HashConsing: {hashconsing_time}")

# Printing the Hash Table
print("\n********************* HASH TABLE *********************\n")
print(hash_table)
