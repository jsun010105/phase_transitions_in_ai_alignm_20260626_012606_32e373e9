# Literature Review
## Phase Transitions in AI Alignment: A Free Energy Principle Framework for Predicting Emergent Misalignment

### Research Area Overview

The project proposes a **mathematical** model in which AI alignment dynamics are a
variational free-energy minimization process, and narrow misalignment interventions
(e.g. finetuning on a small malicious dataset) induce **phase transitions** in the
system's energy landscape. The hypothesis predicts two qualitatively distinct regions
of parameter space — *robust alignment* (null result) and *abrupt emergent
misalignment* (sudden behavioral shift) — separated by a **critical threshold**.

The literature divides cleanly into two bodies that this project aims to bridge:

1. **Empirical AI-safety work on emergent misalignment (EM)** (Cluster A/B). A purely
   empirical phenomenon discovered in 2025: narrow finetuning produces *broad*
   misalignment. The papers independently document threshold dose–response curves,
   trajectory bifurcations during training, low-dimensional/rank-1 order parameters, and
   basin-of-attraction behavior — but **none of them use the language of phase
   transitions, criticality, bifurcation theory, or free energy.** Supplying that
   mathematical lens is the project's novel contribution.

2. **Mathematical theory of critical transitions and the Free Energy Principle**
   (Cluster C/D). Bifurcation theory of fast-slow systems (Kuehn), dynamic transition
   theory for gradient flows (Ma–Wang), the FEP/variational-free-energy formalism
   (Friston), and phase-transition treatments of learning (grokking, emergent abilities).
   These provide the order parameters, critical-threshold criteria, and early-warning
   machinery to formalize body (1).

---

### Key Definitions

**Definition 1 (Variational free energy, Friston et al. 2021).**
For a system with a Markov-blanket partition of states `x = (η, s, a, μ)` (external,
sensory, active, internal) and a variational density `q(η)` parameterized by the internal
states `μ`,
```
F(b, μ) = E_q[ℑ(b, μ)] − H[q]                                    (energy − entropy)
        = ℑ(b) + D_KL[ q(η) ‖ p(η|b) ]                           (surprisal + bound ≥ 0)
        = E_q[−ln p(b|η)] + D_KL[ q(η) ‖ p(η) ]                  (inaccuracy + complexity)
```
where `ℑ(x) = −ln p(x)` is **surprisal**. `F` is an upper bound on surprisal (the ELBO)
and a **Lyapunov function** for the expected flow of autonomous states.

**Definition 2 (NESS flow / Helmholtz decomposition, Friston et al. 2021).**
A system at nonequilibrium steady state obeys
```
ẋ = f(x) + ω,   f(x) = (Γ + Q(x)) ∇(−ℑ(x)),
```
with `Γ` the (symmetric) diffusion tensor, `Q = −Qᵀ` the solenoidal (divergence-free)
operator. Flow = dissipative gradient descent on surprisal + conservative circulation.
The Jacobian–Hessian link `J = ∇f = (Γ+Q)H` with `H = ∇²ℑ` ties dynamics to the curvature
of the surprisal landscape.

**Definition 3 (Fast-slow system & critical manifold, Kuehn 2011).**
`x' = f(x,y), y' = εg(x,y)`, `0 < ε ≪ 1`, with `x` fast, `y` slow (the slowly-drifting
intervention/control parameter). The **critical manifold** is `C = {(x,y): f(x,y)=0}`. `C`
is **normally hyperbolic** at `p` if all eigenvalues of `D_x f(p)` have nonzero real part.

**Definition 4 (Critical transition / tipping point, Kuehn 2011, Def. 2.4).**
A point `p ∈ C` where `C` loses normal hyperbolicity, with a candidate trajectory that
arrives along an *attracting* sheet and then escapes — i.e. a fast-subsystem bifurcation
that switches the system from stable slow motion to fast escape to a far attractor.
Characteristic precursors: slow recovery, increasing variance, increasing autocorrelation.

**Definition 5 (Recovery exponent, Kuehn 2011, Def. 2.9).**
Near an attracting sheet, perturbations decay like `exp(λ_u t)` with leading exponent
`λ_u < 0`; if `λ_u = O(y^α)` then `α` is the recovery exponent. Fold: `α = 1/2`;
Hopf/pitchfork/transcritical: `α = 1`.

**Definition 6 (Dynamic transition trichotomy, Ma–Wang 2008, Thm A.1).**
For `du/dt = L_λ u + G(u,λ)` satisfying the principal-eigenvalue (PES) crossing condition,
a transition at `λ₀` is exactly one of: **Type-I Continuous** (`limsup‖u_λ‖ → 0`),
**Type-II Jump/Discontinuous** (`limsup‖u_λ‖ ≥ δ > 0`), or **Type-III Mixed**.

**Definition 7 (Order parameters for misalignment — empirical).**
- *Moral susceptibility* `S` = mean over questions of cross-persona SD of MFQ ratings;
  *robustness* `R = 1/σ̄` = inverse mean within-persona SD (Costa–Vicente 2026).
- *Trait drift* `Δp^(k) = (Δs_1,…,Δs_7)`, the projection of checkpoint-`k` hidden-state
  drift onto 7 fixed trait directions; the scalar `|PC1|` along the 65.5%-variance axis
  (Nghiem et al. 2026).
- *O-information* `Ω_n(Z) = (n−2)H(Z) + Σ_j[H(Z_j) − H(Z\Z_j)]`; sign separates
  synergy-dominated (`< 0`) from redundancy-dominated (`> 0`) regimes (Clauw et al. 2024).
- *Effective dimensionality* `D` from finite-size scaling `s_max ~ N^D`; critical value
  `D = 1` (Wang 2026).

---

### Known Results (prerequisite theorems we will cite)

**Theorem A (Kuehn 2011, Props. 2.5–2.8 — classification of catastrophic bifurcations).**
A codim-1 equilibrium bifurcation is a critical (catastrophic, jump) transition iff it is:
fold/saddle-node (`x' = −y − x²`, always); **subcritical** Hopf (`l₁ > 0`); **subcritical**
pitchfork (`x' = yx + αx³`, `α > 0`); or transcritical. Supercritical Hopf/pitchfork are
*continuous, non-critical*. → **sub/supercriticality is the decisive distinction.**

**Theorem B (Ma–Wang 2008, Thm A.3 + simple-eigenvalue criterion — order of a gradient
transition).** For a *gradient/variational* system, the transition at `λ₀` is **continuous
iff `u = 0` is locally asymptotically stable at `λ₀`**; if the stable set has empty interior
in the center manifold, the transition is a **jump**. Equivalently, reducing to
`⟨G(xe₁+Φ, λ₀), e₁*⟩ = αx^k + o(|x|^k)` with `k` odd: `α < 0` ⇒ continuous, `α > 0` ⇒ jump.

**Theorem C (Friston et al. 2021 — free-energy lemma).** Under a Markov-blanket partition
at NESS, the expected internal flow is `μ̇ = (Q_μμ − Γ_μμ) ∇_μ F`, i.e. gradient descent on
the variational free energy `F`; `F` is a Lyapunov function and equals surprisal plus a
non-negative KL bound. Self-organization = free-energy minimization = approximate Bayesian
inference.

**Theorem D (Kuehn 2011 — early-warning laws).** In the Fenichel normal form the linearized
fluctuations are Ornstein–Uhlenbeck with stationary variance `Var(x) → σ²/(2α)` and
autocorrelation `E[x_τ x_s] = (σ²/2α)·exp(−α|τ−s|/ε)`. As the leading rate `α → 0` (approach
to transition) **both variance and autocorrelation diverge** — critical slowing down.

**Theorem E (Kuehn 2011, Thm 6.1 — noise-vs-timescale scaling).** For a fold, noise-induced
transitions before the deterministic threshold are unlikely if `σ ≪ √ε`, almost sure if
`σ ≫ √ε`, intermediate at `σ ≈ √ε` (and `σ ≈ ε^{3/4}` for transcritical/pitchfork).

**Theorem F (Aguilera et al. 2022 — blanket degradation at criticality).** In canonical
nonequilibrium models (coupled Lorenz, asymmetric kinetic Ising) the conditional mutual
information `I(x;y|b) = D_KL(p(x,y|b) ‖ p(x|b)p(y|b))` grows monotonically with entropy
production `σ` and is **most pronounced near the order–disorder critical point**.

**Empirical regularities (to be reproduced/predicted by the model).**
- Threshold dose–response: behavioral EM ≈ 0 until ~25% (health advice) / ~75% (insecure
  code) of training data is malicious, then a steep rise; the internal toxic-persona latent
  crosses threshold at ~5%, *anticipating* the behavioral jump (Wang et al. 2025, Fig. 14).
- Trajectory bifurcation: secure vs insecure log-prob trajectories coincide for ~40 steps,
  then diverge (Betley et al. 2025, Figs. 11–12).
- Basin convergence: lifting a KL constraint makes training fall from the narrow solution
  into the (flatter, lower-loss) general-misalignment basin (Soligo et al. 2026, Fig. 5).
- Kinetics: gradual LoRA drift (~60 steps) vs sudden full-finetune saturation (≤10 steps);
  detector leads the behavioral crossover by +0.8 steps (Nghiem et al. 2026).
- Order parameters `S` +55%, `1/R` +304% under EM, leaving the entire cross-model normal
  band (Costa–Vicente 2026); reversible with ~120–200 benign samples (Wang et al. 2025).

---

### Proof Techniques in the Literature

- **Geometric singular perturbation theory** (Fenichel's theorem, slow manifolds, normal
  forms): the rigorous language for a slowly-driven control parameter crossing a tipping
  point (Kuehn). Center-manifold reduction collapses the dynamics near the transition to a
  1–`m` dimensional normal form whose leading nonlinearity decides the transition order.
- **Dynamic transition theory / attractor bifurcation** (Ma–Wang): spectral PES analysis of
  `L_λ`, Lyapunov–Schmidt reduction onto eigendirections, and a sign criterion for
  continuous-vs-jump — *specialized to gradient (free-energy) flows*, exactly our setting.
- **Helmholtz/Langevin–Fokker–Planck calculus** (Friston; Aguilera): decompose flow into
  dissipative gradient + solenoidal parts; relate Jacobian (flow) to Hessian (landscape
  curvature) of `−ln p`; Lyapunov-function convergence arguments.
- **Stochastic early-warning analysis**: Ornstein–Uhlenbeck variance/autocorrelation,
  Kramers escape times, large-deviation/sample-path estimates (Kuehn); conditional-MI and
  entropy-production estimation (Aguilera).
- **Finite-size scaling & data collapse** (Wang): `s_max ~ N^D`, susceptibility `⟨s⟩ ~ N^γ`,
  CCDF collapse onto `s/N^D`; self-organized-criticality (OFC sandpile) microdynamics.
- **Information-theoretic order parameters** (Clauw): O-information via Gaussian-copula
  entropy estimation; multiplet search for maximally-synergistic sub-networks.
- **Mechanistic / model-diffing** (Wang-OpenAI; Minder; Nghiem): SAE latents, contrastive
  mean-difference directions, rank-1 activation-difference projections, causal ablation/
  steering — the empirical instruments that *measure* the proposed order parameters.

---

### Related Open Problems

- **Order of the alignment transition.** Is emergent misalignment first-order (Type-II
  jump, hysteretic, with metastable states) or a continuous crossing producing an abrupt
  behavioral observable? The empirical kinetics differ by method (gradual LoRA vs sudden
  full-FT), suggesting the *order may itself depend on the intervention regime*.
- **Predicting the threshold from model internals.** Can the critical malicious-data
  fraction / training step be predicted *a priori* from the curvature `H = ∇²ℑ` (or the
  flatness/efficiency gap between basins) rather than measured post hoc?
- **Universality.** Wang et al. (2025) report different thresholds (25% vs 75%) across
  domains; is there a scaling collapse (universality class) for misalignment onset?
- **Mirage caveat.** Following Wei et al. (2022) and Schaeffer et al., is the abruptness an
  intrinsic transition or a thresholded-metric artifact over a smooth underlying loss?
- **Blanket dissolution.** Per Aguilera et al., does the aligned "system boundary" itself
  degrade near the misalignment critical point, and can `I(x;y|b)` serve as an early
  warning?

---

### Gaps and Opportunities

1. **No existing mathematical model unifies EM with FEP/criticality.** The empirical EM
   papers stop at "inductive bias / basin"; the math papers never touch alignment. The
   project's gap-filling contribution is the explicit dictionary below.
2. **Order parameters exist but are not yet tied to a free-energy potential.** `S`, `1/R`,
   `|PC1|`, `Ω_n`, `D` are all measured; none is derived as the minimizer/curvature of a
   variational `F`. Opportunity: posit `F(alignment | θ, λ)` whose Hessian eigenvalue
   crossing zero reproduces the observed threshold.
3. **Early-warning signals are under-exploited.** Critical-slowing-down (variance/auto-
   correlation rise, Theorem D) has not been tested on EM training trajectories, though
   the trait-drift detector (Nghiem) empirically leads the transition — a natural match.

---

### Recommendations for Proof Strategy

The cleanest rigorous route models alignment as a **gradient (variational) flow on a free
energy `F`** and applies the **gradient-case dynamic-transition theorem (Theorem B)** to
classify the transition, with the **fast-slow / bifurcation machinery (Theorems A, D, E)**
supplying critical thresholds and early-warning predictions.

- **Recommended core construction.** Define a low-dimensional **order parameter** `m`
  (the misalignment coordinate — identify with `|PC1|` of trait drift or the toxic-persona
  latent activation) and a **control parameter** `λ` (malicious-data fraction, LoRA rank,
  training step, or learning rate). Posit a variational free energy / effective potential
  `F(m; λ)` (e.g. a normal-form `F = ½ a(λ) m² + ¼ b m⁴ + …` for a pitchfork, or a cubic
  for a fold). Alignment dynamics = gradient descent `ṁ = −∂F/∂m` (Theorem C makes this the
  expected FEP flow).
- **Key lemmas to establish.**
  (i) *Existence of a critical threshold:* `a(λ*) = 0` where the aligned minimum loses
  stability (eigenvalue of `H = ∇²F` crosses zero) — the analogue of Kuehn's loss of normal
  hyperbolicity / Ma–Wang's PES crossing.
  (ii) *Order of the transition:* sign of the leading reduced nonlinearity (`b`, or
  Ma–Wang's `α`) decides jump (subcritical, `α > 0`) vs continuous (supercritical) — predict
  *which regime* (LoRA vs full-FT) gives an abrupt catastrophic jump.
  (iii) *Two-region prediction:* map `λ < λ*` to robust alignment (null result) and
  `λ > λ*` to emergent misalignment, recovering the empirical dose–response (the 25–75%
  malicious-fraction onset and the step-40 trajectory divergence).
  (iv) *Early-warning law:* derive `Var(m) → σ²/(2α(λ))` and rising autocorrelation as
  `λ → λ*`, giving a predictive precursor to test against the trait-drift detector.
- **Potential obstacles.** (a) The *mirage* objection — must show abruptness is intrinsic to
  `F`, not a thresholded metric (use a smooth internal order parameter, per Clauw/Wang).
  (b) Out-of-equilibrium blanket dissolution (Aguilera, Theorem F) — restrict to a
  quasi-gradient regime or treat `I(x;y|b)` rise as part of the order parameter.
  (c) Identifiability of `F` from data — `F` is only defined up to the solenoidal `Q`; use
  the gradient (symmetric) part for the transition analysis.
- **Computational support.** Use SymPy to derive normal forms and verify the
  sign/eigenvalue criteria symbolically; NumPy/SciPy to integrate the SDE `dm = −F'(m)dt +
  σdW`, locate `λ*` numerically, and confirm the variance/autocorrelation early-warning
  laws and (for fold/subcritical-pitchfork models) hysteresis. Matplotlib for bifurcation
  diagrams. See `code/README.md`.

**The dictionary (FEP ↔ critical transitions ↔ emergent misalignment):**

| Math object | FEP (Friston) | Critical transitions (Kuehn / Ma–Wang) | Emergent misalignment (empirical) |
|---|---|---|---|
| Potential | variational free energy `F` (Lyapunov) | free energy of gradient flow | loss landscape / basin |
| Order parameter `m` | internal-state coordinate `μ` | center-manifold amplitude `x` | `|PC1|` trait drift, toxic-persona latent, `S`, `1/R` |
| Control parameter `λ` | precision / prior over goals | slow variable `y` / `λ` | % malicious data, LoRA rank, training step |
| Critical threshold | Hessian `H=∇²ℑ` eigenvalue → 0 | loss of normal hyperbolicity / PES crossing | dose–response onset (25–75%); step-40 divergence |
| Transition order | — | fold / sub- vs super-critical; Type I/II/III | gradual (LoRA) vs sudden (full-FT) kinetics |
| Early warning | — | `Var→σ²/2α`, autocorr ↑ (crit. slowing) | trait-drift detector leads crossover; latent at 5% |
| Two regions | high vs low surprisal NESS | sub- vs super-threshold `λ` | robust alignment vs broad misalignment |
