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

**Tier U₀.** A theorem that imports riemann-hypothesis for one of those lemmas and never uses
RH is tier **U₀** (decided 2026-11-24, defined in `AGENTS.md`): tier U's trust caveat applies,
but no RH or GRH hypothesis is discharged. Algebraic geometry and commutative algebra targets
belong in this workspace too (#25–#27).

### Build once: the GRH `ψ(x,χ)` bound

Under GRH, `|ψ(u,χ) − δ_χ u| ≤ C √u log²(qu)`, uniformly in the modulus `q`. Targets 17, 21, 22,
31 and the cheaper forms of #2, #5 and #8 all reduce to it. Its constant is existential, so it
helps `O(·)` statements and does nothing for targets that end in a finite check. Brief H0 below.

### New candidates

| # | Target | Input from riemann-hypothesis | formal-conjectures statement | Tier | Effort |
|---|---|---|---|---|---|
| 17 | Bombieri–Vinogradov, via GRH | GRH, the `ψ(x,χ)` bound | `Wikipedia/ElliottHalberstamConjecture.lean`, `elliott_halberstam.variants.bombieri_vinogradov` | U | M |
| H0 | The GRH `ψ(x,χ)` bound (shared library) | GRH, truncated explicit formula, zero counts | none | U | S–M |
| 18 | Erdős 696 | Siegel–Walfisz, Brun–Titchmarsh, Mertens | `ErdosProblems/696.lean` (solved) | U₀ | M |
| 19 | Erdős 694 | Linnik, Mertens | `ErdosProblems/694.lean` (solved) | U₀ | S–M |
| 20 | Erdős 456, Linnik variant | Linnik | `ErdosProblems/456.lean`, `erdos_456.variants.linniks_theorem` | U₀ | S |
| 21 | Pollack 2017 Thm 1.3 under GRH, then Erdős 1141 | GRH, the `ψ(x,χ)` bound | `ErdosProblems/1141.lean` | U | S–M, plus a port |
| 22 | Erdős 980, `k = 2`: mean of the least quadratic nonresidue | GRH, the `ψ(x,χ)` bound, ankeny-grh | `ErdosProblems/980.lean`, `erdos_980.variants.erdos_two` | U | M |
| 23 | Stark–Heegner (class number one), via GRH | GRH, imaginary-quadratic `ζ_K = ζ·L(χ)` | `Wikipedia/ClassNumberProblem.lean`, `variants.imaginary` (solved) | U | M–L |
| 24 | ERH for every abelian number field | RH, GRH, Kronecker–Weber, `dedekindZeta` continuation | none (formal-conjectures has `DedekindZetaRH` vocabulary only) | U | M–L |
| 25 | Hironaka's resolution in characteristic 0 | functorial resolution (or resolutionorg/hironaka) | `Wikipedia/ResolutionOfSingularities.lean`, `resolution_of_singularities_of_charZero` | U₀, or D | S |
| 26 | Zariski's local uniformisation in characteristic 0 | as 25, plus regular stalks of smooth schemes | `Wikipedia/LocalUniformization.lean` | U₀, or D | M |
| 27 | Auslander–Reiten over a regular local ring | Serre's theorem on projective dimension | `Paper/AuslanderReiten.lean`, `auslander_reiten.variants.regular_local` | U₀ | S–M |
| 28 | Cox: `p = x² + ny²` iff `p` splits completely in the Hilbert class field | Hilbert class field ≃ class group, Chebotarev density | none | U₀ | M |
| 29 | Kummer's criterion, the easy half, and `small_regular_primes` | Stickelberger, Bernoulli/L-value identities | `Wikipedia/RegularPrimes.lean` | U₀ | L |
| 30 | Littlewood: `π(x;4,3) − π(x;4,1)` changes sign infinitely often | GRH for `χ₄` | `Wikipedia/ChebyshevBias.lean`, `littlewood_mod_four_sign_changes` | U | L |
| 31 | Titchmarsh divisor problem | #17, Brun–Titchmarsh | none found *(search was rate-limited)* | U | M |
| 32 | Heilbronn / Siegel: `h(−d) → ∞` | Siegel's theorem, `L(1,χ) = πh/√d` | none | U₀ | M |

The briefs below carry everything the three reports found. Paths are relative to
`riemann-hypothesis/src/` at `507a75d91d`. "Opened" means an agent read that Lean statement;
"inventory" means it is known only from the inventory tables. Every declaration name must be
confirmed with `#check` before anything is built on it.

### How to run a target

This is the same for every brief, so it is written once.

1. **Read first.** `AGENTS.md` (tiers, rules 1–7, README rules), this brief, the inventory file
   the brief cites, and LivingBrain for the target's name (dead ends and constants are there).
2. **Create the repo.** `senamakel/<slug>`, Lean `v4.36.0`, Mathlib `fc4f59e5`, requiring
   erdos-985 at `9538edb` over HTTPS (rule 7). riemann-hypothesis is on the same toolchain and
   Mathlib pin, so its modules import directly. Add the repo as a submodule here, give it a row
   in `README.md` and a section in the `AGENTS.md` checklist.
3. **Fix the statement.** Put the target in `<Pkg>/Statement.lean`. If formal-conjectures has
   it, copy it word for word and link it (rule 3). Don't edit it later to make a proof go
   through; if you prove something weaker, state the weaker theorem and say why in the README.
4. **Smoke-test every imported lemma before building on it.** Write a scratch file that imports
   the one module, `#check`s the declaration and runs `#print axioms` on it. Compile it the way
   `erdos-985/scripts/check-unconditional.sh` does: `LEAN_PATH` from `lake env printenv
   LEAN_PATH` in the riemann-hypothesis checkout, then `lean <file>`. A single `GroundTheory`
   module cost 17 s and 6.6 GB of RAM in artin-grh PR #11; the full `Main` import costs 93 GB
   of cache and 19 GB of RAM. If the axiom list has anything beyond `propext`,
   `Classical.choice` and `Quot.sound`, stop and record it.
5. **Check the definitions, not only the statement.** For each imported lemma that mentions a
   repo-internal definition (`IsKroneckerChar`, `psi0`, `IsBlowup`, `piMod`, …), open the
   definition and write a bridging lemma to the Mathlib object. Record anything degenerate.
6. **Keep the layering.** The main library never imports riemann-hypothesis (rule 1). An
   imported lemma enters the main library as an explicit `Prop` hypothesis whose definition is
   stated in Mathlib terms. `Unconditional/<X>Unconditional.lean` imports the repo and
   discharges each hypothesis in one line. For a U₀ target the hypotheses are the imported
   classical lemmas (Siegel–Walfisz, Linnik, …) instead of RH.
7. **No copying.** riemann-hypothesis has no licence: import it, never paste from it. The
   Apache-2.0 proofs named in #18, #19 and #25 may be vendored with a NOTICE and a Credits
   section (README rule 11).
8. **Assemble first, then fan out.** Prove the top-level assembly from the stated steps with the
   steps as hypotheses, then give one step to each agent in its own worktree
   (`worktree <slug>` at the superproject level).
9. **Finish.** Paste real `#print axioms` output into the README, add
   `scripts/check-unconditional.sh`, tick the checklist in `AGENTS.md`, bump the gitlink, and
   write to LivingBrain whatever git won't hold: an approach that failed, a constant you sized.

### H0. The GRH `ψ(x,χ)` bound (shared library; build before #17, #21, #22, #31)

- **Statement to prove.** Under `hGRH : DirichletLNonvanishingRightOfHalf`: there is `C > 0`
  such that for every `N` with `[NeZero N]`, every Dirichlet character `χ` mod `N` and every
  `u ≥ 2`, `|ψ(u,χ) − δ_χ·u| ≤ C·√u·log²(N·u)`, where `ψ(u,χ) = Σ_{n≤u} Λ(n)χ(n)` and
  `δ_χ = 1` for the principal character, `0` otherwise. `N = 1` gives ζ.
- **Where it lives.** A new module in erdos-985 (the analytic toolkit root), or a small new
  repo `grh-psi` required by the targets that use it. Decide before starting; erdos-985 is
  preferred because every sibling already requires it.
- **Inputs (both opened).**
  - `GlobalTheory.ExplicitFormula.truncated_explicit_formula`,
    `Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/TruncatedExplicitFormula.lean:16`.
    Shape: `∃ C > 0, ∀ N [NeZero N] χ, χ.IsPrimitive → …`, uniform in `N`, `χ`, `T` and `u`.
    Its `psi0` is `Σ_{n ≤ ⌊u⌋} Λχ − [N=1]·u`. It carries an extra term
    `Σ_{|Im ρ|<1} m_ρ/‖ρ‖`.
  - `GlobalTheory.ZeroWindow.count_zeros_window`,
    `…/GlobalInterpolation/FinsumMemLeOfSubset.lean:31`. Zeros in a unit window number at most
    `C·log(N(|t|+2))`, counted with multiplicity through `analyticOrderNatAt`, uniformly in the
    conductor.
  - `Claim.prim_zero` and `UpperTheory.Top.imprimitive`
    (`Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean`, `Imprimitive.lean`)
    for the reduction to primitive characters.
- **Steps.**
  1. Under GRH every nontrivial zero has `Re ρ = 1/2`, so `|u^ρ/ρ| = √u/|ρ|` and `|ρ| ≥ 1/2`.
     The extra term is then at most `C·log 2N` by the window count.
  2. Sum `√u/|ρ|` over `|Im ρ| ≤ T` using the window count: `≪ √u·log T·log(NT)`.
  3. Take `T = u` (or `√u`); the truncation error in the formula becomes `≪ log²(Nu)`.
  4. Imprimitive `χ` mod `N` induced by primitive `χ*`: the two `ψ` differ only at prime powers
     of primes dividing `N`, a difference of at most `log N·log u`.
- **Missing.** Only the bookkeeping above. No new analysis.
- **Risks.** The constant is existential, so this library serves `O(·)` targets only. The
  explicit formula's exact error term and its range of `T` were read, not typechecked: confirm
  them in step 4 of "How to run a target" before writing step 2.
- **Module cost.** `TruncatedExplicitFormula` has about 203 repo files in its import closure
  *(count from one agent, not rebuilt)*.
- **Tier.** The bound is tier C in the main library; its `Unconditional/` discharge is tier U.
- **Effort.** S–M.

### 17. Bombieri–Vinogradov via GRH

- **Statement.** formal-conjectures `Wikipedia/ElliottHalberstamConjecture.lean`,
  `elliott_halberstam.variants.bombieri_vinogradov`. For fixed `x`,
  `E x q = ⨆ a : (ZMod q)ˣ, |π(x;q,a) − π(x)/φ(q)|`, and for every `θ < 1/2` and `A`,
  `Σ_{q ≤ ⌊x^θ⌋} E x q ≤ C·x/log^A x`. There is no maximum over `y ≤ x`; that maximum is what
  forces Vaughan's identity and the maximal large sieve in the unconditional proof, and it is
  absent here. Atlas row `wiki-elliott-halberstam-conjecture`. Copy the statement verbatim and
  confirm this reading of it.
- **Source.** Bombieri 1965; A. I. Vinogradov 1965. Under GRH it is immediate.
- **Repo.** `bombieri-vinogradov-grh`. **Tier** C in the main library
  (`bombieri_vinogradov_of_GRH (hGRH : DirichletLNonvanishingRightOfHalf)`), U in
  `Unconditional/`. **Effort** M. **Depends on** H0.
- **Steps.**
  1. Orthogonality of characters: `ψ(x;q,a) − ψ(x)/φ(q)` is an average of `χ̄(a)ψ(x,χ)` over
     non-principal `χ` mod `q`, so H0 gives `≪ √x·log²(qx)` uniformly in `a`.
  2. Remove prime powers and primes dividing `q` (`≪ √x` and `≪ log q`).
  3. Pass from `ψ` to `π` by partial summation. Only fixed-`t` bounds appear inside
     `∫ θ(t)/(t log² t) dt`, so no maximum over `y` is needed here either.
  4. Sum over `q ≤ x^θ`: `≪ x^{θ+1/2}·log² x ≤ C·x/log^A x` for `θ < 1/2`.
- **Missing.** H0, and the `⨆` over units handled as a finite supremum.
- **Unlocks.** #31. H0 also feeds #21 and #22.

### 18. Erdős 696

- **Statement.** formal-conjectures `ErdosProblems/696.lean`, `erdos_696` (marked solved):
  `H(n)/h(n) → 2` for almost all `n`. Atlas row `erdos-696`. Read the file for the definitions
  of `H` and `h`.
- **Existing proof.** davidturturean/erdos-696, Apache-2.0, Lean v4.28. Complete except for
  three axioms in `Erdos696/AnalyticInputs.lean`: Siegel–Walfisz, Brun–Titchmarsh and Mertens.
- **Repo.** `erdos-696`, vendoring that proof with a NOTICE. **Tier** U₀. **Effort** M.
- **Inputs (opened).**
  - `Formalism.ZeroFreeDirichlet.siegelWalfisz`,
    `Formalism/LandauZeroFreeBounds/SiegelWalfiszAPOfSiegelLower.lean:38`, with
    `chebyshev_progression_orthogonality`. Stated for `ψ(x,χ)` with `q ≤ (log x)^A`, uniform
    `c` and `C`, main term "if `χ = 1` then `x`".
  - `GlobalTheory.Lin.brun_titchmarsh_const`,
    `Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/BrunTitchmarshExistsConst.lean:53`,
    explicit constant 48. With `primesIoc 0 t` filtered by `p ≡ a [MOD q]` and `t ≥ 2q` it gives
    `piMod t q a ≤ C·t/(φ(q)·log(t/q))`, which is the axiom with `x = 0`.
  - `GlobalTheory.mertens_first_vonMangoldt`,
    `…/IwasawaDecomposition/LogFactorialEqSumVonMangoldtMulDiv.lean:64`:
    `|Σ_{n≤y} Λ(n)/n − log y| ≤ log 4 + 4`.
- **Steps.**
  1. Port the vendored proof from v4.28 to v4.36 with the three axioms turned into `Prop`
     hypotheses of the main theorem.
  2. Siegel–Walfisz: convert the `ψ(x,χ)` form to the axiom's `π(t;q,a) − li(t)/φ(q)` form by
     orthogonality and partial summation. The error keeps its `exp(−c√log)` shape.
  3. Mertens: the axiom wants `|Σ_{p≤t} 1/p − log log t − M| ≤ C/log t`. Get it from the first
     theorem by Abel summation. First check whether Mathlib at the pin already has it; no agent
     did.
  4. Discharge the three hypotheses in `Unconditional/`.
- **Risks.** `piMod`'s floor convention must match the axiom's. The port may be the bulk of
  the work.

### 19. Erdős 694

- **Statement.** formal-conjectures `ErdosProblems/694.lean`, `erdos_694` (solved):
  `max f_max/f_min = (e^γ + o(1))·log log x`. Atlas row `erdos-694`.
- **Existing proof.** Shashi456/erdos-formalizations, `Erdos/P694/Proof.lean`, Apache-2.0, Lean
  v4.27, complete except for the axioms `linnik_dvd` and `mertens_product`.
- **Repo.** `erdos-694`. **Tier** U₀. **Effort** S–M.
- **Inputs.**
  - `UpperTheory.T3.smallOne`, `Development/AutomorphicArithmetic/ShortNorms/Primes.lean`
    (opened): for `M ≥ 2` there is a prime `p ≡ 1 (mod M)` with `p ≤ M^A`, `A ≥ 1` real.
  - `GlobalTheory.mertens_first_vonMangoldt` (as in #18).
  - robin-rh's `Robin.mertens_const_eq_gamma`, proved unconditionally from convergence.
- **Steps.**
  1. `linnik_dvd`: take the natural exponent `L = ⌈A⌉`; for `M = 1` use `ℓ = 2`.
  2. `mertens_product` (`∏_{p≤y} p/(p−1) ~ e^γ·log y`): prove that
     `Σ_{p≤x} −log(1−1/p) − log log x` converges, from Mertens' first theorem; then
     `mertens_const_eq_gamma` identifies the limit as `γ`.
  3. Port from v4.27 and discharge in `Unconditional/`.
- **Note.** Step 2 is shared with #18's Mertens work and with #21's `mertens_third`. Put it in
  one place (robin-rh already owns the constant).

### 20. Erdős 456, Linnik variant (do this first)

- **Statement.** formal-conjectures `ErdosProblems/456.lean`,
  `erdos_456.variants.linniks_theorem`: with `p n = sInf {k | k.Prime ∧ k ≡ 1 [MOD n]}`,
  `∃ L, (fun n ↦ (p n : ℝ)) =O[atTop] (fun n ↦ n ^ L)`. Atlas row `erdos-456`.
- **Repo.** `linnik` (or a first module of a shared `rh-imports` library). **Tier** U₀.
  **Effort** S, about 50 lines.
- **Inputs.** `UpperTheory.T3.smallOne` (as in #19), or `UpperTheory.Lit.linnik`,
  `Development/AutomorphicArithmetic/ThetaCorrespondence/Linnik.lean:146` (opened; faithful
  statement, no explicit exponent). `GlobalTheory.Published.Linnik`
  (`Development/AbelianVarietyTheory/PublishedTheorems/PublishedFoundations/PrimesInProgressionNonempty.lean:13`)
  is the same result as a `Prop`.
- **Steps.** Unfold `sInf`; handle `n ≤ 1`; convert the pointwise bound to `=O[atTop]`.
- **Why first.** It exercises the whole pipeline (single-module import, `#print axioms`, the
  hypothesis-then-discharge layout for U₀) at almost no mathematical cost. Record the import's
  time, RAM and module count in the README and in LivingBrain; every later brief needs them.

### 21. Pollack's theorem under GRH, then Erdős 1141

- **Statement.** formal-conjectures `ErdosProblems/1141.lean`:
  `erdos_1141.variants.pollack_1_3`, `.mertens_third`, then `erdos_1141` (solved). Atlas row
  `erdos-1141`.
- **Source.** Pollack, Proc. AMS 145 (2017) 2815–2826, arXiv:1508.05035, Thm 1.3 (confirmed):
  for `ε, A > 0` there is `m₀` such that every quadratic `χ` mod `m > m₀` has at least
  `(log m)^A` primes `ℓ ≤ m^{1/4+ε}` with `χ(ℓ) = 1`.
- **Repo.** `erdos-1141`. **Tier** U. **Effort** S–M, plus a port (M). **Depends on** H0.
- **Why GRH.** Pollack's proof uses Burgess (Norton) and Siegel. The repo has no Burgess
  bound. Under GRH it is one application of H0.
- **Steps.**
  1. At `y = m^{1/4+ε}`: `Σ_{ℓ≤y} (1+χ(ℓ))·log ℓ = y + O(√y·log²(my))` by H0 for `χ` and for
     the trivial character (which `IsQuadratic` allows). So the count is `≫ y/log y ≥ log^A m`.
  2. Imprimitive to primitive: the primes `ℓ ∣ m` number at most `log m`.
  3. `mertens_third` in its weak form `∏_{p≤n}(1−1/p) ≥ 1/(3·log n)`: S, shared with #19.
  4. Port the published deduction of `erdos_1141` from Pollack's theorem.
- **Unverified.** The deduction is formalised in Jayyhk/erdos-lean, whose licence nobody
  checked. Check it before vendoring; if it has none, re-prove the deduction.

### 22. Erdős 980, `k = 2`: the mean of the least quadratic nonresidue

- **Statement.** formal-conjectures `ErdosProblems/980.lean`, `erdos_980.variants.erdos_two`
  (solved): `lim π(x)^{−1}·Σ_{2<p≤x} n₂(p) = Σ_k p_k/2^k ≈ 3.67464`. Atlas row `erdos-980`.
- **Source.** Erdős, Mat. Lapok 12 (1961); constant confirmed in Martin–Pollack, JLMS 2012,
  eq. (1.1).
- **Repo.** `erdos-980`, requiring ankeny-grh. **Tier** U. **Effort** M. **Depends on** H0.
- **Steps.**
  1. For fixed `K`, the density of primes `p` for which `p_1, …, p_{k−1}` are residues and `p_k`
     is not is `2^{−k}`: expand the indicator as a sum of products of Kronecker symbols and
     apply H0 to the `2^k` real characters mod `8·∏_{i≤K} p_i`. Quadratic reciprocity comes
     from Mathlib.
  2. Tail: `#{p ≤ x : p_1, …, p_K all residues} ≪ 2^{−K}·π(x)`, and `n₂(p) ≤ (21/5)·log² p`
     from ankeny-grh's `leastNonresidue_of_GRH`.
  3. Choose `K ≈ 3·log log x / log 2` and track uniformity in `K` (the modulus grows like
     `e^{K log K}`, which H0's `log²(qx)` absorbs).
- **Out of reach.** General `k` (Elliott) needs Chebotarev in the non-abelian Kummer fields
  `ℚ(ζ_k, p^{1/k})`, the same obstruction as artin-grh.

### 1 (revised). Idoneal numbers by the split-prime route

- **Statement.** formal-conjectures `Wikipedia/IdonealCompleteness.lean`,
  `idoneal_numbers_completeness` (**research open**). formal-conjectures defines `IsIdoneal n`
  as "`n` is not `ab + bc + ca` with `0 < a < b < c`" (Rains' form, OEIS A000926). The converse,
  `knownIdonealNumbers_are_idoneal`, is already proved there. Atlas row `wiki-idoneal-number`.
- **Source.** Weinberger, Acta Arith. 22 (1973) 117–124; Kani, Ann. Sci. Math. Québec 35
  (2011), Cor. 23 and Remark 24. Unconditionally at most two more idoneal numbers exist, none
  below `7.75·10^19` (OEIS A000926), so a tier-U proof is a formal result on an open problem.
- **Repo.** `idoneal-grh`, requiring erdos-985 and ankeny-grh. **Tier** U. **Effort** M.
- **Step 1, the witness lemma (elementary, about ten lines).** Let `p` be an odd prime with
  `p ∤ n`, `−n` a square mod `p`, and `p² < n`. Then `n` is not idoneal.
  Proof: pick `x` with `x² ≡ −n (mod p)` and `0 < x < p/2`. Write `n + x² = p·m`. Put
  `a = x`, `b = p − x`, `c = m − x`. Then `(a+b)(a+c) = p·m = n + a²`, so `ab + bc + ca = n`.
  `a < b` because `x < p/2`. `b < c` because `m > n/p > p`. This derivation came from one
  agent and was re-checked by hand; it has not been checked in Lean.
- **Step 2, the analytic bound (the real work).** Under GRH, for `n` above an explicit
  threshold there is an odd prime `p ∤ n` with `χ_{−4n}(p) = 1` and `p ≤ c·log²(4n)`, with an
  explicit `c`. This is the coset form of ankeny-grh's `BachSubgroupBound`: weight `(1 + χ)`
  instead of the characters trivial on a subgroup. Reuse ankeny-grh's explicit formula and
  erdos-985's zero sums; expect a constant near ankeny's `21/5` at first. The repo's H0 inputs
  don't help, because their constants are existential.
- **Step 3, the finite range.** `p² < n` holds once `c²·log⁴(4n) < n`. For `c ≈ 4` that is
  `n` above roughly `10^6` *(order of magnitude from one agent; size it against the `c`
  actually proved before choosing the checker design)*. Below it, supply a witness `(a, b, c)`
  for every `n` not on the list of 65, checked with `native_decide` and a proved-sound checker
  (rule 5).
- **Do not use.** LLS Thm 1.4 (arXiv:1309.3595): its "either `p ≤ 10⁹` or …" escape clause
  pushes the finite range to about `10^18`. The class number formula and genus theory are not
  needed on this route; the repo's formula covers maximal orders only, and `−4n` is usually not
  fundamental.
- **Done when.** `idoneal_numbers_completeness_of_GRH` (C) and its one-line discharge (U), with
  the `native_decide` count and timing in the README.

### 23. Stark–Heegner (class number one) via GRH

- **Statement.** formal-conjectures `Wikipedia/ClassNumberProblem.lean`,
  `class_number_problem.variants.imaginary` (research solved), stated with
  `AdjoinRoot (X² − C d)`. Atlas row `wiki-class-number-problem`. Mathlib has no proof.
- **Repo.** `class-number-one-grh`, sharing step 2 of #1. **Tier** U. **Effort** M–L.
  **Depends on** #1's analytic bound.
- **Inputs (opened).** `GlobalTheory.QuadraticZeta.idealCount_eq_sum` and
  `exists_isKroneckerChar`,
  `Development/AbelianVarietyTheory/Proofs/HomogeneousIdeals/ExistsIsKroneckerCharOfDiscr.lean:358, :458`:
  for `K` with `finrank = 2` and `discr K = −d`, the number of ideals of norm `m` is
  `Σ_{e∣m} χ(e)`. So `χ(p) = 1` gives an ideal of norm `p`.
- **Steps.**
  1. If `h = 1`, an ideal of norm `p` is principal, generated by `α ∉ ℤ` with `N(α) = p`. But
     `N(α) ≥ |D|/4` for `α ∉ ℤ`. So every prime `p < |D|/4` is inert.
  2. The least split prime is `≤ c·log²|D|` under GRH (#1, step 2), so `|D|` is bounded by a few
     hundred.
  3. Finite check of the remaining discriminants.
  4. `h = 1` for the nine fields: Mathlib's `isPrincipalIdealRing_of_abs_discr_lt` covers
     `|D| ≤ 8`; Minkowski's bound with the primes up to 8 covers the rest.
- **Cost centre.** formal-conjectures' encoding: prove
  `discr (AdjoinRoot (X² − d)) = quadFundDisc d` and describe its ring of integers. The pin has
  `Algebra/QuadraticAlgebra`; how far it goes is unknown.
- **Rejected route.** Unconditional Heegner through CM: the repo has the main theorem of CM,
  `K(j) = H_K`, integrality of singular moduli and `f·f₁·f₂ = √2`, but not Weber's algebraicity
  of `f(√−m)^k`. XL.

### 24. ERH for every abelian number field

- **Statement.** New. Use formal-conjectures' `IsDedekindZeta` / `DedekindZetaRH` vocabulary
  (`Millennium/RiemannHypothesis.lean` leaves ERH unstated until a continuation of
  `dedekindZeta` exists): for `K/ℚ` abelian, every zero of `ζ_K` with `0 < Re s < 1` has
  `Re s = 1/2`.
- **Repo.** `abelian-erh`. **Tier** U. **Effort** M–L.
- **Inputs.**
  - `UpperTheory.V.CF.kwHom`,
    `Development/AutomorphicArithmetic/AutomorphicVarieties/GaloisLibrary/ClassFieldRamification/KwHom.lean:13`
    (opened): an abelian `K` embeds in `CyclotomicField N ℚ`. Also `kw`, `kwRam`.
  - `continuedDedekindZeta`, `continuedDedekindZeta_eq`, `completedDedekindZeta_one_sub`,
    `GroundTheory/GlobalFields/TateThesis/Dedekind{Zeta,}Continuation.lean` (opened).
  - `dedekindZeta_eq_exp`,
    `Development/WeilBound/…/ZetaEulerProducts/SummablePrimesRpow.lean:13` (inventory 05): the
    Euler product of `dedekindZeta`.
  - `LFunction_ne_zero_of_half_lt_re` and `riemannHypothesis`.
- **Steps.**
  1. Embed `K` in `ℚ(ζ_N)`. Let `X(K)` be the Dirichlet characters mod `N` trivial on
     `Gal(ℚ(ζ_N)/K)`, imprimitive ones allowed.
  2. For `Re s > 1`: `ζ_K(s) = E(s)·∏_{χ∈X(K)} L(s,χ)` with
     `E(s) = ∏_{p∣N} ∏_{𝔭∣p} (1 − N𝔭^{−s})^{−1}`. Only unramified `p` need an Euler-factor
     identity: Frobenius of `p` is `p`, and
     `∏_{𝔭∣p}(1 − N𝔭^{−s}) = ∏_χ (1 − χ(p)p^{−s})` by orthogonality. Working mod `N` with
     imprimitive characters avoids all conductor and inertia bookkeeping, because `E` is
     holomorphic and zero-free on `Re s > 0`.
  3. On `Re s > 1/2`, `s ≠ 1`: any `Z` with `IsDedekindZeta K Z` equals `E·∏L` by the identity
     theorem, hence is nonzero by GRH.
  4. On `0 < Re s < 1/2`: the functional equation, with the gamma factors nonzero.
- **Missing.** The Euler-factor identity, and "Frobenius at `p` is `p`" in `ℚ(ζ_N)`
  (`GroundTheory/GlobalFields/CyclotomicCharacters/Frobenius.lean` may have it; not opened).
- **What it does not unlock.** Checked case by case: Weinberger's Euclidean rings (Kummer
  fields of units, non-abelian), Bach's class-group generator bound (Hilbert class field,
  generalised dihedral over ℚ), Miller's real-cyclotomic class numbers (Odlyzko bounds on the
  Hilbert class field; confirmed from arXiv:1407.2373), Hooley (`k ≥ 3`). Its value is the
  headline and the factorisation lemma, which #29 reuses.

### 25. Hironaka's resolution of singularities in characteristic 0

- **Statement.** formal-conjectures `Wikipedia/ResolutionOfSingularities.lean`,
  `resolution_of_singularities_of_charZero` (research solved, `sorry`): an integral, separated,
  finite-type scheme `X` over a field of characteristic 0 has `Y` integral and smooth over `k`
  with `Y → X` proper and birational. Atlas row `wiki-resolution-of-singularities` (open only
  because of characteristic `p`).
- **Source.** Hironaka, Ann. Math. 79 (1964).
- **Repo.** `hironaka-fc`. **Effort** S. **Tier** depends on the source chosen:
  - **D**, from [resolutionorg/hironaka](https://github.com/resolutionorg/hironaka):
    Apache-2.0, Lean v4.35.0, created 2026-09-30, `AlgebraicGeometry.exists_isBlowUpAlong_smooth`
    plus Kollár's functorial resolution and principalisation. Its README claims no `sorry`,
    comparator-checked, standard axioms only. **None of that is verified here**, and it is on
    a different toolchain. Check both first.
  - **U₀**, from riemann-hypothesis: `FunctorialResolution.functorialResolutionCharZero`,
    `Development/ResolutionOfSingularities/HasSimpleNormalCrossingsOfInStrictNormalCrossing.lean:19`
    (opened). Its rule `IsResolutionRuleCharZero` takes `k : Type u` of characteristic 0 and
    `X : Scheme.{u}` reduced, quasi-compact and locally of finite type over `Spec k`, and
    returns a finite blowup tower whose top is smooth over `k`, proper over `X`, an isomorphism
    over `f.smoothLocus` with dense preimage, and with SNC exceptional locus. Separatedness is
    not required, so the formal-conjectures hypotheses are stronger and the match is exact.
    `IsBlowup` is the universal property, built on Mathlib's `IdealSheafData.comap`.
  Prefer D if the checks pass; keep riemann-hypothesis as the fallback.
- **Steps (the same glue for either source).**
  1. `Y` is reduced: `isReduced_of_smooth`,
     `Development/ResolutionOfSingularities/EmbeddedResolution/EtaleCoordinates/SmoothRegular.lean:256`.
  2. `Y` is irreducible: the preimage of the smooth locus is dense in `Y` and isomorphic to an
     open of the irreducible `X`. The smooth locus is dense by Mathlib's
     `Scheme.Hom.dense_smoothLocus_of_perfectField`.
  3. The two opens form a Mathlib `PartialIso` over the identity of `X`, giving
     `Scheme.BirationalOver`.
  4. `isIntegral_of_irreducibleSpace_of_isReduced` closes integrality.
- **Unverified.** Only the top two levels of the riemann-hypothesis proof were traced.

### 26. Zariski's local uniformisation in characteristic 0

- **Statement.** formal-conjectures `Wikipedia/LocalUniformization.lean`,
  `local_uniformization_of_charZero` (research solved, `sorry`); the predicate is
  `HasLocalUniformization`. No Atlas row.
- **Source.** Zariski, Ann. Math. 41 (1940) 852–896 (confirmed).
- **Repo.** With #25. **Tier** as #25. **Effort** M. **Depends on** #25's resolution input.
- **Inputs.** As #25, plus `isRegularLocalRing_stalk_of_smooth` (`SmoothRegular.lean:228`,
  opened): for `k : Type u`, `X : Scheme.{u}` smooth over `Spec k` and any point, the stalk is
  Mathlib's `IsRegularLocalRing`.
- **Steps.**
  1. Given the valuation ring `𝒪 ⊆ F`, pick an affine model `B = k[y₁..yₙ] ⊆ 𝒪` with each `yᵢ`
     equal to `xᵢ` or `xᵢ⁻¹`. No projective closure is needed.
  2. Resolve `Spec B`.
  3. Lift `Spec 𝒪` through the proper resolution map with Mathlib's valuative criterion
     (`ValuativeCriterion`, `IsProper.eq_valuativeCriterion`).
  4. Take an affine chart `A` at the centre; its localisation at the centre is the stalk, which
     is regular.
- **Friction.** Universes: formal-conjectures has `k` and `F` in independent universes, while
  the resolution rule needs `Scheme.{u}` with `k : Type u`. Also identifying `Γ(U)` with a
  subalgebra of `F`.

### 27. Auslander–Reiten over a regular local ring

- **Statement.** formal-conjectures `Paper/AuslanderReiten.lean`,
  `auslander_reiten.variants.regular_local` (textbook, `sorry`): over a regular local ring,
  `Extⁱ(M, R) = 0` for all `i > 0` implies `M` free. `R` and `M` share a universe, which fits
  the input.
- **Repo.** `regular-local` (a commutative-algebra repo; #27 is its first theorem).
  **Tier** U₀, or D if Serre's theorem is re-proved (about +M). **Effort** S–M.
- **Input (opened).** `GroundTheory.Arith.SchemeCoh.hasProjectiveDimensionLT_of_isRegularLocalRing`,
  `GroundTheory/ArithmeticGeometry/SchemeCohomology/RegularUFDSerre.lean:197`: for `R : Type u`
  with Mathlib's `IsRegularLocalRing`, `ringKrullDim R = d` and a finite module `M : Type u`,
  `HasProjectiveDimensionLT (ModuleCat.of R M) (d+1)`. This is Serre's theorem; Mathlib lacks
  it.
- **Steps.** Induct on projective dimension. Take `0 → K → F → M → 0` with `F` free. `K`
  satisfies the Ext hypothesis by the long exact sequence and has smaller projective dimension,
  so `K` is free by induction. Then `Ext¹(M, K) ≅ Ext¹(M, R)ⁿ = 0`, the sequence splits, `M` is
  projective, and projective over a local ring is free. About 100 lines on Mathlib's
  `Abelian.Ext`.
- **Note.** Not a headline (textbook), but the cheapest use of the commutative-algebra layer.
  Serre's theorem would be worth upstreaming to Mathlib from an independent proof.

### 28. Cox: primes of the form `x² + ny²`

- **Statement.** None in formal-conjectures; write one (rule 3 then needs a literature
  citation in `Statement.lean`). Cox, *Primes of the form x² + ny²*, Thm 5.1: for `ℤ[√−n]`
  maximal and `p ∤ 2n`, `p = x² + ny²` iff `p` splits completely in the Hilbert class field
  `H_K` of `K = ℚ(√−n)`; such primes have density `1/(2h)`.
- **Repo.** `primes-x2-ny2`. **Tier** U₀. **Effort** M.
- **Inputs.** `hilbertClassFieldArtinEquiv` and `hilbertClassFieldArtinEquiv_mk0`,
  `le_hilbertClassField_iff`, `isUnramifiedEverywhere_hilbertClassField`
  (`GroundTheory/GlobalFields/ClassFieldConsequences/HilbertClassField.lean`, `:73` for the
  equivalence `ClassGroup (𝓞 K) ≃* Gal(H/K)` sending primes to Frobenius);
  `hasDirichletDensity_setOf_splitsCompletely`; `idealCount_eq_sum` (as in #23).
- **Steps.** `p = x² + ny²` iff `p𝓞_K = 𝔭·𝔭̄` with `𝔭` principal; `𝔭` principal iff its
  Frobenius in `Gal(H/K)` is trivial, by the Artin equivalence; that is `𝔭` splitting
  completely in `H`. Then the density statement.
- **Missing.** `H/ℚ` is Galois (invariance under conjugation); the norm-form identification
  for `ℤ[√−n]`.
- **Out of reach.** General `n` needs ring class fields of orders, which the repo lacks.
- **Small siblings, worth one module each in the same repo.** Every ideal class and ray class
  contains primes of density `1/h` (`hasDirichletDensity_setOf_map_eq`,
  `GroundTheory/GlobalFields/TateThesis/RayClassDensity.lean:310`;
  `exists_degOne_prime_in_rayClass`), effort S. `j((1+√−163)/2) ∈ ℤ` and the other `h = 1`,
  `d ≡ 3 (mod 4)` cases, from `ReciprocityTheory.ChartRestriction.L1.cm1`
  (`ReciprocityTheory/ReductiveGroups/UnramifiedIntegrals/IsIntegralOfRoot.lean:56`) and
  `Elliptic.adjoin_j_eq_hilbertClassField`, effort S–M after #23; the link between the internal
  `CMCurve` and Mathlib's `PeriodPair` is unchecked.

### 29. Kummer's criterion, the easy half, and `small_regular_primes`

- **Statement.** formal-conjectures `Wikipedia/RegularPrimes.lean`:
  `isRegularPrime_iff_Bernoulli` (textbook) and `small_regular_primes` (textbook). Target the
  direction "`p ∤ B_k` for all even `k ≤ p−3` ⇒ `p` regular", then `small_regular_primes` by
  computation. Atlas row `wiki-regular-prime`. State the one-directional theorem and say so
  (rule 3).
- **Repo.** `regular-primes`. **Tier** U₀. **Effort** L.
- **Inputs.** `UpperTheory.V.Stick.coef`,
  `Development/AutomorphicArithmetic/AutomorphicVarieties/GaloisLibrary/StickelbergerTheorem/ImportsAlt.lean:13`
  (opened): Stickelberger on Mathlib's `ClassGroup (𝓞 K)` with
  `IsCyclotomicExtension {M} ℚ K`. `Stick.jacobi`; `Bern.b_lval`, `b_primlevel`
  (`…/BernoulliNumbers/BLprim.lean:11`, `L(1−k,χ) = −B_{k,χ}/k`);
  `hilbertClassFieldArtinEquiv`; GroundTheory `KummerTheory/`.
- **Steps.**
  1. Decompose `Cl[p]` into eigenspaces under `(ℤ/p)ˣ` by the Teichmüller character.
  2. Herbrand: Stickelberger kills the `ω^i` eigenspace by `B_{1,ω^{−i}}`, and
     `B_{1,ω^{−i}} ≡ B_{p−i}/(p−i) (mod p)`.
  3. Kummer's reflection, `p ∣ h⁺ ⇒ p ∣ h⁻`, through Kummer theory and the Hilbert class field.
  4. Bernoulli numbers mod `p` by `decide` for the small primes.
- **Before starting.** Check whether flt-regular already has parts of this.
- **Out of reach.** `p ∣ B_k ⇒ irregular`, `not_isRegularPrime_37` and
  `infinitude_of_irregularprimes` need the analytic `h⁻` formula (#24's factorisation, Mathlib's
  `dedekindZeta_residue`, the unit index). XL.

### 30. Littlewood: the mod-4 prime race changes sign infinitely often

- **Statement.** formal-conjectures `Wikipedia/ChebyshevBias.lean`,
  `littlewood_mod_four_sign_changes` (solved): `π(x;4,3) − π(x;4,1)` changes sign infinitely
  often. This is not the Knapowski–Turán item in the rejected list.
- **Source.** Littlewood 1914; the argument below follows Ingham's style, compare Bateman et
  al., arXiv:1910.08983, Lemma 2.1.
- **Repo.** `chebyshev-bias`. **Tier** U. **Effort** L.
- **Steps.**
  1. Suppose the difference is eventually of one sign.
  2. Landau's lemma for Dirichlet integrals with a one-signed integrand makes
     `F(s) = Σ_p χ₄(p)·p^{−s}` analytic on `Re s > 1/2` and gives `|F(σ+iγ)| ≤ |F(σ)| + O(1)`.
  3. At a zero `1/2 + iγ` of `L(s,χ₄)` of order `m ≥ 1`, `log L` contributes
     `m·log 1/(σ−½)`, while `F(σ)` grows only like `½·log 1/(σ−½)` (the prime-square term,
     from `ζ(2s)`). `m ≥ 1 > 1/2` is the contradiction. GRH for `χ₄` puts the zeros on the line
     and removes Littlewood's case split.
- **Missing.**
  - Landau's lemma in `log L` form. The repo's `Deduction.landau_window` and `poleData_char`
    (`Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/`) need pole data
    with positive residues, which doesn't fit `log L`: treat them as a template and expect a
    rewrite.
  - A non-real zero of `L(s,χ₄)` (existence).
  - `L(1/2, χ₄) ≠ 0`, certified (about `0.6677`; unverified).

### 31. Titchmarsh divisor problem

- **Statement.** `Σ_{p≤x} d(p−1) ~ (ζ(2)ζ(3)/ζ(6))·x`. No formal-conjectures statement was
  found, but that search was cut short by a GitHub rate limit: search again before writing one.
- **Source.** Titchmarsh 1930 under GRH; Linnik 1961 and Halberstam 1967 unconditionally
  *(citations from memory, unverified)*.
- **Repo.** With #17. **Tier** U. **Effort** M. **Depends on** #17.
- **Steps.** Dirichlet hyperbola: `d(p−1) = 2·#{d ∣ p−1, d < √(p−1)} + (square term)`. For
  `d ≤ √x`, `Σ π(x;d,1)` by #17. For large `d`, Brun–Titchmarsh (`brun_titchmarsh_const`, as
  in #18) and the symmetry `d ↔ (p−1)/d`.

### 32. Heilbronn / Siegel: `h(−d) → ∞`

- **Statement.** `h(−d) ≫_ε d^{1/2−ε}`, hence `h(−d) → ∞`. No formal-conjectures statement
  (`ClassNumberProblem.lean` has only Stark–Heegner); Atlas row `wiki-class-number-problem`.
- **Source.** Heilbronn 1934; Siegel 1935.
- **Repo.** With #23. **Tier** U₀. **Effort** M.
- **Inputs.** `Formalism.ZeroFreeDirichlet.siegelLower`,
  `Formalism/LandauZeroFreeBounds/FinalSiegel.lean:21` (Siegel's lower bound for `L(1,χ)`);
  `GlobalTheory.QuadraticZeta.LFunction_one_and_mean_log_eta`,
  `Development/AbelianVarietyTheory/Proofs/HomogeneousIdeals/DedekindZetaEqSumRealEisenstein.lean:121`
  (opened: `L(1,χ) = πh/√d` for `d > 4`, given `IsKroneckerChar χ`), with
  `exists_isIdealClassPoint` (`:80`) discharging its class-point hypothesis;
  `dedekindZeta_eq_mul_LFunction` (`…/ExistsIsKroneckerCharOfDiscr.lean:506`).
- **Missing.** The bridge from the repo-internal `IsKroneckerChar` and `IsIdealClassPoint` to
  Mathlib's `classNumber`. Open both definitions first.
- **Limits.** Ineffective: no finite list comes out. The GRH version with an explicit
  `h ≥ c·√d/log log d` is #13, whose class-number step is now free.

### Existing targets, re-costed

- **#2 von Koch and #5 Cramér.** The `O`-forms are now effort S from H0 at `N = 1`:
  `ψ(x) = x + O(√x·log² x)` and gaps `O(√p·log² p)`. The gap bound is one logarithm weaker than
  Cramér's `√p·log p`, which needs a smoothed formula; state it as a deviation (rule 3).
  Schoenfeld's explicit `√x·log x/(8π)` is unchanged at M–L and still needs erdos-985's
  explicit machinery, so **#7 Mills** is unchanged too.
- **#8 density hypothesis.** Effort S. `N(σ,T) = 0` for `σ > 1/2` under RH; at `σ = 1/2`,
  summing `count_zeros_window` over unit windows gives `N(T) ≪ T·log T` with multiplicity.
  formal-conjectures' `Wikipedia/DensityHypothesis.lean` uses `Complex.zeroCountOn`, which also
  counts multiplicity, so one bridging lemma from `analyticOrderNatAt` remains.
- **#9 Li's criterion.** `Σ 1/|ρ|² < ∞` now follows from the window count. Strict positivity
  still needs infinitely many zeros: Hadamard in erdos-985, or a lower bound for `N(T)`. M.
- **#10 Mertens function.** M, down from M–L. The recorded blocker was a sharp-cutoff Perron
  formula. `GlobalTheory.PerronKernel.truncated_perron_kernel`
  (`Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/TruncatedPerronKernel.lean:351`,
  opened) is that kernel lemma, for `y > 0`, `y ≠ 1`, `c > 0`, `T ≥ 1`, with explicit constant
  3. Still to prove: `1/ζ ≪ |t|^ε` on `σ ≥ 1/2 + δ` under RH (Littlewood; lindelof-rh's
  Borel–Carathéodory work), and the contour shift for `Σ μ(n)n^{−s} = 1/ζ(s)`, for which
  `GlobalTheory.ResRect.residue_rectangle` exists. `logDeriv_LFunction_strip` and
  `ZetaWide.main` are related inputs. **#16** follows #10.
- **#13 explicit `L(1,χ)` and class numbers.** The class-number step is free (see #32's
  inputs). The Littlewood bound for `L(1,χ)` with explicit constants is unchanged.
- **#3, #11, #12.** Unchanged: they end in explicit constants, and the repo's are existential.
  The few explicit ones are Brun–Titchmarsh `48`, the Perron kernel `3`, Mertens' first theorem
  `log 4 + 4`, and `π(y) < 1.26·y/log y`.
- **#6 ternary Goldbach.** Unchanged. Only the major arcs get cheaper (Siegel–Walfisz, or
  GRH). The minor arcs need Vaughan's identity and exponential sums over primes; the repo has
  neither.
- **artin-grh.** Done in artin-grh PR #11 (merged): the repo's `continuedDedekindZeta`,
  `completedDedekindZeta_one_sub`, `gammaFactor_one` and `discrNormConductor_one` supply every
  field of `DedekindContinuation` except the strip bound, which the PR proves in the main
  library. `HooleyHypothesis` stays, so the result is tier C with no H hypothesis.

### Lower priority, recorded so they aren't rediscovered

- **Weak unconditional Bombieri–Vinogradov** (some small level `θ₀ > 0`, Rényi 1948). From
  `GlobalTheory.ZeroDensityMult.zero_density_mult` / `ZeroDensityBox` (at most `C·Q^{1/4}`
  characters with a zero in `Re > 1 − 1/400`, `|Im| ≤ Q`), `truncated_explicit_formula` and
  `siegelWalfisz`. One agent's sketch, unverified: a trivial bound on the bad characters, zeros
  with `β ≤ 1 − 1/400` for the rest, `θ₀ ≈ 1/800`. U₀, M–L. Worth doing only if
  Bombieri–Vinogradov should survive a failure of the RH proof.
- **Erdős 971, variant `many_small`** (Erdős 1949; formal-conjectures `ErdosProblems/971.lean`).
  Needs an upper-bound sieve for prime pairs `p`, `p + kd`. The repo's arithmetic large sieve
  (`GlobalTheory.T.arithmeticLargeSieve_one_residue_class_per_prime`) allows one class per
  prime; Mathlib's `SelbergSieve` might fill the gap. U₀, M–L.
- **Cited re-exports.** Kronecker–Weber (`UpperTheory.V.CF.kw`), the Artin map
  (`GroundTheory.Global.artinMap`), Chebotarev density (`hasDirichletDensity_chebotarevSet`,
  `GroundTheory/GlobalFields/TateThesis/Chebotarev.lean:205`), Ferrero–Washington
  (`UpperTheory.V.FW.ferreroWashington`), the Hasse norm theorem
  (`mem_range_norm_iff_forall_local`, `GroundTheory/GlobalFields/HasseNorm.lean:60`), and the
  class-number upper bounds (`KStar.IdealCounting.log_classNumber_le`). Each is a wrapper of
  effort S with no formal-conjectures statement. Collect them in one `rh-imports` module if a
  target needs them.
- **Small Cohen–Macaulay modules in dimension ≤ 2** (formal-conjectures
  `Wikipedia/SmallCohenMacaulayModules.lean`). Needs Nagata's finiteness of normalisation and
  Serre's S₂ criterion; the repo's Cohen–Macaulay lemmas are a minor input. U₀, L.

### Rejected in round 3

- **Catalan / Mihăilescu.** Already proved in Lean 4 (cadamcat/catalan-lean4).
- **Anything Weil-bound shaped.** `WeilBound` contains no Weil bound, and `EtaleCohomology`
  states Poincaré duality and the Frobenius weights without proving them.
- **Unconditional Bombieri–Vinogradov at level 1/2, Vinogradov's three primes, Chowla.** The
  repo has the large sieve and Siegel–Walfisz, but no Vaughan identity, bilinear estimates or
  circle method.
- **Erdős 695, Erdős 980 for general `k`, Erdős–Halberstam proper.** Reasons in the analytic
  report.
- **Briançon–Skoda, Serre's dimension inequality, Fujita-type bounds.** Each is XL.
  Briançon–Skoda has the right Skoda division theorem in the repo
  (`ReciprocityTheory.L2DbarEstimates.skoda`) but no formal statement, no ring of convergent
  germs in Mathlib, and separate arguments for `m = 1` and `m > n`. Serre's inequality needs
  Cohen's structure theorem for the reduction to the diagonal. Fujita-type bounds need the
  multiplier-ideal concentration argument, on internal definitions.
- **Elliott–Halberstam proper (`θ ≥ 1/2`) and Chowla's least-prime conjecture.** Open even
  under GRH. The repo's Linnik exponent is existential, so Xylouris's `L = 5` is out of reach.
- **"No Siegel zeros".** A one-line corollary of GRH with no formal-conjectures statement
  found. Note it in a README; it isn't a target.
- **Bach's class-group generator bound, Miller's real-cyclotomic class numbers, Weinberger's
  Euclidean rings, Harper–Murty.** All need ERH for non-abelian fields or a number-field
  Bombieri–Vinogradov. See #24.
- **Full Kummer criterion, `not_isRegularPrime_37`, infinitely many irregular primes.** Need
  the analytic `h⁻` formula. XL; revisit after #24 and #29.
- **Brauer–Hasse–Noether in full, Grunwald–Wang.** The repo has injectivity and the zero sum of
  invariants only, on a cohomological Brauer group not linked to central simple algebras.
- **Kummer–Vandiver, Leopoldt, Greenberg, Iwasawa main conjecture, Brumer–Stark, Stark,
  Hilbert's twelfth problem.** Open, and nothing in the repo touches them.
- **Brouwer, invariance of domain, Hörmander, Markov, Lie–Trotter, Minkowski II,
  Harder–Narasimhan.** Proved in the repo, but no Atlas or formal-conjectures row turns on them.

## Most famous targets

Ranked by how widely the result is known, across all three rounds. "Open" means the
unconditional statement is open mathematics, so a tier-U proof says something new formally.

| Rank | Target | Why it is known | Open unconditionally? | Tier | Effort |
|---|---|---|---|---|---|
| 1 | #25 Hironaka's resolution of singularities (char 0) | Fields Medal theorem, 1964 | No | D or U₀ | S |
| 2 | #24 ERH for abelian number fields | The extended Riemann hypothesis for a whole class of fields | Yes | U | M–L |
| 3 | #23 Stark–Heegner, class number one | Gauss's class number problem, 1801 | No | U | M–L |
| 4 | #1 Euler's idoneal numbers | Euler's list of 65, 1778 | **Yes** | U | M |
| 5 | #17 Bombieri–Vinogradov | "GRH on average"; behind bounded gaps between primes | No | U | M |
| 6 | #10 Mertens function `M(x) = O(x^{1/2+ε})` | The best-known equivalent form of RH | Yes | U | M |
| 7 | #20 Linnik's theorem | Least prime in an arithmetic progression | No | U₀ | S |
| 8 | #2 / #5 von Koch and Cramér's prime-gap theorem | The classical consequences of RH for primes | Yes | U | S for the `O`-forms |
| 9 | #30 Littlewood's prime-race sign changes | Chebyshev's bias | No | U | L |
| 10 | #28 Cox, primes of the form `x² + ny²` | Fermat's two-squares question in general | No | U₀ | M |
| 11 | #29 Kummer's criterion for regular primes | Kummer's route to Fermat's Last Theorem | No | U₀ | L |
| 12 | #7 Mills' constant | A prime-generating constant; Wikipedia-level | Yes | U | S after #2 |

Best fame for the effort: **#25** (S), **#20** (S), **#1** (M, and the only open
formal-conjectures statement in the top five), **#17** (M). The Erdős problems (#18, #19, #21,
#22) are less famous individually but carry formal-conjectures statements and existing proofs.

## Recommended order

Revised in round 3:

1. **#20 Erdős 456 (Linnik)** as the smoke test for importing one module and running
   `#print axioms` on it, and for the U₀ layout.
2. **The GRH `ψ(x,χ)` bound** as a shared library, then **#17 Bombieri–Vinogradov**, the
   `O`-forms of **#2 / #5**, **#8 density hypothesis**, **#21** and **#22**.
3. **#1 idoneal numbers by the split-prime route**, then **#23 Stark–Heegner**, which shares the
   least-split-prime bound. #1 is the only open formal-conjectures statement here that looks
   reachable at tier U.
4. **#19 and #18**, ports of existing proofs with their axioms discharged.
5. **#2 with Schoenfeld's constant**, then **#7 Mills**; **#4 Dirichlet-L Lindelöf**;
   **#3 / #12** least primes via LLS; **#9 Li's criterion**.
6. **Later:** #10 Mertens, then #16; #24 ERH for abelian fields; #28; #32; #11; #13; #15; #14;
   #29; #30; #31.
7. **Independent of the above, any time:** **#25 Hironaka**, **#26 local uniformisation** and
   **#27 Auslander–Reiten**. They share nothing with the analytic targets.

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
