import pytest
from priority_calculator import parsing, eval_no_paren, eval_with_paren, InvalidOperatorError

# ---------- parsing 테스트 ----------
@pytest.mark.parametrize("expr, expected", [
    ("3 + 4", [3.0, "+", 4.0]),
    ("10 / 2", [10.0, "/", 2.0]),
    ("-5 + 2", [-5.0, "+", 2.0]),
])
def test_parsing_ok(expr, expected):
    assert parsing(expr) == expected

@pytest.mark.parametrize("expr", [
    "",                     # 빈 입력
    "3 3 +",                # 잘못된 패턴
    "3 ^ 2",                # 지원 안 하는 연산자
    "NaN + 1",              # NaN
    "inf + 1",              # inf
])
def test_parsing_error(expr):
    with pytest.raises((ValueError, InvalidOperatorError)):
        parsing(expr)

# ---------- eval_no_paren 테스트 ----------
@pytest.mark.parametrize("tokens, expected", [
    ([3.0, "+", 4.0], 7.0),
    ([3.0, "+", 5.0, "*", 2.0], 13.0),   # * 먼저
    ([10.0, "-", 6.0, "/", 3.0], 8.0),   # / 먼저
])
def test_eval_no_paren(tokens, expected):
    assert eval_no_paren(tokens) == expected

def test_eval_no_paren_zero_div():
    with pytest.raises(ZeroDivisionError):
        eval_no_paren([10.0, "/", 0.0])

# ---------- eval_with_paren 테스트 ----------
@pytest.mark.parametrize("expr, expected", [
    ("( 4 + 5 ) * ( 3 - 2 )", 9.0),
    ("3 + ( 2 * 5 ) - 1", 12.0),
    ("( 3 + 2 ) * ( 4 - ( 1 + 1 ) )", 10.0),
])
def test_eval_with_paren_ok(expr, expected):
    assert eval_with_paren(expr) == expected

@pytest.mark.parametrize("expr", [
    "( 3 + 2",            # 닫는 괄호 없음
    "3 + 2 )",            # 여는 괄호 없음
    "( 3 + ( 2 * 5 )",    # 짝 불일치
])
def test_eval_with_paren_error(expr):
    with pytest.raises(ValueError):
        eval_with_paren(expr)
