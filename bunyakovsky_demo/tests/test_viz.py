"""Tests for the visualization layer (v1.2.0).

The data layer is stdlib-only and always runs; render/encode tests are
skipped when matplotlib (or ffmpeg, or moviepy) is absent. The sympy oracle
test is skipped when sympy is not installed.

Reference values: sympy 1.14.0 GF(p) factorizations, measured 2026-11-23
with the workspace venv (Python 3.11.9).
"""
import math

import pytest

from bunyakovsky_demo.viz import (bateman_horn_frames, cumulative_primes,
                                  draw_frame, encode, encode_moviepy,
                                  euler_frames, factorization_pattern,
                                  pattern_matrix, poster, predicted_series,
                                  render_stills, storyboard, omega_profile)
from bunyakovsky_demo.bunyakovsky import (bunyakovsky_constant, evaluate,
                                          is_prime, predicted_count,
                                          scan_primes)


# ---- data layer: cumulative_primes ----
def test_cumulative_primes_matches_scan():
    for cs in ([1, 0, 1], [41, 1, 1], [2, 0, 0, 1]):
        E = cumulative_primes(cs, 2000)
        assert E[2000] == len(scan_primes(cs, 2000))
        assert E[0] == 0
        assert all(E[i] <= E[i + 1] <= E[i] + 1 for i in range(2000))


def test_cumulative_primes_euler_run():
    # cumulative count starts at n = 1, so the famous 40-in-a-row run
    # (n = 0..39) reads as 39 hits; f(40) = 41^2 adds none; n = 42 adds one.
    E = cumulative_primes([41, 1, 1], 45)
    assert E[39] == 39
    assert E[40] == 39
    assert E[42] == 40


# ---- data layer: predicted_series ----
def test_predicted_series_agrees_with_predicted_count():
    cs = [1, 0, 1]
    C = bunyakovsky_constant(cs, pmax=2000)
    P = predicted_series(cs, 10000, C=C)
    assert P[0] == P[1] == P[2] == 0.0
    ref = predicted_count(cs, 10000, C=C, M=200000)
    assert abs(P[10000] - ref) / ref < 5e-4


def test_predicted_series_monotone():
    P = predicted_series([41, 1, 1], 500, C=6.67)
    assert all(P[i] <= P[i + 1] for i in range(2, 500))


# ---- data layer: omega_profile ----
def test_omega_profile_values():
    prof = dict(omega_profile([1, 0, 1], 13))
    assert [prof[p] for p in (2, 3, 5, 7, 11, 13)] == [1, 0, 2, 0, 0, 2]


def test_omega_detects_fixed_prime():
    # x^2+x+2 has fixed divisor 2 -> omega_f(2) == 2 == p
    assert dict(omega_profile([2, 1, 1], 2))[2] == 2


# ---- data layer: factorization_pattern ----
def test_pattern_matches_degree_and_linears():
    # sum(pattern) == deg f whenever f is squarefree mod p, i.e. for every p
    # except those dividing the discriminant (hard-coded: x^2+1 -> 2;
    # x^3+2 -> 2,3; x^2+x+41 -> 163; x^5-x+1 -> 2,19,151).
    skip = {frozenset((1, 0, 1)): {2}, frozenset((2, 0, 0, 1)): {2, 3},
            frozenset((1, -1, 0, 0, 0, 1)): {2, 19}}
    for cs in ([1, 0, 1], [41, 1, 1], [2, 0, 0, 1], [1, -1, 0, 0, 0, 1]):
        for p in (2, 3, 5, 7, 11, 13, 17):
            if cs[-1] % p == 0:
                continue
            pat = factorization_pattern(cs, p)
            assert pat == sorted(pat) and all(d >= 1 for d in pat)
            if p not in skip.get(frozenset(cs), ()):
                assert sum(pat) == len(cs) - 1, (cs, p, pat)


def test_pattern_irreducible_and_split_cases():
    assert factorization_pattern([1, 0, 1], 3) == [2]      # x^2+1 irred mod 3
    assert factorization_pattern([1, 0, 1], 5) == [1, 1]   # splits mod 5
    assert factorization_pattern([1, 3, 2], 7) == [1, 1]   # (2x+1)(x+1)
    assert factorization_pattern([1, 1, 0, 1], 2) == [3]   # x^3+x+1 irred mod 2


def test_pattern_rejects_bad_prime():
    with pytest.raises(ValueError):
        factorization_pattern([1, 0, 2], 2)                # 2x^2+1, p=2 | lc


def test_pattern_non_squarefree_mod_p():
    # x^3+2 = x^3-1 = (x-1)^3 mod 3: the radical collapses it to one linear.
    assert factorization_pattern([2, 0, 0, 1], 3) == [1]
    # (x-1)^2(x^2+1): mod 3 x^2+1 is irreducible, (x-1)^2 -> one linear
    assert factorization_pattern([1, -2, 2, -2, 1], 3) == [1, 2]
    # mod 2: (x+1)^2(x^2+1) = (x+1)^4 -> radical is (x+1)
    assert factorization_pattern([1, -2, 2, -2, 1], 2) == [1]


def test_blind_spot_never_irreducible():
    # x^4+1 (Gal C2xC2) and x^4-10x^2+1 (V4): the single pattern (4,) must
    # never occur -- that is exactly why the certificate fails for them.
    for cs in ([1, 0, 0, 0, 1], [1, 0, -10, 0, 1]):
        mat = pattern_matrix(cs, 200)
        assert len(mat) > 40
        assert all(pat != (4,) for _, pat in mat)
    # sanity: an honestly irreducible polynomial DOES show (2,) somewhere
    assert any(pat == (2,) for _, pat in pattern_matrix([1, 0, 1], 50))


def test_pattern_matrix_skips_leading_coeff_primes():
    mat = pattern_matrix([2, 0, 1], 20)               # x^2+2, lc = 1 -> all p
    assert [p for p, _ in mat][0] == 2
    mat = pattern_matrix([1, 0, 2], 20)               # 2x^2+1, lc = 2 -> no p=2
    assert 2 not in [p for p, _ in mat]


# ---- sympy oracle (optional) ----
def test_factorization_pattern_vs_sympy():
    pytest.importorskip("sympy")
    from sympy import GF, Poly
    from sympy.abc import x as sx

    polys = {
        "x^2+1": [1, 0, 1],
        "x^2+x+41": [41, 1, 1],
        "x^3+2": [2, 0, 0, 1],
        "x^4+1": [1, 0, 0, 0, 1],
        "x^4-10x^2+1": [1, 0, -10, 0, 1],
        "x^5-x+1": [1, -1, 0, 0, 0, 1],
        "x^6+x+1": [1, 1, 0, 0, 0, 0, 1],
        "(x^2+1)(x^3+2)": [2, 0, 2, 1, 0, 1],
        "(x-1)^2(x^2+1)": [1, -2, 2, -2, 1],
        "x(x^2+1)": [0, 1, 0, 1],
    }
    import sympy
    n = 0
    for name, cs in polys.items():
        d = max(i for i, c in enumerate(cs) if c)
        for p in sympy.primerange(2, 60):
            if cs[d] % p == 0:
                continue
            fl = Poly(list(reversed(cs)), sx, domain=GF(p)).factor_list()
            ref = sorted(fac.degree() for fac, _m in fl[1])
            assert factorization_pattern(cs, p) == ref, (name, p)
            n += 1
    assert n > 150


# ---- frame generators ----
def test_euler_frame_stream_shape():
    fr = list(euler_frames([41, 1, 1], n_max=5, hold=3))
    assert len(fr) == 6 + 3
    assert fr[0]["n"] == 0 and fr[5]["n"] == 5
    assert fr[-1].get("hold") is True


def test_bateman_horn_frames_read_arrays():
    E = cumulative_primes([1, 0, 1], 100)
    P = predicted_series([1, 0, 1], 100, C=1.37)
    fr = list(bateman_horn_frames([1, 0, 1], E, P, n_end=100, n_start=10,
                                  frames=9, ease=1.0))
    assert len(fr) == 10
    assert fr[0]["n"] == 10 and fr[-1]["n"] == 100
    assert all(f["E"] is E and f["P"] is P for f in fr)


def test_storyboard_concatenates():
    a = euler_frames([41, 1, 1], n_max=2, hold=0)
    b = euler_frames([41, 1, 1], n_max=1, hold=0)
    kinds = [(f["kind"], f["n"]) for f in storyboard(a, b)]
    assert kinds == [("euler", 0), ("euler", 1), ("euler", 2),
                     ("euler", 0), ("euler", 1)]


def test_draw_frame_rejects_unknown_kind():
    pytest.importorskip("matplotlib")
    with pytest.raises(ValueError):
        draw_frame({"kind": "nonsense", "n": 1, "coeffs": [1]})


# ---- render layer (matplotlib-gated) ----
def test_render_stills(tmp_path):
    pytest.importorskip("matplotlib")
    from pathlib import Path
    fr = list(euler_frames([41, 1, 1], n_max=4, hold=0))
    paths = render_stills(fr, str(tmp_path), every=2)
    assert len(paths) == 3                       # frames 0, 2, 4
    assert all(Path(p).exists() and Path(p).stat().st_size > 1000
               for p in paths)


def test_poster(tmp_path):
    pytest.importorskip("matplotlib")
    out = tmp_path / "poster.png"
    poster(str(out), N=400, pmax=100)
    assert out.exists() and out.stat().st_size > 10000


def test_encode_mp4(tmp_path):
    pytest.importorskip("matplotlib")
    import shutil
    if shutil.which("ffmpeg") is None:
        pytest.skip("ffmpeg not on PATH")
    out = tmp_path / "mini.mp4"
    fr = euler_frames([41, 1, 1], n_max=6, hold=2)
    encode(fr, str(out), fps=10)
    assert out.exists() and out.stat().st_size > 5000


def test_encode_moviepy(tmp_path):
    pytest.importorskip("matplotlib")
    pytest.importorskip("moviepy")
    out = tmp_path / "mini2.mp4"
    fr = euler_frames([41, 1, 1], n_max=5, hold=1)
    encode_moviepy(fr, str(out), fps=5)
    assert out.exists() and out.stat().st_size > 3000


# ---- CLI wiring ----
def test_cli_plot_and_movie(tmp_path, monkeypatch):
    pytest.importorskip("matplotlib")
    from bunyakovsky_demo.demo import cli
    png, mp4 = tmp_path / "p.png", tmp_path / "m.mp4"
    cli(["--N", "500", "--pmax", "200", "--no-report",
         "--plot", str(png), "--movie", str(mp4)])
    assert png.exists() and png.stat().st_size > 10000
    assert mp4.exists() and mp4.stat().st_size > 5000


def test_cli_stills(tmp_path):
    pytest.importorskip("matplotlib")
    from bunyakovsky_demo.demo import cli
    cli(["--N", "200", "--pmax", "100", "--no-report",
         "--stills", str(tmp_path), "--frames", "12"])
    files = sorted(tmp_path.glob("frame_*.png"))
    # full storyboard: euler scene (0..61 + 15 hold) + 13 BH frames
    assert len(files) == 62 + 15 + 13
