#!/usr/bin/env python3
"""Exact algebra and proof-derived finite cases for the G5_10 obstruction.

The proof is in g5_10_obstruction_v18.tex. There is no denominator cutoff.
The only finite enumeration here is of node budgets and of ordinary-case
parameters proved to satisfy r<=2, S<=3, delta<=3. The infinite negative
exception family is verified coefficientwise, then excluded by inequalities.
"""
from itertools import combinations, product
from math import isqrt
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


class Poly:
    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @classmethod
    def var(cls, name):
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
                mn = tuple(sorted(m + n))
                terms[mn] = terms.get(mn, 0) + c * d
        return Poly(terms)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms


def locate(name):
    for base in (HERE, HERE.parent):
        for folder in ('', 'paper', 'paper_arithmetic', 'verification'):
            p = base / folder / name
            if p.is_file():
                return p
    raise FileNotFoundError(name)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def node_triples(total=5):
    return [(a, b, total-a-b)
            for a in range(total+1) for b in range(total-a+1)]


def signed_divisors(n):
    values = set()
    for d in range(1, isqrt(n)+1):
        if n % d == 0:
            values.update((d, -d, n//d, -n//d))
    return sorted(values)


def matching_low_row(row):
    return sum(row) == -1 and all(row) and sum(x > 0 for x in row) == 1


def main():
    identities = []

    def identity(name, a, b):
        assert a == b, name
        identities.append(name)

    # An exhaustive node enumeration AFTER the displayed proof-derived bounds.
    ordinary = []
    for r in (1, 2):
        for S in range(r+1, 4):
            for delta in (2, 3):
                T = S + delta
                if r*T <= (r+1)*S:
                    continue
                for n, m in product(node_triples(), repeat=2):
                    R0 = (1-n[0], 1-r-n[1], r+2-n[2])
                    R1 = (delta+2-m[0], S+1-m[1], 1-T-m[2])
                    if (matching_low_row(R0) and matching_low_row(R1)
                            and R0[0] == -R1[0]):
                        ordinary.append({'r':r, 'S':S, 'T':T,
                                         'n04':n, 'n14':m, 'R0':R0, 'R1':R1})
    assert len(ordinary) == 2
    assert {(x['r'],x['S'],x['T']) for x in ordinary} == {(2,3,5)}
    assert {(x['R0'],x['R1']) for x in ordinary} == {
        ((1,-1,-1),(-1,4,-4)), ((-4,-1,4),(4,-1,-4))}

    u, v = map(Poly.var, ('u','v'))
    identity('Ordinary pair factorization',
             (7*u+1)*(13*v+1)-((6*u+1)*(15*v+1)-1),
             (u-2)*(v+1)+3)
    # Signed factors of -3, with u,v positive: this is the complete factor list.
    uv = []
    for left in signed_divisors(3):
        right = -3//left
        uu, vv = left+2, right-1
        if uu >= 1 and vv >= 1:
            uv.append((uu,vv))
    assert uv == [(1,2)]
    residues = [d for d in signed_divisors(30) if (d-27) % 31 == 0]
    assert residues == []

    # Exact polynomial form of E*alpha*beta=alpha-beta+1.
    r, h, s, z = map(Poly.var, ('r','h','s','z'))
    S, T = r+h, r+h+2
    a, b = s*S+1, z*T+1
    cleared_pair = (a*r+s*h)*(b*(r+1)-z*(h+1))-(a*b-1)*r*(r+1)
    cleared_E = (s*z*(r*r*(h+1)-(r+1)*(r+1)*h)
                 -s*h*(r+1)+z*(h+1)*r-r*(r+1))
    identity('Difference-two E equation from the original pair equation',
             cleared_pair, -cleared_E)
    identity('E=0 Euclidean obstruction',
             4*r*r-(2*r+1)*(2*r-1), 1)
    rr = z*(h+1)-1
    identity('beta=1 and E=1 factorization',
             rr*rr-(2*rr+1)*h-h*(h+1),
             (h+1)*((h+1)*z*(z-2)-h+1))
    t, w = map(Poly.var, ('t','w'))
    large_z = ((t+2)*(w+3)*(w+1)-(t+1)+1)
    assert all(c > 0 for c in large_z.terms.values())
    assert large_z.terms.get((), 0) == 6
    # Here h=1+t and z=3+w. The positive coefficients exclude all z>=3.

    # Universal symbolic resonance family: no sample values of alpha are used.
    alpha = Poly.var('alpha')
    qq = [12*alpha+1, 13, 1, 1]
    PP = [[0, -(13*alpha+1), 4*alpha, -3*alpha],
          [-12, 0, -3, 2],
          [3, -4, 0, 0],
          [-4, 6, -3, 0]]
    for i in range(4):
        identity(f'Resonance row {i} in order (2,3,0,1)',sum(PP[i]),-qq[i])
    for i,j in combinations(range(4),2):
        identity(f'Resonance pair {i},{j}',PP[i][j]*PP[j][i],qq[i]*qq[j]-1)
    DD = [-qq[i]-sum(PP[j][i] for j in range(4) if j!=i) for i in range(4)]
    expected_D = [12-12*alpha,13*alpha-14,5-4*alpha,3*alpha-3]
    for i in range(4):
        identity(f'Resonance D at ray {(2,3,0,1)[i]}',DD[i],expected_D[i])

    U,V,q = map(Poly.var,('U','V','q'))
    # D^4_1 = 3alpha-3 and D^1_4 = q-2-U+V.
    identity('D14 opposition gives U-V=3alpha+q-5',
             (q-2-U+V)+(3*alpha-3), 3*alpha+q-5-U+V)
    uu,vv = map(Poly.var,('u','v'))
    identity('D04 opposition gives u-v=4alpha-5',
             (uu-vv)+(5-4*alpha),uu-vv-4*alpha+5)
    parity = []
    for small_q in (3,5):
        for parity_alpha in (0,1):
            rhs_parity=(3*parity_alpha+small_q-5)%2
            parity.append({'q01':small_q,'alpha_mod2':parity_alpha,
                           'compatible_with_U_V_even':rhs_parity==0})
    assert [x['alpha_mod2'] for x in parity if x['compatible_with_U_V_even']] == [0,0]

    negative_profiles = []
    for small_q in (3,5):
        for n2 in range(6-small_q):
            n3=5-small_q-n2
            R0=(-(small_q-1),-2-n2,5-n3)
            assert matching_low_row(R0)
            negative_profiles.append({'q01':small_q,'n04':(small_q,n2,n3),'R0':R0})
    assert len(negative_profiles)==4

    # All four possible remaining node distributions on edge24. Signs hold
    # for every alpha>=2 and are certified coefficientwise after alpha=t+2.
    node24=[]
    for nu in range(4):
        first=(8-12*nu)*(t+2)+1-nu
        second=(12*nu-21)*(t+2)+nu-2
        def sign(poly):
            poly=Poly.coerce(poly)
            cs=list(poly.terms.values())
            if all(c<0 for c in cs) and poly.terms.get((),0)<0:return -1
            if all(c>0 for c in cs) and poly.terms.get((),0)>0:return 1
            raise AssertionError('A sign is not coefficientwise fixed')
        signs=(sign(first),sign(second))
        node24.append({'nodes':(nu,3-nu,2),'signs_p40_p41':signs,
                       'both_negative':signs==(-1,-1)})
    assert [x['nodes'] for x in node24 if x['both_negative']] == [(1,2,2)]
    M,N=map(Poly.var,('M','N'))
    D2=-(12*alpha+1)-(-M-N+12)
    identity('D24 opposition gives M+N=24alpha+1',
             D2+(12-12*alpha),M+N-24*alpha-1)
    q02,q12=map(Poly.var,('q02','q12'))
    identity('Strict lower bound for M',
             (12*alpha+1)*q02-1-4*alpha*3*q02,q02-1)
    identity('Strict lower bound for N',
             (12*alpha+1)*q12-1-(9*alpha+1)*q12,3*alpha*q12-1)
    identity('Final strict separation for all alpha>=2',
             39*alpha-20-(24*alpha+1),15*(alpha-2)+9)

    proof=locate('g5_10_obstruction_v18.tex')
    report={
        'version':'v18','status':'PASS',
        'theorem':'gten18:no-support',
        'scope':'G5_10 exact high support; positive integer local charts, clutching, nonnegative nodes and opposing D',
        'quantification':'All denominators; no denominator or matrix-entry cutoff',
        'matching_dependency':'mh18:matching',
        'ordinary_proof_derived_bounds':{'r_max':2,'S_max':3,'delta_max':3},
        'ordinary_node_cases':ordinary,'ordinary_factor_solutions_u_v':uv,
        'ordinary_model':{'r':2,'s':2,'z':6,'S':3,'T':5,'a':7,'b':31,'B':27},
        'signed_divisors_of_30':signed_divisors(30),
        'signed_divisors_30_congruent_27_mod31':residues,
        'positive_exception':'D04,D14 force s-z=1 and q12+q13=q01+2, contradicting odd denominators',
        'negative_exception_profiles':negative_profiles,
        'negative_family':'r3,S4,T6,z2,s3alpha,a12alpha+1,b13; all alpha>=1 symbolically checked',
        'negative_alpha_parity':parity,
        'negative_edge24_node_cases':node24,
        'final_inequality_certificate':'24alpha+1=M+N>3q02+q12>=39alpha-20=(24alpha+1)+15(alpha-2)+9; contradiction for alpha>=2',
        'polynomial_identities':identities,
        'polynomial_identity_count':len(identities),
        'large_z_exclusion_positive_coefficients':[
            {'monomial':list(m),'coefficient':c}for m,c in sorted(large_z.terms.items())],
        'limitations':'Finite checks verify the algebra and proof-derived cases; the full mathematical proof is in TeX and depends on the stated matching theorem.',
        'source_sha256':{proof.name:sha(proof),Path(__file__).name:sha(Path(__file__))},
    }
    output=HERE/'g5_10_obstruction_verification_v18.json'
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','polynomial_identity_count':len(identities),
                      'ordinary_node_cases':len(ordinary),'negative_profiles':len(negative_profiles),
                      'output':str(output)},ensure_ascii=False))


if __name__=='__main__':
    main()
