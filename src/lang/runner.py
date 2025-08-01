from lark import Tree
from lang.runtime import Runtime, RuntimeError

class Runner:
    def __init__(self):
        self.runtime = Runtime()

    def execute(self, tree: Tree):
        for stmt in tree.children:
            self.execute_stmt(stmt)

    def execute_stmt(self, stmt):
        method = getattr(self, f"exec_{stmt.data}", None)
        if method:
            return method(stmt)
        else:
            print(f"[Runner] No handler for {stmt.data}")

    def exec_import_stmt(self, stmt):
        path = stmt.children[0].value.strip('"')
        print(f"[Import] Importing {path}")
        self.runtime.imported.add(path)

    def exec_type_decl(self, stmt):
        name = stmt.children[0].value
        type_def = stmt.children[1]
        if type_def.data == "bits":
            bitsize = int(type_def.children[0].value)
            self.runtime.set_type(name, {"bits": bitsize})
        elif type_def.data == "enum":
            enum_members = {}
            for member in type_def.children[0].children:
                enum_name = member.children[0].value
                enum_val = int(member.children[1].value)
                enum_members[enum_name] = enum_val
            self.runtime.set_type(name, {"enum": enum_members})
        else:
            print(f"[Type] Unknown type definition: {type_def.data}")

    def exec_const_decl(self, stmt):
        name = stmt.children[0].value
        val = self.runtime.eval_expr(stmt.children[1])
        self.runtime.set_const(name, val)

    def exec_var_assign(self, stmt):
        name = stmt.children[0].value
        val = self.runtime.eval_expr(stmt.children[1])
        self.runtime.set_var(name, val)

    def exec_func_def(self, stmt):
        name = stmt.children[0].value
        self.runtime.set_function(name, stmt)

    def exec_loop_stmt(self, stmt):
        # loop (var i = 0; i < MAX; i = i + 1) { ... }
        init = stmt.children[0]
        condition = stmt.children[1]
        update = stmt.children[2]
        body = stmt.children[3:]

        self.execute_stmt(init)
        while self.runtime.eval_expr(condition):
            self.runtime.push_scope()
            for s in body:
                self.execute_stmt(s)
            self.runtime.pop_scope()
            self.execute_stmt(update)

    def exec_if_stmt(self, stmt):
        condition = stmt.children[0]
        then_body = stmt.children[1].children
        else_body = []
        if len(stmt.children) > 2:
            else_body = stmt.children[2].children

        if self.runtime.eval_expr(condition):
            self.runtime.push_scope()
            for s in then_body:
                self.execute_stmt(s)
            self.runtime.pop_scope()
        else:
            self.runtime.push_scope()
            for s in else_body:
                self.execute_stmt(s)
            self.runtime.pop_scope()

    def exec_expr_stmt(self, stmt):
        self.runtime.eval_expr(stmt)

    def exec_instruction_stmt(self, stmt):
        fields = {}
        for field_node in stmt.children:
            key = field_node.children[0].value  # "instruction" or "field"
            val = self.runtime.eval_expr(field_node.children[1])
            if key == "instruction:":
                fields['instruction'] = val
            else:
                fields.setdefault('fields', []).append(val)
        self.runtime.execute_instruction(fields)

    def call_function(self, name, args):
        func_tree = self.runtime.get_function(name)
        self.runtime.push_scope()
        # TODO: bind parameters
        for stmt in func_tree.children[1:]:
            self.execute_stmt(stmt)
        self.runtime.pop_scope()
