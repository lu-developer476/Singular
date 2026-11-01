from src.singular.formatter import format_source


def test_formatter_normalizes_spacing_and_indentation():
    source = 'fn square(x)->{return x*x;}value total=0;for n in range(1,5){total=total+square(n);}print(total);'
    expected = 'fn square(x) -> {\n    return x * x;\n}\nvalue total = 0;\nfor n in range(1, 5) {\n    total = total + square(n);\n}\nprint(total);\n'
    assert format_source(source) == expected


def test_formatter_is_idempotent():
    source = 'value total=0;for n in range(1,5){total=total+n;}print(total);'
    formatted = format_source(source)
    assert format_source(formatted) == formatted
