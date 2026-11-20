#!/usr/bin/env python3
"""Exact certificate for the low-low entry dichotomy and denominator descent.

The unbounded proof is in quintic_minimal_low_entry_v12.tex.  This script checks
its algebra by coefficient comparison, two exact local examples, and one entire
polynomial family with positive high-defect sum.  It performs no denominator-
bounded search.  Only the Python standard library is required.
"""

from fractions import Fraction
from pathlib import Path
import hashlib
import itertools
import json


class Poly:
    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @classmethod
    def variable(cls, name):
        return cls({(name,): 1})

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls({(): int(value)})

    def __add__(self, other):
        terms = self.terms.copy()
        for m, c in self.coerce(other).terms.items():
            terms[m] = terms.get(m, 0) + c
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        terms = {}
        for m, c in self.terms.items():
            for n, d in self.coerce(other).terms.items():
                monomial = tuple(sorted(m + n))
                terms[monomial] = terms.get(monomial, 0) + c * d
        return Poly(terms)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms


def variables(*names):
    return tuple(Poly.variable(name) for name in names)


identities = []


def identity(name, left, right):
    if left != right:
        raise AssertionError(name)
    identities.append(name)


r, s, z, S, T, H, J, w, c, e, j = variables(
    'r', 's', 'z', 'S', 'T', 'H', 'J', 'w', 'c', 'e', 'j')
R = r*(r+1)
F = (r+1)*(r+1)*S-r*r*T-R
identity('negative-sign exclusion of J<=H after clearing HJ',
         (r+1)*(r+1)*H-r*r*J-(2*r+1)*J,
         (r+1)*(r+1)*(H-J))
identity('Ec<=1 comparison numerator, without an ordering assumption',
         e-(e-c+1), c-1)
identity('positive-sign pair-product grouping',
         R+s*(r+1)*(S-r)+z*r*(r+1-T)+s*z*F,
         R+s*(r+1)*(S-r)+z*(s*F-r*(T-r-1)))
identity('positive-sign inequality factor',
         F-r*(T-r-1), (r+1)*((r+1)*S-r*T))
identity('d<=-3 integer-gap identity',
         r*(T-S)-r, r*T-(r+1)*S+S-r)

Q = H*(H+1)
identity('minimal-entry E numerator',
         (H+w+1)*(H+w+1)*H-(H+w)*(H+w)*(H+1), Q-w*w)
identity('E=0 lies strictly between consecutive squares, first gap',
         Q-H*H, H)
identity('E=0 lies strictly between consecutive squares, second gap',
         (H+1)*(H+1)-Q, H+1)
identity('E lower bound when w<=H after clearing H(H+1)',
         Q-w*w-H, (H-w)*(H+w))
delta = e-c
s_minus_z_cleared = (c-e)*Q+w*(c*(H+1)-e*H)
identity('s-z formula for the w<=H branch', s_minus_z_cleared,
         -delta*Q+w*(c-H*delta))
identity('s-z is positive when c>e', s_minus_z_cleared,
         (c-e)*(Q+w*(H+1))+e*w)
identity('strict D_B formula when delta=-j after clearing Hc',
         j*(H*c*w+c*w*w+H)-H-H*c*j+H*c*(H+1),
         j*(H*c*(w-1)+c*w*w)+H*c*(H+1)+H*(j-1))

# Unbounded H>=2 family for future notes.  Every row and crossing determinant
# is checked as a polynomial identity, not by sampling H.
a = 2*H*H+1
b = H*(H-1)*(2*H+1)+1
rr, ss, zz = 2*H, 2*H, (2*H+1)*(H-1)
xx, yy = H, H*(H-1)
AA, BB = a-H, b+H*H-1
pp = [
    [0, -AA, xx, -ss],
    [-BB, 0, -yy, zz],
    [rr, -rr-1, 0, 0],
    [-H, H, -1, 0],
]
qs = [a, b, 1, 1]
for i in range(4):
    identity(f'positive-sum family row {i}', sum(pp[i]), -qs[i])
for i, k in itertools.combinations(range(4), 2):
    identity(f'positive-sum family crossing {i},{k}',
             qs[i]*qs[k]-pp[i][k]*pp[k][i], 1)
defects = [-qs[i]-sum(pp[k][i] for k in range(4) if k != i)
           for i in range(4)]
DA = 2*H*H*H-2*H*H-2*H-1
DB = -2*H*H*H+3*H*H+H+1
identity('positive-sum family D_A', defects[0], DA)
identity('positive-sum family D_B', defects[1], DB)
identity('positive-sum family high-defect sum', DA+DB, H*(H-1))
identity('positive-sum family all-defect sum', sum(defects), 0)
identity('positive-sum family alpha', xx-ss, -H)
identity('positive-sum family beta', yy-zz, -(H*H-1))

# Strict signs for all H>=2: substitute H=t+2 and compare coefficients.
t = Poly.variable('t')
Ht = t+2
identity('positive-sum family D_A positive for H>=2',
         2*Ht*Ht*Ht-2*Ht*Ht-2*Ht-1,
         2*t*t*t+10*t*t+14*t+3)
identity('positive-sum family -D_B positive for H>=2',
         2*Ht*Ht*Ht-3*Ht*Ht-Ht-1,
         2*t*t*t+9*t*t+11*t+1)
identity('positive-sum family b-a positive for H>=2',
         Ht*(Ht-1)*(2*Ht+1)+1-(2*Ht*Ht+1),
         2*t*t*t+9*t*t+11*t+2)


def exact_model(name, aa, bb, rr, ss, zz, ww):
    """Check two prescribed models on the two sides of E=0."""
    assert (aa-1)//ss == (bb-1)//zz == ww
    assert (aa-1) % rr == 0 and (bb-1) % (rr+1) == 0
    xx, yy = (aa-1)//rr, (bb-1)//(rr+1)
    AA, BB = aa+xx-ss, bb-yy+zz
    pp = [[0, -AA, xx, -ss], [-BB, 0, -yy, zz],
          [rr, -rr-1, 0, 0], [-ww, ww, -1, 0]]
    qs = [aa, bb, 1, 1]
    assert all(sum(pp[i]) == -qs[i] for i in range(4))
    assert all(qs[i]*qs[k]-pp[i][k]*pp[k][i] == 1
               for i, k in itertools.combinations(range(4), 2))
    weights = [Fraction(aa), Fraction(bb),
               Fraction(xx)+Fraction(1, 2*rr), Fraction(zz)+Fraction(1, 2*ww)]
    assert all(weights[k]-weights[i]*Fraction(pp[i][k], qs[i]) > 0
               for i in range(4) for k in range(4) if i != k)
    defects = [-qs[i]-sum(pp[k][i] for k in range(4) if k != i)
               for i in range(4)]
    assert aa != bb
    assert (aa-bb)*defects[0] < 0 < (aa-bb)*defects[1]
    HH = rr-ww
    EE = 1-Fraction(ww*ww, HH*(HH+1))
    return {'name': name, 'q': qs, 'p': pp, 'D': defects,
            'r': rr, 's': ss, 'z': zz, 'S': ww, 'T': ww,
            'H': HH, 'E': str(EE), 'weights': [str(x) for x in weights]}


models = [exact_model('E positive; high-defect sum positive', 9, 11, 4, 4, 5, 2),
          exact_model('E negative; high-defect sum negative', 31, 7, 5, 10, 2, 3)]
here = Path(__file__).resolve().parent
source_candidates = [here/'quintic_minimal_low_entry_v12.tex',
                     here.parent/'papers/sections/paper'/'quintic_minimal_low_entry_v12.tex']
source = next((path for path in source_candidates if path.is_file()), None)
if source is None:
    raise FileNotFoundError('quintic_minimal_low_entry_v12.tex')
result = {
    'version': 12, 'passed': True,
    'method': 'Exact polynomial coefficient comparison and Fraction arithmetic; no denominator cutoff.',
    'polynomial_identity_count': len(identities),
    'polynomial_identities': identities,
    'general_results_in_written_proof': [
        'alpha,beta<0 if and only if the nonzero low-low entry d equals -1.',
        'alpha,beta>0 implies rT>(r+1)S and d<=-3; d=-2 is impossible.',
        'When d=-1, the larger high denominator has negative D and the smaller one has positive D.',
        'A high-support cycle whose every core has nonzero low-low entry -1 is impossible under opposing-D cancellation.',
    ],
    'exact_regression_models': models,
    'unbounded_positive_sum_family': {
        'parameter': 'Every integer H>=2.',
        'r': '2H', 'S=T': 'H', 's': '2H', 'z': '(2H+1)(H-1)',
        'a': '2H^2+1', 'b': 'H(H-1)(2H+1)+1',
        'alpha': '-H', 'beta': '-(H^2-1)',
        'D_A': '2H^3-2H^2-2H-1 > 0',
        'D_B': '-2H^3+3H^2+H+1 < 0',
        'high_defect_sum': 'H(H-1)>0',
        'positivity': 'The canonical explicit weights from td12:explicit-weights apply to every H>=2.',
        'verification': 'All row sums, crossings, displayed defects, and signs are polynomial identities or strictly positive coefficient expansions in H-2.',
    },
    'assumptions': [
        'The integer positive two-high standard form and the proven low-entry sign theorem.',
        'For the cycle corollary, every nonzero low-low entry equals -1 and opposing high D coefficients cancel.',
    ],
    'not_required': ['odd denominators', 'a denominator bound', 'puncture clutching', 'a node budget'],
    'limitations': [
        'The script checks algebra; inequalities and exhaustive case distinctions are proved in the source.',
        'The fixed direction chosen by a global labelling can be the zero low-low entry, so its sum does not force all nonzero entries to be -1.',
        'The maximum-denominator sign conclusion is restricted to nonzero low-low entry -1.',
    ],
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
output = here/'minimal_low_entry_verification_v12.json'
output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'passed': True, 'polynomial_identities': len(identities),
                  'exact_models': len(models), 'unbounded_families': 1,
                  'output': str(output)}))
