#!/usr/bin/env python3
"""Independent algebra/index audit of the diamond proof, by the K2,3 worker.

The diamond verifier is not imported. This uses only the standard library and
the sparse integer-polynomial arithmetic from the independently written K2,3
verifier. Inequalities and exhaustion were additionally reviewed in the TeX.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ENGINE = HERE / "verify_k23_obstruction_v15.py"
spec = importlib.util.spec_from_file_location("k23_independent_engine", ENGINE)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
Poly = engine.Poly


def main():
    checks = []

    def identity(name, left, right):
        assert left == right, name
        checks.append(name)

    r, S, rp, Sp, L, h, k, u, v = map(Poly.var, "r S rp Sp L h k u v".split())
    T, Tp = S + L - 1, Sp + L - 1
    # Derived directly from the physical labels in the two canonical matrices.
    p2 = {(3, 0): T, (3, 1): -S, (3, 4): -L,
          (4, 0): -r - 1, (4, 1): r, (4, 3): 0}
    p3 = {(2, 0): -rp - 1, (2, 1): rp, (2, 4): 0,
          (4, 0): Tp, (4, 1): -Sp, (4, 2): -L}
    nodes23 = [1 - p2[(3, j)] - p3[(2, j)] for j in (0, 1, 4)]
    for j, actual, expected in zip((0, 1, 4), nodes23, (rp + 2 - T, 1 + S - rp, 1 + L)):
        identity(f"physical node 23 at puncture {j}", actual, expected)
    identity("nodes on 23 total five", sum(nodes23), 5)
    R0 = -1 + p2[(4, 0)] + p3[(4, 0)]
    R1 = -1 + p2[(4, 1)] + p3[(4, 1)]
    identity("center zero baseline reverse", R0, Tp - r - 2)
    identity("center one baseline reverse", R1, r - Sp - 1)
    identity("central reverse sum", R0 + R1, L - 4)

    Q = Poly.var("Q")
    identity("same positive signed-divisor pair has unchanged reverse sum", 1 + (Q - 1), Q)
    identity("same negative signed-divisor pair has unchanged reverse sum", -1 - (Q - 1), -Q)
    identity("02 switch changes the low reverse by minus b", -1 - (r + 1), -(r + 2))
    identity("03 switch changes the low reverse by b-prime", 1 - (-Tp), Tp + 1)
    identity("13 switch changes the low reverse by minus a-prime", -1 - Sp, -(Sp + 1))
    aa = Poly.var("a")
    identity("12 switch changes the low reverse by a", (-r + aa) - (-r), aa)
    identity("L1 y=1 switch gives center zero reverse Sp", Sp - r - 2 + (r + 2), Sp)
    identity("L1 y=1 switch gives central sum r-1", Sp + (r - Sp - 1), r - 1)

    w, H = map(Poly.var, ("w", "H"))
    identity("L1 y=1 divisor relation", (H + w + 1) - w, H + 1)
    identity("negative x=1 violates the strict upper H bound",
             ((2 + u) * w) * ((2 + u) * w + 1) - 2 * w * w,
             (u * u + 4 * u + 2) * w * w + (u + 2) * w)
    exceptional_pairs = [(hh, ww) for hh in (1, 2) for ww in range(2, hh + 2)
                         if (hh + 1) % ww == 0]
    assert exceptional_pairs == [(1, 2), (2, 3)]
    assert not (Fraction(2**2, 2) < 1 * 2 < 2 * 2**2)
    assert Fraction(3**2, 2) < 2 * 3 < 2 * 3**2
    assert not (Fraction(3**2, 2) < 1 * 2 < 2 * 3**2)

    # L4 switch s'=1: all integer possibilities have S'=2rp,
    # T'=2rp+3, z'=h(rp+1), and the pair residual is exact.
    s4, S4, T4, z4 = 1, 2 * rp, 2 * rp + 3, h * (rp + 1)
    x4, y4 = 2, h * (2 * rp + 3)
    a4, b4 = s4 * S4 + 1, z4 * T4 + 1
    A4, B4 = a4 + x4 - s4, b4 - y4 + z4
    identity("L4 s-prime-one switch pair residual", A4 * B4 - (a4 * b4 - 1), 2 - h * (rp + 1))
    identity("L4 s-prime-one y divisibility", T4 - 2 * (rp + 1), 1)

    # L4 switch z'=1: all integer possibilities have T'=2(rp+1),
    # S'=2rp-1, s'=h*rp.
    s4, S4, T4, z4 = h * rp, 2 * rp - 1, 2 * (rp + 1), 1
    x4, y4 = h * (2 * rp - 1), 2
    a4, b4 = s4 * S4 + 1, z4 * T4 + 1
    A4, B4 = a4 + x4 - s4, b4 - y4 + z4
    identity("L4 z-prime-one switch pair residual", A4 * B4 - (a4 * b4 - 1), h * (rp - 2))
    identity("L4 z-prime-one x divisibility", S4 - 2 * rp, -1)
    identity("L4 r-one switched central sum", Sp + (-Sp - aa), -aa)
    identity("L4 lower bound R>=4", (r + 3 + u) - r + 1, 4 + u)
    identity("L4 saturated node 14 at puncture 2", 1 - (-r) - (r + 1), 0)
    identity("L4 final node 24 at puncture 1", 1 - r - 0, 1 - r)

    final_a, final_b, final_A, final_B = 12 * h + 1, 28 * k + 1, 13 * h + 1, 25 * k + 1
    identity("final (rp,Sp,Tp)=(3,4,7) pair residual",
             final_A * final_B - (final_a * final_b - 1), h + 1 - k * (11 * h + 3))
    identity("final positive h,k contradiction margin",
             (1 + v) * (11 * (1 + u) + 3) - ((1 + u) + 1),
             12 + 10 * u + 14 * v + 11 * u * v)

    source_name = "diamond_obstruction_v15.tex"
    source = next(p for p in (HERE.parent / "diamond" / source_name,
                             HERE.parent / "papers/sections/paper" / source_name, HERE / source_name) if p.is_file())
    result = {
        "version": "v15", "passed": True,
        "reviewer": "K2,3 worker, independent of diamond derivation and verifier",
        "external_peer_review": False,
        "review_type": "Full manual proof/exhaustion/index review plus exact polynomial and proof-derived finite checks",
        "polynomial_identity_count": len(checks), "polynomial_identities": checks,
        "complete_proof_review": [
            "The four D cancellations at the all-low core force equality of the two total low-puncture sums.",
            "The signed-divisor alternatives are exhaustive and preserve the paired sum under taking (q-1)/entry.",
            "The sole remaining low edge forces opposite orientations and equal L in {1,3,4}.",
            "The physical-label node table gives S+L-3<=r-prime<=S+1.",
            "The four switch rows exhaust all signed-divisor alternatives; x=1 is impossible on either branch.",
            "L1 has only the y=1 switch; the unswitched case and both proof-derived (H,S) pairs are excluded.",
            "L3 admits no switch, so the central reverse sum -1 is impossible at Q>1.",
            "L4 switches s-prime=1,z-prime=1 require r-prime=1,2 respectively, contradicting r-prime>=3.",
            "The remaining r=1 switch has opposite nonzero signs and nonzero sum, contradicting the divisor alternatives.",
            "Unswitched L4 uses only actual all-low pair equations and node bounds to force r=1, with no all-low classification assumed.",
            "The final positive-parameter pair equation is impossible for all h,k>=1.",
        ],
        "proof_derived_finite_H_S_cases": exceptional_pairs,
        "denominator_or_entry_cutoff": None,
        "diamond_verifier_imported": False,
        "q3_degenerate_low_core_classification_used": False,
        "limitation": "This audit is not a machine formalization of all inequalities or prior canonical-form results. The written proof remains the primary argument.",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "polynomial_engine": {"file": ENGINE.name, "sha256": hashlib.sha256(ENGINE.read_bytes()).hexdigest()},
    }
    out = HERE / "diamond_independent_audit_v15.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"passed": True, "identities": len(checks), "certificate": str(out)}))


if __name__ == "__main__":
    main()
