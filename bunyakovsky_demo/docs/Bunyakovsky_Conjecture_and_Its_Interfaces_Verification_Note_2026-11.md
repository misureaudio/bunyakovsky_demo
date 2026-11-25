# Verification Note — "Bunyakovsky's Conjecture and Its Interfaces" v1

*2026-11-24. Companion to `Bunyakovsky_Conjecture_and_Its_Interfaces_v1.md`. Per the academic-writing policy, this note — not the essay — carries the process record: measured probes, citation audit, and residual gaps.*

## 1. T0 — measured anchors (2026-11-24, `bunyakovsky_demo` v1.6.2, workspace venv)

Commands: `.venv/Scripts/bunyakovsky-demo --poly "x^2+1"`, `--tuple "x, x+2"`, `--poly "x^2+x+41"`, run from `D:/Source/hermes-dir`. Exit code 0 for all three.

**x²+1:** hypotheses all satisfied (irreducibility certified mod p = 3; fd = 1). ω_f(p) for p = 2,3,5,7,11,13,17,19: 1, 0, 2, 0, 0, 2, 2, 0. C(f) = 1.3710 (product truncated p ≤ 10⁴). Ratios: N=10³: 112/120.9 = 0.9261; N=10⁴: 841/853.4 = 0.9854; N=2·10⁴: 1559/1568.1 = 0.9942. First prime values 2, 5, 17, 37, 101, 197, 257, 401; first composite f(3) = 10 = 2·5.

**x²+x+41:** certified mod p = 2. ω_f(p) = 0 for all p = 2,…,19 (all small primes inert in ℚ(√−163)). C(f) = 6.6561 (p ≤ 10⁴). Ratios: 581/581.6 = 0.9990; 4148/4137.6 = 1.0025; 7619/7607.0 = 1.0016. Longest run n = 1,…,39; first non-prime f(40) = 1681 = 41². (Note: README's older figure C ≈ 6.6658 was truncated at p ≤ 5·10³; the essay quotes today's 6.6561 @ 10⁴.)

**twins (x, x+2):** "This is the twin-prime conjecture"; admissible, "Checked exactly: it suffices to test p ≤ Σᵢ deg fᵢ". C = 1.32049 at p ≤ 10³ with printed note "equals 2·C₂ = 1.32032… (the classical twin-prime constant)" — the 4th-decimal discrepancy is a truncation artifact of the p ≤ 10³ product; the essay says so explicitly. Ratios: 35/44.4 = 0.7891 (10³); 205/212.8 = 0.9633 (10⁴); 342/356.4 = 0.9595 (2·10⁴).

## 2. T1 — citation audit (queries run → authoritative source → outcome)

Method per academic-writing skill: existence confirmed at publisher page / DOI / arXiv `citation_*` meta tags / author's own publication list; search snippets used for discovery only. `web_extract` was unavailable this session (ddgs search-only backend); arXiv metadata was pulled with `curl` + meta-tag grep.

**Corrections the audit forced (errors in the pre-audit notes/chat answer):**

1. **Pila → Bary-Soroker.** arXiv:1005.4528 meta: author *Lior Bary-Soroker*, not Pila. Venue: **Adv. Math. 229 (2012), 854–874**, DOI 10.1016/j.aim.2011.10.006 (TAU CRIS record + author publication list).
2. **1852 → 1857.** English Wikipedia: conjecture "stated in 1857"; French Wikipedia: 1854; 1852 is Chebyshev's memoir (J. Math. Pures Appl. 17, 366–390, Numdam). Essay uses 1857 with the variant noted, plus Jones–Zvonkin fn. 5's warning about the spurious 1840 "Nouveaux théorèmes relatifs à la distinction des nombres premiers…" title.
3. **Pollack venue.** "An explicit approach to Hypothesis H…" is **CRM Proc. Lecture Notes 46 (2008), 47–64** (author CV, pollack-math.net), *not* Proc. AMS 2009 as the notes said. Proc. AMS 136 (2008), 3775–3784 is the separate twin-polynomial paper.
4. **"Debes–Najman" → Bodin–Dèbes–Najib** (arXiv:1902.08155 meta); published in **Transactions of the AMS** (AMS record S0002-9947-2020-08198-7; JSTOR 26972669). Exact volume/pages not captured; essay entry omits them.
5. **JSWW venue.** *Amer. Math. Monthly* **83** (1976), 449–464 (JSTOR 2318339; Taylor & Francis DOI 10.1080/00029890.1976.11994142) — not Bull. AMS as the notes guessed.
6. **Zhang year.** Ann. of Math. **179** (2014), 1121–1174, DOI 10.4007/annals.2014.179.3.7 (Annals page) — published 2014, not 2013.
7. **Sierpiński k·2ⁿ+1 was UNCONDITIONAL.** Notes said "[C] assuming H"; audit (Filaseta–Finch–Kozek paper + Izotov paper, both with the explicit construction) shows Sierpiński's Elem. Math. 15 (1960), 73–74 proof is a covering-congruence + CRT construction (k ≡ 15511380746462593381 mod 2·3·5·17·257·641·65537·6700417), no hypothesis needed; Selfridge's 78557 (1962, unpublished; covering set {3,5,7,13,19,37,73}). Essay §3 states this correctly.
8. **Greaves cubic P₂ — REMOVED.** No primary source located; searches returned Filaseta's squarefree-values paper instead. Replaced by the verified almost-prime ladder (Rademacher 1924; Ricci 1936; Kuhn 1953/54; Buchstab 1967) exactly as tabulated in Pintz 2009 §19 (full PDF text read via search result).
9. **"Jones–Levy: primitive divisors have positive density" — wrong.** Correct content: **Ingram–Silverman** (MPCPS 147, 2009) prove primitive divisors exist for all but boundedly many n; **Jones** (JLMS 78 (2008), 523–544, DOI 10.1112/jlms/jdn034) proves the orbit prime-divisor set has density **zero** for four infinite families. The "<1 density conjecture of Jones and Levy" is attributed in the essay as "reported in the subsequent dynamics literature" — the primary Jones–Levy paper itself was not located this session.
10. **arXiv:2105.03915 is Jones–Zvonkin, not Amarra–Devillers–Praeger.** Meta tags: authors Gareth A. Jones, Alexander K. Zvonkin; title "Block designs and prime values of polynomials"; abstract (read verbatim) states the construction is *by* Amarra–Devillers–Praeger and depends on quadratics taking prime-power values; Bunyakovsky would imply the infinite family; large numbers of prime values agree with Li's Bateman–Horn modification. Published: Trudy IMM UrO RAN 29(1) (2023), 233–253, DOI 10.21538/0134-4889-2023-29-1-233-253. Essay cites ADP only *via* this verified abstract.

**Confirmed without change** (authoritative source in parentheses): Bateman–Horn (Math. Comp. 16, 363–367; AMS/JSTOR); Schinzel–Sierpiński (Acta Arith. 4, 185–208 + erratum 5, 259; MathSciNet MR0106202/EuDML); Hardy–Littlewood (Acta Math. 44, 1–70; Springer DOI); Green–Tao 2008 (Annals 167, 481–547); Green–Tao 2010 (Annals 171, 1753–1850, incl. the "conditional on GI/MN; unconditional s ≤ 2" nuance from the abstract); Green–Tao 2012 (Annals 175, 541–566; abstract wording "one of two major ingredients" quoted); Iwaniec (Invent. Math. 47, 171–188); Friedlander–Iwaniec (Annals 148, 945–1040); Heath-Brown (Acta Math. 186, 1–84); Maynard 2015 (Annals 181, 383–413; MathSciNet MR3272929); Maynard 2020 (Forum Math. Pi 8; Cambridge); Tao 2016 (Forum Math. Pi 4; Cambridge + arXiv 1509.05422 abstract "breaking the parity barrier"); Entin (Compositio 152, 2016; DOI 10.1112/S0010437X16007570; arXiv meta title/author/DOI); Chen (Scientia Sinica 16, 157–176; Sciengine DOI 10.1360/ya1973-16-2-157 + MacTutor); Pintz (JTNB 21, 357–404; Numdam BibTeX); Rabinowitsch (J. Reine Angew. Math. 142, 153–164; two independent secondary statements of the exact theorem — Galbraith lecture notes, Popov reference list); Wagstaff (Math. Comp. 40, 385–397); Aletheia-Zomlefer–Fukshansky–Garcia (Expo. Math. 38, 430–479; cmc.edu page + Jones–Zvonkin bibliography); Maynard ICM 2022 "Counting primes" (official IMU/mathunion PDF).

## 3. Residual gaps (honest leftovers)

- **Entin/CFSG:** the pre-audit claim "proof relies on CFSG" could not be confirmed from the arXiv abstract; the essay keeps the reduction to monodromy/permutation groups but flags the classification dependence as unconfirmed (explicit parenthetical in §6).
- **Bodin–Dèbes–Najib volume/pages** and **Ingram–Silverman pages** omitted from entries rather than guessed.
- **Jones–Levy** primary reference not located; attribution hedged in §7.
- **Bunyakovsky dating** remains conventionally 1857 with the 1854 (fr-Wiki) variant disclosed; the original memoir itself was not examined.
- **Dickson 1904** pages not printed; entry cites via Pintz's survey attribution.
- **Ulam-spiral class-field explanation** is kept as [H] folklore with the class-number-formula caveat stated in §5 (the C(−4) vs C(−163) datum shows h alone does not drive prime-richness).
- **Dirichlet 1837, Landau 1912, Cauchy n-cycle theorem, Selberg parity, DPRM** are named without bibliography entries (textbook-level named results; Landau's four problems documented through Pintz 2009).

## 4. Build record

T15 (pandoc/xelatex): build via `md2pdf-Claude-GPT-Gemini3_1Pro.py` with workspace venv python, `--output` explicit — **exit 0** (wrapper gate: xelatex log clean). pymupdf verification 2026-11-24: **9 pages**, `%%EOF` valid, 5,268 extracted words; probes present — title, §1 heading, measured values 1.3710 / 6.6561 / 0.9942 / 0.9633, all eight ratio-table cells (1559, 1568.1, 7619, 7607.0, 4148, 4137.6, …), "parity barrier", "Rabinowitsch", final sentence of §9, and final reference DOIs. No math collapse detected (no `aligned` environments used, per house constraint).
