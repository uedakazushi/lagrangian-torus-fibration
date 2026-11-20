#!/usr/bin/env python3
"""Exact v22 verification: all nonnegative high-D models for a fixed low row.

Python standard library only. The low row is (-s,-t,s+t-1,0). After fixing
s,t the proved F bound exhausts x,z,b, and the nonzero residual quadratic
exhausts every y>=0 without a search cutoff on any high D or denominator.

Examples:
  python verify_high_d_low_row_finiteness_v22.py --output result.json
  python verify_high_d_low_row_finiteness_v22.py --fixed 3 3 --output fixed.json
  python verify_high_d_low_row_finiteness_v22.py --scan 12 --output result.json

A finite --scan bound restricts s,t only. No global nonexistence claim follows.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path


NAMES = ("s", "t", "x", "y", "z", "b")
NV = len(NAMES)


class Poly:
    """Sparse exact multivariate polynomials with integer coefficients."""

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {key: val for key, val in value.items() if val}
        else:
            self.terms = {(0,) * NV: value} if value else {}

    def __add__(self, other):
        out = defaultdict(int, self.terms)
        for key, val in Poly(other).terms.items():
            out[key] += val
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -val for key, val in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        out = defaultdict(int)
        for key, val in self.terms.items():
            for key2, val2 in Poly(other).terms.items():
                out[tuple(a + b for a, b in zip(key, key2))] += val * val2
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError("nonnegative integer powers only")
        result = Poly(1)
        for _ in range(power):
            result *= self
        return result


VARS = {
    name: Poly({tuple(int(i == j) for i in range(NV)): 1})
    for j, name in enumerate(NAMES)
}


def coefficient_checks():
    """Compare coefficients, never infer identities from finitely many values."""
    s, t, x, y, z, b = (VARS[name] for name in NAMES)
    u, h, B = s + t - 1, s - x, b - 1
    d, lam, mu = x + y + z, u * x + s * z, u * y + t * z
    F = B + lam
    m = F * F + F + 1
    alpha, k = u * d + b - 1 + z, s * d + b - 1 - x
    j, ell = t - y, u + z
    E, J = mu * h - ell - j, h + ell - lam * j
    E0, J0 = t * h * z - u - z - t, h + u + z - lam * t
    a = u * h - B * (F + 1)
    n0 = (F + 1) * (B * t + h) + F * (u + z) + h * t * z
    ns0, c = m * h + F * E0 - J0, F * u * h + B
    ns = m * h + F * E - J
    nt = m * j + E + (F + 1) * J
    nu = m * ell + (F + 1) * E + F * J
    alpha0, H = F + t * z, s + t * b
    A0 = s * alpha0 - t
    L = (2 * s - 1) * F + t * b + 2 * s * t * z + s - 2 * t
    C = F * (b * (t - 1) + s) + b * b * t + b * s - b
    C0 = -H * ns0 + A0 * n0 - b * alpha0 * m
    C1 = -H * c + A0 * a + s * u * n0 - b * u * m
    rr1 = -H * ns + (s * alpha - t) * nt - alpha * b * m
    scalarC = s + u * k
    rr2 = -scalarC * ns + (s * alpha - t + 1) * nu - k * (alpha + 1) * m
    rr3 = (scalarC - 1) * nt + (-H + 1) * nu - (b - 1) * (k + 1) * m
    M = s * t + (2 * u + 1) * h - 2
    Q0 = (-B * F * F + (B * (s * t - 2) + (2 * u + 1) * h - 1) * F
          + B * (t * x - 1) + h * (s - u * t * x) - 1)
    Q1 = (-B * F * F + (B * (s * t - 1) + (2 * u + 1) * h - 1) * F
          - B * (B + 1) + s * h - 1)
    Q2 = -F * F + M * F + s * h - 3
    checks = []

    def check(name, lhs, rhs=0):
        lhs, rhs = Poly(lhs), Poly(rhs)
        difference = lhs - rhs
        assert not difference.terms, (name, difference.terms)
        checks.append(dict(name=name, lhs_monomials=len(lhs.terms),
                           rhs_monomials=len(rhs.terms), difference_monomials=0,
                           status="pass"))

    check("E_affine_y", E, E0 + (u * h + 1) * y)
    check("J_affine_y", J, J0 + lam * y)
    check("S_numerator_affine_y", ns, ns0 + c * y)
    check("T_numerator_affine_y", nt, n0 + a * y)
    check("U_from_S_T_d", nu, ns + nt + (d - 1) * m)
    check("alpha_affine_y", alpha, alpha0 + u * y)
    check("S_slope_at_degeneracy", c, B * m + F * a)
    check("K_numerator", s * nt - b * m, Q0 + s * a * y)
    check("first_bound_gap_nonnegative", Q1 - Q0,
          B * ((s - 1) * x + s * z) + u * h * t * x)
    check("second_bound_gap_nonnegative", Q2 - Q1,
          (B - 1) * (F * (F - s * t + 1) + B + 2))
    check("threshold_a_upper_bound", u * h - (M + 2), -s * t - (u + 1) * h)
    check("threshold_Q2_upper_bound", -(M + 1) + s * h - 3,
          -s * t - (s + 2 * t - 1) * h - 2)
    check("linear_coefficient_nonzero_at_degeneracy", C1, a * L - C)
    check("L_positive_expression", L, (2 * s - 1) * F + t * (b - 2) + 2 * s * t * z + s)
    check("C_positive_expression", C, F * (b * (t - 1) + s) + b * (b * t + s - 1))
    check("residual_quadratic", rr1, s * u * a * y * y + (a * L - C) * y + C0)
    check("original_pair_residual_2_equals_1", rr2, rr1)
    check("original_pair_residual_3_equals_1", rr3, rr1)
    check("single_congruence", E + (F + 1) * J, m * E - (F + 1) * (F * E - J))
    check("degenerate_hypersurface", a, u * (s - b * x) - B * (b + s * z))
    # Independent specialization of the symmetric sector s=t and x=y.
    us, hs, ds = 2 * s - 1, s - x, 2 * x + z
    lams = us * x + s * z
    Fs = b - 1 + lams
    ms = Fs * Fs + Fs + 1
    Es, Js = lams * hs - (us + z) - hs, hs + us + z - lams * hs
    check("symmetric_E_plus_J", Es + Js, 0)
    check("symmetric_S_shift", Fs * Es - Js, (Fs + 1) * Es)
    check("symmetric_T_shift", Es + (Fs + 1) * Js, -Fs * Es)
    check("symmetric_positive_F_gap", Fs - hs - 1, (b - 2) + s * (ds - 1))
    return checks


def quadratic_data(s, t, x, z, b):
    """All integer coefficients for the residual in y at fixed s,t,x,z,b."""
    u, h, B = s + t - 1, s - x, b - 1
    lam = u * x + s * z
    F = B + lam
    m = F * F + F + 1
    a = u * h - B * (F + 1)
    n0 = (F + 1) * (B * t + h) + F * (u + z) + h * t * z
    E0, J0 = t * h * z - u - z - t, h + u + z - lam * t
    ns0, c = m * h + F * E0 - J0, F * u * h + B
    alpha0, H = F + t * z, s + t * b
    A0 = s * alpha0 - t
    L = (2 * s - 1) * F + t * b + 2 * s * t * z + s - 2 * t
    C = F * (b * (t - 1) + s) + b * b * t + b * s - b
    C0 = -H * ns0 + A0 * n0 - b * alpha0 * m
    return dict(u=u, h=h, B=B, lam=lam, F=F, m=m, a=a, n0=n0,
                ns0=ns0, c=c, alpha0=alpha0, L=L, C=C,
                coefficients=(s * u * a, a * L - C, C0))


def nonnegative_integer_roots(A, B, C):
    """Every nonnegative integer root of a nonzero degree <=2 polynomial."""
    if A == 0:
        if B == 0:
            if C == 0:
                raise AssertionError("identically zero residual is forbidden")
            return ()
        numerator = -C
        return (numerator // B,) if numerator % B == 0 and numerator // B >= 0 else ()
    disc = B * B - 4 * A * C
    if disc < 0:
        return ()
    root = isqrt(disc)
    if root * root != disc:
        return ()
    den = 2 * A
    return tuple(sorted({num // den for num in (-B - root, -B + root)
                         if num % den == 0 and num // den >= 0}))


def reconstruct(s, t, x, y, z, b):
    """The earlier reconstruction, evaluated independently with Fractions."""
    u, d, h, j, ell = s + t - 1, x + y + z, s - x, t - y, s + t - 1 + z
    alpha, k = u * d + b - 1 + z, s * d + b - 1 - x
    lam, mu = u * x + s * z, u * y + t * z
    F = b - 1 + lam
    m = F * F + F + 1
    E, J = mu * h - ell - j, h + ell - lam * j
    S = Fraction(h) + Fraction(F * E - J, m)
    T = Fraction(j) + Fraction(E + (F + 1) * J, m)
    U = Fraction(ell) + Fraction((F + 1) * E + F * J, m)
    r = (-s - t * b) * S + (s * alpha - t) * T - alpha * b
    return dict(s=s, t=t, x=x, y=y, z=z, b=b, u=u, d=d, alpha=alpha,
                k=k, F=F, m=m, E=E, J=J, S=S, T=T, U=U, residue=r)


def audit_model(rec):
    s, t, u, alpha, b, k, S, T, U = (rec[n] for n in
        ("s", "t", "u", "alpha", "b", "k", "S", "T", "U"))
    q = (1 + s * S, 1 + t * T, 1 + u * U, Fraction(1))
    P = ((0, t * S + alpha, -(u * S + alpha + 1), -S),
         (s * T - b, 0, -(u * T - b + 1), -T),
         (-(s * U - k), -(t * U + k + 1), 0, U),
         (-s, -t, u, 0))
    rows = [sum(P[i]) + q[i] for i in range(4)]
    pairs = [P[i][j] * P[j][i] - q[i] * q[j] + 1
             for i in range(4) for j in range(i + 1, 4)]
    D = [-q[i] - sum(P[j][i] for j in range(4)) for i in range(4)]
    assert D == [rec["x"], rec["y"], rec["z"], -rec["d"]]
    signs = (t * S + alpha, s * T - b, u * S + alpha + 1,
             u * T - b + 1, s * U - k, t * U + k + 1)
    gaps = None
    weights = None
    if min(S, T, U, *signs) > 0:
        H, K = signs[:2]
        weights = (q[0], H + Fraction(1, 2) / K,
                   u + Fraction(1, 2) / U, Fraction(1))
        gaps = [weights[j] - Fraction(P[i][j], q[i]) * weights[i]
                for i in range(4) for j in range(4) if i != j]
    return dict(q=q, P=P, D=D, row_residues=rows, pair_residues=pairs,
                sign_factors=signs, weights=weights, gaps=gaps)


def reconstruct_fixed_low_row(s, t):
    """A complete finite decision for this low row; no bound on high D."""
    if not isinstance(s, int) or not isinstance(t, int) or min(s, t) < 1:
        raise ValueError("s,t must be positive integers")
    u = s + t - 1
    counts = dict(five_tuples=0, quadratic_tuples=0, linear_tuples=0,
                  nonnegative_integer_residual_roots=0, positive_d=0,
                  nonsingular_sector=0, congruence_pass=0,
                  positive_scales=0, positive_signs=0, exact_models=0)
    models, candidate_examples = [], []
    maxima = dict(F=0, b=0, z=0, integer_root_y=0)
    for x in range(s):
        h = s - x
        M = s * t + (2 * u + 1) * h - 2
        capacity = M - u * x
        if capacity < 1:
            continue
        for z in range((capacity - 1) // s + 1):
            for b in range(2, capacity - s * z + 2):
                data = quadratic_data(s, t, x, z, b)
                counts["five_tuples"] += 1
                counts["linear_tuples" if data["a"] == 0 else "quadratic_tuples"] += 1
                assert data["F"] <= M and data["L"] > 0 and data["C"] > 0
                if data["a"] == 0:
                    assert data["coefficients"][1] == -data["C"] < 0
                for key, value in (("F", data["F"]), ("b", b), ("z", z)):
                    maxima[key] = max(maxima[key], value)
                roots = nonnegative_integer_roots(*data["coefficients"])
                assert len(roots) <= (1 if data["a"] <= 0 else 2)
                for y in roots:
                    counts["nonnegative_integer_residual_roots"] += 1
                    maxima["integer_root_y"] = max(maxima["integer_root_y"], y)
                    A2, A1, A0 = data["coefficients"]
                    assert A2 * y * y + A1 * y + A0 == 0
                    rec = reconstruct(s, t, x, y, z, b)
                    assert rec["residue"] == 0
                    if len(candidate_examples) < 4:
                        candidate_examples.append(dict(data=[s, t, x, y, z, b],
                            scales=[rec["S"], rec["T"], rec["U"]], a=data["a"]))
                    if rec["d"] < 1:
                        continue
                    counts["positive_d"] += 1
                    if not (rec["alpha"] >= rec["k"] >= b + 1):
                        continue
                    counts["nonsingular_sector"] += 1
                    congruence = (rec["F"] * rec["E"] - rec["J"]) % rec["m"] == 0
                    integral = all(rec[q].denominator == 1 for q in ("S", "T", "U"))
                    assert congruence == integral
                    if not congruence:
                        continue
                    counts["congruence_pass"] += 1
                    if min(rec[q] for q in ("S", "T", "U")) <= 0:
                        continue
                    counts["positive_scales"] += 1
                    model = audit_model(rec)
                    if min(model["sign_factors"]) <= 0:
                        continue
                    counts["positive_signs"] += 1
                    assert all(v == 0 for v in model["row_residues"] + model["pair_residues"])
                    assert model["gaps"] is not None and min(model["gaps"]) > 0
                    counts["exact_models"] += 1
                    models.append(dict(parameters=[s, t, x, y, z, b],
                                       scales=[rec[q] for q in ("S", "T", "U")],
                                       **model))
    return dict(fixed_low_row=[s, t], status="complete_for_this_low_row",
                counts=counts, maxima=maxima, models=models,
                candidate_examples=candidate_examples)


def regression_checks():
    results = []
    for name, values in [
        ("known_integer_model_with_one_negative_high_D", (1, 2, -1, 1, 3, 2)),
        ("known_rational_zero_D_model", (3, 4, 0, 0, 0, 6)),
    ]:
        rec = reconstruct(*values)
        model = audit_model(rec)
        assert min(rec[q] for q in ("S", "T", "U")) > 0
        assert all(v == 0 for v in model["row_residues"] + model["pair_residues"])
        assert min(model["sign_factors"]) > 0 and min(model["gaps"]) > 0
        results.append(dict(name=name, status="pass", parameters=values,
                            q=model["q"], D=model["D"], scales=[rec[q] for q in ("S", "T", "U")]))
    for name, values, expected in [
        ("positive_integral_difference_system_but_residual_nonzero", (1, 3, 0, 4, 0, 2), 3),
        ("zero_norm_first_family_at_b3", (3, 3, 0, 0, 1, 3), 3),
        ("zero_norm_second_family_at_b2", (2, 2, 1, 1, 1, 2), -8),
    ]:
        rec = reconstruct(*values)
        data = quadratic_data(values[0], values[1], values[2], values[4], values[5])
        y = values[3]
        A2, A1, A0 = data["coefficients"]
        assert rec["residue"] == expected
        assert A2 * y * y + A1 * y + A0 == rec["m"] * expected
        results.append(dict(name=name, status="pass", parameters=values,
                            original_residue=rec["residue"], residual_polynomial_value=rec["m"] * expected))
    # Exercise exact division with negative leading coefficient, repeated root,
    # linear degeneracy, irrational roots, and a genuine two-root polynomial.
    cases = [((1, -3, 2), (1, 2)), ((-1, -1, 2), (1,)),
             ((1, -4, 4), (2,)), ((0, -7, 21), (3,)),
             ((0, -7, 20), ()), ((1, 0, -2), ())]
    for coeffs, expected in cases:
        assert nonnegative_integer_roots(*coeffs) == expected
    results.append(dict(name="exact_integer_root_edge_cases", status="pass", cases=len(cases)))
    return results


def json_ready(value):
    if isinstance(value, Fraction):
        return value.numerator if value.denominator == 1 else str(value)
    if isinstance(value, dict):
        return {key: json_ready(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(val) for val in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixed", nargs=2, type=int, metavar=("S_LOW", "T_LOW"))
    parser.add_argument("--scan", type=int, help="complete every low row 1<=s,t<=this bound")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.fixed and args.scan:
        parser.error("use --fixed or --scan, not both")
    proof_name = "high_d_fixed_low_row_finiteness_v22.tex"
    here = Path(__file__).resolve().parent
    proof_candidates = (here / proof_name, here.parent / "paper" / proof_name)
    proof_path = next((path for path in proof_candidates if path.is_file()), None)
    result = dict(status="PASS", version=22,
                  theorem="finite reconstruction for a fixed two-integer low row, and exclusion of the symmetric sector",
                  arithmetic="Python standard library; exact integers and Fraction; no floating point",
                  F_bound="F <= s*t + (2*(s+t-1)+1)*(s-x) - 2",
                  scope="Only s,t are bounded in a scan; x,y,z,b and all high denominators are exhaustive for each low row.",
                  global_nonexistence_claim=False,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  proof_file=proof_name,
                  proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest() if proof_path else None,
                  coefficient_checks=coefficient_checks(), regressions=regression_checks())
    if args.fixed:
        result["reconstruction"] = reconstruct_fixed_low_row(*args.fixed)
    if args.scan:
        if args.scan < 1:
            parser.error("--scan must be positive")
        rows = [reconstruct_fixed_low_row(s, t) for s in range(1, args.scan + 1)
                for t in range(1, args.scan + 1)]
        totals = {name: sum(row["counts"][name] for row in rows) for name in rows[0]["counts"]}
        maxima = {name: max(row["maxima"][name] for row in rows) for name in rows[0]["maxima"]}
        result["scan"] = dict(low_row_range=dict(s=[1, args.scan], t=[1, args.scan]),
                              complete_low_rows=len(rows), totals=totals, maxima=maxima,
                              rows=rows)
    if args.output:
        args.output.write_text(json.dumps(json_ready(result), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = dict(coefficient_identities=len(result["coefficient_checks"]),
                   regressions=len(result["regressions"]), status="pass")
    if "scan" in result:
        summary["scan"] = {key: val for key, val in result["scan"].items() if key != "rows"}
    if "reconstruction" in result:
        summary["fixed_low_row"] = result["reconstruction"]["fixed_low_row"]
        summary["counts"] = result["reconstruction"]["counts"]
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
