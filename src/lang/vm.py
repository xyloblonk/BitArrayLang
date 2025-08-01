class Runtime:
    def __init__(self):
        self.vars = {}
        self.memory = []
        self.output = []

    def get_var(self, name):
        return self.vars.get(name, None)

    def set_var(self, name, value):
        self.vars[name] = value
