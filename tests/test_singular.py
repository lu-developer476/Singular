from src.singular.runner import run

def test_singular_calculation():
    output=[]
    run('fn square(x) -> { return x * x; } print(square(7));',output.append)
    assert output == ['49']
