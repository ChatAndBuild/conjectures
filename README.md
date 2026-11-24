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

```bash
git clone --recurse-submodules https://github.com/senamakel/conjectures
```
