#!/usr/bin/env python3
"""Exact certificates for a unit edge between two positive three-high cores.

The unbounded opposite-sign classification is proved in the TeX source.
The bounded regression is explicitly supplementary. No old verifier is imported.
"""
from itertools import product
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json

NAMES = ('s','t','S','T','a','b','u','j','U','n','r','k')
ZERO = (0,)*len(NAMES)

class P:
    def __init__(self, data=0):
        self.d = ({ZERO:data} if data else {}) if isinstance(data,int) else {m:c for m,c in data.items() if c}
    @staticmethod
    def cast(x): return x if isinstance(x,P) else P(x)
    def __add__(self,other):
        d=dict(self.d)
        for m,c in self.cast(other).d.items():d[m]=d.get(m,0)+c
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({m:-c for m,c in self.d.items()})
    def __sub__(self,other):return self+-self.cast(other)
    def __rsub__(self,other):return self.cast(other)+-self
    def __mul__(self,other):
        d={}
        for m,c in self.d.items():
            for n,b in self.cast(other).d.items():
                key=tuple(x+y for x,y in zip(m,n));d[key]=d.get(key,0)+c*b
        return P(d)
    __rmul__=__mul__

def var(name):
    m=list(ZERO);m[NAMES.index(name)]=1
    return P({tuple(m):1})

def opposite(u,j,U,T,alpha,beta):
    return ((u*alpha-1)*U+alpha)*((j*beta+1)*T+beta)-(u*U+1)*(j*T+1)+1

def negative(s,t,S,T,alpha,beta):
    return ((s*alpha+1)*S+alpha)*((t*beta+1)*T+beta)-(s*S+1)*(t*T+1)+1

def divs(n):
    assert n
    out=set()
    for d in range(1,isqrt(abs(n))+1):
        if n%d==0:out.update((d,-d,abs(n)//d,-abs(n)//d))
    return sorted(out)

def prediction(n,u,U,T,alpha,beta):
    j=u+n-1
    if j<1 or u*U%2 or j*T%2:return []
    ans=[]
    if n==0 and alpha==beta==1 and T==U-1:ans.append('P0')
    if n==1 and alpha==beta==1 and U==1:ans.append('P1')
    if n==1 and alpha==beta==-1 and T==1:ans.append('N1')
    if n==2 and alpha==beta==-1 and T==U+1:ans.append('N2')
    if (n,u,alpha,beta)==(0,2,0,-3) and U==T and U%2==0:ans.append('E0')
    if (n,u,alpha,beta)==(1,1,0,-2) and U==T and U%2==0:ans.append('E1')
    if (n,u,U,T,alpha,beta)==(1,2,1,1,0,-3):ans.append('E2')
    if n==1 and u==1 and beta==-1 and T in (2,4) and alpha==-T and U%2==0:ans.append('E3')
    return ans

def main(proof,output):
    s,t,S,T,a,b,u,j,U,n,r,k=map(var,NAMES)
    identities=[]
    def check(name,left,right=0):
        difference=P.cast(left)-right
        assert not difference.d,name
        identities.append({'name':name,'all_coefficients_zero':True})
    C=s*t*(a*b-1)-s*a-t*b+1
    D=s*(a*b-1)-b
    E=t*(a*b-1)-a
    F=a*b
    check('both_negative_expansion',negative(s,t,S,T,-a,-b),C*S*T+D*S+E*T+F)
    check('division_free_bilinear_factorization',(C*S+E)*(C*T+D)-(D*E-C*F),C*(C*S*T+D*S+E*T+F))
    check('both_negative_positive_10',negative(s,t,S,T,1,0),(s+1-s*t)*S*T-s*S+(1-t)*T)
    check('both_negative_A1_s1',negative(1,t,S,T,-1,-b),-(t*T+1)*S+(t*(b-1)-1)*T+b)
    check('both_negative_A1_s2_B2',negative(2,t,S,T,-1,-2),-T*(S-t+1)+2)
    check('both_negative_A1_s3_B2',negative(3,1,S,T,-1,-2),-S*(T-1)+2)
    oc=u*j*(a*b-1)+j*b-u*a-1
    od=u*(a*b-1)+b
    oe=j*(a*b-1)-a
    check('opposite_negative_expansion',opposite(u,j,U,T,-a,-b),oc*U*T+od*U+oe*T+a*b)
    check('opposite_positive_11',opposite(u,u+n-1,U,T,1,1),-n*U*T-U+T+1)
    check('opposite_negative_11',opposite(u,u+n-1,U,T,-1,-1),(n-2)*U*T+U-T+1)
    check('opposite_A0',opposite(u,j,U,T,0,-b),T*((j*(b-u)-1)*U-j)+(b-u)*U)
    check('opposite_j1_B1',opposite(u,1,U,T,-a,-1),-T*(u*U+1)+(u*(a-1)+1)*U+a)
    check('ordinary_P0',opposite(u,u-1,U,U-1,1,1))
    check('ordinary_P1',opposite(u,u,1,T,1,1))
    check('ordinary_N1',opposite(u,u,U,1,-1,-1))
    check('ordinary_N2',opposite(u,u+1,U,U+1,-1,-1))
    check('exception_E0',opposite(2,1,2*r,2*r,0,-3))
    check('exception_E1',opposite(1,1,2*r,2*r,0,-2))
    check('exception_E2',opposite(2,2,1,1,0,-3))
    for kval in (2,4):check('exception_E3_k'+str(kval),opposite(1,1,2*r,kval,-kval,-1))
    check('negative_position_positive_family_1',negative(2,1,S,2,1,0))
    check('negative_position_positive_family_2',negative(1,2,2,T,0,1))
    K=6*r+1
    check('all_external_negative_local_obstruction',(-2*U-2*K)*(-1*(-K-U)-2*K)-8*U*(-K-U),2*(3*U+K)*(U+K))

    expected={
        (1,2,1,3):{(2,1)},(1,2,2,1):{(2,1)},
        (2,1,1,2):{(1,2)},(2,1,3,1):{(1,2)},
        (1,3,2,1):{(2,2)},(3,1,1,2):{(2,2)},
        (2,2,1,2):{(3,1),(2,2)},(2,2,2,1):{(1,3),(2,2)},
    }
    pairs=[(1,1),(1,2),(2,1),(1,3),(3,1),(2,2)]
    records=[]
    points=[]
    for sv,tv in pairs:
      for av,bv in product(range(1,5),repeat=2):
        C=sv*tv*(av*bv-1)-sv*av-tv*bv+1
        D=sv*(av*bv-1)-bv
        E=tv*(av*bv-1)-av
        F=av*bv
        N=D*E-C*F
        solutions=set()
        if not C:
            assert D>=0 and E>=0 and F>0
            method='nonnegative linear coefficients, positive constant'
        elif not N:
            fixed_S=-E//C if E%C==0 else None
            fixed_T=-D//C if D%C==0 else None
            assert fixed_S is None or fixed_S<=0 or sv*fixed_S%2==1
            assert fixed_T is None or fixed_T<=0 or tv*fixed_T%2==1
            method='zero factor product; both possible lines violate positivity or odd denominators'
        else:
            for x0 in divs(N):
                y0=N//x0
                if (x0-E)%C or (y0-D)%C:continue
                Sv,Tv=(x0-E)//C,(y0-D)//C
                if Sv>0 and Tv>0 and sv*Sv%2==0 and tv*Tv%2==0:
                    assert negative(sv,tv,Sv,Tv,-av,-bv)==0
                    solutions.add((Sv,Tv))
            method='all signed divisors of the nonzero exact factor product'
        assert solutions==expected.get((sv,tv,av,bv),set()),(sv,tv,av,bv,solutions)
        records.append({'s':sv,'s_prime':tv,'minus_alpha':av,'minus_beta':bv,
                        'coefficients':[C,D,E,F],'factor_constant':N,'method':method,
                        'all_positive_odd_denominator_solutions':sorted(solutions)})
        for Sv,Tv in solutions:
            points.append({'s':sv,'s_prime':tv,'alpha':-av,'beta':-bv,'S':Sv,'T':Tv,
                           'q':[sv*Sv+1,tv*Tv+1]})
    assert len(records)==96 and len(points)==10

    positive_records=[]
    for sv,tv in pairs:
      for alpha,beta in product((0,1),repeat=2):
        if alpha==beta==0:kind='strictly negative residual'
        elif alpha==beta==1:kind='strictly positive residual'
        elif alpha==1:
            if tv>=2:kind='strictly negative residual'
            elif sv%2:kind='forced T=s gives even high denominator'
            else:
                assert (sv,tv)==(2,1)
                kind='S arbitrary positive, T=2'
        else:
            if sv>=2:kind='strictly negative residual'
            elif tv%2:kind='forced S=s_prime gives even high denominator'
            else:
                assert (sv,tv)==(1,2)
                kind='S=2, T arbitrary positive'
        positive_records.append({'s':sv,'s_prime':tv,'alpha':alpha,'beta':beta,'classification':kind})
    assert len(positive_records)==24

    tested=0;valid=0;family_counts={key:0 for key in ['P0','P1','N1','N2','E0','E1','E2','E3']}
    for uv,nv,Uv,Tv in product(range(1,25),range(3),range(1,21),range(1,21)):
        jv=uv+nv-1
        if jv<1 or uv*Uv%2 or jv*Tv%2:continue
        for alpha,beta in product(range(-4,2),repeat=2):
            actual=opposite(uv,jv,Uv,Tv,alpha,beta)==0
            predicted=prediction(nv,uv,Uv,Tv,alpha,beta)
            assert actual==bool(predicted),(nv,uv,Uv,Tv,alpha,beta)
            assert len(predicted)<=1
            tested+=1
            if actual:
                valid+=1;family_counts[predicted[0]]+=1

    # An exact finite check of the structural node consequences, using the full tables.
    node_records=[]
    for sv,tv in pairs:
        available=any((x['s'],x['s_prime'])==(sv,tv) for x in points) or (sv,tv) in ((2,1),(1,2))
        if not available:continue
        common_node=1+sv+tv
        for na in range(5-common_node+1):
            nb=5-common_node-na
            assert sorted((na,nb,common_node)) in ([0,0,5],[0,1,4])
            node_records.append({'s':sv,'s_prime':tv,'nodes':[na,nb,common_node]})
    for x0 in points:
        q0,q1=x0['q']
        if x0['s']+x0['s_prime']==4:
            assert (q0,q1) in ((3,7),(5,5),(7,3)) and x0['S']+x0['T']==4
        else:assert q0==q1==3
    assert all((da+db==2)==(da==db==1) for da,db in product((0,1),repeat=2))
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    result={
        'version':'v24','status':'PASS',
        'scope':'Triangle necessary conditions across a unit edge joining two positive three-high cores; not a completed global model.',
        'polynomial_identity_count':len(identities),'polynomial_identities':identities,
        'complete_negative_sign_cases':96,'complete_negative_sign_results':records,
        'negative_sign_exact_points':points,'negative_sign_point_count':len(points),
        'complete_positive_sign_cases':24,'complete_positive_sign_results':positive_records,
        'positive_sign_unbounded_families':2,
        'opposite_sign_unbounded_classification':'Four ordinary families and four types of small exceptions, proved by integer/sign arguments in the TeX source.',
        'bounded_regression':{'u_range':[1,24],'U_T_range':[1,20],'node_range':[0,2],
            'tested_odd_denominator_tuples':tested,'solutions':valid,'family_counts':family_counts,
            'purpose':'Regression only; not an unbounded completeness proof.'},
        'unit_node_patterns':[[5,0,0],[4,1,0]],'unit_node_records':node_records,
        'five_node_adjacent_denominator_pairs':[[3,7],[5,5],[7,3]],
        'four_node_minimum_adjacent_denominator':3,
        'five_node_opposite_low_D_forces_two_positive_external_pairs':True,
        'at_least_one_positive_external_pair_for_any_unit_edge':True,
        'all_external_negative_case_forces_low_row':[-2,-1,2],
        'all_external_negative_case_forces_low_column':'(-1,-2,2r), r>=1',
        'all_external_negative_obstruction':'(3A+6r+1)(A+6r+1)=0; first root nonintegral modulo3, second makes another required nonzero entry vanish',
        'G5_14_five_node_cannot_be_at_four_high_core':True,
        'no_arbitrary_cutoff_in_complete_tables':True,
        'old_verifier_imports':False,'external_peer_review':False,'proof_assistant_formalization':False,
        'source_sha256':sha(Path(__file__)),'proof_file':proof.name,'proof_sha256':sha(proof),
    }
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','polynomial_identity_count','complete_negative_sign_cases',
                                           'negative_sign_point_count','complete_positive_sign_cases','unit_node_patterns']},ensure_ascii=False))

if __name__=='__main__':
    here=Path(__file__).resolve().parent
    default=here/'unit_three_high_triangle_reduction_v24.tex'
    if not default.is_file():default=here.parent/'paper'/default.name
    parser=argparse.ArgumentParser()
    parser.add_argument('--proof',type=Path,default=default)
    parser.add_argument('--output',type=Path,default=here/'unit_three_high_triangles_verification_v24.json')
    args=parser.parse_args()
    main(args.proof,args.output)
