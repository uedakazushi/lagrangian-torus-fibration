#!/usr/bin/env python3
"""Exact algebra checks for the positive L=3,4 sector lemma, v21.

Sparse rational coefficient identities and separately labelled matrix regressions.
The inequalities in the proof are analytical, not conclusions of a bounded scan.
Python standard library only; no denominator bound is assumed in the theorem.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

NAMES = ('r', 'h', 'd', 's', 'z', 'alpha', 'beta', 'j')
POLYDIM = len(NAMES)

class Poly:
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {k: Fraction(v) for k, v in value.items() if v}
        else:
            self.terms = {(0,) * POLYDIM: Fraction(value)} if value else {}

    def __add__(self, other):
        other = Poly(other)
        result = defaultdict(Fraction, self.terms)
        for key, value in other.terms.items():
            result[key] += value
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        other = Poly(other)
        result = defaultdict(Fraction)
        for key, value in self.terms.items():
            for key2, value2 in other.terms.items():
                result[tuple(a + b for a, b in zip(key, key2))] += value * value2
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert type(exponent) is int and exponent >= 0
        result = Poly(1)
        for _ in range(exponent):
            result = result * self
        return result


variables = {name: Poly({tuple(int(i == j) for j in range(POLYDIM)): 1})
             for i, name in enumerate(NAMES)}
r,h,d,s,z,alpha,beta,j = (variables[name] for name in NAMES)
identities=[]
def zero(name, polynomial):
    assert not Poly(polynomial).terms, name
    identities.append(name)

k=h+d; S=r+h; T=S+d+1
F=(2*r+1)*h-r*r*d
A=h*(r+1); B=-r*k; C=r*(r+1)
a=s*S+1; b=z*T+1
Unum=r*a+s*h; Vnum=(r+1)*b-z*k
zero('original_high_pair_equation', Unum*Vnum-r*(r+1)*(a*b-1)-(F*s*z+A*s+B*z+C))
zero('reverse_sign_equation_coefficient', r*r*k-(r+1)**2*h+F)
zero('reverse_slope_gap', r*k-(r+1)*h-(r*d-h))
M=r*s+1; N=(r+1)*z+1
zero('Bezout_after_auxiliary_substitution',
     (M+r*alpha)*beta-(N+(r+1)*beta)*alpha+alpha*beta-(M*beta-N*alpha))
zero('positive_F_growth_identity',
     M*(r*beta-(r+1)*alpha)
     -r*(M*beta-N*alpha)-(r*(r+1)*(z-s)-1)*alpha)
zero('j_squared_inequality', j*j-4*(j-1)-(j-2)**2)
zero('negative_F_E_lower_bound', -F-k-(r+1)*(d*(r-1)-2*h))
zero('denominator_difference',
     (M+r*alpha)-(N+(r+1)*beta)-(r*s-(r+1)*z+r*(alpha-beta)-beta))
zero('negative_F_growth_bound',
     F+h*k-(-d*r*r+2*h*r+h*(h+d+1)))
zero('d1_floor_bound_odd',
     (2*(2*j+1)+1)*j-(2*j+1)**2+(j+1))
zero('d1_floor_bound_even',
     (2*(2*j)+1)*j-(2*j)**2-j)
zero('d2_floor_bound',
     (2*r+1)*(r-1)-2*r*r+(r+1))


def check_model(parameters):
    rv,sv,zv,Sv,Tv=parameters
    av,bv=sv*Sv+1,zv*Tv+1
    assert (sv*Sv)%rv==0 and (zv*Tv)%(rv+1)==0
    xv,yv=sv*Sv//rv,zv*Tv//(rv+1)
    Lv=Tv-Sv+1
    Uv,Vv=av+xv-sv,bv-yv+zv
    q=[av,bv,1,1]
    P=[[0,-Uv,xv,-sv],[-Vv,0,-yv,zv],[rv,-rv-1,0,0],[-Sv,Tv,-Lv,0]]
    assert all(sum(P[i])==-q[i] for i in range(4))
    assert all(P[i][j]*P[j][i]==q[i]*q[j]-1 for i,j in combinations(range(4),2))
    DD=[-q[i]-sum(P[j][i] for j in range(4) if j!=i) for i in range(4)]
    weights=[Fraction(av),Fraction(bv),Fraction(xv)+Fraction(1,2*rv),Fraction(zv)+Fraction(1,2*Tv)]
    gaps=[weights[j]-Fraction(P[i][j],q[i])*weights[i] for i in range(4) for j in range(4) if i!=j]
    assert min(gaps)>0
    hv=Sv-rv; dv=Tv-Sv-1; Fv=(2*rv+1)*hv-rv*rv*dv
    assert dv in (1,2) and 0<hv<rv*dv and Fv
    alphav=xv-sv; betav=yv-zv
    assert alphav>0 and betav>0
    if Fv>0:
        assert sv<=zv and DD[3]<0<DD[2] and av<bv
    else:
        assert DD[3]>=0
        assert hv<= ((rv-1)//2 if dv==1 else rv-1)
        assert betav<=hv<rv
        if alphav==betav:
            assert parameters in ((2,2,1,3,6),(3,3,2,4,6)) and av==bv
        else:assert av>bv
    if DD[2]<=0:
        assert Fv<0 and av>bv
        assert Tv<= ((3*rv+3)//2 if dv==1 else 2*rv+2)
    return dict(parameters=list(parameters),q=q,P=P,D=DD,F=Fv,
                alpha=alphav,beta=betav,weights=list(map(str,weights)),
                basin_gaps=list(map(str,gaps)))

regressions=[check_model(p) for p in [
    (1,1,2,2,5),(2,2,6,3,5),(5,10,3,9,12),
    (6,6,3,11,14),(4,4,2,7,10),(2,2,1,3,6),(3,3,2,4,6)]]
script=Path(__file__).resolve()
proof=next(p for p in [script.with_name('positive_small_L_sector_v21.tex'),
                       script.parent.parent/'papers/sections/paper/positive_small_L_sector_v21.tex'] if p.is_file())
report=dict(version='v21',status='PASS',
    scope='All positive integer two-high models with T-S in {2,3}; no parity, node, clutching or denominator cutoff.',
    method='Exact sparse polynomial coefficient identities; explicit matrix regressions are separate.',
    polynomial_identities=len(identities),identity_names=identities,
    script_sha256=sha256(script.read_bytes()).hexdigest(),
    proof_file=proof.name,proof_sha256=sha256(proof.read_bytes()).hexdigest(),
    conclusions=dict(positive_F=['s<=z','D_D<0<D_C','a<b'],
                     negative_F=['D_D>=0','h<=floor((r-1)/2) if delta=2','h<=r-1 if delta=3',
                                 'a>b except the two equal-denominator base points'],
                     nonpositive_D_C=['F<0','a>b','T<=floor((3r+3)/2) if delta=2','T<=2r+2 if delta=3'],
                     book_nonzero_cycle='The three denominators to high vertex 0 are either all smaller or all larger than the corresponding denominators to high vertex 1.'),
    matrix_regressions=regressions,external_peer_review=False,proof_assistant_formalization=False)
output=script.with_name('positive_small_L_sector_verification_v21.json')
output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status='PASS',polynomial_identities=len(identities),matrix_regressions=len(regressions),output=str(output))))
