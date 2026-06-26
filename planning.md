# Planning — Phase Transitions in AI Alignment via the Free Energy Principle

## Research Question
Can AI alignment dynamics be modeled as a variational free-energy (FEP) gradient flow in
which a narrow misalignment intervention of strength `λ` induces a **phase transition** in
the energy landscape? Specifically: (i) does a critical threshold `λ*` exist separating
robust alignment (null result) from emergent misalignment (EM); (ii) what *order* is the
transition (continuous vs catastrophic jump); and (iii) can the framework **predict** which
intervention regimes give a null result vs a sudden behavioral collapse, with quantitative
early-warning precursors?

## Motivation & Novelty Assessment

### Why This Research Matters
Empirical AI-safety work (Betley 2025; Wang/OpenAI 2025; Soligo–Turner 2026; Nghiem 2026)
shows narrow finetuning *sometimes* causes broad misalignment and *sometimes* does not, with
no predictive theory. A mathematical framework that predicts *when* an alignment intervention
catastrophically fails — and provides measurable early-warning signals before the failure — is
directly safety-relevant: it converts a post-hoc empirical surprise into an a-priori
risk calculation.

### Gap in Existing Work
The literature splits cleanly. The empirical EM papers document threshold dose–response
curves, trajectory bifurcations, low-rank order parameters, and basin-of-attraction behavior
— but **none use the language of phase transitions, bifurcation theory, criticality, or free
energy**. The mathematical papers (Kuehn 2011 tipping points; Ma–Wang 2008 dynamic
transitions for gradient flows; Friston 2021 FEP) supply exactly that machinery but **never
touch alignment**. No existing model unifies them.

### Our Novel Contribution
1. An explicit **variational free energy `F(m;λ,h)`** for an alignment order parameter `m`,
   *derived* (not merely posited) from a two-component generative mixture in the FEP
   formalism, whose Landau coefficients carry the `λ`-dependence.
2. A theorem that the aligned→misaligned transition is governed by the **cusp catastrophe**
   `F = ¼ b m⁴ + ½ a(λ) m² − h(λ) m`, which **unifies both empirical regimes in one
   two-parameter family**: the symmetric axis (`h≈0`) gives a *continuous* supercritical
   pitchfork (the gradual-LoRA regime), while the biased branch (`h≠0`) gives a *catastrophic
   fold/jump with hysteresis* (the sudden full-finetune regime). This answers the literature's
   open question "the order may itself depend on the intervention regime."
3. Closed-form **critical thresholds**, **critical exponents**, and **early-warning laws**
   (variance and autocorrelation divergence), with a **data-collapse / universality** claim
   that the disparate empirical thresholds (25% vs 75% malicious fraction) are the *same*
   normal form rescaled by `λ*`.

### Experiment (computational-verification) Justification
- **E1 Microscopic derivation (SymPy):** show the Landau coefficients `a(λ), h(λ), b` emerge
  from a generative mixture free energy — grounds the model, defeats the "ad hoc potential"
  objection.
- **E2 Transition order (SymPy):** verify the stability/sign criterion (Ma–Wang Thm B,
  Kuehn Thm A) and the cusp bifurcation set `27 b h² + 4 a³ = 0` symbolically.
- **E3 Bifurcation numerics (NumPy/SciPy):** continuation of equilibrium branches, Jacobian
  eigenvalues, the `(λ,h)` phase diagram, and hysteresis loop — verifies Theorems 2–4.
- **E4 Early-warning SDE (SciPy):** integrate `dm=−F'dt+σdW`, confirm `Var→σ²/2α`,
  rising autocorrelation, critical slowing, Lyapunov exponents, and JS divergence between the
  simulated stationary law and the Boltzmann form `∝e^{−2F/σ²}` — verifies Theorem 5.
- **E5 Calibration & prediction (SciPy/sklearn-free):** fit `(a₀,c)` to the reported
  dose–response thresholds, report MAE on threshold prediction, ROC-AUC for null-vs-EM
  classification against SDE-generated ground truth, and the data collapse — addresses the
  methodology's evaluation metrics.

## Hypothesis Decomposition
- H1 (existence): ∃ `λ*` with aligned minimum stable for `λ<λ*`, unstable for `λ>λ*`
  (Hessian eigenvalue crosses zero). **Testable:** E2, E3.
- H2 (order): the transition order is set by the sign of the leading reduced nonlinearity and
  by the bias `h`; symmetric ⇒ continuous, biased ⇒ catastrophic jump. **Testable:** E2–E4.
- H3 (prediction): the framework classifies null vs EM outcomes and predicts thresholds with
  low error; disparate empirical thresholds collapse to one normal form. **Testable:** E5.
- H4 (early warning): variance and autocorrelation of `m` diverge as `λ→λ*`. **Testable:** E4.

## Proposed Methodology
### Approach
Model alignment as a 1-D variational free-energy gradient flow (FEP, Friston Thm C), reduce
the transition to the universal cusp normal form, classify it with the gradient
dynamic-transition theorem (Ma–Wang Thm B) and tipping-point classification (Kuehn Thm A),
and verify every analytic claim symbolically (SymPy) and numerically (SciPy SDE).

### Baselines / comparison
- The empirical regularities themselves (25–75% thresholds, step-40 trajectory divergence,
  latent-leads-behavior, gradual-LoRA vs sudden-full-FT kinetics) are the targets to recover.
- A naive **linear/logistic** dose–response (no bistability) as a null model the cusp must
  beat on the hysteresis and bimodality predictions.

### Evaluation Metrics (from the task spec)
- MAE between predicted and reported critical intervention strengths.
- ROC-AUC for null vs EM classification (vs SDE ground truth with finite noise/time).
- Lyapunov exponents of aligned vs misaligned attractors.
- Jensen–Shannon divergence between predicted (Boltzmann) and simulated `m`-distributions.

### Statistical Analysis Plan
Numerical checks use fixed seeds; OU-variance law confirmed within tolerance (~5–10%) across
≥4 control values; ROC-AUC over a grid of ≥200 intervention configs; report agreement
percentages and absolute errors rather than p-values (this is a modeling/verification study).

## Expected Outcomes
Support: a clean `λ*`, supercritical-pitchfork continuous branch, fold/hysteresis under bias,
diverging variance/autocorrelation, AUC ≫ 0.5, low threshold MAE, successful data collapse.
Refute: no eigenvalue crossing, variance not diverging, or the cusp failing to separate
null/EM outcomes better than the linear null model.

## Timeline (≤60 min)
Setup/read (done) → definitions (5m) → E1–E2 symbolic (12m) → E3 numerics (12m) →
E4 SDE (12m) → E5 calibration (8m) → REPORT/README (10m). Buffer absorbed by reusing the
existing `verify_transition_order.py` style.

## Potential Challenges
- Only *summary statistics* (thresholds, % changes) are available, not raw datasets →
  calibration is to reported summaries; stated honestly as a limitation.
- "Mirage" objection (abruptness as metric artifact) → use a *smooth internal* order parameter
  `m`; the bistability/hysteresis is intrinsic to `F`, not a thresholded metric.
- Out-of-equilibrium Markov-blanket dissolution (Aguilera Thm F) → restrict to the
  quasi-gradient regime; flag as scope limit.

## Success Criteria
All four sub-hypotheses (H1–H4) verified symbolically and numerically with agreement to
stated tolerances, the two-regime unification demonstrated, and the evaluation metrics
computed on calibrated/simulated data.
