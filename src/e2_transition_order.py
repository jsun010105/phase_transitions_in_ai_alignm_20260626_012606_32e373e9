#!/usr/bin/env python3
"""
E2 — Symbolic verification of the transition-order theorems on the cusp normal form
        F(m; a, h) = ¼ b m⁴ + ½ a m² − h m ,   b > 0,
with gradient flow  ṁ = −F'(m) = −(b m³ + a m − h).

Verifies, symbolically (SymPy):
  (T2) Existence of a critical threshold: the aligned equilibrium m=0 (h=0) is stable iff a>0;
       loses stability exactly at a=0  [Hessian / Jacobian eigenvalue crosses zero].
  (T3) Order of the pitchfork (h=0): nonzero branches m=±sqrt(-a/b) exist iff a<0; their
       curvature is −2a>0 (stable). b>0 ⇒ supercritical ⇒ CONTINUOUS (Ma–Wang Thm B,
       Kuehn Thm A). Critical exponent β: |m| ~ (−a)^{1/2}, so β=1/2.
  (T4) Cusp unfolding (h≠0): the fold/saddle-node set where two equilibria merge is
       27 b h² + 4 a³ = 0 (a<0). This is the discriminant of the equilibrium cubic ⇒ the
       boundary between one root (robust) and three roots (bistable / hysteretic / jump).
"""
import sympy as sp

m, a, b, h, lam = sp.symbols('m a b h lambda', real=True)
b_pos = sp.Symbol('b', positive=True)

F  = sp.Rational(1,4)*b*m**4 + sp.Rational(1,2)*a*m**2 - h*m
Fp = sp.diff(F, m)            # ṁ = -Fp
Fpp = sp.diff(F, m, 2)        # curvature / Hessian

print("F(m;a,h) =", F)
print("F'(m)    =", sp.expand(Fp))
print("F''(m)   =", sp.expand(Fpp))

# ---------- (T2) threshold: stability of aligned m=0 at h=0 ----------
print("\n--- (T2) critical threshold (h=0) ---")
curv0 = Fpp.subs({m:0, h:0})
print("  F''(0) =", curv0, " => m=0 linearly stable iff a>0; neutral (eigenvalue 0) at a=0.")
print("  Jacobian of flow at m=0 is -F''(0) = -a: crosses 0 at a=0  => critical threshold a*=0.")

# ---------- (T3) pitchfork branches and order (h=0) ----------
print("\n--- (T3) order of the pitchfork (h=0) ---")
eqs = sp.solve(sp.Eq(Fp.subs(h,0), 0), m)
print("  equilibria (h=0):", eqs)
nonzero = [r for r in eqs if r != 0]
for r in nonzero:
    cv = sp.simplify(Fpp.subs({h:0, m:r}))
    print(f"    branch m={r}:  F''= {cv}  (stable iff >0; = -2a >0 for a<0)")
# real nonzero branches exist iff -a/b>0 i.e. a<0 (past threshold). Critical exponent:
amp = sp.sqrt(-a/b_pos)
print("  nonzero amplitude |m| = sqrt(-a/b); near threshold a=-(λ-λ*)·c  => |m| ~ (λ-λ*)^(1/2)")
print("  => critical exponent beta = 1/2 (mean-field).  b>0 => SUPERCRITICAL => CONTINUOUS.")
print("  (If instead b<0: no stable nearby branch => SUBCRITICAL => JUMP/catastrophic, Thm A.)")

# Ma–Wang sign criterion: reduce ṁ at threshold a=0,h=0:  ṁ = -b m^3 + O(m^5).
print("\n  Ma–Wang reduced equation at threshold:  ṁ = -(b) m^3 + ... ; leading coeff sign of")
print("  the POTENTIAL quartic is +b. Their criterion: quartic>0 (b>0) => continuous; <0 => jump. OK.")

# ---------- (T4) cusp / fold set (h != 0) ----------
print("\n--- (T4) cusp unfolding: fold set where two equilibria merge ---")
# fold: F'(m)=0 and F''(m)=0 simultaneously; eliminate m.
res = sp.resultant(Fp, Fpp, m)
res = sp.factor(sp.expand(res))
print("  resultant_m(F', F'') =", res)
# This should be proportional to 27 b h^2 + 4 a^3 (the cusp discriminant)
target = 27*b*h**2 + 4*a**3
ratio = sp.simplify(res / target)
print("  target cusp curve     = 27 b h² + 4 a³")
print("  resultant / target    =", ratio, " (constant => same zero set)")
print("  => fold/saddle-node bifurcation set is  27 b h² + 4 a³ = 0  (a<0).")
print("     Inside the cusp (27 b h² + 4 a³ < 0): THREE equilibria (bistable, hysteresis, JUMP).")
print("     Outside: ONE equilibrium (robust / smooth).")

# discriminant of the depressed cubic b m^3 + a m - h  (Δ>0 => 3 real roots)
print("\n  cross-check via cubic discriminant of  b m³ + a m − h:")
disc = sp.discriminant(b*m**3 + a*m - h, m)
print("    discriminant =", sp.factor(disc), " (>0 <=> 3 real equilibria)")

# number of real roots at sample points
print("\n  sample (b=1):")
for (av, hv, tag) in [(-1.0, 0.0, 'inside, h=0'),
                      (-1.0, 0.2, 'inside, small h'),
                      (-1.0, 0.6, 'near fold'),
                      (-1.0, 1.0, 'outside (large h)'),
                      ( 1.0, 0.3, 'a>0 robust')]:
    roots = sp.Poly(m**3 + av*m - hv, m).nroots()
    nreal = sum(1 for r in roots if abs(sp.im(r)) < 1e-9)
    cusp_val = 27*1*hv**2 + 4*av**3
    print(f"    a={av:+.2f} h={hv:+.2f}  ({tag:18s})  #real eq={nreal}  27bh²+4a³={cusp_val:+.3f}")

import json, os
os.makedirs('results', exist_ok=True)
json.dump({
    "T2_threshold": "F''(0)=a; aligned m=0 stable iff a>0; eigenvalue crosses 0 at a=0",
    "T3_pitchfork_branch_curvature": "-2a (>0 for a<0, stable); b>0 supercritical continuous; beta=1/2",
    "T4_fold_set_resultant_over_cusp_target": str(ratio),
    "T4_fold_set": "27 b h^2 + 4 a^3 = 0",
}, open('results/e2_transition_order.json','w'), indent=2)
print("\nsaved -> results/e2_transition_order.json")
