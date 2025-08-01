from .base import Instruction

class PrintInstruction(Instruction):
    def matches(self, tree):
        return tree.data == "print_stmt"

    def execute(self, runtime, tree):
        arg = tree.children[0]

        if arg.data == "CNAME":
            val = runtime.get_var(arg.children[0].value)
        else:
            val = arg.children[0].value

        print(val)
        runtime.output.append(str(val))
