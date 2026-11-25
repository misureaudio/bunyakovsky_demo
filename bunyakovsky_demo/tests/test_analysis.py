"""Tests for teacher mode (analysis.py, v1.4.0).

All stdlib; the sympy oracle (optional) cross-checks the Z-factorizer.
"""
import pytest

from bunyakovsky_demo.analysis import (analyze, irreducible_z, parse_poly,
                                       render_analysis_md)


# ---- parse_poly ----
def test_parse_expressions():
    assert parse_poly("x^2 + 1") == [1, 0, 1]
    assert parse_poly("x^2+x+41") == [41, 1, 1]
    assert parse_poly("41 + x + x^2") == [41, 1, 1]
    assert parse_poly("-x^2 + 5x + 1") == [1, 5, -1]
    assert parse_poly("5 - x^2") == [5, 0, -1]
    assert parse_poly("3x^2") == [0, 0, 3]
    assert parse_poly("x") == [0, 1]
    assert parse_poly("x**3 - x + 1") == [1, -1, 0, 1]
    assert parse_poly("2*x^2 - 3*x + 1") == [1, -3, 2]
    assert parse_poly("x^2 - 2x + 1") == [1, -2, 1]
    assert parse_poly("n^2 + n + 41") == [41, 1, 1]      # any single letter
    assert parse_poly("x^1 + 1") == [1, 1]


def test_parse_unicode_and_lists():
    assert parse_poly("x² + 1") == [1, 0, 1]
    assert parse_poly("x³ − x + 1") == [1, -1, 0, 1]     # unicode minus
    assert parse_poly("1 0 1") == [1, 0, 1]
    assert parse_poly("41, 1, 1") == [41, 1, 1]
    assert parse_poly("42") == [42]
    assert parse_poly("-7") == [-7]
    assert parse_poly("1 2 0 0") == [1, 2]               # trailing zeros cut


def test_parse_errors():
    for bad in ("", "   ", "1.5x", "x^1.5", "x + y", "hello world",
                "x^x", "2 x 3", "x^2++1", "3.0"):
        with pytest.raises(ValueError):
            parse_poly(bad)


# ---- irreducible_z (decidable) ----
def test_irreducible_true_cases():
    for cs in ([1, 0, 1], [41, 1, 1], [2, 0, 0, 1], [1, -1, 0, 0, 0, 1],
               [2, 3, 0, 1], [1, 1, 1, 1, 1], [2, 3]):
        ok, facs = irreducible_z(cs)
        assert ok, cs
        assert facs == [f for f in facs]                  # list returned
        assert len(facs) == 1


def test_blind_spots_are_decided_irreducible():
    # THE headline feature: x^4+1 and x^4-10x^2+1 have no mod-p certificate
    # (check_hypotheses says satisfies=False) but ARE irreducible over Z.
    for cs in ([1, 0, 0, 0, 1], [1, 0, -10, 0, 1]):
        ok, _ = irreducible_z(cs)
        assert ok, cs


def test_reducible_cases_with_factors():
    ok, facs = irreducible_z([1, 3, 2])                  # (2x+1)(x+1)
    assert not ok
    assert sorted(map(tuple, facs)) == sorted([(1, 2), (1, 1)])
    ok, facs = irreducible_z([1, 0, 0, 0, -1])           # x^4 - 1
    assert not ok and len(facs) == 3                     # (x-1)(x+1)(x^2+1)
    ok, facs = irreducible_z([2, 0, 2])                  # 2x^2 + 2 = 2*(x^2+1)
    assert not ok
    assert [2] in facs and [1, 0, 1] in facs


def test_repeated_factors():
    ok, facs = irreducible_z([1, 0, 2, 0, 1])            # (x^2+1)^2
    assert not ok
    assert facs == [[1, 0, 1], [1, 0, 1]]
    ok, facs = irreducible_z([-1, 0, 0, 1])              # x^3 - 1
    assert not ok and len(facs) == 2                     # (x-1)(x^2+x+1)


def test_degree_zero():
    ok, facs = irreducible_z([5])
    assert not ok and facs is None


def test_factors_multiply_back():
    from bunyakovsky_demo.analysis import _z_mul
    for cs in ([1, 3, 2], [1, 0, 0, 0, -1], [2, 0, 2], [1, 0, 2, 0, 1],
               [6, -5, 1], [1, 0, -10, 0, 1]):
        ok, facs = irreducible_z(cs)
        prod = [1]
        for g in facs:
            prod = _z_mul(prod, g)
        # equal up to sign/content normalization
        from bunyakovsky_demo.bunyakovsky import evaluate
        for x in (2, 3, 5, 7, 11):
            assert abs(evaluate(prod, x)) == abs(evaluate(cs, x))


# ---- sympy oracle for the Z-factorizer (optional) ----
def test_factorizer_vs_sympy():
    pytest.importorskip("sympy")
    from sympy import Poly, factor_list
    from sympy.abc import x as sx

    cases = [[1, 0, 1], [41, 1, 1], [1, 3, 2], [1, 0, 0, 0, 1],
             [1, 0, -10, 0, 1], [1, -1, 0, 0, 0, 1], [1, 0, 0, 0, -1],
             [2, 0, 2], [1, 0, 2, 0, 1], [6, -5, 1], [2, 3, 0, 1],
             [1, 1, 1, 1, 1], [-1, 0, 0, 1], [4, -4, 1]]
    for cs in cases:
        ok, facs = irreducible_z(cs)
        content, fac_list = factor_list(Poly(list(reversed(cs)), sx))
        ref_degs = sorted([p.degree() for p, m in fac_list
                           for _ in range(m) if p.degree() > 0])
        got_degs = sorted(len(g) - 1 for g in facs if len(g) > 1)
        assert got_degs == ref_degs, cs
        # our `ok` means: exactly one irreducible factor of positive degree
        # and no constant prime factors
        n_const = len([g for g in facs if len(g) == 1])
        assert ok == (len(ref_degs) == 1 and n_const == 0), cs


# ---- analyze ----
def test_analyze_euler():
    a = analyze([41, 1, 1], N=2000, pmax=500)
    assert a["satisfies"] is True
    assert a["irreducibility"]["state"] == "certified"
    assert a["irreducibility"]["certificate_prime"] == 2
    assert a["first_composite"] == (40, 1681)
    assert a["prime_run"] == (1, 39)                     # n=1..39 (scan n>=1)
    md = render_analysis_md(a)
    assert "# Analysis" in md and "| Hypothesis" in md
    assert "certified mod $p = 2$" in md


def test_analyze_blind_spot_satisfies():
    a = analyze([1, 0, 0, 0, 1], N=1000, pmax=300)       # x^4 + 1
    assert a["satisfies"] is True                        # the fix vs check_hypotheses
    assert a["irreducibility"]["state"] == "decided"
    md = render_analysis_md(a)
    assert "blind spot" in md


def test_analyze_fixed_divisor():
    a = analyze([2, 1, 1], N=1000, pmax=300)             # x^2+x+2
    assert a["satisfies"] is False
    assert a["fixed_divisor"] == 2
    assert a["C"] == 0.0                                 # omega(2)=2=p kills it
    assert all(c["empirical"] == 0 for c in a["counts"])


def test_analyze_reducible_shows_factors():
    a = analyze([1, 3, 2], N=500, pmax=300)
    assert a["satisfies"] is False
    assert a["irreducibility"]["state"] == "reducible"
    md = render_analysis_md(a)
    assert "2x + 1" in md and "x + 1" in md


def test_analyze_negative_leading():
    a = analyze([1, 5, -1], N=500, pmax=300)
    assert a["positive_leading"] is False
    assert a["satisfies"] is False


def test_analyze_mr_range_guard():
    a = analyze([1, -1, 0, 0, 0, 1], N=100000, pmax=200)  # x^5-x+1 at 1e5 > 3.3e24
    assert a["n_max"] < 100000
    assert any("3.3e24" in w for w in a["warnings"])


def test_analyze_degree_zero():
    a = analyze([7], N=100, pmax=100)
    assert a["satisfies"] is False
    assert any("degree 0" in w for w in a["warnings"])


def test_analyze_mirror_polynomial():
    # x^2 - x + 41 = Euler(x-1): 41 prime values in a row for n = 0..40,
    # so within n >= 1 the run is n = 1..40 (40 primes), f(41) = 41^2.
    a = analyze([41, -1, 1], N=1000, pmax=500)
    assert a["prime_run"] == (1, 40)
    assert a["first_composite"] == (41, 1681)


# ---- CLI wiring ----
def test_cli_poly_card(capsys):
    from bunyakovsky_demo.demo import cli
    cli(["--poly", "x^2 + x + 41", "--N", "1000", "--pmax", "300"])
    out = capsys.readouterr().out
    assert "# Analysis: $x^{2} + x + 41$" in out
    assert "Satisfies all three" in out


def test_cli_poly_bad_input(capsys):
    from bunyakovsky_demo.demo import cli
    with pytest.raises(SystemExit) as e:
        cli(["--poly", "1.5x + q"])
    assert e.value.code == 2
    assert "error" in capsys.readouterr().err


def test_cli_multiple_polys(capsys):
    from bunyakovsky_demo.demo import cli
    cli(["--poly", "x^2+1", "--poly", "x^2+x+2", "--N", "300",
         "--pmax", "200"])
    out = capsys.readouterr().out
    assert out.count("# Analysis") == 2
