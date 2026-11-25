# What this workspace proves, and whose mathematics it is

**What is ours is the Lean proof.** Each repo holds a complete machine-checked proof of a
standard formal statement: the implication "RH/GRH implies X" on Mathlib alone, and X itself
once the hypothesis is supplied by the Lean proof of RH (Alpöge, 20 November 2026; certified by
the Lean FRO and the Mathlib Initiative on 21 November; kernel checks at
<https://math.mit.edu/~drew/grh/>). The theorems on paper are due to the authors listed below.
Each repo's README says which sources were read directly and which were cited through a
secondary source.

## How to describe a result

- **Main library:** "a complete Lean proof that RH/GRH implies X, following author, year".
- **`Unconditional/` theorem:** "X, proved unconditionally in Lean with the certified proof of
  RH/GRH in leanprover-community/riemann-hypothesis".
- **For an RH-equivalent statement,** add: "X is equivalent to RH, so this is RH in another form".
- Say what was added beyond the paper: explicit constants, lemmas the paper leaves unproved,
  proved-sound checkers for finite ranges.
- Credit the conditional theorem to its authors and the proof of RH to Alpöge. The Lean proofs
  of the implications, and the end-to-end theorems, are this workspace's.
- If a flaw were ever found in the RH proof, every tier-U theorem would fall back to its tier-C
  form, which does not depend on it.

## Named conjectures (label **RH-consequence**)

Each was open before the 2026 proof of RH. The conditional theorem is published; the main
library formalises it (tier C) and `Unconditional/` proves the statement outright (tier U).

| Result | Conditional theorem due to |
|---|---|
| erdos-985, a prime primitive root `q < p` | McGown–Treviño–Trudgian 2016, Theorem 1, with a finite check |
| lindelof-rh, the Lindelöf hypothesis for ζ and Dirichlet L | classical; Littlewood |
| density-rh, the density hypothesis | immediate from RH; the zero count `N(T) ≪ T log T` (von Mangoldt 1905) is proved with no hypothesis |
| grosswald-grh, Grosswald's conjecture | McGown–Treviño–Trudgian 2016, with the computation of Cohen–Oliveira e Silva–Trudgian redone here |
| weinberger-grh, Euler's idoneal numbers | Weinberger 1973 |
| abelian-erh, ERH for abelian number fields | follows from GRH for Dirichlet L-functions by the factorisation of the Dedekind zeta function (Washington, *Cyclotomic Fields*, Thm 4.3) |

## Statements equivalent to RH (label **RH-equivalent**)

Each of these is RH in another form, so the unconditional theorem is a second machine-checked
statement of it.

| Result | Equivalence due to |
|---|---|
| robin-rh, Robin's inequality; Lagarias's form | Robin 1984; Lagarias 2002 |
| nicolas-rh, Nicolas' inequality | Nicolas 1983 |
| li-criterion-rh, Li's criterion | Li 1997 (we prove the direction RH ⇒ positivity) |
| speiser-rh, `ζ'(s) ≠ 0` for `0 < Re s < 1/2` | Speiser 1934 |
| mertens-rh, `M(x) = O(x^{1/2+ε})`; Riesz and Hardy–Littlewood criteria; Titchmarsh's sharper bounds | Littlewood 1912; Riesz 1916; Hardy–Littlewood 1916; Titchmarsh 1927 |

## Theorems the literature proves under RH or GRH (label **RH-consequence**)

The first four are proved here with the papers' own constants.

| Result | Conditional theorem due to |
|---|---|
| lls-grh, every theorem of the paper; Bach's bound with constant `2` | Lamzouri–Li–Soundararajan 2015; Bach 1990 |
| bach-sorenson-grh, least prime in a progression, constant `2` | Bach–Sorenson 1996 |
| schoenfeld-rh, `ψ`, `θ`, `π − li` with constant `1/(8π)` | von Koch 1901; Schoenfeld 1976 (Rosser's 1941 zero count is proved with no hypothesis) |
| cramer-rh, prime gaps with constant `22/25`; the mean square of `ψ(x) − x` | Cramér 1920, 1922; Carneiro–Milinovich–Soundararajan 2019 |
| erdos-770, part (iii) with the explicit bound `⌈200 log² n⌉` | the GRH implication is a remark in Korsky's 2026 notes; the explicit all-`n` form was not found in the literature. Parts (i) and (ii) stay open |
| erdos-233, primes in almost all short intervals; `Σ d_n² ≪ N log⁴ N` | Selberg 1943; Cramér 1936. Erdős 233 itself stays open |

## erdos-985 and the literature (checked 2026-11-24)

The conditional theorem is published; the Lean proof, and the unconditional theorem, are ours.

- McGown–Treviño–Trudgian, *Resolving Grosswald's conjecture on GRH*, Funct. Approx. Comment.
  Math. 55 (2016) 215–225, arXiv:1508.05182, Theorem 1: assume GRH; then the least **prime**
  primitive root satisfies `ĝ(p) < √p − 2` for all primes `p > 2791`. Since `√p − 2 < p`,
  Erdős 985 under GRH follows for `p > 2791`, and the 405 odd primes up to 2791 are a trivial
  check (largest value `ĝ(2791) = 53`).
- This has been said in public: erdosproblemaday.com's report on 985 (28 July 2026) notes that
  MTT's Theorem 1 with a finite check proves the statement under GRH.
- Unconditionally the problem is open, even for all large `p`: the best uniform bound is
  `ĝ(p) ≪ p^3.1` (Ha, J. Number Theory 2013).

What the repo can claim: a Lean proof of the conditional theorem (tier C) and its tier-U form;
a complete proof of MTT's Lemma 1, which they state without proof; and a route with a smaller
computation (`10^8`). Label: **RH-consequence**.

**Still to do:** the paper (`paper/erdos985.pdf`) should cite McGown–Treviño–Trudgian's
Theorem 1 as the source of the conditional theorem. Its title, "a formalized proof of Erdős
Problem 985", is accurate now that the proof of RH is certified.

## What the workspace can claim

- Complete Lean proofs of the conditional theorems (tier C), on Mathlib alone.
- With the certified proof of RH, unconditional Lean theorems (tier U) for every row above.
- Explicit constants, completed lemmas (McGown–Treviño–Trudgian's Lemma 1 is proved in full in
  erdos-985) and verified computations that the papers do not contain.

Each unconditional theorem combines a published conditional theorem with Alpöge's proof of RH.
`RH_FULL_BUILD=1` (rebuilding riemann-hypothesis from source on our box) has not been run.
