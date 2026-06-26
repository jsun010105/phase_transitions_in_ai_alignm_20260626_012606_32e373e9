# Resources Catalog

## Summary
Resources gathered for **"Phase Transitions in AI Alignment: A Free Energy Principle
Framework for Predicting Emergent Misalignment."** 13 papers (all deep-read and
extracted), a symbolic/numeric verification toolchain, and an arXiv search helper.

## Papers
Total downloaded: **13** (all verified > 20 KB; see `papers/README.md` for full detail).

| Title | Authors | Year | File | Key results |
|-------|---------|------|------|-------------|
| Emergent Misalignment: Narrow finetuning... | Betley et al. | 2025 | `papers/2502.17424_*.pdf` | Foundational EM; 19.8% misaligned vs 0%; secure/insecure log-prob trajectories diverge ~step 40 |
| EM Is Easy, Narrow Misalignment Is Hard | Soligo, Turner, Rajamanoharan, Nanda | 2026 | `papers/2602.07852_*.pdf` | General solution = lower loss/equal norm + flatter basin; training converges to it once KL lifted |
| Persona Features Control EM | Wang et al. (OpenAI) | 2025 | `papers/2506.19823_*.pdf` | Toxic-persona SAE latent #10 perfectly discriminates; threshold dose–response 25–75%; latent at 5% |
| Persona-Model Collapse in EM | Costa, Vicente | 2026 | `papers/2605.12850_*.pdf` | Order params S (+55%), 1/R (+304%); leaves cross-model normal band |
| Trait-space Monitoring for EM during SFT | Nghiem et al. | 2026 | `papers/2606.07631_*.pdf` | Rank-1 drift axis (65.5% var); gradual LoRA vs sudden full-FT; detector leads crossover |
| Narrow Finetuning Leaves Readable Traces | Minder et al. | 2026 | `papers/2510.13900_*.pdf` | Rank-1 bias direction; ablation raises FT loss / lowers pretrain loss (energetic trade-off) |
| Grokking is an Emergent Phase Transition (info-theoretic) | Clauw, Stramaglia, Marinazzo | 2024 | `papers/2408.08944_*.pdf` | O-information synergy order parameter; early synergy peak predicts grokking |
| Grokking as Dimensional Phase Transition | Wang | 2026 | `papers/2604.04655_*.pdf` | Effective dim D via FSS `s_max~N^D`; D=1 critical; SOC, critical exponents |
| Emergent Abilities of LLMs | Wei et al. | 2022 | `papers/2206.07682_*.pdf` | Scale→capability phase-transition template; emergent risks; mirage debate origin |
| Critical Transitions: Bifurcations, Fast-Slow, Stochastic | Kuehn | 2011 | `papers/1101.2899_*.pdf` | Tipping-point classification; recovery exponents; Var=σ²/2α early-warning laws |
| Cahn-Hilliard & Phase Transition Dynamics | Ma, Wang | 2008 | `papers/0806.1286_*.pdf` | Dynamic transition trichotomy + sign criterion for gradient flows |
| Observations on the Free Energy Principle | Friston, Da Costa, Parr | 2020/21 | `papers/2002.04501_*.pdf` | Variational free energy `F` as Lyapunov function; NESS Helmholtz decomposition |
| Knitting a Markov Blanket is Hard Out-of-Equilibrium | Aguilera et al. | 2022 | `papers/2207.12914_*.pdf` | `I(x;y|b)` grows with entropy production, peaks at criticality |

## Prior Results Catalog (theorems available for our proofs)

| Result | Source | Statement summary | Used for |
|--------|--------|-------------------|----------|
| Thm A — bifurcation classification | Kuehn 2011, Props. 2.5–2.8 | fold/subcritical Hopf/subcritical pitchfork/transcritical = catastrophic jump; supercritical = continuous | Deciding whether EM is an abrupt (catastrophic) transition |
| Thm B — gradient transition order | Ma–Wang 2008, Thm A.3 + sign crit. | gradient flow: continuous iff aligned point loc. asympt. stable; leading nonlinearity α>0 ⇒ jump | Order of the alignment transition (our central lemma) |
| Thm C — free-energy lemma | Friston et al. 2021 | internal flow = gradient descent on variational free energy `F` (Lyapunov) | Casting alignment dynamics as FEP minimization |
| Thm D — early-warning laws | Kuehn 2011 | `Var→σ²/2α`, autocorr↑ as rate α→0 (critical slowing down) | Predictive precursor of misalignment onset |
| Thm E — noise/timescale scaling | Kuehn 2011, Thm 6.1 | noise-induced early transition likely iff σ≫√ε | When a narrow intervention triggers premature jump |
| Thm F — blanket degradation | Aguilera et al. 2022 | `I(x;y|b)` peaks at nonequilibrium critical point | Caveat + candidate order parameter / early warning |

## Computational Tools

| Tool | Purpose | Location | Notes |
|------|---------|----------|-------|
| SymPy | symbolic normal forms, Hessian, sign criterion | `.venv` (pip) | verified in `code/verify_transition_order.py` |
| NumPy / SciPy | SDE integration, root-finding, early-warning checks | `.venv` (pip) | OU variance reproduces `σ²/2a` to ~5% |
| Matplotlib | bifurcation diagrams, potentials | `.venv` (pip) | for the proof phase |
| `search_arxiv.py` | arXiv relevance search | `code/search_arxiv.py` | fallback (paper-finder service was offline) |
| `verify_transition_order.py` | demo of transition-order + early-warning machinery | `code/verify_transition_order.py` | runs clean; output matches theory |

## Resource Gathering Notes

### Search strategy
The paper-finder service at `localhost:8000` was **not running**, so I used the arXiv
Atom API (`code/search_arxiv.py`) with ~10 targeted queries spanning the four clusters
(emergent misalignment; EM mechanism; phase transitions in learning; FEP / critical-
transition mathematics). The arXiv full-text keyword search was noisy for generic physics
terms ("phase transition", "free energy") but precise for distinctive ML/EM terminology;
I selected on relevance, not raw hit count.

### Selection criteria
Prioritized: (1) the foundational EM paper (Betley) and its direct mechanistic follow-ups
that quantify thresholds / order parameters / training dynamics; (2) rigorous mathematical
sources for the *exact* machinery the hypothesis needs — bifurcation theory of tipping
points (Kuehn), dynamic transition theory for gradient flows (Ma–Wang), and the FEP
formalism (Friston). Quality over quantity: 13 directly-load-bearing papers rather than a
broad tangential sweep.

### Challenges encountered
- Paper-finder service offline → manual arXiv search (documented above).
- Several EM papers are 2026-dated preprints; all downloaded successfully from arXiv.
- Native PDF reading was unavailable to the deep-read subagents (no poppler); they
  extracted text via `pymupdf` in a throwaway temp env — **no repo files were polluted**.
- The empirical EM papers do **not** use phase-transition / free-energy vocabulary; the
  mathematical lens is the project's own contribution (flagged throughout the review).

## Recommendations for Proof Construction

1. **Proof strategy.** Model alignment as a gradient (variational) flow `ṁ = −∂F/∂m` on a
   free energy `F(m;λ)` (Thm C). Apply the gradient dynamic-transition theorem (Thm B) to
   classify the aligned→misaligned transition and the bifurcation classification (Thm A)
   to identify its catastrophic regime. Predict two parameter regions and a critical `λ*`.
2. **Key prerequisites to cite.** Friston free-energy lemma (Thm C); Kuehn tipping-point
   definition + recovery exponents + early-warning laws (Thms A, D, E); Ma–Wang sign
   criterion (Thm B); Aguilera blanket caveat (Thm F).
3. **Computational tools.** SymPy for the symbolic order-of-transition check; SciPy for the
   SDE early-warning verification and hysteresis; both demonstrated working in
   `code/verify_transition_order.py`.
4. **Potential difficulties.** The "mirage" objection (use a smooth internal order
   parameter); out-of-equilibrium Markov-blanket dissolution near criticality (restrict to
   quasi-gradient regime); identifiability of `F` up to solenoidal flow (use the symmetric/
   gradient part). Validate the predicted threshold against the empirical dose–response
   (25–75% malicious fraction) and step-40 trajectory divergence.

See `literature_review.md` for the full synthesis, precise theorem statements, and the
FEP ↔ critical-transitions ↔ emergent-misalignment dictionary.
