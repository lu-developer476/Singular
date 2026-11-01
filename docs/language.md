# Singular language reference

Singular (`.sg`) is a minimal language for deterministic calculations and data transformations.

- `value name = expression;` declares a variable.
- `fn name(args) -> { ... }` declares a function.
- `print(expression);` prints a value.
- `if`, `while`, and `for` provide control flow.
- Statements end with semicolons; blocks use braces.
- Imports use `import "module.sg" as alias;`.
- Builtins include `range`, `len`, `push`, `pop`, `first`, `last`, `keys`, `values`, `has`, `join`, `split`, `str`, and `type`.
