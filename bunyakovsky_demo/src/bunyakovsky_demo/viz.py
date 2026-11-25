"""Visualization layer for the Bunyakovsky demo (optional extra: `viz`).

    pip install bunyakovsky_demo[viz]      # pulls matplotlib
    bunyakovsky-demo --plot poster.png --movie movie.mp4

Design rules (why the core stays stdlib-only and movies are cheap):

* DATA and RENDER are separate. Everything numeric lives in pure functions
  (`cumulative_primes`, `predicted_series`, `omega_profile`,
  `factorization_pattern`, `pattern_matrix`) returning plain lists. All
  scanning happens BEFORE frame 1; rendering only draws precomputed data,
  so a frame is O(1) and no primality test or factorization runs during
  encoding.
* `matplotlib` is imported lazily inside the render functions. Importing
  this module (and every data function) works without it.
* Frame generators are plain iterators over small dicts of draw
  instructions. The same stream feeds PNG stills, matplotlib's ffmpeg
  writer, or moviepy -- frame-for-frame identical -- and is testable with
  no encoder present.

Public API: cumulative_primes, predicted_series, omega_profile,
factorization_pattern, pattern_matrix, euler_frames, bateman_horn_frames,
storyboard, draw_frame, render_stills, encode, encode_moviepy, poster.
"""
from __future__ import annotations

import math
from typing import Iterable, Iterator

from .bunyakovsky import (bunyakovsky_constant, degree, evaluate,
                          format_poly, is_prime, primes_upto, roots_mod_p)


# --------------------------------------------------------------------------
# Data layer (pure stdlib; no matplotlib)
# --------------------------------------------------------------------------
def cumulative_primes(coeffs: list[int], N: int) -> list[int]:
    """E[n] = #{1 <= k <= n : f(k) prime}, computed in ONE pass; index = n."""
    E = [0] * (N + 1)
    c = 0
    for n in range(1, N + 1):
        v = evaluate(coeffs, n)
        if v > 1 and is_prime(v):
            c += 1
        E[n] = c
    return E


def predicted_series(coeffs: list[int], N: int, C: float | None = None,
                     pmax: int = 10000, sub: int = 8) -> list[float]:
    """P[n] = C * integral_2^n dt / ln f(t), cumulative trapezoid sampled at
    the integers, so any frame can read P[n] in O(1).

    P[0] = P[1] = P[2] = 0.0 (the integral starts at 2): form ratios from
    n >= 3. `sub` = trapezoid panels per unit interval.
    """
    if C is None:
        C = bunyakovsky_constant(coeffs, pmax)
    step = 1.0 / sub
    P = [0.0] * (N + 1)
    acc, prev = 0.0, None
    for i in range((N - 2) * sub + 1):
        t = 2.0 + i * step
        v = evaluate(coeffs, t)
        y = 1.0 / math.log(v) if v > 1 else 0.0
        if prev is not None:
            acc += 0.5 * (prev + y) * step
        prev = y
        if i % sub == 0:
            P[2 + i // sub] = C * acc
    return P


def omega_profile(coeffs: list[int], pmax: int = 200) -> list[tuple[int, int]]:
    """[(p, omega_f(p))] for primes p <= pmax: the local data behind every
    factor of the Bateman-Horn constant. omega_f(p) == p exactly when p
    divides the fixed divisor (hypothesis 3 fails)."""
    return [(p, roots_mod_p(coeffs, p)) for p in primes_upto(pmax)]


# ---- finite-field helpers (F_p only, module-private) ----
def _trim(a: list[int]) -> list[int]:
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _mod(a: list[int], b: list[int], p: int) -> list[int]:
    a = [x % p for x in a]
    b = _trim([x % p for x in b])
    binv = pow(b[-1], -1, p)
    while len(a) >= len(b):
        s = len(a) - len(b)
        q = a[-1] * binv % p
        for j in range(len(b)):
            a[s + j] = (a[s + j] - q * b[j]) % p
        a.pop()
        if not a:
            return [0]
    return _trim(a)


def _gcd(a: list[int], b: list[int], p: int) -> list[int]:
    a, b = _trim([x % p for x in a]), _trim([x % p for x in b])
    while b != [0]:
        a, b = b, _mod(a, b, p)
    inv = pow(a[-1], -1, p)
    return _trim([(c * inv) % p for c in a])


def _mul(a: list[int], b: list[int], p: int) -> list[int]:
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return r


def _powmod(base: list[int], e: int, m: list[int], p: int) -> list[int]:
    r, b = [1], _mod(base, m, p)
    while e:
        if e & 1:
            r = _mod(_mul(r, b, p), m, p)
        b = _mod(_mul(b, b, p), m, p)
        e >>= 1
    return r


def _div_exact(a: list[int], b: list[int], p: int) -> list[int]:
    """Exact quotient a / b over F_p (b | a assumed; remainder discarded)."""
    a = _trim([x % p for x in a])
    b = _trim([x % p for x in b])
    q = [0] * (len(a) - len(b) + 1)
    r = list(a)
    binv = pow(b[-1], -1, p)
    for k in range(len(q) - 1, -1, -1):
        coef = r[k + len(b) - 1] * binv % p
        q[k] = coef
        for j in range(len(b)):
            r[k + j] = (r[k + j] - coef * b[j]) % p
    return _trim(q)


def _radical(f: list[int], p: int) -> list[int]:
    """Product of the DISTINCT irreducible factors of f over F_p (Yun's
    squarefree factorization specialized to the radical). Handles both
    characteristic-p traps: f' == 0 (f is a p-th power: pull p-th roots of
    the exponent vector) and p | e_q (f/gcd(f,f') silently DROPS factors whose
    multiplicity is divisible by p -- those live in g, minus the ones w
    already covers)."""
    deriv = _trim([(i * c) % p for i, c in enumerate(f)][1:] or [0])
    if deriv == [0]:
        return _radical(_trim(f[::p]), p) if len(f) > 1 else f
    g = _gcd(f, deriv, p)
    if g == [1]:
        return f                                   # already squarefree
    w = _div_exact(f, g, p)                        # squarefree; all q with p∤e_q
    while True:
        h = _gcd(g, w, p)
        if h == [1]:
            break
        g = _div_exact(g, h, p)                    # drop q's covered by w
    return _trim(_mul(w, _radical(g, p), p))


def _edf_split(f: list[int], d: int, p: int, acc: list[int]) -> None:
    """Cantor-Bach equal-degree split: append the degrees of the irreducible
    factors of squarefree f (all of degree d). Deterministic scan of
    a = b*x + c, so results are reproducible. p == 2 uses the trace variant."""
    deg = len(f) - 1
    if deg <= 0:
        return
    if deg == d:
        acc.append(d)
        return
    e = (p ** d - 1) // 2
    b = 1
    while True:                                # a splitter always exists
        for c in range(p):
            a = [c, b]
            if p > 2:
                h = _powmod(a, e, f, p)
                h[0] = (h[0] - 1) % p          # Cantor-Bach: gcd(f, h - 1)
            else:                              # trace: h = sum a^(2^i)
                h, ap = list(a), list(a)
                for _ in range(d - 1):
                    ap = _powmod(ap, 2, f, 2)
                    m = max(len(h), len(ap))
                    h = [(h[i] if i < len(h) else 0)
                         + (ap[i] if i < len(ap) else 0) for i in range(m)]
            g = _gcd(f, _trim([x % p for x in h]), p)
            if [1] != g != f:
                _edf_split(g, d, p, acc)
                _edf_split(_div_exact(f, g, p), d, p, acc)
                return
        b += 1


def factorization_pattern(coeffs: list[int], p: int) -> list[int]:
    """Degrees of the DISTINCT irreducible factors of f mod p (ascending),
    via the radical (Yun) + distinct-degree factorization + Cantor-Bach
    equal-degree split. Verified against sympy's GF(p) factorizer
    (tests/test_viz.py, optional oracle).

    This is the Chebotarev picture behind demo section [6]: the multiset of
    patterns as p varies reflects the Galois group, and "never the single
    pattern (deg f)" is exactly what defeats the mod-p irreducibility
    certificate (x^4+1, x^4-10x^2+1 -- Galois group has no full-cycle
    element). Raises ValueError if p divides the leading coefficient.
    """
    d = degree(coeffs)
    if coeffs[d] % p == 0:
        raise ValueError(f"p={p} divides the leading coefficient")
    f = [c % p for c in coeffs[:d + 1]]
    inv = pow(f[d], -1, p)
    f = _trim([(c * inv) % p for c in f])          # monic
    f = _radical(f, p)
    d = len(f) - 1
    out: list[int] = []
    rem, xpow = f, [0, 1]
    for k in range(1, d // 2 + 1):
        if len(rem) - 1 < k:
            break
        # xpow = x^(p^k) mod f; gcd(rem, xpow - x) = product of deg-k factors
        xpow = _powmod(xpow, p, f, p)
        h = list(xpow) + [0] * (2 - len(xpow))
        h[1] = (h[1] - 1) % p
        g = _gcd(rem, _trim(h), p)
        if g != [1]:
            if k == 1:
                out.extend([1] * (len(g) - 1))    # product of distinct linears
            else:
                _edf_split(g, k, p, acc=out)
            rem = _div_exact(rem, g, p)
    if len(rem) - 1 > 0:                          # survivor is irreducible
        out.append(len(rem) - 1)
    out.sort()
    return out


def pattern_matrix(coeffs: list[int], pmax: int = 97) -> list[tuple[int, tuple[int, ...]]]:
    """[(p, pattern)] for primes p <= pmax with p not | lc(f): the Chebotarev
    data for the blind-spot heatmap (demo section [6])."""
    d = degree(coeffs)
    return [(p, tuple(factorization_pattern(coeffs, p)))
            for p in primes_upto(pmax) if coeffs[d] % p]


# --------------------------------------------------------------------------
# Frame generators (pure: they yield draw instructions, they don't draw)
# --------------------------------------------------------------------------
def euler_frames(coeffs: list[int], n_max: int = 61,
                 hold: int = 15) -> Iterator[dict]:
    """Scene: the Euler prime run, one dot per n, then a hold on the failure."""
    for n in range(n_max + 1):
        yield {"kind": "euler", "n": n, "coeffs": coeffs}
    for _ in range(hold):
        yield {"kind": "euler", "n": n_max, "coeffs": coeffs, "hold": True}


def bateman_horn_frames(coeffs: list[int], E: list[int], P: list[float],
                        n_end: int, n_start: int = 50, frames: int = 260,
                        ease: float = 1.6) -> Iterator[dict]:
    """Scene: the empirical count chasing the Bateman-Horn curve. Frames read
    the precomputed arrays only."""
    for i in range(frames + 1):
        n = int(n_start + (n_end - n_start) * (i / frames) ** ease)
        yield {"kind": "bateman_horn", "n": n, "coeffs": coeffs, "E": E, "P": P}


def storyboard(*scenes: Iterable[dict]) -> Iterator[dict]:
    """Concatenate scene generators into one movie timeline."""
    return (f for sc in scenes for f in sc)


# --------------------------------------------------------------------------
# Render layer (matplotlib imported lazily)
# --------------------------------------------------------------------------
def draw_frame(frame: dict, ax=None):
    """Draw one frame dict. ax=None -> a fresh figure is made and returned;
    passing an Axes reuses it (the animation path)."""
    import matplotlib.pyplot as plt
    own_fig = ax is None
    if own_fig:
        _, ax = plt.subplots(figsize=(9.6, 5.4))
    kind, n, coeffs = frame["kind"], frame["n"], frame["coeffs"]
    ax.clear()
    if kind == "euler":
        xs = list(range(n + 1))
        ys = [evaluate(coeffs, k) for k in xs]
        cols = ["#2ca02c" if (v > 1 and is_prime(v)) else "#d62728" for v in ys]
        ax.scatter(xs, ys, c=cols, s=34, zorder=3)
        ax.set_xlim(-1.5, max(xs) + 1.5)
        ax.set_ylim(0, max(ys) * 1.15 if ys else 1)
        ax.set_xlabel("n")
        ax.set_title(f"{format_poly(coeffs)} — prime values in green")
        if not frame.get("hold"):
            ax.text(0.02, 0.94, f"prime run so far: {n + 1}",
                    transform=ax.transAxes, va="top", fontsize=11)
    elif kind == "bateman_horn":
        nn = list(range(3, n + 1))
        ax.step(nn, frame["E"][3:n + 1], where="post", color="k", lw=1.2,
                label=f"empirical = {frame['E'][n]}")
        ax.plot(nn, frame["P"][3:n + 1], color="#1f77b4", lw=1.8, ls="--",
                label=f"predicted = {frame['P'][n]:.0f}")
        ax.set_xlim(0, n * 1.02)
        ax.set_ylim(0, max(frame["E"][n], frame["P"][n]) * 1.12 + 1)
        ax.set_xlabel("n")
        ax.set_title(f"{format_poly(coeffs)}: count vs Bateman–Horn")
        if frame["P"][n] > 0:
            ax.text(0.97, 0.94,
                    f"n = {n}    ratio = {frame['E'][n] / frame['P'][n]:.3f}",
                    transform=ax.transAxes, ha="right", va="top", fontsize=12,
                    family="monospace")
        ax.legend(loc="lower right", fontsize=9)
    else:
        raise ValueError(f"unknown frame kind {kind!r}")
    return ax if not own_fig else ax.get_figure()


def render_stills(frames: Iterable[dict], out_dir: str,
                  every: int = 1) -> list[str]:
    """Render a frame stream to numbered PNGs (no encoder involved; feed them
    to ffmpeg later: `ffmpeg -framerate 25 -i frame_%05d.png out.mp4`)."""
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(out_dir, exist_ok=True)
    paths: list[str] = []
    for i, fr in enumerate(frames):
        if i % every:
            continue
        fig = draw_frame(fr)
        path = os.path.join(out_dir, f"frame_{i:05d}.png")
        fig.savefig(path)
        plt.close(fig)
        paths.append(path)
    return paths


def encode(frames: Iterable[dict], out_path: str, fps: int = 25,
           bitrate: int = 2400) -> str:
    """Render a frame stream to mp4 via matplotlib's ffmpeg writer
    (needs the ffmpeg binary on PATH)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter, FuncAnimation
    fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=110)
    anim = FuncAnimation(fig, lambda fr: draw_frame(fr, ax), frames=frames,
                         cache_frame_data=False)
    anim.save(out_path, writer=FFMpegWriter(fps=fps, bitrate=bitrate))
    plt.close(fig)
    return out_path


def encode_moviepy(frames: Iterable[dict], out_path: str, fps: int = 25) -> str:
    """Alternative encoder: same frame stream through moviepy's
    ImageSequenceClip (frame-for-frame identical to `encode`)."""
    import tempfile
    import matplotlib
    matplotlib.use("Agg")
    try:
        from moviepy import ImageSequenceClip          # moviepy >= 2.0
    except ImportError:                                # moviepy 1.x
        from moviepy.editor import ImageSequenceClip
    with tempfile.TemporaryDirectory() as td:
        paths = render_stills(frames, td)
        clip = ImageSequenceClip(paths, fps=fps)
        clip.write_videofile(out_path, codec="libx264", audio=False,
                             ffmpeg_params=["-crf", "20"])
        clip.close()
    return out_path


def poster(out_path: str, N: int = 20000, pmax: int = 3000,
           C: float | None = None) -> str:
    """Static 2x2 overview: (a) x^2+1 count vs Bateman-Horn, (b) the ratio
    drifting to 1, (c) the 11x C(f) contrast of demo section [7], (d) Euler's
    run with the 41^2 failure. Returns out_path."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    bh, euler = [1, 0, 1], [41, 1, 1]
    unlucky, lucky = [41, -1, 1, 1], [1, -1, 0, 0, 0, 1]
    if C is None:
        C = bunyakovsky_constant(bh, pmax)
    E_bh, P_bh = cumulative_primes(bh, N), predicted_series(bh, N, C)
    N2 = min(N, 2000)
    C_un = bunyakovsky_constant(unlucky, pmax)
    C_lu = bunyakovsky_constant(lucky, pmax)
    E_un, P_un = cumulative_primes(unlucky, N2), predicted_series(unlucky, N2, C_un)
    E_lu, P_lu = cumulative_primes(lucky, N2), predicted_series(lucky, N2, C_lu)

    fig, axs = plt.subplots(2, 2, figsize=(11, 7.5), dpi=130)
    n_ax = range(2, N + 1)
    ax = axs[0, 0]
    ax.step(n_ax, E_bh[2:], where="post", color="k", lw=1.2, label="empirical")
    ax.plot(n_ax, P_bh[2:], color="#1f77b4", lw=1.8, ls="--",
            label="Bateman–Horn")
    ax.set_title(r"$x^2+1$: prime values vs $C(f)\,\int_2^n dt/\ln f(t)$")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_xlabel("n")

    ax = axs[0, 1]
    ax.plot(range(3, N + 1),
            [E_bh[n] / P_bh[n] for n in range(3, N + 1)],
            color="#1f77b4", lw=1.0)
    ax.axhline(1.0, color="#7f7f7f", lw=0.8, ls=":")
    ax.set_xscale("log")
    ax.set_ylim(0.8, 1.3)
    ax.set_title("ratio empirical / predicted  →  1")
    ax.set_xlabel("n (log)")

    ax = axs[1, 0]
    n2 = range(2, N2 + 1)
    ax.plot(n2, E_lu[2:], color="#2ca02c", lw=1.4,
            label=rf"$x^5-x+1$  (C={C_lu:.2f})")
    ax.plot(n2, P_lu[2:], color="#2ca02c", lw=1.0, ls="--")
    ax.plot(n2, E_un[2:], color="#d62728", lw=1.4,
            label=rf"$x^3+x^2-x+41$  (C={C_un:.2f})")
    ax.plot(n2, P_un[2:], color="#d62728", lw=1.0, ls="--")
    ax.set_title("11× density gap, same conjecture")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_xlabel("n")

    ax = axs[1, 1]
    vals = [evaluate(euler, n) for n in range(0, 60)]
    cols = ["#2ca02c" if (v > 1 and is_prime(v)) else "#d62728" for v in vals]
    cols[40] = "#9467bd"
    ax.bar(range(60), vals, color=cols, width=0.8)
    ax.annotate("f(40)=1681=41²", xy=(40, 1681), xytext=(42, 900),
                arrowprops=dict(arrowstyle="->", color="#9467bd"),
                color="#9467bd", fontsize=9)
    ax.set_title(r"Euler $x^2+x+41$: 40 primes, then $41^2$")
    ax.set_xlabel("n")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    return out_path
