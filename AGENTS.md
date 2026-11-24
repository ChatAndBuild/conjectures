# Conjectures workspace

This superproject (`github.com/senamakel/conjectures`) tracks the Lean 4 projects that formalise
number-theory conjectures and theorems, most of them conditional on RH or GRH. Each project is a
submodule (`github.com/senamakel/<name>`) pinned to the commit last reviewed. This file is the
tracker: when a box changes, update it here and bump the gitlink in the same commit.

Status as of 2026-11-24, read from each repo's `main` (sources, READMEs, `docs/`). **None of it
has been rebuilt on this box yet**; each "no sorry" claim comes from grepping the sources and
reading the READMEs. Re-check before you rely on a box below.

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

## Cross-repo issues (fix these first)

- [ ] **Dependency pins don't resolve.** All six sibling repos pin erdos-985 at
      `63d68188f2e4…`, which no longer exists on GitHub: erdos-985's history was rewritten
      (current `main` is `9538edb`). The commit survives only in the old checkout at
      `~/work/personal/erdos-985` (branch `audit-proof-63d6818`). Its tree differs from
      `9538edb` only by one README line, so repinning every sibling to `9538edb` (and updating
      `lake-manifest.json`) is safe. Until then, a fresh `lake build` fails in every repo except
      erdos-985.
- [ ] **SSH require URLs.** The siblings use `git@github.com:senamakel/...`. Switch them to `https://`
      so anonymous builds work (rule 7).
- [ ] `miller-grh` pins `ankeny-grh` at `035c7aa`. ankeny `main` is `129ad57`, two merges ahead.
      Bump it with the erdos repin.
- [ ] No repo has a `LICENSE` file, and artin-grh's README says riemann-hypothesis has no licence
      either. Decide on a licence, and check that copying its statement definitions word for word
      is acceptable.
- [ ] No CI anywhere. Add a GitHub Action that runs `lake build` and checks
      `#print axioms` against an allow-list (the cheap build, not the unconditional one).
- [ ] No unconditional check has run on this box. Run `scripts/check-unconditional.sh` once
      per repo and record the date and commit here.

## Per-repo checklist

### erdos-985: every odd prime has a prime primitive root `q < p` · **tier U, complete**
- [x] Statement matches formal-conjectures `erdos_985` verbatim
- [x] `erdos_985_of_GRH` (C), no `sorry`
- [x] `Unconditional/`: `erdos_985` (U), standard three + 20 `native_decide`
- [x] Finite check `p < 10^8` with a proved-sound checker
- [x] Paper (`paper/erdos985.pdf`)
- [ ] README: add a Credits section (Vendor/PNT is mentioned only inline) and a tier line
- [ ] Clean up the old checkout `~/work/personal/erdos-985` (branch `audit-proof-63d6818`, untracked `worktrees/`)

### ankeny-grh: Bach's explicit Ankeny bound · **tier U with constant 21/5, complete for 21/5**
- [x] `bach_of_GRH : BachSubgroupBound (21/5)`, `leastNonresidue_of_GRH`, no `sorry`
- [x] `Unconditional/`: `bach_unconditional`, `leastNonresidue_unconditional` (U), + 8 `native_decide`
- [x] README explains the deviation from Bach's `2`
- [ ] Optional: get to `c ≈ 4.05` by extending the computation to `2^18` (about 4× the work)
- [ ] Open: Bach's constant `2`, which needs a sharper explicit formula in erdos-985 (out of scope for now)

### miller-grh: deterministic Miller–Rabin under GRH · **tier U with constant 21/5, complete**
- [x] `miller_of_bach` and `prime_iff_of_bach` (reduction, standard axioms only)
- [x] `miller_of_GRH : MillerStatement (21/5)` and the executable `millerTestGRH_iff_prime`
- [x] `Unconditional/`: `miller_unconditional`, `millerTestGRH_iff_prime_unconditional` (U)
- [ ] `millerTest_iff_prime` assumes `BachSubgroupBound 2`, which no repo proves. In the README,
      label it conditional on Bach's constant, or drop it (rule 12)
- [ ] README heading "Results (no `sorry`, standard axioms only)" overclaims for the GRH
      theorems, which carry ankeny's 8 `native_decide`. Fix the wording
- [ ] Bump the ankeny pin (see cross-repo issues)

### grosswald-grh: `g(p) < √p − 2` for `p > 409` · **tier U for `p > 2.5·10^15`, tier H for the full statement**
- [x] `prime_primitive_root_of_GRH_large` (C), no `sorry`, + 10 `native_decide`
- [x] `Unconditional/`: `prime_primitive_root_large_unconditional` (U)
- [x] `grosswald_of_GRH` / `grosswald_of_verified` with `VerifiedUpTo 2500000000000000` as a hypothesis
- [ ] The full `GrosswaldStatement` stays tier H: the Cohen–Oliveira e Silva–Trudgian range
      `409 < p ≤ 2.5·10^15` (about 7·10^13 primes) is too large to replay. The only path to tier
      U is lowering the analytic threshold far enough that the remaining range fits in
      `native_decide`. Decide whether to attempt that or record it as the final state
- [ ] `scripts/__pycache__` is in the repo tree. Remove it and add a `.gitignore`

### robin-rh: Robin's inequality `σ(n) < e^γ n log log n`, `n > 5040` · **tier U + H**
- [x] `robin_of_RH_of_verified` (C + H), no `sorry`; `RobinVerifiedRange` is the Morrill–Platt range
- [x] `Unconditional/`: `robin_of_verified` (U + H), standard three only
- [x] `lagarias_of_RH`, Lagarias's form, with 1 `native_decide` for `13 ≤ n ≤ 5040`
- [ ] **Rule 4 violation**: `robin_small_range` in `Robin/Small.lean` is a cited `sorry`, and
      `robin_unconditional` / `lagarias_unconditional` carry `sorryAx`. Make
      `lagarias_of_RH_of_verified` take the range as a hypothesis too, then delete the `sorry`
      or move it into a clearly labelled `Cited/` module that no headline theorem uses
- [ ] Open: push the analytic threshold `x ≥ e^30` down far enough to check the remaining range
      directly (that would make it tier U with no H). Probably out of reach; record it as the final state if so

### lindelof-rh: Lindelöf from RH · **tier U for ζ, complete; Dirichlet stretch goal open**
- [x] `lindelof_of_RH` (C), no `sorry` on its path
- [x] `Unconditional/`: `lindelof_hypothesis` (U), standard three only
- [ ] Stretch: `dirichletLindelof_of_GRH` in `Lindelof/Dirichlet.lean` is `sorry`. Steps 1–8 of
      `docs/BLUEPRINT.md` with `ξ` replaced by the completed L-function of the inducing primitive character
- [ ] README is missing the standard sections (rule 10's table and caveat, Building, Layout). Add them

### artin-grh: Hooley's theorem (Artin under GRH for Kummer fields) · **tier C + H; formal-conjectures target still `sorry`**
- [x] Sieve half `artin_of_effectiveKummerChebotarev`, no `sorry`
- [x] Analytic core (explicit formula, zero sums, Hadamard, unsmoothing), no `sorry`
- [x] `conditional_artin_primitive_roots.parts.i_of_continuation` (C + H), standard three only;
      Hecke's continuation `DedekindContinuation` is the H hypothesis
- [ ] `effectiveKummerChebotarev_of_hooley` (`Artin/Interfaces.lean:53`) is `sorry`, so the
      formal-conjectures statement in `Artin/Main.lean` (without `hc`) is not proved. Closing it
      needs Hecke's continuation, functional equation and strip bound for `ζ_K`, which neither the
      Mathlib pin nor upstream Mathlib has
- [ ] Cannot become tier U: riemann-hypothesis gives RH for ζ and GRH for Dirichlet L only, and
      the Kummer fields are non-abelian, so `HooleyHypothesis` stays a hypothesis. That's fine and
      the README says so; the target is "C + Hecke formalised"
- [ ] The GitHub repo description is empty. Set one
- [ ] No `scripts/check-unconditional.sh` and no `Unconditional/` (expected; keep the README's explanation)
- [ ] README: the build section mentions a `../lean-grh-shared/packages` symlink that doesn't exist
      on this box. Either document how to set it up or drop it

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
