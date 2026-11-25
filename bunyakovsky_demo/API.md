# bunyakovsky_demo — API reference

All public names are re-exported from the package root:

```python
from bunyakovsky_demo import check_hypotheses, scan_primes, bunyakovsky_constant
```

Stdlib only; no configuration; every function is a pure function of its
arguments.

## The one convention

A polynomial is a plain `list[int]` of coefficients **low-to-high**:

| Polynomial | coeffs |
|---|---|
| `x^2 + 1` | `[1, 0, 1]` |
| `x^2 + x + 41` | `[41, 1, 1]` |
| `3x + 2` | `[2, 3]` |
| `-x^2 + 5x + 1` | `[1, 5, -1]` |

No symbolic objects anywhere in the API.

## 1. Polynomial core

### `evaluate(coeffs, n) -> int`
f(n) by Horner's rule. `n` may be a float (used internally by the
Bateman–Horn integral); with int input the result is exact Python int
(arbitrary precision).

### `degree(coeffs) -> int`
Degree, ignoring trailing zero coefficients: `degree([1, 2, 0, 0]) == 1`,
`degree([5, 0, 0]) == 0`.

### `format_poly(coeffs) -> str`
Human-readable form: `format_poly([1, 5, -1]) == "-x^2 + 5x + 1"`,
`format_poly([41, 1, 1]) == "x^2 + x + 41"`.

## 2. Hypothesis machinery

The three Bunyakovsky hypotheses: (1) positive leading coefficient,
(2) irreducible over ℤ, (3) no prime dividing all values f(1), f(2), …

### `fixed_divisor(coeffs) -> int`
The gcd of **all** values f(1), f(2), … — the *fixed divisor*. Computed
from only deg+1 evaluations via the classical theorem
`gcd(all values) = gcd(f(0), f(1), …, f(deg f))` (binomial-coefficient
basis). **Hypothesis 3 holds exactly when the result is 1**, so it is
decidable. Examples: `fixed_divisor([2, 1, 1]) == 2` (x²+x+2 always even);
`fixed_divisor([1, 3, 2]) == 1` ((2x+1)(x+1) *passes* hypothesis 3).

### `primes_upto(n) -> list[int]`
Sieve of Eratosthenes, primes ≤ n. Empty list for n < 2.

### `is_prime(n) -> bool`
Deterministic Miller–Rabin, bases 2..37 — exact for every n < 3.3·10²⁴
(the demo stays far below, so primality decisions are proofs, not guesses).
`n < 2` → False, negatives → False.

### `roots_mod_p(coeffs, p) -> int`
ω_f(p): the number of residue classes x mod p with f(x) ≡ 0 (mod p).
Brute force over all residues, hence correct even when p divides the
leading coefficient (the reduction may become a constant → 0 roots).
This is the local quantity feeding `bunyakovsky_constant`.
Example: `[roots_mod_p([1,0,1], p) for p in (2,3,5,7,11,13)] == [1,0,2,0,0,2]`.

### `is_irreducible_mod_p(coeffs, p) -> bool`
Rabin's irreducibility test over 𝔽ₚ: f is irreducible iff it is squarefree
(gcd(f, f′) = 1) and gcd(f, x^(p^k) − x) = 1 for all 1 ≤ k ≤ deg(f)//2.
Raises `ValueError` if p divides the leading coefficient.

### `irreducible_certificate(coeffs, max_p=200) -> tuple[bool, int | None]`
Searches primes p ≤ max_p with p ∤ lc(f) for one where f mod p is
irreducible — that is **proof** f is irreducible over ℤ. Returns
`(True, p)` on success, `(False, None)` otherwise.

> **One-way by design.** `(False, None)` means *not certified*, not
> *reducible*: some irreducible polynomials (e.g. x⁴−10x²+1, Galois group
> V₄) factor modulo *every* prime and can never be certified this way.

### `check_hypotheses(coeffs) -> dict`
The headline gate. Returns:

```python
{
  "degree": 2,
  "leading_coeff": 1,
  "positive_leading": True,        # hypothesis 1
  "fixed_divisor": 1,
  "no_fixed_prime": True,          # hypothesis 3
  "irreducible_certified": True,   # hypothesis 2 (one-way, see above)
  "certificate_prime": 3,          # None if not certified
  "satisfies": True,               # all three
}
```

## 3. Quantitative side (Bateman–Horn / Hardy–Littlewood Conjecture F)

For f satisfying the hypotheses, the conjectured count of prime values is

    #{n ≤ N : f(n) prime}  ~  C(f) · ∫₂ᴺ dt / ln f(t)

### `scan_primes(coeffs, N, start=1) -> list[tuple[int, int]]`
Empirical side: every `(n, f(n))` with `start <= n <= N` and f(n) prime.
Values ≤ 1 are never prime. Example:
`len(scan_primes([41, 1, 1], 39, start=0)) == 40` (Euler's run).

### `bunyakovsky_constant(coeffs, pmax=10000) -> float`
The Euler product C(f) = ∏_p (1 − ω_f(p)/p) / (1 − 1/p), truncated at
p ≤ pmax. Sanity property: `bunyakovsky_constant([0, 1]) == 1.0` exactly
(f(t) = t ⇒ ω(p) = 1 ⇒ every factor is 1, and the formula collapses to
Li(N)). Measured: C(x²+1) = 1.371023 at pmax=10⁴ (literature ≈ 1.37281;
truncation error ≈ 0.13%).

### `predicted_count(coeffs, N, C=None, pmax=10000, M=20000) -> float`
Conjectural count C(f)·∫₂ᴺ dt/ln f(t) by trapezoid (M panels). Pass a
precomputed `C=` to avoid recomputing the product on every call.

**Measured agreement** (the demo prints this table): ratios
empirical/predicted drift toward 1 as N grows — 0.926 (N=10³),
0.985 (N=10⁴), **1.008** (N=10⁵, 6656 vs 6601.1) for x²+1;
0.999 for x²+x+41 at N=10⁴.

## 4. Runner

- `bunyakovsky_demo.demo.main(N, pmax) -> None` — prints the 7-section
  **Markdown** report (GitHub pipe tables + `$\LaTeX$` math, ready for
  `pandoc report.md -o report.pdf`): hypotheses table, Euler spotlight,
  Bateman–Horn check, why the hypotheses matter, cyclotomic structure,
  certificate blind spots, what C(f) means.
- `bunyakovsky_demo.demo.cli(argv=None) -> None` — argparse wrapper behind
  the `bunyakovsky-demo` console script and `python -m bunyakovsky_demo.demo`
  (`--N`, `--pmax`, plus `--plot PNG`, `--movie MP4`, `--stills DIR`,
  `--frames K`, `--no-report`, `--poly EXPR`; graphics need the `viz`
  extra). Graphics
  progress messages go to **stderr** so stdout stays a clean Markdown
  document when redirected.

## 5. Visualization layer (`bunyakovsky_demo.viz`, optional extra `viz`)

Data functions are pure stdlib; matplotlib is imported lazily inside the
render functions only.

| Function | What it gives |
|---|---|
| `cumulative_primes(coeffs, N)` | `E[n]` = #prime values for 1 ≤ k ≤ n, one pass |
| `predicted_series(coeffs, N, C, pmax, sub)` | `P[n]` = C·∫₂ⁿ dt/ln f(t) at every integer, cumulative trapezoid (`P[0..2] = 0`; ratio from n ≥ 3) |
| `omega_profile(coeffs, pmax)` | `[(p, ω_f(p))]` — local data behind the Euler product |
| `factorization_pattern(coeffs, p)` | degrees of the DISTINCT irreducible factors of f mod p (Yun radical + distinct-degree + Cantor–Bach); `ValueError` if p ∤ lc is violated |
| `pattern_matrix(coeffs, pmax)` | `[(p, pattern)]` — the Chebotarev heatmap data; blind spots never show the single pattern `(deg f)` |
| `euler_frames` / `bateman_horn_frames` / `storyboard` | scene generators yielding frame dicts (pure) |
| `draw_frame(frame, ax=None)` | renders one frame dict |
| `render_stills(frames, out_dir, every)` | numbered PNGs, no encoder |
| `encode(frames, out_path, fps, bitrate)` | mp4 via matplotlib's ffmpeg writer |
| `encode_moviepy(frames, out_path, fps)` | same stream through moviepy |
| `poster(out_path, N, pmax, C)` | the 2×2 overview PNG |

Verified 2026-11-23: `factorization_pattern` agrees with sympy 1.14 GF(p)
factorizations on 170 (polynomial, prime) pairs including the
characteristic-p traps (`f' ≡ 0`, `p | e_q`); the movie path was
round-tripped through ffmpeg 7.1 (h264, 338 frames, 13.5 s).

## 6. Teacher mode (`bunyakovsky_demo.analysis`, stdlib)

A teacher types a polynomial; the card decides the conjecture question.

| Function | What it gives |
|---|---|
| `parse_poly(s)` | human input → low-to-high `list[int]`: `"x^2 + x + 41"`, `"x² − x + 41"`, `"x**3 - x + 1"`, any single letter, or a bare `"1 0 1"` list. Never `eval`; raises `ValueError` with a message |
| `irreducible_z(coeffs)` | `(is_irreducible, factors)` — DECIDABLE over ℤ (Zassenhaus: squarefree prime above the Landau–Mignotte bound, mod-p factorization, subset products scaled by lc divisors, exact division; Yun peel for repeated factors). Blind spots like `x^4+1` return True. Factors include prime constants of the content |
| `analyze(coeffs, N=20000, pmax=3000)` | full verdict dict: hypotheses (irreducibility state `certified`/`decided`/`reducible`), ω_f profile, C(f), counts/ratios, first primes, longest prime run, first composite + factorization, warnings. `N` auto-reduced to keep `\|f(n)\| ≤ 3.3·10²⁴` |
| `render_analysis_md(a)` | the Markdown card (pipe tables + `$\LaTeX$`, pandoc-ready) |

`--poly EXPR` on the CLI (repeatable) prints one card per polynomial to
stdout instead of the standard report. `satisfies` here uses the DECIDABLE
test, so it can differ from `check_hypotheses()["satisfies"]` (one-way
certificate) exactly at the blind spots — the card is right, and says why.
Cross-checked against sympy's `factor_list` on 14 cases
(`tests/test_analysis.py`, optional oracle).

## 7. Hypothesis H mode (`bunyakovsky_demo.tuples`, stdlib)

| Function | Contract |
|:---|:---|
| `nu_mod_p(polys, p)` | distinct roots mod p of the product (brute force, exact) |
| `admissible(polys)` | `(is_admissible, witness_p or None)` — EXACT: testing primes `p <= sum(deg f_i)` suffices |
| `hypothesis_h_constant(polys, pmax=10000)` | `prod_p (1 - nu_p/p)/(1 - 1/p)^k` |
| `predicted_tuple_count(polys, N, C=None, pmax=10000)` | `C * int_2^N dt/(ln f_1 ... ln f_k)` (trapezoid) |
| `tuple_prime_scan(polys, N)` | `[(n, (f_1(n), ...))]` where all values are prime |
| `analyze_tuple(polys, N=20000, pmax=1000)` | dict: members (per-polynomial irreducibility + evidence), admissible/witness, `satisfies`, `C`, counts table, first hits, `twin` flag, warnings |
| `render_tuple_md(a)` | Markdown card (pipe tables + `$\LaTeX$`) |

`{x, x+2}` is detected and labeled as the twin-prime conjecture; its
constant equals 2·C₂ = 1.32032... (verified in tests against 1.31–1.33
at pmax=10⁴). `{x, x+2, x+4}` returns `witness=3` with the (3,5,7) note.

## 8. Landscape census (`bunyakovsky_demo.census`, stdlib)

| Function | Contract |
|:---|:---|
| `enumerate_polys(D, B)` | primitive polys, deg 1..D, positive leading coeff, all \|a_i\| <= B; deterministic order |
| `run_census(D=3, B=2, scan_N=300, pmax_C=200, blind_pmax=200, limit=20000)` | rows (per-polynomial: fd, decided irreducibility, certificate, satisfies, blind_spot, primes/longest run, C) + stats + by_degree + archetypes; raises `ValueError` above `limit` |
| `render_census_md(res)` | Markdown: class table, by-degree table, archetype tables (luckiest/unluckiest C, longest runs, blind spots, fd violators) |

Blind spots are confirmed via `viz.factorization_pattern` (import is lazy
at call time; still stdlib). By-degree table must show 0 blind spots at
prime degrees (Cauchy's theorem) — asserted in tests.

## 9. GUI (`bunyakovsky_demo.gui`, stdlib tkinter)

Imported ONLY on demand (`bunyakovsky-gui`, `bunyakovsky-demo --gui`,
or directly) — the package root never pulls tkinter.

| Function | Contract |
|:---|:---|
| `main(initial="")` | open the app; optional expression pre-fills and auto-runs |
| `compute_for(expr)` | analysis-card Markdown: single poly, or Hypothesis H card when `expr` contains a comma; raises `ValueError` on bad input |
| `compute_census(D, B)` | census Markdown |
| `render_lines(md)` | `[(tag, text)]` with tags `h1 h2 table bullet text`; tables re-aligned, all `$...$`/`**`/`\|` artifacts removed |
| `pretty_math(s)` | `$...$` spans → Unicode: `x^{2}`→x², `\mathbb{Z}`→ℤ, `\le`→≤, `\nu`→ν, `\dots`→…; unknown commands dropped |

Threading: scans run in a daemon worker; results re-enter Tk via
`root.after()` (Tk touched from the main thread only). Tests: pure
logic runs headless; the Tk roundtrip test skips without a display.

## Cost guide

| Call | Approx. cost |
|---|---|
| `check_hypotheses` (any demo polynomial) | ~ms |
| `scan_primes` per 10⁵ values | ~0.5 s |
| `bunyakovsky_constant` at pmax=10⁴ | ~2 s (root counting is O(p²/ln p) overall) |
| full `bunyakovsky-demo --N 100000` | ~25 s |

## Caveats

1. Irreducibility certificates are one-way (see above).
2. Miller–Rabin is deterministic only below 3.3·10²⁴; for N > 10⁸ with
   high-degree coefficients primality is only probabilistically sound.
3. C(f) truncation at pmax=10⁴ is ~0.13% low for x²+1; raising pmax is
   quadratic in cost.
