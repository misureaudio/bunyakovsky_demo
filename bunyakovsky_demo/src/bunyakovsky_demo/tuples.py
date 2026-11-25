"""Hypothesis H mode: tuples of polynomials (twin primes and beyond).

Schinzel's Hypothesis H (1958) generalizes Bunyakovsky to k-tuples: if
f_1, ..., f_k have positive leading coefficients, are irreducible over Z,
and the product f_1...f_k has no complete set of residues mod p for any
prime p (ADMISSIBILITY), then all f_i(n) are simultaneously prime for
infinitely many n. Quantitative form (Bateman-Horn for tuples):

    #{n <= N : all f_i(n) prime} ~ C * int_2^N dt / (ln f_1(t) ... ln f_k(t))
    C = prod_p (1 - nu_p/p) / (1 - 1/p)^k,

with nu_p = number of distinct residue classes solving the product == 0
mod p. The tuple {x, x+2} IS the twin-prime conjecture, and its C equals
2*C_2 = 1.32032... (the classical twin-prime constant appears inside).

Stdlib only. Public: nu_mod_p, admissible, hypothesis_h_constant,
predicted_tuple_count, tuple_prime_scan, analyze_tuple, render_tuple_md.
"""
from __future__ import annotations

import math

from .analysis import _safe_N, irreducible_z
from .bunyakovsky import (degree, evaluate, format_poly,
                          irreducible_certificate, is_prime, primes_upto)


def nu_mod_p(polys: list[list[int]], p: int) -> int:
    """nu_p: distinct roots mod p of the product (brute force, exact)."""
    reds = [[c % p for c in f] for f in polys]
    return sum(1 for x in range(p)
               if any(evaluate(r, x) % p == 0 for r in reds))


def admissible(polys: list[list[int]]):
    """(is_admissible, witness_p or None).

    Exact decision: nu_p <= sum(deg f_i) < p for every p > sum(deg f_i),
    so checking all primes p <= sum(deg f_i) suffices.
    """
    s = sum(degree(f) for f in polys)
    for p in primes_upto(s):
        if nu_mod_p(polys, p) >= p:
            return False, p
    return True, None


def hypothesis_h_constant(polys: list[list[int]], pmax: int = 10000) -> float:
    """C = prod_p (1 - nu_p/p) / (1 - 1/p)^k, truncated at p <= pmax."""
    k = len(polys)
    c = 1.0
    for p in primes_upto(pmax):
        nu = nu_mod_p(polys, p)
        c *= (1.0 - nu / p) / (1.0 - 1.0 / p) ** k
    return c


def predicted_tuple_count(polys: list[list[int]], N: int,
                          C: float | None = None, pmax: int = 10000,
                          M: int = 20000) -> float:
    """C * int_2^N dt / (ln f_1 ... ln f_k) by trapezoid."""
    if C is None:
        C = hypothesis_h_constant(polys, pmax)
    h = (N - 2) / M
    s = 0.0
    for i in range(M + 1):
        t = 2 + i * h
        lg = 1.0
        ok = True
        for f in polys:
            v = evaluate(f, t)
            if v <= 1:
                ok = False
                break
            lg *= math.log(v)
        y = (1.0 / lg) if ok else 0.0
        s += y if 0 < i < M else 0.5 * y
    return C * s * h


def tuple_prime_scan(polys: list[list[int]], N: int, start: int = 1):
    """All (n, (f_1(n), ..., f_k(n))) with every value prime."""
    out = []
    for n in range(start, N + 1):
        vals = tuple(evaluate(f, n) for f in polys)
        if all(v > 1 and is_prime(v) for v in vals):
            out.append((n, vals))
    return out


def _is_twin(polys: list[list[int]]) -> bool:
    return len(polys) == 2 and sorted(map(list, polys)) == [[0, 1], [2, 1]]


def analyze_tuple(polys: list[list[int]], N: int = 20000,
                  pmax: int = 1000) -> dict:
    """Verdict + data for a Hypothesis H tuple."""
    polys = [list(map(int, f)) for f in polys]
    k = len(polys)
    members = []
    for f in polys:
        cert_ok, cert_p = (irreducible_certificate(f)
                           if degree(f) >= 1 else (False, None))
        dec, facs = irreducible_z(f)
        members.append({
            "coeffs": f, "degree": degree(f), "leading_coeff": f[degree(f)],
            "positive_leading": f[degree(f)] > 0,
            "irreducible": dec, "certificate_prime": cert_p, "factors": facs,
        })
    adm, witness = admissible(polys)
    satisfies = adm and all(m["positive_leading"] and m["irreducible"]
                            and m["degree"] >= 1 for m in members)
    n_max = min(_safe_N(f, N) for f in polys) if k else N
    warnings: list[str] = []
    C = hypothesis_h_constant(polys, pmax) if adm else None
    counts = []
    if adm:
        marks = sorted({m for m in (1000, 10000, n_max) if 3 <= m <= n_max})
        hits = set()
        for n, _ in tuple_prime_scan(polys, n_max):
            hits.add(n)
        for m_ in marks:
            emp = sum(1 for n in hits if n <= m_)
            pred = predicted_tuple_count(polys, m_, C=C)
            counts.append({"N": m_, "empirical": emp, "predicted": pred,
                           "ratio": emp / pred if pred > 1e-9 else None})
    first = tuple_prime_scan(polys, min(n_max, 2000))[:10] if adm else []
    if _is_twin(polys):
        warnings.append("this tuple is {n, n+2}: the TWIN PRIME conjecture "
                        "-- open. Its Bateman-Horn constant equals "
                        "2*C_2 = 1.32032... (the classical twin-prime "
                        "constant). Best proved result nearby: bounded "
                        "gaps (Zhang 2014, Maynard 2015).")
    if not adm:
        if witness == 3 and k == 3:
            warnings.append(
                f"inadmissible: at p = {witness} the entries cover every "
                "residue class, so some f_i(n) is always divisible by "
                f"{witness}; prime tuples can then occur only where some "
                f"f_i(n) = {witness} itself. For the famous "
                "{n, n+2, n+4} pattern this leaves exactly one instance, "
                "(3, 5, 7).")
        else:
            warnings.append(
                f"inadmissible: at p = {witness} the entries cover every "
                "residue class, so for every n some f_i(n) is divisible by "
                f"{witness} -- only tuples with some f_i(n) = {witness} can "
                "be all-prime.")
    warnings.append("all-prime values for infinitely many n is CONJECTURAL "
                    "(Hypothesis H) whenever at least one degree >= 1 "
                    "member is involved; the count column is the "
                    "Bateman-Horn prediction, not a theorem.")
    return {"polys": polys, "members": members, "admissible": adm,
            "witness": witness, "satisfies": satisfies, "C": C,
            "pmax": pmax, "n_max": n_max, "counts": counts, "first": first,
            "twin": _is_twin(polys), "warnings": warnings}


def render_tuple_md(a: dict) -> str:
    import re as _re
    tex_exp = _re.compile(r"\^(\d+)")

    def tex(c):
        return tex_exp.sub(r"^{\1}", format_poly(c))

    L: list[str] = []
    entries = ", ".join(f"${tex(m['coeffs'])}$" for m in a["members"])
    L.append(f"# Hypothesis H: $({entries})$\n")
    if a["twin"]:
        L.append("**This is the twin-prime conjecture.**\n")
    if a["satisfies"]:
        L.append("**Verdict: the tuple satisfies Hypothesis H** "
                 "(each entry irreducible with positive leading "
                 "coefficient, and the tuple is admissible). "
                 "Infinitely many all-prime positions are "
                 "**conjectured**.\n")
    else:
        L.append("**Verdict: Hypothesis H fails** -- see table.\n")
    L.append("| Member | Leading coeff | Irreducible over $\\mathbb{Z}$ | "
             "Evidence |")
    L.append("|:---|---:|:---:|:---|")
    for m in a["members"]:
        if m["certificate_prime"] is not None:
            ev = f"certified mod $p = {m['certificate_prime']}$"
        elif m["irreducible"]:
            ev = "decided (blind spot: no mod-$p$ certificate)"
        else:
            ev = "factors: " + ", ".join(
                f"${tex(g)}$" for g in (m["factors"] or []))
        L.append(f"| ${tex(m['coeffs'])}$ | {m['leading_coeff']} "
                 f"| {'yes' if m['irreducible'] else 'no'} | {ev} |")
    adm = ("yes" if a["admissible"]
           else f"no -- witness $p = {a['witness']}$")
    L.append(f"\n**Admissible** (no prime $p$ with $\\nu_p = p$)? {adm}. "
             "Checked exactly: it suffices to test $p \\le "
             "\\sum_i \\deg f_i$.\n")
    if a["C"] is not None:
        L.append(f"Bateman-Horn constant $C = {a['C']:.5f}$ "
                 f"($p \\le {a['pmax']}$).\n")
        L.append("| $N$ | empirical | predicted | ratio |")
        L.append("|------:|--------:|----------:|------:|")
        for c in a["counts"]:
            pred = f"{c['predicted']:.1f}" if c["predicted"] is not None \
                else "—"
            rat = f"{c['ratio']:.4f}" if c["ratio"] is not None else "—"
            L.append(f"| {c['N']} | {c['empirical']} | {pred} | {rat} |")
    if a["first"]:
        L.append("\nFirst all-prime positions:\n")
        for n, vals in a["first"][:8]:
            vs = ", ".join(f"${v}$" for v in vals)
            L.append(f"- $n = {n}$: {vs}")
    if a["warnings"]:
        L.append("\n## Notes\n")
        for w in a["warnings"]:
            L.append(f"- {w}")
    L.append("")
    return "\n".join(L)
