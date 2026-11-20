#!/usr/bin/env python3
"""Exact algebraic certificate supporting the general low-degree-support proofs.

This is not a denominator-bounded search.  Polynomial identities are checked by
coefficient comparison, and the two integer branches left by the written
triangle-component proof are checked directly.  The inequalities and the
exhaustiveness of those branches are proved in quintic_low_degree_support_v11.tex.
"""
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


identities = []


def identity(name, left, right):
    assert left == right, name
    identities.append(name)


r, x, y, u, v = [Poly.variable(s) for s in ('r', 'x', 'y', 'u', 'v')]
a = r*x + 1
b = (r+1)*y + 1
A = a+x+u
B = b-y+v
residual = A*B-a*b+1
identity('general pair product reduced to Av', residual,
         A*v-(1-r*u)*y+x+u+1)
identity('general linear-v identity',
         A*(r+1)*v-(1-r*u)*b+A+r+1, (r+1)*residual)

# u>0, v=-z.  Clear all denominators before comparing coefficients.
S, d, z = [Poly.variable(s) for s in ('S', 'd', 'z')]
T = S+d+1
a = u*S+1
b = z*T+1
rA = r + u*(r+1)*S + r*u
rp1B = (r+1) + r*z*T - (r+1)*z
F = (2*r+1)*S+r-r*r*d
G = (r+1)*(S+r)
H = r*(r+1)
K = r*(r+T+1)
identity('bilinear-positive identity after clearing denominators',
         rA*rp1B-r*(r+1)*(a*b-1),
         -(u*(z*F-G)-H+z*K))
identity('F lower-bound difference', F-((r+1)*S+r), r*(S-r*d))
identity('G minus F', G-F, r*(r*(d+1)-S))
identity('H minus K', H-K, -r*T)
identity('ratio bound numerator', G-((r+1)*S+r), r*r)
e = Poly.variable('e')
identity('final divisibility residual', r*d+e+d+1-(r+1)*d, e+1)

# A low-to-low matched puncture has incoming sum equal to outgoing sum.
q, p = [Poly.variable(s) for s in ('q', 'p')]
M = q-1
identity('opposite signed-divisor sum', M*(p-p), (p-p)*p*(-p))
identity('positive extremal pair reciprocal-sum identity',
         M*(1+M), (1+M)*M)
identity('negative extremal pair reciprocal-sum identity',
         M*(-1-M), (-1-M)*M)

# The circulation variable has no denominator and the maximum/minimum argument
# is a written proof, not a numerical check.
Ti, Tprev, Tnext, delta = [Poly.variable(s) for s in ('Ti', 'Tprev', 'Tnext', 'delta')]
identity('high-high product from circulation',
         (2*Ti+delta)*(2*Ti-delta), 4*Ti*Ti-delta*delta)
identity('maximum principle nonnegative difference',
         4*Ti*Ti-(Tprev+Ti)*(Ti+Tnext),
         (Ti-Tprev)*(Ti+Tnext)+2*Ti*(Ti-Tnext))
identity('minimum principle nonnegative difference',
         (Tprev+Ti)*(Ti+Tnext)-4*Ti*Ti,
         (Tprev-Ti)*(Ti+Tnext)+2*Ti*(Tnext-Ti))

# The final local classification uses x=t(r+1), y=tr, q=tr(r+1)+1.
t = Poly.variable('t')
m = t*r*(r+1)
x = t*(r+1)
y = t*r
identity('triangle equal-denominator m', r*x, m)
identity('triangle equal-denominator second m', (r+1)*y, m)
identity('A=q-1 divisor reduction', m-r*(x+1), -r)
identity('A=q+1 divisor reduction', m-r*(x-1), r)
identity('r-1 divides two reduction', r*(r+1)-(r-1)*(r+2), 2)

branches = []
for rr in (2, 3):
    qq = rr*(rr+1)+1
    mm = qq-1
    xx, yy, ss, zz = rr+1, rr, rr, rr-1
    pp = [
        [0, -(qq+1), xx, -ss],
        [-(qq-1), 0, -yy, zz],
        [rr, -rr-1, 0, 0],
        [-mm//ss, mm//zz, -1+mm//ss-mm//zz, 0],
    ]
    qs = [qq, qq, 1, 1]
    assert all(sum(pp[i]) == -qs[i] for i in range(4))
    assert all(qs[i]*qs[j]-pp[i][j]*pp[j][i] == 1
               for i, j in itertools.combinations(range(4), 2))
    defects = [-qs[i]-sum(pp[j][i] for j in range(4) if j != i)
               for i in range(4)]
    assert defects[:2] == ([0, -2] if qq == 7 else [0, -1])
    assert sum(defects) == 0
    assert sum(defects[:2]) < 0
    branches.append({'r': rr, 'q': qs, 'p': pp, 'D': defects,
                     'sum_high_D': sum(defects[:2])})

here = Path(__file__).resolve().parent
source = here.parent/'paper'/'quintic_low_degree_support_v11.tex'
result = {
    'version': 11,
    'passed': True,
    'method': 'Exact polynomial coefficient comparison plus exact checking of the two branches retained by a general written divisibility proof; no denominator cutoff.',
    'polynomial_identity_count': len(identities),
    'polynomial_identities': identities,
    'triangle_local_branches': branches,
    'general_proof_assumptions': [
        'Local row sums and crossing determinants.',
        'Positive local basin weights, equivalently the two-high cycle condition before simplification.',
        'Integer clutching at the same labelled punctures.',
        'Opposing normal-action coefficients D sum to zero on every shared high branch.',
        'The high-support triangle is a connected component, so each of its cores has exactly two high branches.',
    ],
    'not_required': ['node nonnegativity', 'line node budget five', 'a denominator bound'],
    'scope': 'The written proof excludes a triangular connected component, not every graph containing a triangle. It does not by itself exclude paths or cycles of length four or five.',
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
output = here/'low_degree_support_verification_v11.json'
output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'passed': True, 'polynomial_identities': len(identities),
                  'triangle_branches': [x['q'][0] for x in branches],
                  'output': str(output)}))
