import json
import math
from pathlib import Path
from . import ast
from .errors import RuntimeLangError

def _reject_json_constant(value):
    raise ValueError(f"invalid JSON numeric constant: {value}")


def _unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _parse_json_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"JSON number is outside the supported range: {value}")
    return number


def json_parse_strict(source):
    if not isinstance(source, str):
        raise TypeError("json_parse expects text")
    return json.loads(
        source,
        parse_constant=_reject_json_constant,
        parse_float=_parse_json_float,
        object_pairs_hook=_unique_json_object,
    )


def _validate_json_value(value):
    if value is None or isinstance(value, (str, bool, int, float)):
        return
    if isinstance(value, list):
        for item in value:
            _validate_json_value(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("JSON object keys must be text")
            _validate_json_value(item)
        return
    raise TypeError(f"value of type {type(value).__name__} is not JSON-compatible")


def json_stringify_strict(value):
    _validate_json_value(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
class R(Exception):
 def __init__(self,v):self.v=v
class B(Exception):pass
class C(Exception):pass
class Env:
 def __init__(self,p=None):self.p=p;self.d={}
 def define(self,k,v):self.d[k]=v
 def get(self,k):
  if k in self.d:return self.d[k]
  if self.p:return self.p.get(k)
  raise RuntimeLangError('undefined '+k)
 def assign(self,k,v):
  if k in self.d:self.d[k]=v
  elif self.p:self.p.assign(k,v)
  else:raise RuntimeLangError('undefined '+k)
class Fn:
 def __init__(self,s,e,i):self.s=s;self.e=e;self.i=i
 def __call__(self,a):
  if len(a)!=len(self.s.params):raise RuntimeLangError('wrong argument count')
  e=Env(self.e)
  for k,v in zip(self.s.params,a):e.define(k,v)
  try:self.i.block(self.s.body,e)
  except R as x:return x.v
  except (B,C):raise RuntimeLangError('loop control outside loop')
class VM:
 def __init__(self,printer=print,loader=None,extension='.sg'):
  self.printer=printer;self.loader=loader;self.extension=extension;self.env=Env();self.root=None;self.path=None;self.cache={};self.loading=set()
  f={'range':lambda *a:list(range(*map(int,a))),'len':len,'push':lambda a,x:(a.append(x) or a),'pop':lambda a:a.pop() if a else None,'first':lambda a:a[0] if a else None,'last':lambda a:a[-1] if a else None,'keys':lambda x:list(x.keys()),'values':lambda x:list(x.values()),'has':lambda x,k:k in x,'join':lambda a,s:s.join(map(str,a)),'split':lambda s,d:s.split(d),'str':str,'json_parse':json_parse_strict,'json_stringify':json_stringify_strict,'type':lambda x:'nil' if x is None else 'bool' if isinstance(x,bool) else 'number' if isinstance(x,(int,float)) else 'text' if isinstance(x,str) else 'array' if isinstance(x,list) else 'map'}
  for k,v in f.items():self.env.define(k,lambda a,v=v:v(*a))
 def show(self,x):
  if x is None:return 'nil'
  if isinstance(x,bool):return str(x).lower()
  if isinstance(x,list):return '['+', '.join(map(self.show,x))+']'
  if isinstance(x,dict):return '{'+', '.join(str(k)+': '+self.show(v) for k,v in x.items())+'}'
  return str(x)
 def run(self,p,source_path=None):
  if source_path:self.path=Path(source_path).resolve();self.root=self.path.parent
  try:
   for s in p.statements:self.stmt(s)
  except R:raise RuntimeLangError('return outside function')
  except (B,C):raise RuntimeLangError('loop control outside loop')
 def block(self,ss,e):
  old=self.env;self.env=e
  try:
   for s in ss:self.stmt(s)
  finally:self.env=old
 def stmt(self,s):
  if isinstance(s,ast.ImportStmt):
   if not self.path or not self.loader:raise RuntimeLangError('imports require a file-backed program')
   p=Path(s.path);q=(self.path.parent/p).resolve()
   if p.is_absolute() or p.suffix!=self.extension or not q.is_relative_to(self.root):raise RuntimeLangError('invalid module path')
   if q in self.loading:raise RuntimeLangError('cyclic module import')
   if q not in self.cache:
    self.loading.add(q);old=self.path;e=Env(self.env);oldenv=self.env
    try:self.path=q;self.block(self.loader(q.read_text()).statements,e);self.cache[q]={k:v for k,v in e.d.items() if not k.startswith('_')}
    finally:self.path=old;self.env=oldenv;self.loading.remove(q)
   self.env.define(s.alias,self.cache[q])
  elif isinstance(s,ast.VarDecl):self.env.define(s.name,self.expr(s.expr))
  elif isinstance(s,ast.Assign):self.env.assign(s.name,self.expr(s.expr))
  elif isinstance(s,ast.IndexAssign):self.expr(s.target)[self.expr(s.index)]=self.expr(s.expr)
  elif isinstance(s,ast.FunctionDecl):self.env.define(s.name,Fn(s,self.env,self))
  elif isinstance(s,ast.PrintStmt):self.printer(self.show(self.expr(s.expr)))
  elif isinstance(s,ast.ExprStmt):self.expr(s.expr)
  elif isinstance(s,ast.ReturnStmt):raise R(self.expr(s.expr))
  elif isinstance(s,ast.BreakStmt):raise B()
  elif isinstance(s,ast.ContinueStmt):raise C()
  elif isinstance(s,ast.IfStmt):self.block(s.then_body if self.expr(s.condition) else s.else_body,Env(self.env))
  elif isinstance(s,ast.WhileStmt):
   while self.expr(s.condition):
    try:self.block(s.body,Env(self.env))
    except C:continue
    except B:break
  elif isinstance(s,ast.ForStmt):
   for v in self.expr(s.iterable):
    e=Env(self.env);e.define(s.name,v)
    try:self.block(s.body,e)
    except C:continue
    except B:break
 def expr(self,e):
  if isinstance(e,ast.Literal):return e.value
  if isinstance(e,ast.Variable):return self.env.get(e.name)
  if isinstance(e,ast.Array):return [self.expr(x) for x in e.items]
  if isinstance(e,ast.Map):return {self.expr(k):self.expr(v) for k,v in e.pairs}
  if isinstance(e,ast.Index):return self.expr(e.target)[self.expr(e.index)]
  if isinstance(e,ast.Unary):return not self.expr(e.expr) if e.op=='not' else -self.expr(e.expr)
  if isinstance(e,ast.Binary):
   a=self.expr(e.left);b=self.expr(e.right);return {'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b,'/':lambda:a/b,'%':lambda:a%b,'==':lambda:a==b,'!=':lambda:a!=b,'<':lambda:a<b,'<=':lambda:a<=b,'>':lambda:a>b,'>=':lambda:a>=b,'and':lambda:bool(a) and bool(b),'or':lambda:bool(a) or bool(b)}[e.op]()
  if isinstance(e,ast.Call):
   f=self.expr(e.callee);a=[self.expr(x) for x in e.args]
   if not callable(f):raise RuntimeLangError('not callable')
   return f(a)
  raise RuntimeLangError('unknown expression')
Interpreter=VM


# Keep implementation details private while exposing stable language-level errors.
from .errors import LanguageError
_BaseInterpreter = Interpreter

class Interpreter(_BaseInterpreter):
 def run(self, program, source_path=None):
  try:
   return super().run(program, source_path=source_path)
  except LanguageError:
   raise
  except Exception as error:
   raise RuntimeLangError('runtime operation failed: ' + str(error)) from error
 def expr(self, expression):
  if isinstance(expression, ast.Binary) and expression.op == 'and':
   return bool(self.expr(expression.left)) and bool(self.expr(expression.right))
  if isinstance(expression, ast.Binary) and expression.op == 'or':
   return bool(self.expr(expression.left)) or bool(self.expr(expression.right))
  result = super().expr(expression)
  if isinstance(expression, (ast.Binary, ast.Unary)) and isinstance(result, float):
   if not math.isfinite(result):
    raise RuntimeLangError('arithmetic operation produced a non-finite number')
  return result

 def __init__(self, printer=print, loader=None, extension='.sg'):
  super().__init__(printer, loader, extension)
  self.global_env = self.env
 def import_module(self, statement):
  if not self.path or not self.loader or not self.root:
   raise RuntimeLangError('imports require a file-backed program')
  requested = Path(statement.path)
  if requested.is_absolute() or requested.suffix != self.extension:
   raise RuntimeLangError('invalid module path or extension')
  try:
   target = (self.path.parent / requested).resolve(strict=True)
  except OSError as error:
   raise RuntimeLangError('cannot resolve module: ' + str(error)) from error
  if not target.is_relative_to(self.root):
   raise RuntimeLangError('module path escapes the project directory')
  if target in self.loading:
   raise RuntimeLangError('cyclic module import detected')
  if target not in self.cache:
   self.loading.add(target)
   previous_path, previous_env = self.path, self.env
   module_env = Env(self.global_env)
   try:
    self.path = target
    self.env = module_env
    source = target.read_text(encoding='utf-8')
    self.block(self.loader(source).statements, module_env)
    self.cache[target] = {name: value for name, value in module_env.d.items() if not name.startswith('_')}
   finally:
    self.path, self.env = previous_path, previous_env
    self.loading.remove(target)
  self.env.define(statement.alias, self.cache[target])

 def stmt(self, statement):
  if isinstance(statement, ast.ImportStmt):
   return self.import_module(statement)
  return super().stmt(statement)
