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
        if self.name != 'x':
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
    
class Let(Expr):
    def __init__(self, var_name: str, var_expr: Expr, body: Expr):
        self.var_name = var_name
        self.var_expr = var_expr
        self.body = body
        self.args = (var_name, var_expr, body)

    def eval(self, env: Dict[str, float]) -> float:
        new_env = env.copy()
        new_env[self.var_name] = self.var_expr.eval(env)
        return self.body.eval(new_env)

    def __repr__(self):
        return f"{self.body}"


    


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

    if isinstance(exprs, Let):
        if exprs in hash_table:
            return hash_table[exprs], hash_table, count + 1
        else:
            hashed_var_expr, hash_table, count = get_exprs_hash(exprs.var_expr, hash_table, count)
            new_env = hash_table.copy()
            new_env.update({exprs.var_name: hashed_var_expr})
            hashed_body_expr, hash_table, count = get_exprs_hash(exprs.body, new_env, count)
            hashed = Let(exprs.var_name, hashed_var_expr, hashed_body_expr)
            hash_table[hashed] = hashed
            # remove the last item
            hash_table.popitem()

            # remove the first item
            keys = list(hash_table.keys())
            del hash_table[keys[0]]
            return hashed, hash_table, count + 1

    raise ValueError(f"Unsupported expression type: {type(exprs)}")








# Test the hash consing
print("\n********************* RESULTS *********************\n")
x = float(input("Enter the value of x: "))


env = {}
let_expr = Let('x', Const(x), Add(Add(Var('x'), Const(2)),Add(Var('x'), Const(2))))
# let_expr = Let('x', Const(x), Sub( Sub( Add( Sub( Add( Const(5), Const(2) ), Add( Const(3), Const(2) ) ), Sub( Add( Var('x'), Const(2) ), Add( Const(1), Const(2) ) ) ), Add( Const(1), Const(2) ) ), Sub( Add( Var('x'), Const(2) ), Add( Const(1), Const(2) ) ) ) )


# Evaluation without HashConsing
print("********************* EVALUATON *********************")
result = let_expr.eval(env)
print(f"Evaluation without HashConsing: {result}")



# Evaluation with HashConsing
hashed_exprs, hash_table, count = get_exprs_hash(let_expr, {})
result = hashed_exprs.eval(env)
print(f"Evaluation with HashConsing: {result}")


print("\n********************* #CALCULATIONS *********************")
# Compare the number of calculations with and without HashConsing
hashed_exprs, hash_table, count = get_exprs_hash(let_expr, {})
count -= 1
print(f"Number of calculations without HashConsing: {count}")

num_calculations_with_hashconsing = len(hash_table) if hash_table else 0
print(f"Number of calculations with HashConsing: {num_calculations_with_hashconsing}")


# Printing the final expression
print("\n********************* FINAL EXPRS *********************")
print(f"Final expression: {hashed_exprs}")


print("\n********************* TIME *********************")
# Time performance without hash consing
time_no_hashconsing = timeit.timeit(
    stmt="let_expr.eval(env)",
    globals=globals(),
    number=10000,
)
print(f"Time without HashConsing: {time_no_hashconsing}")


# Time performance with hash consing
hashconsing_time = timeit.timeit(
    stmt="get_exprs_hash(let_expr, {}, 0)",
    globals=globals(),
    number=10000,
)
_, _, hashconsing_calcs = get_exprs_hash(let_expr, {}, 0)
print(f"Time with HashConsing: {hashconsing_time}")

# Printing the Hash Table
print("\n********************* HASH TABLE *********************\n")
print(hash_table)
