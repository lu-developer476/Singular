# Singular

**Singular** is a minimal, deterministic language for calculations, data transformations, and small verifiable programs.

## Language surface (v2.8.0)

- .sg source files.
- Explicit declarations: `value`, `fn`, `print`.
- Semicolon-terminated statements and brace-delimited blocks.
- Integer, decimal, and scientific-notation numeric literals.
- Integer arithmetic retains arbitrary precision; decimal/scientific values use finite IEEE-754 binary64.
- Decimal overflow and nonzero underflow-to-zero are rejected; representable subnormal values are accepted.
- Functions, lexical scopes, closures, if / else, while, and for; short-circuit boolean operators.
- `break;`, `continue;`, arrays, maps, indexed access, and assignment.
- Imports: `import "lib/numbers.sg" as numbers;`
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
value record = json_parse("{\\"result\\":\\"ok\\",\\"total\\":10}");
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

---

# Singular

**Singular** es un lenguaje minimalista y determinista para cálculos, transformaciones de datos y pequeños programas verificables.

## Características del lenguaje (v2.8.0)

- Archivos de código fuente con extensión .sg.
- Declaraciones explícitas: `value`, `fn` y `print`.
- Sentencias terminadas en punto y coma y bloques delimitados por llaves.
- Literales numéricos enteros, decimales y en notación científica.
- La aritmética entera conserva precisión arbitraria; los valores decimales y científicos utilizan IEEE-754 binary64 finito.
- Se rechazan el desbordamiento decimal y el subdesbordamiento no nulo a cero; se aceptan los valores subnormales representables.
- Funciones, ámbitos léxicos, closures, condicionales if / else y bucles while / for; operadores booleanos con evaluación de cortocircuito.
- `break;`, `continue;`, arrays, mapas, acceso por índice y asignación.
- Imports: `import "lib/numbers.sg" as numbers;`
- Funciones integradas para rangos, colecciones, inspección de tipos y conversión a texto.
- Análisis estricto de JSON y serialización compacta determinista; se rechazan claves duplicadas, constantes no estándar, valores no compatibles, desbordamientos y subdesbordamientos no nulos a cero.
- Diagnósticos léxicos y sintácticos estructurados, errores de ejecución normalizados y formateador oficial.

## Requisitos e instalación

Python 3.11 o superior.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Ejecución

```bash
singular path/to/program.sg
```

## Ejemplo

```singular
fn square(x) -> {
  return x * x;
}
value total = 0;
for n in range(1, 5) {
  total = total + square(n);
}
value record = json_parse("{\\"result\\":\\"ok\\",\\"total\\":10}");
print(json_stringify(record));
```

## Contrato de reproducibilidad numérica

- La aritmética entera utiliza enteros de precisión arbitraria.
- Los literales decimales y científicos utilizan IEEE-754 binary64. Se rechazan los valores no finitos y los valores no nulos que se convierten en cero por subdesbordamiento; los valores subnormales representables siguen siendo válidos.
- Las comparaciones son exactas y no aplican una tolerancia implícita. En comparaciones mixtas entre enteros y flotantes, se conserva el valor del operando entero en lugar de redondearlo primero a binary64.
- La serialización JSON es compacta, ordena lexicográficamente las claves de los objetos y conserva Unicode. Esto garantiza una salida estable para los mismos valores, pero no cálculos de punto flotante idénticos bit a bit entre distintos entornos de ejecución.

## Pruebas y formato

```bash
python -m pytest
singular format examples/square.sg
singular format --check examples/square.sg
```

Singular prioriza la sintaxis explícita, la ejecución predecible y los resultados reproducibles. Debe mantenerse pequeño y determinista, en lugar de incorporar comodidades expresivas solo porque sean fáciles de implementar.
