"""Core routines for the Bunyakovsky-conjecture demo (stdlib only).

Convention: a polynomial is a list of integer coefficients LOW-to-HIGH,
e.g. x^2 + 1  ->  [1, 0, 1].
"""
from __future__ import annotations

import math


# --------------------------------------------------------------------------
# Polynomial core
# --------------------------------------------------------------------------
def degree(coeffs: list[int]) -> int:
    """Degree, ignoring trailing zero coefficients. degree([0]) == 0."""
    d = len(coeffs) - 1
    while d > 0 and coeffs[d] == 0:
        d -= 1
    return d


def evaluate(coeffs: list[int], n) -> int:
    """f(n) by Horner's rule (also accepts float n)."""
    acc = 0
    for c in reversed(coeffs):
        acc = acc * n + c
    return acc


def format_poly(coeffs: list[int]) -> str:
    """Human-readable polynomial, e.g. [41, 1, 1] -> 'x^2 + x + 41'."""
    d = degree(coeffs)
    parts: list[str] = []
    for k in range(d, -1, -1):
        c = coeffs[k]
        if c == 0:
            continue
        mag = abs(c)
        if k == 0:
            term = str(mag)
        elif k == 1:
            term = "x" if mag == 1 else f"{mag}x"
        else:
            term = f"x^{k}" if mag == 1 else f"{mag}x^{k}"
        if not parts:
            parts.append(("-" if c < 0 else "") + term)
        else:
            parts.append((" - " if c < 0 else " + ") + term)
    return "".join(parts) if parts else "0"


# --------------------------------------------------------------------------
# Fixed divisor (decidable hypothesis 3)
# --------------------------------------------------------------------------
def fixed_divisor(coeffs: list[int]) -> int:
    """gcd(f(1), f(2), f(3), ...) -- the FIXED DIVISOR of f.

    Classical theorem (binomial-coefficient basis): the gcd of ALL values of
    f equals gcd(f(0), f(1), ..., f(deg f)).  Bunyakovsky hypothesis 3 is
    exactly  fixed_divisor(f) == 1, so it is decidable from deg+1 values.
    """
    d = degree(coeffs)
    g = 0
    for k in range(d + 1):
        g = math.gcd(g, evaluate(coeffs, k))
    return g


# --------------------------------------------------------------------------
# Primes: sieve + deterministic Miller-Rabin
# --------------------------------------------------------------------------
_MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def primes_upto(n: int) -> list[int]:
    """Sieve of Eratosthenes, primes <= n."""
    if n < 2:
        return []
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    i = 2
    while i * i <= n:
        if s[i]:
            s[i * i:n + 1:i] = bytearray(len(range(i * i, n + 1, i)))
        i += 1
    return [k for k in range(2, n + 1) if s[k]]


def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin with bases 2..37 (exact below 3.3e24)."""
    if n < 2:
        return False
    for p in _MR_BASES:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in _MR_BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


# --------------------------------------------------------------------------
# omega_f(p): root counting mod p
# --------------------------------------------------------------------------
def roots_mod_p(coeffs: list[int], p: int) -> int:
    """omega_f(p): number of residue classes x mod p with f(x) == 0 (mod p).

    Brute force over all residues -- correct even when p divides lc(f).
    """
    red = [c % p for c in coeffs]
    return sum(1 for x in range(p) if evaluate(red, x) % p == 0)


# --------------------------------------------------------------------------
# Irreducibility certificate (Rabin test over F_p)
# --------------------------------------------------------------------------
def _trim(a: list[int]) -> list[int]:
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _poly_mod(a: list[int], b: list[int], p: int) -> list[int]:
    """a mod b over F_p, b != 0."""
    a = [x % p for x in a]
    b = _trim([x % p for x in b])
    binv = pow(b[-1], -1, p)
    while len(a) >= len(b):
        shift = len(a) - len(b)
        f = a[-1] * binv % p
        for j in range(len(b)):
            a[shift + j] = (a[shift + j] - f * b[j]) % p
        a.pop()
        if not a:
            return [0]
    return _trim(a)


def _poly_gcd(a: list[int], b: list[int], p: int) -> list[int]:
    """Monic gcd over F_p."""
    a, b = _trim([x % p for x in a]), _trim([x % p for x in b])
    while b != [0]:
        a, b = b, _poly_mod(a, b, p)
    inv = pow(a[-1], -1, p)
    return _trim([(c * inv) % p for c in a])


def _poly_mul_mod(a: list[int], b: list[int], m: list[int], p: int) -> list[int]:
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return _poly_mod(r, m, p)


def _poly_pow_mod(base: list[int], e: int, m: list[int], p: int) -> list[int]:
    r = [1]
    while e:
        if e & 1:
            r = _poly_mul_mod(r, base, m, p)
        base = _poly_mul_mod(base, base, m, p)
        e >>= 1
    return r


def is_irreducible_mod_p(coeffs: list[int], p: int) -> bool:
    """Rabin's irreducibility test over F_p.

    Requires p not dividing the leading coefficient. f (degree d >= 1) is
    irreducible over F_p iff f is squarefree (gcd(f, f') == 1) and
    gcd(f, x^(p^k) - x) == 1 for every 1 <= k <= d//2: squarefree with no
    factor of degree <= d//2 forces a single irreducible factor.
    """
    d = degree(coeffs)
    f = [c % p for c in coeffs[:d + 1]]
    if f[d] == 0:
        raise ValueError(f"p={p} divides the leading coefficient")
    inv = pow(f[d], -1, p)
    f = [(c * inv) % p for c in f]              # monic
    deriv = _trim([(i * c) % p for i, c in enumerate(f)][1:] or [0])
    if _poly_gcd(f, deriv, p) != [1]:           # squarefree?
        return False
    if d == 1:
        return True
    h = [0, 1]                                  # h = x, becomes x^(p^k) mod f
    for _ in range(d // 2):                     # k = 1 .. floor(d/2)
        h = _poly_pow_mod(h, p, f, p)
        g = list(h) + [0] * (2 - len(h))        # pad so g[1] exists
        g[1] = (g[1] - 1) % p                   # h - x
        if _poly_gcd(f, _trim(g), p) != [1]:
            return False
    return True


def irreducible_certificate(coeffs: list[int], max_p: int = 200):
    """Try to certify irreducibility over Z: find prime p, p not | lc, with
    f mod p irreducible (sufficient, not necessary -- e.g. x^4-10x^2+1 has
    no such p). Returns (certified, p_or_None)."""
    d = degree(coeffs)
    if d < 1:
        return False, None
    for p in primes_upto(max_p):
        if coeffs[d] % p:
            if is_irreducible_mod_p(coeffs, p):
                return True, p
    return False, None


# --------------------------------------------------------------------------
# Hypothesis gate
# --------------------------------------------------------------------------
def check_hypotheses(coeffs: list[int]) -> dict:
    """Evaluate the three Bunyakovsky hypotheses (irreducibility one-way)."""
    d = degree(coeffs)
    lc = coeffs[d]
    fd = fixed_divisor(coeffs)
    irr, cert = irreducible_certificate(coeffs)
    return {
        "degree": d,
        "leading_coeff": lc,
        "positive_leading": lc > 0,
        "fixed_divisor": fd,
        "no_fixed_prime": fd == 1,
        "irreducible_certified": irr,
        "certificate_prime": cert,
        "satisfies": d >= 1 and lc > 0 and fd == 1 and irr,
    }


# --------------------------------------------------------------------------
# Prime-value scan
# --------------------------------------------------------------------------
def scan_primes(coeffs: list[int], N: int, start: int = 1) -> list[tuple[int, int]]:
    """All (n, f(n)) with start <= n <= N and f(n) prime."""
    out = []
    for n in range(start, N + 1):
        v = evaluate(coeffs, n)
        if v > 1 and is_prime(v):
            out.append((n, v))
    return out


# --------------------------------------------------------------------------
# Bateman-Horn constant + predicted count
# --------------------------------------------------------------------------
def bunyakovsky_constant(coeffs: list[int], pmax: int = 10000) -> float:
    """C(f) = prod_p (1 - omega_f(p)/p) / (1 - 1/p), truncated at p <= pmax.

    Bateman-Horn / Hardy-Littlewood Conjecture F constant for a single
    polynomial. Factors are 1 + O(1/p^2) on average, so the product
    converges; truncation at 10^4 is within ~0.2% for x^2+1.
    """
    c = 1.0
    for p in primes_upto(pmax):
        w = roots_mod_p(coeffs, p)
        c *= (1.0 - w / p) / (1.0 - 1.0 / p)
    return c


def predicted_count(coeffs: list[int], N: int, C: float | None = None,
                    pmax: int = 10000, M: int = 20000) -> float:
    """Conjectural count of prime values for 1 <= n <= N:
    C(f) * integral_2^N dt / ln f(t)   (trapezoid, M panels).
    """
    if C is None:
        C = bunyakovsky_constant(coeffs, pmax)
    h = (N - 2) / M
    s = 0.0
    for i in range(M + 1):
        t = 2 + i * h
        v = evaluate(coeffs, t)
        y = 1.0 / math.log(v) if v > 1 else 0.0
        s += y if 0 < i < M else 0.5 * y
    return C * s * h
