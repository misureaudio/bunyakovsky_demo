"""Teacher mode (v1.4.0): parse a human-entered polynomial, DECIDE the three
Bunyakovsky hypotheses over Z, and render a Markdown analysis card.

Unlike the one-way mod-p certificate in bunyakovsky.py, irreducibility here
is fully decidable (Zassenhaus-style: factor mod a large squarefree prime
above the Landau-Mignotte bound, subset products + exact division over Z,
with a Yun-style repeated-factor peel over Q). Stdlib only; nothing here
imports matplotlib.

Public API: parse_poly, irreducible_z, analyze, render_analysis_md.
"""
from __future__ import annotations

import math
import re
from fractions import Fraction

from .bunyakovsky import (bunyakovsky_constant, degree, evaluate,
                          fixed_divisor, irreducible_certificate, is_prime,
                          predicted_count, roots_mod_p)

#: deterministic Miller-Rabin range for bases 2..37 (see bunyakovsky.py)
MR_LIMIT = 3317044064679887385961981

_TEX_EXP = re.compile(r"\^(\d+)")


# --------------------------------------------------------------------------
# Human input: parse, never eval
# --------------------------------------------------------------------------
_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def parse_poly(s: str) -> list[int]:
    """Parse a teacher-supplied polynomial into low-to-high integer coeffs.

    Accepts "x^2 + x + 41", "x**3 - x + 1", "-3x^3 + 2x - 1", "x² + 1",
    "5 - x^2", any single-letter variable, implicit coefficients and '*'
    signs, and a bare low-to-high coefficient list ("1 0 1" / "1, 0, 1").
    Raises ValueError otherwise. Never uses eval().
    """
    s = s.strip()
    s = re.sub("[\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078"
               "\u2079]+",
               lambda m: "^" + m.group().translate(_SUP), s)
    s = s.replace("**", "^").replace("*", "")
    s = s.replace("\u2212", "-")
    if not s:
        raise ValueError("empty polynomial")
    parts = re.split(r"[,\s]+", s)
    if len(parts) > 1 and all(re.fullmatch(r"[+-]?\d+", t) for t in parts):
        coeffs = [int(t) for t in parts]
        while len(coeffs) > 1 and coeffs[-1] == 0:
            coeffs.pop()
        return coeffs
    s = "".join(s.split())                       # expression path: no spaces
    var = None
    for ch in s:
        if ch.isalpha():
            if var is None:
                var = ch
            elif ch != var:
                raise ValueError(
                    f"multiple variables ({var!r} and {ch!r}) in {s!r}")
    if var is None:
        if not re.fullmatch(r"[+-]?\d+", s):
            raise ValueError(f"cannot parse {s!r} (not a polynomial)")
        return [int(s)]
    terms = re.findall(r"[+-]?[^+-]+", s)
    if "".join(terms) != s:
        raise ValueError(f"cannot parse {s!r}")
    coeffs = [0]
    for t in terms:
        sign = -1 if t[0] == "-" else 1
        body = t.lstrip("+-")
        if not body:
            raise ValueError(f"cannot parse term {t!r} in {s!r}")
        if re.fullmatch(r"\d+", body):                    # constant term
            coef, deg = int(body), 0
        else:
            m = re.fullmatch(r"(\d+)?" + re.escape(var) + r"(?:\^(\d+))?",
                             body)
            if not m:
                raise ValueError(f"cannot parse term {t!r} in {s!r}")
            coef = int(m.group(1)) if m.group(1) else 1
            deg = int(m.group(2)) if m.group(2) else 1
        if deg > 64:
            raise ValueError(f"degree {deg} too large (max 64)")
        if len(coeffs) <= deg:
            coeffs += [0] * (deg + 1 - len(coeffs))
        coeffs[deg] += sign * coef
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
    return coeffs


# --------------------------------------------------------------------------
# Integer / rational / F_p polynomial helpers (module-private)
# --------------------------------------------------------------------------
def _trim_i(a: list[int]) -> list[int]:
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _content(a: list[int]) -> int:
    g = 0
    for c in a:
        g = math.gcd(g, c)
    return g or 1


def _deriv_z(a: list[int]) -> list[int]:
    return _trim_i([i * c for i, c in enumerate(a)][1:] or [0])


def _z_mul(a: list[int], b: list[int]) -> list[int]:
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] += ai * bj
    return _trim_i(r)


def _z_divmod(f: list[int], g: list[int]):
    """Exact quotient over Z if g | f, else None (schoolbook long division)."""
    f, g = _trim_i(list(f)), _trim_i(list(g))
    if g == [0]:
        raise ZeroDivisionError
    if len(f) < len(g):
        return None
    r, q = f[:], [0] * (len(f) - len(g) + 1)
    for k in range(len(q) - 1, -1, -1):
        top = r[k + len(g) - 1]
        if top % g[-1]:
            return None
        c = top // g[-1]
        q[k] = c
        for j in range(len(g)):
            r[k + j] -= c * g[j]
    return _trim_i(q) if _trim_i(r) == [0] else None


def _prime_factors(m: int) -> list[int]:
    m = abs(m)
    out: list[int] = []
    d = 2
    while d * d <= m:
        while m % d == 0:
            out.append(d)
            m //= d
        d += 1
    if m > 1:
        out.append(m)
    return out


def _tq(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _mod_q(f, g):
    f = [Fraction(c) for c in f]
    g = _tq([Fraction(c) for c in g])
    binv = 1 / g[-1]
    while len(f) >= len(g):
        s = len(f) - len(g)
        q = f[-1] * binv
        for j in range(len(g)):
            f[s + j] -= q * g[j]
        f.pop()
        if not f:
            return [Fraction(0)]
    return _tq(f)


def _gcd_q(f, g):
    """Monic gcd over Q."""
    f, g = _tq([Fraction(c) for c in f]), _tq([Fraction(c) for c in g])
    while g != [Fraction(0)]:
        f, g = g, _mod_q(f, g)
    inv = 1 / f[-1]
    return _tq([c * inv for c in f])


def _clear_denoms(hq) -> list[int]:
    """Integer primitive positive-lc version of a Q-polynomial (a monic
    divisor of an integer polynomial has integer coefficients anyway)."""
    lcm = 1
    for c in hq:
        lcm = lcm * c.denominator // math.gcd(lcm, c.denominator)
    out = _trim_i([int(c * lcm) for c in hq])
    if out[-1] < 0:
        out = [-c for c in out]
    c = _content(out)
    return [x // c for x in out]


def _t(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _pmod(a, b, p):
    a = [x % p for x in a]
    b = _t([x % p for x in b])
    binv = pow(b[-1], -1, p)
    while len(a) >= len(b):
        s = len(a) - len(b)
        q = a[-1] * binv % p
        for j in range(len(b)):
            a[s + j] = (a[s + j] - q * b[j]) % p
        a.pop()
        if not a:
            return [0]
    return _t(a)


def _pgcd(a, b, p):
    a, b = _t([x % p for x in a]), _t([x % p for x in b])
    while b != [0]:
        a, b = b, _pmod(a, b, p)
    inv = pow(a[-1], -1, p)
    return _t([(c * inv) % p for c in a])


def _pmul(a, b, m, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return _pmod(r, m, p)


def _ppow(base, e, m, p):
    r, b = [1], _pmod(base, m, p)
    while e:
        if e & 1:
            r = _pmul(r, b, m, p)
        b = _pmul(b, b, m, p)
        e >>= 1
    return r


def _pdiv(a, b, p):
    """Exact quotient over F_p (b | a assumed)."""
    a, b = _t([x % p for x in a]), _t([x % p for x in b])
    q = [0] * (len(a) - len(b) + 1)
    r = list(a)
    binv = pow(b[-1], -1, p)
    for k in range(len(q) - 1, -1, -1):
        coef = r[k + len(b) - 1] * binv % p
        q[k] = coef
        for j in range(len(b)):
            r[k + j] = (r[k + j] - coef * b[j]) % p
    return _t(q)


def _pedf(g, k, p) -> list[list[int]]:
    """Cantor-Bach equal-degree split: irreducible factors of squarefree g,
    all of degree k (deterministic scan; p == 2 uses the trace variant)."""
    if k == 1:
        fs = []
        for a in range(p):
            lin = [(-a) % p, 1]
            if _pmod(g, lin, p) == [0]:
                fs.append(lin)
        return fs
    if len(g) - 1 == k:
        return [g]
    e = (p ** k - 1) // 2
    b = 1
    while True:
        for c in range(p):
            a = [c, b]
            if p > 2:
                h = _ppow(a, e, g, p)
                h = list(h) + [0] * (1 - len(h))
                h[0] = (h[0] - 1) % p
            else:
                h, ap = list(a), list(a)
                for _ in range(k - 1):
                    ap = _ppow(ap, 2, g, 2)
                    m = max(len(h), len(ap))
                    h = [(h[i] if i < len(h) else 0)
                         + (ap[i] if i < len(ap) else 0) for i in range(m)]
            dd = _pgcd(g, _t([x % p for x in h]), p)
            if [1] != dd != g:
                return _pedf(dd, k, p) + _pedf(_pdiv(g, dd, p), k, p)
        b += 1


def _mod_factors(f: list[int], p: int) -> list[list[int]]:
    """Irreducible factors of squarefree f over F_p (monic)."""
    g = [c % p for c in f]
    inv = pow(g[-1], -1, p)
    g = _t([c * inv % p for c in g])
    out: list[list[int]] = []
    rem, xpow = g, [0, 1]
    k = 1
    while len(rem) - 1 >= 2 * k:
        xpow = _ppow(xpow, p, g, p)
        h = list(xpow) + [0] * (2 - len(xpow))
        h[1] = (h[1] - 1) % p
        gg = _pgcd(rem, _t(h), p)
        if gg != [1]:
            out += _pedf(gg, k, p)
            rem = _pdiv(rem, gg, p)
        k += 1
    if len(rem) - 1 > 0:
        out += _pedf(rem, len(rem) - 1, p)
    return out


def _good_prime(f: list[int], d: int) -> int:
    """Prime p > 2 * Landau-Mignotte bound, p not | lc, f squarefree mod p."""
    norm2 = math.isqrt(sum(c * c for c in f)) + 1
    target = max(5, (1 << (d // 2 + 1)) * norm2 + 5)
    p, tried = target | 1, 0
    while tried < 20000:
        if is_prime(p) and f[d] % p:
            fp = _t([i * c % p for i, c in enumerate(f)][1:] or [0])
            if _pgcd([c % p for c in f], fp, p) == [1]:
                return p
        p += 2
        tried += 1
    raise ValueError("input too wild for teacher mode (no good prime found)")


# --------------------------------------------------------------------------
# Decidable irreducibility / factorization over Z
# --------------------------------------------------------------------------
def _split_z(g: list[int], gmods: list[list[int]], p: int) -> list[list[int]]:
    """Zassenhaus subset test: lift products of mod-p factor subsets, scaled
    by every positive divisor of lc(g) (Z-factors need not be monic), using
    the unique centered lift (p exceeds twice the coefficient bound), and
    test exact divisibility in Z[x]."""
    if len(gmods) == 1:
        return [g]
    lc = g[-1]
    scalars = [s for s in range(1, abs(lc) + 1) if lc % s == 0]
    rest = gmods[1:]
    for mask in range(1 << len(rest)):
        sel = [gmods[0]] + [r for i, r in enumerate(rest) if (mask >> i) & 1]
        if len(sel) == len(gmods):
            continue
        P = [1]
        for qf in sel:
            P = _z_mul(P, qf)
        for s in scalars:
            G = _trim_i([(v if v <= p // 2 else v - p)
                         for v in ((s * c) % p for c in P)])
            if G[-1] <= 0:
                continue
            H = _z_divmod(g, G)
            if H is not None:
                comp = [qf for qf in gmods
                        if not any(qf == t for t in sel)]
                return _split_z(G, sel, p) + _split_z(H, comp, p)
    return [g]


def _factor_primitive(f: list[int]) -> list[list[int]]:
    """Irreducible factorization of primitive, positive-lc f, deg >= 1."""
    d = len(f) - 1
    if d == 1:
        return [f]
    hq = _gcd_q(f, _deriv_z(f))
    if len(hq) - 1 >= 1:                     # repeated factors: peel (Yun)
        h_int = _clear_denoms(hq)
        q_int = _z_divmod(f, h_int)          # exact: monic divisor
        if q_int is None:                    # mathematically impossible
            raise RuntimeError("exact division failed (bug)")
        return _factor_primitive(h_int) + _factor_primitive(q_int)
    p = _good_prime(f, d)
    return _split_z(f, _mod_factors(f, p), p)


def _factor_z(f: list[int]) -> list[list[int]]:
    """Complete factorization: irreducibles primitive with positive leading
    coefficient; prime factors of |content| appear as constant [q] factors."""
    f = _trim_i(list(f))
    if f[-1] < 0:
        f = [-c for c in f]
    c = _content(f)
    prim = [x // c for x in f]
    out = [[q] for q in _prime_factors(c)]
    if degree(prim) >= 1:
        out += _factor_primitive(prim)
    return out


def irreducible_z(coeffs: list[int]):
    """DECIDE irreducibility over Z (unlike the one-way mod-p certificate).

    Returns (is_irreducible, factors): the complete factorization into
    irreducibles (primitive, positive leading coefficient; prime factors of
    the content listed as constant polynomials), or (False, None) when
    degree < 1. Blind spots such as x^4 + 1 are decided TRUE here even
    though no mod-p certificate can exist for them.
    """
    f = _trim_i([int(c) for c in coeffs])
    if degree(f) < 1:
        return False, None
    facs = _factor_z(f)
    return len(facs) == 1 and degree(facs[0]) >= 1, facs


# --------------------------------------------------------------------------
# analyze(): the full teacher-mode verdict
# --------------------------------------------------------------------------
def _safe_N(coeffs: list[int], want: int) -> int:
    """Largest n <= want with |f(n)| <= MR_LIMIT (primality stays a proof)."""
    if degree(coeffs) <= 1:
        return want

    def ok(n: int) -> bool:
        return abs(evaluate(coeffs, n)) <= MR_LIMIT

    if ok(want):
        return want
    lo, hi = 1, want
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid
    return lo


def analyze(coeffs: list[int], N: int = 20000, pmax: int = 3000,
            omega_pmax: int = 19) -> dict:
    """Full verdict on the Bunyakovsky hypotheses + data for the card.

    Irreducibility uses the DECIDABLE test (irreducible_z), so a blind-spot
    polynomial such as x^4+1 satisfies=True here, unlike in check_hypotheses
    (whose certificate is one-way). All primality decisions stay inside the
    deterministic Miller-Rabin range: N is silently reduced when needed
    (reported in warnings).
    """
    f = _trim_i([int(c) for c in coeffs])
    d, lc = degree(f), f[degree(f)]
    fd = fixed_divisor(f)
    cert_ok, cert_p = (irreducible_certificate(f) if d >= 1
                       else (False, None))
    dec, facs = irreducible_z(f)
    state = ("certified" if cert_ok else "decided" if dec else "reducible")
    satisfies = d >= 1 and lc > 0 and fd == 1 and dec
    warnings: list[str] = []
    if d < 1:
        warnings.append("degree 0: the conjecture concerns polynomials of "
                        "positive degree.")
    n_max = _safe_N(f, N)
    if n_max < N:
        warnings.append(
            f"scan reduced N = {N} -> {n_max}: |f(n)| must stay below "
            "3.3e24 so primality remains a proof, not a guess.")
    C = bunyakovsky_constant(f, pmax) if d >= 1 else None

    # one scan, everything else reads the flags
    flags = [False] * (n_max + 1)
    for n in range(1, n_max + 1):
        v = evaluate(f, n)
        flags[n] = v > 1 and is_prime(v)
    counts = []
    prefix = 0
    pref_at = {}
    marks = sorted({m for m in (1000, 10000, n_max) if 3 <= m <= n_max})
    for n in range(1, n_max + 1):
        prefix += flags[n]
        if n in marks:
            pref_at[n] = prefix
    for m in marks:
        pred = predicted_count(f, m, C=C) if C is not None else None
        emp = pref_at.get(m, 0)
        counts.append({"N": m, "empirical": emp, "predicted": pred,
                       "ratio": (emp / pred) if (pred and pred > 1e-9)
                       else None})
    first_primes = [(n, evaluate(f, n)) for n in range(1, n_max + 1)
                    if flags[n]][:10]
    first_composite = None
    for n in range(1, n_max + 1):
        if not flags[n]:
            first_composite = (n, evaluate(f, n))
            break
    # longest run of consecutive prime values for n >= 1 (within 5000)
    run_scan = min(n_max, 5000)
    best_len, best_start, cur = 0, 0, 0
    for n in range(1, run_scan + 1):
        if flags[n]:
            cur += 1
            if cur > best_len:
                best_len, best_start = cur, n - cur + 1
        else:
            cur = 0
    if state == "decided":
        warnings.append(
            "blind spot: f is irreducible over Z (decided), but f mod p is "
            "reducible for EVERY prime p -- no mod-p certificate can ever "
            "exist for this polynomial (its Galois group has no full "
            "cycle). check_hypotheses() reports satisfies=False for this "
            "reason; this card is right.")
    if state == "reducible" and facs:
        warnings.append("hypothesis 2 fails: see the factorization.")
    if fd > 1:
        warnings.append(
            f"fixed divisor {fd}: every value f(n) is divisible by {fd}, so "
            "the only possible prime value is " + (f"{fd} itself." if fd
            == 2 else f"{fd} (never reached for n >= 1 if f > fd)."))
    return {
        "coeffs": f, "degree": d, "leading_coeff": lc,
        "positive_leading": lc > 0,
        "fixed_divisor": fd, "no_fixed_prime": fd == 1,
        "irreducibility": {"state": state, "certificate_prime": cert_p,
                           "decided": dec, "factors": facs},
        "satisfies": satisfies,
        "C": C, "pmax": pmax, "omega_profile": omega_profile(f, omega_pmax),
        "counts": counts, "n_max": n_max,
        "first_primes": first_primes, "first_composite": first_composite,
        "prime_run": (best_start, best_len) if best_len else None,
        "warnings": warnings,
    }


def omega_profile(coeffs: list[int], pmax: int = 19):
    return [(p, roots_mod_p(coeffs, p))
            for p in _primes_small(pmax)]


def _primes_small(n: int) -> list[int]:
    from .bunyakovsky import primes_upto
    return primes_upto(n)


# --------------------------------------------------------------------------
# Markdown card renderer
# --------------------------------------------------------------------------
def _fac_str(multifac: dict) -> str:
    parts = []
    for q in sorted(multifac):
        e = multifac[q]
        parts.append(str(q) if e == 1 else f"{q}^{e}")
    return " \\cdot ".join(parts)


def _factor_capped(m: int, cap: int = 100000) -> tuple[dict, bool]:
    """Trial-division factorization capped at `cap`; second return value is
    False when a large cofactor could not be certified prime."""
    m = abs(m)
    facs: dict[int, int] = {}
    d = 2
    while d * d <= m:
        while m % d == 0:
            facs[d] = facs.get(d, 0) + 1
            m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        facs[m] = facs.get(m, 0) + 1
    known = all(is_prime(q) for q in facs)
    return facs, known


def render_analysis_md(a: dict) -> str:
    from .bunyakovsky import format_poly

    def tex(c):
        return _TEX_EXP.sub(r"^{\1}", format_poly(c))

    L: list[str] = []
    L.append(f"# Analysis: ${tex(a['coeffs'])}$\n")
    verdict = "**Satisfies all three Bunyakovsky hypotheses.**" \
        if a["satisfies"] else "**Does not satisfy the hypotheses.**"
    tail = ""
    if a["satisfies"]:
        tail = (" Infinitely many prime values follow from **Dirichlet's "
                "theorem** (1837)." if a["degree"] == 1 else
                " Infinitely many prime values are **conjectured** "
                "(the degree $\\ge 2$ case is open).")
    L.append(verdict + tail + "\n")

    irr = a["irreducibility"]
    if irr["state"] == "certified":
        irr_txt = f"yes -- certified mod $p = {irr['certificate_prime']}$"
    elif irr["state"] == "decided":
        irr_txt = ("yes -- decided over $\\mathbb{Z}$; no mod-$p$ "
                   "certificate is possible (*blind spot*, see notes)")
    elif irr["state"] == "reducible":
        irr_txt = "no: $" + "$ $\\cdot$ $".join(
            tex(g) for g in irr["factors"]) + "$"
    else:
        irr_txt = "n/a"
    pos = "yes" if a["positive_leading"] else "no"
    nf = "yes" if a["no_fixed_prime"] else "no"
    L.append("| Hypothesis | Verdict | Evidence |")
    L.append("|:---|:---|:---|")
    L.append(f"| 1. positive leading coefficient | {pos} "
             f"| $a_d = {a['leading_coeff']}$ |")
    L.append(f"| 2. irreducible over $\\mathbb{{Z}}$ | {irr_txt} "
             f"| decidable test, not just the mod-$p$ certificate |")
    L.append(f"| 3. no fixed prime divisor | {nf} "
             f"| $\\gcd$ of all values $= {a['fixed_divisor']}$ |")

    prof = a["omega_profile"]
    if prof:
        L.append("\n## Where the luck lives: $\\omega_f(p)$\n")
        L.append("| $p$ | " + " | ".join(str(p) for p, _ in prof) + " |")
        L.append("|---" * (len(prof) + 1) + "|")
        L.append("| $\\omega_f(p)$ | "
                 + " | ".join(str(w) for _, w in prof) + " |")

    L.append("\n## Bateman-Horn\n")
    if a["C"] is not None:
        L.append(f"$C(f) = {a['C']:.4f}$ "
                 f"(Euler product truncated at $p \\le {a['pmax']}$).\n")
    if a["counts"]:
        L.append("| $N$ | empirical | predicted | ratio |")
        L.append("|------:|--------:|----------:|------:|")
        for c in a["counts"]:
            pred = f"{c['predicted']:.1f}" if c["predicted"] is not None \
                else "—"
            rat = f"{c['ratio']:.4f}" if c["ratio"] is not None else "—"
            L.append(f"| {c['N']} | {c['empirical']} | {pred} | {rat} |")

    L.append("\n## Samples\n")
    if a["first_primes"]:
        fps = ", ".join(f"${evaluate(a['coeffs'], n)}$"
                        for n, _ in a["first_primes"][:8])
        L.append(f"- first prime values: {fps} ...")
    if a["prime_run"]:
        s, ln = a["prime_run"]
        L.append(f"- longest run of consecutive prime values: "
                 f"$n = {s}, \\dots, {s + ln - 1}$ ({ln} primes)")
    if a["first_composite"]:
        n, v = a["first_composite"]
        facs, known = _factor_capped(v)
        fs = _fac_str(facs) if facs else str(v)
        note = "" if known else " (large cofactor, not fully factored)"
        L.append(f"- first non-prime value: $f({n}) = {v}$ = ${fs}$"
                 f"{note}")
    if a["first_composite"] and a["satisfies"]:
        L.append("- a composite value does not contradict the conjecture: "
                 "*infinitely many* primes, not *all* primes.")

    if a["warnings"]:
        L.append("\n## Notes\n")
        for w in a["warnings"]:
            L.append(f"- {w}")
    L.append("")
    return "\n".join(L)
