import pytest
from src.parser import parser

def test_basic_parse():
    program = '''
    func main def {instruction: "0x00", field: "reg_dst", field: [0]} =>
      {instruction: "0x01", field: "reg_src", field: [1]}
    '''
    ast = parser.parse(program)
    assert isinstance(ast, list)
    assert ast[0]['func'] == 'main'
    assert len(ast[0]['main']) == 1
