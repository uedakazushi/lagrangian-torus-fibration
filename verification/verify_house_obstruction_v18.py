#!/usr/bin/env python3
"""Proof-derived certificate for the G5_5 house support obstruction.

All ranges in this certificate are derived in the proof. There is no chosen
denominator cutoff. The general exhaustion of canonical C/D types and the
node inequalities is recorded separately from the complete seven-model
fixed-a=7 classification. The latter is independently reconstructed by a
bounded original-matrix search whose bound follows from exact identities.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations,permutations,product
from math import isqrt
import hashlib,json

HERE=Path(__file__).resolve().parent

def divisors(n):
    out=[]
    for d in range(1,isqrt(n)+1):
        if n%d==0:
            out.append(d)
            if d*d!=n:out.append(n//d)
    return sorted(out)

def matrix(a,b,r,s,z):
    assert min(a,b)>1 and a%2==b%2==1
    assert (a-1)%r==(a-1)%s==(b-1)%(r+1)==(b-1)%z==0
    x,y,S,T=(a-1)//r,(b-1)//(r+1),(a-1)//s,(b-1)//z
    A,B=a+x-s,b-y+z
    P=[[0,-A,x,-s],[-B,0,-y,z],[r,-r-1,0,0],[-S,T,S-T-1,0]]
    q=[a,b,1,1]
    assert all(sum(P[i])==-q[i] for i in range(4))
    assert all(P[i][j]*P[j][i]==q[i]*q[j]-1 for i,j in combinations(range(4),2))
    positive_cycles=[]
    for n in (2,3,4):
        for cyc in permutations(range(4),n):
            if cyc[0]!=min(cyc):continue
            prod=Fraction(1)
            for i,j in zip(cyc,cyc[1:]+cyc[:1]):
                if P[i][j]<=0:break
                prod*=Fraction(P[i][j],q[i])
            else:
                assert prod<1
                positive_cycles.append({'cycle':cyc,'gain':str(prod)})
    D=[-q[i]-sum(P[j][i] for j in range(4) if i!=j) for i in range(4)]
    return {'a':a,'b':b,'r':r,'s':s,'z':z,'S':S,'T':T,'P':P,'q':q,'D':D,
            'positive_cycles':positive_cycles}

def factor_catalog():
    trials=[];models=[]
    for s in divisors(6):
        # z*((s+1)T-2(13-s))=2(7-s)>0.
        A=13-s;K=2*(7-s)
        for z in divisors(K):
            num=2*A+K//z;den=s+1
            row={'s':s,'z':z,'T':str(Fraction(num,den))}
            if num%den:
                row['outcome']='T is not integral'
            else:
                T=num//den;b=z*T+1
                if b%2!=1:
                    row['outcome']='b is even'
                else:
                    m=matrix(7,b,1,s,z)
                    assert m['S']>m['r']
                    row['outcome']='accepted';row['model']=m
                    models.append(m)
            trials.append(row)
    return trials,sorted(models,key=lambda m:(m['b'],m['s'],m['z']))

def direct_matrix_catalog():
    """Independent original row/pair reconstruction, with proved bounds.

    s=6 has S=1=r and cannot be a positive branch. For s=1,2,3,
    z*((s+1)T-2A)=K>0 gives
    T>=floor(2A/(s+1))+1 and z<=floor(K/gap).
    Then b=(2A*z+K)/(s+1)+1 supplies a derived bound, not a cutoff.
    The audit enumerates odd b, reconstructs P10 from its pair product,
    reconstructs P13 from its row sum, then tests the original equations.
    """
    rows=[];models=[]
    for s in (1,2,3):
        A=13-s;K=2*(7-s);den=s+1
        Tmin=2*A//den+1;gap=den*Tmin-2*A
        zmax=K//gap
        bmax=(2*A*zmax+K)//den+1
        rec={'s':s,'Tmin':Tmin,'positive_integer_gap':gap,'derived_zmax':zmax,
             'derived_bmax':bmax,'trials':[]}
        for b in range(3,bmax+1,2):
            row={'b':b}
            if (7*b-1)%A:
                row['outcome']='original high-high pair fails divisibility'
            else:
                B=(7*b-1)//A;y=(b-1)//2;z=B-b+y
                if z<=0 or (b-1)%z:
                    row['outcome']='row-reconstructed positive z fails its pair'
                else:
                    m=matrix(7,b,1,s,z)
                    assert m['S']>1
                    row['outcome']='accepted';row['model']=m;models.append(m)
            rec['trials'].append(row)
        rows.append(rec)
    return rows,sorted(models,key=lambda m:(m['b'],m['s'],m['z']))

def common_low_types():
    # (low canonical type, shared high canonical type).
    types=[('C','A'),('C','B'),('D','A'),('D','B')]
    positive={('C','A'),('D','B')}
    records=[]
    for left,right in product(types,repeat=2):
        lp,rp=left in positive,right in positive
        if not lp and not rp:
            verdict='negative exceptional impossible: both absolute entries proper'
        elif lp and rp:
            if left[0]==right[0]=='C':
                verdict='positive exceptional impossible: both x>=2'
            elif left[0]==right[0]=='D':
                verdict='positive exceptional impossible: both z proper'
            else:verdict='remaining positive exceptional C-A / D-B'
        elif ('D','B') in (left,right):
            verdict='ordinary impossible: reverse T>=5 contradicts bound4'
        elif left[0]==right[0]=='C':
            verdict='remaining ordinary C-C with opposite A/B'
        else:
            assert left[1]==right[1]=='A'
            verdict='remaining ordinary C-A / D-A'
        records.append({'left':left,'right':right,'outcome':verdict})
    assert sum(r['outcome'].startswith('remaining') for r in records)==6
    return records

def relabel(m,order):
    return {'p':{a:{b:m['P'][i][j] for j,b in enumerate(order)} for i,a in enumerate(order)},
        'q':{a:m['q'][i] for i,a in enumerate(order)},'D':{a:m['D'][i] for i,a in enumerate(order)}}

def patch_audit(models):
    mid=relabel(matrix(11,19,1,5,3),(0,1,4,3))
    m3=relabel(matrix(3,7,1,1,1),(0,4,1,2))
    assert mid['D'][3]==1 and mid['D'][4]==3 and m3['D'][2]==-1
    records=[]
    for m in models:
        m4=relabel(m,(3,1,2,0))
        cores={2:mid,3:m3,4:m4};nodes={};clutching={};D={}
        for i,j in combinations((2,3,4),2):
            q=cores[i]['q'][j];assert q==cores[j]['q'][i]
            values={str(k):Fraction(q-cores[i]['p'][j][k]-cores[j]['p'][i][k],q)
                for k in set(range(5))-{i,j}}
            nodes[f'{i}{j}']={k:str(v) for k,v in values.items()}
            clutching[f'{i}{j}']=all(v.denominator==1 for v in values.values())
            D[f'{i}{j}']=cores[i]['D'][j]+cores[j]['D'][i]
        assert D['23']==0 and D['24']==3+m['D'][2]>0
        records.append({'outer4_b':m['b'],'outer4_s':m['s'],'outer4_z':m['z'],
            'node_numbers':nodes,'integer_clutching':clutching,'opposing_D_sums':D,
            'decisive_failure':'D23=0 forces t=3, then D24=3+D_C>0'})
    return records

def polynomial_checks():
    # A small self-contained polynomial implementation, independent of the
    # canonical-model constructors and historical verifier imports.
    class Poly:
        def __init__(self,d=None):self.d={m:c for m,c in (d or {}).items() if c}
        @staticmethod
        def co(x):return x if isinstance(x,Poly) else Poly({():x})
        def __add__(self,o):
            d=self.d.copy()
            for m,c in self.co(o).d.items():d[m]=d.get(m,0)+c
            return Poly(d)
        __radd__=__add__
        def __neg__(self):return Poly({m:-c for m,c in self.d.items()})
        def __sub__(self,o):return self+-self.co(o)
        def __rsub__(self,o):return self.co(o)+-self
        def __mul__(self,o):
            d={}
            for m,c in self.d.items():
                for n,e in self.co(o).d.items():
                    k=tuple(sorted(m+n));d[k]=d.get(k,0)+c*e
            return Poly(d)
        __rmul__=__mul__
        def __eq__(self,o):return self.d==self.co(o).d
    t,s,z,T= [Poly({(name,):1}) for name in ('t','s','z','T')]
    checks=[]
    def check(name,a,b):assert a==b,name;checks.append(name)
    q=[4*t-1,6*t+1,1,1]
    p=[[0,-(6*t-2),4*t-2,-(2*t-1)],[-(4*t+1),0,-3*t,t],
        [1,-2,0,0],[-2,6,-5,0]]
    for i in range(4):check(f'middle family row{i}',sum(p[i]),-q[i])
    for i,j in combinations(range(4),2):check(f'middle family pair{i}{j}',p[i][j]*p[j][i],q[i]*q[j]-1)
    dd=[-q[i]-sum(p[j][i] for j in range(4) if j!=i) for i in range(4)]
    check('middle D_C',dd[2],6-t);check('middle D_D',dd[3],t-2)
    check('low D23 opposition polynomial',(t-2)-1,t-3)
    check('r1,S2,z1 residual factor',(s+1)*T-8*s-4,(s+1)*(T-8)+4)
    check('r1,S2,T6 residual factor',2+2*s-4*z,2*(s-2*z+1))
    # General fixed a=7,r=1 high-high residual, multiplied by2.
    b=z*T+1;AA=13-s
    check('fixed seven original pair residual',AA*(b+1+2*z)-2*(7*b-1),
          2*(7-s)-z*((s+1)*T-2*(13-s)))
    r2,r3,r4,S2,S3,S4,T2,T3,T4=[Poly({(name,):1}) for name in
        ('r2','r3','r4','S2','S3','S4','T2','T3','T4')]
    def lows(order,r,S,T):
        A,B,C,D=order
        return {C:{A:r,B:-r-1,C:0,D:0},D:{A:-S,B:T,C:S-T-1,D:0}}
    def node(mid,outer,i,k):return 1-mid[i][k]-outer[2][k]
    parallel=lows((0,1,3,4),r2,S2,T2)
    crossed=lows((0,1,4,3),r2,S2,T2)
    c3_A=lows((4,0,2,1),r3,S3,T3)
    c3_B=lows((0,4,2,1),r3,S3,T3)
    check('C-C crossed physical node23;1',node(crossed,c3_A,3,1),1-T2)
    check('C-C parallel sharedA physical node23;4',node(parallel,c3_A,3,4),1-r3)
    check('C-C parallel sharedB physical node23;0',node(parallel,c3_B,3,0),1-r2-r3)
    d3_A=lows((4,0,1,2),r3,S3,T3)
    check('ordinary Dside3 physical node23;0',node(parallel,d3_A,3,0),1-r2-T3)
    c3_A_reverse=lows((4,0,2,1),S4,S3,T3)
    check('ordinary Dside4 physical node23;0',node(crossed,c3_A_reverse,3,0),S2+S4+2)
    d4_B=lows((1,3,0,2),r4,S4,T4)
    check('exception Dside4 physical node24;0',node(parallel,d4_B,4,0),1+S2+(T4-S4+1))
    d3_B=lows((0,4,1,2),r3,S3,T3)
    check('exception Dside3 physical node23;0',node(crossed,d3_B,3,0),1+S2+S3)
    crossed_S2=lows((0,1,4,3),r2,2,T2)
    d3_B_S2=lows((0,4,1,2),r3,2,T3)
    check('exception forcedS physical node23;1',node(crossed_S2,d3_B_S2,3,1),T3-T2)
    check('exception forcedS physical node23;4',node(crossed_S2,d3_B_S2,3,4),T2-T3)
    return checks

def main():
    trials,models=factor_catalog();audit,auditmodels=direct_matrix_catalog()
    assert models==auditmodels
    assert len(models)==7
    assert sorted(m['D'][2] for m in models)==[4,9,15,18,19,23,40]
    small=[]
    for d in divisors(4):
        s=d-1;T=8-4//d
        ok=s>=1 and T%2==0
        small.append({'s_plus_one':d,'s':s,'T':T,'accepted':ok})
    assert [(r['s'],r['T']) for r in small if r['accepted']]==[(1,6)]
    assert [(S2,S3) for S2 in range(2,5) for S3 in range(2,5) if S2+S3<=4]==[(2,2)]
    proof=HERE.parent/'papers/sections/paper/house_support_obstruction_v18.tex'
    result={'scope':'Unbounded G5_5 support exclusion in the standard quintic arithmetic gluing problem',
        'status':'PASS','denominator_cutoff':None,
        'assumptions':['integer row sums','integer pair products','positive local weights',
            'marked integer clutching','nonnegative nodes with automatic total5',
            'opposing D only on low edges23 and24'],
        'does_not_claim':['classification of arbitrary Lagrangian torus fibrations',
            'geometric existence of partial necessary data','external peer review'],
        'common_low_type_exhaustion':common_low_types(),
        'node_contradictions':[
            {'case':'C-C, middle C4','node':'n23;1=1-T2','upper_bound':-1},
            {'case':'C-C, middle C3, sharedA at3','node':'n23;4=1-r3, r3=r4+1','upper_bound':-1},
            {'case':'C-C, middle C3, sharedB at3','node':'n23;0=1-r2-r3','upper_bound':-1},
            {'case':'ordinary C-D, Dside3','node':'n23;0=1-r2-T3','upper_bound':-5},
            {'case':'ordinary C-D, Dside4','node':'n23;0=S2+S4+2','lower_bound':6},
            {'case':'positive exceptional C-D, Dside4','node':'n24;0=1+S2+L4','lower_bound':6}],
        'remaining_node_type':{'Dside':3,'Cside':4,'forced_S2_S3':[2,2],
            'remaining_node_numbers':['n23;1=T3-T2','n23;4=T2-T3'],'forced_T2_equals_T3':True},
        'outer3_exact_divisor_trials':small,
        'remaining_middle_family':{'r':1,'s':'2t-1','z':'t','S':2,'T':6,'t':'integer>=1',
            'D_low3':'t-2','D_low4':'6-t'},
        'outer3_model':matrix(3,7,1,1,1),
        'D23_forces_t':3,
        'fixed_seven_divisor_trials':trials,'fixed_seven_models':models,
        'independent_original_matrix_audit':audit,
        'fixed_seven_audit_matches':True,
        'fixed_seven_role':'q34 is forced to canonical A; the fixed-B resonance with r=2 is not in this role',
        'final_patch_original_matrix_checks':patch_audit(models),
        'polynomial_identity_checks':polynomial_checks(),
        'source_hashes':{Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            proof.name:hashlib.sha256(proof.read_bytes()).hexdigest()}}
    out=HERE/'house_support_obstruction_verification_v18.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','certificate':out.name,'type_cases':16,
        'fixed_seven_models':7,'polynomial_identities':len(result['polynomial_identity_checks']),
        'independent_original_matrix_match':True,'denominator_cutoff':None},indent=2))

if __name__=='__main__':main()
