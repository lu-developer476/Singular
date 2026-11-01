from src.common.lexer import Lexer, SINGULAR_KEYWORDS
from src.common.runtime import Interpreter
from .parser_core import SingularParser

def parse(source): return SingularParser(Lexer(source, keywords=SINGULAR_KEYWORDS).tokens()).parse()
def run(source, printer=print, source_path=None):
    vm=Interpreter(printer, loader=parse, extension='.sg')
    vm.run(parse(source), source_path=source_path)
