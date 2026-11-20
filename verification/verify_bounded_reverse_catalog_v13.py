#!/usr/bin/env python3
"""Exact complete local catalog under 2<=S<=4 and 1<=r<=3.

The denominator itself is unbounded. Proven inequalities bound T; each of the
remaining nondegenerate cases reduces to positive divisors of one integer.
The three infinite families are verified as polynomial identities. This code
does not claim that the local models glue into any global atlas.
"""

from pathlib import Path
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json


HERE = Path(__file__).resolve().parent
DEP_NAME = 'verify_fixed_denominator_partners_v12.py'
for dep in (HERE/DEP_NAME,
            HERE.parents[1]/'deliverables/general_type_surface_fibration_v12/verification'/DEP_NAME):
    if dep.exists():
        spec = importlib.util.spec_from_file_location('fixed_partner_v12', dep)
        fp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fp)
        break
else:
    raise FileNotFoundError(DEP_NAME)


RANGES = [(1, 2, 5, 7), (1, 3, 7, 13), (1, 4, 9, 19),
          (2, 3, 5, 6), (2, 4, 7, 8), (3, 4, 6, 6)]
EXPECTED = {
    (1,2,5,1,2,3,11,6,-10), (1,2,5,2,6,5,31,18,-27),
    (1,3,8,2,5,7,41,21,-36), (1,3,9,2,2,7,19,7,-15),
    (1,3,9,4,6,13,55,23,-41), (1,3,9,6,26,19,235,127,-211),
    (1,3,11,8,2,25,23,-9,9), (1,3,12,4,1,13,13,-3,-2),
    (1,4,9,1,4,5,37,21,-36), (1,4,10,1,2,5,21,11,-21),
    (1,4,12,1,1,5,13,6,-15), (1,4,12,3,5,13,61,26,-49),
    (1,4,12,4,13,17,157,78,-138), (1,4,13,9,28,37,365,177,-312),
    (1,4,13,10,62,41,807,428,-747), (1,4,15,6,2,25,31,-4,-1),
    (1,4,15,25,4,101,61,-63,102), (1,4,16,3,1,13,17,0,-9),
    (1,4,16,13,2,53,33,-31,45), (1,4,18,7,1,29,19,-15,15),
    (2,3,5,2,6,7,31,21,-25), (2,4,7,3,12,13,85,58,-73),
}


def main():
    identities = []

    def identity(name, left, right):
        assert left == right, name
        identities.append(name)

    r,s,z,S,T = [fp.Poly.variable(n) for n in ('r','s','z','S','T')]
    a,b = s*S+1,z*T+1
    R,U,V = r*(r+1),(r+1)*(S-r),r*(T-r-1)
    E = r*r*T-(r+1)*(r+1)*S+R
    rA,rpB = r*a+s*S-r*s,(r+1)*b-z*T+(r+1)*z
    identity('cleared pair product equals the bilinear equation',
             rA*rpB-R*(a*b-1), R+U*s-V*z-E*s*z)
    identity('bilinear product factorization',
             (E*s+V)*(E*z-U)-(E*R-U*V),
             E*(E*s*z+V*z-U*s-R))

    bounds, seeds, models, branches = [], [], [], []
    for rr,SS,tmin,tmax in RANGES:
        assert tmin == ((rr+1)*SS)//rr+1
        # At and beyond T0, E-U >=0 and E-U > R-V. Both inequalities
        # persist since their T-slopes are r^2>0 and r^2+r>0.
        T0 = tmax+1
        RR = rr*(rr+1); UU=(rr+1)*(SS-rr)
        E0=rr*rr*T0-(rr+1)**2*SS+RR
        V0=rr*(T0-rr-1)
        assert E0-UU >=0 and E0-UU > RR-V0
        bounds.append({'r':rr,'S':SS,'T_min':tmin,'T_max':tmax,
                       'T0':T0,'E_minus_U_at_T0':E0-UU,
                       'R_minus_V_at_T0':RR-V0,
                       'positive_difference_slope':rr*rr+rr})
        for TT in range(tmin,tmax+1):
            VV=rr*(TT-rr-1)
            EE=rr*rr*TT-(rr+1)**2*SS+RR
            CC=EE*RR-UU*VV
            seed={'r':rr,'S':SS,'T':TT,'R':RR,'U':UU,'V':VV,'E':EE,'C':CC,'trials':[]}
            if EE==0:
                assert rr==1 and TT==4*SS-2
                if SS==2:
                    seed['degenerate_branch']='s=2*z-1, every integer z>=1'
                    branches.append((rr,SS,TT,'affine'))
                else:
                    seed['degenerate_branch']='Impossible: (S-1)*(2*z-s)=1 and S-1>1.'
            elif CC==0:
                assert (rr,SS,TT) in ((2,3,6),(3,4,6))
                zz=Fraction(UU,EE)
                assert zz.denominator==1
                seed['degenerate_branch']=('z=1,s=2*k,k>=1' if rr==2
                                            else 'z=2,s=3*k,k>=1')
                branches.append((rr,SS,TT,'fixed-partner'))
            else:
                for dd in fp.positive_divisors(abs(CC)):
                    ss=Fraction(dd-VV,EE)
                    trial={'d':dd,'s':str(ss)}
                    if ss.denominator!=1 or ss<=0:
                        trial['outcome']='s is not a positive integer'
                    else:
                        ss=int(ss);zz=Fraction(UU*ss+RR,dd)
                        trial['z']=str(zz)
                        if zz.denominator!=1 or zz<=0:
                            trial['outcome']='z is not a positive integer'
                        else:
                            zz=int(zz);aa=ss*SS+1;bb=zz*TT+1
                            if ss*SS%rr or zz*TT%(rr+1):
                                trial['outcome']='remaining numerator integrality fails'
                            elif aa%2==0 or bb%2==0:
                                trial['outcome']='a or b is even'
                            else:
                                m=fp.model(aa,bb,rr,ss,zz)
                                assert m['S']==SS and m['T']==TT
                                trial['outcome']='accepted'
                                trial['a']=aa;trial['b']=bb
                                models.append(m)
                    seed['trials'].append(trial)
            seeds.append(seed)
    assert len(seeds)==26 and len(models)==22
    assert set(branches)=={(1,2,6,'affine'),(2,3,6,'fixed-partner'),(3,4,6,'fixed-partner')}
    actual={(m['r'],m['S'],m['T'],m['s'],m['z'],m['a'],m['b'],m['D'][0],m['D'][1]) for m in models}
    assert actual==EXPECTED
    assert max(max(m['a'],m['b']) for m in models)==807

    t=fp.Poly.variable('t')
    families=[]
    for name,rr,ss,zz,SS,TT,aa,bb,xx,yy,DD in [
        ('both denominators grow',1,2*t-1,t,2,6,4*t-1,6*t+1,4*t-2,3*t,[3,-7,6-t,t-2]),
        ('fixed seven',2,2*t,1,3,6,6*t+1,7,3*t,2,[6-6*t,7*t-9,5-3*t,2*t-2]),
        ('fixed thirteen',3,3*t,2,4,6,12*t+1,13,4*t,3,[12-12*t,13*t-14,5-4*t,3*t-3]),
    ]:
        AA=aa+xx-ss;BB=bb-yy+zz
        pp=[[0,-AA,xx,-ss],[-BB,0,-yy,zz],[rr,-rr-1,0,0],[-SS,TT,SS-TT-1,0]]
        qq=[aa,bb,1,1]
        for i in range(4):
            identity(f'{name}: row {i}',sum(pp[i]),-qq[i])
            identity(f'{name}: coefficient {i}',-qq[i]-sum(pp[j][i] for j in range(4)),DD[i])
        for i,j in itertools.combinations(range(4),2):
            identity(f'{name}: pair {i},{j}',qq[i]*qq[j]-pp[i][j]*pp[j][i],1)
        identity(f'{name}: negative reverse divisibility',ss*SS,aa-1)
        identity(f'{name}: positive reverse divisibility',rr*xx,aa-1)
        # For t>=1 all indicated parameters are positive integers; the
        # inherited explicit-weight theorem provides positivity uniformly.
        families.append({'name':name,'r':rr,'S':SS,'T':TT,
                         'parameter':'every integer t>=1',
                         'verification':'all rows, all crossings, and all four D entries are polynomial identities; positive weights follow from the standard-form theorem'})

    source_name='notes_bounded_reverse_catalog_v13.tex'
    source=next((p for p in (HERE/source_name,HERE.parent/'papers/sections/notes'/source_name) if p.exists()),None)
    result={'status':'passed',
            'scope':'Complete odd two-high local canonical catalog under 2<=S<=4 and1<=r<=3; no denominator cutoff; not a global atlas existence test.',
            'source':None if source is None else {'file':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()},
            'dependency':{'file':dep.name,'sha256':hashlib.sha256(dep.read_bytes()).hexdigest()},
            'polynomial_identity_count':len(identities),'polynomial_identities':identities,
            'small_reverse_pairs':6,'complete_T_cases':26,
            'finite_model_count':22,'infinite_family_count':3,
            'T_bound_certificates':bounds,'complete_factorization_trials':seeds,
            'finite_models':sorted(models,key=lambda m:tuple(m[k] for k in ('r','S','T','s','z'))),
            'infinite_families':families,
            'negative_h_branch':'The sole case r=3,S=2 forces T=2,s=3*u,z=2*v and u*(1-v)-v=1, impossible for u,v>=1.'}
    target=HERE/'bounded_reverse_catalog_verification_v13.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'passed','finite_models':22,'infinite_families':3,
                      'T_cases':26,'polynomial_identities':len(identities),'output':str(target)},ensure_ascii=False))


if __name__=='__main__':
    main()
