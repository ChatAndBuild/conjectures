# What is new here and what is not

Written 2026-11-24. Read this before describing any result in this workspace to anyone.

**With one possible exception (erdos-985, below), nothing in this workspace is new mathematics.**
Every other target, finished or planned, is a theorem already in the literature, either proved outright or proved assuming RH or GRH. What the repos
add is a machine-checked Lean proof of a standard formal statement. The three groups below say
what kind of claim each result supports. Literature attributions are from memory unless a brief
in [`NEXT_TARGETS.md`](NEXT_TARGETS.md) marks them confirmed: check the primary source before
citing one in a README.

## How to describe a result

- **Group A:** "a Lean formalisation of X (author, year)". Never "a proof of X".
- **Group B:** "a Lean proof that GRH implies X, following author, year" for the main library.
  For the `Unconditional/` theorem: "X, given the Lean proof of RH/GRH in
  leanprover-community/riemann-hypothesis, which has not been independently verified". Never
  "X is now proved" or "we solved X".
- **Group C:** as B, plus: "X is equivalent to RH, so this says nothing beyond the RH claim".
- If the RH proof in riemann-hypothesis fails verification, every tier-U theorem falls back to
  its tier-C form. The tier-C forms and everything in group A marked "no RH used" survive.
- Credit for any unconditional consequence of RH belongs to the RH proof, if it stands, and to
  the authors of the conditional theorem. It does not belong to this workspace.

## Group A: theorems already proved unconditionally (labels **known** and **known, via GRH here**)

A formalisation, nothing more. Where our proof goes through GRH, it is **weaker** than the
literature: the main-library theorem assumes a hypothesis the published proof does not need.

| Result | Proved by | Our route | Note |
|---|---|---|---|
| hironaka-fc (#25), Hironaka's resolution in characteristic 0 | Hironaka 1964 | no RH; imports the RH repo's resolution proof (U₀) | glue only; the algorithm is not ours |
| #26 Zariski's local uniformisation | Zariski 1940 | no RH (U₀) | |
| #27 Auslander–Reiten over regular local rings | textbook | no RH (U₀) | |
| #20 Linnik's theorem | Linnik 1944 | no RH (U₀) | |
| #18 Erdős 696, #19 Erdős 694 | marked solved on erdosproblems.com | no RH (U₀) | existing Lean proofs with axioms; we discharge the axioms |
| #28 Cox, primes `x² + ny²` | classical (class field theory) | no RH (U₀) | |
| #29 Kummer's criterion | Kummer 1850 | no RH (U₀) | |
| #32 `h(−d) → ∞` | Heilbronn 1934, Siegel 1935 | no RH (U₀) | |
| density-rh, `N(T) ≪ T log T` | von Mangoldt 1905 | no RH (D) | |
| mills-rh, lower bound for Mills' constant | elementary | no RH (D) | |
| #17 Bombieri–Vinogradov | Bombieri 1965, A. I. Vinogradov 1965 | **via GRH** | weaker than the literature |
| #21 Pollack's theorem, Erdős 1141 | Pollack 2017 | **via GRH** | weaker than the literature |
| #22 Erdős 980, `k = 2` | Erdős 1961 | **via GRH** | weaker than the literature |
| #23 class number one | Heegner 1952, Baker 1966, Stark 1967 | **via GRH** | weaker than the literature |
| #30 Littlewood's sign changes | Littlewood 1914 | **via GRH** | weaker than the literature |
| #31 Titchmarsh divisor problem | Linnik 1961 | **via GRH** | weaker than the literature |
| #6 goldbach-grh, ternary Goldbach | Helfgott 2013 (Deshouillers–Effinger–te Riele–Zinoviev 1997 under GRH) | **via GRH** | weaker than the literature |

For the "via GRH" rows the honest headline is "X under GRH, in Lean". The unconditional theorem
is somebody else's and our proof does not reach it without the RH repo.

## Group B: known consequences of RH or GRH, open without them (label **RH-consequence**)

Each is a published conditional theorem. The main library formalises it (tier C). The
`Unconditional/` theorem is exactly as reliable as the RH repo's proof.

| Result | Conditional theorem due to |
|---|---|
| ankeny-grh, least quadratic nonresidue `≪ log² p` | Ankeny 1952; explicit, Bach 1990 (constant 2; ours is `21/5`, weaker) |
| miller-grh, deterministic Miller–Rabin | Miller 1976 (unconditional polynomial-time primality is Agrawal–Kayal–Saxena 2002, by another method) |
| bach-sorenson-grh, least prime in a progression | Bach–Sorenson 1996 (constant 2; ours is `7/2`, weaker) |
| grosswald-grh | Cohen–Oliveira e Silva–Trudgian 2016 |
| lindelof-rh, Lindelöf for ζ and Dirichlet L | classical; Littlewood |
| artin-grh, Artin's conjecture under GRH for Kummer fields | Hooley 1967. Stays tier C: the RH repo does not cover those fields |
| #1 weinberger-grh, idoneal numbers | Weinberger 1973 |
| #2 schoenfeld-rh, #5 cramer-rh | von Koch 1901, Schoenfeld 1976; Cramér 1920 |
| mills-rh, the enclosure of Mills' constant | Caldwell–Cheng 2005 |
| density-rh, the density hypothesis | immediate from RH |
| #12, #13 lls-grh | Lamzouri–Li–Soundararajan 2015 |
| #14 erdos-233, upper bound | Cramér 1936, Selberg 1943 |
| #15 littlewood-rh | Littlewood 1924 |
| #24 ERH for abelian number fields | standard: equivalent to GRH for Dirichlet L-functions |

## The one candidate for "new": erdos-985

Erdős Problem 985 (every odd prime `p` has a prime primitive root `q < p`) is open. The
implication "GRH implies Erdős 985" is proved in this workspace: in Lean (`erdos_985_of_GRH`)
and in the repo's own paper, `paper/erdos985.pdf` (November 2026). Its method is credited to
Bach's explicit bounds on weighted prime sums, through Lemma 1 of McGown–Treviño–Trudgian,
*Resolving Grosswald's conjecture on GRH* (arXiv:1508.05182). Neither session knows of an
earlier published proof of the implication itself.

What that supports, and what it doesn't:

- If no earlier proof exists, "GRH implies Erdős 985" is a new **conditional** theorem. That is
  a real, modest result, and it stands whatever happens to the RH repo.
- It is not a solution of Erdős 985. The unconditional statement still rests on the unverified
  RH proof, like everything in group B.
- "No earlier proof exists" has not been checked. Before the label **new** is used: search the
  literature (erdosproblems.com's page for 985 and its references, MathSciNet/zbMATH for
  primitive roots under GRH, the papers citing arXiv:1508.05182), and have the paper read by
  someone outside the project. McGown–Treviño–Trudgian prove a prime primitive root below
  `√p − 2` for large `p` under GRH, which is close to this statement; check whether their
  result with a finite computation already gives it.
- The label is the user's decision.

## Group C: statements equivalent to RH (label **RH-equivalent**)

Proving one of these "unconditionally" is a restatement of the RH claim. They are the riskiest
to announce.

| Result | Equivalence due to |
|---|---|
| robin-rh, Robin's inequality; Lagarias's form | Robin 1984; Lagarias 2002 |
| nicolas-rh | Nicolas 1983 |
| li-criterion-rh | Li 1997 (we prove the direction RH ⇒ positivity) |
| #10 mertens-rh, `M(x) = O(x^{1/2+ε})` | Littlewood 1912 |
| #16 Riesz and Hardy–Littlewood criteria | Riesz 1916; Hardy–Littlewood 1916 |

## Is anything a genuine solution?

No open problem is settled by an argument that is ours. One conditional theorem may be new:
"GRH implies Erdős 985" (see above).

- Three rounds of search found no open problem that follows from the RH repo's lemmas by a new
  argument. Every open statement we can reach (idoneal numbers, the density hypothesis, the
  Mertens bound, Erdős 233, …) is in group B or C: its conditional proof is published, and the
  only new ingredient is the RH proof itself.
- A genuine solution would need one of two things. Either an open problem **not** already known
  to follow from RH or GRH, proved with new mathematics; or an independently verified RH proof,
  in which case groups B and C become real unconditional theorems, with the credit described
  above.
- The second is the dependency everything hangs on. Two concrete steps would firm it up:
  `RH_FULL_BUILD=1` (rebuild riemann-hypothesis from source; never run), and following the
  community Comparator verification in that repository.

What the workspace can claim today without risk: Lean formalisations of the conditional
theorems (tier C), the group A results that use no RH, and working links from the RH repo's
statements to a dozen classical consequences, which is useful evidence for whoever verifies it.
