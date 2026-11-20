#!/usr/bin/env python3
"""Exact verification of fixed-low three-high reconstruction.

General statements are proved in the accompanying TeX. Polynomial identities
are checked coefficientwise. The finite small-input grid is an implementation
cross-check against complete signed-divisor reconstruction for each fixed
input, not a classification at an arbitrary denominator bound.
"""
from pathlib import Path
from itertools import combinations, permutations, product
from math import isqrt
from fractions import Fraction
import hashlib
import importlib.util
import json

HERE=Path(__file__).resolve().parent


def locate(name):
    for base in (HERE,HERE.parent):
        for folder in ('','paper','notes','research','verification'):
            path=base/folder/name
            if path.is_file():
                return path
    raise FileNotFoundError(name)


HELPER=locate('exact_three_high_completion_v17.py')
spec=importlib.util.spec_from_file_location('fixed_low_completion',HELPER)
completion=importlib.util.module_from_spec(spec);spec.loader.exec_module(completion)


class Poly:
    def __init__(self, terms=None):
        self.terms={m:c for m,c in (terms or {}).items() if c}
    @classmethod
    def var(cls,name):return cls({(name,):1})
    @classmethod
    def coerce(cls,value):return value if isinstance(value,cls) else cls({():int(value)})
    def __add__(self,other):
        terms=self.terms.copy()
        for m,c in self.coerce(other).terms.items():terms[m]=terms.get(m,0)+c
        return Poly(terms)
    __radd__=__add__
    def __neg__(self):return Poly({m:-c for m,c in self.terms.items()})
    def __sub__(self,other):return self+(-self.coerce(other))
    def __rsub__(self,other):return self.coerce(other)-self
    def __mul__(self,other):
        terms={}
        for m,c in self.terms.items():
            for n,d in self.coerce(other).terms.items():
                mn=tuple(sorted(m+n));terms[mn]=terms.get(mn,0)+c*d
        return Poly(terms)
    __rmul__=__mul__
    def __eq__(self,other):return self.terms==self.coerce(other).terms


def signed_divisors(n):
    values=set()
    for a in range(1,isqrt(n)+1):
        if n%a==0:values.update((a,n//a,-a,-n//a))
    return sorted(values)


def independent_fixed_reconstruction(r,x):
    """Original-order signed divisors; no quadratic or permutation from helper."""
    q=[1+a*b for a,b in zip(r,x)]
    s=[-a-b for a,b in zip(q,x)]
    out=[]
    for A in signed_divisors(q[0]*q[1]-1):
        C=s[0]-A
        if not C or (q[0]*q[2]-1)%C:
            continue
        B=(q[0]*q[1]-1)//A;D=(q[0]*q[2]-1)//C
        E=s[1]-B;F=s[2]-D
        if E*F != q[1]*q[2]-1:
            continue
        P=[[0,*r],[x[0],0,A,C],[x[1],B,0,E],[x[2],D,F,0]]
        out.append(tuple(tuple(row) for row in P))
    return sorted(out)


def strict_positive(P,q):
    for length in (2,3,4):
        for cyc in permutations(range(4),length):
            edges=list(zip(cyc,cyc[1:]+cyc[:1]))
            if all(P[i][j]>0 for i,j in edges):
                if Fraction(prod(P[i][j] for i,j in edges),prod(q[i] for i,j in edges))>=1:
                    return False
    return True


def prod(values):
    answer=1
    for x in values:answer*=x
    return answer


def main():
    identities=[]
    def identity(name,a,b):
        assert a==b,name
        identities.append(name)
    s1,s2,s3,U,V,W,A=map(Poly.var,'s1 s2 s3 U V W A'.split())
    a=W-s2*s3;b=s2*(s3*s1-V)+U*s3-W*s1;c=-U*(s3*s1-V)
    phi=(s2*A-U)*(s3*(s1-A)-V)-W*A*(s1-A)
    identity('Cleared final pair equals the explicit quadratic',phi,a*A*A+b*A+c)
    C=s1*s2*s3-s1*W-s2*V-s3*U
    identity('Symmetric discriminant',b*b-4*a*c,C*C-4*U*V*W)
    h,v,P,z,t=map(Poly.var,'h v P z t'.split())
    q1,q2,q3=P+1,P-h+2,h*v+1
    ss1,ss2,ss3=-q1-1,-q2+1,-q3+v
    Q12,Q13,Q23=q1*q2-1,q1*q3-1,q2*q3-1
    AA=ss1-t
    phi_tail=(ss2*AA-Q12)*(ss3*(ss1-AA)-Q13)-Q23*AA*(ss1-AA)
    At=v*t*t+2*(h*v+1)*t+(h-1)*(h*v+1)
    Bt=v*t*t+(v*(h+1)+1-h)*t+h*v*(h-1)
    identity('Opposite-exception tail is linear in P',phi_tail,P*At+Bt)
    Az=v*z*z-2*(h*v+1)*z+(h-1)*(h*v+1)
    Bz=v*z*z-(v*(h+1)+1-h)*z+h*v*(h-1)
    identity('Tail difference excludes resonance',Bz-Az,((h-1)*v+h+1)*z-(h-1))
    endpoint=2*h+2
    identity('Proved endpoint for the negative high entry',v*endpoint*endpoint-2*(h*v+1)*endpoint+(h-1)*(h*v+1),
             (v-1)*(h*h+3*h+4)+(h*h-1))
    identity('Tail B is positive past the endpoint',Bz,v*z*(z-h-1)+(h-1)*z+h*v*(h-1))
    identity('The small forbidden core is a sum of squares',24*(6*A*A+17*A+14),(12*A+17)*(12*A+17)+47)

    grid=[];count_by_completions={0:0,1:0,2:0}
    for r in product((-3,-2,-1,1,2,3),repeat=3):
        if sum(r)!=-1:continue
        for magnitudes in product(range(1,4),repeat=3):
            x=tuple((1 if a>0 else -1)*b for a,b in zip(r,magnitudes))
            expected=independent_fixed_reconstruction(r,x)
            actual=completion.complete_three_high(r,x,False)
            normalized=sorted(tuple(tuple(row) for row in sol['P']) for sol in actual)
            assert normalized==expected,(r,x)
            for sol in actual:
                assert sol['positive']==strict_positive(sol['P'],sol['q'])
            positive=completion.complete_three_high(r,x,True)
            assert len(positive)==sum(sol['positive'] for sol in actual)
            count_by_completions[len(actual)]+=1
            grid.append({'r':r,'x':x,'integer_completions':len(actual),'positive_completions':len(positive)})

    family=[]
    for n in (0,1,10,10**6):
        S,T,U=136+200*n,291+425*n,93+136*n
        r=(-3,-12,14);x=(-S,-T,U)
        expected=[[0,-3,-12,14],[-S,0,12*S+12,-14*S-13],[-T,3*T-4,0,-14*T+3],[U,-3*U+1,-12*U-2,0]]
        actual=completion.complete_three_high(r,x,True)
        assert expected in [s['P'] for s in actual]
        if n<=10:
            assert sorted(tuple(tuple(row) for row in s['P']) for s in completion.complete_three_high(r,x,False))==independent_fixed_reconstruction(r,x)
        family.append({'n':n,'q':(1,1+3*S,1+12*T,1+14*U),'positive_completions':len(actual),'known_rank_two_family_member_recovered':True})

    small=completion.fixed_data((-4,1,2),(-1,2,1))
    assert small['coefficients']==(-12,-34,-28)
    assert small['discriminant']==-188
    assert completion.complete_three_high((-4,1,2),(-1,2,1),False)==[]

    # The tail is a proved finite corollary when h<=4 and the ordinary q<=25.
    tail=[]
    for h0 in range(1,5):
        for v0 in range(1,24//h0+1):
            for z0 in range(1,2*h0+2):
                az=v0*z0*z0-2*(h0*v0+1)*z0+(h0-1)*(h0*v0+1)
                bz=v0*z0*z0-(v0*(h0+1)+1-h0)*z0+h0*v0*(h0-1)
                assert bz-az>0
                if az>=0 or (-bz)%az:
                    continue
                P0=(-bz)//az
                if P0<h0:
                    continue
                bound=((h0-1)*v0+h0+1)*(2*h0+1)-h0
                assert P0<=bound
                r=(P0,-P0+h0-1,-h0);x=(1,-1,-v0)
                out=completion.complete_three_high(r,x,False)
                tail.append({'h':h0,'v':v0,'z':z0,'P':P0,'q_ordinary':h0*v0+1,'proved_bound':bound,'completions':len(out)})

    sharp_r=(-2,-2,3);sharp_x=(-3,-3,2)
    sharp=completion.complete_three_high(sharp_r,sharp_x)
    assert len(sharp)==2
    sharp_matrix=[[0,-2,-2,3],[-3,0,4,-8],[-3,12,0,-16],[2,-6,-3,0]]
    assert any(s['P']==sharp_matrix for s in sharp)
    assert all(s['q']==(1,7,7,7) and s['positive'] for s in sharp)
    for s in sharp:
        assert {tuple(c['gain']) for c in s['positive_cycles']}=={(6,7),(48,49)}

    sources=[locate('three_high_fixed_low_completion_v17.tex'),locate('three_high_opposite_exception_note_v17.tex')]
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    result={'version':'v17','passed':True,'scope':'Complete integer three-high reconstruction for fixed low row AND column; no claim classifying all varying low data.',
            'general_result':'At most two completions; a same-sign high pair gives a genuine quadratic with nonzero leading coefficient.',
            'polynomial_identity_count':len(identities),'polynomial_identities':identities,
            'small_input_crosscheck':{'purpose':'Implementation validation, not the range of the theorem','all_grid_cases':len(grid),'r_values':[-3,-2,-1,1,2,3],'x_absolute_values':[1,2,3],'count_by_completions':count_by_completions,'all_matched_independent_signed_divisors':True,'cases':grid},
            'rank_two_family_examples':family,'forbidden_335_data':small,
            'sharp_labeled_bound':{'r':sharp_r,'x':sharp_x,'completions':sharp,'up_to_permutation':'The two completions exchange high labels 1 and 2; geometric inequivalence is not asserted.'},
            'proof_derived_tail_checks':{'conditions':'h<=4 and hv+1<=25','all_proved_z_intervals_checked':True,'arbitrary_cutoff':False,'records':tail},
            'source_sha256':{p.name:sha(p) for p in sources},'script_sha256':sha(Path(__file__)),
            'research_helper':{'file':'research/'+HELPER.name,'sha256':sha(HELPER)},
            'external_peer_review':False,'proof_assistant_formalization':False}
    out=HERE/'three_high_completion_verification_v17.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'polynomial_identities':len(identities),'independent_fixed_input_cases':len(grid),'count_by_completions':count_by_completions,'forbidden_335_discriminant':small['discriminant'],'tail_candidates':len(tail),'result':str(out)},ensure_ascii=False))


if __name__=='__main__':main()
