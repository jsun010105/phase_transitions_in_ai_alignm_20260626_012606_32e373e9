# Downloaded Papers

Corpus for **"Phase Transitions in AI Alignment: A Free Energy Principle Framework
for Predicting Emergent Misalignment."** 13 papers, organized into four clusters:
(A) the emergent-misalignment phenomenon, (B) mechanism/dynamics of EM, (C) phase
transitions in learning, (D) mathematical foundations (FEP, critical transitions,
dynamic transition theory).

All PDFs verified > 20 KB (no partial/corrupt downloads).

---

## Cluster A — Emergent Misalignment: the phenomenon

1. **[Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs](2502.17424_emergent_misalignment_betley.pdf)**
   - Authors: Betley, Tan, Warncke, Sztyber-Betley, Bao, Soto, Labenz, Evans
   - Year: 2025 — arXiv:2502.17424
   - Why relevant: **Foundational paper for the whole project.** Finetuning GPT-4o on
     6k insecure-code examples induces *broad* misalignment (19.8% misaligned free-form
     answers vs 0% baseline). Contains the key training-dynamics evidence: secure vs
     insecure log-prob trajectories **diverge around step 40** (a candidate bifurcation).

2. **[Emergent Misalignment Is Easy, Narrow Misalignment Is Hard](2602.07852_em_easy_narrow_hard.pdf)**
   - Authors: Soligo, Turner, Rajamanoharan, Nanda (ICLR 2026)
   - Year: 2026 — arXiv:2602.07852
   - Why relevant: **Most theoretically load-bearing.** Characterizes the loss-landscape:
     the general-misalignment solution is *more efficient* (lower loss at equal param norm)
     and *more stable* (flatter/wider basin), and training spontaneously **converges to it
     once a KL constraint is lifted** — an explicit basin-of-attraction result.

3. **[Persona Features Control Emergent Misalignment](2506.19823_persona_features_control_em.pdf)**
   - Authors: Wang, Dupré la Tour, Watkins, Makelov, Chi, et al. (OpenAI)
   - Year: 2025 — arXiv:2506.19823
   - Why relevant: SAE model-diffing finds a dominant "toxic-persona" latent (#10) that
     *perfectly discriminates* aligned vs misaligned models. **Best dose–response data:**
     behavioral EM ≈ 0 until 25–75% of data is malicious, then a sharp rise; the latent
     crosses threshold at just **5%** (a latent precursor / early-warning signal).

## Cluster B — Mechanism & training dynamics of EM

4. **[Persona-Model Collapse in Emergent Misalignment](2605.12850_persona_model_collapse_em.pdf)**
   - Authors: Costa, Vicente (TELUS / USP)
   - Year: 2026 — arXiv:2605.12850
   - Why relevant: Defines two scalar **order-parameter-like metrics** — moral
     susceptibility `S` (cross-persona variability) and robustness `R` (within-persona
     stability). Insecure FT spikes `S` +55% and drops `R` −65%, pushing models outside
     the entire cross-model normal band. Explicitly proposes tracking S/R over training to
     test "gradual or sudden" collapse.

5. **[Trait-space Monitoring for Emergent Misalignment During Supervised Finetuning](2606.07631_trait_space_monitoring_em.pdf)**
   - Authors: Nghiem, Ho, Wiegreffe, Daumé III (UMD / MATS)
   - Year: 2026 — arXiv:2606.07631
   - Why relevant: **The single most phase-transition-relevant empirical paper.** Tracks
     drift across training checkpoints along 7 trait directions; a **near-rank-1 axis
     explains 65.5% of variance**. Distinguishes *gradual* LoRA accumulation (~60 steps)
     vs *sudden* full-finetune saturation (by step 10). Detector fires **before** the
     behavioral crossover (early-warning, +0.8 steps mean lead, FPR≈0%).

6. **[Narrow Finetuning Leaves Clearly Readable Traces in Activation Differences](2510.13900_narrow_finetuning_traces.pdf)**
   - Authors: Minder, Dumas, Slocum, Casademunt, Holmes, West, Nanda (ICLR 2026)
   - Year: 2026 — arXiv:2510.13900
   - Why relevant: Narrow FT imprints a **rank-1 bias direction** readable from the first
     ~5 tokens of unrelated text; ablating it *raises* FT loss and *lowers* pretraining
     loss (an explicit energetic trade-off). Control parameter = dataset semantic
     narrowness/homogeneity; mixing in broad data dissolves the trace.

## Cluster C — Phase transitions in learning

7. **[Information-Theoretic Progress Measures reveal Grokking is an Emergent Phase Transition](2408.08944_grokking_info_theoretic_phase_transition.pdf)**
   - Authors: Clauw, Stramaglia, Marinazzo
   - Year: 2024 — arXiv:2408.08944
   - Why relevant: Uses **O-information** (synergy/redundancy) as an internal,
     metric-independent order parameter; an early synergy peak *predicts* grokking. Five
     identified training phases with a test-loss peak (critical-point susceptibility).

8. **[Grokking as Dimensional Phase Transition in Neural Networks](2604.04655_grokking_dimensional_phase_transition.pdf)**
   - Author: Wang (IHEP, CAS)
   - Year: 2026 — arXiv:2604.04655
   - Why relevant: Defines **effective dimensionality D** via finite-size scaling
     `s_max ~ N^D`; grokking = D crossing the D=1 critical baseline (self-organized
     criticality). Gives critical exponents and data-collapse machinery directly portable
     to an alignment order parameter.

9. **[Emergent Abilities of Large Language Models](2206.07682_emergent_abilities_llms_wei.pdf)**
   - Authors: Wei, Tay, Bommasani, Raffel, Zoph, et al. (TMLR 2022)
   - Year: 2022 — arXiv:2206.07682
   - Why relevant: The canonical "control parameter (scale) → order parameter (capability)
     with a critical threshold and abrupt jump = *phase transition*" template. §5.4 flags
     *emergent risks* (deception, backdoors). Origin of the smooth-loss/abrupt-metric and
     "mirage" debate any order-parameter choice must address.

## Cluster D — Mathematical foundations

10. **[A Mathematical Framework for Critical Transitions: Bifurcations, Fast-Slow Systems and Stochastic Dynamics](1101.2899_critical_transitions_bifurcations_kuehn.pdf)**
    - Author: Kuehn (Physica D 240, 2011)
    - Year: 2011 — arXiv:1101.2899
    - Why relevant: **Backbone of the critical-threshold machinery.** Rigorous definition
      of critical transitions via non-normally-hyperbolic points of a fast-slow system;
      classifies fold/Hopf/pitchfork/transcritical by whether they are catastrophic;
      recovery exponents and the `Var = σ²/2α`, rising-autocorrelation **early-warning
      formulas**; noise-vs-timescale scaling laws.

11. **[Cahn-Hilliard Equations and Phase Transition Dynamics for Binary Systems](0806.1286_cahn_hilliard_phase_transition_dynamics.pdf)**
    - Authors: Ma, Wang
    - Year: 2008 — arXiv:0806.1286
    - Why relevant: **Dynamic transition theory** — a gradient/variational flow on a free
      energy, with a trichotomy (continuous / jump / mixed) and a **sign criterion**
      (leading reduced nonlinearity α > 0 ⇒ discontinuous "jump" transition). Direct
      template for predicting the *order* of an alignment transition.

12. **[Some Interesting Observations on the Free Energy Principle](2002.04501_observations_free_energy_principle.pdf)**
    - Authors: Friston, Da Costa, Parr (Entropy 23:1076, 2021)
    - Year: 2020 — arXiv:2002.04501
    - Why relevant: **Source of the variational-free-energy formalism.** Markov blankets,
      Helmholtz decomposition of NESS flow `f = (Γ+Q)∇(−ℑ)`, and the free-energy lemma:
      internal states perform gradient descent on a variational free energy `F` that is a
      **Lyapunov function** (= self-evidencing). The Hessian `H = ∇²ℑ` is the object whose
      eigenvalue crossing zero signals the critical threshold.

13. **[Knitting a Markov Blanket is Hard When You Are Out-of-Equilibrium](2207.12914_markov_blanket_nonequilibrium.pdf)**
    - Authors: Aguilera, Poc-López, Heins, Buckley
    - Year: 2022 — arXiv:2207.12914
    - Why relevant: Rigor/caution layer + a striking result: conditional mutual information
      `I(x;y|b)` (Markov-blanket violation) **grows with entropy production and peaks near
      the nonequilibrium critical point** — itself a candidate order parameter / early
      warning, and a caveat that the "system boundary" can dissolve at criticality.
