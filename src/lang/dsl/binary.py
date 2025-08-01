from .base import Instruction

class BinaryInstruction(Instruction):
    def matches(self, tree):
        return tree.data == "binary_stmt"

    def execute(self, runtime, tree):
        binary_token = tree.children[0]
        raw_val = binary_token.value.replace("_", "")
        runtime.memory.append(raw_val)
