"""Tests for the Bunyakovsky-conjecture demo package.

Expected values were measured on 2026-11-22 with the workspace venv
(Python 3.11.9) and re-verified on Python 3.14.
"""
import math
import subprocess
import sys

from bunyakovsky_demo.bunyakovsky import (
    bunyakovsky_constant, check_hypotheses, degree, evaluate, fixed_divisor,
    format_poly, irreducible_certificate, is_irreducible_mod_p, is_prime,
    predicted_count, primes_upto, roots_mod_p, scan_primes)


# ---- Task 2: polynomial core ----
def test_package_imports():
    import bunyakovsky_demo  # noqa: F401


def test_evaluate_horner():
    assert evaluate([1, 0, 1], 10) == 101          # x^2 + 1
    assert evaluate([41, 1, 1], 40) == 1681        # x^2 + x + 41 at 40
    assert evaluate([7], 999) == 7


def test_degree_strips_trailing_zeros():
    assert degree([1, 0, 1]) == 2
    assert degree([5, 0, 0, 0]) == 0
    assert degree([1, 2, 0, 0]) == 1


def test_format_poly():
    assert format_poly([1, 0, 1]) == "x^2 + 1"
    assert format_poly([41, 1, 1]) == "x^2 + x + 41"
    assert format_poly([2, 3]) == "3x + 2"
    assert format_poly([1, 3, 2]) == "2x^2 + 3x + 1"
    assert format_poly([1, 5, -1]) == "-x^2 + 5x + 1"


# ---- Task 3: fixed divisor ----
def test_fixed_divisor_values():
    assert fixed_divisor([1, 0, 1]) == 1          # x^2 + 1
    assert fixed_divisor([2, 1, 1]) == 2          # x^2 + x + 2: always even
    assert fixed_divisor([41, 1, 1]) == 1         # x^2 + x + 41
    assert fixed_divisor([2, 3]) == 1             # 3x + 2
    assert fixed_divisor([1, 3, 2]) == 1          # (2x+1)(x+1): fd = 1!
    assert fixed_divisor([1, 1, 0, 1]) == 1       # x^3 + x + 1


def test_fixed_divisor_matches_brute_force():
    """Theorem: gcd of all values == gcd(f(0)..f(deg)). Check vs brute force."""
    for cs in ([1, 0, 1], [2, 1, 1], [41, 1, 1], [2, 3], [1, 3, 2],
               [1, 1, 0, 1], [6, 5, 4, 3]):
        brute = 0
        for k in range(1, 201):
            brute = math.gcd(brute, evaluate(cs, k))
        assert fixed_divisor(cs) == brute


# ---- Task 4: sieve + Miller-Rabin ----
def test_primes_upto():
    assert primes_upto(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert primes_upto(1) == []
    assert len(primes_upto(1000)) == 168


def test_is_prime_small():
    for n in range(2, 100):
        assert is_prime(n) == (n in primes_upto(100))


def test_is_prime_carmichael():
    # Measured 2026-11-22: trial division alone would call these prime.
    assert not is_prime(561)
    assert not is_prime(3215031751)
    assert is_prime(104729)
    assert is_prime(1000000007)
    assert not is_prime(0)
    assert not is_prime(1)
    assert not is_prime(-7)


# ---- Task 5: omega_f(p) ----
def test_roots_of_x2_plus_1():
    assert [roots_mod_p([1, 0, 1], p)
            for p in (2, 3, 5, 7, 11, 13)] == [1, 0, 2, 0, 0, 2]
    # p=2: x=1 double root -> 1 solution; p=5: x=2,3; p=13: x=5,8.


def test_roots_linear_and_degenerate():
    assert roots_mod_p([2, 3], 5) == 1     # 3x+2=0 mod 5 -> x=1
    # mod 3 the leading coeff vanishes: reduction is the constant 2 -> 0 roots
    assert roots_mod_p([2, 3], 3) == 0


# ---- Task 6: irreducibility certificate ----
def test_is_irreducible_mod_p_basics():
    assert is_irreducible_mod_p([1, 0, 1], 3)        # x^2+1 no roots in F3
    assert not is_irreducible_mod_p([1, 0, 1], 5)    # splits mod 5
    assert is_irreducible_mod_p([1, 1, 0, 1], 2)     # x^3+x+1, no F2 roots


def test_certificates_found():
    ok, p = irreducible_certificate([1, 0, 1])       # x^2 + 1
    assert ok and p == 3
    ok, p = irreducible_certificate([41, 1, 1])      # x^2 + x + 41 (irred mod 2)
    assert ok and p == 2
    ok, p = irreducible_certificate([2, 3])          # linear: certified at p=2
    assert ok and p == 2


def test_no_certificate_for_reducible():
    ok, p = irreducible_certificate([1, 3, 2])       # (2x+1)(x+1): reducible
    assert not ok and p is None


# ---- Task 7: hypothesis gate ----
def test_hypotheses_all_satisfied():
    for cs in ([2, 3], [1, 0, 1], [41, 1, 1], [1, 1, 0, 1]):
        h = check_hypotheses(cs)
        assert h["satisfies"], cs
        assert h["no_fixed_prime"] and h["irreducible_certified"]


def test_hypotheses_fixed_prime_violation():
    h = check_hypotheses([2, 1, 1])              # x^2+x+2
    assert h["fixed_divisor"] == 2
    assert not h["no_fixed_prime"]
    assert h["irreducible_certified"]            # irreducible mod 3 -- yes
    assert not h["satisfies"]


def test_hypotheses_reducible_violation():
    h = check_hypotheses([1, 3, 2])              # (2x+1)(x+1)
    assert h["no_fixed_prime"]                   # sneaks past hypothesis 3!
    assert not h["irreducible_certified"]
    assert not h["satisfies"]


def test_hypotheses_negative_leading():
    h = check_hypotheses([1, 5, -1])             # -x^2 + 5x + 1
    assert not h["positive_leading"]
    assert not h["satisfies"]


# ---- Task 8: prime scan ----
def test_euler_polynomial_40_primes():
    primes = scan_primes([41, 1, 1], 39, start=0)
    assert len(primes) == 40                     # n = 0..39 all prime
    assert primes[0] == (0, 41)
    assert scan_primes([41, 1, 1], 40, start=0)[-1][0] == 39   # n=40 fails
    assert evaluate([41, 1, 1], 40) == 41 * 41   # first composite is 41^2


def test_euler_primes_resume_at_42():
    # f(41) = 41*43 composite; true primes resume at n = 42 (f(42) = 1847).
    assert not is_prime(evaluate([41, 1, 1], 41))
    assert is_prime(evaluate([41, 1, 1], 42))


def test_reducible_never_prime_beyond_factors():
    # (2x+1)(x+1): both factors > 1 for n >= 2 -> zero primes. Measured: 0.
    assert scan_primes([1, 3, 2], 300, start=2) == []


def test_fixed_prime_only_produces_that_prime():
    # x^2+x+2 always even; the single even prime 2 is hit at n=-2, never n>=1.
    assert scan_primes([2, 1, 1], 100, start=1) == []


def test_x2_plus_1_count_1e4():
    assert len(scan_primes([1, 0, 1], 10000)) == 841   # measured 2026-11-22


# ---- Task 9: Bateman-Horn constant ----
def test_identity_polynomial_gives_li():
    # f(t) = t has omega(p) = 1 for every p -> every factor is 1 -> C = 1.
    assert bunyakovsky_constant([0, 1], pmax=1000) == 1.0


def test_constant_x2_plus_1_truncated():
    # Measured 2026-11-22, pmax=10^4: 1.371023 (literature 1.37281...).
    c = bunyakovsky_constant([1, 0, 1], pmax=10000)
    assert 1.34 < c < 1.40


def test_constant_positive_for_satisfying_polys():
    for cs in ([2, 3], [41, 1, 1], [1, 1, 0, 1]):
        assert bunyakovsky_constant(cs, pmax=2000) > 0


# ---- Task 10: predicted count ----
def test_predicted_count_x2_plus_1():
    c = bunyakovsky_constant([1, 0, 1], pmax=10000)
    pred = predicted_count([1, 0, 1], 100000, C=c)
    # Measured: empirical 6656 vs predicted 6601.1 -> ratio 1.0083.
    assert 0.95 < 6656 / pred < 1.05


def test_predicted_count_euler():
    c = bunyakovsky_constant([41, 1, 1], pmax=5000)   # measured C ~ 6.67
    pred = predicted_count([41, 1, 1], 10000, C=c)
    assert 0.95 < 4148 / pred < 1.05


def test_predicted_count_computes_C_when_omitted():
    # Measured 2026-11-22: empirical at N=1e3 is 112; prediction ~ 120.9.
    pred = predicted_count([1, 0, 1], 1000, pmax=2000)
    assert 100 < pred < 140


# ---- Higher-degree screening (measured 2026-11-22; C at pmax=3000) ----
def test_new_satisfying_certificates():
    ok, p = irreducible_certificate([2, 0, 0, 1])          # x^3 + 2
    assert ok and p == 7
    ok, p = irreducible_certificate([1, 1, 1, 1, 1])       # Phi_5
    assert ok and p == 2
    ok, p = irreducible_certificate([1, -1, 0, 0, 0, 1])   # x^5 - x + 1
    assert ok and p == 3
    for cs in ([2, 0, 0, 1], [1, 1, 1, 1, 1], [1, -1, 0, 0, 0, 1],
               [41, -1, 1, 1]):
        assert check_hypotheses(cs)["satisfies"], cs


def test_new_counts_1e4():
    assert len(scan_primes([2, 0, 0, 1], 10000)) == 520        # x^3 + 2
    assert len(scan_primes([1, 1, 1, 1, 1], 10000)) == 950     # Phi_5
    assert len(scan_primes([1, -1, 0, 0, 0, 1], 10000)) == 1246  # x^5-x+1
    assert len(scan_primes([41, -1, 1, 1], 10000)) == 189      # unlucky one


def test_irreducible_but_fixed_prime_degree3():
    # x^3+3x+2: irreducible (cert p=5, no rational root) yet x^3+3x is
    # always even -> no primes for n >= 1. (NOT x^3+x+2, which factors.)
    h = check_hypotheses([2, 3, 0, 1])
    assert h["fixed_divisor"] == 2 and h["irreducible_certified"]
    assert not h["satisfies"]
    assert scan_primes([2, 3, 0, 1], 200, start=1) == []


def _factor(m: int) -> set[int]:
    fs: set[int] = set()
    d = 2
    while d * d <= m:
        while m % d == 0:
            fs.add(d)
            m //= d
        d += 1
    if m > 1:
        fs.add(m)
    return fs


def test_cyclotomic_divisors_mod_5():
    # q | Phi_5(n), q != 5  =>  ord_q(n) = 5  =>  q = 1 (mod 5).
    for n in range(2, 41):
        for q in _factor(evaluate([1, 1, 1, 1, 1], n)):
            assert q == 5 or q % 5 == 1, (n, q)


def test_contrast_constants():
    c_low = bunyakovsky_constant([41, -1, 1, 1], pmax=3000)     # 0.4366
    c_high = bunyakovsky_constant([1, -1, 0, 0, 0, 1], pmax=3000)  # 4.9047
    assert 0.42 < c_low < 0.46
    assert 4.85 < c_high < 4.96


def test_blind_spots_not_certified_but_prime_rich():
    # x^4+1 (Gal C2xC2) and x^4-10x^2+1 (V4): irreducible over Z, but
    # reducible mod every prime -> no certificate; empirically rich anyway.
    for cs in ([1, 0, 0, 0, 1], [1, 0, -10, 0, 1]):
        h = check_hypotheses(cs)
        assert h["fixed_divisor"] == 1
        assert not h["irreducible_certified"]
    assert len(scan_primes([1, 0, 0, 0, 1], 10000)) == 790
    assert len(scan_primes([1, 0, -10, 0, 1], 10000)) == 920


# ---- Task 11: demo smoke ----
def test_public_api_surface():
    """Every documented public name is importable from the package root.

    Regression: format_poly was listed in the package docstring but
    missing from the actual imports/__all__.
    """
    import bunyakovsky_demo as pkg

    assert set(pkg.__all__) == {
        "__version__",
        "analyze", "analyze_tuple", "admissible", "bunyakovsky_constant",
        "check_hypotheses", "degree",
        "evaluate", "fixed_divisor", "format_poly", "hypothesis_h_constant",
        "irreducible_certificate",
        "irreducible_z", "is_irreducible_mod_p", "is_prime", "parse_poly",
        "predicted_count", "primes_upto", "render_analysis_md",
        "render_census_md", "render_tuple_md", "run_census", "roots_mod_p",
        "scan_primes"}
    for name in pkg.__all__:
        if name == "__version__":  # the only non-callable export (a str)
            assert isinstance(pkg.__version__, str) and pkg.__version__
        else:
            assert callable(getattr(pkg, name))


def test_demo_module_runs():
    import os
    from pathlib import Path

    env = dict(os.environ)
    src = str(Path(__file__).resolve().parents[1] / "src")
    env["PYTHONPATH"] = os.pathsep.join(
        filter(None, [src, env.get("PYTHONPATH", "")]))
    r = subprocess.run(
        [sys.executable, "-m", "bunyakovsky_demo.demo",
         "--N", "2000", "--pmax", "1000"],
        capture_output=True, text=True, timeout=180, env=env)
    assert r.returncode == 0
    for needle in ("# Bunyakovsky", "$x^{2} + 1$", "## 2. Euler spotlight",
                   "| ratio |", "|:---"):
        assert needle in r.stdout
