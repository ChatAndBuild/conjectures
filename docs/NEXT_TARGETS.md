# Next targets

Working notes, 2026-11-24, on which RH/GRH consequences to formalise next. Tiers (D, U, C, H)
and the rules they refer to are defined in [`AGENTS.md`](../AGENTS.md). Status of the existing
seven repos lives in `AGENTS.md`, not here.

## The test a candidate has to pass

[riemann-hypothesis](https://github.com/leanprover-community/riemann-hypothesis) proves exactly
two things: `riemannHypothesis : RiemannHypothesis` (ζ) and
`LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf` (Dirichlet L-functions).
It says nothing about Dedekind zeta functions of non-abelian fields, Hecke L-functions or
elliptic-curve L-functions.

So a result can reach tier U only if its analytic input is RH for ζ or GRH for Dirichlet L, and
any finite range left below the analytic threshold fits in `native_decide` with a proved-sound
checker. Anything else stays C or H at best. That is the filter applied below.

## Ranked candidates

| # | Target | Analytic input | Expected tier | Reuses |
|---|---|---|---|---|
| 1 | Euler's idoneal numbers and Gauss class number one under GRH (Weinberger 1973) | GRH, real characters | U | erdos-985 zero sums |
| 2 | von Koch / Schoenfeld bound for `π(x) − li(x)` under RH | RH | U, if the small range fits | erdos-985 explicit formula, robin-rh `Robin/RH/` |
| 3 | Least prime in an arithmetic progression under GRH (Bach–Sorenson 1996) | GRH | U | ankeny-grh, miller-grh |
| 4 | Lindelöf for Dirichlet L-functions under GRH | GRH | U | lindelof-rh blueprint (statement already stubbed) |
| 5 | Cramér's prime-gap theorem under RH (1920) | RH | U | #2 |
| 6 | Ternary Goldbach under GRH (Deshouillers–Effinger–te Riele–Zinoviev 1997) | GRH | U only if the computation fits; otherwise H | erdos-985 |

### 1. Idoneal numbers and class number one (Weinberger)

Euler's 65 idoneal numbers are known to be the complete list under GRH. Unconditionally,
Weinberger's 1973 results leave room for at most two more. Some sources say "at most one",
which is wrong. The unconditional question is still open, so a tier-U proof would
be a formal result about an open problem, not just a re-proof. Class number one for imaginary
quadratic fields (`h(−d) = 1` exactly for the nine Heegner discriminants) runs on the same
machinery and comes almost for free:

1. A GRH lower bound for `L(1, χ_d)`, from erdos-985's zero-sum toolkit.
2. The class number formula `h(−d) = w √d · L(1, χ_d) / (2π)`.
3. Genus theory. An idoneal discriminant has a class group of exponent at most 2, so
   `h = 2^(t−1)`, where `t` is the number of prime factors of the discriminant.
4. Steps 1–3 make `h` too large for every discriminant beyond an explicit bound. A finite
   `native_decide` check covers the rest.

**Main cost:** Mathlib's support for class groups of binary quadratic forms and for genus
theory is thin. Scope that before writing any proof: check that steps 2 and 3 can be *stated*
against the Mathlib pin. If they can't, this becomes a Mathlib project first.

Statement source: check formal-conjectures for an idoneal statement to copy verbatim (rule 3).
The Conjecture Atlas carries the rows `wiki-idoneal-number` and `wiki-class-number-problem`.

### 2. von Koch / Schoenfeld under RH

Schoenfeld (1976): under RH, `|π(x) − li(x)| < √x log x / (8π)` for `x ≥ 2657`, and a
companion bound holds for `ψ(x)`. Very well known, and needs RH for ζ only. erdos-985's
weighted explicit formula and robin-rh's `Robin/RH/Bach.lean` and `Robin/RH/Psi1.lean` already
do most of the analytic work. The risk is bookkeeping the explicit constants. The range just
above 2657 may need a direct computation, which decides whether it is U or U + H.

### 3. Least prime in an arithmetic progression (Bach–Sorenson)

Under GRH, the least prime `p ≡ a (mod q)` satisfies `p ≤ 2 (q log q)²` (Bach–Sorenson 1996;
Lamzouri–Li–Soundararajan sharpen it). This is the GRH form of Linnik's problem. The machinery
is almost identical to ankeny-grh's subgroup bound, so expect a weaker constant first, as with
ankeny's `21/5`. Record any deviation in the README (rule 3).

### 4. Dirichlet-L Lindelöf

`dirichletLindelof_of_GRH` already exists in `lindelof-rh/Lindelof/Dirichlet.lean`, with its
proof left as `sorry`. The `AGENTS.md` checklist gives the plan: steps 1–8 of
`lindelof-rh/docs/BLUEPRINT.md`, with `ξ` replaced by the completed L-function of the inducing
primitive character. This is the quickest win here.

### 5. Cramér's prime-gap theorem

Cramér (1920): under RH, `p_{n+1} − p_n = O(√p_n log p_n)`. This is his *theorem*, not his
conjecture (gaps `≪ log² p`), which is rejected below. It follows naturally from #2. An explicit
version (Carneiro–Milinovich–Soundararajan 2019, `p_{n+1} − p_n < (22/25) √p_n log p_n` for
`p_n > 3`) would make a better headline than a bare `O(·)`.

### 6. Ternary Goldbach under GRH (DETZ)

The analytic half fits: GRH for Dirichlet L-functions is exactly the input. The blocker is the
range below the GRH threshold, which is far larger than erdos-985's `10^8` check. This is tier U
only if that computation can be done in `native_decide` chunks with a sound checker. Otherwise
it lands at tier H, like grosswald-grh's range. (`calr3/ternary-goldbach` exists but assumes
binary Goldbach up to `4·10^18`.)

## Round 2 (2026-11-24): revisions to the list above

A second research pass, filtered the same way, changed four things:

- **#2 von Koch / Schoenfeld moves to the front.** Mills (#7) and Nicolas (#11) are built on it.
- **#5 Cramér folds into #2.** Dudek ([arXiv:1402.6417](https://arxiv.org/abs/1402.6417), Thm 2):
  under RH there is a prime in `(x − (4/π)√x log x, x]` for `x ≥ 2`, which follows almost directly
  from the explicit `π(x) − li(x)` bound.
- **#3: target Lamzouri–Li–Soundararajan, not Bach–Sorenson.** LLS (Math. Comp. 84 (2015),
  [arXiv:1309.3595](https://arxiv.org/abs/1309.3595)) Cor 1.2 gives `P(a,q) ≤ (φ(q) log q)²` for
  `q > 3`, which is stronger.
- **#1 Weinberger: a cheaper finite check.** If `h(−q) = 1`, every prime below `q/4` is inert, and
  LLS Thm 1.4 bounds the least split prime, which caps `q`. LLS also gives `h(−q) ≥ 9053` for
  `q ≥ 10^11` under GRH.

## Round 2: new candidates

| # | Target | Input | formal-conjectures statement | Expected tier | Effort |
|---|---|---|---|---|---|
| 7 | Mills' constant: `A ∈ (1.3063778838, 1.3063778839)` | RH | `Wikipedia/Mills.lean`, `Mills.lower_bound_of_RH` | U | S, after #2 |
| 8 | Density hypothesis | RH | `Wikipedia/DensityHypothesis.lean`, **research open** | U | S–M |
| 9 | Li's criterion, RH ⇒ `λ_n > 0` | RH | `Paper/RiemannHypothesisEquivalents.lean`, `li_criterion_rhs`, **research open** | U | M |
| 10 | Mertens `M(x) = O(x^{1/2+ε})`, with Redheffer and Franel–Landau as corollaries | RH | none | U | M–L |
| 11 | Nicolas' criterion (the φ version of Robin) | RH | none | U, if the small range fits | M–L |
| 12 | LLS upgrade of ankeny-grh / miller-grh (constant near 1 instead of `21/5`) | GRH | none | U | M |
| 13 | Explicit Littlewood bounds for `L(1,χ)` and class numbers | GRH | none | U | M–L |
| 14 | Erdős 233, upper bound: `Σ_{n<N} gap_n² = O(N log⁴ N)` | RH | `ErdosProblems/233.lean`, `erdos_233.variants.upper_bound` | U | L |
| 15 | Littlewood's bound `log ζ(1/2+it) ≪ log t / log log t` | RH | none | U | M |
| 16 | Riesz and Hardy–Littlewood criteria | RH | none | U | S–M, after #10 |

Statements the research could not confirm against the primary source are marked *(unverified)*.
Check them before fixing a `Statement.lean`.

### 7. Mills' constant

Caldwell–Cheng, J. Integer Seq. 8 (2005), Art. 05.4.1, Thm 1, through Lemma 5: under RH there is
a prime between `x³` and `(x+1)³`, via Schoenfeld's bound for `x ≥ 2657`, i.e. #2. The lower bound
needs no RH: `q_n ≥ P_n` for the greedy sequence 2, 11, 1361, 2521008887. The upper bound needs
the greedy limit to be a Mills number, which is where primes between cubes come in.
`P₄^{1/81} = 1.30637788386308…` and `(P₄+1)^{1/81} = 1.30637788386947…` both lie inside the
target interval. The finite work is one primality certificate, six compositeness checks and two
rational 81st-power comparisons, all within `norm_num` / `decide` range. Wikipedia-level, with a
ready statement.

### 8. Density hypothesis

Under RH, `N(σ,T) = 0` for `σ > 1/2`. At `σ = 1/2` only `N(T) ≪ T log T` is needed (Riemann–von
Mangoldt; Titchmarsh ch. 9 *(section unverified)*). It reuses erdos-985's `XiGrowth` with
Mathlib's Jensen formula (`Analysis/Complex/JensenFormula.lean`). formal-conjectures'
`zeroCountOn` counts multiplicity, which Jensen handles. The zero-counting lemma is shared with
#9 and #14, so build it once as a library.

### 9. Li's criterion (RH ⇒ positivity)

Li, J. Number Theory 65 (1997) 325–333; Bombieri–Lagarias, JNT 77 (1999) 274–287. Under RH,
`|1 − 1/ρ| = 1`, so each term is `2(1 − cos nθ_ρ) ≥ 0`. Missing: summability from
`Σ 1/|ρ|² < ∞`, and, for strict positivity, infinitely many zeros. Mathlib has no theorem that
ζ has any zero; erdos-985's Hadamard factorisation plus the Γ growth of `ξ` supplies one.
formal-conjectures' `lambda` sums over a set, ignoring multiplicity, which is harmless here.

### 10. Mertens function

Littlewood, C. R. Acad. Sci. 154 (1912) 263–266 *(attribution from surveys)*. Redheffer's
`det R_n = M(n)` *(1977; venue unverified)* and Franel–Landau (Gött. Nachr. 1924) come almost
free afterwards. Needs `1/ζ ≪ |t|^ε` on `σ ≥ 1/2 + δ`, which lindelof-rh's log-ζ /
Borel–Carathéodory work should reach, and a **sharp-cutoff Perron formula**, which Mathlib
lacks. erdos-985's smoothed Perron stops at `x^{3/4+ε}`, the same barrier robin-rh hit with `ψ`.
This is the most famous RH equivalence on the list.

### 11. Nicolas' criterion

`N_k/φ(N_k) > e^γ log log N_k` for every primorial `N_k` (Nicolas, JNT 17 (1983) 375–388
*(theorem number unverified)*; restated in Acta Arith. 155 (2012)). Uses Schoenfeld's
`|θ(x) − x| ≤ √x log²x/(8π)` for `x ≥ 599`, `θ(x) < x` below `8·10^11`, and
`Σ 1/(ρ(1−ρ)) = 2 + γ − log 4π`. Reuses robin-rh's Mertens estimates and #2. The size of the
finite check is not yet established; probably `≤ 10^8`.

### 12. LLS upgrade of ankeny-grh and miller-grh

LLS Thm 1.1: for `q ≥ 3000`, the least prime `ℓ ∤ q` outside a proper subgroup is
`≤ (log q + B(q))²`. Thm 1.4 (`q ≥ 20000`) handles cosets, including the least prime quadratic
residue. This replaces ankeny-grh's `21/5`, which is weaker than Bach's own `2`, with a constant
near 1. The `q < 3000` check is trivial. Deterministic Tonelli–Shanks (polynomial-time square
roots mod `p` under GRH) is a free corollary.

### 13. Explicit `L(1,χ)` and class-number bounds

LLS Thm 1.5 and Cor 1.3, for `q ≥ 10^10`: `|L(1,χ)| ≤ 2e^γ(log log q − log 2 + 1/2 + 1/log log q)`,
a matching lower bound, and `h(−q) ≥ (π/(12e^γ)) √q / (log log q + …)`. Also an input to #1.

### 14. Erdős 233 (upper bound)

Selberg, Arch. Math. Naturvid. 47 (1943): the mean-square lemma
`∫|θ(y+δy) − θ(y) − δy|² ≪ δx² log² x` is confirmed. The exact `Σ d_n²` form, and
formal-conjectures' attribution to Cramér, are *unverified*. Explicit version: Cully-Hugill–Dudek,
[arXiv:2206.00433](https://arxiv.org/abs/2206.00433). Needs a Gallagher/Plancherel mean-value
lemma and #8's zero counting.

### 15. Littlewood's strong Lindelöf bound

`log|ζ(1/2+it)| ≤ C log t / log log t`. Littlewood 1924 gives an unspecified `C`
*(Titchmarsh §14.14, unverified)*, which is the realistic target and extends lindelof-rh. The
sharp `(log 2)/2 + o(1)` is Chandee–Soundararajan, Bull. LMS 43 (2011), Thm 1.1 (effort L).

### 16. Riesz and Hardy–Littlewood criteria

Under RH, the Riesz function is `O(x^{1/4+ε})` (Riesz, Acta Math. 40 (1916)), and
`Σ μ(n)/n · e^{−x/n²} = O(x^{−1/4+ε})` (Hardy–Littlewood, Acta Math. 41 (1916)). Both are
Mellin–Barnes contour shifts once #10's `1/ζ` bound exists. They are smoothed by nature, so no
sharp-cutoff Perron is needed.

## Round 3 (2026-11-24): what riemann-hypothesis proves along the way

Rounds 1 and 2 treated riemann-hypothesis as two theorems. Round 3 read the whole repo and
inventoried its intermediate lemmas in [`rh-lemmas/`](rh-lemmas/README.md). Three follow-up
reports matched those lemmas against the Conjecture Atlas and formal-conjectures:
[analytic](rh-lemmas/targets-analytic.md), [algebraic](rh-lemmas/targets-algebraic.md) and
[geometry and algebra](rh-lemmas/targets-geometry-algebra.md). They hold the declaration names,
paths and the full reasoning for every row below.

All of it was read from statements. Nothing was built, and no `#print axioms` was run. The
first step on any target here is to import the one module it needs and check the statement and
its axioms. artin-grh PR #11 shows that works: importing a single `GroundTheory` module took
17 s and 6.6 GB of RAM, not the 93 GB / 19 GB of the full import.

### The filter changes

The round 1 test was "the analytic input is RH for ζ or GRH for Dirichlet L". The repo also
proves, with no hypothesis, Siegel–Walfisz, Linnik, Brun–Titchmarsh, the large sieve, a
truncated explicit formula, global class field theory, Chebotarev density, the continuation of
`dedekindZeta`, and Hironaka in characteristic 0. So a target can now also qualify because its
missing input is one of those.

**Open decision.** The tier table has no row for a theorem that imports riemann-hypothesis for
a lemma and never uses RH. Below such targets are written **U₀**: tier U's trust caveat applies
(untrusted cache, no licence, import only), but no RH hypothesis is discharged. Either add U₀
to `AGENTS.md` or decide this workspace doesn't take such targets.

### Build once: the GRH `ψ(x,χ)` bound

Under GRH, `|ψ(u,χ) − δ_χ u| ≤ C √u log²(qu)`, uniformly in the modulus `q`, from the repo's
truncated explicit formula and its zero count in unit windows (both hold for every primitive
character with one constant, ζ included). Targets 17, 21, 22 and the cheaper forms of #2, #5 and
#8 all reduce to it. Its constant is existential, so it helps `O(·)` statements and does nothing
for targets that end in a finite check.

### New candidates

| # | Target | Input from riemann-hypothesis | formal-conjectures statement | Tier | Effort |
|---|---|---|---|---|---|
| 17 | Bombieri–Vinogradov, via GRH | GRH, the `ψ(x,χ)` bound | `Wikipedia/ElliottHalberstamConjecture.lean`, `elliott_halberstam.variants.bombieri_vinogradov` | U | M |
| 18 | Erdős 696 | Siegel–Walfisz, Brun–Titchmarsh, Mertens | `ErdosProblems/696.lean` (solved) | U₀ | M |
| 19 | Erdős 694 | Linnik, Mertens | `ErdosProblems/694.lean` (solved) | U₀ | S–M |
| 20 | Erdős 456, Linnik variant | Linnik | `ErdosProblems/456.lean`, `erdos_456.variants.linniks_theorem` | U₀ | S |
| 21 | Pollack 2017 Thm 1.3 under GRH, then Erdős 1141 | GRH, the `ψ(x,χ)` bound | `ErdosProblems/1141.lean` | U | S–M, plus a port |
| 22 | Erdős 980, `k = 2`: mean of the least quadratic nonresidue | GRH, the `ψ(x,χ)` bound, ankeny-grh | `ErdosProblems/980.lean`, `erdos_980.variants.erdos_two` | U | M |
| 23 | Stark–Heegner (class number one), via GRH | GRH, imaginary-quadratic `ζ_K = ζ·L(χ)` | `Wikipedia/ClassNumberProblem.lean`, `variants.imaginary` (solved) | U | M–L |
| 24 | ERH for every abelian number field | RH, GRH, Kronecker–Weber, `dedekindZeta` continuation | none (formal-conjectures has `DedekindZetaRH` vocabulary only) | U | M–L |
| 25 | Hironaka's resolution in characteristic 0 | functorial resolution | `Wikipedia/ResolutionOfSingularities.lean`, `resolution_of_singularities_of_charZero` | U₀, or D | S |
| 26 | Zariski's local uniformisation in characteristic 0 | as 25, plus regular stalks of smooth schemes | `Wikipedia/LocalUniformization.lean` | U₀, or D | M |
| 27 | Auslander–Reiten over a regular local ring | Serre's theorem on projective dimension | `Paper/AuslanderReiten.lean`, `auslander_reiten.variants.regular_local` | U₀ | S–M |
| 28 | Cox: `p = x² + ny²` iff `p` splits completely in the Hilbert class field | Hilbert class field ≃ class group, Chebotarev density | none | U₀ | M |
| 29 | Kummer's criterion, the easy half, and `small_regular_primes` | Stickelberger, Bernoulli/L-value identities | `Wikipedia/RegularPrimes.lean` | U₀ | L |
| 30 | Littlewood: `π(x;4,3) − π(x;4,1)` changes sign infinitely often | GRH for `χ₄` | `Wikipedia/ChebyshevBias.lean`, `littlewood_mod_four_sign_changes` | U | L |
| 31 | Titchmarsh divisor problem | #17, Brun–Titchmarsh | none found *(search was rate-limited)* | U | M |
| 32 | Heilbronn / Siegel: `h(−d) → ∞` | Siegel's theorem, `L(1,χ) = πh/√d` | none | U₀ | M |

Notes on the rows that need one:

- **18, 19.** Complete Apache-2.0 Lean proofs already exist (davidturturean/erdos-696,
  Shashi456's Erdős 694) resting on three and two axioms. The repo proves those axioms. The
  work is statement conversion (`ψ`-form Siegel–Walfisz to `π(t;q,a)`, Mertens' second and
  third theorems from the first, with robin-rh's `mertens_const_eq_gamma`) and a port from Lean
  v4.27/v4.28.
- **20** is one lemma. Do it first, as the smoke test for importing a single module.
- **21.** The unconditional proof needs Burgess, which the repo lacks. The licence of the
  existing Lean deduction of Erdős 1141 (Jayyhk/erdos-lean) is unchecked.
- **24** unlocks less than it sounds. Weinberger's Euclidean rings, Bach's class-group
  generators and Hooley all need non-abelian fields.
- **25, 26.** [resolutionorg/hironaka](https://github.com/resolutionorg/hironaka) is a separate
  Apache-2.0 Lean library that proves Hironaka in Mathlib's terms. Its README says it has no
  `sorry` *(unverified)*. Using it makes both tier D with no riemann-hypothesis import. Neither
  is a consequence of RH, so decide whether they belong in this workspace.
- **28, 32** bridge the repo's internal `IsKroneckerChar` / `IsIdealClassPoint` to Mathlib's
  `classNumber`. 32 is ineffective and gives no finite list.

### Existing targets, re-costed

- **#1 idoneal numbers: a new route with no class number formula and no genus theory.** If `p`
  is an odd prime, `p ∤ n`, `−n` is a square mod `p` and `p² < n`, then `n = ab + bc + ca` with
  `0 < a < b < c`, which is formal-conjectures' definition of "not idoneal". Proof: pick `x`
  with `x² ≡ −n (mod p)` and `0 < x < p/2`, write `n + x² = p·m`, and take `a = x`,
  `b = p − x`, `c = m − x`; then `(a+b)(a+c) = n + a²` and `m > n/p > p`. Under GRH such a
  prime exists below `c·log²(4n)`, which leaves a finite check estimated at about `10⁶`
  *(not sized carefully)*. Still missing: an explicit Bach-style GRH bound for the least prime
  with `χ_{−4n}(p) = 1`, adapted from ankeny-grh. LLS Thm 1.4 does not serve: its `p ≤ 10⁹`
  escape clause pushes the finite range to about `10¹⁸`. This revises round 2's suggestion.
  Statement: `Wikipedia/IdonealCompleteness.lean`, `idoneal_numbers_completeness` (open).
- **#2, #5:** the `O`-forms `ψ(x) = x + O(√x log² x)` and gaps `O(√p log² p)` are effort S from
  the `ψ` bound. Schoenfeld's `1/(8π)` and Cramér's `√p log p` are unchanged.
- **#8 density hypothesis:** effort S. Zero counts in unit windows sum to `N(T) ≪ T log T`,
  with multiplicity; a bridge to `Complex.zeroCountOn` remains.
- **#9 Li's criterion:** `Σ 1/|ρ|² < ∞` is covered. "Infinitely many zeros" is still missing.
- **#10 Mertens function:** M, down from M–L. The repo's truncated Perron kernel is the
  sharp-cutoff formula this target lacked. The `1/ζ` bound is still ours to prove.
- **#13:** the class-number step is free (`L(1,χ) = πh/√d` is in the repo, for maximal orders).
- **Unchanged:** #7 Mills, #11 Nicolas, #12 LLS upgrade and the explicit half of #13. They end
  in explicit constants, and the repo's constants are existential. #6 ternary Goldbach stays
  blocked on the minor arcs.
- **artin-grh:** the repo's `dedekindZeta` continuation discharges `DedekindContinuation` once
  a strip bound is added. artin-grh PR #11 does this. `HooleyHypothesis` stays, so the result
  is tier C with no H hypothesis, not tier U.

### Rejected in round 3

- **Catalan / Mihăilescu.** Already proved in Lean 4 (cadamcat/catalan-lean4).
- **Anything Weil-bound shaped.** `WeilBound` contains no Weil bound, and `EtaleCohomology`
  states Poincaré duality and the Frobenius weights without proving them.
- **Unconditional Bombieri–Vinogradov at level 1/2, Vinogradov's three primes, Chowla.** The
  repo has the large sieve and Siegel–Walfisz, but no Vaughan identity, bilinear estimates or
  circle method.
- **Erdős 695, Erdős 980 for general `k`, Erdős–Halberstam proper.** Reasons in the analytic
  report.
- **Briançon–Skoda, Serre's dimension inequality, Fujita-type bounds.** Each is XL: they need
  convergent germ rings, Cohen's structure theorem or multiplier-ideal constructions that
  neither Mathlib nor the repo has.
- **Brouwer, invariance of domain, Hörmander, Markov, Lie–Trotter, Minkowski II,
  Harder–Narasimhan.** Proved in the repo, but no Atlas or formal-conjectures row turns on them.

## Recommended order

Revised in round 3:

1. **#20 Erdős 456 (Linnik)** as the smoke test for importing one module and running
   `#print axioms` on it. Settle the U₀ question at the same time.
2. **The GRH `ψ(x,χ)` bound** as a shared library, then **#17 Bombieri–Vinogradov**, the
   `O`-forms of **#2 / #5**, **#8 density hypothesis**, **#21** and **#22**.
3. **#1 idoneal numbers by the split-prime route**, then **#23 Stark–Heegner**, which shares the
   least-split-prime bound. #1 is the only open formal-conjectures statement here that looks
   reachable at tier U.
4. **#19 and #18**, ports of existing proofs with their axioms discharged.
5. **#2 with Schoenfeld's constant**, then **#7 Mills**; **#4 Dirichlet-L Lindelöf**;
   **#3 / #12** least primes via LLS; **#9 Li's criterion**.
6. **Later:** #10 Mertens, then #16; #24 ERH for abelian fields; #28; #32; #11; #13; #15; #14;
   #29; #30; #31. **#25–#27** only if non-RH algebraic geometry belongs here.

Use the workflow that worked for lindelof-rh: fix every step's Lean statement in
`<Pkg>/Statement.lean` and prove the assembly first, then run parallel agents on one step each,
in separate worktrees.

## Considered and rejected

Kept so the next search doesn't rediscover these and argue about them again.

- **Gilbreath, binary Goldbach, twin primes, Legendre, Cramér's conjecture.** Not consequences of
  RH. Unreachable even with it.
- **Unconditional Artin.** Hooley's hypothesis is RH for the zeta functions of the Kummer fields
  `ℚ(ζ_k, a^(1/k))`, which are non-abelian over ℚ for `k > 2`. Their zeta functions are not
  products of Dirichlet L-functions. Even with Hecke's continuation formalised, riemann-hypothesis
  cannot discharge it. artin-grh's target stays "C + Hecke formalised".
- **Closing robin-rh's or grosswald-grh's computed range by brute force.** Morrill–Platt
  (`5040 < n ≤ exp(e^30)`) and Cohen–Oliveira e Silva–Trudgian (`409 < p ≤ 2.5·10^15`, about
  7·10^13 primes) are far beyond `native_decide`. The only route to tier U is a new argument that
  lowers the analytic threshold. See their checklist items in `AGENTS.md`.
- **Weil positivity and Beurling–Nyman** (formal-conjectures `_rhs` forms). The RH ⇒ criterion
  direction needs the full Weil explicit formula for `C_c^∞` test functions, or the hard
  direction of Nyman–Beurling. XL.
- **Knapowski–Turán refutation** (Kaczorowski, Analysis 15 (1995)). Needs oscillation theorems and
  certified zero data for `L(s, χ₄)`.
- **Montgomery pair correlation and zeta-moment asymptotics.** Not consequences of RH.
  **Rubinstein–Sarnak** needs the linear independence hypothesis (LI).
- **Euclidean rings of integers (Weinberger 1973) and Breuillard–Varjú.** Need GRH for Dedekind
  zeta of non-abelian fields.
- **Lagarias's criterion.** Already proved as `lagarias_of_RH` in robin-rh. Upstream it to
  formal-conjectures (`lagarias_criterion_rhs` / `robin_criterion_rhs`) rather than redoing it.
- **Báez-Duarte criterion.** No formal-conjectures statement, and less famous; fold it into #16 if
  wanted.

## See also

- The lemma inventory behind round 3: [`rh-lemmas/README.md`](rh-lemmas/README.md).
- Reasoning behind these choices is recorded in LivingBrain (see `AGENTS.md`, "Memory").
- The Conjecture Atlas note with the same ranking:
  [senamakel/tiny-cortexdb-mathagent#1](https://github.com/senamakel/tiny-cortexdb-mathagent/pull/1).
