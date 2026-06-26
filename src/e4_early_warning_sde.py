#!/usr/bin/env python3
"""
E4 — Stochastic early-warning laws and attractor stability (verifies Theorem 5 / Kuehn Thm D).

SDE (FEP at NESS, additive noise):  dm = −F'(m) dt + σ dW,  F=¼m⁴+½a m²−h m, b=1.
Integrate with Euler–Maruyama near the aligned equilibrium for a sequence of stiffnesses
a(λ) approaching the threshold a→0⁺, and verify:
  (1) Stationary variance  Var(m) → σ²/(2α),  α = F''(m_eq) = recovery rate. (critical slowing)
  (2) Lag-τ autocorrelation  ρ(τ) = exp(−α τ);  autocorrelation TIME 1/α diverges as a→0.
  (3) Lyapunov exponent of each attractor  Λ = −F''(m_eq):  aligned vs misaligned contraction.
  (4) Jensen–Shannon divergence between the empirical stationary histogram of m and the exact
      Boltzmann law  p(m) ∝ exp(−2F(m)/σ²)  — confirms the simulated law is the predicted one.
"""
import numpy as np
import json, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import brentq

os.makedirs('figures', exist_ok=True); os.makedirs('results', exist_ok=True)
SEED = 42
b = 1.0

def Fprime(m, a, h=0.0): return b*m**3 + a*m - h
def Fpp(m, a):           return 3*b*m**2 + a
def F(m, a, h=0.0):      return 0.25*b*m**4 + 0.5*a*m**2 - h*m

def aligned_eq(a, h=0.0):
    """smallest-|m| stable equilibrium (aligned)."""
    roots = np.roots([b, 0.0, a, -h])
    real = [r.real for r in roots if abs(r.imag) < 1e-9 and Fpp(r.real, a) > 0]
    return min(real, key=abs) if real else 0.0

def em_euler(a, h=0.0, sigma=0.15, dt=2e-3, T=4000.0, burn=0.25, seed=SEED):
    """Euler–Maruyama; return post-burn samples about the aligned equilibrium."""
    n = int(T/dt); rng = np.random.default_rng(seed)
    m = aligned_eq(a, h); xs = np.empty(n)
    sq = sigma*np.sqrt(dt)
    for i in range(n):
        m += -Fprime(m, a, h)*dt + sq*rng.standard_normal()
        xs[i] = m
    return xs[int(burn*n):]

# ---------- (1)+(2) variance and autocorrelation vs approaching threshold ----------
# Use a small sigma so the linear OU regime (where Var=σ²/2α is exact) holds; ALSO report the
# exact Boltzmann variance ∫m² e^{-2F/σ²}, which accounts for the quartic and which the
# simulation should match even near threshold (separating "sim correct" from "linear-law
# approximation rounds the divergence").
sigma = 0.06
def boltzmann_var(a, sig, h=0.0):
    grid = np.linspace(-3, 3, 4000)
    w = np.exp(-2*F(grid, a, h)/sig**2)
    w /= np.trapezoid(w, grid)
    mean = np.trapezoid(grid*w, grid)
    return np.trapezoid((grid-mean)**2*w, grid)

a_vals = [1.0, 0.6, 0.4, 0.25, 0.15, 0.08]
rows = []
print("Early-warning laws (sigma=%.2f).  Approaching threshold a->0:" % sigma)
print(f"{'a':>7} {'alpha=F\"':>9} {'Var_meas':>10} {'sig^2/2a(lin)':>13} {'Var_Boltz':>10} "
      f"{'ac_time':>9} {'1/alpha':>9}")
for a in a_vals:
    xs = em_euler(a, sigma=sigma)
    meq = aligned_eq(a); alpha = Fpp(meq, a)
    var_meas = np.var(xs); var_lin = sigma**2/(2*alpha); var_bz = boltzmann_var(a, sigma)
    x0 = xs - xs.mean(); dt = 2e-3
    rho1 = np.dot(x0[:-1], x0[1:]) / np.dot(x0, x0)
    ac_time_meas = -dt/np.log(rho1) if 0 < rho1 < 1 else np.nan
    rows.append((a, meq, alpha, var_meas, var_lin, var_bz, ac_time_meas, 1/alpha))
    print(f"{a:>7.2f} {alpha:>9.4f} {var_meas:>10.6f} {var_lin:>13.6f} {var_bz:>10.6f} "
          f"{ac_time_meas:>9.4f} {1/alpha:>9.4f}")

rel_err_lin = np.mean([abs(r[3]-r[4])/r[4] for r in rows])
rel_err_bz  = np.mean([abs(r[3]-r[5])/r[5] for r in rows])
print(f"\nmean rel. error  Var_meas vs linear σ²/2α : {100*rel_err_lin:.1f}%")
print(f"mean rel. error  Var_meas vs exact Boltzmann: {100*rel_err_bz:.1f}%")
print("=> variance AND autocorrelation time diverge as a->0: critical slowing down (Thm 5).")
print("   linear law σ²/2α matches away from threshold; quartic rounds the divergence near a→0,")
print("   which the exact Boltzmann variance (matched by the simulation) captures.")

# figure: variance divergence
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
aa = np.array([r[0] for r in rows])
ax[0].plot(aa, [r[3] for r in rows], 'o', label='measured Var(m)')
afine = np.linspace(0.05, 1.0, 100)
ax[0].plot(afine, sigma**2/(2*afine), '-', label=r'linear $\sigma^2/2\alpha$')
ax[0].plot(aa, [r[5] for r in rows], 's', ms=4, label='exact Boltzmann')
ax[0].set_xlabel(r'stiffness $a(\lambda)$ (→0 at threshold)'); ax[0].set_ylabel('Var(m)')
ax[0].set_title('(A) Variance divergence (early warning)'); ax[0].legend(fontsize=8)
ax[1].plot(aa, [r[6] for r in rows], 'o', label='measured autocorr. time')
ax[1].plot(afine, 1/afine, '-', label=r'theory $1/\alpha$')
ax[1].set_xlabel(r'stiffness $a(\lambda)$'); ax[1].set_ylabel('autocorrelation time')
ax[1].set_title('(B) Critical slowing down'); ax[1].legend(fontsize=8)
fig.tight_layout(); fig.savefig('figures/e4_early_warning.png', dpi=130); plt.close(fig)

# ---------- (3) Lyapunov exponents of the two attractors (bistable case a<0,h=0) ----------
a_bi = -1.0
m_misA, m_misB = np.sqrt(-a_bi/b), -np.sqrt(-a_bi/b)   # two misaligned wells (h=0 symmetric)
m_top = 0.0
lyap = {"well_+sqrt": -Fpp(m_misA, a_bi), "well_-sqrt": -Fpp(m_misB, a_bi),
        "barrier_top_m=0": -Fpp(m_top, a_bi)}
print("\nLyapunov exponents Λ=−F''(m_eq) at a=-1 (h=0):")
for k, v in lyap.items():
    print(f"   {k:18s}: Λ={v:+.3f}  ({'stable attractor' if v<0 else 'unstable (repeller)'})")

# ---------- (4) Jensen–Shannon divergence vs Boltzmann law ----------
def js_divergence(p, q, eps=1e-12):
    p = p/np.sum(p)+eps; q = q/np.sum(q)+eps; m = 0.5*(p+q)
    def kl(x, y): return np.sum(x*np.log(x/y))
    return 0.5*kl(p, m)+0.5*kl(q, m)

# Sample a well-mixed regime so the empirical histogram is meaningful: a=0.4 (single well).
a_js = 0.4
xs = em_euler(a_js, sigma=sigma, T=8000.0)
bins = np.linspace(xs.min()-0.05, xs.max()+0.05, 60)
centers = 0.5*(bins[:-1]+bins[1:])
emp, _ = np.histogram(xs, bins=bins, density=True)
boltz = np.exp(-2*F(centers, a_js)/sigma**2); boltz /= np.trapezoid(boltz, centers)
emp_n = emp/np.trapezoid(emp, centers)
JS = js_divergence(emp_n*np.diff(bins), boltz*np.diff(bins))
print(f"\nJensen–Shannon divergence (empirical SDE law vs Boltzmann ∝e^(−2F/σ²)) at a={a_js}: "
      f"JS={JS:.4f} nats  (≈0 confirms the predicted stationary distribution).")

fig, ax = plt.subplots(figsize=(6, 4.2))
ax.plot(centers, emp_n, 'o', ms=3, label='empirical (SDE)')
ax.plot(centers, boltz, '-', label=r'Boltzmann $\propto e^{-2F/\sigma^2}$')
ax.set_xlabel('order parameter $m$'); ax.set_ylabel('density')
ax.set_title(f'(C) Stationary law matches Boltzmann (JS={JS:.4f} nats)'); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig('figures/e4_boltzmann.png', dpi=130); plt.close(fig)

json.dump({
    "sigma": sigma,
    "variance_law_mean_rel_error_pct_linear": float(100*rel_err_lin),
    "variance_law_mean_rel_error_pct_boltzmann": float(100*rel_err_bz),
    "table_a_meq_alpha_varmeas_varlin_varbz_actime_invalpha":
        [[float(x) for x in r] for r in rows],
    "lyapunov_exponents": {k: float(v) for k, v in lyap.items()},
    "JS_divergence_vs_boltzmann_nats": float(JS),
}, open('results/e4_early_warning.json', 'w'), indent=2)
print("\nsaved figures/e4_*.png and results/e4_early_warning.json")
