"""Landscape census: classify every small-coefficient polynomial.

Enumerates the primitive polynomials of degree 1..D with positive leading
coefficient and all coefficients |a_i| <= B, classifies each against
Bunyakovsky's conjecture using the DECIDABLE irreducibility test, and
selects archetypes: luckiest / unluckiest Bateman-Horn constants, longest
prime runs, hypothesis violators, and BLIND SPOTS -- polynomials
irreducible over Z yet reducible mod p for every prime tested (the
certificate's blind spots, found empirically rather than hand-picked).

A theorem makes the blind-spot hunt structural: irreducible => Gal(f)
transitive => n divides |Gal| => (Cauchy) Gal contains an n-cycle when n
is prime => blind spots are impossible at prime degree. The census can
verify exactly that on its own data (zero blind spots at degree 2 or 3,
hits at degree 4).

Public: run_census, render_census_md.
"""
from __future__ import annotations

import itertools
import math

from .analysis import irreducible_z
from .bunyakovsky import (bunyakovsky_constant, degree, evaluate,
                          fixed_divisor, format_poly, irreducible_certificate,
                          is_prime, primes_upto)


def enumerate_polys(D: int, B: int):
    """Primitive polys, degrees 1..D, positive leading coeff, |a_i| <= B.
    Deterministic order: by degree, then leading coeff, then coeffs
    low-to-high lexicographic."""
    for d in range(1, D + 1):
        for lead in range(1, B + 1):
            for rest in itertools.product(range(-B, B + 1), repeat=d):
                coeffs = list(rest) + [lead]          # low-to-high
                g = 0
                for c in coeffs:
                    g = math.gcd(g, c)
                if g == 1:
                    yield coeffs


def _scan_stats(coeffs: list[int], scan_N: int):
    n_primes, best_len, best_start, cur = 0, 0, 0, 0
    for n in range(1, scan_N + 1):
        v = evaluate(coeffs, n)
        if v > 1 and is_prime(v):
            n_primes += 1
            cur += 1
            if cur > best_len:
                best_len, best_start = cur, n - cur + 1
        else:
            cur = 0
    return n_primes, best_start, best_len


def _blind_check(coeffs: list[int], blind_pmax: int):
    """Confirm a blind spot with the mod-p factorization pattern:
    returns (confirmed, p_where_irreducible_or_None). pattern == [d]
    means f is irreducible mod p, i.e. a certificate EXISTS at p."""
    from .viz import factorization_pattern
    d = degree(coeffs)
    for p in primes_upto(blind_pmax):
        if coeffs[d] % p == 0:
            continue
        if factorization_pattern(coeffs, p) == [d]:
            return False, p
    return True, None


def run_census(D: int = 3, B: int = 2, scan_N: int = 300, pmax_C: int = 200,
               blind_pmax: int = 200, limit: int = 20000) -> dict:
    """Classify all primitive polynomials in the box; return rows, stats,
    archetypes. Cost grows like B^(D+1): defaults are seconds,
    (D=4, B=3) is a ~1-2 minute run."""
    polys = list(enumerate_polys(D, B))
    if len(polys) > limit:
        raise ValueError(
            f"census would classify {len(polys)} polynomials "
            f"(limit {limit}); lower --height or --degree")
    rows = []
    for coeffs in polys:
        d = degree(coeffs)
        fd = fixed_divisor(coeffs)
        dec, _facs = irreducible_z(coeffs)
        cert_ok, cert_p = (irreducible_certificate(coeffs) if dec
                           else (False, None))
        satisfies = fd == 1 and dec
        n_primes, run_start, run_len = _scan_stats(coeffs, scan_N)
        blind_cand = satisfies and not cert_ok
        blind_ok, late_p = _blind_check(coeffs, blind_pmax) \
            if blind_cand else (False, None)
        C = (bunyakovsky_constant(coeffs, pmax_C)
             if satisfies and fd == 1 else None)
        rows.append({
            "coeffs": coeffs, "degree": d, "fixed_divisor": fd,
            "irreducible": dec, "certified": cert_ok,
            "certificate_prime": cert_p, "satisfies": satisfies,
            "blind_spot": blind_ok, "late_certificate_p": late_p,
            "n_primes": n_primes, "run_start": run_start, "run_len": run_len,
            "C": C,
        })
    # missed blind spots with a certificate above the search cap:
    # blind_cand but late_p found -> not blind, just uncatalogued cert
    stats = {
        "total": len(rows),
        "satisfies": sum(r["satisfies"] for r in rows),
        "fd_violation": sum(r["fixed_divisor"] > 1 for r in rows),
        "reducible": sum(not r["irreducible"] for r in rows),
        "blind": sum(r["blind_spot"] for r in rows),
    }
    by_degree = {}
    for d in range(1, D + 1):
        sub = [r for r in rows if r["degree"] == d]
        by_degree[d] = {"total": len(sub),
                        "satisfies": sum(r["satisfies"] for r in sub),
                        "blind": sum(r["blind_spot"] for r in sub)}
    sat = [r for r in rows if r["satisfies"] and r["C"] is not None]
    arch = {
        "luckiest": sorted(sat, key=lambda r: -r["C"])[:3],
        "unluckiest": sorted(sat, key=lambda r: r["C"])[:3],
        "runs": sorted((r for r in rows if r["run_len"] > 0),
                       key=lambda r: (-r["run_len"], r["coeffs"]))[:3],
        "blind": [r for r in rows if r["blind_spot"]],
        "fd_examples": [r for r in rows if r["fixed_divisor"] > 1][:5],
    }
    return {"rows": rows, "stats": stats, "by_degree": by_degree,
            "archetypes": arch,
            "params": {"D": D, "B": B, "scan_N": scan_N, "pmax_C": pmax_C,
                       "blind_pmax": blind_pmax}}


def render_census_md(res: dict) -> str:
    import re as _re
    tex_exp = _re.compile(r"\^(\d+)")

    def tex(c):
        return tex_exp.sub(r"^{\1}", format_poly(c))

    p = res["params"]
    s = res["stats"]
    L: list[str] = []
    L.append(f"# Census of small polynomials "
             f"(degree $\\le {p['D']}$, height $\\le {p['B']}$)\n")
    L.append(f"**{s['total']} primitive polynomials** classified against "
             "Bunyakovsky's conjecture with the DECIDABLE irreducibility "
             "test (Zassenhaus). Categories overlap: a polynomial can fail "
             "both 2 and 3.\n")
    L.append("| class | count | share |")
    L.append("|:---|---:|---:|")
    L.append(f"| satisfies all three hypotheses | {s['satisfies']} "
             f"| {s['satisfies'] / s['total']:.1%} |")
    L.append(f"| fails 2: reducible over $\\mathbb{{Z}}$ | {s['reducible']} "
             f"| {s['reducible'] / s['total']:.1%} |")
    L.append(f"| fails 3: fixed divisor $> 1$ | {s['fd_violation']} "
             f"| {s['fd_violation'] / s['total']:.1%} |")
    L.append(f"| blind spots (satisfy, yet no mod-$p$ certificate for "
             f"$p \\le {p['blind_pmax']}$) | {s['blind']} "
             f"| {s['blind'] / s['total']:.1%} |")
    L.append("\n## By degree\n")
    L.append("| degree | total | satisfies | blind spots |")
    L.append("|---:|---:|---:|---:|")
    for d, st in res["by_degree"].items():
        L.append(f"| {d} | {st['total']} | {st['satisfies']} "
                 f"| {st['blind']} |")
    L.append("\n## Archetypes\n")
    for key, title in (("luckiest", "Luckiest — highest $C(f)$"),
                       ("unluckiest", "Unluckiest — lowest $C(f)$")):
        L.append(f"**{title}** (among satisfying, $C$ truncated at "
                 f"$p \\le {p['pmax_C']}$):\n")
        L.append("| $f(x)$ | $C(f)$ | primes ($n \\le "
                 f"{p['scan_N']}$) |")
        L.append("|:---|---:|---:|")
        for r in res["archetypes"][key]:
            L.append(f"| ${tex(r['coeffs'])}$ | {r['C']:.4f} "
                     f"| {r['n_primes']} |")
        L.append("")
    L.append("**Longest runs of consecutive prime values**:\n")
    L.append("| $f(x)$ | run | where |")
    L.append("|:---|---:|:---|")
    for r in res["archetypes"]["runs"]:
        L.append(f"| ${tex(r['coeffs'])}$ | {r['run_len']} "
                 f"| $n = {r['run_start']}, \\dots, "
                 f"{r['run_start'] + r['run_len'] - 1}$ |")
    L.append("")
    if res["archetypes"]["blind"]:
        L.append("**Blind spots found** (irreducible over $\\mathbb{Z}$, "
                 "yet the factorization pattern mod $p$ is never the "
                 "single pattern $(d)$ for any prime $p \\le "
                 f"{p['blind_pmax']}$ — no certificate can exist, the "
                 "Galois group has no full cycle):\n")
        L.append("| $f(x)$ | degree | primes ($n \\le "
                 f"{p['scan_N']}$) |")
        L.append("|:---|---:|---:|")
        for r in res["archetypes"]["blind"]:
            L.append(f"| ${tex(r['coeffs'])}$ | {r['degree']} "
                     f"| {r['n_primes']} |")
    if res["archetypes"]["fd_examples"]:
        L.append("\n**Fixed-divisor violators** (sample): " + ", ".join(
            f"${tex(r['coeffs'])}$ (${r['fixed_divisor']}$)"
            for r in res["archetypes"]["fd_examples"]) + ".")
    L.append("\n## Notes\n")
    L.append("- $C(f)$ is truncated at small $p_{max}$ for speed: use the "
             "values for *ranking*, not as published constants.")
    L.append("- Degree 1 with $\\gcd = 1$ always satisfies (Dirichlet: "
             "proved); degrees $\\ge 2$ satisfy = conjecture.")
    L.append("- Blind spots are possible only at COMPOSITE degree "
             "(Cauchy: a transitive Galois group of prime degree contains "
             "an $n$-cycle, which is exactly a certificate). The "
             "by-degree table should show 0 at degrees 2 and 3.")
    L.append("")
    return "\n".join(L)
