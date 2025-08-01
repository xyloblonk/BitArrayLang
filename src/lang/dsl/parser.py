from lark import Lark
import os

grammar_path = os.path.join(os.path.dirname(__file__), "grammar.lark")

parser = Lark.open(grammar_path, parser="lalr", propagate_positions=True, maybe_placeholders=False)

def parse(source_code):
    return parser.parse(source_code)
