from dataclasses import dataclass
from .errors import LexError
@dataclass(frozen=True)
class Token:
    kind: str
    value: object
    line: int
    column: int
COMMON_KEYWORDS = {'if', 'else', 'while', 'for', 'in', 'return', 'true', 'false', 'nil', 'and', 'or', 'not', 'break', 'continue', 'import', 'as'}
KITSUNE_KEYWORDS = COMMON_KEYWORDS | {'let', 'spell', 'echo'}
SINGULAR_KEYWORDS = COMMON_KEYWORDS | {'value', 'fn', 'print'}
KEYWORDS = KITSUNE_KEYWORDS | SINGULAR_KEYWORDS
class Lexer:
    def __init__(self, source): self.source=source; self.i=0; self.line=1; self.col=1
    def peek(self,n=0): return self.source[self.i+n] if self.i+n<len(self.source) else '\0'
    def advance(self):
        c=self.peek(); self.i+=1
        if c=='\n': self.line+=1; self.col=1
        else: self.col+=1
        return c
    def tokens(self):
        out=[]
        while self.peek()!='\0':
            c=self.peek()
            if c.isspace(): self.advance(); continue
            line,col=self.line,self.col
            if c.isdigit():
                s=''
                while self.peek().isdigit(): s+=self.advance()
                out.append(Token('NUMBER',int(s),line,col)); continue
            if c.isalpha() or c=='_':
                s=''
                while self.peek().isalnum() or self.peek()=='_': s+=self.advance()
                out.append(Token(s if s in self.keywords else 'IDENT',s,line,col)); continue
            if c=='"':
                self.advance(); s=''
                while self.peek() not in ('"','\0'): s+=self.advance()
                if self.peek()=='\0': raise LexError('Unterminated string')
                self.advance(); out.append(Token('STRING',s,line,col)); continue
            pair=c+self.peek(1)
            if pair in ('==','!=','<=','>=','->'):
                self.advance(); self.advance(); out.append(Token(pair,pair,line,col)); continue
            if c in '+-*/%=<>(){}[],;:.': self.advance(); out.append(Token(c,c,line,col)); continue
            raise LexError('Unexpected character')
        out.append(Token('EOF',None,self.line,self.col)); return out
