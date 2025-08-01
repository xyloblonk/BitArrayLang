class Instruction:
    """
    Base class for DSL instruction handlers.
    Each instruction must implement:
      - matches(tree): bool
      - execute(runtime, tree): None
    """
    def matches(self, tree):
        raise NotImplementedError()

    def execute(self, runtime, tree):
        raise NotImplementedError()
