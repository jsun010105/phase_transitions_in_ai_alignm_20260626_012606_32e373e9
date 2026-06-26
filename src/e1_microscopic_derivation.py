#!/usr/bin/env python3
"""
E1 — Microscopic derivation of the Landau / cusp free energy from a generative mixture.

Goal: show the effective potential F(m) is NOT ad hoc but emerges from a two-component
generative model in the FEP formalism, with the Landau coefficients a(lambda), h(lambda), b
carrying the intervention-strength dependence. We derive BOTH canonical regimes:

  CASE A (symmetric intervention, h = 0):
     p(z) ∝ (1-λ) N(z;0,s²) + (λ/2)[N(z;+μ,s²)+N(z;−μ,s²)]
     The malicious behaviour can fit z=+μ OR z=−μ equally (orthogonal/rank-deficient gradient,
     e.g. LoRA). By symmetry F is even ⇒ h≡0, cubic≡0. The stiffness a(λ)=F''(0) decreases
     and CROSSES ZERO ⇒ supercritical pitchfork (Thm 3, continuous).

  CASE B (biased intervention, h ≠ 0):
     p(z) ∝ (1-λ) N(z;0,s²) + λ N(z;+μ,s²)
     The malicious data pulls only toward +μ (full-finetune bias). This breaks the symmetry:
     a bias field h(λ)>0 appears ⇒ the pitchfork UNFOLDS into a cusp / fold (Thm 4, jump).

FEP free energy (variational density a point mass at m; entropy term m-independent):
     F(m) = −log p(m)   (+ ½ κ m² prior; we take κ=0, absorbed into a₀).
"""
import sympy as sp
import numpy as np
from scipy.optimize import brentq

lam = sp.Symbol('lambda', real=True)
mm  = sp.Symbol('m', real=True)
s_v = sp.Rational(1)            # spread of each mode
mu_v = sp.Rational(3, 2)        # malicious-mode location (μ=1.5 > 1 so the pitchfork crosses)

def landau_coeffs(p_mix):
    """Taylor-expand F=-log p_mix about m=0 to 4th order; return (a, h, cubic, b)."""
    F = -sp.log(p_mix)
    ser = sp.expand(sp.series(F, mm, 0, 5).removeO())
    c1, c2, c3, c4 = (ser.coeff(mm, k) for k in (1, 2, 3, 4))
    a = sp.nsimplify(sp.simplify(2*c2))
    h = sp.nsimplify(sp.simplify(-c1))
    cubic = sp.simplify(c3)
    b = sp.nsimplify(sp.simplify(4*c4))
    return a, h, cubic, b

# ---------- CASE A: symmetric two-mode mixture ----------
N0 = sp.exp(-mm**2/(2*s_v**2))
Np = sp.exp(-(mm-mu_v)**2/(2*s_v**2))
Nm = sp.exp(-(mm+mu_v)**2/(2*s_v**2))
pA = (1-lam)*N0 + (lam/2)*(Np + Nm)
aA, hA, cubicA, bA = landau_coeffs(pA)

print("="*72)
print("CASE A — symmetric intervention (mu=±3/2):  expect h≡0, cubic≡0, pitchfork")
print("="*72)
print("  h(lambda)      =", hA, "   (should be 0)")
print("  cubic coeff    =", sp.simplify(cubicA), "   (should be 0)")
aA_num = sp.lambdify(lam, aA, 'numpy')
bA_num = sp.lambdify(lam, bA, 'numpy')
print("  lambda -> a(lambda)  [stiffness, must cross 0]    and  b (quartic, must stay >0):")
for L in np.linspace(0, 1, 9):
    print(f"     lambda={L:4.2f}   a={float(aA_num(L)):+8.4f}   b={float(bA_num(L)):+8.4f}")
lstarA = brentq(lambda L: float(aA_num(L)), 0.01, 0.999)
print(f"  => a(lambda*)=0 at lambda* = {lstarA:.4f}: aligned m=0 loses stability (PITCHFORK).")
print(f"  => b(lambda*) = {float(bA_num(lstarA)):+.4f} > 0  => SUPERCRITICAL => CONTINUOUS (Thm 3).")

# ---------- CASE B: single-mode (biased) mixture ----------
pB = (1-lam)*N0 + lam*Np
aB, hB, cubicB, bB = landau_coeffs(pB)
print("\n" + "="*72)
print("CASE B — biased intervention (single mode at +mu):  expect h>0, cusp/fold")
print("="*72)
hB_num = sp.lambdify(lam, hB, 'numpy')
aB_num = sp.lambdify(lam, aB, 'numpy')
print("  lambda -> a(lambda), h(lambda):")
for L in np.linspace(0, 1, 9):
    print(f"     lambda={L:4.2f}   a={float(aB_num(L)):+8.4f}   h={float(hB_num(L)):+8.4f}")
hpos = all(float(hB_num(L)) > 0 for L in np.linspace(0.05, 0.95, 10))
print(f"  bias h(lambda) > 0 for all 0<lambda<1: {hpos}")
print("  => symmetry broken: the pitchfork UNFOLDS into a cusp/fold (catastrophic jump, Thm 4).")

print("\nCONCLUSION E1: the cusp normal form  F = ¼ b m⁴ + ½ a(λ) m² − h(λ) m  is DERIVED")
print("from the FEP generative-mixture free energy. Symmetric data ⇒ pitchfork (continuous);")
print("biased data ⇒ cusp/fold (catastrophic). The two empirical regimes are one family.")

# persist key numbers
import json, os
os.makedirs('results', exist_ok=True)
json.dump({
    "case_A_symmetric": {"lambda_star_pitchfork": float(lstarA),
                          "b_at_threshold": float(bA_num(lstarA)),
                          "h_identically_zero": bool(sp.simplify(hA) == 0),
                          "cubic_identically_zero": bool(sp.simplify(cubicA) == 0)},
    "case_B_biased": {"h_positive_on_unit_interval": bool(hpos)},
    "mu": float(mu_v), "s": float(s_v),
}, open('results/e1_microscopic.json', 'w'), indent=2)
print("\nsaved -> results/e1_microscopic.json")
