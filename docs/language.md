# Singular language reference

Singular (`.sg`) is a minimal language for deterministic calculations and data transformations.

- `value name = expression;` declares a variable.
- `fn name(args) -> { ... }` declares a function.
- `print(expression);` prints a value.
- `if`, `while`, and `for` provide control flow.
- Statements end with semicolons; blocks use braces.
- Imports use `import "module.sg" as alias;`.
- Builtins include `range`, `len`, `push`, `pop`, `first`, `last`, `keys`, `values`, `has`, `join`, `split`, `str`, and `type`.

## Numeric literals

Singular accepts integer, decimal, and scientific-notation literals:

```singular
print(42);
print(0.125);
print(1.25e-2);
print(2e3);
```

Integer literals use Python's arbitrary-precision integer representation. Decimal and scientific-notation literals use IEEE-754 binary64. Non-finite results from literal conversion are rejected, as are nonzero decimal literals that underflow all the way to zero. Representable subnormal values remain valid. Malformed exponents (for example, `3e+`) are rejected as lexical errors with source locations.

## Strict JSON built-ins

- `json_parse(text)` parses JSON text into Singular values.
- `json_stringify(value)` emits compact JSON with lexicographically sorted object keys and preserved Unicode.
- Parsing rejects `NaN`, infinities, duplicate object keys, and numbers outside the finite floating-point range supported by the runtime.
- Serialization requires text object keys and JSON-compatible values; unsupported values and non-finite numbers are rejected.

This makes JSON output reproducible for data pipelines and small verification programs:

```singular
value input = json_parse("{\"count\":3,\"valid\":true}");
print(json_stringify(input));
```

## Runtime behavior

- `and` and `or` short-circuit and return boolean values.
- Runtime failures (invalid operations, indexing, and builtin calls) are normalized to `RuntimeLangError`.
- Arithmetic operations that produce non-finite floating-point results (`NaN` or infinity) are rejected as `RuntimeLangError`; arbitrary-precision integer arithmetic remains available.
- Lexical and syntax errors include source line and column information.
- Only Singular declaration words (`value`, `fn`, `print`) are reserved by this frontend; Kitsune's `let`, `spell`, and `echo` remain ordinary Singular identifiers.
- Imports resolve relative to the importing file, are confined to the project root, require `.sg`, and are cached after a successful load.

## Official formatter

Format a source file in place with `singular format path/to/program.sg`; use `singular format --check path/to/program.sg` to verify formatting without modifying the file. The formatter parses the program before writing, preserves comments and string literals, uses four-space indentation, and is idempotent.
