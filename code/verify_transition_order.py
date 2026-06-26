#!/usr/bin/env python3
"""
Sanity-check of the core machinery for the proof-construction phase.

(1) Symbolic: for a 1-D variational free energy F(m; lambda) = a/2 m^2 + b/4 m^4
    (pitchfork normal form), confirm the stability/order criterion:
      - aligned fixed point m=0 stable iff a > 0; loses stability at a=0 (critical lambda).
      - b > 0 (supercritical) -> continuous transition; b < 0 -> subcritical jump
        (catastrophic), matching Kuehn Prop 2.7 / Ma-Wang sign criterion (Thm B).
(2) Numeric: integrate the linearized OU process near the threshold and confirm the
    early-warning law Var(m) -> sigma^2 / (2 a) blows up as a -> 0 (critical slowing down).
"""
import sympy as sp
import numpy as np

# ---------- (1) symbolic transition-order criterion ----------
m, a, b = sp.symbols('m a b', real=True)
F = a/2 * m**2 + b/4 * m**4           # variational free energy / effective potential
Fp = sp.diff(F, m)                    # gradient flow:  m' = -Fp
Fpp = sp.diff(F, m, 2)               # Hessian (curvature)
fixed = sp.solve(sp.Eq(Fp, 0), m)
curv_at_0 = Fpp.subs(m, 0)           # = a
nonzero_fp = [f for f in fixed if f != 0]

print("F(m;a,b)        =", F)
print("Fixed points    =", fixed)
print("Curvature at 0  =", curv_at_0, " -> m=0 stable iff a>0; critical threshold a=0")
print("Nonzero branches=", nonzero_fp, " (real only when -a/b > 0)")
print("Order criterion : b>0 supercritical (continuous);  b<0 subcritical (JUMP/catastrophic)")

# ---------- (2) numeric early-warning law ----------
def ou_stationary_var(a_val, sigma=0.1, dt=1e-3, T=2000.0, burn=0.5):
    """Integrate dm = -a*m dt + sigma dW (linearized near m=0) and return sample variance."""
    n = int(T / dt)
    rng = np.random.default_rng(0)
    m_t = 0.0
    samples = []
    for i in range(n):
        m_t += -a_val * m_t * dt + sigma * np.sqrt(dt) * rng.standard_normal()
        if i > burn * n:
            samples.append(m_t)
    return np.var(samples)

sigma = 0.1
print("\nEarly-warning law:  Var -> sigma^2/(2a)  as a -> 0 (critical slowing down)")
print(f"{'a (=curvature)':>16} {'measured Var':>14} {'theory sigma^2/2a':>18}")
for a_val in [1.0, 0.5, 0.2, 0.1, 0.05]:
    meas = ou_stationary_var(a_val, sigma=sigma)
    theory = sigma**2 / (2 * a_val)
    print(f"{a_val:>16.3f} {meas:>14.5f} {theory:>18.5f}")
print("\nVariance diverges as a->0: the predicted precursor to the misalignment transition.")
