from collections import deque

class RuntimeError(Exception):
    pass

class Runtime:
    def __init__(self):
        self.vars = [{}]
        self.consts = {}
        self.types = {}
        self.functions = {}
        self.output = []
        self.memory = []
        self.call_stack = deque()
        self.imported = set()

    def push_scope(self):
        self.vars.append({})

    def pop_scope(self):
        self.vars.pop()

    def set_var(self, name, value):
        self.vars[-1][name] = value

    def get_var(self, name):
        for scope in reversed(self.vars):
            if name in scope:
                return scope[name]
        if name in self.consts:
            return self.consts[name]
        raise RuntimeError(f"Variable or constant '{name}' not found")

    def set_const(self, name, value):
        self.consts[name] = value

    def set_type(self, name, value):
        self.types[name] = value

    def get_type(self, name):
        return self.types.get(name, None)

    def set_function(self, name, func):
        self.functions[name] = func

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        raise RuntimeError(f"Function '{name}' not defined")

    def print(self, *args):
        line = " ".join(str(a) for a in args)
        self.output.append(line)
        print(line)

    def execute_instruction(self, fields):
        # fields: {'instruction': str, 'fields': list}
        instr = fields.get('instruction')
        args = fields.get('fields', [])
        print(f"[VM] Executing instruction {instr} with fields {args}")
        self.output.append(f"Executed {instr} {args}")

    def eval_expr(self, tree):
        from lark.tree import Tree
        from lark.lexer import Token

        if isinstance(tree, Tree):
            if tree.data == "bin_expr":
                left = self.eval_expr(tree.children[0])
                op = tree.children[1].value
                right = self.eval_expr(tree.children[2])
                return self.apply_bin_op(left, op, right)
            elif tree.data == "unary_expr":
                op = tree.children[0].value
                val = self.eval_expr(tree.children[1])
                return self.apply_unary_op(op, val)
            elif tree.data == "func_call":
                fname = tree.children[0].value
                args = [self.eval_expr(c) for c in tree.children[1:]]
                func = self.get_function(fname)
                return func(self, *args)
            elif tree.data == "atom":
                return self.eval_expr(tree.children[0])
            else:
                # Should not reach here usually
                raise RuntimeError(f"Unknown expr node: {tree.data}")
        elif isinstance(tree, Token):
            if tree.type == "CNAME":
                return self.get_var(tree.value)
            elif tree.type == "INT":
                return int(tree.value)
            elif tree.type == "HEX":
                return int(tree.value, 16)
            elif tree.type == "BIN":
                return int(tree.value.replace("_", ""), 2)
            elif tree.type == "STRING":
                return tree.value.strip('"').strip("'")
            else:
                raise RuntimeError(f"Unknown token type: {tree.type}")
        else:
            return tree

    def apply_bin_op(self, left, op, right):
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return left // right
        elif op == "&":
            return left & right
        elif op == "|":
            return left | right
        elif op == "^":
            return left ^ right
        elif op == "==":
            return int(left == right)
        elif op == "!=":
            return int(left != right)
        elif op == "<":
            return int(left < right)
        elif op == ">":
            return int(left > right)
        elif op == "<=":
            return int(left <= right)
        elif op == ">=":
            return int(left >= right)
        else:
            raise RuntimeError(f"Unknown binary operator: {op}")

    def apply_unary_op(self, op, val):
        if op == "-":
            return -val
        elif op == "!":
            return int(not val)
        else:
            raise RuntimeError(f"Unknown unary operator: {op}")
