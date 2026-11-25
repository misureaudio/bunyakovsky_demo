# Bunyakovsky's conjecture and its interfaces across mathematics — a connections map

*Working notes, v0 (frozen source for the essay) — 2026-11-24.*
Derived from the session discussion of 2026-11-24; feeds the writing plan
`D:/Source/hermes-dir/.hermes/plans/2026-11-24_223058-bunyakovsky-connections-essay.md`.
Measured numbers quoted from this repo's `README.md` (measured 2026-11-22, v1.x).

**Status legend:** **[T]** theorem · **[C]** conditional on H or similar · **[H]** heuristic/model · **[O]** open.

---

## 0. Statement and notation

**Bunyakovsky's conjecture.** If $f \in \mathbb Z[x]$ has positive leading
coefficient, is irreducible over $\mathbb Z$, and has fixed divisor
$\mathrm{fd}(f) := \gcd\{f(n) : n \in \mathbb Z\} = 1$, then $f(n)$ is prime
for infinitely many $n$.

Notation: $\nu_p(f) = \#\{x \bmod p : f(x) \equiv 0 \pmod p\}$; a system
$\{f_1,\dots,f_k\}$ is **admissible** if $\nu_p(\prod_i f_i) < p$ for every
prime $p$. The conjecture is a **local–global statement**: the hypothesis is
purely local (congruential), the conclusion global (infinitude).

The memoir is variously dated 1852 (presentation) / 1854 (French extract) /
1857 (full Russian *Mémoire*); this repo's README uses **1857**. *(Flagged
for the essay citation pass.)*

## 1. Genealogy inside analytic number theory

- **Dirichlet 1837 [T]**: the linear case is a theorem — Bunyakovsky is
  "Dirichlet beyond degree 1".
- **Dickson 1904 [O]**: linear *systems* (prime constellations; twins) =
  Bunyakovsky restricted to linear forms.
- **Landau 1912**: problem on $n^2+1$ — the emblematic quadratic case.
- **Hardy–Littlewood 1923 [O]**: quantitative k-tuples conjecture
  (Conjecture F for $n^2+1$).
- **Schinzel (with Sierpiński) 1958**: **Hypothesis H** — systems of
  polynomials; Bunyakovsky = H for one polynomial.
- **Bateman–Horn 1962 [O]**: quantitative form,
  $\#\{n\le N : f(n)\in\mathbb P\} \sim \frac{C(f)}{\deg f}\frac{N}{\log N}$,
  with singular series $C(f) = \prod_p \frac{1-\nu_p(f)/p}{1-1/p}$;
  Bunyakovsky is its qualitative shadow. The inclusion chain
  Bunyakovsky ⊂ H ⊂ Bateman–Horn (as statement strength inverts).

## 2. Sieve methods and the parity problem

- **Selberg's parity problem**: sieves fed only local (mod-$p$) information
  cannot separate primes from semiprimes — exactly the input Bunyakovsky's
  hypothesis provides. This is *why* the conjecture is open. [T-observation]
- Footholds on this fault line: Brun; **Chen [T]**; **Iwaniec 1978 [T]**:
  infinitely many $n$ with $n^2+1$ a $P_2$; **Greaves 1992 [T]**: cubics hit
  $P_2$ infinitely often.
- Multivariate breakthroughs (two variables supply the bilinear "Type II"
  structure one-variable values lack): **Friedlander–Iwaniec 1998 [T]**
  $a^2+b^4$; **Heath-Brown 2001 [T]** $x^3+2y^3$; **Maynard 2020 [T]**,
  *primes represented by incomplete norm forms* (Forum Math. Pi). No
  single-variate irreducible $f$ of degree $\ge 2$ has ever been proved to
  produce infinitely many primes **[O]**.
- **Zhang 2013 / Maynard–Tao 2014 [T]**: bounded prime gaps use *admissible
  tuples* — Bunyakovsky's local condition verbatim, in linear form.

## 3. Additive combinatorics and Möbius randomness

- **Green–Tao 2004 [T]**: arbitrarily long APs of primes; the proof needs
  Dickson-type linear-forms conditions for the primes.
- **Green–Tao, *Linear equations in primes* (Ann. of Math. 2010) [T]**:
  asymptotic counts of prime solutions to linear systems subject to local
  solubility — the largest proved chunk of Dickson's conjecture.
- Conceptual home: "$f(n)$ prime" means $\mu(f(n)) = -1$, so Bunyakovsky
  asserts the Möbius function does not correlate with polynomial
  compositions — the territory of the **Chowla / Elliott / Sarnak**
  conjectures **[O]**; partial: Green–Tao–Ziegler Möbius–nilsequence
  orthogonality **[T]**, Tao's log-averaged Chowla **[T]**.

## 4. Algebraic number theory: class numbers, Chebotarev, Hilbert

- **Rabinowitsch 1913 [T]**: $n^2+n+A$ prime for $n = 0,\dots,A-2$
  $\Longleftrightarrow$ $\mathbb Q(\sqrt{1-4A})$ has class number one.
  Euler's $n^2+n+41$ $\leftrightarrow$ $\mathbb Q(\sqrt{-163})$; the class
  number one problem (Heegner–Baker–Stark) governs these all-prime initial
  segments, while infinitude stays Bunyakovsky.
- For quadratic $f$ the Bateman–Horn constant is expressible via
  $L(1,\chi_D)$ and the class number $h(D)$ (analytic class number formula)
  **[T]** — the accepted heuristic explanation of prime-rich diagonals in
  the **Ulam spiral [H]**.
- The local factors $\nu_p(f)$ are Chebotarev/Frobenius splitting data;
  **Hilbert irreducibility** is H's "irreducible-values sibling" **[T]**.
- **Pila 2010 (arXiv:1005.4528) [C]**: Hypothesis H used to prove results
  on irreducible values of polynomials with Diophantine-geometry
  applications — H as a working axiom.

## 5. Function fields and geometry

- Over $\mathbb F_q[t]$ (primes = irreducibles): **Pollack 2009 [T]** —
  function-field H holds when $q$ is large compared to the degrees
  (explicit, effective Chebotarev). **Entin (arXiv:1409.0846, Compositio)
  [T]** — full Bateman–Horn asymptotic in the $q\to\infty$ regime; the
  proof **relies on CFSG** (monodromy-group control).
- With $q$ **fixed** even twin irreducibles over $\mathbb F_q[t]$ remain
  open **[O]** — so H escapes methods even where RH is a theorem.
- **Debes–Najman 2019 (arXiv:1902.08155) [T]**: when the ring of integers
  is replaced by a *polynomial ring*, the Schinzel hypothesis becomes a
  theorem for wide classes (transfer phenomenon).
- Geometric reformulation: admissibility = "Frobenius conjugacy classes in
  the splitting tower do not cover the residue fields"; monodromy / étale
  $\pi_1$ formulations (image = full symmetric group; Kowalski's blog note,
  inspired by Katz–Rains). The demo's **blind spots** ($x^4+1$,
  $x^4-10x^2+1$ with Galois groups $C_2\times C_2$, $V_4$) are exactly this
  group-theoretic obstruction made visible in mod-$p$ factorization data.

## 6. Divisibility sequences and arithmetic dynamics

- Prime terms of Lucas sequences / elliptic divisibility sequences **[O]**;
  flagship = Mersenne primes, with the **Lenstra–Pomerance–Wagstaff 1980**
  heuristic **[H]**. Discriminator: $\sum_n 1/\log u_n$ diverges
  (exponential growth ⇒ infinitely many primes predicted) vs. converges
  (doubly exponential orbits ⇒ only finitely many predicted).
- Proven substitute for orbits: **Jones–Levy [T]** — primitive prime
  divisors of quadratic-polynomial orbits have positive density; recent
  work (2023) links primitive divisors in the **critical orbit** to
  periodicity of the orbit under reduction.

## 7. Conditional consequences and applied corners

- **Sierpiński 1960 [C]**: assuming H, an odd $k$ exists with $k2^n+1$
  composite for all $n$; **Selfridge [T]** later gave $k = 78557$
  unconditionally via covering congruences — the mirror image: local
  conditions *conspiring* to kill primality.
- **Amarra–Devillers–Praeger 2021 (arXiv:2105.03915) [C/H]**: block-design
  constructions depending on quadratics taking **prime-power** values
  infinitely often — Bunyakovsky-type hypotheses feeding finite geometry.
- Inverse Galois: Hilbert irreducibility is the workhorse; demanding
  *prime* (not merely irreducible) specialization values brings in H
  **[C]**. *(Phrasing kept generic pending citation pass.)*

## 8. What is achievable algorithmically (worked example: this repo's demo)

The conjecture's logical shape: every ingredient is **computable** except
the infinitude assertion itself. The demo
(`bunyakovsky_demo`, stdlib-only, v1.6.2) is the maximal algorithmic shadow
of an open $\Pi_2$-type statement.

**Decidable / computable fragments**

1. **Fixed divisor [T]**: $\mathrm{fd}(f) = \gcd(f(0),\dots,f(\deg f))$
   (binomial-coefficient basis $f = \sum_k \Delta^k f(0)\binom{x}{k}$) —
   $\deg f + 1$ evaluations. Demo: `check_hypotheses`; verified against
   brute-force gcd over $f(1..200)$.
2. **Irreducibility over $\mathbb Z$ [T]**: decidable
   (Gauss–Zassenhaus; LLL-based in practice). Demo: `analysis.irreducible_z`
   (Yun squarefree + Zassenhaus lifting). The mod-$p$ certificate
   (Rabin) is **one-way**: blind spots $x^4+1$, $x^4-10x^2+1$ factor mod
   *every* $p$ (Galois $C_2\times C_2$, $V_4$) yet are irreducible — no
   mod-$p$ certificate *can* exist, but the full $\mathbb Z$-decision still
   answers.
3. **Hypothesis H admissibility [T]**: an obstructing prime must satisfy
   $p \le \sum_i \deg f_i$ (root count $\nu_p \le \sum \deg < p$) — finite
   exact check. Demo: `tuples.admissible`; decides twins $\{x,x+2\}$ pass,
   rejects $\{x,x+2,x+4\}$.
4. **A theorem visible in the demo's own data [T]**: blind spots are
   impossible at prime degree — Cauchy: a transitive Galois group of prime
   degree contains an $n$-cycle, which *is* a certificate. `census.py`
   verifies this across the enumerated box and rediscovers $x^4+1$ at
   degree 4.
5. **The conjectural constant is computable to any precision**: the
   Bateman–Horn Euler product has a bounded tail. Measured (README):
   $C(x^2+1) = 1.371023$ at $p \le 10^4$ (literature $\approx 1.37281$,
   $-0.13\%$); twins reproduce $2C_2 = 1.32032\ldots$
6. **Empirical validation of the heuristic [H, confirmed by data]**:
   empirical/predicted prime-value ratios $0.9854 \to 1.0083$
   ($N = 10^4 \to 10^5$, $x^2+1$); Euler 41 ratio $\approx 0.999$ at
   $N = 10^4$ with $C \approx 6.67$.
7. **Primality of individual values [T]**: deterministic Miller–Rabin
   (bases 2–37) below $3.3\cdot 10^{24}$; AKS/ECPP in general.

**Beyond what any algorithm currently achieves**

8. **The infinitude decision [O]**: no known procedure decides "does $f$
   take infinitely many prime values?" for a given $f$; not one
   single-variate irreducible $f$ of degree $\ge 2$ has been proved to. The
   demo certifies every decidable fragment and predicts the density — the
   gap it cannot cross *is* the conjecture.
9. **Logical-status caution**: the set of primes is **Diophantine**
   (Jones–Sato–Wada–Wiens 1976 **[T]**), and DPRM makes the existential
   theory of $\mathbb Z$ undecidable; but there is **no theorem** making
   Bunyakovsky-type statements undecidable. Do not claim "proved
   undecidable" — the decision problem is simply out of reach.

**Beyond the demo (adjacent algorithmic landscape)**

10. **Negative side [T]**: covering congruences give unconditional
    compositeness certificates (Sierpiński/Riesel numbers; Selfridge's
    78557) — exponential families, adjacent to but outside Bunyakovsky.
11. **Proved territory [T]**: function fields, $q \to \infty$
    (Pollack; Entin) — where the conjecture is a theorem, algorithms follow
    (effective Chebotarev).
12. **Search infrastructure [H]**: prime-constellation projects run exactly
    the admissibility check of item 3; GIMPS verifies the LPW Mersenne
    predictions statistically.

## 9. The unifying thread

Bunyakovsky is the prototype **local–global statement for primes**: "no
congruence obstruction is the only obstruction." Every interface above is a
lens on why local data fails to force global primality over $\mathbb Z$
(parity; missing bilinear structure; one variable), and where it succeeds
(Dirichlet; many-variable linear systems; function fields with $q$ large;
polynomial rings). The algorithmic shadow (§8) marks precisely where the
computable fragments stop and the conjecture begins.

---

## References

**Verified this session (2026-11-24):**

- Entin, *On the Bateman–Horn conjecture for polynomials over large finite
  fields*, Compositio Math. (arXiv:1409.0846; proof uses CFSG).
- Pollack, *An explicit approach to Hypothesis H for polynomials over a
  finite field* (author PDF at pollack-math.net; venue Proc. AMS ~2009 —
  verify).
- Maynard, *Primes represented by incomplete norm forms*, Forum of
  Mathematics, Pi (2020).
- Pila, *Irreducible values of polynomials* (arXiv:1005.4528).
- Debes–Najman, *The Schinzel hypothesis for polynomials* (arXiv:1902.08155).
- Amarra–Devillers–Praeger, *Block designs and prime values of polynomials*
  (arXiv:2105.03915).
- *Primitive prime divisors in the critical orbit of polynomial dynamics*
  (2023) — author list to confirm in essay pass.

**Flagged for the essay citation pass** (standard attributions; full
bibliographic detail to be verified against authoritative sources):
Bunyakovsky memoir dating (1852/1854/1857); Dickson 1904; Landau 1912;
Hardy–Littlewood 1923; Schinzel–Sierpiński 1958; Bateman–Horn 1962;
Rabinowitsch 1913; Sierpiński 1960; Iwaniec 1978; Friedlander–Iwaniec 1998;
Heath-Brown 2001; Greaves 1992; Green–Tao 2004 & 2010; Jones–Levy;
Lenstra–Pomerance–Wagstaff 1980; Jones–Sato–Wada–Wiens 1976; Zhang 2013;
Maynard–Tao 2014.
