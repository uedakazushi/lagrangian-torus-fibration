#!/usr/bin/env python3
"""v25 exact degenerate divisor identities and fixed-b reconstruction.
Only the proved fixed-b sector a=0,x>=1 is reconstructed. No unbounded
nonexistence claim follows from finitely many input b values.
Standard library only; no previous verification program is imported or run.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
NAMES=('s','u','b','F','ell','T','y','h','R','L')
DIM=len(NAMES)

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


def coefficient_checks():
    s,u,b,F,ell,T,y,h,R,L=[VARIABLES[n] for n in NAMES]
    B=b-1; t=u-s+1; A=B*s-b; m=F*F+F+1
    aa=u*h-B*(F+1); Q=R*m-(h*A+b)*F-b*b+s*h
    LL=(F+1)*R-h*A; M=u*R-B*A
    C=F*(b*(t-1)+s)+b*b*t+b*s-b
    SS=F*T-B*(t-y)-ell; alpha=F+t*(ell-u)+u*y
    rr=-(s+t*b)*SS+(s*alpha-t)*T-alpha*b
    records=[]
    def check(name,left,right):
        assert not (left-right).c, (name,(left-right).c)
        records.append({'name':name,'status':'PASS','left_monomials':len(left.c),'right_monomials':len(right.c)})
    check('hM_minus_BL',h*M-B*LL,R*aa)
    check('FL_identity_before_R_substitution',F*LL-b*F-s*(T-h),Q+b*b-s*T-R)
    check('strict_positive_slope_identity',m*M-C,u*Q+(F*A-s)*aa)
    check('original_pair_product_factorization',rr,
          ((u*(b*b-s*T)-B*A)*(t-y)-t*T)+(s*ell-b*F)*(t*T+1))
    check('h_ge_b_gap',(s-b)*b-(s-1),(b-1)*(s-b-1))
    return records


def fixed_b(b):
    if not isinstance(b,int) or b<2:raise ValueError('b must be an integer >=2')
    counts={'s_x_pairs':0,'noncoprime_pairs':0,'T_L_candidates':0,'integral_F':0,
            'integral_degenerate_data':0,'scale_equation':0,'integer_y':0}
    models=[]; B=b-1
    for s in range(b+1,b*b):
        for x in range(1,(s-1)//b+1):
            counts['s_x_pairs']+=1
            h=s-x;g=gcd(h,B);A=B*s-b
            assert h>=b
            if g==1:continue
            counts['noncoprime_pairs']+=1
            for T in range(1,min(b-2,(b*b-1)//s)+1):
                R=b*b-s*T
                for L in range(h//g,B+1,h//g):
                    assert B*L%h==0
                    M=B*L//h
                    if M<T:continue
                    counts['T_L_candidates']+=1
                    fn=s*(h-T);fd=b-L
                    assert fn>0 and fd>0
                    if fn%fd:continue
                    F=fn//fd;counts['integral_F']+=1
                    if B*(F+1)%h or b*F%s:continue
                    u=B*(F+1)//h;ell=b*F//s;t=u-s+1;z=ell-u
                    if t<1 or z<0 or F!=B+u*x+s*z:continue
                    counts['integral_degenerate_data']+=1
                    if L!=(F+1)*R-h*A:continue
                    counts['scale_equation']+=1
                    assert M==u*R-B*A and M>0
                    if t*T%M:continue
                    y=t-t*T//M
                    if y<0:continue
                    counts['integer_y']+=1
                    result=original_model(s,t,x,y,z,b)
                    assert result['a']==0 and result['scales'][1]==T
                    assert result['original_residual']==0
                    if result['model']:models.append(result)
    return {'b':b,**counts,'models':models,
            'scope':'All a=0,x>=1 nonnegative-high-D canonical models for this fixed b; no bound on all b.'}

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

def clean(value):
    if isinstance(value,Fraction):
        return value.numerator if value.denominator==1 else f'{value.numerator}/{value.denominator}'
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v) for v in value]
    return value


def main():
    parser=argparse.ArgumentParser();here=Path(__file__).resolve().parent
    options=[here/'degenerate_divisor_reduction_v25.tex',here.parent/'papers/sections/paper/degenerate_divisor_reduction_v25.tex']
    parser.add_argument('--proof',type=Path,default=next((p for p in options if p.exists()),options[0]))
    parser.add_argument('--output',type=Path,default=here/'degenerate_divisor_verification_v25.json')
    parser.add_argument('--fixed-b',nargs='+',type=int,default=list(range(2,21)))
    args=parser.parse_args();checks=coefficient_checks()
    fixed=[fixed_b(b) for b in args.fixed_b]
    # Valid scale data need not satisfy the original pair equation.
    false=original_model(3,138,0,0,4,16)
    s,t,x,y,z,b=false['parameters'];B=b-1;u=s+t-1;h=s-x
    T=false['scales'][1];R=b*b-s*T;A=B*s-b;M=u*R-B*A
    assert false['original_residual']==M*(t-y)-t*T==5658
    assert not false['model']
    out={'version':'v25','status':'PASS','coefficient_identity_count':len(checks),
         'coefficient_identities':checks,
         'new_unbounded_exclusion':'a=0, h>=b, gcd(h,b-1)=1; in particular applies to x>=1',
         'proved_positive_divisor_relations':['hM=BL','Mj=tT','1<=L<=b-1 if h>=b','T<=M<=b-2 if h>=b'],
         'fixed_b_reconstructions':fixed,
         'regression_original_residual_retained':false,
         'general_degenerate_nonexistence_claim':False,
         'fixed_b_scan_is_not_global_proof':True,
         'earlier_verifier_imported':False,'old_fixed_s_scan_rerun':False,
         'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'proof_file':str(args.proof),'proof_sha256':sha256(args.proof.read_bytes()).hexdigest(),
         'dependencies':'Python standard library only','external_peer_review':False,'proof_assistant_formalization':False}
    args.output.write_text(json.dumps(clean(out),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','identities':len(checks),'input_b_count':len(fixed),
                      'models':sum(len(r['models']) for r in fixed)},ensure_ascii=False))
if __name__=='__main__':main()
