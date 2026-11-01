from src.common import ast
from src.common.errors import ParseError
from src.common.parser_base import ParserBase
from src.common.pratt import ExpressionParserMixin
class SingularParser(ExpressionParserMixin,ParserBase):
 def parse(self):
  out=[]
  while not self.check('EOF'):out.append(self.stmt())
  return ast.Program(out)
 def block(self):
  self.expect('{');a=[]
  while not self.check('}'):a.append(self.stmt())
  self.expect('}');return a
 def semi(self):self.expect(';')
 def stmt(self):
  if self.match('import'):
   p=self.expect('STRING').value;self.expect('as');n=self.expect('IDENT').value;self.semi();return ast.ImportStmt(p,n)
  if self.match('value'):
   n=self.expect('IDENT').value;self.expect('=');e=self.expression();self.semi();return ast.VarDecl(n,e)
  if self.match('fn'):
   n=self.expect('IDENT').value;self.expect('(');p=[]
   if not self.check(')'):
    p.append(self.expect('IDENT').value)
    while self.match(','):p.append(self.expect('IDENT').value)
   self.expect(')');self.expect('->');return ast.FunctionDecl(n,p,self.block())
  if self.match('print'):
   self.expect('(');e=self.expression();self.expect(')');self.semi();return ast.PrintStmt(e)
  if self.match('return'):e=self.expression();self.semi();return ast.ReturnStmt(e)
  if self.match('break'):self.semi();return ast.BreakStmt()
  if self.match('continue'):self.semi();return ast.ContinueStmt()
  if self.match('if'):
   c=self.expression();a=self.block();b=self.block() if self.match('else') else [];return ast.IfStmt(c,a,b)
  if self.match('while'):return ast.WhileStmt(self.expression(),self.block())
  if self.match('for'):
   n=self.expect('IDENT').value;self.expect('in');return ast.ForStmt(n,self.expression(),self.block())
  e=self.expression()
  if self.match('='):
   v=self.expression();self.semi()
   if isinstance(e,ast.Variable):return ast.Assign(e.name,v)
   if isinstance(e,ast.Index):return ast.IndexAssign(e.target,e.index,v)
   t=self.peek(); raise ParseError('Invalid assignment target',t.line,t.column)
  else:self.semi()
  if isinstance(e,ast.Variable) or isinstance(e,ast.Index):
   return ast.ExprStmt(e)
  return ast.ExprStmt(e)
