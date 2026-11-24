# Conjectures

The tracking superproject for the Lean 4 formalisations of conjectures conditional on RH/GRH.
Each project is a submodule pinned to the commit last reviewed. [`AGENTS.md`](AGENTS.md) holds
the status checklist, the proof-tier rules (when a result counts as a direct proof) and the README rules.

| Submodule | Result | Tier |
|---|---|---|
| [erdos-985](https://github.com/senamakel/erdos-985) | every odd prime has a prime primitive root `q < p` | U |
| [ankeny-grh](https://github.com/senamakel/ankeny-grh) | Bach's Ankeny bound, constant `21/5` | U |
| [miller-grh](https://github.com/senamakel/miller-grh) | deterministic Miller–Rabin, `4.2 log² n` bases | U |
| [grosswald-grh](https://github.com/senamakel/grosswald-grh) | Grosswald's conjecture | U for `p > 2.5·10^15`, H below |
| [robin-rh](https://github.com/senamakel/robin-rh) | Robin's inequality | U + H (Morrill–Platt range) |
| [lindelof-rh](https://github.com/senamakel/lindelof-rh) | Lindelöf hypothesis for ζ | U |
| [artin-grh](https://github.com/senamakel/artin-grh) | Hooley's conditional Artin theorem | C + H (Hecke continuation) |

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
| 3 | Least prime in an arithmetic progression (Bach–Sorenson 1996) | GRH | U |
| 4 | Lindelöf for Dirichlet L-functions (stubbed in lindelof-rh) | GRH | U |
| 5 | Cramér's prime-gap theorem (1920) | RH | U |
| 6 | Ternary Goldbach (Deshouillers–Effinger–te Riele–Zinoviev 1997) | GRH | U or H, depending on the computation |

Out of reach even with riemann-hypothesis: unconditional Artin (needs RH for non-abelian
Kummer-field zeta functions), and Gilbreath, binary Goldbach, twin primes, Legendre and
Cramér's conjecture, which RH does not imply.

```bash
git clone --recurse-submodules https://github.com/senamakel/conjectures
```
