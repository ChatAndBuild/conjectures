# Conjectures workspace

This superproject (`github.com/senamakel/conjectures`) tracks the Lean 4 projects that formalise
number-theory conjectures and theorems, most of them conditional on RH or GRH. Each project is a
submodule (`github.com/senamakel/<name>`) pinned to the commit last reviewed. This file is the
tracker: when a box changes, update it here and bump the gitlink in the same commit.

Status as of 2026-11-24. Every box marked **verified** below was rebuilt from source on the
build box that day, its `#print axioms` output read, and (for tier U) its
`scripts/check-unconditional.sh` run against riemann-hypothesis `507a75d91d`. Boxes for repos
whose work is still on an open branch are marked **in progress** and are not yet verified.

## Memory: LivingBrain

Memory for this work lives in [LivingBrain](https://livingbrain.com), the same memory layer the
OpenHuman agents used to build erdos-985. Claude Code reaches it through the `livingbrain` MCP
server (`https://livingbrain.fernmcp.dev/livingbrain`, configured in `~/.claude.json`).

- At the start of a session, recall what LivingBrain holds about the conjecture you're working
  on before you re-derive it: approaches tried, dead ends, constants, why a hypothesis exists.
- Write to LivingBrain whatever the repos can't hold: an approach that failed and why, a
  threshold or constant you sized up, a decision and its reason. Don't store anything git
  already records.
- This file stays the source of truth for **status**. LivingBrain holds the reasoning behind
  it. When a checklist box changes here, record the why in LivingBrain.
- If the `livingbrain` tools aren't loaded in a session, say so and don't fall back silently to
  local memory files.
- Brain: `projec1006` (`63af7dac-de64-581f-9949-9e1bed98d7fd`). Earlier captures used the source
  label "RH formalization repos"; keep using it.

### Ingestion

`scripts/lb_ingest.py` keeps the brain in step with the repos. For each submodule's remote
default branch, and for this superproject's `AGENTS.md`, `README.md` and everything under
`docs/` (read from the working tree; a file over 45,000 characters is sent in parts, because
LivingBrain rejects content over 50,000), it captures:
- documentation (`README.md`, `AGENTS.md`, `docs/*.md`, `paper/README.md`) whenever its content changes;
- new commit messages: the history of attempts, one note per repo per run;
- every PR, in any state, re-captured when it's updated. A PR closed without merging is
  labelled an abandoned attempt;
- branches with unmerged commits: attempts in flight or abandoned.

Captures are idempotent: `originRef` carries the commit, content hash or update time, and
`~/.local/state/conjectures-lb-ingest.json` records what was already sent. `--dry-run` shows the
captures without sending anything. Credentials come from `~/.claude.json` and are never printed.
Cron runs it hourly from the primary checkout and logs to `~/.cache/conjectures-lb-ingest.log`:

```
17 * * * * cd $HOME/work/personal/conjectures && flock -n $HOME/.cache/conjectures-lb-ingest.lock python3 -I scripts/lb_ingest.py >> $HOME/.cache/conjectures-lb-ingest.log 2>&1
```

The script records only what git and GitHub know. Reasoning that never reaches a commit (an
approach dropped mid-session, a constant sized up in a scratch script) has to be written to
LivingBrain by hand, as above.

## Shared facts

- Toolchain: Lean `v4.36.0`, Mathlib `fc4f59e5`. `erdos-985` is the root: it holds the analytic
  toolkit (weighted explicit formula, Hadamard factorisation, zero sums under GRH) and the GRH
  statement. Every other repo requires it as a lake dependency. `miller-grh` also requires `ankeny-grh`.
- RH/GRH come from [leanprover-community/riemann-hypothesis](https://github.com/leanprover-community/riemann-hypothesis),
  checked against commit `507a75d91d`. It proves `riemannHypothesis : RiemannHypothesis` and
  `LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf`. The import needs about
  93 GB of cache, about 19 GB of RAM and roughly 900k open files. That build comes from an
  untrusted community cache and **has not been independently re-verified**
  (`RH_FULL_BUILD=1` rebuilds it from source).
- Dependency graph:

  ```
  riemann-hypothesis ──(only in Unconditional/)──┐
  erdos-985 ──┬── ankeny-grh ── miller-grh        │
              ├── grosswald-grh                    ├─ each Unconditional/*.lean
              ├── robin-rh                         │
              ├── lindelof-rh                      │
              └── artin-grh (no Unconditional/) ───┘
  ```

## Proof tiers: when a result counts as a direct proof

Each headline theorem has exactly one tier, and the README must say which.

| Tier | Name | Meaning | Allowed axioms |
|---|---|---|---|
| **D** | Direct | A closed statement with no hypotheses, proved inside the repo without importing riemann-hypothesis | standard three + documented `native_decide` |
| **U** | Unconditional via RH | `Unconditional/<X>Unconditional.lean` imports riemann-hypothesis and closes the RH/GRH hypothesis in one line | same as D; the README carries the trust caveat |
| **C** | Conditional | RH/GRH (or another open conjecture) is an explicit argument of the main-library theorem | same as D |
| **U₀** | Unconditional via an RH-repo lemma | `Unconditional/` imports riemann-hypothesis for a lemma that does not depend on RH (Siegel–Walfisz, Linnik, class field theory, resolution of singularities, …) and discharges it in one line. No RH or GRH hypothesis is involved | same as D; the README carries the trust caveat |
| **H** | Cited hypothesis | A known result we don't re-prove (a large computation, a theorem missing from Mathlib) appears as an explicit `Prop` argument | same as D |

Rules:

1. **The main library never imports riemann-hypothesis.** RH/GRH enters as an explicit
   hypothesis (`(hRH : RiemannHypothesis)` / `(hGRH : DirichletLNonvanishingRightOfHalf)`).
   Only `Unconditional/` imports the RH repo, and its theorems discharge the hypothesis in one
   line. If riemann-hypothesis ever turns out wrong, the main library is still correct as a
   conditional result.
2. **Hypothesis definitions are copied word for word** from their source
   (riemann-hypothesis `src/Statements.lean`, Mathlib's `RiemannHypothesis`, or
   formal-conjectures). Both projects use the same Lean and Mathlib pin, so the definitions are the
   same term and the one-line discharge typechecks. Never restate a hypothesis in your own words.
3. **Target statements are fixed.** `<Pkg>/Statement.lean` holds the target definitions. When a
   formal-conjectures statement exists, copy it verbatim and link to it. Don't edit these files to
   make a proof go through. If the proved constant differs from the literature (e.g. `21/5`
   instead of Bach's `2`), state the weaker theorem and say why in the README.
4. **No `sorry` on the path to a headline theorem.** Prefer a tier-H hypothesis to a cited
   `sorry`: put the input in a `Prop` (`RobinVerifiedRange`, `VerifiedUpTo`,
   `DedekindContinuation`) and prove `X_of_..._of_verified`. A theorem whose
   `#print axioms` shows `sorryAx` is not a result. It may exist only as a clearly labelled
   convenience wrapper, never as the headline.
5. **`#print axioms` is the source of truth.** Every headline theorem's axiom list goes in the
   README, pasted from real output. Allowed: `propext`, `Classical.choice`, `Quot.sound`, and
   `*._native.native_decide.ax_*`. Each `native_decide` needs a soundness proof for its checker
   and its count in the README. No `axiom` or `opaque` declarations for mathematical content.
6. **"Done" means tier D, U or U₀ for the full target statement**, with every remaining H
   hypothesis named. A repo whose best result is C or H is not done. It is done as far as it can
   go only when its README explains why no unconditional version is possible (artin-grh).
7. **Pins must resolve.** Every `[[require]]` rev must exist on the remote's default branch, and
   its URL must be an HTTPS URL that an anonymous `lake` can fetch.

## Literature status: label every result

With one possible exception, nothing in this workspace is new mathematics: every result is
already a theorem in the literature, and what is new is the Lean proof. The exception is
erdos-985, whose implication "GRH implies Erdős 985" has no earlier publication we know of
(see `docs/LITERATURE_STATUS.md`); whether it gets the **new** label is the user's call. So each result carries a second label next to its
tier, saying how it stands in the literature. The label goes in the README table, in the
checklist heading below, and in the opening paragraph of the repo's README (README rule 13).
Attributions are in [`docs/LITERATURE_STATUS.md`](docs/LITERATURE_STATUS.md).

| Label | Meaning | How to describe it |
|---|---|---|
| **known** | Proved in the literature with no hypothesis, and not in Lean before. Our proof uses no RH | "a Lean formalisation of X (author, year)" |
| **known, via GRH here** | Proved in the literature with no hypothesis, but our proof assumes RH or GRH. Ours is the weaker result | "X under GRH, in Lean; X itself is a theorem of (author, year)" |
| **RH-consequence** | A published theorem of the form "RH/GRH implies X", with X open otherwise | main library: "GRH implies X, following (author, year)"; `Unconditional/`: "X, given the unverified Lean proof of RH/GRH in riemann-hypothesis" |
| **RH-equivalent** | X is known to be equivalent to RH, so an unconditional X says nothing beyond the RH claim | as RH-consequence, and say it is equivalent |
| **new** | An open problem settled, or a new conditional theorem proved, by an argument of ours. **No result has this label yet**; erdos-985 is the one candidate | needs the user's sign-off before any README uses it |

Rules:

- A result is never called "solved", "settled" or "now proved" on the strength of
  riemann-hypothesis. Its proof of RH has not been independently verified. If it fails, every
  tier-U theorem falls back to tier C.
- "Not in Lean before" is a claim too. Before writing it, search Mathlib, formal-conjectures'
  `formal_proof` attributes and GitHub for an existing formalisation, and say what was searched.
- When picking a target, record its label in `docs/NEXT_TARGETS.md` first. A **known** target is
  a formalisation project; choose it for that reason, not because it sounds like a conjecture.

## README rules

Each README follows the shape already used across these repos:

1. **Title**: `# <Result> under <RH|GRH> in Lean` (or `from RH`). No marketing.
2. **Opening paragraph**: the classical statement with its source (author, year, journal or arXiv),
   and what is known unconditionally.
3. **Headline Lean block**: the exact Lean signatures of the main theorems, hypotheses included,
   copied from the source.
4. **Tier and provenance**: say which tier each headline theorem is in. Name every hypothesis and
   where its definition was copied from. If formal-conjectures has the statement, link to it.
5. **Axioms**: real `#print axioms` output in a code block, and one sentence on each non-standard
   axiom (what the `native_decide` computes and how long it takes).
6. **Proof outline**: numbered steps that point at files, with the key inequality or constant at
   each step. Put the full blueprint in `docs/PLAN.md` or `docs/BLUEPRINT.md` and link to it.
7. **Layout table** (`| File | Content |`) when there are more than about 6 modules.
8. **Deviations from the literature**: a section on any weaker constant, larger threshold or
   extra hypothesis, with the reason (see ankeny-grh's "Why `21/5`").
9. **Building**: the exact `lake build` target, toolchain and Mathlib pin, and the CPU or wall
   time of the expensive modules.
10. **Unconditional version**: a table `| Theorem | Statement | Axioms |`, the riemann-hypothesis
    commit, the `scripts/check-unconditional.sh` command, the resource needs (93 GB, 19 GB RAM,
    open-file limit), and this caveat word for word: *"The riemann-hypothesis proof adds no axioms of its
    own. The cache contains outputs of untrusted builds, so this links the proofs but does not
    re-verify the RH/GRH proof, whose independent verification is still pending."* If there is
    no unconditional version, a "This result stays conditional" section saying why.
11. **Credits** for every vendored file: source repo, commit, licence, NOTICE.
12. **Claims stay calibrated.** Never write "proves the conjecture" for a tier-C or tier-H
    result. Write "proves X under GRH" or "proves X, given the computation Y". A section
    heading must not claim more than its table shows (e.g. "standard axioms only" above
    theorems that use `native_decide`).
13. **Say what is already known.** The opening paragraph states the result's status in the
    literature, using the wording in [`docs/LITERATURE_STATUS.md`](docs/LITERATURE_STATUS.md):
    proved unconditionally (group A), a published consequence of RH/GRH (group B), or
    equivalent to RH (group C). Nothing here is new mathematics. A README never says a result
    is "solved" or "now proved" on the strength of riemann-hypothesis, and when a theorem known
    unconditionally is proved here through GRH, the README says our proof is the weaker one.

## Cross-repo issues

- [x] **Dependency pins resolve.** Every merged sibling requires erdos-985 at `9538edb` (an
      ancestor of its `main`, now `83cad09`) over HTTPS; miller-grh and bach-sorenson-grh require
      ankeny-grh at `129ad57` (an ancestor of its `main`, now `61dee5c`). robin-rh and
      grosswald-grh carry the same fix on their open `finality` PRs (#3 each).
- [x] **SSH require URLs** switched to `https://` in every merged repo (rule 7). The repos are
      private, so an anonymous `lake` still cannot fetch them; that is a visibility decision.
- [x] **Unconditional checks run on this box**, 2026-11-24, riemann-hypothesis `507a75d91d`
      (98 GB cache at `~/work/personal/riemann-hypothesis`, linked from the community cache, not
      rebuilt from source): erdos-985 `57436d3`, ankeny-grh `dcc7a79`, miller-grh `81154df`,
      lindelof-rh `3975bbb` (one rename-only commit before the merged head), artin-grh `53073d1`,
      li-criterion-rh `f058257`, bach-sorenson-grh `2242e96`, density-rh `637fd12`, nicolas-rh `4229e63`. No `sorryAx` in any log.
      The shell's hard open-file limit (524288) is too low for the import: run
      `sudo prlimit --pid $$ --nofile=2000000:2000000` first. Up to four checks fit in RAM at once.
- [ ] No repo has a `LICENSE` file, and riemann-hypothesis has no licence either. Decide on a
      licence, and check that copying its statement definitions word for word is acceptable.
- [ ] No CI anywhere. Add a GitHub Action that runs `lake build` and checks
      `#print axioms` against an allow-list (the cheap build, not the unconditional one).
- [ ] `RH_FULL_BUILD=1` (rebuilding riemann-hypothesis from source) has never been run.

## Per-repo checklist

### erdos-985: every odd prime has a prime primitive root `q < p` · **tier U, complete, verified** · *RH-consequence, first proved here (unreviewed); candidate for new, pending the user*
- [x] Statement matches formal-conjectures `erdos_985` verbatim
- [x] `erdos_985_of_GRH` (C), no `sorry`
- [x] `Unconditional/`: `erdos_985` (U), standard three + 20 `native_decide`. The `sorryAx` seen
      on 2026-11-22 came from a stale checkout and is not present on `main`
- [x] Finite check `p < 10^8` with a proved-sound checker
- [x] Paper (`paper/erdos985.pdf`)
- [x] README: Credits section and tier line
- [ ] Clean up the old checkout `~/work/personal/erdos-985` (branch `audit-proof-63d6818`, untracked `worktrees/`)

### ankeny-grh: Bach's explicit Ankeny bound · **tier U with constant 21/5, complete for 21/5, verified** · *RH-consequence*
- [x] `bach_of_GRH : BachSubgroupBound (21/5)`, `leastNonresidue_of_GRH`, no `sorry`
- [x] `Unconditional/`: `bach_unconditional`, `leastNonresidue_unconditional` (U), + 8 `native_decide`
- [x] README explains the deviation from Bach's `2`
- [ ] Optional: get to `c ≈ 4.05` by extending the computation to `2^18` (about 80 CPU-minutes, 4× today's)
- [ ] Open: Bach's constant `2`. The erdos-985 zero-sum bound caps this method at `c > 16/9`
      asymptotically and at `q ≳ 10^28` for `c = 2`; it needs a sharper explicit formula
      (lls-grh is attempting one)

### miller-grh: deterministic Miller–Rabin under GRH · **tier U with constant 21/5, complete, verified** · *RH-consequence*
- [x] `miller_of_bach` and `prime_iff_of_bach` (reduction, standard axioms only)
- [x] `miller_of_GRH : MillerStatement (21/5)` and the executable `millerTestGRH_iff_prime`
- [x] `Unconditional/`: `miller_unconditional`, `millerTestGRH_iff_prime_unconditional` (U), + ankeny's 8 `native_decide`
- [x] `millerTest_iff_prime` (assumes `BachSubgroupBound 2`) is labelled "conditional on Bach's
      constant 2 (not a headline result)" in the README
- [x] README headings no longer claim "standard axioms only" for the GRH theorems
- [x] ankeny pin at `129ad57`

### grosswald-grh: `g(p) < √p − 2` for `p > 409` · **tier U for `p > 2.5·10^15`, tier H for the full statement; in progress** · *RH-consequence*
- [x] `prime_primitive_root_of_GRH_large` (C), no `sorry`, + 10 `native_decide`
- [x] `Unconditional/`: `prime_primitive_root_large_unconditional` (U)
- [x] `grosswald_of_GRH` / `grosswald_of_verified` with `VerifiedUpTo 2500000000000000` as a hypothesis
- [ ] The full `GrosswaldStatement` is still tier H: the Cohen–Oliveira e Silva–Trudgian range
      `409 < p ≤ 2.5·10^15` (about 7·10^13 primes) is too large to replay as it stands. An agent
      is lowering the analytic threshold and sizing a proved-sound checker (PR #3, open)
- [ ] `scripts/__pycache__` removal and `.gitignore` are on PR #3

### robin-rh: Robin's inequality `σ(n) < e^γ n log log n`, `n > 5040` · **tier U + H; in progress** · *RH-equivalent*
- [x] `robin_of_RH_of_verified` (C + H), no `sorry`; `RobinVerifiedRange` is the Morrill–Platt range
- [x] `Unconditional/`: `robin_of_verified` (U + H), standard three only
- [x] `lagarias_of_RH`, Lagarias's form, with 1 `native_decide` for `13 ≤ n ≤ 5040`
- [ ] Rule 4 violation on `main`: `robin_small_range` in `Robin/Small.lean` is a cited `sorry`.
      PR #3 (open) removes it and makes the range a hypothesis everywhere
- [ ] Open: eliminate `RobinVerifiedRange` (lower the analytic threshold `x ≥ e^30` and check the
      remaining colossally abundant numbers with a sound checker). An agent is sizing this

### lindelof-rh: Lindelöf from RH/GRH, for ζ and Dirichlet L · **tier U, complete, verified** · *RH-consequence*
- [x] `lindelof_of_RH` (C) and `Unconditional/` `lindelof_hypothesis` (U), standard three only
- [x] `dirichletLindelof_of_GRH` (C) proved, target statement unchanged; `Unconditional/`
      `dirichletLindelof` (U), standard three only
- [x] README has the standard sections

### artin-grh: Hooley's theorem (Artin under GRH for Kummer fields) · **tier C, at its ceiling, verified** · *RH-consequence*
- [x] Sieve half and analytic core, no `sorry`; the repo contains no `sorry` at all
- [x] `conditional_artin_primitive_roots.parts.i_of_continuation` (C + H) in the main library
- [x] Hecke's continuation discharged: `Artin.Unconditional.dedekindContinuation` imports the
      Tate-thesis module of riemann-hypothesis (the strip bound is proved here from Mathlib
      alone), giving the formal-conjectures statement
      `Artin.Unconditional.conditional_artin_primitive_roots_parts_i` with `HooleyHypothesis`
      as its only hypothesis, standard three only
- [x] `scripts/check-unconditional.sh`, repo description, real build section
- [ ] Cannot become tier U (verified at `507a75d91d`): every zero-location theorem in
      riemann-hypothesis is for ζ or Dirichlet L; it has Hecke L-functions but nothing on their
      zeros in the critical strip, and the Kummer fields are non-abelian for odd prime `k`
- [ ] Optional: Hecke's continuation inside the main library without riemann-hypothesis
      (Poisson summation on `ℝ^{r₁} × ℂ^{r₂}`, theta inversion per ideal class; multi-week)

### li-criterion-rh: Li's criterion, RH ⇒ `λ_n > 0` · **tier U, complete, verified** · *RH-equivalent*
- [x] `nontrivialPosZeros`, `lambda` copied verbatim from formal-conjectures (`86a2f58a`)
- [x] `li_criterion_rhs_of_RH` (C) and `Unconditional/` `li_criterion_rhs` (U), standard three
      only. This is the entry formal-conjectures lists as open
- [ ] Out of scope so far: the converse (positivity ⇒ RH, Bombieri–Lagarias)

### bach-sorenson-grh: least prime `p ≡ a (mod q)` · **tier U with constant 7/2, complete for 7/2, verified** · *RH-consequence*
- [x] `bachSorenson_of_GRH : BachSorensonBound (7/2)` (C), `p < (7/2)(q log q)²` for `q ≥ 2`
- [x] `Unconditional/`: `bachSorenson_unconditional` (U), standard three + 16 `native_decide`
      (every class for `q < 2^15`, proved-sound checker)
- [ ] Open: the paper's constant `2` (same barrier as ankeny-grh)

### density-rh: zero counting and the density hypothesis · **tier U (library tier D), complete, verified** · *RH-consequence; the zero count is known*
- [x] Zero-counting library `Density.ZeroCount`, unconditional (D), standard three only:
      `N(T) ≪ T log T` (`zeroCountOn_riemannZeta_le_of_subset_strip`) and
      `N(T+1) − N(T) ≪ log T` (`zeroCountOn_riemannZeta_le_of_subset_box`), with multiplicity.
      Other repos require density-rh for it instead of copying `Complex.zeroCountOn`
- [x] `densityHypothesis_of_RH` (C) and `Unconditional/` `density_hypothesis` (U), standard three
      only; statement verbatim from formal-conjectures `density_hypothesis_zeta_zeros` (open there).
      Checked 2026-11-24 at `637fd12`. Under RH the count is zero for `σ > 1/2`, and `σ = 1/2`
      is the unconditional `N(T)` bound
- [ ] In progress: `guth_maynard_zero_density` (the 30/13 statement) as a corollary

### nicolas-rh: Nicolas' inequality `N_k/φ(N_k) > e^γ log log N_k`, all `k ≥ 1` · **tier U, complete, verified** · *RH-equivalent*
- [x] `nicolas_of_RH` (C) and `Unconditional/` `nicolas_unconditional` (U): standard three + 1
      `native_decide` (`Nicolas.Check.loop_ok`: rational interval check at the 9591 primes
      `3 ≤ p ≤ 10^5`, proved-sound checker). Checked 2026-11-24 at `4229e63`
- [x] No formal-conjectures statement exists; `kthPrimorial` copied verbatim from it
- [x] Requires robin-rh at `dfa8d63` for its Mertens and RH estimates; does not import `Robin/Small.lean`
- [ ] Bump the robin-rh pin once robin PR #3 merges

### mills-rh: Mills' constant in `(1.3063778838, 1.3063778839)` · **lower bound tier D; enclosure C + H; in progress** · *known (lower bound); RH-consequence (enclosure)*
- [x] `mills_lower_bound` (D), standard three only; statements verbatim from formal-conjectures
- [x] `mills_bounds_of_primeBetweenCubes` from the single hypothesis `PrimeBetweenCubes x₀`,
      any `x₀ ≤ 2521008887` (PR #1, open)
- [ ] Discharge `PrimeBetweenCubes` from Schoenfeld's bound once schoenfeld-rh is on `main`

### hironaka-fc: Hironaka's resolution of singularities in characteristic 0 · **tier U₀, complete on PR #1 (open), verified** · *known*
- [x] Statement matches formal-conjectures `resolution_of_singularities_of_charZero` verbatim
- [x] `hironaka_of_smoothModification` (H; input `SmoothModification`, Mathlib objects only), no
      `sorry`, standard three only
- [x] `Unconditional/`: `resolution_of_singularities_of_charZero` (U₀), standard three only. It
      imports one riemann-hypothesis module and uses no RH or GRH theorem
- [x] Group A in `docs/LITERATURE_STATUS.md`: a formalisation of Hironaka 1964. The resolution
      algorithm is the RH repo's; this repo proves the glue (about 90 lines)
- [ ] Tier D: discharge `SmoothModification` from resolutionorg/hironaka (Apache-2.0) once it is
      ported from Lean `v4.35.0` (420,000 lines, 835 Mathlib commits behind the pin)
- [ ] #26 Zariski's local uniformisation belongs in this repo; not started

### In progress, nothing verified yet
Scaffolded 2026-11-24, one agent each on branch `finality`; the gitlink is the scaffold commit.
- [ ] weinberger-grh: idoneal numbers and class number one under GRH (#1) · *RH-consequence*
- [ ] schoenfeld-rh: `|π(x) − li(x)| < √x log x/(8π)` under RH (#2); target statements fixed · *RH-consequence*
- [ ] cramer-rh: Cramér's prime-gap theorem under RH (#5) · *RH-consequence*
- [ ] goldbach-grh: ternary Goldbach under GRH (#6) · *known, via GRH here*
- [ ] mertens-rh: `M(x) = O(x^{1/2+ε})`, plus Riesz and Hardy–Littlewood (#10, #16) · *RH-equivalent*
- [ ] lls-grh: Lamzouri–Li–Soundararajan least primes and `L(1,χ)` bounds (#12, #13) · *RH-consequence*
- [ ] erdos-233: sum of squared prime gaps under RH (#14) · *RH-consequence*
- [ ] littlewood-rh: `log|ζ(1/2+it)| ≪ log t / log log t` (#15) · *RH-consequence*

## Working here

- Changes to this superproject's own files (`AGENTS.md`, `README.md`, `docs/`, `scripts/`) go
  straight to `main`: no worktree, no PR.
- For cross-repo work inside the submodules, run `worktree <slug>` here at the top level
  (never inside a submodule). PR each submodule branch to `senamakel/<repo>`, then commit the
  updated gitlinks and checklist here. To refresh every pin:
  `git submodule update --remote` followed by a review of what changed.
- Adding a conjecture: `git submodule add https://github.com/senamakel/<repo>.git <repo>`, then
  give it a row in `README.md` and a section in the checklist below.
- Lean projects with no `.lake` here yet: run `lake exe cache get` first in erdos-985. The
  siblings will build only after the pins are fixed.
- Build one module at a time when iterating (`lake build Artin.Main`). The `native_decide`
  modules dominate build time (grosswald about 10 CPU-minutes, ankeny about 20).
- After any change to a headline theorem, re-run `#print axioms` and update the README block in
  the same PR.
