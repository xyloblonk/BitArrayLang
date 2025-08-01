import sys
from lang.dsl.parser import parse
from lang.runner import Runner

def main():
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <file.bal>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path) as f:
        source = f.read()

    tree = parse(source)
    runner = Runner()
    runner.execute(tree)

if __name__ == "__main__":
    main()
