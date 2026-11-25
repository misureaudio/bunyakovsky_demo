# bunyakovsky_demo

A self-contained (stdlib-only) demo of **Bunyakovsky's conjecture** (1857):

> If $f \in \mathbb{Z}[x]$ has (1) positive leading coefficient, (2) is
> irreducible over $\mathbb{Z}$, and (3) has no prime dividing all of its
> values $f(1), f(2), \dots$, then $f(n)$ is prime for infinitely many $n$.

The linear case is Dirichlet's theorem (1837, **proved**); every degree
$\ge 2$ case is open — $x^2+1$ is Landau's problem #1 (1912). The general
form for several polynomials is Schinzel's Hypothesis H (1958). The
quantitative companion used here is **Hardy–Littlewood Conjecture F /
Bateman–Horn**, not Bunyakovsky's original statement.

## Install & quickstart

```bash
pip install .                     # from this repo root
bunyakovsky-demo                  # console entry point (Markdown report)
bunyakovsky-demo --N 100000       # bigger scan
bunyakovsky-demo > report.md      # the report IS markdown (pipe tables + $LaTeX$)
pandoc report.md -o report.pdf    # PDF conversion
```

Or run without installing, from a checkout root:

```bash
python -m bunyakovsky_demo.demo   # needs src/ on PYTHONPATH, e.g.
PYTHONPATH=src python -m bunyakovsky_demo.demo
pytest                            # 103 tests (pythonpath configured in pyproject)
```

## Graphics & movie (v1.2.0, optional extra)

```bash
pip install "bunyakovsky_demo[viz]"        # pulls matplotlib; mp4 needs ffmpeg
bunyakovsky-demo --plot poster.png         # 2x2 static overview
bunyakovsky-demo --movie movie.mp4         # 2-scene film (Euler run, then
                                           # Bateman-Horn count chase on x^2+1)
bunyakovsky-demo --stills frames/          # PNG frames, encode later with ffmpeg
```

The `viz` layer keeps the core stdlib-only and splits DATA from RENDER:
`cumulative_primes`/`predicted_series`/`pattern_matrix` compute everything
once; scenes (`euler_frames`, `bateman_horn_frames`, `storyboard`) are pure
iterators of draw instructions; `draw_frame`/`encode`/`encode_moviepy`/
`poster` only draw. A frame is therefore O(1) — the 13.5 s, 338-frame movie
encodes in ~25 s because no primality test runs during encoding.
`factorization_pattern` (radical + distinct-degree + Cantor-Bach, stdlib)
exposes the Chebotarev picture behind the certificate blind spots and is
verified against sympy's GF(p) factorizer in `tests/test_viz.py`.

```python
from bunyakovsky_demo import check_hypotheses, scan_primes
check_hypotheses([1, 3, 2])   # (2x+1)(x+1): passes fd, fails irreducibility
scan_primes([41, 1, 1], 39, start=0)   # Euler: 40 primes in a row
```

Full function-by-function reference: **[API.md](API.md)**.

## GUI (v1.6.0, stdlib tkinter — no extra dependencies)

```bash
bunyakovsky-gui                   # or: bunyakovsky-demo --gui
bunyakovsky-gui "x, x+2"          # open pre-loaded with a result
```

One window for the whole lab: type a polynomial (or a comma-separated
Hypothesis H tuple) and press Enter, pick a preset specimen (Landau,
Euler, the blind spot $x^4+1$, twins, the failing triplet), or run the
census with degree/height spinboxes. The Markdown cards are rendered
readable — headings, aligned monospace tables, and real Unicode math
($x^{2}$ → x², $\mathbb{Z}$ → ℤ, $\le$ → ≤, $\nu$ → ν) — while
**Copy Markdown** / **Save .md** keep the raw card for pandoc. Scans run
in a worker thread, so the window stays responsive during a census.
Parsing still goes through `parse_poly` — never `eval`. Module:
`bunyakovsky_demo.gui` (imported only on demand; `pretty_math`,
`render_lines`, `compute_for`, `compute_census` are pure and tested
headless).

## Teacher mode (v1.4.0): analyze any polynomial

```bash
bunyakovsky-demo --poly "x^4 + 1"                # Markdown analysis card
bunyakovsky-demo --poly "x² - x + 41" --poly "2x^2+3x+1"   # repeatable
bunyakovsky-demo --poly "x^2+1" > card.md && pandoc card.md -o card.pdf
```

A teacher-typed expression (`x^2 + x + 41`, `x² − x + 41`, `x**3 - x + 1`,
or a bare low-to-high list `1 0 1`) is parsed — never `eval`ed — and the
card decides all three hypotheses with witnesses: the fixed divisor, the
factorization or certificate prime, the $\omega_f(p)$ profile, $C(f)$ with
empirical/predicted counts, first primes, longest prime run, first
composite value with its factorization. Unlike `check_hypotheses`,
hypothesis 2 here is **decidable** (Zassenhaus-style factorization over
$\mathbb{Z}$, stdlib): blind spots such as $x^4+1$ correctly report
`satisfies: yes`, with a note explaining why no mod-$p$ certificate can
exist. Primality stays inside the deterministic Miller–Rabin range
($N$ is auto-reduced and the card says so). API: `parse_poly`,
`irreducible_z`, `analyze`, `render_analysis_md`.

## Hypothesis H mode (v1.5.0): tuples, twin primes included

```bash
bunyakovsky-demo --tuple "x, x+2"            # the twin-prime conjecture
bunyakovsky-demo --tuple "x, x+2, x+4"       # inadmissible: only (3,5,7)
bunyakovsky-demo --tuple "x, x^2+1"          # admissible? the card decides
```

Schinzel's Hypothesis H (1958) is Bunyakovsky for k-tuples: each entry
irreducible with positive leading coefficient, plus **admissibility** —
no prime $p$ for which the product $\prod f_i$ vanishes in every residue
class. The card decides admissibility *exactly* (it suffices to test
$p \le \sum_i \deg f_i$), computes the tuple Bateman–Horn constant
$C = \prod_p (1 - \nu_p/p)/(1-1/p)^k$ and the empirical vs predicted
all-prime counts. For $\{n, n+2\}$ the code reproduces the classical
constant $2C_2 = 1.32032\ldots$ and the twin-prime prediction to within
a few percent at $N = 10^4$ — with the honest label that this IS the
twin-prime conjecture (open; nearest theorems: Zhang 2014, Maynard
bounded gaps). API: `admissible`, `hypothesis_h_constant`,
`analyze_tuple`, `render_tuple_md`.

## Landscape census (v1.5.0): the whole box, classified

```bash
bunyakovsky-demo --census --degree 3 --height 2      # seconds
bunyakovsky-demo --census --degree 4 --height 2      # ~1-2 minutes
```

Enumerates every primitive polynomial of degree $\le D$, positive leading
coefficient, $\|f\| \le B$, and classifies each with the DECIDABLE
irreducibility test: satisfies / reducible / fixed-divisor violator,
plus $C(f)$ (small-$p$ truncation — for ranking), prime-value counts and
longest runs, and **blind spots found empirically** (satisfies, yet the
mod-$p$ factorization pattern is never $(d)$ up to $p \le 200$). The
output verifies a real theorem on its own data — blind spots are
impossible at prime degree (Cauchy: a transitive Galois group of prime
degree contains an $n$-cycle, which is precisely a certificate) — and
rediscovers $x^4+1$ at degree 4. Archetype tables: luckiest/unluckiest
$C(f)$, longest prime runs, violator samples. API: `run_census`,
`render_census_md`.

## Key idea — hypothesis 3 is decidable

The gcd of *all* values of $f$ equals $\gcd(f(0), f(1), \dots, f(\deg f))$
(classical theorem, via the binomial-coefficient basis
$f(x) = \sum_k \Delta^k f(0)\binom{x}{k}$), so "no fixed prime divisor"
needs only $\deg f + 1$ evaluations. Verified against brute-force gcd over
$f(1..200)$ for all demo polynomials.

## Measured results (2026-11-22, Python 3.11.9, this venv)

| Quantity | Value |
|---|---|
| $C(x^2+1)$, Euler product truncated at $p \le 10^4$ | 1.371023 (literature ≈ 1.37281) |
| $x^2+1$ prime values, $n \le 10^5$: empirical / predicted | 6656 / 6601.1 → ratio 1.0083 |
| $x^2+x+41$ ($C \approx 6.67$), $n \le 10^4$: empirical / predicted | 4148 / 4153.6 → ratio ≈ 0.999 |
| Euler $x^2+x+41$ | prime for $n = 0..39$, $f(40) = 1681 = 41^2$, resumes at $n=42$ |
| $2x^2+3x+1 = (2x+1)(x+1)$ | fixed divisor **1**, yet **0** primes for $n \in [2,300]$ |
| $x^2+x+2$ | fixed divisor **2** — all values even |

The Bateman–Horn ratios drifting toward 1.0 as $N$ grows (0.93 → 0.99 →
1.008 over $N = 10^3 \to 10^5$) is the heuristic working — it is real
number theory, not noise.

## Higher degrees (demo sections [5]–[7], all measured 2026-11-22)

| Polynomial | role | fd | cert | primes ≤10⁴ |
|---|---|---|---|---|
| $x^3+2$ | Eisenstein at 2, satisfies | 1 | p=7 | 520 |
| $\Phi_5(x)=x^4{+}x^3{+}x^2{+}x{+}1$ | satisfies; every prime divisor $q = 5$ or $q \equiv 1 \pmod 5$ (78 factors checked, 0 exceptions) | 1 | p=2 | 950 |
| $x^5-x+1$ | satisfies; densest, $C=4.90$ | 1 | p=3 | 1246 |
| $x^3+3x+2$ | irreducible (cert p=5) **but** always even → 0 primes ($n\ge1$) | 2 | p=5 | 0 |
| $x^4+1$ | **certificate blind spot**: irreducible over ℤ, factors mod *every* p (Gal $C_2\times C_2$) → reported `satisfies=False` despite being prime-rich | 1 | none | 790 |
| $x^4-10x^2+1$ | the classic $V_4$ blind spot | 1 | none | 920 |
| $x^3+x^2-x+41$ | "unlucky" contrast: $C=0.44$ vs 4.90 for $x^5-x+1$ — an 11× density gap, both predicted within a few % | 1 | p=5 | 189 |

No single-variate polynomial of degree ≥ 2 has ever been *proved* to
produce infinitely many primes; the proved results nearby
(Friedlander–Iwaniec $x^2+y^4$, Heath-Brown $x^3+2y^3$) are
multivariate and out of this module's scope.

## Caveats

1. **Irreducibility is certified one-way.** `irreducible_certificate`
   proves irreducibility when $f \bmod p$ is irreducible for some
   $p \nmid \mathrm{lc}(f)$, but "not certified" ≠ "reducible": e.g.
   $x^4 - 10x^2 + 1$ is irreducible over $\mathbb{Z}$ yet factors modulo
   *every* prime (Galois group $V_4$), so it would report `satisfies=False`.
2. **Miller–Rabin range.** Bases 2–37 are deterministic below
   $3.3\cdot 10^{24}$; the demo stays far below. For $N > 10^8$ with
   high-degree coefficients, primality is only probabilistically sound.
3. **Constant truncation.** $C(f)$ at $p_{max}=10^4$ is ~0.13% low for
   $x^2+1$; the root-counting product costs $O(p_{max}^2/\ln p_{max})$.

## Changelog

- **1.6.3**: bounded-gaps citations in the twin card and README corrected
  to the published years — Zhang, *Bounded gaps between primes*, Ann. of
  Math. **179** (2014); Maynard, *Small gaps between primes*, Ann. of
  Math. **181** (2015) — replacing the arXiv-era "Zhang 2013,
  Maynard–Tao 2014".
- **1.6.2**: `__version__` attribute from distribution metadata
  (`0.0.0+local` fallback from an uninstalled source tree); exported,
  covered by the API-surface test.
- **1.6.1**: analysis/census on worker threads (window stays responsive);
  clearer "CENSUS → degree height" labels.
- **1.6.0**: optional GUI (`--gui`, `bunyakovsky-gui`).
- **1.5.0**: Hypothesis H tuple mode; landscape census.
- **1.4.0**: decidable-over-ℤ irreducibility; `--poly` teacher mode; safe
  parser.
- **1.3.0**: Markdown reports.
- **1.2.0**: visualization layer (`--plot`/`--movie`/`--stills`).
