from src.common.errors import ParseError, RuntimeLangError
from src.singular.runner import run


def test_invalid_assignment_target_is_a_parse_error():
    import pytest
    with pytest.raises(ParseError, match='Invalid assignment target'):
        run('(1) = 2;')


def test_loop_control_inside_function_cannot_escape_to_caller():
    import pytest
    with pytest.raises(RuntimeLangError, match='loop control'):
        run('fn stop() -> { break; } while true { stop(); }')
