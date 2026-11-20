#!/usr/bin/env python3
"""Independent original-equation audit of the analytic G5_10 obstruction.

No primary-verifier import, denominator search, or numerical tolerance.
Polynomial identities use exact coefficient dictionaries. Finite node tests
use only ranges explicitly derived in the proof, plus all 21 node triples.
This is internal review, not external refereeing or proof-assistant checking.
"""
from pathlib import Path
from itertools import combinations,product
from math import isqrt
import argparse,hashlib,json

class P:
    def __init__(self,d=None):self.d={m:c for m,c in (d or {}).items() if c}
    @staticmethod
    def co(x):return x if isinstance(x,P) else P({():x})
    @staticmethod
    def var(x):return P({(x,):1})
    def __add__(self,x):
        d=self.d.copy()
        for m,c in self.co(x).d.items():d[m]=d.get(m,0)+c
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({m:-c for m,c in self.d.items()})
    def __sub__(self,x):return self+-self.co(x)
    def __rsub__(self,x):return self.co(x)+-self
    def __mul__(self,x):
        d={}
        for m,c in self.d.items():
            for n,e in self.co(x).d.items():
                k=tuple(sorted(m+n));d[k]=d.get(k,0)+c*e
        return P(d)
    __rmul__=__mul__
    def __eq__(self,x):return self.d==self.co(x).d

def run():
    names='r s z S T x y A B a b delta n1 n2 n3 m0 m2 m3 q U V u v h alpha nu0 M N q02 q12'
    var={name:P.var(name) for name in names.split()}
    r,s,z,S,T,x,y,A,B,a,b,delta,n1,n2,n3,m0,m2,m3,q,U,V,u,v,h,alpha,nu0,M,N,q02,q12=[var[name] for name in names.split()]
    identities=[]
    def check(name,left,right):
        assert left==right,name
        identities.append(name)
    # Original physical labels, not implicit canonical index positions.
    p4={2:{2:0,3:-A,0:x,1:-s},3:{2:-B,3:0,0:-y,1:z},
        0:{2:r,3:-r-1,0:0,1:0},1:{2:-S,3:T,0:S-T-1,1:0}}
    check('R0 physical node04;1',1-n1-p4[0][1],1-n1)
    check('R0 physical node04;2',1-n2-p4[0][2],1-r-n2)
    check('R0 physical node04;3',1-n3-p4[0][3],r+2-n3)
    check('R1 physical node14;0',1-m0-p4[1][0],T-S+2-m0)
    check('R1 physical node14;2',1-m2-p4[1][2],S+1-m2)
    check('R1 physical node14;3',1-m3-p4[1][3],1-T-m3)
    check('D4 low0 from original column',-1-sum(p4[j][0] for j in (2,3,1)),T-S+y-x)
    check('D4 low1 from original column',-1-sum(p4[j][1] for j in (2,3,0)),s-z-1)
    # Ordinary branch factorization, r=2,S=3,T=5,s=2u,z=3v.
    check('ordinary high-high pair factor',
        (7*u+1)*(13*v+1)-((6*u+1)*(15*v+1)-1),
        (u-2)*(v+1)+3)
    # Positive exception D opposition with physical low columns.
    q03=P.var('q03')
    D04=-1-((q-1)-(q02-1)-(q03-1))+(delta+y-x)
    check('positive exception D04 sum',D04,q02+q03-q-2+delta+y-x)
    check('positive exception q delta relation',
        q02+q03-(delta+3-m0)-2+delta+y-x,
        q02+q03-5+m0+y-x)
    check('positive exception D14 sum',-1-(1-U-V)+(s-z-1),U+V+s-z-3)
    # Beta=1, E=1 elimination, r=z(h+1)-1.
    rr=z*(h+1)-1
    check('negative beta1 elimination',rr*rr*(h+1)-(rr+1)*(rr+1)*h-h*(h+1),
        (h+1)*((h+1)*z*(z-2)-(h-1)))
    # Complete original resonance matrix and all pair equations.
    aa=12*alpha+1
    R={2:{2:0,3:-(13*alpha+1),0:4*alpha,1:-3*alpha},
       3:{2:-12,3:0,0:-3,1:2},0:{2:3,3:-4,0:0,1:0},
       1:{2:-4,3:6,0:-3,1:0}}
    Q={2:aa,3:13,0:1,1:1}
    for i in (2,3,0,1):check(f'resonance original row{i}',sum(R[i].values()),-Q[i])
    for i,j in combinations((2,3,0,1),2):
        check(f'resonance original pair{i}{j}',R[i][j]*R[j][i],Q[i]*Q[j]-1)
    DD={i:-Q[i]-sum(R[j][i] for j in Q if j!=i) for i in Q}
    for i,want in [(2,12-12*alpha),(3,13*alpha-14),(0,5-4*alpha),(1,3*alpha-3)]:
        check(f'resonance original D4_{i}',DD[i],want)
    check('negative exception D14',-1-(-(q-1)+U-V)+DD[1],3*alpha+q-5-U+V)
    check('negative exception D04',-1-(-1-u+v)+DD[0],u-v+5-4*alpha)
    # Recover the high row at core2 by physical nodes on edge24.
    p240=aa*(1-nu0)-R[2][0]
    p241=aa*(1-(3-nu0))-R[2][1]
    check('core2 node24;0 reconstruction',p240,(8-12*nu0)*alpha+1-nu0)
    check('core2 node24;1 reconstruction',p241,(12*nu0-21)*alpha+nu0-2)
    check('core2 node24;3=2',aa-alpha+R[2][3]*(-1),2*aa)
    check('M lower bound numerator',aa*q02-1-4*alpha*(3*q02),q02-1)
    check('N lower bound numerator',aa*q12-1-(9*alpha+1)*q12,3*alpha*q12-1)
    check('D24 opposition original columns',-aa-(-M-N+12)+DD[2],M+N-24*alpha-1)
    check('terminal strict lower estimate',3*(8*alpha-7)+(15*alpha+1),39*alpha-20)
    check('terminal gap alpha>=2',(39*alpha-20)-(24*alpha+10),15*(alpha-2))

    nodes=[ns for ns in product(range(6),repeat=3) if sum(ns)==5]
    assert len(nodes)==21
    ordinary=[]
    # These finite central ranges are obtained analytically, not chosen.
    branches={'R01 positive':[(rr,ss,ss+2) for rr in (1,2) for ss in range(rr+1,2*rr)],
              'R01 negative':[(rr,ss,ss+dd) for ss in (2,3) for rr in range(1,ss)
                  for dd in range(2,6-ss) if rr*dd>ss]}
    for branch,triples in branches.items():
        for rr,ss,tt in triples:
            for ns,ms in product(nodes,repeat=2):
                n1,n2,n3=ns;m0,m2,m3=ms
                R0=(1-n1,1-rr-n2,rr+2-n3)
                R1=(tt-ss+2-m0,ss+1-m2,1-tt-m3)
                if not all(R0) or not all(R1):continue
                if sum(x>0 for x in R0)!=1 or sum(x>0 for x in R1)!=1:continue
                if R0[0]+R1[0]:continue
                if (R0[0]>0)!=(branch=='R01 positive'):continue
                ordinary.append({'branch':branch,'rST':[rr,ss,tt],'node04':ns,'node14':ms,'R0':R0,'R1':R1})
    assert len(ordinary)==2 and all(x['rST']==[2,3,5] for x in ordinary)
    signed_divisors=[d for d in range(-30,31) if d and 30%d==0]
    assert not [d for d in signed_divisors if (d-27)%31==0]
    nu_tests=[]
    for nn in range(4):
        # Both expressions are affine in alpha>=2. Record exact coefficients.
        c0,b0=8-12*nn,1-nn;c1,b1=12*nn-21,nn-2
        both=c0*2+b0<0 and c1*2+b1<0 and c0<=0 and c1<=0
        nu_tests.append({'nu0':nn,'nu1':3-nn,'p240_coeff_constant':[c0,b0],
            'p241_coeff_constant':[c1,b1],'both_negative_for_all_alpha_ge2':both})
    assert [x['nu0'] for x in nu_tests if x['both_negative_for_all_alpha_ge2']]==[1]
    return {'status':'PASS','review_scope':'internal independent mathematical review and exact original-equation audit',
        'external_refereeing':False,'proof_assistant_formalization':False,'denominator_cutoff':None,
        'polynomial_identity_count':len(identities),'polynomial_identities':identities,
        'ordinary_node_cases_complete_derived_ranges':ordinary,
        'ordinary_p342_signed_divisors_of30':signed_divisors,
        'ordinary_p342_residue27_mod31_matches':[],
        'negative_resonance_nu_cases':nu_tests,
        'analytical_review':[
            'Both graph automorphisms used for canonical order preserve H.',
            'Matching gives one positive and two negative nonzero low-row entries at cores0,1,2.',
            'Ordinary cases force r2,S3,T5 without D opposition; the derived divisor equation has u1,v2 only.',
            'Positive exception: D04 gives x-y>0, D14 gives s-z<=1; positive branch gives s-z>=1; the forced low column creates an odd/even contradiction.',
            'Negative exception retains q01=3 or5 and all positive alpha; no initial alpha cutoff is used.',
            'For alpha,beta>1, normal signed-divisor choices make E integral with abs(E)<1, hence E0, impossible by gcd(r,2r+1)=1.',
            'For alpha1,beta>1, integrality forces beta2,E0, also impossible; beta1 remains.',
            'Beta1,E1 and z>=2 force h1,z2,r3,S4,T6, leaving the entire fixed13 resonance.',
            'U,V are positive even integers from original pairs and odd denominators; alpha is therefore even>=2.',
            'All final node and D equations were checked in physical labels, including D4_2=12-12alpha and M+N=24alpha+1.',
            'Strict estimates M>3q02,N>q12 hold by positive original-pair residuals and contradict the exact D sum for every alpha>=2.']}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--proof',type=Path,required=True)
    ap.add_argument('--output',type=Path,default=Path(__file__).with_name('g5_10_original_equations_independent_audit_v18.json'))
    args=ap.parse_args()
    r=run();r['source_hashes']={args.proof.name:hashlib.sha256(args.proof.read_bytes()).hexdigest(),
        Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':'PASS','polynomial_identities':r['polynomial_identity_count'],
        'complete_ordinary_node_cases':len(r['ordinary_node_cases_complete_derived_ranges']),
        'negative_nu_cases':4,'denominator_cutoff':None,'output':args.output.name},indent=2))

if __name__=='__main__':main()
