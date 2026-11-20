#!/usr/bin/env python3
"""Exact certificates for the unbounded v12 cycle-completion arguments.

Only the Python standard library is used.  Polynomial identities are checked
by coefficient comparison.  The finite cases are proof-derived binary signs
and endpoint choices, not a truncation in the high denominators.  Inequality
arguments are recorded through their exact positive-remainder identities;
the TeX proof supplies the quantified order assumptions.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

NAMES = ('r', 'x', 'T', 'z', 'a', 'b', 's')
N = len(NAMES)
ZERO = (0,) * N


class Poly:
    def __init__(self, terms=0):
        if isinstance(terms, dict):
            self.d = {k: F(v) for k, v in terms.items() if v}
        else:
            self.d = {ZERO: F(terms)} if terms else {}

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Poly) else Poly(value)

    def __add__(self, other):
        d = dict(self.d)
        for k, v in self.coerce(other).d.items():
            d[k] = d.get(k, F(0)) + v
        return Poly(d)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.d.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        d = {}
        for k, v in self.d.items():
            for j, w in self.coerce(other).d.items():
                key = tuple(ki + ji for ki, ji in zip(k, j))
                d[key] = d.get(key, F(0)) + v * w
        return Poly(d)

    __rmul__ = __mul__

    def __pow__(self, power):
        assert power >= 0
        ans = Poly(1)
        for _ in range(power):
            ans = ans * self
        return ans

    def substitute(self, **mapping):
        ans = Poly()
        for powers, coefficient in self.d.items():
            term = Poly(coefficient)
            for name, exponent in zip(NAMES, powers):
                term *= self.coerce(mapping.get(name, variables[name])) ** exponent
            ans += term
        return ans


variables = {}
for i, name in enumerate(NAMES):
    exponent = [0] * N
    exponent[i] = 1
    variables[name] = Poly({tuple(exponent): 1})
r, x, T, z, a, b, s = (variables[name] for name in NAMES)
checks = []


def check(condition, label):
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def identity(left, right, label):
    check(not (Poly.coerce(left) - right).d, label)


# The maximal-negative specialization is s=a-1=rx, A=x+1, b=zT+1.
aa, bb, AA = r * x + 1, z * T + 1, x + 1
bracket = (1 + r * r * x) * T - (x + 1) * (r + 1)
equation = z * bracket + (r + 1) * ((r - 1) * x - 1)
pair_residual = AA * (r * bb + 1 + (r + 1) * z) - (r + 1) * (aa * bb - 1)
identity(pair_residual, -equation, 'maximal-negative equation from the original pair product')
identity(bracket - (x * (r * r - r - 1) - r),
         (1 + r * r * x) * (T - 1), 'first lower bound, T>=1')
identity(x * (r * r - r - 1) - r - (r * r - 2 * r - 1),
         (x - 1) * (r * r - r - 1), 'second lower bound, x>=1')
identity((r * r - 2 * r - 1).substitute(r=r + 3),
         r * r + 4 * r + 2, 'strict positivity for r>=3, using r-3>=0')
identity((r * r - r - 1).substitute(r=r + 3),
         r * r + 5 * r + 5, 'positive coefficient in the x>=1 bound')
identity((r - 1) * x - 1,
         (r - 1) * (x - 1) + r - 2, 'right side is strictly negative for r>=3')
identity(bracket.substitute(r=2),
         (1 + 4 * x) * (T - 1) + x - 2, 'r=2, x>=2 lower bound')
identity(equation.substitute(r=2),
         z * ((1 + 4 * x) * (T - 1) + x - 2) + 3 * (x - 1),
         'r=2, x>=2 strict nonzero residual')
identity(equation.substitute(r=2, x=1), z * (5 * T - 6),
         'last maximal-negative branch gives z(5T-6)=0')
check(6 % 5 != 0, '5T=6 has no integer solution')
identity((a * b - (a * x - 1)), a * (b - x) + 1,
         'r=1 obstruction is a nonzero residue 1 modulo a>1')

# The extremal positive entry is impossible at canonical B: T=1 and S<=T
# force S=1 and hence the already excluded s=a-1.  This uses the proved
# low-entry theorem, not an extra finite computation.

# For r=z=1 the determinant and coefficient identities are exact.
AA = 2 * a - 1 - s
twice_B = b + 3
identity(AA * twice_B - 2 * (a * b - 1),
         6 * a + 2 - (s + 1) * (b + 3),
         'r=z=1 factorization from original determinant')
twice_s_DA = s * (b + 1 - 2 * a) + 2 * (a - 1)
identity(s * (-2 * a + twice_B - 2) + 2 * (a - 1),
         twice_s_DA, 'D_A from its incoming column sum')
DB = 2 * (a - b) + 2 - s
identity(AA + 2 - b - (b - 1), DB, 'D_B from its incoming column sum')
identity(DB + s, 2 * (a - b + 1), 'b>a implies D_B<=-s')
identity(6 * a + 2 - 2 * (b + 3), 2 * (3 * a - 2 - b),
         's=1 implies b=3a-2')
check(2 % 3 != 0, 's=2 would require 3 to divide 6a+2')
identity(twice_s_DA + (a - 1) * (s - 2), s * (b - a),
         'a>=b and s>=3 imply D_A<0 by an explicit nonpositive remainder')
identity(DB.substitute(b=a), 2 - s, 'a=b also has D_B<0 for s>=3')

# Binary sign cases use no denominator cutoff.
c4_patterns = []
for eps in product((-1, 1), repeat=4):
    allowed = all(not (eps[i] == -1 and eps[(i + 1) % 4] == 1)
                  for i in range(4))
    check(allowed == (len(set(eps)) == 1),
          'C4 no-negative-common-puncture forces constant pairing')
    if allowed:
        c4_patterns.append(eps)
check(c4_patterns == [(-1,) * 4, (1,) * 4], 'exactly two constant labelled C4 patterns')

c5_two_types, c5_final = [], []
for eps in product((-1, 1), repeat=5):
    no_adjacent_plus = all(not (eps[i] == eps[(i + 1) % 5] == 1)
                           for i in range(5))
    no_distance_two_plus = all(not (eps[i] == eps[(i + 2) % 5] == 1)
                               for i in range(5))
    allowed = no_adjacent_plus and no_distance_two_plus
    check(allowed == (eps.count(1) <= 1), 'C5 exact adjacency/distance-two sign intersection')
    if allowed:
        lam = tuple(-(eps[i] + eps[(i + 1) % 5]) // 2 for i in range(5))
        counts = (lam.count(1), lam.count(0), lam.count(-1))
        check(counts in ((5, 0, 0), (3, 2, 0)), 'C5 two preliminary lambda types')
        record = {'epsilon': eps, 'lambda': lam, 'counts': counts}
        c5_two_types.append(record)
        if counts != (5, 0, 0):
            check(eps.count(1) == 1, 'excluding all-positive common punctures leaves one plus')
            center = eps.index(1)
            check({i for i, value in enumerate(lam) if value == 0}
                  == {(center - 1) % 5, center}, 'zero lambdas lie on the two edges at the plus vertex')
            c5_final.append(record)
check(len(c5_two_types) == 6 and len(c5_final) == 5,
      'six preliminary and five final labelled C5 sign patterns')

# Each of five edges supplies one full positive numerator q-1; no core can
# receive more than one.  Verify the exact finite incidence implication.
full_endpoint_assignments = []
for ends in product((0, 1), repeat=5):
    occupied = [0] * 5
    for i, end in enumerate(ends):
        occupied[(i + end) % 5] += 1
    if max(occupied) <= 1:
        check(occupied == [1] * 5, 'five full entries force exactly one at each core')
        full_endpoint_assignments.append(ends)
check(len(full_endpoint_assignments) == 2, 'the two possible full-entry incidence orientations')

# Exact rational sanity checks are illustrations, not the quantified proof.
examples = []
for aa, bb, ss in [(3, 7, 1), (5, 13, 1), (13, 13, 4), (29, 19, 7)]:
    SS, yy, TT = F(aa - 1, ss), F(bb - 1, 2), bb - 1
    check(SS.denominator == yy.denominator == 1, 'illustrative local integrality')
    AA, BB = 2 * aa - 1 - ss, F(bb + 3, 2)
    q = (aa, bb, 1, 1)
    P = ((0, -AA, aa - 1, -ss), (-BB, 0, -yy, 1),
         (1, -2, 0, 0), (-SS, TT, SS - TT - 1, 0))
    weights = (F(aa), F(bb), F(aa - 1) + F(1, 2), F(1) + F(1, 2 * TT))
    check(all(sum(P[i]) == -q[i] for i in range(4)), 'illustrative local row sums')
    check(all(P[i][j] * P[j][i] == q[i] * q[j] - 1
              for i in range(4) for j in range(i + 1, 4)), 'illustrative six exact determinants')
    check(all(weights[j] - weights[i] * F(P[i][j], q[i]) > 0
              for i in range(4) for j in range(4) if i != j), 'illustrative exact positive basins')
    defects = [-q[i] - sum(P[j][i] for j in range(4) if j != i) for i in range(4)]
    check(all(defects[i] < 0 for i in (0, 1) if q[i] == max(q[:2])),
          'illustrative maximum denominator has negative coefficient, including equality')
    examples.append({'a': aa, 'b': bb, 's': ss,
                     'D': [str(v) for v in defects],
                     'weights': [str(v) for v in weights]})

tex = Path(__file__).with_name('quintic_cycle_completion_v12.tex')
if not tex.is_file():
    tex = Path(__file__).resolve().parent.parent / 'paper' / 'quintic_cycle_completion_v12.tex'
out = {
    'version': 12, 'status': 'passed', 'check_count': len(checks), 'checks': checks,
    'scope': 'Exact polynomial identities, proof-derived finite sign and incidence cases, and illustrative exact local models. No high-denominator cutoff is used. The quantified inequalities and prior theorems are documented in the TeX proof.',
    'dependencies': ['standard positive two-high normal form',
                     'td12:low-entry (S<=T)',
                     'cq12:no-constant-pairing',
                     'path and triangle component obstructions'],
    'local_lemma_requires': 'positive integral local model only; no parity, clutching, D cancellation or node condition',
    'C4_requires': 'positive local charts, integer marked clutching, opposing D cancellation, nonnegative nodes',
    'C5_all_positive_common_exclusion_requires': 'positive local charts, odd high denominators, integer marked clutching, opposing D cancellation; no node condition',
    'remaining_C5_type': [3, 2, 0],
    'C4_patterns_before_constant_pairing_obstruction': c4_patterns,
    'C5_preliminary_patterns': c5_two_types, 'C5_final_patterns': c5_final,
    'full_endpoint_assignments': full_endpoint_assignments, 'exact_examples': examples,
    'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    'source_sha256': sha256(tex.read_bytes()).hexdigest(),
}
path = Path(__file__).with_name('cycle_completion_verification_v12.json')
path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'status': 'passed', 'check_count': len(checks), 'output': str(path)}, indent=2))
