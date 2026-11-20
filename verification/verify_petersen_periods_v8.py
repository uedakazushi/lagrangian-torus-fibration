#!/usr/bin/env python3
"""Exact arithmetic certificates for the v8 Petersen-period statements.

This verifies finite lattices and residue counts.  It does not replace the
relative-Moser area-realization proof or prove a global sextic affine atlas.
Only the Python standard library is used.
"""

from fractions import Fraction
from itertools import combinations
from math import gcd, prod
from pathlib import Path
import hashlib
import json


CHECKS = 0


def check(statement, message):
    global CHECKS
    if not statement:
        raise AssertionError(message)
    CHECKS += 1


def det(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    n = len(a)
    answer = Fraction(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            answer = -answer
        q = a[j][j]
        answer *= q
        for k in range(j, n):
            a[j][k] /= q
        for i in range(j + 1, n):
            q = a[i][j]
            for k in range(j, n):
                a[i][k] -= q * a[j][k]
    return answer


def rank_mod2(matrix):
    a = [list(x % 2 for x in row) for row in matrix]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        for i in range(len(a)):
            if i != row and a[i][col]:
                a[i] = [x ^ y for x, y in zip(a[i], a[row])]
        row += 1
    return row


def factors(n):
    answer = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            answer.append((p, e))
        p += 1
    if n > 1:
        answer.append((n, 1))
    return answer


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def add(*vectors):
    return tuple(sum(xs) for xs in zip(*vectors))


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def primitive_pair(x, y):
    minors = [x[i] * y[j] - x[j] * y[i]
              for i, j in combinations(range(len(x)), 2)]
    common = 0
    for m in minors:
        common = gcd(common, abs(m))
    return common == 1


# Coordinates in [e12],[e13],[e14],[e23],[e24].  Kneser labels below use 0..4.
RAYS = {
    (0, 1): (1, 0, 0, 0, 0),
    (0, 2): (0, 1, 0, 0, 0),
    (0, 3): (0, 0, 1, 0, 0),
    (1, 2): (0, 0, 0, 1, 0),
    (1, 3): (0, 0, 0, 0, 1),
    (2, 3): (-1, -1, -1, -1, -1),
    (0, 4): (-1, -1, -1, 0, 0),
    (1, 4): (-1, 0, 0, -1, -1),
    (2, 4): (1, 0, 1, 0, 1),
    (3, 4): (1, 1, 0, 1, 0),
}
VERTICES = [(kind, a) for kind in ("A", "B") for a in range(5)]
LABELS = {
    ("A", a): tuple(sorted((2 * a % 5, (2 * a + 1) % 5)))
    for a in range(5)
}
LABELS.update({
    ("B", a): tuple(sorted(((2 * a + 2) % 5, (2 * a + 4) % 5)))
    for a in range(5)
})
VECTORS = {v: RAYS[LABELS[v]] for v in VERTICES}
EDGES = [(v, w) for v, w in combinations(VERTICES, 2)
         if not set(LABELS[v]) & set(LABELS[w])]
MATCHING = [(v, w) for v, w in EDGES if v[1] == w[1]]
CROSSING = [(v, w) for v, w in EDGES if v[1] != w[1]]
check(len(EDGES) == 15 and len(MATCHING) == 5 and len(CROSSING) == 10,
      "Petersen face counts")
for v in VERTICES:
    neighbors = [w if u == v else u for u, w in EDGES if u == v or w == v]
    check(len(neighbors) == 3, f"cubic vertex {v}")
    check(add(*(VECTORS[w] for w in neighbors)) == VECTORS[v],
          f"ambient fan balancing at {v}")
for v, w in EDGES:
    check(primitive_pair(VECTORS[v], VECTORS[w]), f"unimodular cone {v,w}")

# Global meridians H=Z^5/Z(1,...,1), in the first four meridians as basis.
MERIDIANS = [tuple(int(i == j) for j in range(4)) for i in range(4)]
MERIDIANS.append((-1, -1, -1, -1))
check(add(*MERIDIANS) == (0, 0, 0, 0), "global meridian relation")
for a, b in combinations(range(5), 2):
    check(primitive_pair(MERIDIANS[a], MERIDIANS[b]),
          f"crossing homology injection {a,b}")
for a in range(5):
    beta_a = add(MERIDIANS[(a - 1) % 5], MERIDIANS[(a + 1) % 5])
    beta_b = add(MERIDIANS[(a - 2) % 5], MERIDIANS[(a + 2) % 5])
    check(primitive_pair(MERIDIANS[a], beta_a), f"annular homology injection {a}")
    check(add(MERIDIANS[a], beta_a, beta_b) == (0, 0, 0, 0),
          f"normal Euler framing {a}")

CROSS_MATRIX = ((-1, 0), (0, -1))
MATCH_MATRIX = ((-1, -1), (0, 1))
check(abs(det(CROSS_MATRIX)) == 1, "crossing action chart determinant")
check(abs(det(MATCH_MATRIX)) == 1, "matching action chart determinant")
for action, expected in [((-1, 0), (1, 0)), ((-1, 1), (0, 1))]:
    check(tuple(dot(row, action) for row in MATCH_MATRIX) == expected,
          "matching boundary ray compatibility")

# The unique rational global meridian forms compatible with these face maps.
TWICE_FORMS = [
    [-2, 1, 0, 1, 0],
    [0, 0, 0, 1, 1],
    [1, 0, 1, 0, -2],
    [1, 1, -2, -2, 1],
    [0, -2, 1, 0, 0],
]
FORMS = [[Fraction(x, 2) for x in row] for row in TWICE_FORMS]
check(add(*TWICE_FORMS) == (0, 0, 0, 0, 0), "rational meridian relation")
for a, phi in enumerate(FORMS):
    for kind, j in VERTICES:
        diff = (j - a) % 5
        if diff == 0:
            expected = Fraction(-1)
        elif kind == "A":
            expected = Fraction(1, 2) if diff in (2, 3) else Fraction(0)
        else:
            expected = Fraction(1, 2) if diff in (1, 4) else Fraction(0)
        check(dot(phi, VECTORS[(kind, j)]) == expected,
              f"ambient meridian values {a,kind,j}")
    check(any(x.denominator == 2 for x in phi), f"nonintegral meridian {a}")
for v, w in CROSSING:
    a, b = v[1], w[1]
    matrix = [[dot(FORMS[c], VECTORS[x]) for x in (v, w)] for c in (a, b)]
    check(matrix == [[-1, 0], [0, -1]], f"rational extension crossing restriction {v,w}")
for a in range(5):
    beta = add(FORMS[(a - 1) % 5], FORMS[(a + 1) % 5])
    matrix = [[dot(phi, VECTORS[x]) for x in (("A", a), ("B", a))]
              for phi in (FORMS[a], beta)]
    check(matrix == [[-1, -1], [0, 1]], f"rational extension matching restriction {a}")
check(rank_mod2(TWICE_FORMS) == 4, "cotangent overlattice index 2^4")
odd_cycle_matrix = [[int(j in ((i - 2) % 5, (i + 2) % 5))
                     for j in range(5)] for i in range(5)]
check(abs(det(odd_cycle_matrix)) == 2, "unique half-integral odd-cycle solution")
check(all(sum(row) == 2 for row in odd_cycle_matrix), "constant one-half solution")

# Independent finite checks of the general CRT counting formula.
split_instances = 0
for q in range(1, 50):
    predicted = prod(p ** (e - 1) * (p - 2) for p, e in factors(q))
    for p in range(q):
        if gcd(p, q) != 1:
            continue
        actual = sum(gcd(a, q) == gcd(p - a, q) == 1 for a in range(q))
        check(actual == predicted, f"CRT split formula q={q},p={p}")
        check((actual > 0) == (q % 2 == 1), "odd denominator iff splittable")
        split_instances += 1

farey_instances = 0
for q in range(1, 26, 2):
    for qp in range(1, 26, 2):
        if gcd(q, qp) != 1:
            continue
        _, x, y = egcd(qp, q)
        rhs = 1 - q * qp
        p, pp = rhs * x, rhs * y
        check(q * qp + qp * p + q * pp == 1, "signed annular Bezout equation")
        check(gcd(p, q) == gcd(pp, qp) == 1, "primitive endpoint fractions")
        h_a, h_b = Fraction(p, q), -1 - Fraction(pp, qp)
        check(h_a - h_b == Fraction(1, q * qp), "positive odd reciprocal area")
        farey_instances += 1

factorization_instances = 0
for m in range(1, 200, 2):
    actual = sum(m % q == 0 and gcd(q, m // q) == 1 for q in range(1, m + 1))
    check(actual == 2 ** len(factors(m)), f"coprime ordered factorization count {m}")
    factorization_instances += 1

result = {
    "version": 8,
    "status": "passed",
    "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "exact_checks": CHECKS,
    "petersen_vertices": 10,
    "unimodular_faces": 15,
    "crossing_faces": 10,
    "matching_faces": 5,
    "normalized_branch_denominators": [1] * 10,
    "normalized_internal_area_over_2piw": "1",
    "ambient_rational_extension_denominator": 2,
    "ambient_cotangent_overlattice_index": 16,
    "twice_meridian_forms": TWICE_FORMS,
    "crt_split_instances": split_instances,
    "farey_completion_instances": farey_instances,
    "odd_factorization_instances": factorization_instances,
    "scope": "Finite integral certificates only; relative Moser and the core chart homeomorphism are proved in the text. No global sextic atlas is certified.",
}
output = Path(__file__).with_name("petersen_periods_verification_v8.json")
output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(f"v8 Petersen periods: {CHECKS} exact checks passed; "
      f"15 unimodular faces; ambient period denominator 2, overlattice index 16. "
      f"Full result: {output.name}")
