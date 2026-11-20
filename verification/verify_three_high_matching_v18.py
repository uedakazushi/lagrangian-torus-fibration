#!/usr/bin/env python3
"""Exact certificates for the unbounded three-high matching theorem.

The mathematical proof is in three_high_matching_v18.tex.  Coefficientwise
polynomial identities and explicit sign certificates are checked here.
The small fixed-input grid is a regression check, not the general proof.
Python standard library only.
"""
from pathlib import Path
from itertools import combinations, product
from fractions import Fraction
import argparse
import hashlib
import importlib.util
import json


class Poly:
    def __init__(self, terms=None):
        self.terms = {m:c for m,c in (terms or {}).items() if c}
    @classmethod
    def var(cls, name):
        return cls({(name,):1})
    @classmethod
    def coerce(cls, value):
        return value if isinstance(value,cls) else cls({():int(value)})
    def __add__(self, other):
        terms=self.terms.copy()
        for m,c in self.coerce(other).terms.items():
            terms[m]=terms.get(m,0)+c
        return Poly(terms)
    __radd__=__add__
    def __neg__(self):
        return Poly({m:-c for m,c in self.terms.items()})
    def __sub__(self, other):
        return self+(-self.coerce(other))
    def __rsub__(self, other):
        return self.coerce(other)-self
    def __mul__(self, other):
        terms={}
        for m,c in self.terms.items():
            for n,d in self.coerce(other).terms.items():
                mn=tuple(sorted(m+n))
                terms[mn]=terms.get(mn,0)+c*d
        return Poly(terms)
    __rmul__=__mul__
    def __eq__(self, other):
        return self.terms==self.coerce(other).terms
    def substitute(self, values):
        answer=Poly()
        for monomial,coefficient in self.terms.items():
            term=Poly.coerce(coefficient)
            for v in monomial:
                term=term*values.get(v,Poly.var(v))
            answer=answer+term
        return answer


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--bundle',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--source',type=Path)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('three_high_matching_verification_v18.json'))
    args=parser.parse_args()
    source=args.source or args.bundle/'paper/three_high_matching_v18.tex'
    helper=args.bundle/'research/exact_three_high_completion_v17.py'
    spec=importlib.util.spec_from_file_location('fixed_low',helper)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    identities=[]
    def check(name,left,right):
        assert left==right,name
        identities.append(name)

    # The same residual equation applies to both forbidden path types.
    a,b,d,B,C,k,L=map(Poly.var,'a b d B C k L'.split())
    cleared=k*(L+B)*(d+C*L)-a*(d+C*L)-b*L*(L+B)
    check('universal path residual',
          cleared,(k*C-b)*L*L+(k*d-a*C+B*(k*C-b))*L+d*(k*B-a))
    s,t,S,T,U=map(Poly.var,'s t S T U'.split())
    path_certificates=[]
    for kind,epsilon in [('P3_low_endpoint',-1),('P4_low_internal',1)]:
        u=s+t+epsilon
        q1,q2,q3=s*S+1,t*T+1,u*U+1
        a,b,d=q1*q2-1,q2*q3-1,q1*q3-1
        B,C,k=q1+epsilon*S,q3-epsilon*U,q2+epsilon*T
        leading=k*C-b
        constant=k*B-a
        middle_part=k*d-a*C
        check(kind+' leading',leading,epsilon*(U*(s*T-1)+T)+1)
        check(kind+' constant factor',constant,epsilon*(u*S*T+S+T)+1)
        check(kind+' middle component',middle_part,
              epsilon*(d*T+a*U)+q3-q2)
        # Shift all positive integer variables by one.  Every coefficient
        # of epsilon times each expression is nonnegative; the nonzero
        # constants for the latter two certify strictness.
        shifted={}
        substitutions={name:Poly.var(name)+1 for name in 's t S T U'.split()}
        for name,expression in [('leading',leading),('constant_factor',constant),
                                ('middle_component',middle_part)]:
            poly=(epsilon*expression).substitute(substitutions)
            assert all(c>0 for c in poly.terms.values())
            if name!='leading' or epsilon==1:
                assert poly.terms.get((),0)>0
            shifted[name]={'monomials':len(poly.terms),
                           'minimum_nonzero_coefficient':min(poly.terms.values()),
                           'constant_coefficient':poly.terms.get((),0),
                           'all_nonzero_coefficients_positive':True}
        path_certificates.append({'type':kind,'coefficient_sign':epsilon,
                                  'shifted_positive_polynomials':shifted})

    # Triangle: derive equations directly from the original pair products.
    alpha,beta,k=map(Poly.var,'alpha beta k'.split())
    u=s+t+1
    q1,q2,q3=s*S+1,t*T+1,u*U+1
    H,K=t*S+alpha,s*T+beta
    LL,NN=u*S+alpha+1,u*T+beta+1
    MM,OO=s*U-k,t*U+k+1
    A,b,C=s*alpha-t,s-t*beta,s+u*k
    E1=b*S-A*T-alpha*beta
    E2=(A-1)*U-C*S-k*(alpha+1)
    E3=(b+1)*U-(C+1)*T-(k+1)*(beta+1)
    check('triangle pair12 residual',H*K-(q1*q2-1),-E1)
    check('triangle pair13 residual',LL*MM-(q1*q3-1),E2)
    check('triangle pair23 residual',NN*OO-(q2*q3-1),-E3)
    F=A*(s*(1-U+T)-k*beta)-b*s*U-b*k*(s+t)-C*t*beta
    check('triangle integer-gap certificate',F,C*s*E1+b*s*E2-A*s*E3)

    # Check a nonpositive integer triangle.  This is an actual counterexample
    # to dropping positivity, not merely a necessary parameter pattern.
    q=(1,5,19,31)
    P=[[0,1,1,-3],[4,0,2,-11],[18,47,0,-84],[-10,-14,-7,0]]
    assert all(sum(P[i])==-q[i] for i in range(4))
    assert all(P[i][j]*P[j][i]==q[i]*q[j]-1 for i,j in combinations(range(4),2))
    gain=Fraction(P[0][2]*P[2][1]*P[1][0],q[0]*q[2]*q[1])
    assert gain==Fraction(188,95)>1
    assert not module.positive_cycle_test(P,q)[0]

    # Fixed low row and column reconstruction uses the previously verified
    # exact quadratic, retaining physical labels.  This finite regression
    # grid is explicitly not an exhaustive classification of denominators.
    tested=0
    chart_count=0
    counts={'matching_positive':0,'triangle_nonpositive':0}
    signatures={}
    for ss,tt in product(range(1,6),repeat=2):
        for r in [(-ss,-tt,ss+tt-1),(ss,tt,-ss-tt-1)]:
            for magnitudes in product(range(1,13),repeat=3):
                x=tuple(v if a>0 else -v for a,v in zip(r,magnitudes))
                if any(a*b%2 for a,b in zip(r,x)):
                    continue
                tested+=1
                for sol in module.complete_three_high(r,x,False):
                    chart_count+=1
                    pp=sol['P']
                    edges=[(i,j) for i,j in combinations(range(4),2) if pp[i][j]>0]
                    deg=tuple(sum(i in e for e in edges) for i in range(4))
                    matching=deg==(1,1,1,1)
                    triangle=sorted(deg)==[0,2,2,2] and deg[0]==2
                    assert matching or triangle,(r,x,pp)
                    assert sol['positive']==matching,(r,x,pp)
                    key='matching_positive' if matching else 'triangle_nonpositive'
                    counts[key]+=1
                    signatures.setdefault(key,{'r':r,'x':x,'q':sol['q'],'P':pp})
    assert all(counts.values()),counts
    report={
        'version':'v18','status':'PASS',
        'theorem_scope':'All positive integer three-high local charts with q0=1; no denominator cutoff, global clutching, D cancellation, or node conditions.',
        'proof':'The TeX proof eliminates paths by coefficient signs and positive triangles by an integer-gap identity. The finite regression grid is not the proof.',
        'polynomial_identities':identities,
        'identity_count':len(identities),
        'path_sign_certificates':path_certificates,
        'triangle_integer_gap':{
            'alpha_beta_nonnegative':'Strict positive three-cycle inequalities and integrality.',
            'A_gt_1_b_gt_0':'Second, then first pair equations.',
            'U_gt_T':'(A-1)U >= CS >= bS = AT+alpha beta >= AT.',
            'delta_ge_1':'U,T are integers.',
            'contradiction':'Left side A[s(1-delta)-k beta] <=0; right side bsU+bk(s+t)+Ct beta >0.'
        },
        'nonpositive_triangle':{'q':q,'P':P,'cycle':[0,2,1],'gain':[gain.numerator,gain.denominator]},
        'regression_grid':{'inputs':tested,'integer_charts':chart_count,
                           'counts':counts,'representatives':signatures,
                           'scope':'s,t=1..5, |x_i|=1..12, even r_i*x_i only; not a denominator classification.'},
        'source_sha256':sha(source),
        'helper_sha256':sha(helper),
        'verifier_sha256':sha(Path(__file__)),
    }
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','identities':len(identities),
                      'regression_inputs':tested,'integer_charts':chart_count,
                      'counts':counts,'output':str(args.output)},ensure_ascii=False))


if __name__=='__main__':
    main()
