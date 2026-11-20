#!/usr/bin/env python3
"""Exact v13 Schur bounds and beta=-1 slice identities.

No new denominator-box search is performed. The proof of the strict signed
bounds and of integrality equivalence is in the accompanying research note.
This script checks the polynomial algebra, an explicit positive integral
example, and its occurrence in the inherited catalog when that file exists.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json


class Poly(dict):
    nvars = 5

    @staticmethod
    def constant(value):
        return Poly({(0,) * Poly.nvars: value}) if value else Poly()

    @staticmethod
    def variable(index):
        return Poly({tuple(int(i == index) for i in range(Poly.nvars)): 1})

    @staticmethod
    def cast(value):
        return value if isinstance(value, Poly) else Poly.constant(value)

    def __add__(self, other):
        out = Counter(self)
        for monomial, coefficient in self.cast(other).items():
            out[monomial] += coefficient
        return Poly({key: value for key, value in out.items() if value})

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.items()})

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        out = Counter()
        for left, a in self.items():
            for right, b in self.cast(other).items():
                out[tuple(i + j for i, j in zip(left, right))] += a * b
        return Poly({key: value for key, value in out.items() if value})

    __rmul__ = __mul__

    def __pow__(self, exponent):
        result = self.constant(1)
        for _ in range(exponent):
            result = result * self
        return result


def determinant(matrix):
    answer = Poly()
    for perm in permutations(range(3)):
        inversions = sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3))
        term = Poly.constant((-1) ** inversions)
        for row in range(3):
            term = term * matrix[row][perm[row]]
        answer = answer + term
    return answer


checks = []


def identity(name, left, right=0):
    assert Poly.cast(left) - Poly.cast(right) == {}, name
    checks.append(name)


A, E, C, x, y = [Poly.variable(i) for i in range(5)]
B = -E - 1
delta = -B * (A + 1) * (C - 1) + A * C * (B + 1)
identity("determinant in positive signed variables", delta,
         C * (A + E + 1) - (A + 1) * (E + 1))
identity("singular divisor identity",
         (A + 1 - C) * (E + 1 - C) - C * (C - 1), -delta)
s, alpha, beta, t, k = [Poly.variable(i) for i in range(5)]
identity("A=0 implication for B", (s * alpha) * beta - s,
         s * (alpha * beta - 1))
identity("C=1 third-row coefficient", (t * beta - 1) + 1, t * beta)

# Conditional slice t=1, beta=-1, k=0, before imposing integrality.
A = s * alpha - 1
B = -s - 1
C = s
M = [[B, A, 0], [-C, 0, A + 1], [0, C - 1, B + 1]]
rhs = [alpha, 0, 0]
delta = determinant(M)
identity("beta=-1 slice determinant", delta, s * (s - alpha))
expected_numerators = [-alpha ** 2 * s * (s - 1), -alpha * s ** 2, -alpha * s * (s - 1)]
for column in range(3):
    replaced = [[rhs[row] if j == column else M[row][j]
                 for j in range(3)] for row in range(3)]
    identity(f"beta=-1 slice Cramer numerator {column}",
             determinant(replaced), expected_numerators[column])
d = alpha - s
identity("T integrality numerator", alpha * s, s ** 2 + d * s)
identity("U integrality numerator", alpha * (s - 1), s * (s - 1) + d * (s - 1))

# Complete integral parameter family d,e >= 1, de >= 2.
d, e = Poly.variable(0), Poly.variable(1)
s = d * e
alpha = d * (e + 1)
S = d * (e + 1) ** 2 * (d * e - 1)
T = d * e * (e + 1)
U = (e + 1) * (d * e - 1)
q = [1 + s * S, 1 + T, 1 + s * U, 1]
p = [[0, S + alpha, -s * S - alpha - 1, -S],
     [s * T - 1, 0, -s * T, -T],
     [-s * U, -U - 1, 0, U],
     [-s, -1, s, 0]]
for i in range(4):
    identity(f"family row {i}", sum(p[i]), -q[i])
for i, j in combinations(range(4), 2):
    identity(f"family pair {i},{j}", p[i][j] * p[j][i], q[i] * q[j] - 1)
schur = [[(q[i] if i == j else p[i][j]) - p[i][3] * p[3][j]
          for j in range(3)] for i in range(3)]
expected_schur = [[1, alpha, -alpha - 1], [-1, 1, 0], [0, -1, 1]]
for i in range(3):
    for j in range(3):
        identity(f"family Schur entry {i},{j}", schur[i][j], expected_schur[i][j])
D0 = S + T - U - 1
identity("family positive low defect formula", D0, (alpha - 1) * U + T - 1)
expected_defects = [-s * D0, -D0 - alpha, s * D0 + alpha, D0]
for i in range(4):
    identity(f"family defect {i}", -q[i] - sum(p[j][i] for j in range(4)), expected_defects[i])
identity("family total defect", sum(expected_defects))
identity("family determinant", s * (s - alpha), -d ** 2 * e)
identity("family even q_a-1 factorization", q[0] - 1,
         d ** 2 * e * (e + 1) ** 2 * (d * e - 1))
identity("family even q_b-1 factorization", q[1] - 1, d * e * (e + 1))
identity("family even q_c-1 factorization", q[2] - 1, d * e * (e + 1) * (d * e - 1))
H, K = S + alpha, s * T - 1
identity("positive reverse AB area numerator", 2 * q[0] * q[1] - 2 * H * K - 1, 1)
identity("positive reverse C0 area numerator", 2 * q[2] - 2 * s * U - 1, 1)

# One exact model, already present in the inherited finite catalog.
q = [19, 7, 7, 1]
p = [[0, 12, -22, -9], [11, 0, -12, -6], [-6, -4, 0, 3], [-2, -1, 2, 0]]
w = [Fraction(19), Fraction(265, 22), Fraction(13, 6), Fraction(1)]
assert all(sum(p[i]) == -q[i] for i in range(4))
assert all(p[i][j] * p[j][i] == q[i] * q[j] - 1 for i, j in combinations(range(4), 2))
gaps = [w[j] - w[i] * p[i][j] / q[i] for i in range(4) for j in range(4) if i != j]
assert all(gap > 0 for gap in gaps)
defects = [-q[i] - sum(p[j][i] for j in range(4)) for i in range(4)]
assert defects == [-22, -14, 25, 11]
positive_edge_gaps = [w[j] - w[i] * p[i][j] / q[i] for i, j in [(0, 1), (1, 0), (3, 2), (2, 3)]]
assert positive_edge_gaps == [Fraction(1, 22), Fraction(1, 14), Fraction(1, 6), Fraction(1, 14)]
catalog_candidates = [Path(__file__).with_name('quintic_denominators_verification_v10.json'),
                      Path(__file__).resolve().parents[2] / 'deliverables/general_type_surface_fibration_v12/verification/quintic_denominators_verification_v10.json']
catalog = next((path for path in catalog_candidates if path.exists()), None)
catalog_ids = []
if catalog is not None:
    for model in json.loads(catalog.read_text())['catalog_models']:
        if sorted(model['q']) != sorted(q):
            continue
        for perm in permutations(range(4)):
            if ([model['q'][i] for i in perm] == q
                and [[model['p'][i][j] for j in perm] for i in perm] == p):
                catalog_ids.append(model['id'])
                break
    assert catalog_ids == [513, 514]

result = {
    'version': 'v13', 'passed': True,
    'polynomial_identities': len(checks), 'identity_names': checks,
    'family_parameters': 'positive integers d,e with de>=2',
    'classification_scope': 'The additional matching sign hypothesis and t=1,beta=-1,k=0 slice only.',
    'explicit_example': {'q': q, 'p': p, 'D': defects, 'weights': list(map(str, w)),
                         'positive_edge_area_gaps': list(map(str, positive_edge_gaps))},
    'inherited_catalog_ids_of_example': catalog_ids,
    'limitations': [
        'No arbitrary three-high all-positive exclusion is asserted.',
        'No general matching-sign theorem is asserted.',
        'The explicit example is not new; the note records a complete unbounded parameter slice.',
        'No classification of all singular Schur systems is asserted.',
    ],
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
output = Path(__file__).with_name('three_high_bounds_verification_v13.json')
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'passed': True, 'polynomial_identities': len(checks),
                  'catalog_ids': catalog_ids, 'output': str(output)}, ensure_ascii=False))
