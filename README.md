# Phase Transitions in AI Alignment — Free Energy Principle Framework

A rigorous mathematical model in which **AI alignment dynamics are a variational free-energy
(FEP) gradient flow**, and a narrow misalignment intervention of strength `λ` triggers a
**phase transition** — universally reducible to the **cusp catastrophe**
`F(m;a,h) = ¼ b m⁴ + ½ a(λ) m² − h(λ) m`. The framework predicts *when* alignment robustly
holds (null result) vs *when* it catastrophically collapses (emergent misalignment), with
quantitative early-warning signals.

## Key results (all proved and computationally verified)
- **Critical threshold (Thm 2):** aligned state `m=0` stable iff `a(λ)>0`; loses stability at
  `λ*` (Hessian eigenvalue crosses zero) → robust-alignment vs emergent-misalignment regions.
- **Order of the transition (Thms 3–4):** *symmetric* intervention (`h=0`) → **continuous**
  supercritical pitchfork (`β=1/2`) — the gradual-LoRA regime; *biased* intervention (`h≠0`) →
  **catastrophic fold/jump with hysteresis** on the exact cusp curve `27bh²+4a³=0` — the
  sudden full-finetune regime. **One normal form unifies both empirical regimes.**
- **Early warning (Thm 5):** variance `σ²/2α` and autocorrelation time `1/α` **diverge** as
  `λ→λ*` (critical slowing down); the internal order parameter *leads* the behavioural jump.
- **Microscopic origin (Prop. 1):** the cusp is *derived* from a two-component FEP generative
  mixture, not assumed.
- **Evaluation:** universality data-collapse `R²=1.000`; null-vs-EM **ROC-AUC = 0.996**;
  threshold **MAE = 0.056**; Boltzmann stationary law matched to **JS = 6×10⁻⁴ nats**;
  hysteresis folds match analytics to **<1%**.

See **[REPORT.md](REPORT.md)** for full theorem statements, proofs, and discussion.

## Reproduce
```bash
source .venv/bin/activate        # Python 3.12, numpy/scipy/sympy/matplotlib (see pyproject.toml)
python src/run_all.py            # runs E1–E5; ~1–2 min CPU; writes results/ and figures/
```

## File structure
```
planning.md          research plan + motivation/novelty (Phase 0–1)
definitions.md       all notation, the free energy, cited prior theorems (A–F)
REPORT.md            PRIMARY DELIVERABLE: theorems 1–6, full proofs, verification, discussion
src/
  e1_microscopic_derivation.py   cusp derived from FEP mixture (SymPy)            [Prop. 1]
  e2_transition_order.py         threshold, pitchfork order, cusp set (SymPy)     [Thms 2–4]
  e3_bifurcation_numerics.py     bifurcation diagrams, phase map, hysteresis      [Thms 2–4]
  e4_early_warning_sde.py        critical slowing, Lyapunov exps, Boltzmann/JS    [Thm 5]
  e5_calibration_prediction.py   calibration, data-collapse, ROC-AUC, MAE         [Cor. 6]
  run_all.py                     reproduce everything
results/*.json       machine-readable numerical results for each experiment
figures/*.png        bifurcation diagrams, phase diagram, hysteresis, early-warning, collapse
papers/, literature_review.md, resources.md   pre-gathered background
```

## Scope / honesty
Calibration is to *reported summary statistics* (thresholds, % changes) from the empirical EM
literature, not raw per-sample data; the data-collapse is a consistency statement, not a
raw-data fit. The model is a 1-D mean-field reduction (justified by the empirically observed
rank-1 dominance) in the quasi-gradient regime. See REPORT.md §8 (Limitations).
