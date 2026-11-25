# Hypothesis H: ($x$, $x + 2$)

**This is the twin-prime conjecture.**

**Verdict: the tuple satisfies Hypothesis H** (each entry irreducible with positive leading coefficient, and the tuple is admissible). Infinitely many all-prime positions are **conjectured**.

| Member | Leading coeff | Irreducible over $\mathbb{Z}$ | Evidence |
|:---|---:|:---:|:---|
| $x$ | 1 | yes | certified mod $p = 2$ |
| $x + 2$ | 1 | yes | certified mod $p = 2$ |

**Admissible** (no prime $p$ with $\nu_p = p$)? yes. Checked exactly: it suffices to test $p \le \sum_i \deg f_i$.

Bateman-Horn constant $C = 1.32049$ ($p \le 1000$).

| $N$ | empirical | predicted | ratio |
|------:|--------:|----------:|------:|
| 1000 | 35 | 44.4 | 0.7891 |
| 10000 | 205 | 212.8 | 0.9633 |

First all-prime positions:

- $n = 3$: $3$, $5$
- $n = 5$: $5$, $7$
- $n = 11$: $11$, $13$
- $n = 17$: $17$, $19$
- $n = 29$: $29$, $31$
- $n = 41$: $41$, $43$
- $n = 59$: $59$, $61$
- $n = 71$: $71$, $73$

## Notes*

- this tuple is {n, n+2}: the TWIN PRIME conjecture -- open. Its Bateman-Horn constant equals 2*C_2 = 1.32032... (the classical twin-prime constant). Best proved result nearby: bounded gaps (Zhang 2013, Maynard-Tao 2014).

- all-prime values for infinitely many n is CONJECTURAL (Hypothesis H) whenever at least one degree >= 1 member is involved; the count column is the Bateman-Horn prediction, not a theorem.

## Census of small polynomials (degree $\le 4$, height $\le 2$)

**1440 primitive polynomials** classified against Bunyakovsky's conjecture with the DECIDABLE irreducibility test (Zassenhaus). Categories overlap: a polynomial can fail both 2 and 3.

| class | count | share |
|:---|---:|---:|
| satisfies all three hypotheses | 738 | 51.2% |
| fails 2: reducible over $\mathbb{Z}$ | 576 | 40.0% |
| fails 3: fixed divisor $> 1$ | 368 | 25.6% |
| blind spots (satisfy, yet no mod-$p$ certificate for $p \le 200$) | 14 | 1.0% |

## By degree

| degree | total | satisfies | blind spots |
|---:|---:|---:|---:|
| 1 | 7 | 7 | 0 |
| 2 | 41 | 25 | 0 |
| 3 | 223 | 120 | 0 |
| 4 | 1169 | 586 | 14 |

## Archetypes

**Luckiest — highest $C(f)$** (among satisfying, $C$ truncated at $p \le 200$):

| $f(x)$ | $C(f)$ | primes ($n \le 300$) |
|:---|---:|---:|
| $x^{4} + x^{3} - 2x - 1$ | 5.1225 | 88 |
| $x^{4} + 2x^{3} - x - 1$ | 5.1225 | 81 |
| $x^{4} - 2x^{3} + x - 1$ | 5.1225 | 81 |

**Unluckiest — lowest $C(f)$** (among satisfying, $C$ truncated at $p \le 200$):

| $f(x)$ | $C(f)$ | primes ($n \le 300$) |
|:---|---:|---:|
| $2x^{4} - x^{2} + 2$ | 0.6155 | 10 |
| $x^{4} + 2x^{3} - 2x + 2$ | 0.6339 | 12 |
| $x^{4} - 2x^{3} + 2x + 2$ | 0.6339 | 12 |

**Longest runs of consecutive prime values**:

| $f(x)$ | run | where |
|:---|---:|:---|
| $x^{4} + x^{3} - 2x - 1$ | 7 | $n = 2, \dots, 8$ |
| $2x^{3} + x^{2} - x - 1$ | 6 | $n = 2, \dots, 7$ |
| $x^{4} - x^{2} - 1$ | 6 | $n = 2, \dots, 7$ |

**Blind spots found** (irreducible over $\mathbb{Z}$, yet the factorization pattern mod $p$ is never the single pattern $(d)$ for any prime $p \le 200$ — no certificate can exist, the Galois group has no full cycle):

| $f(x)$ | degree | primes ($n \le 300$) |
|:---|---:|---:|
| $x^{4} + 2x^{3} + 2x^{2} - 2x + 1$ | 4 | 40 |
| $x^{4} + x^{3} + 2x^{2} - x + 1$ | 4 | 41 |
| $x^{4} - x^{2} + 1$ | 4 | 65 |
| $x^{4} + 1$ | 4 | 44 |
| $x^{4} - x^{3} + 2x^{2} + x + 1$ | 4 | 44 |
| $x^{4} - 2x^{3} + 2x^{2} + 2x + 1$ | 4 | 45 |
| $x^{4} - 2x^{3} + 2x^{2} + 2$ | 4 | 22 |
| $x^{4} + 2x^{3} + 2x^{2} + 2$ | 4 | 23 |
| $2x^{4} + 2x^{2} - 2x + 1$ | 4 | 35 |
| $2x^{4} + 2x^{2} + 2x + 1$ | 4 | 34 |
| $2x^{4} - 2x^{3} + x^{2} - 2x + 2$ | 4 | 25 |
| $2x^{4} - x^{2} + 2$ | 4 | 10 |
| $2x^{4} + x^{2} + 2$ | 4 | 26 |
| $2x^{4} + 2x^{3} + x^{2} + 2x + 2$ | 4 | 35 |

**Fixed-divisor violators** (sample): $x^{2} - x - 2$ ($2$), $x^{2} + x - 2$ ($2$), $x^{2} - x$ ($2$), $x^{2} + x$ ($2$), $x^{2} - x + 2$ ($2$).

## Notes**

- $C(f)$ is truncated at small $p_{max}$ for speed: use the values for *ranking*, not as published constants.
- Degree 1 with $\gcd = 1$ always satisfies (Dirichlet: proved); degrees $\ge 2$ satisfy = conjecture.
- Blind spots are possible only at COMPOSITE degree (Cauchy: a transitive Galois group of prime degree contains an $n$-cycle, which is exactly a certificate). The by-degree table should show 0 at degrees 2 and 3.
