#!/usr/bin/env python3
"""Exact algebraic certificate for the arbitrary two-high defect theorem.

This script uses only the Python standard library.  Every symbolic check is a
coefficient comparison of polynomials; denominators are cleared explicitly.
The unbounded inequalities and exhaustive sign cases are a written proof in
quintic_two_high_defect_v12.tex, not a numerical search.  The five local models
are regression examples, not evidence replacing that proof.
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


# First promote the v11 notes-only low-low-entry sign calculation.
r, s, z, S, T = variables('r', 's', 'z', 'S', 'T')
a, b = s*S+1, z*T+1
R = r*(r+1)
K = (r+1)*(r+1)*S-r*r*T-R
rA = r+s*(r+1)*S-r*s
rp1B = r+1+r*z*T+(r+1)*z
low_expression = R+s*(r+1)*(S-r)+z*r*(r+1-T)+s*z*K
identity('low-low entry pair-product identity',
         rA*rp1B-R*(a*b-1), low_expression)
identity('K rewritten with d=S-T-1', K,
         (2*r+1)*S+r*r*(S-T-1)-r)
identity('low-entry branch T>r+1 comparison',
         K-r*(T-r-1), (r+1)*((r+1)*S-r*T))
identity('low-entry branch S<r comparison',
         K-T*(r-S), (r+1)*((r+1)*S-r*T-r)+S*T)
identity('strict low-entry comparison from S>=T+1',
         (r+1)*S-r*T-r-(T+1), (r+1)*(S-T-1))

# Free alpha,beta,M,N capture all of the determinant/defect identities.
alpha, beta, M, N, h, k = variables('alpha', 'beta', 'M', 'N', 'h', 'k')
delta = alpha-beta
a, b = M+r*alpha, N+(r+1)*beta
A, B = a+alpha, b-beta
L = M-N+r*delta
bezout = M*beta-N*alpha
identity('pair product becomes the Bezout identity',
         a*b-A*B, bezout)
identity('alpha L minus a delta is the Bezout residual',
         alpha*L-a*delta, bezout)
identity('beta(L+delta) minus b delta is the Bezout residual',
         beta*(L+delta)-b*delta, bezout)
identity('B-a equals -L', B-a, -L)
identity('A-b equals L+delta', A-b, L+delta)
identity('sum of high defects', (B-a+h)+(A-b-k), h-k+delta)

# Substitute alpha=sh/r and beta=zk/(r+1), clearing r(r+1).
cleared_bezout = r*(r*s+1)*z*k-(r+1)*((r+1)*z+1)*s*h
cleared_delta = (r+1)*s*h-r*z*k
identity('sign-ratio identity after clearing r(r+1)',
         cleared_bezout+cleared_delta,
         s*z*(r*r*k-(r+1)*(r+1)*h))
identity('positive branch ratio strictness',
         r*r*(k-h)-(2*r+1)*h,
         r*r*k-(r+1)*(r+1)*h)
identity('positive branch first rational gap numerator',
         h*h*(s*(r+h)+1)-s*h*h*(r+h), h*h)
identity('positive branch second rational gap numerator',
         h*(r+h)-h*h, r*h)

# Negative alpha,beta branch: alpha=-c,beta=-e,h=-H,k=-K.
H, Kn, w, c, dd, E = variables('H', 'Kn', 'w', 'c', 'delta', 'E')
E_numerator = (r+1)*(r+1)*H-r*r*Kn
identity('negative-branch comparison K<=H',
         E_numerator-(2*r+1)*Kn, (r+1)*(r+1)*(H-Kn))
identity('negative-branch reduction K=H+1, r=H+w',
         (H+w+1)*(H+w+1)*H-(H+w)*(H+w)*(H+1),
         H*(H+1)-w*w)
identity('negative-branch coprime determinant factor at delta zero',
         M*(-c)-N*(-c), c*(N-M))
identity('E<1/2 has a uniformly positive numerator for c>=2',
         c*(c+dd)-2*(dd+1), (c-2)*(c+dd+2)+2)
identity('negative-branch U after clearing Hc',
         H+((H+w)*c*w+H)*dd,
         H*c*w*dd+c*w*w*dd+H*(dd+1))

# Here w^2=H(H+1)(1-E), a relation established in the written proof.
w_square = H*(H+1)*(1-E)
identity('negative-branch D_B using E after clearing Hc',
         H*c*(H+1+dd)-H*c*w*dd-c*w_square*dd-H*(dd+1),
         H*c*((H+1)*(1-dd+dd*E)+dd*(1-w))-H*(dd+1))
identity('delta>=2 coefficient strictness decomposition',
         2*c*(c+dd)*(1-dd)+2*dd*(dd+1),
         c*(c+dd)*(2-dd)-dd*(c*(c+dd)-2*(dd+1)))
identity('delta=1 final defect after clearing c(c+1)',
         2*(H+1)+c*(c+1)*(1-w)-2*(c+1),
         c*(c+1)*(1-w)+2*(H-c))
identity('delta=1 upper bound gap for H>=c>=2',
         c*(c+1)*(H-2)-6*(H-c),
         (c-2)*((H-c)*(c+3)+c*(c+1)))
identity('delta=1 square lower bound for c>=2',
         c*(c+1)-6, (c-2)*(c+3))
identity('delta=1 final strict square comparison',
         6*H*(H+1)-(H+1)*(H+1), (H+1)*(5*H-1))

# The explicit positive basin weights have fixed margins.
x = Poly.variable('x')
identity('A to C basin margin after clearing 2r',
         2*r*x+1-2*r*x, 1)
identity('C to A basin margin after clearing 2',
         2*(r*x+1)-2*r*x-1, 1)
identity('B to D basin margin after clearing 2T',
         2*T*z+1-2*T*z, 1)
identity('D to B basin margin after clearing 2',
         2*(T*z+1)-2*T*z-1, 1)


def local_model(name, aa, bb, rr, ss, zz):
    """Construct a prescribed standard-form model and check it exactly."""
    assert min(aa, bb) > 1
    assert min(rr, ss, zz) > 0
    assert (aa-1) % rr == (aa-1) % ss == 0
    assert (bb-1) % (rr+1) == (bb-1) % zz == 0
    xx, yy = (aa-1)//rr, (bb-1)//(rr+1)
    SS, TT = (aa-1)//ss, (bb-1)//zz
    AA, BB = aa+xx-ss, bb-yy+zz
    pp = [[0, -AA, xx, -ss], [-BB, 0, -yy, zz],
          [rr, -rr-1, 0, 0], [-SS, TT, SS-TT-1, 0]]
    qs = [aa, bb, 1, 1]
    assert all(sum(pp[i]) == -qs[i] for i in range(4))
    assert all(qs[i]*qs[j]-pp[i][j]*pp[j][i] == 1
               for i, j in itertools.combinations(range(4), 2))
    ww = [Fraction(aa), Fraction(bb),
          Fraction(xx)+Fraction(1, 2*rr), Fraction(zz)+Fraction(1, 2*TT)]
    basin = [[None if i == j else ww[j]-ww[i]*Fraction(pp[i][j], qs[i])
              for j in range(4)] for i in range(4)]
    assert all(basin[i][j] > 0 for i in range(4)
               for j in range(4) if i != j)
    assert [basin[0][2], basin[2][0], basin[1][3], basin[3][1]] == [
        Fraction(1, 2*rr), Fraction(1, 2), Fraction(1, 2*TT), Fraction(1, 2)]
    defects = [-qs[i]-sum(pp[j][i] for j in range(4) if j != i)
               for i in range(4)]
    assert sum(defects) == 0
    assert min(defects[:2]) < 0
    assert SS <= TT
    hh, kk = SS-rr, TT-rr-1
    al, be = xx-ss, yy-zz
    de = al-be
    MM, NN = rr*ss+1, (rr+1)*zz+1
    LL = MM-NN+rr*de
    assert al*be > 0 and hh*kk > 0
    assert MM*be-NN*al == 1
    assert al*LL == 1+aa*de
    assert defects[:2] == [hh-LL, LL+de-kk]
    if de >= 0 and al < 0:
        assert SS == TT
        assert defects[1] < 0
    return {
        'name': name, 'q': qs, 'p': pp, 'D': defects,
        'r': rr, 's': ss, 'z': zz, 'S': SS, 'T': TT,
        'alpha': al, 'beta': be, 'delta': de,
        'weights': [str(wi) for wi in ww],
        'basins': [[None if entry is None else str(entry) for entry in row]
                   for row in basin],
    }


models = [
    local_model('positive alpha, delta negative', 3, 7, 1, 1, 1),
    local_model('positive alpha, delta zero; zero high coefficient', 7, 7, 2, 2, 1),
    local_model('positive alpha, delta positive; D_A negative', 31, 31, 2, 6, 3),
    local_model('negative alpha, delta one; positive high-coefficient sum', 9, 11, 4, 4, 5),
    local_model('largest denominator can have positive coefficient', 19, 17, 3, 2, 1),
]
assert models[3]['D'][:2] == [3, -1]
assert models[4]['D'][:2] == [1, -6]

here = Path(__file__).resolve().parent
source_candidates = [here/'quintic_two_high_defect_v12.tex',
                     here.parent/'paper'/'quintic_two_high_defect_v12.tex']
source = next((path for path in source_candidates if path.is_file()), None)
if source is None:
    raise FileNotFoundError('quintic_two_high_defect_v12.tex')
result = {
    'version': 12,
    'passed': True,
    'method': 'Exact polynomial coefficient comparison and Fraction arithmetic. No denominator cutoff or enumeration is used.',
    'general_theorem': 'Every positive integer local model with q=(a,b,1,1), a,b>1, has min(D_A,D_B)<0.',
    'stronger_negative_branch': 'For alpha>=beta<0 the standard form has S=T and D_B<0.',
    'polynomial_identity_count': len(identities),
    'polynomial_identities': identities,
    'exact_regression_models': models,
    'proof_dependencies': [
        'Standard two-high numerator factorization.',
        'The general positivity/sign theorem u<0<v.',
        'Positive integer a,b>1 and all standard-form integrality constraints.',
    ],
    'proved_in_source': [
        'The low-low entry d=S-T-1 is negative.',
        'The displayed rational weights have positive basin areas.',
        'Alpha,beta,h,k are nonzero and have the same sign.',
        'The three sign/order cases are exhaustive, with unbounded inequalities in each.',
    ],
    'not_required': [
        'a=b', 'odd denominators', 'a denominator bound',
        'integer puncture clutching', 'node nonnegativity', 'a node budget',
        'opposing-end defect cancellation',
    ],
    'limitations': [
        'The script checks algebra, not the logical completeness of the written proof.',
        'A negative minimum does not imply that the sum of the two high coefficients is negative.',
        'The local theorem alone does not resolve arbitrary global high-denominator atlases.',
    ],
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
output = here/'two_high_defect_verification_v12.json'
output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'passed': True, 'polynomial_identities': len(identities),
                  'exact_local_models': len(models), 'output': str(output)}))
