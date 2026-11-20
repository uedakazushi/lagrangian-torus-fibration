#!/usr/bin/env python3
"""Exact algebra certificate for the v15 diamond obstruction.

Python standard library only. The proof in diamond_obstruction_v15.tex is
analytic and contains no denominator cutoff or catalog search. This script
checks its polynomial substitutions and the two logically forced small
negative-branch cases. It also verifies a reusable three-core partial patch;
that patch is not a global solution, and fails the new hub-balance condition.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


class Poly:
    """Sparse integer polynomial; equality compares every coefficient."""
    variables = ('H', 'S', 'u', 'v', 'r', 'h', 'k', 'L', 'rp', 'q')
    size = len(variables)

    def __init__(self, coefficients=None):
        self.c = {m: n for m, n in (coefficients or {}).items() if n}

    @classmethod
    def constant(cls, value):
        return cls({(0,) * cls.size: value})

    @classmethod
    def variable(cls, name):
        m = [0] * cls.size
        m[cls.variables.index(name)] = 1
        return cls({tuple(m): 1})

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls.constant(value)

    def __add__(self, other):
        other = self.coerce(other)
        out = dict(self.c)
        for m, value in other.c.items():
            out[m] = out.get(m, 0) + value
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -value for m, value in self.c.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        out = {}
        for a, av in self.c.items():
            for b, bv in other.c.items():
                m = tuple(x + y for x, y in zip(a, b))
                out[m] = out.get(m, 0) + av * bv
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert exponent >= 0
        answer = Poly.constant(1)
        for _ in range(exponent):
            answer *= self
        return answer

    def __eq__(self, other):
        return self.c == self.coerce(other).c

    def serial(self):
        return [{'powers': dict((v, n) for v, n in zip(self.variables, m) if n),
                 'coefficient': coefficient}
                for m, coefficient in sorted(self.c.items())]


checks = []

def identity(label, actual, expected):
    assert actual == expected, label
    checks.append({'identity': label, 'residual': (actual - expected).serial()})


H, S, u, v, r, h, k, L, rp, q = map(Poly.variable, Poly.variables)

# Negative branch: multiply the pair determinant residual by H(H+1).
an = u * (H + S) * S + H
bn = v * (H + S + 1) * S + H + 1
negative_residual = ((an - H * u) * (bn + (H + 1) * v)
                     - an * bn + H * (H + 1))
identity('negative_branch_E_identity', negative_residual,
         (S * S - H * (H + 1)) * u * v
         + H * (H + 1) * (v - u + 1))

# Four common-low alternatives exchange x and its (q-1)/x partner.
identity('positive_unit_pair_outgoing_sum', 1 + (q - 1), q)
identity('negative_unit_pair_outgoing_sum', -1 - (q - 1), -q)

# The n23 triple is forced by the two oriented canonical models.
identity('n23_total', (rp + 2 - (S + L - 1)) + (1 + S - rp) + (1 + L), 5)
identity('central_reverse_baseline_sum', ((S + L - 1) - r - 2) + (r - S - 1), L - 4)

# L=4, primed s'=1, S'=2r', T'=2r'+3, z'=h(r'+1).
a = 2 * r + 1
b = h * (r + 1) * (2 * r + 3) + 1
x = Poly.constant(2)
y = h * (2 * r + 3)
A = a + x - 1
B = b - y + h * (r + 1)
identity('L4_s_unit_pair_residual', A * B - a * b + 1, 2 - h * (r + 1))

# L=4, primed z'=1, S'=2r'-1, T'=2r'+2, s'=hr'.
a = h * r * (2 * r - 1) + 1
b = 2 * r + 3
x = h * (2 * r - 1)
y = Poly.constant(2)
A = a + x - h * r
B = b - y + 1
identity('L4_z_unit_pair_residual', A * B - a * b + 1, h * (r - 2))

# The final forced model r'=3,S'=4,T'=7.
a, b = 12 * h + 1, 28 * k + 1
A, B = 13 * h + 1, 25 * k + 1
identity('L4_terminal_pair_residual', A * B - a * b + 1,
         h + 1 - k * (11 * h + 3))

# L=1, y=1 switch forces H in {1,2}, S>=2, and S|(H+1).
negative_small = []
for Hvalue in (1, 2):
    for Svalue in range(2, Hvalue + 2):
        if (Hvalue + 1) % Svalue:
            continue
        rvalue = Hvalue + Svalue
        if not Fraction(Svalue * Svalue, 2) < Hvalue * (Hvalue + 1) < 2 * Svalue * Svalue:
            reason = 'unprimed strict H bound fails'
            detail = {'H': Hvalue, 'S': Svalue}
        else:
            Sprime = rvalue - 2
            lower, upper = Sprime + 1, Svalue + 1
            assert lower == upper
            rprime = lower
            Hprime = rprime - Sprime
            assert not (Fraction(Sprime * Sprime, 2) < Hprime * (Hprime + 1)
                        < 2 * Sprime * Sprime)
            reason = 'primed strict H bound fails'
            detail = {'H': Hvalue, 'S': Svalue, 'r': rvalue,
                      'Sprime': Sprime, 'rprime': rprime, 'Hprime': Hprime}
        negative_small.append({'parameters': detail, 'exclusion': reason})
assert [(e['parameters']['H'], e['parameters']['S']) for e in negative_small] == [(1, 2), (2, 3)]


def verify_local(qvalues, matrix, weights):
    assert len(qvalues) == len(matrix) == len(weights) == 4
    for i in range(4):
        assert matrix[i][i] == 0
        assert sum(matrix[i]) == -qvalues[i]
    for i, j in combinations(range(4), 2):
        assert matrix[i][j] * matrix[j][i] == qvalues[i] * qvalues[j] - 1
    slack = []
    for i in range(4):
        for j in range(4):
            if i != j:
                d = weights[j] - weights[i] * Fraction(matrix[i][j], qvalues[i])
                assert d > 0
                slack.append(d)
    D = [-qvalues[i] - sum(matrix[j][i] for j in range(4)) for i in range(4)]
    assert sum(D) == 0
    return D, min(slack)


# A nonempty low-edge subsystem: its unequal lengths block global completion.
q2 = [7, 7, 1, 1]
p2 = [[0, -6, 1, -2], [-8, 0, -2, 3], [6, -3, 0, -4], [-3, 2, 0, 0]]
w2 = list(map(Fraction, [7, 7])) + [Fraction(13, 12), Fraction(13, 4)]
q3 = [11, 9, 1, 1]
p3 = [[0, -14, -2, 5], [-7, 0, 2, -4], [-5, 4, 0, 0], [2, -2, -1, 0]]
w3 = list(map(Fraction, [11, 9])) + [Fraction(17, 8), Fraction(21, 4)]
V = [[0, 0, -1, 0], [2, 0, 0, -3], [0, -1, 0, 0], [-3, 0, 2, 0]]
w4 = list(map(Fraction, [3, 1, 3, 1]))
D2, slack2 = verify_local(q2, p2, w2)
D3, slack3 = verify_local(q3, p3, w3)
D4, slack4 = verify_local([1, 1, 1, 1], V, w4)
assert D2 == [-2, 0, 0, 2]
assert D3 == [-1, 3, 0, -2]
assert D4 == [0, 0, -2, 2]
assert D2[2] + D3[2] == D2[3] + D4[2] == D3[3] + D4[3] == 0
n23 = [1 - p2[2][0] - p3[2][0], 1 - p2[2][1] - p3[2][1], 1 - p2[2][3] - p3[2][3]]
n24 = [1 - p2[3][0] - V[2][0], 1 - p2[3][1] - V[2][1], 1 - p2[3][2] - V[2][3]]
n34 = [1 - p3[3][0] - V[3][0], 1 - p3[3][1] - V[3][1], 1 - p3[3][2] - V[3][2]]
assert [n23, n24, n34] == [[0, 0, 5], [4, 0, 1], [2, 3, 0]]
for n in (n23, n24, n34):
    assert min(n) >= 0 and sum(n) == 5
hub_defect = p2[2][3] + p3[2][3] - p2[3][2] - p3[3][2]
assert hub_defect == -3

script_path = Path(__file__).resolve()
source_candidates = [script_path.with_name('diamond_obstruction_v15.tex'),
                     script_path.parent.parent / 'papers/sections/paper' / 'diamond_obstruction_v15.tex']
source_path = next((candidate for candidate in source_candidates if candidate.is_file()), None)
assert source_path is not None, 'The accompanying analytic proof must be available.'

result = {
    'status': 'PASS',
    'passed': True,
    'version': 'v15',
    'script_sha256': sha256(script_path.read_bytes()).hexdigest(),
    'source_sha256': sha256(source_path.read_bytes()).hexdigest(),
    'scope': 'Symbolic integer-polynomial identities and exactly two logically forced small cases. No denominator bound and no local-model catalog used. The analytic proof is in diamond_obstruction_v15.tex.',
    'polynomial_identity_count': len(checks),
    'polynomial_identities': checks,
    'negative_branch_complete_small_cases': negative_small,
    'partial_patch': {
        'scope': 'Three positive local cores satisfying all three mutual low-edge node and D conditions; not a global diamond solution.',
        'core_orders': {'2': [0, 1, 3, 4], '3': [0, 1, 2, 4], '4': [0, 1, 2, 3]},
        'q': {'2': q2, '3': q3, '4': [1, 1, 1, 1]},
        'p': {'2': p2, '3': p3, '4': V},
        'D': {'2': D2, '3': D3, '4': D4},
        'weights': {'2': list(map(str, w2)), '3': list(map(str, w3)), '4': list(map(str, w4))},
        'minimum_positive_slack': {'2': str(slack2), '3': str(slack3), '4': str(slack4)},
        'nodes': {'23': n23, '24': n24, '34': n34},
        'hub_balance_defect': hub_defect,
        'global_completion': 'Impossible by the new hub-balance identity; diamond exclusion does not rely on this example.'
    }
}
output = script_path.with_name('diamond_obstruction_verification_v15.json')
output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'polynomial_identities': len(checks),
                  'negative_small_cases': len(negative_small), 'output': output.name}, ensure_ascii=False))
