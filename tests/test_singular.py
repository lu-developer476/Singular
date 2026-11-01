from src.singular.runner import run


def test_singular_calculation():
    output=[]
    run('fn square(x) -> { return x * x; } print(square(7));',output.append)
    assert output == ['49']


def test_singular_supports_fractional_and_scientific_numbers():
    output = []
    run('print(1.25e-2); print(2e3); print(4.5);', output.append)
    assert output == ['0.0125', '2000.0', '4.5']


def test_singular_rejects_incomplete_numeric_exponents():
    import pytest
    from src.common.errors import LexError

    with pytest.raises(LexError):
        run('print(3e+);')


def test_singular_accepts_representable_subnormal_and_zero_values():
    output = []
    run('print(5e-324); print(0e-9999);', output.append)
    assert output == ['5e-324', '0.0']


def test_singular_rejects_float_literal_overflow_with_source_location():
    import pytest
    from src.common.errors import LexError

    with pytest.raises(LexError) as error:
        run('value ok = 1;\nprint(1e309);')
    assert error.value.line == 2
    assert error.value.column == 7
    assert 'finite floating-point range' in error.value.message


def test_singular_rejects_float_literal_underflow_to_zero_with_source_location():
    import pytest
    from src.common.errors import LexError

    with pytest.raises(LexError) as error:
        run('print(1e-9999);')
    assert error.value.line == 1
    assert error.value.column == 7
    assert 'smaller than the supported floating-point range' in error.value.message


def test_singular_rejects_non_finite_arithmetic_results():
    import pytest
    from src.common.errors import RuntimeLangError

    with pytest.raises(RuntimeLangError, match="non-finite"):
        run("print(1e308 * 1e308);")


def test_singular_preserves_integer_precision_and_binary64_arithmetic():
    output = []
    run("print(900719925474099312345 + 1); print(10 / 4); print(10 % 4);", output.append)
    assert output == ["900719925474099312346", "2.5", "2"]


def test_singular_normalizes_division_by_zero():
    import pytest
    from src.common.errors import RuntimeLangError

    with pytest.raises(RuntimeLangError):
        run("print(1 / 0);")


def test_singular_numeric_comparisons_are_exact_not_tolerance_based():
    output = []
    run("print(1 == 1.0); print(0.1 + 0.2 == 0.3); print(9007199254740993 == 9007199254740992);", output.append)
    assert output == ["true", "false", "false"]


def test_singular_json_serialization_is_stable_and_round_trips():
    output = []
    run(r'value data = json_parse("{\"z\":2,\"a\":\"café 🌙\"}"); print(json_stringify(data)); print(json_stringify(json_parse(json_stringify(data))));', output.append)
    assert output == ['{"a":"café 🌙","z":2}', '{"a":"café 🌙","z":2}']


def test_singular_json_rejects_non_finite_and_preserves_large_integers():
    import pytest
    from src.common.errors import RuntimeLangError

    with pytest.raises(RuntimeLangError):
        run('print(json_stringify({value: 1e308 * 1e308}));')
    output = []
    run('print(json_stringify({integer: 900719925474099312345}));', output.append)
    assert output == ['{"integer":900719925474099312345}']
