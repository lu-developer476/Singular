import pytest

from src.common.errors import RuntimeLangError
from src.singular.runner import run


def test_module_import_and_nested_relative_imports(tmp_path):
    library = tmp_path / 'lib'
    library.mkdir()
    (library / 'base.sg').write_text('fn triple(x) -> { return x * 3; }', encoding='utf-8')
    (library / 'math.sg').write_text('import "base.sg" as base; fn answer() -> { return base.triple(14); }', encoding='utf-8')
    output = []
    run('import "lib/math.sg" as math; print(math.answer());', output.append, source_path=tmp_path / 'main.sg')
    assert output == ['42']


def test_module_cache_executes_a_module_once(tmp_path):
    (tmp_path / 'once.sg').write_text('print("loaded"); value answer = 42;', encoding='utf-8')
    output = []
    run('import "once.sg" as first; import "once.sg" as second; print(second.answer);', output.append, source_path=tmp_path / 'main.sg')
    assert output == ['loaded', '42']


def test_module_cycles_are_controlled(tmp_path):
    (tmp_path / 'a.sg').write_text('import "b.sg" as b;', encoding='utf-8')
    (tmp_path / 'b.sg').write_text('import "a.sg" as a;', encoding='utf-8')
    with pytest.raises(RuntimeLangError, match='cyclic'):
        run('import "a.sg" as a;', source_path=tmp_path / 'main.sg')


def test_import_requires_file_backed_execution():
    with pytest.raises(RuntimeLangError, match='file-backed'):
        run('import "missing.sg" as missing;')
