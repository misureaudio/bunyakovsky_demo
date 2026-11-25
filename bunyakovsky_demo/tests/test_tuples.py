"""Tests for Hypothesis H tuple mode (tuples.py)."""
from bunyakovsky_demo import admissible, analyze_tuple, hypothesis_h_constant
from bunyakovsky_demo.demo import cli
from bunyakovsky_demo.tuples import (predicted_tuple_count, render_tuple_md,
                                     nu_mod_p, tuple_prime_scan)

TWIN = [[0, 1], [2, 1]]                       # x, x+2


def test_nu_twin():
    assert nu_mod_p(TWIN, 2) == 1              # x(x+2) = x^2 mod 2
    assert nu_mod_p(TWIN, 3) == 2              # roots 0, 1
    assert nu_mod_p(TWIN, 5) == 2              # roots 0, 3


def test_twin_constant_matches_literature():
    # Bateman-Horn for {x, x+2} = 2*C_2 = 1.32032... (twin-prime constant)
    c = hypothesis_h_constant(TWIN, pmax=10000)
    assert 1.31 < c < 1.33


def test_admissibility():
    assert admissible(TWIN) == (True, None)
    ok, w = admissible([[0, 1], [2, 1], [4, 1]])   # n, n+2, n+4
    assert ok is False and w == 3


def test_twin_scan_small():
    hits = tuple_prime_scan(TWIN, 100)
    ns = [n for n, _ in hits]
    assert ns == [3, 5, 11, 17, 29, 41, 59, 71]
    assert hits[0][1] == (3, 5)


def test_twin_prediction_accurate():
    n_max = 10000
    emp = len(tuple_prime_scan(TWIN, n_max))
    pred = predicted_tuple_count(TWIN, n_max, pmax=10000)
    assert 0.8 < emp / pred < 1.2


def test_analyze_twin():
    a = analyze_tuple(TWIN, N=5000)
    assert a["satisfies"] is True and a["twin"] is True
    assert a["C"] is not None and 1.2 < a["C"] < 1.4
    assert a["first"][0] == (3, (3, 5))
    md = render_tuple_md(a)
    assert "twin-prime conjecture" in md
    assert "| 1000 |" in md                    # counts table present


def test_analyze_inadmissible():
    a = analyze_tuple([[0, 1], [2, 1], [4, 1]], N=500)
    assert a["satisfies"] is False and a["witness"] == 3
    md = render_tuple_md(a)
    assert "(3, 5, 7)" in md


def test_analyze_reducible_member():
    # x^2 + 2x + 1 = (x+1)^2 : admissible but hypothesis 2 fails
    b = analyze_tuple([[1, 2, 1], [1, 1]], N=500)
    assert b["admissible"] is True
    assert b["satisfies"] is False
    md = render_tuple_md(b)
    assert "Hypothesis H fails" in md
    assert "x + 1" in md                       # factor shown in evidence


def test_cli_tuple(capsys):
    cli(["--tuple", "x, x+2"])
    out = capsys.readouterr().out
    assert "twin-prime conjecture" in out
