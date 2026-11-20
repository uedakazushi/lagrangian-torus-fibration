#!/usr/bin/env python3
"""Exact v24 positive-axis and exceptional-degenerate obstructions.

The unbounded conclusions are proved in the accompanying TeX. This program
checks polynomial identities coefficient by coefficient, recomputes Sylvester
determinants, and verifies complete shifted-coefficient sign certificates.
The optional fixed-s reconstruction has a proved bound and no t,D,q cutoff.
No older verification program is imported or executed. Standard library only.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
import json
from math import isqrt
from pathlib import Path

NAMES = ('s', 'c', 'L', 'w', 'y', 'B', 'z', 'p', 't', 'M', 'v')
DIM = len(NAMES)


class Polynomial:
    def __init__(self, value=0):
        if isinstance(value, Polynomial):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {a: b for a, b in value.items() if b}
        else:
            self.c = {(0,)*DIM: value} if value else {}
    def __add__(self, other):
        out = defaultdict(int, self.c)
        for a, b in Polynomial(other).c.items():
            out[a] += b
        return Polynomial(out)
    __radd__ = __add__
    def __neg__(self):
        return Polynomial({a: -b for a, b in self.c.items()})
    def __sub__(self, other):
        return self + -Polynomial(other)
    def __rsub__(self, other):
        return Polynomial(other) + -self
    def __mul__(self, other):
        out = defaultdict(int)
        for a, b in self.c.items():
            for x, y in Polynomial(other).c.items():
                out[tuple(i+j for i, j in zip(a, x))] += b*y
        return Polynomial(out)
    __rmul__ = __mul__
    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError('Nonnegative integer powers only')
        result = Polynomial(1)
        for _ in range(n):
            result *= self
        return result
    def substitute(self, values):
        values = {NAMES.index(k): Polynomial(v) for k, v in values.items()}
        out = Polynomial()
        for exps, coeff in self.c.items():
            term = Polynomial(coeff)
            for i, power in enumerate(exps):
                if power:
                    term *= values.get(i, VARIABLES[NAMES[i]])**power
            out += term
        return out


VARIABLES = {name: Polynomial({tuple(int(i == j) for i in range(DIM)): 1})
             for j, name in enumerate(NAMES)}


def determinant(matrix):
    n = len(matrix)
    answer = Polynomial()
    for perm in permutations(range(n)):
        sign = (-1)**sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        term = Polynomial(sign)
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        answer += term
    return answer


def resultant(f, g):
    """Sylvester determinant, coefficients in descending degree order."""
    m, n = len(f)-1, len(g)-1
    rows = []
    for i in range(n):
        rows.append([0]*i + list(f) + [0]*(n-1-i))
    for i in range(m):
        rows.append([0]*i + list(g) + [0]*(m-1-i))
    return determinant(rows)


def coefficient_checks():
    records = []
    def check(name, left, right=0):
        left, right = Polynomial(left), Polynomial(right)
        assert not (left-right).c, (name, (left-right).c)
        records.append({'name': name, 'status': 'PASS',
                        'left_monomials': len(left.c), 'right_monomials': len(right.c)})
    s, c, L, w, y, B, z, p, t, M, v = [VARIABLES[n] for n in NAMES]

    # Remaining positive axis: the original residual is retained.
    b, F = B+1, B+z
    m, C = F*F+F+1, F+2
    S, T = (F+1)*p-z-1, t+z+1-F*p
    alpha = t*(z+1)+F
    r = -(1+t*b)*S+(alpha-t)*T-alpha*b
    Q = (z-1)*(t-1)-m*p+F*(z+2)
    R = t-B*(p+z+1)
    N, K = b*b+b*z+z*z, (z+1)*F+1
    check('axis_original_residual', r, (t+1)*Q+t*R-B*C)
    check('axis_linear_elimination', B*Q, m*R+B*C*K-N*t)
    check('axis_remainder_three', m, C*(F-1)+3)
    check('axis_integer_divisor', R*R+B*R*(p+z+1)-B*C, t*R-B*C)
    check('axis_z1_gap', ((B+1)**2+(B+1)+1)-3*(B+1), B*B)
    check('axis_elimination_after_common_root',
          B*R*Q+N*(t*R-B*C), m*R*R-B*C*(N-R*K))

    # Exceptional degenerate branch: all expressions remain over Z.
    K0 = s*s-s+1
    bb, ff = s*c+1, s*L
    uu, tt = c*(s*L+1), c*s*L+c-s+1
    zz, ell = L-c, bb*L
    TT = c*(s*c+2)
    SS = (s*c-1)*L+s*c*(s-c-1+y)
    aa = uu*(y+zz)+s*c+zz
    rr = -(s+tt*bb)*SS+(s*aa-tt)*TT-aa*bb
    ww = L+1-c*K0
    DD = s*(ww+c)+1
    QQ = s*L*ww-s*c*c+s-2*c
    check('degenerate_a_zero', uu*s, s*c*(ff+1))
    check('degenerate_ell', ell, uu+zz)
    check('degenerate_R_one', s*TT, bb*bb-1)
    check('degenerate_S', SS, ff*TT-s*c*(tt-y)-ell)
    check('degenerate_original_residual', rr, c*(tt*(s*ww-1)-DD*y))
    check('degenerate_scale_polynomial', ff*ff+ff+1-(bb*K0-s*s)*ff-bb*bb+s*s, s*QQ)

    LL = c*K0+w-1
    t0 = c*s*LL+c-s+1
    Q0 = s*LL*w-s*c*c+s-2*c
    D0 = s*(w+c)+1
    As = s*s*K0*c*c+s*(s-1)**2*c-(s*s+s+1)
    Gs = s*s*(s-1)*c*c-s*c-s+1
    Hs = (s*c+2)*Gs
    check('degenerate_Q_mod_D', s*Q0+As, D0*(c*s*s*(s-1)+s*w-s-1))
    check('degenerate_residual_mod_D', t0*(s*w-1)+Hs,
          D0*(c*c*s*s*(s-1)+c*s*w-c*s-c-s+1))
    check('degenerate_offset_equation', Q0,
          s*(w*w-w+1)-c*(s*(c-K0*w)+2))

    af = [s*s*K0, s*(s-1)**2, -(s*s+s+1)]
    gf = [s*s*(s-1), -s, 1-s]
    linear = [s, 2]
    hf = [s*gf[0], 2*gf[0]+s*gf[1], 2*gf[1]+s*gf[2], 2*gf[2]]
    Cs = K0*((s-1)**4+3)
    check('Sylvester_resultant_linear', resultant(af, linear), s*s*K0)
    check('Sylvester_resultant_quadratic', resultant(af, gf), -s**6*((s-1)**4+3))
    check('Sylvester_resultant_cubic', resultant(af, hf), -s**8*Cs)
    check('cofactor_upper_gap', s*s*(K0+1)**2-Cs,
          3*s**4*(s-2)+10*s*s*(s-1)+8*s-4)
    quad = s*K0*c*c+(2-s*(M*(K0-2)+1))*c-s*(M*(M-1)+1)
    check('kappa_quadratic', Q0.substitute({'w': M-c}), -quad)

    # Clear the denominator 4 before computing the discriminant.
    beta4 = 8-(Cs-4)*(K0-2)-4*s
    disc16 = beta4*beta4+4*K0*(Cs-4)**2-16*s*K0*(Cs-4)+64*s*s*K0
    P = s**8-6*s**7+17*s**6-30*s**5+41*s**4-44*s**3+34*s*s-20*s-2
    W = 2*s**7-13*s**6+34*s**5-73*s**4+100*s**3-106*s*s+68*s-15
    G = 2*P-1-4*W
    check('discriminant_between_squares', disc16, P*P-4*W)
    wc = [609,6324,8934,5652,1967,394,43,2,0]
    gc = [26135,42152,34636,19704,8134,2316,422,44,2]
    check('positive_W_shift', W.substitute({'s':v+4}), sum(a*v**i for i,a in enumerate(wc)))
    check('positive_square_gap_shift', G.substitute({'s':v+4}), sum(a*v**i for i,a in enumerate(gc)))
    assert all(a >= 0 for a in wc+gc) and wc[0] > 0 and gc[0] > 0
    return records, {'shift': 'v=s-4>=0', 'W_coefficients_ascending': wc,
                     'gap_coefficients_ascending': gc, 'all_nonnegative': True,
                     'both_constants_positive': True}


def positive_integer_roots(a, b, c):
    assert a > 0
    D = b*b-4*a*c
    if D < 0:
        return []
    d = isqrt(D)
    if d*d != D:
        return []
    return sorted({n//(2*a) for n in {-b-d, -b+d} if n > 0 and n%(2*a) == 0})


def original_model(s,t,x,y,z,b):
    """Recompute original rows, products and weights, without old imports."""
    B,u,d,h,j = b-1,s+t-1,x+y+z,s-x,t-y
    ell,lam,mu = u+z,u*x+s*z,u*y+t*z
    F=B+lam;m=F*F+F+1
    E,J = mu*h-ell-j,h+ell-lam*j
    S=Fraction(h)+Fraction(F*E-J,m)
    T=Fraction(j)+Fraction(E+(F+1)*J,m)
    U=S+T+d-1
    alpha,k=u*d+B+z,s*d+B-x
    q=[1+s*S,1+t*T,1+u*U,Fraction(1)]
    P=[[0,t*S+alpha,-(u*S+alpha+1),-S],
       [s*T-b,0,-(u*T-b+1),-T],
       [-(s*U-k),-(t*U+k+1),0,U],[-s,-t,u,0]]
    rows=[sum(P[i])+q[i] for i in range(4)]
    pairs=[P[i][j]*P[j][i]-q[i]*q[j]+1 for i in range(4) for j in range(i+1,4)]
    Ds=[-q[i]-sum(P[j][i] for j in range(4)) for i in range(4)]
    r=-(s+t*b)*S+(s*alpha-t)*T-alpha*b
    signs=[t*S+alpha,s*T-b,u*S+alpha+1,u*T-b+1,s*U-k,t*U+k+1]
    assert rows == [0]*4 and Ds == [x,y,z,-d]
    assert [pairs[0],pairs[1],pairs[3]] == [r]*3
    assert [pairs[2],pairs[4],pairs[5]] == [0]*3
    answer={'parameters':[s,t,x,y,z,b], 'scales':[S,T,U], 'q':q,
            'pair_residuals':pairs, 'original_residual':r, 'D':Ds,
            'sign_factors':signs, 'a':u*h-B*(F+1),
            'single_congruence':(F*E-J)%m==0}
    answer['model']=bool(d>=1 and h>=1 and alpha>=k>=b+1
        and all(v.denominator == 1 for v in [S,T,U])
        and min(S,T,U,*signs)>0 and r==0)
    if answer['model']:
        weights=[q[0],signs[0]+Fraction(1,2)/signs[1],u+Fraction(1,2)/U,Fraction(1)]
        gaps=[weights[j]-Fraction(P[i][j],q[i])*weights[i]
              for i in range(4) for j in range(4) if i!=j]
        assert min(gaps)>0 and all(v==0 for v in pairs)
        answer.update(P=P,weights=weights,basin_gaps=gaps)
    return answer


def degenerate_fixed_s(s):
    """All degenerate nonnegative-D models for a specified positive integer s.

    Uses the proved exceptional-branch exclusion. This does not bound s.
    """
    if not isinstance(s,int) or s<1:
        raise ValueError('s must be a positive integer')
    if s<=2:
        return {'s':s,'models':[], 'reason':'v23 complete s<=2 obstruction', 'quadratics':0,
                'integer_F_roots':0,'integral_reconstructions':0,'nonnegative_integer_y':0}
    counts={'quadratics':0,'integer_F_roots':0,'integral_reconstructions':0,'nonnegative_integer_y':0}
    models=[]
    for x in range(s):
        h=s-x;K0=h*(s-1)+1
        bmax=(s-1)//x if x else 1+s*s*(s-1)**2
        for b in range(2,bmax+1):
            B=b-1
            for R0 in range(1 if x else 2,K0+1):
                if h*(s-1)*(R0-1)%B:
                    continue
                counts['quadratics']+=1
                roots=positive_integer_roots(R0,R0-b*K0+s*h,R0-b*b+s*h)
                for F in roots:
                    if F<B:continue
                    counts['integer_F_roots']+=1
                    un,eln,Tn=B*(F+1),b*F,b*b-R0
                    if un%h or eln%s or Tn%s:continue
                    u,ell,T=un//h,eln//s,Tn//s
                    t,z=u-s+1,ell-u
                    if t<1 or z<0 or T<1:continue
                    if F!=B+u*x+s*z:continue
                    counts['integral_reconstructions']+=1
                    S0=F*T-B*t-ell;alpha0=F+t*z
                    H,K=s+t*b,s*T-b
                    rho=B*H-u*K
                    assert rho>0, (s,t,x,z,b,F,R0,rho)
                    r0=-H*S0+(s*alpha0-t)*T-alpha0*b
                    if r0<0 or r0%rho:continue
                    y=r0//rho
                    counts['nonnegative_integer_y']+=1
                    model=original_model(s,t,x,y,z,b)
                    assert model['a']==0 and model['scales'][1]==T
                    assert model['original_residual']==0
                    if model['model']:
                        models.append(model)
    return {'s':s,'models':models,'proved_b_upper':1+s*s*(s-1)**2,**counts,
            'scope':'All remaining integers and denominators for this fixed s on a=0; s itself unbounded.'}


def clean(value):
    if isinstance(value,Fraction):
        return value.numerator if value.denominator==1 else f'{value.numerator}/{value.denominator}'
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v) for v in value]
    return value


def main():
    parser=argparse.ArgumentParser()
    here=Path(__file__).resolve().parent
    possible=[here/'high_d_axis_and_degenerate_obstruction_v24.tex',
              here.parent/'papers/sections/paper/high_d_axis_and_degenerate_obstruction_v24.tex']
    parser.add_argument('--proof',type=Path,default=next((p for p in possible if p.exists()),possible[0]))
    parser.add_argument('--output',type=Path,default=here/'high_d_axis_degenerate_verification_v24.json')
    parser.add_argument('--fixed-s',nargs='+',type=int,default=[3,4,5])
    args=parser.parse_args()
    identities,positive=coefficient_checks()
    false_candidate=original_model(3,138,0,0,4,16)
    assert false_candidate['a']==0 and false_candidate['original_residual']==5658
    assert false_candidate['scales']==[54,84,141]
    assert false_candidate['single_congruence'] and min(false_candidate['sign_factors'])>0
    assert not false_candidate['model']
    mixed=original_model(1,2,-1,1,3,2)
    assert mixed['original_residual']==0 and min(mixed['sign_factors'])>0
    assert mixed['q']==[5,11,23,1]
    fixed=[degenerate_fixed_s(s) for s in args.fixed_s]
    out={'version':'v24','status':'PASS','coefficient_identity_count':len(identities),
         'coefficient_identities':identities,'positive_coefficient_certificate':positive,
         'complete_unbounded_exclusions':['delta=1,x=0','a=0,x=0,R0=1'],
         'combined_with_v23':'All delta=1 excluded; all a=0 models finitely reconstructible after fixing s.',
         'exceptional_divisor_bound':'D | (s^2-s+1)((s-1)^4+3)',
         'degenerate_b_bound':'2 <= b <= 1+s^2(s-1)^2 for s>=3',
         'fixed_s_reconstructions':fixed,
         'regressions':[{'name':'positive_scale_degenerate_false_candidate_requires_original_residual','data':false_candidate},
                        {'name':'genuine_mixed_D_model_not_in_excluded_hypotheses','data':mixed}],
         'old_144_low_row_scan_rerun':False,'earlier_verifier_imported':False,
         'bounded_regression_not_used_as_unbounded_proof':True,
         'general_nonnegative_D_nonexistence_claim':False,
         'general_degenerate_nonexistence_claim':False,
         'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'proof_file':str(args.proof),'proof_sha256':sha256(args.proof.read_bytes()).hexdigest(),
         'dependencies':'Python standard library only',
         'external_peer_review':False,'proof_assistant_formalization':False}
    args.output.write_text(json.dumps(clean(out),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','identities':len(identities),
                      'fixed_s':[{'s':d['s'],'quadratics':d['quadratics'],'models':len(d['models'])} for d in fixed]},ensure_ascii=False))


if __name__=='__main__':main()
