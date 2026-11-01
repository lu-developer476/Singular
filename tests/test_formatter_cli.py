import pytest
from src.singular.__main__ import main

def test_formatter_cli(tmp_path, monkeypatch):
    path=tmp_path / 'sample.sg'
    path.write_text('value total=1;print(total);',encoding='utf-8')
    monkeypatch.setattr('sys.argv',['singular','format','--check',str(path)])
    with pytest.raises(SystemExit) as error: main()
    assert error.value.code == 1
    monkeypatch.setattr('sys.argv',['singular','format',str(path)])
    main()
    assert path.read_text(encoding='utf-8') == 'value total = 1;\nprint(total);\n'
    monkeypatch.setattr('sys.argv',['singular','format','--check',str(path)])
    main()
