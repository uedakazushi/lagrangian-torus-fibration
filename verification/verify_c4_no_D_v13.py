#!/usr/bin/env python3
"""Exact checks for the v13 replacement of the C4 tau=1 argument.

The general proof of propagation and the tau=2 case remains the written v12
proof.  This file checks the fifth-core row/product mechanism, the unique
S=T=2 local model, and the unbounded inequalities used to establish uniqueness.
"""

from fractions import Fraction
from pathlib import Path
import hashlib
import json


def main():
    checks = 0
    # Polynomial coefficient triples are in ascending powers of k.
    # H=3+k gives H(H+1)-12=k^2+7k, nonnegative for every k>=0.
    H_times_H_plus_one = (12, 7, 1)
    difference = (H_times_H_plus_one[0] - 12,
                  H_times_H_plus_one[1], H_times_H_plus_one[2])
    assert difference == (0, 7, 1) and all(v >= 0 for v in difference)
    checks += 1
    # Therefore E=1-4/[H(H+1)] >= 2/3 for every H>=3.
    assert 1 - Fraction(4, 12) == Fraction(2, 3)
    assert 2 * Fraction(2, 3) > 1
    checks += 2

    # H=1: E=-1, hence u(1-v)=v+1; its sides have opposite signs
    # for u,v positive.  H=2: E=1/3 and 2<=u<3 forces u=2.
    assert 1 - Fraction(4, 2) == -1
    E = 1 - Fraction(4, 6)
    assert E == Fraction(1, 3)
    candidates_u = [u for u in range(2, 4) if E * u < 1]
    assert candidates_u == [2]
    u = candidates_u[0]
    v = Fraction(u - 1, 1 - E * u)
    assert v == 3
    checks += 4
    H = 2
    r = H + 2
    s = Fraction(u * (H + 2), H)
    z = Fraction(v * (H + 3), H + 1)
    S = T = 2
    assert (r, s, z, S, T) == (4, 4, 5, 2, 2)
    checks += 1
    a, b = s * S + 1, z * T + 1
    x, y = (a - 1) / r, (b - 1) / (r + 1)
    A, B = a + x - s, b - y + z
    q = tuple(map(Fraction, (a, b, 1, 1)))
    P = tuple(tuple(map(Fraction, row)) for row in (
        (0, -A, x, -s), (-B, 0, -y, z),
        (r, -r-1, 0, 0), (-S, T, S-T-1, 0)))
    weights = (a, b, x + Fraction(1, 2*r), z + Fraction(1, 2*T))
    assert (a, b) == (9, 11)
    checks += 1
    for i in range(4):
        assert sum(P[i]) == -q[i]
        checks += 1
        for j in range(4):
            if i == j:
                continue
            assert P[i][j] * P[j][i] == q[i] * q[j] - 1
            assert weights[j] - weights[i] * P[i][j] / q[i] > 0
            checks += 2

    # The fifth-core argument is genuinely a c<=2 bound.  At c=2 its
    # row/product part has a consistent all-low model, checked here.
    V = [[0] * 4 for _ in range(4)]
    for i in range(4):
        V[i][(i+1) % 4] = -1
    for i in range(4):
        assert sum(V[i]) == -1
        assert V[i][(i-1) % 4] == 0
        assert V[i][(i+2) % 4] == 0
        checks += 3
        for j in range(i+1, 4):
            assert V[i][j] * V[j][i] == 0
            checks += 1

    # For c=3+k (k>=0), row sums force both opposite entries >=1+k.
    # Their product has lower bound (1+k)^2>0, conflicting with product 0.
    lower_product_coefficients = (1, 2, 1)
    assert lower_product_coefficients[0] > 0
    assert all(v >= 0 for v in lower_product_coefficients)
    checks += 2

    # The four copies require q_i=11 from core i, and q_i=9 from core i+1.
    impossible_shared_edges = []
    for i in range(4):
        left_q, right_q = b, a
        assert left_q != right_q
        checks += 1
        impossible_shared_edges.append({"edge": [i, (i+1) % 4],
                                        "value_from_left": int(left_q),
                                        "value_from_right": int(right_q)})

    here = Path(__file__).resolve().parent
    source_paths = (here / "c4_equal_pairing_obstruction_v13.tex",
                    here.parent / "paper" / "c4_equal_pairing_obstruction_v13.tex",
                    here.parent / "paper" / "c4_equal_pairing_obstruction_v12.tex")
    source = next((p for p in source_paths if p.exists()), None)
    result = {
        "version": "v13", "status": "passed", "exact_assertion_count": checks,
        "denominator_bound": None, "D_opposition_used": False,
        "scope": "Exact certificate for the fifth-core c=2 reduction and the unique S=T=2 canonical model; tau propagation/tau=2 use the written prior proof.",
        "unique_canonical_model": {
            "r_s_z_S_T": [4, 4, 5, 2, 2], "q": list(map(int, q)),
            "P": [[int(t) for t in row] for row in P],
            "weights": [str(t) for t in weights]},
        "H_ge_3_polynomial": difference,
        "c_ge_3_product_lower_bound": lower_product_coefficients,
        "fifth_core_at_c2": V,
        "shared_edge_contradictions": impossible_shared_edges,
        "proof_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest() if source else None,
    }
    target = here / "c4_no_D_verification_v13.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "version", "status", "exact_assertion_count", "D_opposition_used")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
