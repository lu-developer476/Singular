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
