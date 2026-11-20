#!/usr/bin/env python3
"""Independent review checks for unit-edge triangles and the four-ray sign theorem.
No import or execution of either producer's verifier. Exact arithmetic only.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import isqrt
import json


def signed_divisors(n):
    assert n
    return sorted({sgn*d for a in range(1,isqrt(abs(n))+1) if n%a==0
                   for d in (a,abs(n)//a) for sgn in (-1,1)})


def negative_table():
    all_rows=[]; cases=[]
    for s in range(1,4):
        for t in range(1,5-s):
            for A,B in product(range(1,5),repeat=2):
                c=s*t*(A*B-1)-s*A-t*B+1
                d=s*(A*B-1)-B; e=t*(A*B-1)-A;f=A*B
                determinant=d*e-c*f
                rows=[]
                if c==0:
                    assert d>=0 and e>=0 and f>0
                    method='positive affine expression'
                elif determinant==0:
                    assert c>0 and d>=0 and e>=0
                    method='two positive factors cannot multiply to zero'
                else:
                    method='all signed divisors of d*e-c*f'
                    for u in signed_divisors(determinant):
                        v=determinant//u
                        if (u-e)%c or (v-d)%c:continue
                        S=(u-e)//c;T=(v-d)//c
                        if min(S,T)<=0 or s*S%2 or t*T%2:continue
                        assert (((-s*A+1)*S-A)*((-t*B+1)*T-B)
                                ==(s*S+1)*(t*T+1)-1)
                        rows.append((s,t,-A,-B,S,T,s*S+1,t*T+1))
                all_rows.extend(rows)
                cases.append({'s':s,'s_prime':t,'A':A,'B':B,'coefficients':[c,d,e,f],
                              'factor_product':determinant,'method':method,'solutions':rows})
    expected=[(1,2,-1,-3,2,1,3,3),(1,2,-2,-1,2,1,3,3),
              (2,1,-1,-2,1,2,3,3),(2,1,-3,-1,1,2,3,3),
              (1,3,-2,-1,2,2,3,7),(3,1,-1,-2,2,2,7,3),
              (2,2,-1,-2,3,1,7,3),(2,2,-1,-2,2,2,5,5),
              (2,2,-2,-1,2,2,5,5),(2,2,-2,-1,1,3,3,7)]
    assert len(cases)==96 and sorted(all_rows)==sorted(expected)
    return cases,all_rows


def listed_opposite(n,u,j,a,b,U,T):
    normal=(n==0 and a==b==1 and T==U-1 and u>=2 and U>=2 and (u-U)%2!=0)
    normal|=(n==1 and a==b==1 and U==1 and u%2==0)
    normal|=(n==1 and a==b==-1 and T==1 and u%2==0)
    normal|=(n==2 and a==b==-1 and T==U+1 and (u-U)%2!=0)
    small=(n==0 and u==2 and j==1 and a==0 and b==-3 and U==T and U%2==0)
    small|=(n==1 and u==1 and j==1 and a==0 and b==-2 and U==T and U%2==0)
    small|=(n==1 and u==j==2 and a==0 and b==-3 and U==T==1)
    small|=(n==1 and u==j==1 and a in (-2,-4) and b==-1 and T==-a and U%2==0)
    return normal or small


def opposite_regression():
    tested=0;solutions=0
    for n in range(3):
        for u in range(1,13):
            j=u+n-1
            if j<1:continue
            for U,T in product(range(1,25),repeat=2):
                if u*U%2 or j*T%2:continue
                for a,b in product(range(-4,2),repeat=2):
                    left=((u*a-1)*U+a)*((j*b+1)*T+b)
                    actual=left==(u*U+1)*(j*T+1)-1
                    listed=listed_opposite(n,u,j,a,b,U,T)
                    assert actual==listed,(n,u,j,a,b,U,T)
                    tested+=1;solutions+=actual
    return {'parameter_boxes':{'u':[1,12],'U':[1,24],'T':[1,24]},
            'exact_odd_denominator_cases':tested,'matching_solutions':solutions,
            'role':'bounded regression only; the infinite families were independently checked by hand in the accompanying review'}


def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items():out[e]=out.get(e,0)+c
    return {e:c for e,c in out.items() if c}


def scale(p,c):return {e:a*c for e,a in p.items() if a*c}


def multiply(p,q):
    out={}
    for e,c in p.items():
        for f,d in q.items():
            g=tuple(a+b for a,b in zip(e,f));out[g]=out.get(g,0)+c*d
    return {e:c for e,c in out.items() if c}


def all_negative_witness():
    A={(1,0):1};K={(0,1):1};C=scale(add(A,K),-1)
    lhs=add(multiply(add(scale(A,-2),scale(K,-2)),add(scale(C,-1),scale(K,-2))),
            scale(multiply(A,C),-8))
    rhs=scale(multiply(add(scale(A,3),K),add(A,K)),2)
    assert lhs==rhs
    return {'cleared_identity':'AC*((-2-2K/A)*(-1-2K/C)-8)=2*(3A+K)*(A+K), C=-K-A',
            'coefficients':[(list(e),c) for e,c in sorted(lhs.items())],
            'K_mod_3':1,'zero_C_branch_excluded':True,'nonintegral_A_branch_excluded':True}


def four_ray():
    counts=Counter();cert=[]
    vertices=range(4);edges=list(combinations(vertices,2))
    for subset in product((False,True),repeat=6):
        chosen=[e for e,flag in zip(edges,subset) if flag]
        degree=[sum(i in e for e in chosen) for i in vertices]
        if any(d not in (1,2) for d in degree):continue
        code=tuple(sorted(degree));counts[str(code)]+=1
        assert code in [(1,1,1,1),(1,1,2,2),(2,2,2,2)]
    assert sorted(counts.values())==[3,3,12]
    for nxt in product(*[tuple(j for j in range(3) if j!=i) for i in range(3)]):
        seen={};path=[];v=0
        while v not in seen:
            seen[v]=len(path);path.append(v);v=nxt[v]
        cyc=path[seen[v]:];balance=[0]*3
        for i in cyc:balance[i]-=1;balance[nxt[i]]+=1
        assert balance==[0]*3 and len(cyc) in (2,3)
        cert.append({'successors':nxt,'cycle':cyc,'telescoping_balance':balance})
    # Integer-gap identity checked via an independently chosen exact rational fixture.
    qh=13;qi=7;c=(2,5,6);i=0;pih=-Fraction(qi*qh-1,c[i]);pij=Fraction(9,2)
    pik=-qi-pih-pij
    gaps=[qi*c[1]-c[0]*pij,qi*c[2]-c[0]*pik]
    assert sum(gaps)==1
    return {'all_64_graphs_classified':True,'degree_sequence_counts':dict(counts),
            'all_eight_outgoing_maps':cert,'independent_gap_fixture':[str(g) for g in gaps],
            'proof_review':'Integer gap sum=1; directed selection contradicts strict basin cycle condition. Degree<=2, no isolated vertex leaves 2K2/P4/C4; C4 violates one negative pair product. Forest converse by positive rational intervals.'}


def main():
    here=Path(__file__).resolve().parent
    work=here.parent
    paths=[work/'g514/unit_three_high_triangle_reduction_v24.tex',
           work/'g514/verify_unit_three_high_triangles_v24.py',
           work/'root/four_ray_positive_graph_v24.tex',
           work/'root/verify_four_ray_positive_graph_v24.py']
    if not all(p.exists() for p in paths):
        base=here.parent.parent
        paths=[base/'paper/unit_three_high_triangle_reduction_v24.tex',
               base/'verification/verify_unit_three_high_triangles_v24.py',
               base/'paper/four_ray_positive_graph_v24.tex',
               base/'verification/verify_four_ray_positive_graph_v24.py']
    cases,table=negative_table()
    result={'version':'v24','status':'PASS','reviewer':'highd_proportional_v24',
            'scope':'Independent full read-through of both proofs, exact complete negative-triangle divisor enumeration, all-negative witness factor, graph and cycle checks. Opposite-family numerical cases are regression only.',
            'producer_code_imported_or_executed':False,'negative_signed_cases':len(cases),
            'negative_solution_rows':table,'all_negative_case_certificates':cases,
            'opposite_family_regression':opposite_regression(),'all_negative_witness':all_negative_witness(),
            'four_ray':four_ray(),'source_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in paths},
            'review_script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'mathematical_issues':[],'external_peer_review':False,'proof_assistant_formalization':False}
    output=here/'local_signs_and_unit_triangles_independent_review_v24.json'
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','negative_cases':len(cases),'negative_rows':len(table),
                      'opposite_regression_cases':result['opposite_family_regression']['exact_odd_denominator_cases'],
                      'four_ray_graphs':64,'outgoing_maps':8}))

if __name__=='__main__':main()
