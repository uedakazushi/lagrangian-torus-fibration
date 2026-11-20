#!/usr/bin/env python3
"""Exact verification and finite reconstruction for the v21 three-high D cone.

Python standard library only.  No search cutoff is imposed on b in
reconstruct_fixed_data(): the proved Eisenstein-norm bound supplies its finite
range.  Any displayed box still bounds s,t,x,y,z and is NOT a proof of global
nonexistence.

Usage:
  python verify_high_d_reconstruction_v21.py --output result.json
  python verify_high_d_reconstruction_v21.py --fixed 3 4 0 1 1
  python verify_high_d_reconstruction_v21.py --scan 8 4 --output result.json

The --fixed arguments are s,t,x,y,z.  The optional scan uses
1<=s,t<=first bound, 0<=x<s, 0<=y,z<=second bound, x+y+z>=1,
and exhausts every integer b>=2 for each such fixed tuple.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import permutations
from math import isqrt
import hashlib
import json
from pathlib import Path


NAMES = ("s", "t", "x", "y", "z", "b", "S", "T", "U", "v", "w")
NV = len(NAMES)


class Poly:
    """Sparse exact polynomials; coefficients are Python integers."""

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {key: val for key, val in value.items() if val}
        else:
            self.terms = {(0,) * NV: value} if value else {}

    def __add__(self, other):
        other = Poly(other)
        out = defaultdict(int, self.terms)
        for key, value in other.terms.items():
            out[key] += value
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        other = Poly(other)
        out = defaultdict(int)
        for key, value in self.terms.items():
            for key2, value2 in other.terms.items():
                exponent = tuple(a + b for a, b in zip(key, key2))
                out[exponent] += value * value2
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError("nonnegative integer powers only")
        out = Poly(1)
        for _ in range(power):
            out = out * self
        return out


VARIABLES = {
    name: Poly({tuple(int(i == j) for i in range(NV)): 1})
    for j, name in enumerate(NAMES)
}


def det3(matrix):
    out = Poly(0)
    for perm in permutations(range(3)):
        inversions = sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3))
        term = Poly((-1) ** inversions)
        for i in range(3):
            term *= matrix[i][perm[i]]
        out += term
    return out


def coefficient_checks():
    s, t, x, y, z, b, S, T, U, v, w = (VARIABLES[name] for name in NAMES)
    u = s + t - 1
    d = x + y + z
    a = u * d + b - 1 + z
    k = s * d + b - 1 - x
    A, B, C = s * a - t, -s - t * b, s + u * k
    h, j, ell = s - x, t - y, u + z
    lam, mu = u * x + s * z, u * y + t * z
    F = b - 1 + lam
    m = F * F + F + 1
    E, J = mu * h - ell - j, h + ell - lam * j
    R = (b - 1) * j + ell
    W = (a + 1) * h - ell
    ns = m * h + F * E - J
    nt = m * j + E + (F + 1) * J
    nu = m * ell + (F + 1) * E + F * J
    r1 = B * S + A * T - a * b
    r2 = -C * S + (A + 1) * U - k * (a + 1)
    r3 = (C - 1) * T + (B + 1) * U - (b - 1) * (k + 1)
    all_checks = []

    def check(name, lhs, rhs=0):
        lhs, rhs = Poly(lhs), Poly(rhs)
        difference = lhs - rhs
        assert not difference.terms, (name, difference.terms)
        all_checks.append({
            "name": name,
            "lhs_monomials": len(lhs.terms),
            "rhs_monomials": len(rhs.terms),
            "difference_monomials": 0,
            "status": "pass",
        })

    check("alpha_minus_k", a - k, t * d - y)
    check("alpha_from_F", a, F + mu)
    check("k_from_F", k, F + s * y - t * x)
    check("ell_from_h_j_d", ell, h + j + d - 1)
    check("W_forms", W, a * (s - x) + 1 - t - x - z)
    check("R_forms", R, s + t * b - 1 - (b - 1) * y + z)
    check("first_pair_product", (t * S + a) * (s * T - b) - ((1 + s * S) * (1 + t * T) - 1), r1)
    check("second_pair_product", (u * S + a + 1) * (s * U - k) - ((1 + s * S) * (1 + u * U) - 1), r2)
    check("third_pair_product", (u * T - b + 1) * (t * U + k + 1) - ((1 + t * T) * (1 + u * U) - 1), r3)
    check("row2_minus_row1", r2 - r1, (F + 1) * S + T - W + (A + 1) * (U - S - T - d + 1))
    check("row1_minus_row3", r1 - r3, -S + F * T - R - (B + 1) * (U - S - T - d + 1))
    check("numerator_S", ns, F * W - R)
    check("numerator_T", nt, W + (F + 1) * R)
    check("numerator_U", nu, ns + nt + (d - 1) * m)
    check("linear_relation_1", ns - F * nt, -m * R)
    check("linear_relation_2", (F + 1) * ns + nt, m * W)
    check("single_congruence", E + (F + 1) * J, m * E - (F + 1) * (F * E - J))
    ee, jj = (F + 1) * v + w, -v + F * w
    check("Eisenstein_norm", ee * ee + ee * jj + jj * jj, m * (v * v + v * w + w * w))
    check("inverse_E", (F + 1) * (ns - m * h) + (nt - m * j), m * E)
    check("inverse_J", -(ns - m * h) + F * (nt - m * j), m * J)
    check("E_plus_J", E + J, ell * (s * y - t * x) + h - j)
    check("determinant", det3([[B, A, 0], [-C, 0, A + 1], [0, C - 1, B + 1]]), C * (A - B) + B * (A + 1))
    # Clear m in the entire original system, rather than checking only a new equation.
    rr1 = B * ns + A * nt - a * b * m
    rr2 = -C * ns + (A + 1) * nu - k * (a + 1) * m
    rr3 = (C - 1) * nt + (B + 1) * nu - (b - 1) * (k + 1) * m
    check("cleared_row2_equals_row1", rr2, rr1)
    check("cleared_row3_equals_row1", rr3, rr1)
    return all_checks


def data(s, t, x, y, z, b):
    """Algebraic reconstruction, without imposing nonnegative D or positivity."""
    u, d = s + t - 1, x + y + z
    a, k = u * d + b - 1 + z, s * d + b - 1 - x
    h, j, ell = s - x, t - y, u + z
    lam, mu = u * x + s * z, u * y + t * z
    F = b - 1 + lam
    m = F * F + F + 1
    E, J = mu * h - ell - j, h + ell - lam * j
    S = Fraction(h) + Fraction(F * E - J, m)
    T = Fraction(j) + Fraction(E + (F + 1) * J, m)
    U = Fraction(ell) + Fraction((F + 1) * E + F * J, m)
    A, B, C = s * a - t, -s - t * b, s + u * k
    residues = (B * S + A * T - a * b,
                -C * S + (A + 1) * U - k * (a + 1),
                (C - 1) * T + (B + 1) * U - (b - 1) * (k + 1))
    assert residues[0] == residues[1] == residues[2]
    assert S + T + d - 1 == U
    assert (F * E - J) % m == 0 if all(q.denominator == 1 for q in (S, T, U)) else (F * E - J) % m != 0
    norm = E * E + E * J + J * J
    assert Fraction(norm, m) == (S - h) ** 2 + (S - h) * (T - j) + (T - j) ** 2
    return dict(s=s, t=t, x=x, y=y, z=z, b=b, u=u, d=d, alpha=a, k=k,
                h=h, j=j, ell=ell, lam=lam, mu=mu, F=F, m=m, E=E, J=J,
                norm=norm, S=S, T=T, U=U, residue=residues[0])


def exact_model(record):
    """Return every row, pair, D and positive-weight gap; no floating point."""
    s, t, u, a, b, k, S, T, U = (record[name] for name in ("s", "t", "u", "alpha", "b", "k", "S", "T", "U"))
    q = (1 + s * S, 1 + t * T, 1 + u * U, Fraction(1))
    P = ((0, t * S + a, -(u * S + a + 1), -S),
         (s * T - b, 0, -(u * T - b + 1), -T),
         (-(s * U - k), -(t * U + k + 1), 0, U),
         (-s, -t, u, 0))
    row_residues = [sum(row) + q[i] for i, row in enumerate(P)]
    pair_residues = [P[i][j] * P[j][i] - q[i] * q[j] + 1 for i in range(4) for j in range(i + 1, 4)]
    D = [-q[i] - sum(P[j][i] for j in range(4)) for i in range(4)]
    assert D == [record["x"], record["y"], record["z"], -record["d"]]
    H, K = P[0][1], P[1][0]
    magnitudes = (H, K, -P[0][2], -P[1][2], -P[2][0], -P[2][1], S, T, U)
    weights = None
    gaps = None
    if all(value > 0 for value in magnitudes):
        weights = (q[0], H + Fraction(1, 2) / K, u + Fraction(1, 2) / U, Fraction(1))
        gaps = [weights[j] - Fraction(P[i][j], q[i]) * weights[i] for i in range(4) for j in range(4) if i != j]
    return dict(q=q, P=P, D=D, row_residues=row_residues,
                pair_residues=pair_residues, magnitudes=magnitudes, weights=weights, gaps=gaps)


def reconstruct_fixed_data(s, t, x, y, z):
    """Exhaust ALL b>=2 for fixed admissible (s,t,x,y,z), with a proved bound.

    Returns a certificate description and any actual positive integer models.
    The absence of a returned model proves nonexistence only for this fixed
    five-tuple.  The global three-high question is deliberately not asserted.
    """
    assert all(isinstance(value, int) for value in (s, t, x, y, z))
    if s < 1 or t < 1 or min(x, y, z) < 0 or x + y + z < 1:
        raise ValueError("require s,t>=1, x,y,z>=0 and x+y+z>=1")
    probe = data(s, t, x, y, z, 2)
    result = {"fixed": [s, t, x, y, z], "models": [], "b_candidates_examined": 0,
              "norm_divisible_candidates": 0, "integral_scale_candidates": 0,
              "positive_scale_candidates": 0, "status": "complete_for_fixed_data"}
    if probe["h"] <= 0:
        result["exclusion"] = "positive scales imply h=s-x>=1"
        return result
    if probe["norm"] == 0:
        assert (s, t, x, y, z) in ((3, 3, 0, 0, 1), (2, 2, 1, 1, 1))
        result["exclusion"] = "classified zero-norm case; original first row has no integer b>=2 root"
        return result
    Fmax = (isqrt(4 * probe["norm"] - 3) - 1) // 2
    bmax = Fmax - probe["lam"] + 1
    result["norm"] = probe["norm"]
    result["F_max"] = Fmax
    result["b_max"] = bmax
    for b in range(2, bmax + 1):
        result["b_candidates_examined"] += 1
        F = b - 1 + probe["lam"]
        m = F * F + F + 1
        if probe["norm"] % m:
            continue
        result["norm_divisible_candidates"] += 1
        if (F * probe["E"] - probe["J"]) % m:
            continue
        r = data(s, t, x, y, z, b)
        assert all(r[name].denominator == 1 for name in ("S", "T", "U"))
        result["integral_scale_candidates"] += 1
        if min(r["S"], r["T"], r["U"]) <= 0:
            continue
        result["positive_scale_candidates"] += 1
        # The residual is the exact original equation, not a new surrogate.
        if r["residue"] != 0:
            continue
        if r["k"] < b + 1 or r["alpha"] < r["k"]:
            continue
        model = exact_model(r)
        if min(model["magnitudes"]) <= 0:
            continue
        assert all(value == 0 for value in model["row_residues"] + model["pair_residues"])
        assert all(value > 0 for value in model["gaps"])
        assert all(value >= 0 for value in model["D"][:3])
        result["models"].append({"parameters": r, "model": model})
    return result


def regressions():
    output = []
    cases = [
        ("known_integer_mixed_D", (1, 2, -1, 1, 3, 2), (4, 5, 11), True),
        ("known_singular_rank_two_family_n0", (3, 12, -997, -4007, 4671, 4), (136, 291, 93), True),
        ("rational_all_D_zero", (3, 4, 0, 0, 0, 6), (Fraction(34, 31), Fraction(168, 31), Fraction(171, 31)), False),
    ]
    for name, parameters, scales, integral in cases:
        r = data(*parameters)
        assert tuple(r[key] for key in ("S", "T", "U")) == scales
        assert r["residue"] == 0
        assert all(r[key].denominator == 1 for key in ("S", "T", "U")) == integral
        model = exact_model(r)
        assert all(value == 0 for value in model["row_residues"] + model["pair_residues"])
        assert min(model["magnitudes"]) > 0
        assert min(model["gaps"]) > 0
        output.append({"name": name, "status": "pass", "parameters": parameters,
                       "scales": scales, "integral": integral, "D": model["D"],
                       "minimum_basin_gap": min(model["gaps"]),
                       "all_high_D_nonnegative": min(model["D"][:3]) >= 0,
                       "in_new_d_positive_domain": r["d"] >= 1 and min(r["x"], r["y"], r["z"]) >= 0})
    zero_norm_cases = [((3, 3, 0, 0, 1), 3, 3), ((2, 2, 1, 1, 1), 2, -8)]
    for fixed, b, residue in zero_norm_cases:
        r = data(*fixed, b)
        assert r["E"] == r["J"] == 0
        assert r["residue"] == residue
        certificate = reconstruct_fixed_data(*fixed)
        assert certificate["models"] == []
        output.append({"name": "zero_norm_exception_" + "_".join(map(str, fixed)),
                       "status": "pass", "fixed": fixed, "test_b": b,
                       "original_first_row_residue": residue,
                       "all_b_exclusion": certificate["exclusion"]})
    return output


def bounded_fixed_data_scan(stmax, yzmax):
    counts = {"fixed_data": 0, "b_candidates_examined": 0,
              "norm_divisible_candidates": 0, "integral_scale_candidates": 0,
              "positive_scale_candidates": 0, "early_h_exclusions": 0,
              "zero_norm_exclusions": 0, "models": []}
    for s in range(1, stmax + 1):
        for t in range(1, stmax + 1):
            for x in range(s):
                for y in range(yzmax + 1):
                    for z in range(yzmax + 1):
                        if x + y + z == 0:
                            continue
                        item = reconstruct_fixed_data(s, t, x, y, z)
                        counts["fixed_data"] += 1
                        for key in ("b_candidates_examined", "norm_divisible_candidates", "integral_scale_candidates", "positive_scale_candidates"):
                            counts[key] += item[key]
                        if "classified zero-norm" in item.get("exclusion", ""):
                            counts["zero_norm_exclusions"] += 1
                        counts["models"].extend(item["models"])
    counts["bounds"] = {"s_and_t": [1, stmax], "x": "0<=x<s", "y_and_z": [0, yzmax],
                        "d": "x+y+z>=1", "b": "all integers b>=2, exhausted by the proved norm bound"}
    counts["scope"] = "Exact finite-family verification only. No global nonexistence conclusion."
    return counts


def encode(value):
    if isinstance(value, Fraction):
        return value.numerator if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    raise TypeError(type(value).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("high_d_reconstruction_verification_v21.json"))
    parser.add_argument("--fixed", nargs=5, type=int, metavar=("s", "t", "x", "y", "z"))
    parser.add_argument("--scan", nargs=2, type=int, metavar=("ST_MAX", "YZ_MAX"))
    args = parser.parse_args()
    checks = coefficient_checks()
    proof_name = "high_d_eisenstein_reconstruction_v21.tex"
    proof_path = next(path for path in (
        Path(__file__).with_name(proof_name),
        Path(__file__).parent.parent / "paper" / proof_name,
    ) if path.is_file())
    result = {
        "status": "PASS",
        "version": 21,
        "theorem": "three-high nonnegative-D Eisenstein reconstruction and finite b bound",
        "arithmetic": "integer and Fraction only; sparse exact polynomial coefficient checks",
        "coefficient_check_count": len(checks),
        "coefficient_checks": checks,
        "regressions": regressions(),
        "global_nonexistence_claimed": False,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_file": proof_name,
        "proof_sha256": hashlib.sha256(proof_path.read_bytes()).hexdigest(),
    }
    if args.fixed:
        result["fixed_reconstruction"] = reconstruct_fixed_data(*args.fixed)
    if args.scan:
        result["finite_family_scan"] = bounded_fixed_data_scan(*args.scan)
    rendered = json.dumps(result, default=encode, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
        print(json.dumps({"status": "PASS", "output": str(args.output), "coefficient_checks": len(checks),
                          "regressions": len(result["regressions"]),
                          "finite_family": {key: val for key, val in result.get("finite_family_scan", {}).items() if key != "models"},
                          "found_models": len(result.get("finite_family_scan", {}).get("models", []))}, ensure_ascii=False))
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
