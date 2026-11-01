# Singular language reference

Singular (`.sg`) is a minimal language for deterministic calculations and data transformations.

- `value name = expression;` declares a variable.
- `fn name(args) -> { ... }` declares a function.
- `print(expression);` prints a value.
- `if`, `while`, and `for` provide control flow.
- Statements end with semicolons; blocks use braces.
- Imports use `import "module.sg" as alias;`.
- Builtins include `range`, `len`, `push`, `pop`, `first`, `last`, `keys`, `values`, `has`, `join`, `split`, `str`, and `type`.

## Runtime behavior

- `and` and `or` short-circuit and return boolean values.
- Runtime failures (invalid operations, indexing, and builtin calls) are normalized to `RuntimeLangError`.
- Lexical and syntax errors include source line and column information.
- Only Singular declaration words (`value`, `fn`, `print`) are reserved by this frontend; Kitsune's `let`, `spell`, and `echo` remain ordinary Singular identifiers.
- Imports resolve relative to the importing file, are confined to the project root, require `.sg`, and are cached after a successful load.
