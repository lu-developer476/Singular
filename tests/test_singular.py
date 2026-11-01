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
