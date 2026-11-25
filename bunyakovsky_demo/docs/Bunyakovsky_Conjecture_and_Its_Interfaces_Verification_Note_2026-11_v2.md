# Verification Note — "Bunyakovsky's Conjecture and Its Interfaces" v2

*2026-11-24. Companion to `Bunyakovsky_Conjecture_and_Its_Interfaces_v2.md` (supersedes the v1 note; v1 files frozen). Per the academic-writing policy, this note — not the essay — carries the process record: measured probes, citation audit, disposition of review r0, and residual gaps.*

## 1. T0 — measured anchors (2026-11-24, `bunyakovsky_demo` v1.6.2, workspace venv)

Commands: `.venv/Scripts/bunyakovsky-demo --poly "x^2+1"`, `--tuple "x, x+2"`, `--poly "x^2+x+41"`, run from `D:/Source/hermes-dir`. Exit code 0 for all three.

**x²+1:** hypotheses all satisfied (irreducibility certified mod p = 3; fd = 1). ω_f(p) for p = 2,3,5,7,11,13,17,19: 1, 0, 2, 0, 0, 2, 2, 0. C(f) = 1.3710 (product truncated p ≤ 10⁴). Ratios: N=10³: 112/120.9 = 0.9261; N=10⁴: 841/853.4 = 0.9854; N=2·10⁴: 1559/1568.1 = 0.9942. First prime values 2, 5, 17, 37, 101, 197, 257, 401; first composite f(3) = 10 = 2·5.

**x²+x+41:** certified mod p = 2. ω_f(p) = 0 for all p = 2,…,19 (all small primes inert in ℚ(√−163)). C(f) = 6.6561 (p ≤ 10⁴). Ratios: 581/581.6 = 0.9990; 4148/4137.6 = 1.0025; 7619/7607.0 = 1.0016. Longest run n = 1,…,39; first non-prime f(40) = 1681 = 41². (Note: README's older figure C ≈ 6.6658 was truncated at p ≤ 5·10³; the essay quotes today's 6.6561 @ 10⁴.)

**twins (x, x+2):** "This is the twin-prime conjecture"; admissible, "Checked exactly: it suffices to test p ≤ Σᵢ deg fᵢ". C = 1.32049 at p ≤ 10³ with printed note "equals 2·C₂ = 1.32032… (the classical twin-prime constant)" — the 4th-decimal discrepancy is a truncation artifact of the p ≤ 10³ product; the essay says so explicitly. Ratios: 35/44.4 = 0.7891 (10³); 205/212.8 = 0.9633 (10⁴); 342/356.4 = 0.9595 (2·10⁴).

## 2. T1 — citation audit (queries run → authoritative source → outcome)

Method per academic-writing skill: existence confirmed at publisher page / DOI / arXiv `citation_*` meta tags / author's own publication list; search snippets used for discovery only. `web_extract` was unavailable this session (ddgs search-only backend); arXiv metadata was pulled with `curl` + meta-tag grep.

**Corrections the audit forced (errors in the pre-audit notes/chat answer):**

1. **Pila → Bary-Soroker.** arXiv:1005.4528 meta: author *Lior Bary-Soroker*, not Pila. Venue: **Adv. Math. 229 (2012), 854–874**, DOI 10.1016/j.aim.2011.10.006 (TAU CRIS record + author publication list).
2. **1852 → 1857.** English Wikipedia: conjecture "stated in 1857"; French Wikipedia: 1854; 1852 is Chebyshev's memoir (J. Math. Pures Appl. 17, 366–390, Numdam). Essay uses 1857 with the variant noted, plus the Jones–Zvonkin footnote warning (see §5 item 4.3 below for the verbatim text).
3. **Pollack venue.** "An explicit approach to Hypothesis H…" is **CRM Proc. Lecture Notes 46 (2008), 47–64** (author CV, pollack-math.net), *not* Proc. AMS 2009 as the notes said. Proc. AMS 136 (2008), 3775–3784 is the separate twin-polynomial paper.
4. **"Debes–Najman" → Bodin–Dèbes–Najib** (arXiv:1902.08155 meta); published in **Transactions of the AMS** (AMS record S0002-9947-2020-08198-7; JSTOR 26972669). Exact volume/pages not captured; essay entry omits them.
5. **JSWW venue.** *Amer. Math. Monthly* **83** (1976), 449–464 (JSTOR 2318339; Taylor & Francis DOI 10.1080/00029890.1976.11994142) — not Bull. AMS as the notes guessed.
6. **Zhang year.** Ann. of Math. **179** (2014), 1121–1174, DOI 10.4007/annals.2014.179.3.7 (Annals page) — published 2014, not 2013.
7. **Sierpiński k·2ⁿ+1 was UNCONDITIONAL.** Notes said "[C] assuming H"; audit (Filaseta–Finch–Kozek paper + Izotov paper, both with the explicit construction) shows Sierpiński's Elem. Math. 15 (1960), 73–74 proof is a covering-congruence + CRT construction (k ≡ 15511380746462593381 mod 2·3·5·17·257·641·65537·6700417), no hypothesis needed; Selfridge's 78557 (1962, unpublished; covering set {3,5,7,13,19,37,73}). Essay §3 states this correctly.
8. **Greaves cubic P₂ — REMOVED.** No primary source located; searches returned Filaseta's squarefree-values paper instead. Replaced by the verified almost-prime ladder (Rademacher 1924; Ricci 1936; Kuhn 1953/54; Buchstab 1967) exactly as tabulated in Pintz 2009 §19 (full PDF text read via search result).
9. **"Jones–Levy: primitive divisors have positive density" — wrong.** Correct content: **Ingram–Silverman** (MPCPS 147, 2009) prove primitive divisors exist for all but finitely many n; **Jones** (JLMS 78 (2008), 523–544, DOI 10.1112/jlms/jdn034) proves the orbit prime-divisor set has density **zero** for four infinite families. The "<1 density conjecture of Jones and Levy" is attributed in the essay as "reported in the subsequent dynamics literature" — the primary Jones–Levy paper itself was not located this session.
10. **arXiv:2105.03915 is Jones–Zvonkin, not Amarra–Devillers–Praeger.** Meta tags: authors Gareth A. Jones, Alexander K. Zvonkin; title "Block designs and prime values of polynomials"; abstract (read verbatim) states the construction is *by* Amarra–Devillers–Praeger and depends on quadratics taking prime-power values; Bunyakovsky would imply the infinite family; large numbers of prime values agree with Li's Bateman–Horn modification. Published: Trudy IMM UrO RAN 29(1) (2023), 233–253, DOI 10.21538/0134-4889-2023-29-1-233-253. Essay cites ADP only *via* this verified abstract.

**Confirmed without change** (authoritative source in parentheses): Bateman–Horn (Math. Comp. 16, 363–367; AMS/JSTOR); Schinzel–Sierpiński (Acta Arith. 4, 185–208 + erratum 5, 259; MathSciNet MR0106202/EuDML); Hardy–Littlewood (Acta Math. 44, 1–70; Springer DOI); Green–Tao 2008 (Annals 167, 481–547); Green–Tao 2010 (Annals 171, 1753–1850, incl. the "conditional on GI/MN; unconditional s ≤ 2" nuance from the abstract); Green–Tao 2012 (Annals 175, 541–566; abstract wording "one of two major ingredients" quoted); Iwaniec (Invent. Math. 47, 171–188); Friedlander–Iwaniec (Annals 148, 945–1040); Heath-Brown (Acta Math. 186, 1–84); Maynard 2015 (Annals 181, 383–413; MathSciNet MR3272929); Maynard 2020 (Forum Math. Pi 8; Cambridge); Tao 2016 (Forum Math. Pi 4; Cambridge + arXiv 1509.05422 abstract "breaking the parity barrier"); Entin (Compositio 152, 2016; DOI 10.1112/S0010437X16007570; arXiv meta title/author/DOI); Chen (Scientia Sinica 16, 157–176; Sciengine DOI 10.1360/ya1973-16-2-157 + MacTutor); Pintz (JTNB 21, 357–404; Numdam BibTeX); Rabinowitsch (J. Reine Angew. Math. 142, 153–164; two independent secondary statements of the exact theorem — Galbraith lecture notes, Popov reference list); Wagstaff (Math. Comp. 40, 385–397); Aletheia-Zomlefer–Fukshansky–Garcia (Expo. Math. 38, 430–479; cmc.edu page + Jones–Zvonkin bibliography); Maynard ICM 2022 "Counting primes" (official IMU/mathunion PDF).

## 3. Residual gaps (honest leftovers)

- **Entin/CFSG:** the pre-audit claim "proof relies on CFSG" could not be confirmed from the arXiv abstract; the essay keeps the reduction to monodromy/permutation groups but flags the classification dependence as unconfirmed (explicit parenthetical in §6).
- **Bodin–Dèbes–Najib volume/pages** and **Ingram–Silverman pages** omitted from entries rather than guessed.
- **Jones–Levy** primary reference not located; attribution hedged in §7.
- **Bunyakovsky dating** remains conventionally 1857 with the 1854 (fr-Wiki) variant disclosed; the original memoir itself was not examined.
- **Ulam-spiral class-field explanation** is kept as [H] folklore; the §5 statement C(f) = κ_f·L(1,χ_D)⁻¹ ∝ √|D|/h(D) is the authors' own derivation from the Euler factors 1 − (D/p)/(p−1) plus the class number formula, cross-checked against both demo constants (1.3710 vs 1.27 and 6.6561 vs 4.07 for the main factor) — not lifted from a source.
- **Dirichlet 1837, Landau 1912, Cauchy d-cycle theorem, Jordan fixed-point-free theorem, Selberg parity, DPRM** are named without bibliography entries (textbook-level named results; Landau's four problems documented through Pintz 2009).

## 4. Build record

T15 (pandoc/xelatex), v1 build: exit 0; pymupdf: 9 pages, %%EOF valid, 5,268 words, all probes present.

T15 v2 build: exit 0 (wrapper gate, xelatex log clean); pymupdf verification appended below after execution.

## 5. Disposition of review r0 (file `Bunyakovsky_Conjecture_and_Its_Interfaces_v1_r0_Hyd.md`)

Every item adjudicated against primary sources; **accepted** = fixed in v2, **rejected** = kept as in v1.

**§1 Critical — all five ACCEPTED.**
1.1 **BH denominator exponent.** Correct and important: the exponent is k (number of polynomials), not deg f; the reviewer's divergence argument (mean ν_p = 1 by Chebotarev/Davenport) is sound, and the demo's own numbers (1.3710 ≈ literature 1.37281) confirm the k=1 convention. v2 §2 now displays the general k-tuple BH (B(F)/d · Li_k(N), exponent k) and the k=1 specialization; π_f defined over 1 ≤ n ≤ N.
1.2 **Index set.** Correct; v2 defines π_f(N) = #{1 ≤ n ≤ N: …}, matching the demo docstring ("prime values for 1 <= n <= N", `bunyakovsky.py::predicted_count`).
1.3 **Monodromy paragraph.** All three sub-points correct: V₄ acts regularly (non-identity elements are double transpositions — fixed-point-free); ν₃,ν₅,ν₇(x⁴+1) = 0 (checked by hand: x⁴ ∈ {0,1} mod 3 and mod 5; {0,1,2,4} mod 7), so root-avoidance certificates exist and only the *irreducibility* certificate fails; admissibility is automatic for p > Σdeg (x²+x+2 vs x²+x+1 at p=2 shows small primes are invisible to G). v2 §6 rewritten around the corrected dictionary (ν_p = fixed points of Frob_p; d-cycle ⟺ positive density of irreducible reductions; Jordan's theorem for fixed-point-free elements; Cauchy d-cycle for prime degree). Also self-caught while re-checking: the JZ warning is **footnote 1**, not fn. 5 — fixed.
1.4 **μ vs primality.** Correct — μ(m) = −1 for all odd-parity squarefree values (30); that is the parity ambiguity itself. v2 §4c restated via von Mangoldt Λ and Λ = −μ∗log.
1.5 **Ingram–Silverman hypothesis.** Correct — the theorem needs "0 not periodic"; the x², a=2 orbit is a clean counterexample to the essay's formulation. v2 §7 states the hypothesis and keeps the counterexample as motivation.

**§2 Omissions — all three ACCEPTED.**
2.1 **GI(s) completion.** Correct gap; citation verified at the publisher: **Green, Tao, Ziegler, *An inverse theorem for the Gowers U^{s+1}[N]-norm*, Ann. of Math. 176 (2012) no. 2, 1231–1372, DOI 10.4007/annals.2012.176.2.11** — Annals page confirms three authors and "for all s ≥ 1; this is new for s ≥ 4". Added to §4c, §9, and the reference list; the linear-forms theorem is now stated unconditional at every fixed complexity.
2.2 **Chain vs single-polynomial BH.** Correct; v2 §2 notes that the k-tuple BH implies H while the displayed k=1 form implies only Bunyakovsky.
2.3 **Normalization.** Correct, confirmed from source: `predicted_count` = C·∫₂^N dt/ln f(t) (trapezoid, 20000 panels) and `predicted_tuple_count` = C·∫₂^N dt/(ln f₁·ln f₂) ≈ C·Li₂(N) (1.32049·Li₂(10⁴) ≈ 1.32049·161.2 = 212.8 ✓ reproduces the card). v2 §8 item 6 states the exact integrals; §2 states the asymptotic form.

**§3 Minor — all ACCEPTED.**
3.1 F_q[t] PNT is Gauss-elementary; Weil = RH for curves (Chebotarev-type applications); Deligne = higher dimensions. Fixed.
3.2 Modulus added: k ≡ 15511380746462593381 (mod 2·3·5·17·257·641·65537·6700417) (= 2(2⁶⁴−1) since F₀⋯F₅ = 2⁶⁴−1); residue is odd so the class is odd.
3.3 Maynard: liminf ≤ 600 (not <). Fixed.
3.4 Mersenne divisors: q ≡ 1 (mod 2p), q ≡ ±1 (mod 8). Fixed.
3.5 EDS: log u_n ≍ n² → the divergence test predicts *finitely many* prime terms; restructured so EDS sit on the convergent side. Fixed.
3.6 All six items fixed: "Zassenhaus factoring algorithm — Berlekamp–Zassenhaus, LLL-based refinements in practice"; primitivity parenthetical in item 3; "d-cycle" replaces "n-cycle"; demo run-counter clarification (n = 1..39 is the demo's counter; including n = 0 gives Rabinowitsch's 40 values); "the 12 prime bases 2–37".
3.7 Class-number direction: accepted and *strengthened* — v2 §5 derives C(f) = κ_f·L(1,χ_D)⁻¹ ∝ √|D|/h(D) explicitly (factor 1 − (D/p)/(p−1); κ_f absolutely convergent) and checks it against the two measured constants.

**§4 Bibliographic — accepted with two corrections to the reviewer.**
4.1 Initials fixed: S. L. Aletheia-Zomlefer, L. Fukshansky, S. R. Garcia.
4.2 **10.7 figure: ACCEPTED and resolved from the primary source.** Extracted verbatim from arXiv:2105.03915 §11: "for the well-known Euler polynomial t²+t+41 … the constant found in [Cohen] is 3.31977318, while for the polynomial t²+t+75 it is 0.31097668 … the first polynomial produces, approximately, 10.7 times as many primes as the second one." So 10.7× is the Euler-41 vs t²+t+75 count ratio (Cohen's constants), not a ratio to the twin-prime constant — the reviewer's arithmetic suspicion was right; v2 §6 now states the correct comparison, plus Rivin's champion t²−2619t+1291 (C = 6.3722) from the same passage.
4.3 **1857/1840 title: REJECTED (no inversion found).** The JZ footnote extracted verbatim from the PDF: "Numerous publications give the following wrong title for Bunyakovsky's paper: 'Nouveaux théorèmes relatifs à la distinction des nombres premiers et à la décomposition des entiers en facteurs'. According to the French Wikipedia, an article with this title does indeed exist, but it was published in 1840 and not in 1857, and it does not discuss the conjecture in question." The essay reported this faithfully; the reviewer's quoted "standard" attribution is the *short*-title 1857 memoir (Mém. Acad. Sci. St.-Pétersbourg 6, 305–329 — volume/pages per the review, not independently verified here), which is compatible: the two titles differ ("relatifs aux nombres premiers" vs "relatifs à la distinction… et à la décomposition…"). Essay keeps the report of JZ's footnote, with the footnote number corrected to fn. 1.
4.4 **Dickson venue: ACCEPTED with correction to the reviewer's title.** Venue/pages confirmed: *Messenger of Mathematics* **33** (1904), 155–161 — but the actual title is **"A new extension of Dirichlet's theorem on prime numbers"** (OEIS wiki file page hosting the scan, "Dickson's 1904 paper introducing his conjecture on the infinitude of prime tuples"; independent reference lists agree), not "A new extension of Fermat's theorem" as both v1 and the review had it. Reference entry corrected accordingly; the "as cited in Pintz" hedge dropped.
4.5 Accuracy phrasing aligned: Abstract, §2, §9 now say "within a few percent" with "fractions of a percent" reserved for the best-behaved cases.
4.6 **REJECTED: the date is intentional.** 2026-11-24 is the session date (the desktop runtime date), not a typo.
