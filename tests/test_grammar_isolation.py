from src.singular.runner import run

def test_singular_keyword_isolation():
    output=[]
    run('value let = 42; print(let);', output.append)
    assert output == ['42']
