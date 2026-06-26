# Definitions and Notation

All notation is fixed here and used consistently throughout the proofs and code.

## State and parameters
- **m ∈ ℝ** — the scalar **misalignment order parameter** (the internal-state coordinate `μ`
  of the FEP). Identified empirically with `|PC1|` of trait drift (Nghiem 2026), the
  toxic-persona latent activation (Wang/OpenAI 2025), or the susceptibility `S` /
  inverse-robustness `1/R` (Costa–Vicente 2026). `m=0` ≙ aligned; `m>0` ≙ misaligned.
  We allow `m∈ℝ` so the symmetric (pitchfork) structure is visible; the physical observable
  is `|m|`.
- **λ ≥ 0** — the **control / intervention-strength parameter**: malicious-data fraction, or
  (rescaled) training step, LoRA rank, or learning rate. Plays the role of Kuehn's slow
  variable `y` and Ma–Wang's `λ`.
- **h ∈ ℝ** — the **explicit misalignment bias field**: the *direct* pull of the malicious
  data toward `m>0` (asymmetry of the intervention). `h=0` ≙ a perfectly symmetric
  (rank-deficient / orthogonal-gradient) intervention; `h>0` ≙ a biased one. The two
  unfolding parameters of the cusp are `(a,h)`, both functions of `λ`.

## Free energy
- **Variational free energy / effective potential** `F(m; λ, h)`. By the FEP free-energy
  lemma (Friston, Thm C below) the expected internal dynamics are gradient descent on `F`.
- **Landau / cusp normal form** (central object):
  ```
  F(m; a, h) = ¼ b m⁴ + ½ a m² − h m ,      b > 0 .
  ```
  with **stiffness** `a = a(λ)` and **bias** `h = h(λ)`. We use the affine calibration
  ```
  a(λ) = a₀ − c λ   (c>0, a₀>0)        h(λ) = h₀ + e λ   (e≥0, h₀≥0).
  ```
- **Gradient flow** (deterministic): `ṁ = −∂F/∂m = −(b m³ + a m − h)`.
- **Stochastic dynamics** (FEP at NESS, additive noise): `dm = −F'(m)\,dt + σ\,dW`,
  `σ>0` the fluctuation amplitude.

## Stability objects
- **Curvature / Hessian** `H(m) = ∂²F/∂m² = 3 b m² + a`. Eigenvalue (1-D) of the Jacobian of
  the flow at an equilibrium `m_e` is `−H(m_e)`; `m_e` is linearly stable iff `H(m_e)>0`.
- **Recovery rate** `α(λ) = H(m_e(λ))` at the aligned equilibrium — the OU relaxation rate.
- **Lyapunov exponent** of an equilibrium = `−H(m_e)` (contraction rate of the gradient flow).

## Bifurcation sets
- **Equilibrium set** `b m³ + a m − h = 0` (the cubic; the cusp catastrophe manifold).
- **Fold / saddle-node set**: equilibria where additionally `H=0`, i.e.
  `27 b h² + 4 a³ = 0` with `a<0` (the **cusp curve** in the `(a,h)` plane). Inside the cusp:
  three equilibria (bistable, hysteretic); outside: one.
- **Critical threshold** `λ*`: smallest `λ` at which the aligned equilibrium loses stability.
  - Symmetric case `h≡0`: `λ* = a₀/c` (pitchfork, `a(λ*)=0`).
  - Biased case `h≠0`: `λ_fold`, the `λ` solving the fold equation along `(a(λ),h(λ))`.

## Cited prior results (full statements in `literature_review.md`)
- **Thm A (Kuehn 2011)** — a codim-1 equilibrium bifurcation is catastrophic (jump) iff
  fold / subcritical-Hopf / subcritical-pitchfork / transcritical; supercritical = continuous.
- **Thm B (Ma–Wang 2008)** — for a gradient flow the transition is continuous iff the aligned
  point stays locally asymptotically stable at `λ₀`; reduced leading nonlinearity `α<0`
  (here `b>0`) ⇒ continuous, `α>0` (here `b<0`) ⇒ jump.
- **Thm C (Friston 2021)** — internal flow = gradient descent on variational free energy `F`;
  `F` is a Lyapunov function. Grounds `ṁ=−F'`.
- **Thm D (Kuehn 2011)** — OU stationary variance `Var→σ²/(2α)`, autocorrelation `e^{−α|τ|}`;
  both diverge as `α→0` (critical slowing down). Recovery exponent `α∼(λ*−λ)^p`, `p=1`
  (pitchfork), `p=1/2` (fold).
- **Thm E (Kuehn 2011, Thm 6.1)** — noise-induced early transition likely iff `σ≫√ε`.
- **Thm F (Aguilera 2022)** — conditional MI `I(x;y|b)` peaks at criticality (blanket caveat).

## Conventions
`□` ends a proof. Numerical seeds are fixed (`seed=0/42`). All `λ` are dimensionless. Unless
stated, `b=1` (rescaling `m`), so only the ratios `a/b`, `h/b` matter (used in the data
collapse).
