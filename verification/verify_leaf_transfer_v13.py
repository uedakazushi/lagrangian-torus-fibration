#!/usr/bin/env python3
"""Unbounded leaf-to-degree-two normal forms and continuation obstruction.

Polynomial identities verify the three candidate families. Signed-divisor
residue identities exclude two families at the continuation edge without a
denominator bound or node nonnegativity. The proof of exhaustiveness is in the
accompanying Japanese source. No global geometric existence is asserted.
"""

from pathlib import Path
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json


HERE=Path(__file__).resolve().parent
DEP_NAME='verify_fixed_denominator_partners_v12.py'
for dep in (HERE/DEP_NAME,
            HERE.parents[1]/'deliverables/general_type_surface_fibration_v12/verification'/DEP_NAME):
    if dep.exists():
        spec=importlib.util.spec_from_file_location('fixed_partner_v12',dep)
        fp=importlib.util.module_from_spec(spec);spec.loader.exec_module(fp)
        break
else:
    raise FileNotFoundError(DEP_NAME)


def main():
    checks=[]
    def identity(name,left,right):
        assert left==right,name
        checks.append(name)

    h,t=fp.Poly.variable('h'),fp.Poly.variable('t')
    family_data=[
        ('positive mixed entry',h*(h+1)+1,(h+1)*(h+2)+1,
         h,1,1,h*(h+1),(h+1)*(h+2),h+1,h+2,
         [h*(h+1)+1,-((h+1)*(h+2)+1),2*h+3,-1]),
        ('negative mixed entry h=1',2*t+1,6*t+1,
         1,1,1,2*t,6*t,2*t,3*t,[3*t,1-8*t,5*t,-1]),
        ('negative mixed entry h=2',6*t+1,20*t-1,
         1,2,2,3*t,10*t-1,6*t,10*t-1,[7*t,3-18*t,11*t-2,-1]),
    ]
    families=[]
    for name,a,b,r,s,z,S,T,x,y,Ds in family_data:
        A=a+x-s;B=b-y+z
        pp=[[0,-A,x,-s],[-B,0,-y,z],[r,-r-1,0,0],[-S,T,S-T-1,0]]
        qq=[a,b,1,1]
        for i in range(4):
            identity(f'{name}: row {i}',sum(pp[i]),-qq[i])
            identity(f'{name}: coefficient {i}',-qq[i]-sum(pp[j][i] for j in range(4)),Ds[i])
        for i,j in itertools.combinations(range(4),2):
            identity(f'{name}: crossing {i},{j}',qq[i]*qq[j]-pp[i][j]*pp[j][i],1)
        identity(f'{name}: r*x=a-1',r*x,a-1)
        identity(f'{name}: s*S=a-1',s*S,a-1)
        identity(f'{name}: (r+1)*y=b-1',(r+1)*y,b-1)
        identity(f'{name}: z*T=b-1',z*T,b-1)
        families.append({'name':name,'parameter':'every integer h>=1' if name.startswith('positive') else 'every integer t>=1',
                         'verification':'all rows, crossings, coefficients, and divisibility identities are polynomial; standard explicit weights are positive'})

    # Exhaustiveness identities. These record algebra used in the written
    # sign-case proof, not a finite sample of possible leaf denominators.
    m=t*h*(h+1)
    b_positive=m+1+h+t*(h+1)+1
    identity('positive case: factor b-1',b_positive-1,(h+1)*(t*(h+1)+1))
    identity('positive canonical A: z quotient numerator',
             t*(h+1),(t*h+1)+(t-1))
    identity('positive canonical B: necessary equation after clearing denominators',
             (m-1)*(t+1)-t*h*(t*(h+1)+1),t*(h*h-1)-1)
    identity('negative full mixed entry: candidate b',
             4*(m+1)-2*(m+1)+1,2*m+3)
    identity('negative full mixed entry: z quotient remainder',
             2*t*h*h,2*h*(t*h+1)-2*h)
    b_short=4*(m+1)-2*((h+1)+t*h)+1
    identity('negative short mixed entry: b expression',
             b_short,2*t*h*(2*h+1)+3-2*h)
    identity('negative short mixed entry: z=h',
             2*(2*(m+1)-t*h-b_short-h),-(b_short-1))
    identity('negative short mixed entry: integer T forces h|2',
             b_short-1,h*(2*t*(2*h+1)-2)+2)

    # The only possible signed divisor representatives of B mod b are B and
    # B-b since 0<B<b and |p|<=b-1. Positive B is a proper divisor larger than
    # half b-1 in all three families, so cannot divide b-1.
    a=h*(h+1)+1;b=(h+1)*(h+2)+1;B=b-h-1
    identity('positive family: B-b',B-b,-h-1)
    identity('positive family: positive representative is proper',(b-1)-B,h)
    identity('positive family: positive representative exceeds half',2*B-(b-1),h*h+h+2)
    identity('positive family: negative representative divides b-1',(h+1)*(h+2),b-1)
    identity('positive family: increasing denominators',b-a,2*h+2)
    identity('positive family: a modulo h+1',a-h*(h+1),1)

    b=6*t+1;B=3*t+2;d=3*t-1
    identity('negative h1: B-b',B-b,-d)
    identity('negative h1: positive representative is proper',(b-1)-B,3*t-2)
    identity('negative h1: positive representative exceeds half',2*B-(b-1),4)
    identity('negative h1: divisor remainder',(b-1)-2*d,2)
    identity('negative h1: lower bound after t=u+2',3*(t+2)-1,3*t+5)
    assert (6*1)%(3*1-1)==0

    b=20*t-1;B=10*t+2;d=10*t-3
    identity('negative h2: B-b',B-b,-d)
    identity('negative h2: positive representative is proper',(b-1)-B,10*t-4)
    identity('negative h2: positive representative exceeds half',2*B-(b-1),6)
    identity('negative h2: divisor remainder',(b-1)-2*d,4)
    identity('negative h2: divisor exceeds remainder after t=u+1',10*(t+1)-3,10*t+7)

    # Finite concrete models verify exact rational positivity and illustrate
    # why the leaf pair alone does not imply D_b<=-b.
    concrete=[]
    for hh in (1,2,4):
        aa=hh*(hh+1)+1;bb=(hh+1)*(hh+2)+1
        mm=fp.model(aa,bb,hh,1,1)
        assert mm['D'][0]==aa and mm['D'][1]==-bb
        candidates=[p for p in (mm['p'][1][0]*-1,mm['p'][1][0]*-1-bb)
                    if p!=0 and (bb-1)%abs(p)==0]
        assert candidates==[-hh-1]
        concrete.append({'family':'positive','parameter':hh,'model':mm,'continuation_signed_divisors':candidates})
    for hh in (1,2):
        for tt in (1,2):
            aa=(2*tt+1) if hh==1 else (6*tt+1)
            bb=(6*tt+1) if hh==1 else (20*tt-1)
            mm=fp.model(aa,bb,1,hh,hh)
            BB=-mm['p'][1][0]
            candidates=[p for p in (BB,BB-bb) if p!=0 and (bb-1)%abs(p)==0]
            assert bool(candidates)==(hh==1 and tt==1)
            concrete.append({'family':f'negative h={hh}','parameter':tt,'model':mm,'continuation_signed_divisors':candidates})

    source_name='leaf_transfer_v13.tex'
    source=next((p for p in (HERE/source_name,HERE.parent/'geometry'/source_name,
                              HERE.parent/'papers/sections/paper'/source_name) if p.exists()),None)
    result={'status':'passed','scope':'Three unbounded candidate leaf-pair families, with signed-divisor continuation reducing to the positive family; no denominator cutoff or node requirement in the main result.',
            'source':None if source is None else {'file':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()},
            'dependency':{'file':dep.name,'sha256':hashlib.sha256(dep.read_bytes()).hexdigest()},
            'polynomial_identity_count':len(checks),'polynomial_identities':checks,
            'unbounded_candidate_families':families,'concrete_exact_models':concrete}
    target=HERE/'leaf_transfer_verification_v13.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'passed','polynomial_identities':len(checks),
                      'candidate_families':3,'exact_models':len(concrete),
                      'output':str(target)},ensure_ascii=False))


if __name__=='__main__':
    main()
