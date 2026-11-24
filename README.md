# Conjectures

The tracking superproject for the Lean 4 formalisations of conjectures conditional on RH/GRH.
Each project is a submodule pinned to the commit last reviewed. [`AGENTS.md`](AGENTS.md) holds
the status checklist, the proof-tier rules (when a result counts as a direct proof) and the README rules.

| Submodule | Result | Tier |
|---|---|---|
| [erdos-985](https://github.com/senamakel/erdos-985) | every odd prime has a prime primitive root `q < p` | U |
| [ankeny-grh](https://github.com/senamakel/ankeny-grh) | Bach's Ankeny bound, constant `21/5` | U |
| [miller-grh](https://github.com/senamakel/miller-grh) | deterministic Miller–Rabin, `4.2 log² n` bases | U |
| [lindelof-rh](https://github.com/senamakel/lindelof-rh) | Lindelöf hypothesis for ζ and for Dirichlet L-functions | U |
| [li-criterion-rh](https://github.com/senamakel/li-criterion-rh) | Li's criterion, positivity direction: `λ_n > 0` for `n ≥ 1` | U |
| [bach-sorenson-grh](https://github.com/senamakel/bach-sorenson-grh) | least prime `p ≡ a (mod q)` is `< (7/2)(q log q)²` | U |
| [grosswald-grh](https://github.com/senamakel/grosswald-grh) | Grosswald's conjecture | U for `p > 2.5·10^15`, H below |
| [robin-rh](https://github.com/senamakel/robin-rh) | Robin's inequality | U + H (Morrill–Platt range) |
| [artin-grh](https://github.com/senamakel/artin-grh) | Hooley's conditional Artin theorem, Hecke's continuation discharged | C (GRH for the Kummer fields) |
| [mills-rh](https://github.com/senamakel/mills-rh) | Mills' constant: lower bound `1.3063778838 < A` | D; upper bound C + H, in progress |

The rows marked U were rebuilt and checked against riemann-hypothesis `507a75d91d` on
2026-11-24. That links the proofs to a community build cache; it does not re-verify the RH/GRH
proof itself.

In progress (scaffolded, nothing verified yet):
[weinberger-grh](https://github.com/senamakel/weinberger-grh),
[schoenfeld-rh](https://github.com/senamakel/schoenfeld-rh),
[cramer-rh](https://github.com/senamakel/cramer-rh),
[goldbach-grh](https://github.com/senamakel/goldbach-grh),
[density-rh](https://github.com/senamakel/density-rh),
[mertens-rh](https://github.com/senamakel/mertens-rh),
[nicolas-rh](https://github.com/senamakel/nicolas-rh),
[lls-grh](https://github.com/senamakel/lls-grh),
[erdos-233](https://github.com/senamakel/erdos-233),
[littlewood-rh](https://github.com/senamakel/littlewood-rh).

Tiers: **D** direct, **U** unconditional through
[riemann-hypothesis](https://github.com/leanprover-community/riemann-hypothesis), **C** conditional
on RH/GRH, **H** cited result taken as a hypothesis. See `AGENTS.md`.

## Next targets

Candidates whose analytic input is only RH for ζ or GRH for Dirichlet L, so they can reach
tier U. Details, the expected tier of each, and rejected candidates are in
[`docs/NEXT_TARGETS.md`](docs/NEXT_TARGETS.md).

| # | Target | Input | Expected tier |
|---|---|---|---|
| 1 | Euler's idoneal numbers and class number one (Weinberger 1973) | GRH | U |
| 2 | von Koch / Schoenfeld bound for `π(x) − li(x)` | RH | U, if the small range fits |
| 3 | Least prime in an arithmetic progression (Bach–Sorenson 1996) | GRH | **done**, U with constant `7/2` (bach-sorenson-grh) |
| 4 | Lindelöf for Dirichlet L-functions | GRH | **done**, U (lindelof-rh) |
| 5 | Cramér's prime-gap theorem (1920) | RH | U |
| 6 | Ternary Goldbach (Deshouillers–Effinger–te Riele–Zinoviev 1997) | GRH | U or H, depending on the computation |
| 7 | Mills' constant `A ∈ (1.3063778838, 1.3063778839)` (Caldwell–Cheng 2005) | RH | U |
| 8 | Density hypothesis (open in formal-conjectures) | RH | U |
| 9 | Li's criterion, RH ⇒ `λ_n > 0` (open in formal-conjectures) | RH | **done**, U (li-criterion-rh) |
| 10 | Mertens `M(x) = O(x^{1/2+ε})`, Redheffer, Franel–Landau | RH | U |
| 11 | Nicolas' criterion (the φ version of Robin) | RH | U, if the small range fits |
| 12 | Lamzouri–Li–Soundararajan least primes, upgrading ankeny-grh / miller-grh | GRH | U |
| 13 | Explicit `L(1,χ)` and class-number bounds (LLS) | GRH | U |
| 14 | Erdős 233, sum of squared prime gaps | RH | U |
| 15 | Littlewood's `log ζ(1/2+it) ≪ log t / log log t` | RH | U |
| 16 | Riesz and Hardy–Littlewood criteria | RH | U |

Revised order: #2 first, with #7 Mills on top of it, and #5 Cramér following almost directly.
In parallel, zero counting leads to #8 and then #9. See [`docs/NEXT_TARGETS.md`](docs/NEXT_TARGETS.md).

Out of reach even with riemann-hypothesis: unconditional Artin (needs RH for non-abelian
Kummer-field zeta functions), and Gilbreath, binary Goldbach, twin primes, Legendre and
Cramér's conjecture, which RH does not imply.

```bash
git clone --recurse-submodules https://github.com/senamakel/conjectures
```
