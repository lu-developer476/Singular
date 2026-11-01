from .errors import ParseError
class ParserBase:
    def __init__(self,tokens): self.tokens=tokens; self.i=0
    def peek(self,n=0): return self.tokens[min(self.i+n,len(self.tokens)-1)]
    def check(self,*kinds): return self.peek().kind in kinds
    def match(self,*kinds):
        if self.check(*kinds):
            token=self.peek(); self.i+=1; return token
        return None
    def expect(self,kind,msg=None):
        token=self.match(kind)
        if token:return token
        raise ParseError(msg or 'Expected '+kind+', got '+self.peek().kind)
