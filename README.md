# Singular

**Singular** is a minimal, deterministic language for calculations, data transformations, and small verifiable programs.

This repository contains the independent Python implementation of Singular, based on the v1.8.0 prototype. It does not depend on Kitsune or the original `Languages` repository.

## Current language surface

- `.sg` source files.
- Explicit declarations: `value`, `fn`, `print`.
- Semicolon-terminated statements and brace-delimited blocks.
- Functions, lexical scopes, closures, `if` / `else`, `while`, and `for`.
- `break;`, `continue;`, arrays, maps, indexed access, and assignment.
- Imports: `import "lib/numbers.sg" as numbers;`.
- Built-ins for ranges, collections, type inspection, and string conversion.

## Requirements

Python 3.11 or newer.

## Install

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
print(total);
```

## Test

```bash
python -m pytest
```

## Design principle

Singular favors explicit syntax, predictable execution, and reproducible results. It should remain small and deterministic rather than adopting expressive conveniences merely because they are easy to implement.
