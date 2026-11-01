# Singular

**Singular** is a minimal, deterministic language for calculations, data transformations, and small verifiable programs.

## Language surface (v2.5.3)

- \`.sg\` source files.
- Explicit declarations: \`value\`, \`fn\`, \`print\`.
- Semicolon-terminated statements and brace-delimited blocks.
- Integer, decimal, and scientific-notation numeric literals (\`1.25e-2\`).
- Decimal/scientific literals use finite IEEE-754 binary64 values; overflow and nonzero underflow-to-zero are rejected.
- Functions, lexical scopes, closures, \`if\` / \`else\`, \`while\`, and \`for\`; short-circuit boolean operators.
- \`break;\`, \`continue;\`, arrays, maps, indexed access, and assignment.
- Imports: \`import "lib/numbers.sg" as numbers;\`.
- Built-ins for ranges, collections, type inspection, and string conversion.
- JSON built-ins: \`json_parse(text)\` and \`json_stringify(value)\`; compact, sorted output, preserved Unicode, and rejection of duplicate/non-text keys, unsupported values, non-standard constants, and out-of-range numbers.
- Structured lexical/syntax diagnostics, normalized runtime errors, and an official formatter.

## Requirements and installation

Python 3.11 or newer.

\`\`\`bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
\`\`\`

## Run

\`\`\`bash
singular path/to/program.sg
\`\`\`

## Example

\`\`\`singular
fn square(x) -> {
  return x * x;
}
value total = 0;
for n in range(1, 5) {
  total = total + square(n);
}
value record = json_parse("{\"result\":\"ok\",\"total\":10}");
print(json_stringify(record));
\`\`\`

## Test and formatting

\`\`\`bash
python -m pytest
singular format examples/square.sg
singular format --check examples/square.sg
\`\`\`

Singular favors explicit syntax, predictable execution, and reproducible results. It should remain small and deterministic rather than adopting expressive conveniences merely because they are easy to implement.
