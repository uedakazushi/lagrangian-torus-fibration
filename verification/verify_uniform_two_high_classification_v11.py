#!/usr/bin/env python3
"""Exact certificates for the complete positive equal-two-high classification.

Uses only the standard library and the polynomial implementation supplied in
verify_equal_two_high_negativity_v11.py.  The classification proof is general;
the final parameter sample is only an additional consistency check.
"""
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from verify_equal_two_high_negativity_v11 import polynomial_ring, lmn, positive_divisors


def main():
    checks=[]
    def check(condition,label):
        if not condition:raise AssertionError(label)
        checks.append(label)

    _,(H,t,K)=polynomial_ring('H t K')
    L=(H+1)**2-4*H*t
    check(((H-1)*K+1)**2-((t-1)*K+1)*(4*H*K+1)
          ==K*(L*K-t-2*H-1),'LK identity from the two exact squares')
    _,(t,k)=polynomial_ring('t k')
    H=4*t-2+k
    check((H+1)**2-4*H*t==1+(4*t-2)*k+k*k,
          'L after H=4t-2+k')
    check(t+2*H+1==9*t-3+2*k,'numerator in the integer K formula')
    _,(u,v)=polynomial_ring('u v')
    t=u+1;k=v+3
    difference=k*k+(4*t-4)*k-9*t+4
    check(difference==4+3*u+6*v+v*v+4*u*v,
          'positive-coefficient exclusion for every t>=1,k>=3')
    _,(t,)=polynomial_ring('t')
    check((9*t+1)-(8*t+1)==t and 2*(8*t+1)-(9*t+1)==7*t+1,
          'k=2 ratio strictly between one and two')
    check((9*t-1)-2*(4*t)==t-1,'k=1 permits t=1 only')

    # Infinite family: the whole numerator matrix, not just its denominator.
    r=6*t-3;R=r*(r+1);m=t*R;q=m+1;s=3*t;z=3*t-1
    S=(2*t-1)*(6*t-2);Z=6*t*(2*t-1);x=t*(6*t-2);y=t*(6*t-3)
    A=q+x-s;B=q-y+z;H=Z-S
    check(m==s*S and m==z*Z,'symbolic divisibility of both s and z for every t')
    check(s*z+(1+t*r*r)*s-(1+t*(r+1)**2)*z==t+1,'infinite family conic identity')
    check(H==4*t-2,'infinite family reciprocal difference')
    P=[[0,-A,x,-s],[-B,0,-y,z],[r,-r-1,0,0],[-S,Z,-H-1,0]]
    denominators=[q,q,1,1]
    for i in range(4):
        check(sum(P[i])==-denominators[i],f'infinite family row sum {i}')
        for j in range(i+1,4):
            check(denominators[i]*denominators[j]-P[i][j]*P[j][i]==1,
                  f'infinite family crossing determinant {i},{j}')
    expected=[2*(3*t-2)*(t-1),-(3*t-2)*(2*t-1),3*t-2,0]
    for i in range(4):
        check(-denominators[i]-sum(P[j][i] for j in range(4))==expected[i],
              f'infinite family defect {i}')

    # Exact finite eliminations used after the general negativity theorem.
    check(lmn(2,1,1)[0]==-4,'delta=2,J=1 begins below zero')
    check(lmn(3,2,1)[0]==16 and lmn(3,2,2)[0]==-26,
          'delta=3,J=2 requires G=1')
    L,M,N=lmn(3,2,1)
    common=gcd(gcd(abs(L),abs(M)),abs(N))
    check((L//common,-M//common,-N//common)==(4,-23,-6),
          'delta=3,J=2 residual factor (R-6)(4R+1)')

    explicit=[]
    for r,t,s,z in [(2,1,2,1),(1,6,4,1),(2,5,6,3)]:
        m=t*r*(r+1);q=m+1;S=m//s;Z=m//z;x=m//r;y=m//(r+1)
        A=q+x-s;B=q-y+z;H=Z-S
        P=[[0,-A,x,-s],[-B,0,-y,z],[r,-r-1,0,0],[-S,Z,-H-1,0]]
        qs=[q,q,1,1]
        w=[Fraction(q),Fraction(q),Fraction(x)+Fraction(1,2*r),Fraction(z)+Fraction(1,2*Z)]
        check(m%s==0 and m%z==0 and s*z+(1+t*r*r)*s-(1+t*(r+1)**2)*z==t+1,
              f'sporadic data q={q}')
        check(all(sum(P[i])==-qs[i] for i in range(4)) and
              all(qs[i]*qs[j]-P[i][j]*P[j][i]==1 for i in range(4) for j in range(i+1,4)),
              f'sporadic rows and determinants q={q}')
        check(all(w[j]-w[i]*Fraction(P[i][j],qs[i])>0 for i in range(4) for j in range(4) if i!=j),
              f'explicit positive rational weights q={q}')
        D=[-qs[i]-sum(P[j][i] for j in range(4)) for i in range(4)]
        explicit.append({'r':r,'t':t,'s':s,'z':z,'q':q,'P':P,'weights':list(map(str,w)),'D':D})

    # Complete sample in parameter boxes, not the unbounded proof.
    observed=[];predicted=[]
    for r in range(1,81):
      for t in range(1,41):
        m=t*r*(r+1);A0=1+t*r*r;B0=1+t*(r+1)**2
        for s in positive_divisors(m):
            numerator=A0*s-t-1;denominator=B0-s
            if numerator<=0 or numerator%denominator:continue
            z=numerator//denominator
            if m%z:continue
            observed.append((r,t,s,z))
    for data in [(2,1,2,1),(1,6,4,1),(2,5,6,3)]:
        if data[0]<=80 and data[1]<=40:predicted.append(data)
    for t in range(1,41):
        if 6*t-3<=80:predicted.append((6*t-3,t,3*t,3*t-1))
    check(sorted(observed)==sorted(predicted),'all sample solutions agree with the complete classification')

    result={'version':11,'status':'passed','check_count':len(checks),'checks':checks,
            'scope':'Exact identities for the unbounded classification, finite residual algebra, and explicit positive weights. The parameter box is supplementary only.',
            'sporadic_models':explicit,'sample_parameter_box':{'r':[1,80],'t':[1,40]},
            'sample_solution_count':len(observed),'sample_solutions':observed,
            'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'polynomial_dependency_sha256':sha256(Path(__file__).with_name('verify_equal_two_high_negativity_v11.py').read_bytes()).hexdigest()}
    out=Path(__file__).with_name('uniform_two_high_classification_verification_v11.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'passed','check_count':len(checks),'sample_solution_count':len(observed),'output':str(out)},indent=2))


if __name__=='__main__':main()
