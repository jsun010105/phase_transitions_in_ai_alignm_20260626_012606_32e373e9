# Computational Tools

Lightweight computational support for the proof-construction phase. The research is
primarily analytical (bifurcation / dynamic-transition theory applied to a variational
free energy), so tools are used for **symbolic derivation of normal forms** and
**numerical verification** of critical thresholds, transition order, and early-warning
laws.

## Installed packages (in the workspace `.venv`)

| Tool | Purpose | How used |
|------|---------|----------|
| SymPy | symbolic computation | derive/normalize normal forms; verify the sign/eigenvalue criteria for transition order (Ma–Wang Thm B); compute Hessians `H = ∇²F` and locate `a(λ*)=0` symbolically |
| NumPy / SciPy | numerical integration & root-finding | integrate the SDE `dm = −F'(m)dt + σ dW`; locate the critical `λ*`; confirm `Var(m)→σ²/2α` and rising autocorrelation; detect hysteresis in fold / subcritical-pitchfork models |
| Matplotlib | visualization | bifurcation diagrams, potential `F(m;λ)` plots, early-warning variance curves |

All are pip/uv packages — no external repositories required. Install (already done):
```bash
source .venv/bin/activate
uv pip install sympy numpy scipy matplotlib
```

## Scripts

### `search_arxiv.py`
arXiv Atom-API search helper used during literature review (relevance-ranked, prints
title / id / date / abstract). Usage:
```bash
python code/search_arxiv.py 'all:emergent misalignment narrow finetuning' 8
```
Used because the paper-finder service at `localhost:8000` was not running in this
environment; manual arXiv search was the fallback.

## Notes for proof construction

- The key symbolic check is **the order of the transition**: reduce the alignment free
  energy `F(m;λ)` to a 1-D normal form near the aligned fixed point and read the sign of
  the leading reduced nonlinearity (`α > 0` ⇒ first-order jump / catastrophic misalignment;
  `α < 0` ⇒ continuous). SymPy `series` + `solve` handle this directly.
- The key numerical check is the **early-warning law**: integrate the linearized OU
  process near `λ*` and confirm stationary variance `σ²/(2α(λ))` blows up as `α(λ) → 0`.
- No SageMath needed; everything fits in SymPy/SciPy.
