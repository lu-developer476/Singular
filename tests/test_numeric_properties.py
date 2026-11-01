import pytest

from src.common.errors import RuntimeLangError
from src.singular.runner import run


def evaluate(source):
    output = []
    run(source, output.append)
    return output


@pytest.mark.parametrize(
    "integer",
    [
        "0",
        "1",
        "-1",
        "9007199254740991",
        "9007199254740992",
        "9007199254740993",
        "18446744073709551616",
        "115792089237316195423570985008687907853269984665640564039457584007913129639935",
    ],
)
def test_integer_arithmetic_identities_hold_without_precision_loss(integer):
    assert evaluate(
        f"print(({integer}) + 0); print(({integer}) - ({integer})); "
        f"print(({integer}) * 1); print(({integer}) == ({integer}));"
    ) == [integer, "0", integer, "true"]


@pytest.mark.parametrize(
    "number",
    [
        "5e-324",
        "1e-323",
        "2.2250738585072014e-308",
        "1.7976931348623157e308",
    ],
)
def test_json_accepts_representable_binary64_boundary_values(number):
    assert evaluate(f'print(json_parse("{number}") > 0);') == ["true"]


@pytest.mark.parametrize("number", ["1e-324", "-1e-324", "1e309", "-1e309"])
def test_json_rejects_values_outside_representable_binary64_range(number):
    with pytest.raises(RuntimeLangError):
        run(f'print(json_parse("{number}"));')


def test_numeric_comparison_near_integer_float_precision_boundary_is_exact():
    assert evaluate(
        "print(9007199254740991 < 9007199254740992.0); "
        "print(9007199254740992 == 9007199254740992.0); "
        "print(9007199254740993 > 9007199254740992.0);"
    ) == ["true", "true", "true"]
