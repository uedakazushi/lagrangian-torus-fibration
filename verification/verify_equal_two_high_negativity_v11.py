#!/usr/bin/env python3
"""Exact algebraic certificate for the unbounded equal-two-high sign proof.

Python standard library only.  Polynomial identities, sign-bound coefficients,
and all four residual quadratic equations are checked exactly.  A separate
finite parameter sample is a supplementary implementation check and is not the
proof of the unbounded theorem.
"""

from argparse import ArgumentParser
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import json


def polynomial_ring(names):
    names = tuple(names.split())
    length = len(names)

    class Poly:
        def __init__(self, terms=None):
            if isinstance(terms, Poly):
                self.terms = dict(terms.terms)
            elif isinstance(terms, (int, Fraction)):
                self.terms = {(0,) * length: Fraction(terms)} if terms else {}
            else:
                self.terms = {a: Fraction(b) for a, b in (terms or {}).items() if b}

        def __add__(self, other):
            other = Poly(other)
            answer = dict(self.terms)
            for monomial, coefficient in other.terms.items():
                answer[monomial] = answer.get(monomial, 0) + coefficient
            return Poly(answer)

        __radd__ = __add__

        def __neg__(self):
            return Poly({a: -b for a, b in self.terms.items()})

        def __sub__(self, other):
            return self + -Poly(other)

        def __rsub__(self, other):
            return Poly(other) - self

        def __mul__(self, other):
            other = Poly(other)
            answer = {}
            for a, b in self.terms.items():
                for c, d in other.terms.items():
                    monomial = tuple(x + y for x, y in zip(a, c))
                    answer[monomial] = answer.get(monomial, 0) + b * d
            return Poly(answer)

        __rmul__ = __mul__

        def __pow__(self, exponent):
            if not isinstance(exponent, int) or exponent < 0:
                raise ValueError("Only nonnegative integer powers are allowed")
            answer = Poly(1)
            for _ in range(exponent):
                answer *= self
            return answer

        def __eq__(self, other):
            return self.terms == Poly(other).terms

    variables = []
    for i in range(length):
        monomial = [0] * length
        monomial[i] = 1
        variables.append(Poly({tuple(monomial): 1}))
    return Poly, variables


def positive_divisors(number):
    result = []
    for divisor in range(1, isqrt(number) + 1):
        if number % divisor == 0:
            result.append(divisor)
            if divisor * divisor != number:
                result.append(number // divisor)
    return sorted(result)


def lmn(d, J, G):
    L = (d * d * (d * J - 4 * d + 4) * G * G
         + d * J * (2 * d * J - 6 * d + 8) * G
         + J * (d * (J - 1) ** 2 + 4 * J))
    M = d * d * (2 * J + d - 1) * G * G + d * J * (d + 2 * J) * G - J * J
    N = d * J * (d - 1) * G * G + d * J * J * G
    return L, M, N


def main():
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("equal_two_high_negativity_verification_v11.json"))
    args = parser.parse_args()
    checks = []

    def check(condition, label):
        if not condition:
            raise AssertionError(label)
        checks.append(label)

    # Exact polynomial identities behind the change of variables.
    _, (r, t, s, z) = polynomial_ring("r t s z")
    R = r * (r + 1)
    n = 2 * r + 1
    m = t * R
    q = m + 1
    d = s - z
    e = t - d
    A0 = 1 + t * r * r
    B0 = 1 + t * (r + 1) ** 2
    E = s * z + A0 * s - B0 * z - t - 1
    K = n * z - r * r * d + 1
    check((B0 - s) * (A0 + z) - (q * q - 1) == -E,
          "original conic equals the high-high determinant equation")
    check(E == s * z + d - 1 - t * K,
          "K identity after setting delta=s-z")
    G_numerator = r * r * m * d + R * s * z - n * m * z
    check(G_numerator - R * (e + 1) == R * E,
          "integer G equals R(e+1)/(sz) on the conic")
    J_numerator = m * d - d * R * (e + 1)
    check(J_numerator == d * (d - 1) * R,
          "Jsz=delta(delta-1)R")
    check(t * J_numerator == (d - 1) * m * d,
          "tJ=(delta-1)H")

    _, (r, m, S, Z) = polynomial_ring("r m S Z")
    R = r * (r + 1)
    n = 2 * r + 1
    H = Z - S
    q = m + 1
    A_numerator = r * S * q + m * S - m * r
    B_numerator = (r + 1) * Z * q - m * Z + m * (r + 1)
    reciprocal = m * m * (n * S - r * r * H - R) + m * (S * Z - R * H) + R * S * Z
    check(A_numerator * B_numerator - R * S * Z * (q * q - 1) == reciprocal,
          "reciprocal identity used to exclude nonpositive delta")

    # Central elimination, independently expanded from the two factors S,Z.
    _, (r, d, J, G) = polynomial_ring("r d J G")
    R = r * (r + 1)
    n = 2 * r + 1
    H = d * G + J
    S_numerator = (d * r * r - 1) * G + (J + 1) * r * r + r
    Z_numerator = S_numerator + n * H
    L = (d * d * (d * J - 4 * d + 4) * G * G
         + d * J * (2 * d * J - 6 * d + 8) * G
         + J * (d * (J - 1) ** 2 + 4 * J))
    M = d * d * (2 * J + d - 1) * G * G + d * J * (d + 2 * J) * G - J * J
    N = d * J * (d - 1) * G * G + d * J * J * G
    direct = d * J * S_numerator * Z_numerator - (d - 1) * R * n * n * H * H
    check(direct == R * R * L - R * M - N,
          "full unbounded polynomial elimination R^2 L-R M-N=0")

    # Three sign boundaries, certified by positive shifted coefficients.
    _, (x,) = polynomial_ring("x")
    shifted = [
        ("J=1, delta>=3", 3 * (x + 3) ** 3 - 8 * (x + 3) - 4, [53, 73, 27, 3]),
        ("J=2, delta>=4", 2 * (x + 4) ** 3 - 18 * (x + 4) - 16, [40, 78, 24, 2]),
        ("J=3, delta>=9", (x + 9) ** 3 - 4 * (x + 9) ** 2 - 36 * (x + 9) - 36, [45, 135, 23, 1]),
    ]
    sign_boundaries = []
    for label, polynomial, expected in shifted:
        coefficients = [polynomial.terms.get((i,), 0) for i in range(4)]
        check(coefficients == expected and all(c > 0 for c in coefficients),
              "positive coefficient certificate: " + label)
        sign_boundaries.append({"case": label, "coefficients_in_delta_minus_lower_bound": expected})
    _, (d,) = polynomial_ring("d")
    check(-(2 * d * d * (4 - d) + 24 * d) == 2 * d * (d - 6) * (d + 2),
          "negative derivative of J=3 L at G=1 for delta>=9")

    # The only finite portion of the unbounded proof.
    limits = {5: 5, 6: 2, 7: 1, 8: 1}
    bounded_cases = []
    residual = []
    for d, upper in limits.items():
        cut = upper + 1
        leading = d * d * (4 - d)
        derivative_at_cut = 2 * leading * cut + 24 * d
        L_cut = lmn(d, 3, cut)[0]
        check(leading < 0 and derivative_at_cut < 0 and L_cut < 0,
              f"J=3 exact upper bound G<={upper} when delta={d}")
        admissible = []
        for G in range(1, upper + 1):
            if ((d - 1) * (d * G + 3)) % 3 == 0:
                admissible.append(G)
                residual.append((d, G))
        bounded_cases.append({"delta": d, "G_upper": upper, "L_at_first_excluded_G": L_cut,
                              "integer_t_candidates": admissible})
    check(residual == [(5, 3), (6, 1), (6, 2), (7, 1)],
          "complete finite residual list after integer t")

    expected_quadratics = {
        (5, 3): (77, -912, -225),
        (6, 1): (20, -67, -16),
        (6, 2): (12, -223, -52),
        (7, 1): (47, -284, -63),
    }
    quadratic_table = []
    for d, G in residual:
        L, M, N = lmn(d, 3, G)
        coefficients = (L, -M, -N)
        common = gcd(gcd(abs(coefficients[0]), abs(coefficients[1])), abs(coefficients[2]))
        primitive = tuple(c // common for c in coefficients)
        check(primitive == expected_quadratics[(d, G)],
              f"independent residual quadratic delta={d},G={G}")
        a, b, c = primitive
        discriminant = b * b - 4 * a * c
        lower = isqrt(discriminant)
        check(lower * lower < discriminant < (lower + 1) ** 2,
              f"nonsquare discriminant delta={d},G={G}")
        quadratic_table.append({"delta": d, "G": G, "coefficients_in_R": primitive,
                                "discriminant": discriminant, "strict_square_bounds": [lower, lower + 1]})

    # Supplementary exact sample.  This is deliberately separated from the
    # symbolic proof certificate and carries no unbounded enumeration claim.
    sample = []
    for r, t in product(range(1, 81), range(1, 41)):
        R = r * (r + 1)
        m = t * R
        A0 = 1 + t * r * r
        B0 = 1 + t * (r + 1) ** 2
        for s in positive_divisors(m):
            numerator = A0 * s - t - 1
            denominator = B0 - s
            if numerator <= 0 or numerator % denominator:
                continue
            z = numerator // denominator
            if m % z:
                continue
            S, Z = m // s, m // z
            H, d = Z - S, s - z
            e = t - d
            G = r * r * H + R - (2 * r + 1) * S
            J = H - d * G
            eta = d + H - t - 1
            check(s * z + A0 * s - B0 * z == t + 1,
                  f"sample conic r={r},t={t},s={s},z={z}")
            check(1 <= d <= t and H > 0 and G > 0 and eta > 0,
                  f"sample all sign conclusions r={r},t={t},s={s},z={z}")
            check(G * s * z == R * (e + 1) and J * s * z == d * (d - 1) * R,
                  f"sample G,J identities r={r},t={t},s={s},z={z}")
            check((d == 1 and J == 0) or (d >= 2 and d - 1 <= J <= 3),
                  f"sample small-J conclusion r={r},t={t},s={s},z={z}")
            sample.append({"r": r, "t": t, "m": m, "s": s, "z": z,
                           "delta": d, "H": H, "G": G, "J": J, "eta": eta})

    result = {
        "version": 11,
        "status": "passed",
        "proof_scope": "Exact algebraic certificates for the unbounded equal-two-high-denominator inequality; the text supplies the general order and integer arguments.",
        "check_count": len(checks),
        "checks": checks,
        "sign_boundaries": sign_boundaries,
        "bounded_J3_cases": bounded_cases,
        "residual_quadratics": quadratic_table,
        "supplementary_sample": {
            "scope": "All positive divisor solutions for 1<=r<=80 and 1<=t<=40; not used to infer the unbounded result.",
            "parameter_pairs": 80 * 40,
            "solution_count": len(sample),
            "solutions": sample,
        },
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "check_count": len(checks),
                      "sample_solutions": len(sample), "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
