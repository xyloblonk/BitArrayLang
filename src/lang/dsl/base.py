class Instruction:
    """
    Base class for DSL instruction handlers.
    Each instruction must implement:
      - matches(tree): bool  # can this instruction handle this parse tree node?
      - execute(runtime, tree): None  # execute the instruction in given runtime context
    """
    def matches(self, tree):
        raise NotImplementedError()

    def execute(self, runtime, tree):
        raise NotImplementedError()
