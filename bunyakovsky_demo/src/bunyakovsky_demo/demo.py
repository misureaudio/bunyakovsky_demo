"""Runnable report: Bunyakovsky's conjecture, hypotheses, and heuristics.

The report is Markdown (GitHub pipe tables + $\\LaTeX$ math), designed to be
redirected and converted to PDF:

    bunyakovsky-demo > report.md
    pandoc report.md -o report.pdf

Graphics progress messages go to stderr, so stdout stays a clean document.

Usage (from the workspace root):
    .venv/Scripts/python.exe -m bunyakovsky_demo.demo [--N 20000] [--pmax 10000]
"""
from __future__ import annotations

import argparse
import re
import sys

from .bunyakovsky import (bunyakovsky_constant, check_hypotheses, evaluate,
                          fixed_divisor, format_poly, is_prime,
                          predicted_count, scan_primes)

SATISFYING = [
    ([2, 3], "linear case: Dirichlet's theorem (PROVED, 1837)"),
    ([1, 0, 1], "Landau problem #1 (OPEN since 1912)"),
    ([41, 1, 1], "Euler's polynomial: 40 consecutive primes"),
    ([1, 1, 0, 1], "cubic case"),
    ([2, 0, 0, 1], "Eisenstein at $p=2$ -- irreducibility provable by hand"),
    ([1, 1, 1, 1, 1], "cyclotomic $\\Phi_5$: prime divisors $q = 5$ or "
                      "$q \\equiv 1 \\pmod{5}$, see section 5"),
    ([1, -1, 0, 0, 0, 1], "densest of the demo set: $C = 4.90$, see section 7"),
]
VIOLATING = [
    ([2, 1, 1], "hypothesis 3 fails: every value is even"),
    ([1, 3, 2], "hypothesis 2 fails: $(2x+1)(x+1)$, composite for $n \\ge 2$"),
    ([1, 5, -1], "hypothesis 1 fails: negative leading coefficient"),
    ([2, 3, 0, 1], "hypothesis 3 at degree 3: irreducible (certified $p=5$) "
                   "yet $x^3+3x+2$ is always even"),
]
BLIND_SPOTS = [
    ([1, 0, 0, 0, 1], "Galois group $C_2 \\times C_2$: Frobenius orders "
                      "$\\le 2$, so it factors mod every $p$"),
    ([1, 0, -10, 0, 1], "the classic $V_4$ example: irreducible over "
                        "$\\mathbb{Z}$, reducible mod every $p$"),
]
CONTRAST = [
    ([41, -1, 1, 1], "x^3 + x^2 - x + 41"),
    ([1, -1, 0, 0, 0, 1], "x^5 - x + 1"),
]
PHI5 = [1, 1, 1, 1, 1]

_TEX_EXP = re.compile(r"\^(\d+)")


def _tex(coeffs: list[int]) -> str:
    """LaTeX form for the Markdown tables: format_poly with braced exponents,
    e.g. [1, 0, 1] -> 'x^{2} + 1' (safe for exponents of any width)."""
    return _TEX_EXP.sub(r"^{\1}", format_poly(coeffs))


def _factor_small(m: int) -> dict[int, int]:
    """Prime factorization by trial division (small demo values only)."""
    f: dict[int, int] = {}
    d = 2
    while d * d <= m:
        while m % d == 0:
            f[d] = f.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        f[m] = f.get(m, 0) + 1
    return f


def main(N: int, pmax: int) -> None:
    print("# Bunyakovsky's Conjecture (1857)\n")
    print("If $f \\in \\mathbb{Z}[x]$ has positive leading coefficient, is "
          "irreducible over $\\mathbb{Z}$, and no prime divides all of its "
          "values $f(1), f(2), \\dots$, then $f(n)$ is prime for infinitely "
          "many $n$.\n")
    print("The linear case is **Dirichlet's theorem** (proved, 1837); every "
          "case of degree $\\ge 2$ is **open** -- $x^2 + 1$ is Landau's "
          "problem #1 (1912). The quantitative companion used here is "
          "**Bateman-Horn** (Hardy-Littlewood Conjecture F).\n")

    print("## 1. Hypotheses table\n")
    print("Fixed divisor from the theorem "
          "$\\gcd(\\text{all values}) = \\gcd\\big(f(0), \\dots, "
          "f(\\deg f)\\big)$; irreducibility certified mod some prime $p$ "
          "(one-way: `none` means *not certified*, not *reducible* -- see "
          "section 6).\n")
    print("| $f(x)$ | deg | fixed divisor | irr. certificate | satisfies |")
    print("|:------------------------|----:|----:|:----:|:----:|")
    for cs, _ in SATISFYING + VIOLATING:
        h = check_hypotheses(cs)
        cert = (f"$p = {h['certificate_prime']}$"
                if h["irreducible_certified"] else "none")
        print(f"| ${_tex(cs)}$ | {h['degree']} | {h['fixed_divisor']} "
              f"| {cert} | {'yes' if h['satisfies'] else 'no'} |")
    print()
    for cs, note in VIOLATING:
        print(f"- **Hypothesis violation** -- ${_tex(cs)}$: {note}")
    print()

    print("## 2. Euler spotlight: $x^2 + x + 41$\n")
    first_bad = next(n for n in range(0, 100)
                     if evaluate([41, 1, 1], n) <= 1
                     or not is_prime(evaluate([41, 1, 1], n)))
    print(f"Prime values for every $n = 0, \\dots, {first_bad - 1}$ "
          f"({first_bad} in a row), then "
          f"$f({first_bad}) = {evaluate([41, 1, 1], first_bad)} = 41^2$.\n")
    print("The hypotheses still hold, so the conjecture claims infinitely "
          "many primes anyway -- true primes resume at $n = 42$.\n")

    print("## 3. Heuristic check: empirical vs. Bateman-Horn\n")
    print(f"Predicted count $C(f) \\int_2^N dt / \\ln f(t)$, with $C(f)$ "
          f"truncated at $p \\le {pmax}$.\n")
    print("| $f(x)$ | $N$ | $C(f)$ | empirical | predicted | ratio |")
    print("|:------------------------|-------:|-------:|--------:|--------:|"
          "------:|")
    for cs in ([1, 0, 1], [41, 1, 1], [2, 0, 0, 1], PHI5,
               [1, -1, 0, 0, 0, 1]):
        C = bunyakovsky_constant(cs, pmax=pmax)
        for nmax in sorted({1000, 10000, min(N, 100000)}):
            emp = len(scan_primes(cs, nmax))
            pred = predicted_count(cs, nmax, C=C)
            print(f"| ${_tex(cs)}$ | {nmax} | {C:.4f} | {emp} | {pred:.1f} "
                  f"| {emp / pred:.4f} |")
    print()
    print("The ratios drift toward $1.00$ as $N$ grows (measured reference: "
          "$1.0083$ for $x^2+1$ at $N = 10^5$).\n")

    print("## 4. Why the hypotheses matter\n")
    print(f"- ${_tex([2, 1, 1])}$: fixed divisor {fixed_divisor([2, 1, 1])} "
          "-- every value is even, and the single even prime $2$ is never "
          "hit for $n \\ge 1$.")
    print("- $2x^2+3x+1 = (2x+1)(x+1)$: fixed divisor $1$, yet composite "
          "for every $n \\ge 2$ -- irreducibility is essential.")
    print("- Linear cases are Dirichlet's theorem; every degree "
          "$\\ge 2$ case remains open.\n")

    print("## 5. Cyclotomic structure: "
          "$\\Phi_5(n) = n^4 + n^3 + n^2 + n + 1$\n")
    print("Every prime divisor $q$ of $\\Phi_5(n)$ satisfies $q = 5$ or "
          "$q \\equiv 1 \\pmod{5}$. Checked on $n = 2..40$:\n")
    facs: dict[int, int] = {}
    for n in range(2, 41):
        for q, e in _factor_small(evaluate(PHI5, n)).items():
            facs[q] = facs.get(q, 0) + e
    bad = [q for q in facs if q != 5 and q % 5 != 1]
    print(f"- {sum(facs.values())} prime factors (with multiplicity): "
          f"{facs.get(5, 0)} equal $5$, all the rest are "
          f"$q \\equiv 1 \\pmod{5}$; exceptions: {len(bad)}.")
    print("- Reason: $q \\mid \\Phi_5(n)$ and $q \\ne 5$ give "
          "$\\operatorname{ord}_q(n) = 5$, hence $5 \\mid q - 1$.\n")

    print("## 6. Certificate blind spots\n")
    print("Believed to satisfy the hypotheses, yet $f \\bmod p$ is reducible "
          "for **every** prime $p$, so the mod-$p$ certificate can never "
          "prove irreducibility (reported `satisfies: no`):\n")
    print("| $f(x)$ | fixed divisor | certified | primes ($n \\le 10^4$) |"
          " why |")
    print("|:-----------------|----:|:----:|-----:|:------------------------"
          "--|")
    for cs, note in BLIND_SPOTS:
        h = check_hypotheses(cs)
        cnt = len(scan_primes(cs, 10000))
        print(f"| ${_tex(cs)}$ | {h['fixed_divisor']} | no | {cnt} | {note} |")
    print()

    print("## 7. What $C(f)$ means\n")
    print("Both polynomials satisfy the hypotheses; $C$ computed at "
          "$p_{max} = 3000$:\n")
    print("| $f(x)$ | $C(f)$ | primes ($n \\le 10^4$) |")
    print("|:-----------------|-------:|-----:|")
    for cs, name in CONTRAST:
        C = bunyakovsky_constant(cs, pmax=3000)
        cnt = len(scan_primes(cs, 10000))
        print(f"| ${_tex(cs)}$ | {C:.4f} | {cnt} |")
    print()
    print("Same conjecture, an $11\\times$ density difference -- and both "
          "counts match $C(f) \\int_2^n dt/\\ln f(t)$ within a few percent. "
          "$C(f)$ is the arithmetic *luck* of the polynomial: local "
          "obstructions at small primes make $\\omega_f(p)$ larger (unlucky) "
          "or smaller (lucky).\n")


def cli(argv=None) -> None:
    """Console-script / `python -m` entry point."""
    ap = argparse.ArgumentParser(
        prog="bunyakovsky-demo",
        description="Bunyakovsky conjecture demo: hypotheses, prime scans, "
                    "Bateman-Horn heuristic. The report is Markdown "
                    "(redirect it, e.g. bunyakovsky-demo > report.md; "
                    "pandoc report.md -o report.pdf). Optional graphics "
                    "(--plot, --movie, --stills; needs "
                    "bunyakovsky_demo[viz]).")
    ap.add_argument("--N", type=int, default=20000, help="scan bound")
    ap.add_argument("--pmax", type=int, default=10000, help="constant truncation")
    ap.add_argument("--plot", metavar="PNG", help="render the 2x2 poster PNG")
    ap.add_argument("--movie", metavar="MP4", help="render the 2-scene movie")
    ap.add_argument("--stills", metavar="DIR",
                    help="render movie frames as PNGs (no encoder needed)")
    ap.add_argument("--frames", type=int, default=260,
                    help="Bateman-Horn scene frame count")
    ap.add_argument("--no-report", action="store_true",
                    help="skip the console report (graphics only)")
    ap.add_argument("--poly", metavar="EXPR", action="append",
                    help='teacher mode: analyze a polynomial, e.g. '
                         '--poly "x^2 + x + 41" (Markdown analysis card; '
                         'replaces the standard report; repeatable)')
    ap.add_argument("--tuple", metavar="F1,F2,...", action="append",
                    help='Hypothesis H mode: analyze a tuple of '
                         'polynomials, e.g. --tuple "x, x+2" for twin '
                         'primes (replaces the report; repeatable)')
    ap.add_argument("--census", action="store_true",
                    help='landscape census of all small polynomials '
                         '(replaces the report); cost grows like '
                         'height^(degree+1)')
    ap.add_argument("--degree", type=int, default=3,
                    help='census: maximum degree (default 3)')
    ap.add_argument("--height", type=int, default=2,
                    help="census: maximum |coefficient| (default 2)")
    ap.add_argument("--gui", action="store_true",
                    help="open the tkinter GUI instead (bunyakovsky-gui)")
    args = ap.parse_args(argv)

    if args.gui:
        from .gui import main as gui_main
        gui_main()
        return
    if args.poly and args.tuple:
        print("error: use --poly or --tuple, not both", file=sys.stderr)
        raise SystemExit(2)
    if args.poly or args.tuple or args.census:
        args.no_report = True

    if args.poly:
        from .analysis import analyze, parse_poly, render_analysis_md
        for expr in args.poly:
            try:
                cs = parse_poly(expr)
            except ValueError as e:
                print(f"error: {e}", file=sys.stderr)
                raise SystemExit(2)
            print(render_analysis_md(analyze(cs, N=args.N, pmax=args.pmax)))
    elif args.tuple:
        from .analysis import parse_poly
        from .tuples import analyze_tuple, render_tuple_md
        for expr in args.tuple:
            try:
                polys = [parse_poly(part) for part in expr.split(",")]
            except ValueError as e:
                print(f"error: {e}", file=sys.stderr)
                raise SystemExit(2)
            print(render_tuple_md(analyze_tuple(polys, N=args.N)))
    elif args.census:
        from .census import render_census_md, run_census
        try:
            res = run_census(D=args.degree, B=args.height)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            raise SystemExit(2)
        print(render_census_md(res))
    elif not args.no_report:
        main(args.N, args.pmax)

    if args.plot or args.movie or args.stills:
        from .viz import (bateman_horn_frames, cumulative_primes, encode,
                          euler_frames, poster, predicted_series,
                          render_stills, storyboard)
        if args.plot:
            print(f"rendering poster -> {args.plot}", file=sys.stderr)
            poster(args.plot, N=min(args.N, 20000))
        if args.movie or args.stills:
            bh = [1, 0, 1]
            n_bh = min(args.N, 20000)
            print(f"precomputing x^2+1 scan to N={n_bh} ...", file=sys.stderr)
            E = cumulative_primes(bh, n_bh)
            P = predicted_series(bh, n_bh, pmax=args.pmax)
            scenes = storyboard(euler_frames([41, 1, 1]),
                                bateman_horn_frames(bh, E, P, n_end=n_bh,
                                                    frames=args.frames))
            if args.stills:
                paths = render_stills(scenes, args.stills)
                print(f"rendered {len(paths)} PNG frames -> {args.stills}",
                      file=sys.stderr)
            if args.movie:
                encode(scenes, args.movie)
                print(f"rendered movie -> {args.movie}", file=sys.stderr)


if __name__ == "__main__":
    cli()
