from src.singular.runner import run

def test_singular_loop_and_sum():
    output=[]
    run('value total = 0; for n in range(1, 5) { total = total + n; } print(total);', output.append)
    assert output == ['10']

def test_singular_map_and_index_access():
    output=[]
    run('value data = {"answer": 42}; print(data["answer"]);', output.append)
    assert output == ['42']
