# Singular

**Singular** es un lenguaje minimalista y determinista para cálculo, transformaciones de datos y programas pequeños verificables.

Esta es la implementación independiente de Singular, separada del prototipo conjunto `Languages`. La versión inicial conserva el comportamiento de `Languages` v1.8.0. Lexer, AST y runtime viven en este repositorio para que el lenguaje pueda evolucionar y publicar versiones sin depender de Kitsune.

## Características de v1.8.0

- Sintaxis explícita: `value`, `fn`, `print`, sentencias terminadas en `;`.
- Funciones, closures, scopes léxicos, condicionales y bucles `while` / `for`.
- `break;` y `continue;` locales al bucle actual.
- Arrays, mapas, acceso indexado y asignación mutable.
- Builtins: `range`, `len`, `push`, `pop`, `first`, `last`, `join`, `split`, `keys`, `values`, `has`, `type`, `str`.
- Imports `import "lib/numbers.sg" as numbers;`, con caché, scopes aislados y protección contra rutas externas y ciclos.
- CLI `singular` y entrada estándar mediante `singular -`.

## Requisitos e instalación

Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -e ".[dev]"
```

## Ejecutar

```bash
singular examples/hello.sg
```

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

## Módulos

Los imports son explícitos y requieren punto y coma. Se resuelven desde el archivo importador y quedan confinados al directorio raíz del proyecto:

```singular
import "lib/numbers.sg" as numbers;
print(numbers.double(21));
```

Los nombres top-level que no empiezan con `_` se exponen en el alias. Cada módulo se ejecuta una vez por intérprete y conserva su entorno para closures.

## Desarrollo

```bash
python -m pytest
```

GitHub Actions ejecuta la suite en Python 3.11, 3.12 y 3.13. Consulta [`docs/language.md`](docs/language.md) para la referencia del lenguaje.

## Filosofía

Singular prioriza previsibilidad, sintaxis explícita y resultados reproducibles. Su evolución debe favorecer programas pequeños verificables, transformaciones de datos y cálculo; no añadir expresividad por conveniencia si compromete su determinismo.