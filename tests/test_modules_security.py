def test_imports_cannot_escape_project_root(tmp_path):
    import pytest
    from src.common.errors import RuntimeLangError
    from src.singular.runner import run
    (tmp_path.parent / 'outside.sg').write_text('print(1);', encoding='utf-8')
    with pytest.raises(RuntimeLangError, match='escapes'):
        run('import "../outside.sg" as outside;', source_path=tmp_path / 'main.sg')


def test_import_extension_must_match_language(tmp_path):
    import pytest
    from src.common.errors import RuntimeLangError
    from src.singular.runner import run
    with pytest.raises(RuntimeLangError, match='extension'):
        run('import "module.kit" as wrong;', source_path=tmp_path / 'main.sg')
