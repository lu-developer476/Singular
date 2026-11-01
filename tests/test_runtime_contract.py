import pytest

from src.common.errors import ParseError, RuntimeLangError
from src.singular.runner import run


def test_boolean_operators_short_circuit():
    output = []
    run('print(false and missing_name); print(true or another_missing_name);', output.append)
    assert output == ['false', 'true']


@pytest.mark.parametrize('source', ['print(1 / 0);', 'print([][0]);', 'print(len(1));'])
def test_runtime_failures_are_language_errors(source):
    with pytest.raises(RuntimeLangError):
        run(source)


def test_parser_errors_have_a_language_error_type_and_location():
    with pytest.raises(ParseError) as error:
        run('value = 10;')
    assert error.value.line == 1
    assert error.value.column is not None
