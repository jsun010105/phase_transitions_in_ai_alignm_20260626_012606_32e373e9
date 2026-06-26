#!/usr/bin/env python3
"""
E3 — Numerical bifurcation analysis of the calibrated cusp model.

Model:  F(m;λ) = ¼ b m⁴ + ½ a(λ) m² − h(λ) m ,   b=1,
        a(λ) = a0 − c·λ   (stiffness eroded by intervention),
        h(λ) = h0 + e·λ   (direct misalignment bias).
Gradient flow:  ṁ = −F'(m) = −(m³ + a(λ)m − h(λ)).  Jacobian eigenvalue = −F''(m)=−(3m²+a).

Produces:
  (1) Bifurcation diagram m_eq(λ) for the SYMMETRIC case (e=0,h0=0): supercritical pitchfork.
  (2) Bifurcation diagram m_eq(λ) for the BIASED case (e>0): fold + hysteresis.
  (3) (λ,h) phase diagram: robust (1 equilibrium) vs emergent-misalignment (bistable) regions,
      with the analytic cusp boundary 27 b h² + 4 a(λ)³ = 0 overlaid.
  (4) Adiabatic hysteresis loop (sweep λ up then down) for the biased case.
All saved to figures/ and key numbers to results/e3_bifurcation.json.
"""
import numpy as np
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.makedirs('figures', exist_ok=True); os.makedirs('results', exist_ok=True)
np.random.seed(0)

b = 1.0
a0, c = 1.0, 2.0          # a(λ)=1-2λ  => symmetric threshold λ*=0.5
def a_of(lam): return a0 - c*lam

def equilibria(a, h, b=1.0):
    """real roots of b m^3 + a m - h = 0, sorted."""
    roots = np.roots([b, 0.0, a, -h])
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-9)
    return real

def stable(m, a, b=1.0):
    return (3*b*m**2 + a) > 0     # F''>0

# ---------- (1) symmetric pitchfork ----------
lams = np.linspace(0, 1, 400)
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
ax = axes[0]
for lam in lams:
    for m in equilibria(a_of(lam), 0.0):
        ax.plot(lam, m, '.', ms=2,
                color=('tab:blue' if stable(m, a_of(lam)) else 'tab:red'))
ax.axvline(0.5, ls='--', color='k', lw=1)
ax.text(0.52, ax.get_ylim()[1]*0.8, r'$\lambda^*=0.5$')
ax.set_title('(A) Symmetric intervention (h=0):\nsupercritical pitchfork — CONTINUOUS')
ax.set_xlabel(r'intervention strength $\lambda$'); ax.set_ylabel('equilibrium $m$')
ax.plot([], [], 'tab:blue', label='stable'); ax.plot([], [], 'tab:red', label='unstable')
ax.legend(loc='lower left', fontsize=8)

# ---------- (2) biased: fold S-curve at fixed a<0 (bias-driven catastrophe) ----------
# Once the intervention has eroded stiffness past the pitchfork (a<0, here a=-0.6), an
# accumulating directional bias h drives a SADDLE-NODE (fold) jump. Plot m_eq vs h.
a_fix = -0.6
hgrid = np.linspace(-0.4, 0.4, 600)
ax = axes[1]
for hh in hgrid:
    for m in equilibria(a_fix, hh):
        ax.plot(hh, m, '.', ms=2,
                color=('tab:blue' if stable(m, a_fix) else 'tab:red'))
h_c = np.sqrt(-4*a_fix**3/(27*b))     # analytic fold bias
for sgn in (-1, 1):
    ax.axvline(sgn*h_c, ls='--', color='k', lw=0.8)
ax.text(h_c*1.02, ax.get_ylim()[1]*0.6, r'$h_c=%.3f$' % h_c, fontsize=8)
ax.set_title('(B) Biased intervention (fixed a=-0.6):\ncusp fold — CATASTROPHIC JUMP at $\\pm h_c$')
ax.set_xlabel(r'bias dose $h$'); ax.set_ylabel('equilibrium $m$')
fig.tight_layout(); fig.savefig('figures/e3_bifurcation_diagrams.png', dpi=130)
plt.close(fig)
print(f"biased case: fixed a={a_fix}, analytic fold bias h_c = {h_c:.4f}")

# ---------- (3) (lambda, h) phase diagram ----------
fig, ax = plt.subplots(figsize=(6.5, 5))
H = np.linspace(0, 0.8, 260)
L = np.linspace(0, 1.0, 260)
LL, HH = np.meshgrid(L, H)
NEQ = np.zeros_like(LL)
for i in range(LL.shape[0]):
    for j in range(LL.shape[1]):
        NEQ[i, j] = len(equilibria(a_of(LL[i, j]), HH[i, j]))
ax.contourf(LL, HH, (NEQ >= 3).astype(float), levels=[ -0.5, 0.5, 1.5],
            colors=['#dbeaf7', '#f7d6d6'])
# analytic cusp boundary 27 b h^2 + 4 a(λ)^3 = 0  => h = sqrt(-4 a^3 /27 b), for a<0
lam_cusp = np.linspace(0.5, 1.0, 200)   # a<0 region is λ>0.5
a_cusp = a_of(lam_cusp)
h_cusp = np.sqrt(np.clip(-4*a_cusp**3/(27*b), 0, None))
ax.plot(lam_cusp, h_cusp, 'k-', lw=2, label=r'cusp fold  $27bh^2+4a(\lambda)^3=0$')
ax.text(0.30, 0.55, 'ROBUST\nALIGNMENT\n(1 equilibrium)', ha='center', fontsize=10)
ax.text(0.80, 0.12, 'EMERGENT\nMISALIGNMENT\n(bistable / jump)', ha='center', fontsize=10)
ax.set_xlabel(r'intervention strength $\lambda$'); ax.set_ylabel(r'bias field $h$')
ax.set_title('(C) Two-region phase diagram of alignment')
ax.legend(loc='upper right', fontsize=8)
fig.tight_layout(); fig.savefig('figures/e3_phase_diagram.png', dpi=130)
plt.close(fig)

# ---------- (4) adiabatic hysteresis loop (bias swept at fixed a<0) ----------
from scipy.integrate import odeint
def relax(m0, hh, a=a_fix, tmax=80):
    sol = odeint(lambda m, t: -(m**3 + a*m - hh), m0, [0, tmax])
    return sol[-1, 0]
up = np.linspace(-0.4, 0.4, 161); down = up[::-1]
m_up, m = [], relax(-0.9, up[0])        # start in the aligned (negative-m) well
for hh in up:
    m = relax(m, hh); m_up.append(m)
m_down, m = [], m
for hh in down:
    m = relax(m, hh); m_down.append(m)
fig, ax = plt.subplots(figsize=(6, 4.5))
ax.plot(up, m_up, '-o', ms=3, label='increasing bias (training)')
ax.plot(down, m_down, '-s', ms=3, label='decreasing bias (remediation)')
for sgn in (-1, 1):
    ax.axvline(sgn*h_c, ls='--', color='k', lw=0.8)
ax.set_xlabel(r'bias dose $h$'); ax.set_ylabel('order parameter $m$')
ax.set_title('(D) Hysteresis: misalignment onset vs. remediation\n(fixed a=-0.6; folds at $\\pm h_c$)')
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig('figures/e3_hysteresis.png', dpi=130)
plt.close(fig)
jump_up = up[int(np.argmax(np.diff(m_up)) + 1)]
jump_down = down[int(np.argmax(np.abs(np.diff(m_down))) + 1)]
hyst_width = abs(jump_up - jump_down)
print(f"hysteresis: jump-up h≈{jump_up:+.3f}, jump-down h≈{jump_down:+.3f}, "
      f"width≈{hyst_width:.3f}  (analytic 2·h_c={2*h_c:.3f})")

json.dump({
    "model_symmetric": "a(λ)=1-2λ, b=1, h=0",
    "symmetric_threshold_lambda_star": 0.5,
    "biased_fixed_a": a_fix,
    "analytic_fold_bias_h_c": float(h_c),
    "hysteresis_jump_up_h": float(jump_up),
    "hysteresis_jump_down_h": float(jump_down),
    "hysteresis_width": float(hyst_width),
    "hysteresis_width_analytic_2hc": float(2*h_c),
}, open('results/e3_bifurcation.json', 'w'), indent=2)
print("saved figures/e3_*.png and results/e3_bifurcation.json")
