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

## Recommended order

1. **Now, in parallel:** #4 (statement exists) and #3 (closest to existing code). Both are short
   and reuse erdos-985 and ankeny-grh almost directly.
2. **Scoping spike:** #1, to settle whether the class-group statements can be written against the
   Mathlib pin. This decides whether the most valuable target is weeks of work or a Mathlib
   project.
3. **Then:** #2, followed by #5.

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

## See also

- Reasoning behind these choices is recorded in LivingBrain (see `AGENTS.md`, "Memory").
- The Conjecture Atlas note with the same ranking:
  [senamakel/tiny-cortexdb-mathagent#1](https://github.com/senamakel/tiny-cortexdb-mathagent/pull/1).
