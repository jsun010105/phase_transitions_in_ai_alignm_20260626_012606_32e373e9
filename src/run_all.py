#!/usr/bin/env python3
"""Reproduce every computational result. Usage:  python src/run_all.py
Runs E1–E5 in order; each writes results/*.json and figures/*.png. Deterministic (fixed seeds)
except for negligible Euler–Maruyama sampling scatter, which is also seeded."""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
for script in ["e1_microscopic_derivation.py", "e2_transition_order.py",
               "e3_bifurcation_numerics.py", "e4_early_warning_sde.py",
               "e5_calibration_prediction.py"]:
    print("\n" + "#"*72 + f"\n# {script}\n" + "#"*72)
    r = subprocess.run([sys.executable, os.path.join(HERE, script)])
    if r.returncode != 0:
        sys.exit(f"FAILED: {script}")
print("\nAll experiments completed. See results/ and figures/.")
