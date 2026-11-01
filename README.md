# Singular

**Singular** is a minimal, deterministic language for calculations, data transformations, and small verifiable programs.

## Language surface (v2.8.0)

- .sg source files.
- Explicit declarations: value, fn, print.
- Semicolon-terminated statements and brace-delimited blocks.
- Integer, decimal, and scientific-notation numeric literals.
- Integer arithmetic retains arbitrary precision; decimal/scientific values use finite IEEE-754 binary64.
- Decimal overflow and nonzero underflow-to-zero are rejected; representable subnormal values are accepted.
- Functions, lexical scopes, closures, if / else, while, and for; short-circuit boolean operators.
- break;, continue;, arrays, maps, indexed access, and assignment.
- Imports: import "lib/numbers.sg" as numbers;
- Built-ins for ranges, collections, type inspection, and string conversion.
- Strict JSON parsing and deterministic compact serialization; duplicate keys, non-standard constants, unsupported values, overflow, and nonzero underflow-to-zero are rejected.
- Structured lexical/syntax diagnostics, normalized runtime errors, and an official formatter.

## Requirements and installation

Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run

```bash
singular path/to/program.sg
```

## Example

```singular
fn square(x) -> {
  return x * x;
}
value total = 0;
for n in range(1, 5) {
  total = total + square(n);
}
value record = json_parse("{\"result\":\"ok\",\"total\":10}");
print(json_stringify(record));
```

## Numeric reproducibility contract

- Integer arithmetic uses arbitrary-precision integers.
- Decimal and scientific literals use IEEE-754 binary64. Non-finite values and nonzero values that underflow to zero are rejected; representable subnormals remain valid.
- Comparisons are exact, with no implicit epsilon. Mixed integer/float comparisons preserve the integer operand's value rather than rounding it to binary64 first.
- JSON serialization is compact, sorts object keys lexicographically, and preserves Unicode. This guarantees stable output for the same values, not bit-identical floating-point calculations across different runtimes.

## Test and formatting

```bash
python -m pytest
singular format examples/square.sg
singular format --check examples/square.sg
```

Singular favors explicit syntax, predictable execution, and reproducible results. It should remain small and deterministic rather than adopting expressive conveniences merely because they are easy to implement.
