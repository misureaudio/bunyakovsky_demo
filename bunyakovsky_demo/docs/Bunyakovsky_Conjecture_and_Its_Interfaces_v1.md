# Bunyakovsky's Conjecture and Its Interfaces Across Mathematics

*v1 — 2026-11-24. Derived from the frozen connections map `Bunyakovsky_Connections_Map_2026-11.md`; all computational claims re-measured 2026-11-24 with `bunyakovsky_demo` v1.6.2. The citation audit trail lives in the companion Verification Note.*

**Status tags used throughout:** **[T]** theorem · **[C]** conditional on Hypothesis H or a comparable hypothesis · **[H]** heuristic or predictive model · **[O]** open.

**Abstract.** Bunyakovsky's conjecture (1857) asserts that every irreducible integer polynomial with positive leading coefficient and no fixed prime divisor assumes prime values infinitely often. It is the prototype of a *local–global statement for primes*: the hypothesis is a family of congruence conditions, the conclusion is an infinitude, and nothing else is assumed. This essay maps the conjecture's interfaces with other areas of mathematics — the genealogy inside analytic number theory (Dickson, Landau, Hardy–Littlewood, Schinzel, Bateman–Horn), sieve methods and the parity barrier, additive combinatorics and Möbius randomness, class field theory and the class number one problem, function fields and permutation-group geometry, arithmetic dynamics, and logic — and lands on an algorithmic question: which fragments of the conjecture are decidable, and exactly where does computation stop? That boundary is worked out concretely on a small open-source demo (the `bunyakovsky_demo` package), which certifies every decidable ingredient of the conjecture, predicts the density of prime values to within a few percent, and cannot cross the one step that remains open. The intended reader is a mathematically mature mathematician who does not work in analytic number theory.

---

## 1. The simplest open problem about primes

**Conjecture (Bunyakovsky, 1857).** *Let $f \in \mathbb{Z}[x]$ have positive leading coefficient, be irreducible over $\mathbb{Z}$, and have no fixed prime divisor, i.e.*

$$\mathrm{fd}(f) := \gcd\{\, f(n) : n \in \mathbb{Z} \,\} = 1 .$$

*Then $f(n)$ is prime for infinitely many integers $n$.* [O]

Each hypothesis is necessary. Irreducibility: a composite $f = gh$ takes prime values only where one factor is $\pm 1$. Fixed divisor: $f(n) = n^2 + n + 2$ is always even, so the best it can do is finitely many primes. The condition $\mathrm{fd}(f) = 1$ has an equivalent local form: for every prime $p$, writing

$$\nu_p(f) := \#\{\, x \bmod p : f(x) \equiv 0 \pmod p \,\},$$

we require $\nu_p(f) < p$ — some residue class mod $p$ avoids all roots. The emblematic open case is $f(n) = n^2 + 1$ (Landau's first problem of 1912): the roots of $x^2 + 1$ mod $p$ exist only for $p = 2$ and $p \equiv 1 \pmod 4$, so $\nu_p \le 2 < p$ for all large $p$, the local test passes everywhere — and infinitude is unknown. **No single-variate irreducible polynomial of degree $\ge 2$ has ever been proved to take infinitely many prime values** [O].

The logical shape deserves emphasis, because it organizes everything below. The hypothesis is *local*: it is a statement about the reductions $f \bmod p$ for every prime $p$. The conclusion is *global*: an infinitude over $\mathbb{Z}$. Bunyakovsky's conjecture is thus the prototype of a **local–global principle for primes** — "the congruence obstructions are the only obstructions" — and every interface surveyed here is a lens on one question: *why doesn't local data force prime values, and where does it manage to anyway?*

A dating caution for the unwary. The conjecture is conventionally attributed to Viktor Bunyakovsky's memoir of **1857** (the French Wikipedia dates the relevant work 1854; several secondary sources print 1852, which is actually the year of Chebyshev's *Mémoire sur les nombres premiers* [Chebyshev 1852, J. Math. Pures Appl. 17, 366–390]). Jones and Zvonkin [Jones–Zvonkin 2023, fn. 5] warn that a title long attached to the conjecture in the literature ("Nouveaux théorèmes relatifs à la distinction des nombres premiers…") belongs to a different, earlier paper (1840) that does not discuss the conjecture. We follow the 1857 convention.

## 2. Genealogy: a family tree with a proved root

The conjecture sits inside a nested family of statements about prime values of polynomial systems, whose inclusion chain is worth fixing once:

$$\text{Bunyakovsky} \;\subset\; \text{Hypothesis H} \;\subset\; \text{Bateman--Horn}$$

in the sense that each later statement implies the earlier ones and adds quantitative or structural content.

**Dirichlet (1837) [T]** is the proved root: for coprime $a, q$, the progression $a + qn$ contains infinitely many primes — exactly Bunyakovsky's conjecture for linear $f$, where $\nu_p \le 1 < p$ reduces the hypothesis to $\gcd(a, q) = 1$. Bunyakovsky's conjecture is "Dirichlet beyond degree one", and the gap between degree 1 and degree 2 is the gap between a classical theorem and 170 years of failure.

**Dickson (1904) [O]** treats *systems* of linear forms: if $\{a_i n + b_i\}$ has no fixed prime divisor, infinitely many $n$ make all of them prime simultaneously — prime constellations; the pair $\{n, n+2\}$ is the twin prime conjecture. Dickson's conjecture is Bunyakovsky restricted to linear polynomials but extended to $k > 1$ (Pintz's survey [Pintz 2009] lays out the attributions precisely).

**Landau (1912)** listed four problems on primes at the Cambridge International Congress as "unattackable at the present state of science"; the first is $n^2 + 1$, the simplest case of the conjecture with $\deg f > 1$ [Pintz 2009].

**Hardy–Littlewood (1923) [O]** supplied the first *quantitative* conjectures for prime $k$-tuples (their Conjecture F predicts the count of primes $n^2 + 1$ below $x$) [Hardy–Littlewood 1923].

**Schinzel and Sierpiński (1958) [O]** formulated **Hypothesis H**: for irreducible $f_1, \dots, f_k \in \mathbb{Z}[x]$ whose product has no fixed prime divisor and which are positive for large $n$, infinitely many $n$ make *all* $f_i(n)$ prime [Schinzel–Sierpiński 1958]. Bunyakovsky is Hypothesis H with $k = 1$.

**Bateman and Horn (1962) [O]** gave the full quantitative form. For a single polynomial,

$$\pi_f(N) := \#\{\, n \le N : f(n) \in \mathbb{P} \,\} \;\sim\; \frac{C(f)}{\deg f}\,\mathrm{Li}(N), \qquad C(f) := \prod_p \frac{1 - \nu_p(f)/p}{(1 - 1/p)^{\deg f}},$$

with $\mathrm{Li}(N) = \int_2^N dt/\log t$ [Bateman–Horn 1962]. The Euler product $C(f)$ — the *singular series* — is assembled from the same local data $\nu_p(f)$ that appear in the conjecture's hypothesis; Bunyakovsky's conjecture is its qualitative shadow ($C(f) > 0$ and the right side diverges). The constant is a genuine predictor, not a formal device: §8 measures $C(x^2+1) = 1.3710$ and $C(x^2+x+41) = 6.6561$ directly from truncated Euler products, and the empirical prime counts follow them to within fractions of a percent. The survey [Aletheia-Zomlefer–Fukshansky–Garcia 2020] covers the heuristics and history of Bateman–Horn in depth.

## 3. Why local data cannot finish the job: the parity barrier

If the hypothesis is a complete list of congruence obstructions, why can't we just sieve them away and count? This is where the deepest structural fact about the problem lives.

The classical sieve of Eratosthenes, in every refined form (Brun, Selberg, linear and combinatorial sieves), operates by *inclusion–exclusion over residue classes* — that is, its input is exactly the local data $\nu_p(f)$, the same data that form the conjecture's hypothesis. Selberg's **parity problem** [T] says this is fatal: any sieve argument that uses only the distribution of the sequence $\{f(n)\}$ among residue classes cannot distinguish integers with an even number of prime factors from integers with an odd number of them. Concretely, the sieve cannot tell primes (one prime factor, odd parity) from semiprimes (two prime factors, even parity); it sees both as "not eliminated by small primes". The best unconditional sieve results therefore stop at *almost primes* — values with boundedly many prime factors — no matter how clever the weights (§4). Maynard's ICM survey [Maynard 2022] frames the parity phenomenon and its avatars (Siegel zeroes, the limits of the Bombieri–Vinogradov theorem) as the central obstacle in the theory of prime counting.

This gives the honest answer to "why is Bunyakovsky open": the conjecture's hypothesis is precisely the information that sieves can read, and it has been proved (parity) that this information is not sufficient. Any proof must import *non-sieve* structure — global analytic input (as for Dirichlet's theorem, where characters of $\mathbb{Z}/q\mathbb{Z}$ supply more than congruence counting), bilinear structure (as for the multivariate theorems of §4), or something new.

There is also a mirror-image phenomenon showing how *conspiracies* of local data can kill primality rather than merely fail to certify it. Sierpiński proved unconditionally that a positive proportion of odd integers $k$ have $k \cdot 2^n + 1$ composite for every $n$: a finite *covering system* of congruences on $n$ (moduli $2, 4, 8, \dots, 64$) paired with the seven primes $3, 5, 17, 257, 641, 65537, 6700417$ and the Chinese remainder theorem produces $k \equiv 15511380746462593381$ with every value forced composite [Sierpiński 1960]; Selfridge found in 1962 the smallest known example, $k = 78557$, covered by $\{3, 5, 7, 13, 19, 37, 73\}$. These are exponential families, adjacent to but outside Bunyakovsky's polynomial world — but they demonstrate that "no local obstruction" is a far weaker condition than a heuristic reader might guess, since finitely many local obstructions can be *arranged* to cover every index.

## 4. Proven footholds

What *is* known falls into four families, each showing exactly how much non-local input buys.

**(a) Almost primes: the ladder of $P_r$.** For irreducible $f$ with $\mathrm{fd}(f) = 1$, let $p(f)$ be the least $r$ such that $f(n)$ has at most $r$ prime factors for infinitely many $n$. Pintz's survey [Pintz 2009, §19] records the classical ladder: Rademacher (1924) proved $p(f) \le 4\deg f - 1$; Ricci (1936) $3\deg f - 1$; Kuhn (1953/54) $\deg f + c\log\deg f$; **Buchstab (1967) $p(f) \le \deg f + 1$** [T]. So every admissible polynomial is known to produce *almost primes of optimal order* infinitely often — and the parity barrier is what prevents the final $-1$. For the emblematic quadratic, **Iwaniec (1978) [T]**: infinitely many $n$ with $n^2 + 1$ a $P_2$ (a prime or semiprime), via the half-dimensional sieve [Iwaniec 1978]. In an adjacent direction, **Chen (1973) [T]**: every sufficiently large even integer is $p + m$ with $m$ a prime or semiprime [Chen 1973] — the same "one factor short" signature.

**(b) Multivariate polynomials: bilinear structure breaks parity.** When the polynomial has several variables, the extra variables supply "Type II" bilinear sums that sieve weights can exploit, and genuine primes become reachable: **Friedlander–Iwaniec (1998) [T]**: infinitely many primes of the shape $a^2 + b^4$ [Friedlander–Iwaniec 1998]; **Heath-Brown (2001) [T]**: infinitely many primes $x^3 + 2y^3$ [Heath-Brown 2001]; **Maynard (2020) [T]**: primes represented by incomplete norm forms in sufficiently many variables [Maynard 2020]. The contrast is the sharpest available statement of the one-variable obstruction: two variables suffice for primes, one variable has defeated everyone.

**(c) Linear systems: the largest proved chunk of Dickson's conjecture.** **Green–Tao (2008) [T]**: the primes contain arbitrarily long arithmetic progressions [Green–Tao 2008]. Their technology matured into **Green–Tao, *Linear equations in primes* [T]**: an asymptotic count of prime solutions to any *finite-complexity* system of linear equations, subject only to the local (Dickson-type) solubility conditions — proved in Annals in 2010 unconditionally for systems of complexity $s \le 2$, and conditional on two then-conjectural ingredients, $(\mathrm{GI}(s))$ and $(\mathrm{MN}(s))$, in general [Green–Tao 2010]. The Möbius–nilsequence orthogonality $\mathrm{MN}(s)$ for all $s$ was settled by **Green–Tao (2012) [T]**, described in the paper's own abstract as "one of two major ingredients" of the generalized Hardy–Littlewood programme [Green–Tao 2012]. Conceptually: for *linear* polynomials in *many* variables, local data really do control prime patterns.

The conceptual home of this programme is **Möbius randomness**. "$f(n)$ is prime" is (up to the usual weighting) the assertion $\mu(f(n)) = -1$; Bunyakovsky-type conjectures predict that the Möbius function does not correlate with polynomial compositions. That prediction is the territory of the Chowla, Elliott and Sarnak conjectures [O]. Partial results exist and are suggestive about the parity barrier's porosity: **Tao (2016) [T]** proved the *logarithmically averaged* two-point Chowla conjecture, explicitly "breaking the parity barrier for this problem" [Tao 2016] — while the un-averaged conjecture, and anything as strong as Bunyakovsky, remain open.

**(d) Bounded gaps: the local condition as working tool.** **Zhang (2014) [T]**: $\liminf (p_{n+1} - p_n) < 7 \times 10^7$ [Zhang 2014]; **Maynard (2015) [T]**: the same with $600$, and $\liminf (p_{n+m} - p_n) < \infty$ for every $m$ [Maynard 2015]. Both theorems are theorems about **admissible tuples** $\mathcal{H} = \{h_1, \dots, h_k\}$ — sets for which $\nu_p(\prod_i (x + h_i)) < p$ for every $p$, i.e., Bunyakovsky's local condition verbatim, in Dickson's linear form. The prime $k$-tuples conjecture asserts every admissible tuple is hit infinitely often; Zhang and Maynard proved that admissible tuples of large enough size contain *two* offsets hit infinitely often. The conjecture's hypothesis, in other words, is not just an obstacle description — it is the exact admissibility criterion that the strongest unconditional results of the last decade are stated in.

## 5. Algebraic number theory: class numbers and Chebotarev data

The local invariants of a quadratic polynomial are splitting data, and the global invariants of the corresponding quadratic field enter at every turn.

Let $f(n) = n^2 + n + A$ with discriminant $D = 1 - 4A < 0$. For odd $p \nmid D$ the root count is exactly

$$\nu_p(f) = 1 + \left(\frac{D}{p}\right),$$

so $\nu_p = 0$ means $p$ is *inert* in $\mathbb{Q}(\sqrt{D})$, $\nu_p = 2$ means it *splits*: the Euler factors of $C(f)$ are Kronecker symbols, i.e. Frobenius/Chebotarev data for the quadratic extension, and $C(f)$ is the Euler product of a Dirichlet $L$-function-flavoured object at $s = 1$. The analytic class number formula $L(1, \chi_D) = 2\pi h(D) / (w \sqrt{|D|})$ then ties the Bateman–Horn constant to the class number $h(D)$ — with the caveat, visible in the data, that $C(f)$ is not *only* $L(1,\chi_D)$: the demo measures $C(x^2+1) = 1.3710$ ($D = -4$, $h = 1$) and $C(x^2+x+41) = 6.6561$ ($D = -163$, $h = 1$), so the same class number can sit under constants five times apart; the size of $C(f)$ is governed by the accumulated local factors, of which the class-number term is one component. This is the accepted heuristic explanation of *prime-rich* quadratic polynomials and of the prime-rich diagonals of the Ulam spiral [H]: large singular series, computed from class-field data, means more primes per value.

The hard theorem in this neighborhood is **Rabinowitsch (1913) [T]**: for $A \ge 2$, the polynomial $n^2 + n + A$ is prime for *all* $n = 0, 1, \dots, A-2$ if and only if $\mathbb{Q}(\sqrt{1-4A})$ has class number one [Rabinowitsch 1913; see Cox 2022]. With the Heegner–Baker–Stark classification of class-number-one imaginary quadratic fields (nine discriminants, the largest being $-163$), this converts Euler's celebrated $n^2 + n + 41$ — prime for $n = 0, \dots, 39$ — into a statement about $\mathbb{Q}(\sqrt{-163})$, and shows the "all-prime initial segments" phenomenon is *exactly classified*, while the infinitude of prime values of the same polynomial remains Bunyakovsky [O]. The demo makes the mechanism visible: for $x^2 + x + 41$ the table of $\omega_f(p)$ (= the $\nu_p$ above) is $0$ for all $p = 2, 3, \dots, 19$ — every small prime is inert in $\mathbb{Q}(\sqrt{-163})$, every inert prime multiplies the singular series up, and the resulting $C = 6.6561$ predicts the measured prime density to within a quarter percent (§8).

Two further connections. **Hilbert's irreducibility theorem [T]** is Hypothesis H's "irreducible-values sibling": it guarantees that irreducible $f(x, t) \in \mathbb{Q}(t)[x]$ stays irreducible for infinitely many integer $t$ — the same phenomenon ("generic local behaviour persists globally") with *irreducibility* replacing *primality*, and it is proved, via Hilbertianity, where the prime version fails. And in the inverse Galois programme, demanding that specialization values generate *prime* ideals (not merely irreducible polynomials) is exactly where Hypothesis H is invoked as a working hypothesis [C] — see [Jones–Zvonkin 2023] for the interface of Bunyakovsky-type hypotheses with permutation groups and designs (§6).

## 6. Function fields and geometry: where the conjecture is a theorem

Replace $\mathbb{Z}$ by $\mathbb{F}_q[t]$ and "prime" by "monic irreducible". The prime number theorem for function fields is classical and exact (counts are $q^n/n$ with square-root error, a theorem — the Riemann hypothesis for curves over finite fields, Weil/Deligne). What does Bunyakovsky/H look like there?

**As $q \to \infty$ with degrees fixed, H is a theorem.** **Pollack (2008) [T]** gave an explicit, effective proof of function-field Hypothesis H for large $q$ via effective Chebotarev [Pollack 2008], together with the twin-irreducible analogue [Pollack 2008b] and simultaneous prime specializations [Pollack 2008c]. **Entin (2016) [T]** established the *full Bateman–Horn asymptotic* over $\mathbb{F}_q[t]$ in the large-$q$ regime [Entin 2016]; the proof runs through the monodromy groups of the families $f(x) - t$ and needs permutation-group input about fixed-point-free elements (a point of the reduction we flag in the Verification Note, since we confirmed the theorem and venue but not the classification-theorem dependence from the primary text). **Bary-Soroker (2012) [T]** proves a quantitative arithmetic analogue of Hypothesis H for polynomial rings over pseudo-algebraically-closed fields, transferring to large finite fields by model theory, via a Hilbert-irreducibility-type theorem [Bary-Soroker 2012].

**With $q$ fixed, the conjecture is open** — even the existence of infinitely many pairs $P, P + 1$ of irreducibles in $\mathbb{F}_2[t]$ is unknown [O]. This is a philosophically important datum: over $\mathbb{F}_q[t]$ the Riemann hypothesis is a theorem, every Dirichlet analogue is known with exact error terms — and the twin-prime analogue still escapes. RH is not the missing input; the parity barrier lives deeper.

**When $\mathbb{Z}$ is replaced by a polynomial ring, H becomes a theorem.** **Bodin–Dèbes–Najib (2020) [T]** prove the Schinzel hypothesis when the base ring of integers is replaced by a polynomial ring — for polynomials in at least one variable over $\mathbb{Z}$, and in several variables over an arbitrary field, among other classes [Bodin–Dèbes–Najib 2020]. Adding a free variable converts the conjecture into a theorem: the same "extra variable" phenomenon that powers Friedlander–Iwaniec-type results, in algebraic dress.

The **geometric reformulation** makes the permutation-group content explicit. The conditions $\nu_p(\prod f_i) < p$ say that no Frobenius conjugacy class in the splitting tower of $\prod f_i$ covers all residue classes — an assertion about how the arithmetic monodromy group $G \le S_d$ acts: Bunyakovsky-type behaviour requires that for every $p$, some element of the relevant Frobenius set is fixed-point-free. The failure modes are group-theoretic, and the demo exhibits them: $x^4 + 1$ and $x^4 - 10x^2 + 1$ are irreducible over $\mathbb{Z}$ yet factor mod *every* prime, because their Galois groups ($C_2 \times C_2$ and $V_4$) have no element acting as a 4-cycle — every Frobenius has a fixed point, so no mod-$p$ root-avoidance certificate can exist, while the polynomials remain irreducible [T]. This is the same dictionary used in **Jones–Zvonkin (2023)**: building on Amarra–Devillers–Praeger's block-design construction that requires certain quadratics (e.g. $f_{2,3}(t) = 32t^2 + 20t + 1$) to take prime-power values infinitely often — which Bunyakovsky would guarantee [C] — they compute $C(f_{2,3}) = 4.721240276\ldots$, about $10.7$ times the twin-prime constant, and verify large numbers of prime values against Li's refinement of Bateman–Horn, "strong evidence" (their phrase) for both conjectures [Jones–Zvonkin 2023].

## 7. Divisibility sequences and arithmetic dynamics

Bunyakovsky's question — "does this explicit sequence contain infinitely many primes?" — has exponential cousins where the answer is conjectured differently.

**Mersenne primes.** $2^p - 1$ is prime for $p = 2, 3, 5, 7, 13, 17, 19, 31, \dots$; infinitude is open [O]. Because $\log(2^p - 1) \sim p \log 2$, a naive prime-density heuristic gives $\sum_p 1 / \log(2^p) = \infty$, and the refined **Lenstra–Pomerance–Wagstaff heuristic [H]** predicts $\#\{p : 2^p - 1 < x \text{ Mersenne prime}\} \sim e^{\gamma} \log_2 \log_2 x$ (Wagstaff's published formulation of the prediction, with the correction factor for the $2p \pm 1$ structure of Mersenne divisors) [Wagstaff 1983]. The divergence test is the right general discriminator for divisibility sequences $(u_n)$: if $\sum_n 1/\log u_n$ diverges (exponential growth), infinitely many primes are predicted; if it converges (doubly exponential growth, as in orbits $u_{n} = f^{\circ n}(a)$ of degree-$\ge 2$ polynomials), only finitely many primes are predicted [H]. Infinitude of Fibonacci primes, of Mersenne primes, of prime terms of general Lucas or elliptic divisibility sequences: all open [O].

**What is proved for orbits** substitutes *primitive divisors* for primes. **Ingram–Silverman (2009) [T]**: every non-degenerate orbit of a polynomial of degree $d \ge 2$ over a number field has a *primitive prime divisor* — a prime dividing $f^{\circ n}(a)$ that divides no earlier term — for all but boundedly many $n$ [Ingram–Silverman 2009]. **Jones (2008) [T]**, on the other hand, proves that for four infinite families of quadratic polynomials (including $x^2 + k$, $k \in \mathbb{Z} \setminus \{-1\}$), the set of primes ever dividing a given orbit has *density zero* among all primes [Jones 2008] — the orbit sees almost no primes, yet always finds primitive ones. It is conjectured (in work of Jones and Levy, as reported in the subsequent dynamics literature) that the orbit prime-divisor set always has density $< 1$. The moral for Bunyakovsky: orbits are the *anti*-Bunyakovsky regime — so much composite structure that primality is predicted to be finite — and the primitive-divisor theorems are exactly the kind of statement that survives parity.

## 8. The algorithmic shadow: what decidability reaches

The conjecture's ingredients are, almost all of them, *computable*:

1. **Fixed divisor [T].** $\mathrm{fd}(f) = \gcd(f(0), f(1), \dots, f(\deg f))$: in the binomial-coefficient basis $f = \sum_k \Delta^k f(0) \binom{x}{k}$ every value is an integer combination of $f(0), \dots, f(\deg f)$, so $\deg f + 1$ evaluations decide the third hypothesis. The demo's `check_hypotheses` implements this and was validated against a brute-force gcd over $f(1), \dots, f(200)$.
2. **Irreducibility over $\mathbb{Z}$ [T].** Decidable (Gauss–Zassenhaus; LLL-based variants in practice). The demo's `analysis.irreducible_z` (Yun squarefree decomposition + Zassenhaus lifting) answers *yes/no with proof*, which matters because the cheap certificate — "irreducible mod $p$" — is **one-way**: the blind spots $x^4+1$, $x^4 - 10x^2 + 1$ (§6) are irreducible yet reducible mod every prime. "Not certified" never means "reducible"; only the full $\mathbb{Z}$-decision closes the gap.
3. **Admissibility [T].** An obstructing prime for $\{f_1, \dots, f_k\}$ must satisfy $p \le \sum_i \deg f_i$, since $\nu_p \le \sum_i \deg f_i < p$ otherwise — a finite exact check. The demo's `tuples` mode decides $\{x, x+2\}$ admissible and rejects $\{x, x+2, x+4\}$ (the latter has $\nu_3 = 3$).
4. **A theorem visible in the demo's own data [T].** Blind spots are impossible at prime degree: by a theorem of Cauchy, a transitive permutation group of prime degree contains an $n$-cycle, which yields a mod-$p$ irreducibility certificate. The demo's `census` mode verifies this across its enumerated box of small polynomials and rediscovers $x^4 + 1$ as the minimal blind spot at degree 4.
5. **The conjectural constant [T to compute].** $C(f)$ is an Euler product with bounded tail: truncating at $p \le 10^4$ leaves a provable error. Measured 2026-11-24 with v1.6.2: $C(x^2+1) = 1.3710$ (literature $1.37281$; $-0.13$ percent truncation bias), $C(x^2+x+41) = 6.6561$, twins $C = 1.32049$ at $p \le 10^3$ against the classical twin-prime constant $2C_2 = 1.32032\ldots$ (the fourth decimal differs because the twin card truncates at $10^3$).
6. **Empirical validation [H, confirmed].** With the demo's normalization $\pi_f(N) \approx C(f)\,\mathrm{Li}(N)/\deg f$:

| $f$ | $N$ | empirical | predicted | ratio |
|:---|---:|---:|---:|---:|
| $x^2+1$ | $10^3$ | 112 | 120.9 | 0.9261 |
| $x^2+1$ | $10^4$ | 841 | 853.4 | 0.9854 |
| $x^2+1$ | $2\cdot 10^4$ | 1559 | 1568.1 | 0.9942 |
| $x^2+x+41$ | $10^3$ | 581 | 581.6 | 0.9990 |
| $x^2+x+41$ | $10^4$ | 4148 | 4137.6 | 1.0025 |
| $x^2+x+41$ | $2\cdot 10^4$ | 7619 | 7607.0 | 1.0016 |
| twins $\{x, x+2\}$ | $10^4$ | 205 | 212.8 | 0.9633 |
| twins $\{x, x+2\}$ | $2\cdot 10^4$ | 342 | 356.4 | 0.9595 |

*How to read the table:* the ratio is empirical count divided by Bateman–Horn prediction; values drifting toward $1.0$ (and fluctuating within a few percent, as the twins do) are what "the heuristic is right" looks like at computable heights — the ratios are evidence for Bateman–Horn [H], exactly the reading Jones–Zvonkin give their much larger counts. The Euler $x^2 + x + 41$ track hugs its prediction better than $x^2+1$ does at the same $N$: its values are larger ($\approx n^2$ shifted), the singular series is $4.9$ times larger, and the longest all-prime initial run visible in the demo is $n = 1, \dots, 39$, ending at $f(40) = 1681 = 41^2$ — the Rabinowitsch boundary of §5.
7. **Primality of individual values [T].** Deterministic Miller–Rabin (bases $2$–$37$) below $3.3 \cdot 10^{24}$; AKS or ECPP beyond. Every value the demo labels is proved prime within the displayed range.

**What no algorithm achieves.** 8. There is **no procedure known** that decides, for a given admissible irreducible $f$, whether $f$ takes infinitely many prime values [O] — the infinitude step of the conjecture is not known to be decidable *or* undecidable. 9. A caution against a tempting non-sequitur: the set of primes is **Diophantine** — Jones, Sato, Wada and Wiens exhibited a polynomial in 26 variables whose positive values are exactly the primes [Jones–Sato–Wada–Wiens 1976] — and DPRM makes the existential theory of $\mathbb{Z}$ undecidable. But definability of the primes yields **no theorem** that Bunyakovsky-type statements are undecidable; the decision problem simply sits out of reach in both directions, and the honest statement is that the demo certifies every fragment that *is* decidable and stops exactly where the conjecture begins.

Around the demo, the adjacent algorithmic landscape is three-fold. **Negative certificates** exist: covering congruences prove *compositeness for all $n$* in exponential families (Sierpiński 1960; Selfridge's $78557$; the Seventeen-or-Bust programme searches for primes $k \cdot 2^n + 1$ to eliminate the remaining candidates $k < 78557$) — the negative side of the local–global dictionary is fully algorithmic. **Proved territory** comes with algorithms: in the large-$q$ function-field regime (Pollack; Entin) the conjecture is a theorem and its proof is effective (effective Chebotarev). And **search infrastructure** — prime-constellation projects — runs exactly the admissibility check of item 3 at industrial scale. The demo is the maximal elementary instance of the same shadow: complete decidability up to the boundary, a computable prediction across it, and nothing beyond.

## 9. Synthesis: where local forces global

Assemble the map of §4–§6. Local data **do** force prime values: for degree 1 over $\mathbb{Z}$ (Dirichlet); for all systems of linear forms in many variables (Green–Tao, at complexity $\le 2$ outright and thereafter with the nilsequence ingredients settled in [Green–Tao 2012]); for one- and many-variable polynomials over $\mathbb{F}_q[t]$ with $q$ large (Pollack; Entin); for polynomial rings replacing rings of integers (Bodin–Dèbes–Najib). Local data **do not** (so far) force prime values: for one variable over $\mathbb{Z}$ of degree $\ge 2$ (Bunyakovsky, open); for any fixed $q$ over $\mathbb{F}_q[t]$ (even twins, open). The frontier is not arithmetic complexity but *dimension and supply of structure*: one variable over $\mathbb{Z}$ is exactly the place where sieves see everything there is to see and parity forbids finishing.

Three open questions mark the interfaces most productively. (i) Is there *any* irreducible $f \in \mathbb{Z}[x]$ with $\deg f \ge 2$, $\mathrm{fd}(f) = 1$ whose prime values can be proved infinite — say $n^2 + 1$ — and what non-sieve input would buy the last step? (ii) Are there infinitely many twin irreducibles in $\mathbb{F}_2[t]$ — a question with RH already in hand, isolating parity from all analytic darkness? (iii) Does the Möbius randomness philosophy (Chowla–Elliott–Sarnak), whose logarithmically-averaged forms Tao proved by breaking parity, extend far enough to imply Bateman–Horn-type statements for polynomials?

Bunyakovsky's conjecture endures as the smallest fully explicit counterexample to the local–global dream for primes: every ingredient computable except the assertion, every obstruction named except the one that matters. The algorithmic shadow — decidable hypotheses, certifiable blind spots, a computable constant, densities confirmed to a fraction of a percent — is not a consolation prize; it is the precise shape of the open problem, visible in miniature in a few hundred lines of stdlib Python.

---

## References

*(Accessed/verified 2026-11-24; section cross-references in parentheses. Full audit log: companion Verification Note.)*

- [Aletheia-Zomlefer–Fukshansky–Garcia 2020] N. Aletheia-Zomlefer, E. Fukshansky, R. Garcia, *The Bateman–Horn conjecture: heuristics, history, and applications*, Expositiones Mathematicae 38 (2020), 430–479; arXiv:1807.08899. (§2)
- [Bateman–Horn 1962] P. T. Bateman, R. A. Horn, *A heuristic asymptotic formula concerning the distribution of prime numbers*, Math. Comp. 16 (1962), 363–367. DOI 10.2307/2004056. (§2, §5, §8)
- [Bary-Soroker 2012] L. Bary-Soroker, *Irreducible values of polynomials*, Adv. Math. 229 (2012), 854–874; arXiv:1005.4528. (§6)
- [Bodin–Dèbes–Najib 2020] A. Bodin, P. Dèbes, S. Najib, *The Schinzel hypothesis for polynomials*, Trans. Amer. Math. Soc. (2020); arXiv:1902.08155. (§6, §9)
- [Chen 1973] J. R. Chen, *On the representation of a larger even integer as the sum of a prime and the product of at most two primes*, Scientia Sinica 16 (1973), 157–176. (§4)
- [Chebyshev 1852] P. L. Chebyshev, *Mémoire sur les nombres premiers*, J. Math. Pures Appl. (sér. 1) 17 (1852), 366–390. (§1)
- [Cox 2022] D. A. Cox, *Primes of the Form $x^2 + ny^2$: Fermat, Class Field Theory, and Complex Multiplication*, 3rd ed., Amer. Math. Soc., 2022. (§5)
- [Dickson 1904] L. E. Dickson, *A new extension of Fermat's theorem*, Bull. Amer. Math. Soc. 10 (1904) — attribution as stated in [Pintz 2009]. (§2)
- [Entin 2016] A. Entin, *On the Bateman–Horn conjecture for polynomials over large finite fields*, Compositio Math. 152 (2016), DOI 10.1112/S0010437X16007570; arXiv:1409.0846. (§6, §8, §9)
- [Friedlander–Iwaniec 1998] J. Friedlander, H. Iwaniec, *The polynomial $X^2 + Y^4$ captures its primes*, Ann. of Math. 148 (1998), 945–1040; arXiv:math/9811185. (§4, §6)
- [Green–Tao 2008] B. Green, T. Tao, *The primes contain arbitrarily long arithmetic progressions*, Ann. of Math. 167 (2008), 481–547. DOI 10.4007/annals.2008.167.481. (§4)
- [Green–Tao 2010] B. Green, T. Tao, *Linear equations in primes*, Ann. of Math. 171 (2010), 1753–1850. DOI 10.4007/annals.2010.171.1753. (§4, §9)
- [Green–Tao 2012] B. Green, T. Tao, *The Möbius function is strongly orthogonal to nilsequences*, Ann. of Math. 175 (2012), 541–566. DOI 10.4007/annals.2012.175.2.3. (§4, §9)
- [Hardy–Littlewood 1923] G. H. Hardy, J. E. Littlewood, *Some problems of 'Partitio numerorum'; III: On the expression of a number as a sum of primes*, Acta Math. 44 (1923), 1–70. DOI 10.1007/BF02403921. (§2)
- [Heath-Brown 2001] D. R. Heath-Brown, *Primes represented by $x^3 + 2y^3$*, Acta Math. 186 (2001), 1–84. DOI 10.1007/BF02392715. (§4)
- [Ingram–Silverman 2009] P. Ingram, J. H. Silverman, *Primitive divisors in arithmetic dynamics*, Math. Proc. Cambridge Philos. Soc. 147 (2009). (§7)
- [Iwaniec 1978] H. Iwaniec, *Almost-primes represented by quadratic polynomials*, Invent. Math. 47 (1978), 171–188. DOI 10.1007/BF01578070. (§4)
- [Jones 2008] R. Jones, *The density of prime divisors in the arithmetic dynamics of quadratic polynomials*, J. London Math. Soc. 78 (2008), 523–544. DOI 10.1112/jlms/jdn034. (§7)
- [Jones–Sato–Wada–Wiens 1976] J. P. Jones, D. Sato, H. Wada, D. Wiens, *Diophantine representation of the set of prime numbers*, Amer. Math. Monthly 83 (1976), 449–464. JSTOR 2318339. (§8)
- [Jones–Zvonkin 2023] G. A. Jones, A. K. Zvonkin, *Block designs, permutation groups and prime values of polynomials* (Russian), Trudy Instituta Matematiki i Mekhaniki UrO RAN 29 (2023), no. 1, 233–253; arXiv:2105.03915. (§1, §5, §6, §8)
- [Maynard 2015] J. Maynard, *Small gaps between primes*, Ann. of Math. 181 (2015), 383–413. DOI 10.4007/annals.2015.181.1.7. (§4)
- [Maynard 2020] J. Maynard, *Primes represented by incomplete norm forms*, Forum of Mathematics, Pi 8 (2020). DOI 10.1017/fmp.2019.8; arXiv:1507.05080. (§4)
- [Maynard 2022] J. Maynard, *Counting primes*, Proceedings of the International Congress of Mathematicians 2022 (Helsinki), European Mathematical Society. (§3)
- [Pintz 2009] J. Pintz, *Landau's problems on primes*, J. Théor. Nombres Bordeaux 21 (2009), 357–404. DOI 10.5802/jtnb.676. (§2, §4)
- [Pollack 2008] P. Pollack, *An explicit approach to Hypothesis H for polynomials over a finite field*, in: The Anatomy of Integers (Montréal, 2006), CRM Proc. Lecture Notes 46, Amer. Math. Soc., 2008, 47–64. (§6, §9)
- [Pollack 2008b] P. Pollack, *A polynomial analogue of the twin prime conjecture*, Proc. Amer. Math. Soc. 136 (2008), 3775–3784. (§6)
- [Pollack 2008c] P. Pollack, *Simultaneous prime specializations of polynomials over finite fields*, Proc. London Math. Soc. 97 (2008), 545–567. (§6)
- [Rabinowitsch 1913] G. Rabinowitsch, *Eindeutigkeit der Zerlegung in Primzahlfaktoren in quadratischen Zahlkörpern*, J. Reine Angew. Math. 142 (1913), 153–164. (§5, §8)
- [Schinzel–Sierpiński 1958] A. Schinzel, W. Sierpiński, *Sur certaines hypothèses concernant les nombres premiers*, Acta Arith. 4 (1958), 185–208; erratum Acta Arith. 5 (1959), 259. DOI 10.4064/aa-4-3-185-208. (§2)
- [Sierpiński 1960] W. Sierpiński, *Sur un problème concernant les nombres $k \cdot 2^n + 1$*, Elem. Math. 15 (1960), 73–74; corrigendum 17 (1962), 85. (§3, §8)
- [Tao 2016] T. Tao, *The logarithmically averaged Chowla and Elliott conjectures for two-point correlations*, Forum of Mathematics, Pi 4 (2016). DOI 10.1017/fmp.2016.6; arXiv:1509.05422. (§4)
- [Wagstaff 1983] S. S. Wagstaff, *Divisors of Mersenne numbers*, Math. Comp. 40 (1983), 385–397. (§7)
- [Zhang 2014] Y. Zhang, *Bounded gaps between primes*, Ann. of Math. 179 (2014), 1121–1174. DOI 10.4007/annals.2014.179.3.7. (§4)
