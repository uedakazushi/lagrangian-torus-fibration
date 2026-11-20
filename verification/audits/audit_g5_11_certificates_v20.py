#!/usr/bin/env python3
"""Independent reconstruction of the complete G5_11 arithmetic certificate.

No primary generator is imported.  Reverse bounds remain the separate
analytical proof obligation.  Within those bounds, scales are independently
reconstructed using primitive divisibility steps, including every F=0 line
and every zero-factor line.  The primary residue splitting is checked to
cover exactly the resulting half-lines, without a parameter cutoff.
"""

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import product
from math import gcd, isqrt, lcm
from pathlib import Path
import argparse
import hashlib
import json


def ceildiv(a,b):
    return -((-a)//b)


def signed_divisors(n):
    assert n>0
    out=set()
    for d in range(1,isqrt(n)+1):
        if n%d==0:
            out.update((d,-d,n//d,-n//d))
    return sorted(out)


def direct_coefficients(r,S,T):
    # From U=1+u*s, V=1+v*z and qA=1+S*s, qB=1+T*z.
    u=Q(S)+Q(S,r)-1
    v=Q(T)-Q(T,r+1)+1
    R=r*(r+1)
    cs=((u*v-S*T)*R,(u-S)*R,(v-T)*R,Q(R))
    assert all(c.denominator==1 for c in cs)
    return tuple(map(int,cs))


def independent_scale_cells(r,S,T):
    # Enforce integrality and odd q before solving the equation.  Thus s=ms*u,
    # z=mz*v with u,v>=1; no residue splitting is needed.
    ms=lcm(r,2)//gcd(S,lcm(r,2))
    mz=lcm(r+1,2)//gcd(T,lcm(r+1,2))
    f,a,b,c=direct_coefficients(r,S,T)
    f*=ms*mz
    a*=ms
    b*=mz
    factor=a*b-f*c
    points=set()
    lines=set()
    if f and factor:
        for x in signed_divisors(abs(factor)):
            y=factor//x
            if (x-b)%f or (y-a)%f:
                continue
            u,v=(x-b)//f,(y-a)//f
            if min(u,v)>=1:
                points.add((ms*u,0,mz*v,0))
    elif f:
        if -b%f==0 and -b//f>=1:
            lines.add((ms*(-b//f),0,mz,mz))
        if -a%f==0 and -a//f>=1:
            lines.add((ms,ms,mz*(-a//f),0))
    else:
        assert a>0>b
        g=gcd(a,-b)
        if c%g:
            return []
        aa,bb,cc=a//g,-b//g,c//g
        u0=(-cc*pow(aa,-1,bb))%bb
        v0=(aa*u0+cc)//bb
        assert aa*u0-bb*v0==-cc
        k=max(ceildiv(1-u0,bb),ceildiv(1-v0,aa))
        lines.add((ms*(u0+bb*k),ms*bb,mz*(v0+aa*k),mz*aa))
    return sorted(points|lines)


def reverse_allowed(r,S,T,typ):
    positive=S>r and r*T>(r+1)*S
    negative=S==T<r and S*S<2*(r-S)*(r-S+1)<4*S*S
    if not (positive or negative):
        return False
    if typ==3 and positive:
        return False
    if typ==1 and r>3 or typ==2 and r>4 or typ==4 and S>4:
        return False
    return True


def check_scale_coverage(catalog):
    grouped=defaultdict(list)
    for f in catalog:
        grouped[(f['r'],f['S'],f['T'],f['typ'])].append(tuple(f['scale']))
    expected_groups={}
    summary=Counter()
    primitive_lines=[]
    for r in range(1,10):
        for S in range(2,8):
            for T in range(S,14):
                for typ in range(1,5):
                    if not reverse_allowed(r,S,T,typ):
                        continue
                    expected=independent_scale_cells(r,S,T)
                    if not expected:
                        continue
                    key=(r,S,T,typ)
                    expected_groups[key]=expected
                    actual=grouped[key]
                    points=[p for p in expected if p[1]==p[3]==0]
                    lines=[p for p in expected if p[1] or p[3]]
                    if not lines:
                        assert set(actual)==set(points)
                        summary['primitive_points']+=len(points)
                        continue
                    assert len(lines)==1 and not points
                    s,ds,z,dz=lines[0]
                    progressions=[]
                    for a,da,b,db in actual:
                        if ds:
                            assert (a-s)%ds==0 and da%ds==0
                            offset,step=(a-s)//ds,da//ds
                        else:
                            assert (b-z)%dz==0 and db%dz==0
                            offset,step=(b-z)//dz,db//dz
                        assert offset>=0 and step>0
                        assert (a,da,b,db)==(s+ds*offset,ds*step,z+dz*offset,dz*step)
                        progressions.append((offset,step))
                    period=lcm(*(step for _,step in progressions))
                    threshold=max(offset for offset,_ in progressions)
                    assert all(any(n>=offset and (n-offset)%step==0 for offset,step in progressions)
                               for n in range(threshold+period))
                    summary['primitive_halflines']+=1
                    summary['primary_residue_halflines']+=len(progressions)
                    primitive_lines.append({'reverse_and_type':key,'primitive_scale':lines[0],
                                            'primary_parameter_progressions':progressions,
                                            'coverage_period':period,'coverage_threshold':threshold})
    assert set(grouped)==set(expected_groups)
    assert summary=={'primitive_points':90,'primitive_halflines':11,'primary_residue_halflines':78}
    return dict(summary),primitive_lines


def polynomial_product(a,b):
    return (a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[1]*b[1])


def reconstruct_family(f):
    r,S,T=f['r'],f['S'],f['T']
    s,ds,z,dz=f['scale']
    i=f['vertex']
    assert i in (3,4)
    exclusive=i-2
    other_low=7-i
    other_high=3-exclusive
    orders={1:(0,exclusive,other_low,other_high),
            2:(exclusive,0,other_low,other_high),
            3:(0,exclusive,other_high,other_low),
            4:(exclusive,0,other_high,other_low)}
    order=orders[f['typ']]
    if 'order' in f:
        assert list(order)==f['order']
    a=(s*S+1,ds*S)
    b=(z*T+1,dz*T)
    x=(Q(s*S,r),Q(ds*S,r))
    y=(Q(z*T,r+1),Q(dz*T,r+1))
    assert all(v.denominator==1 for v in x+y)
    x,y=tuple(map(int,x)),tuple(map(int,y))
    U=(a[0]+x[0]-s,a[1]+x[1]-ds)
    V=(b[0]-y[0]+z,b[1]-y[1]+dz)
    negative=lambda p:tuple(-v for v in p)
    P=(((0,0),negative(U),x,(-s,-ds)),
       (negative(V),(0,0),negative(y),(z,dz)),
       ((r,0),(-r-1,0),(0,0),(0,0)),
       ((-S,0),(T,0),(-(T-S+1),0),(0,0)))
    q=dict(zip(order,(a,b,(1,0),(1,0))))
    p={u:{v:P[ii][jj] for jj,v in enumerate(order)} for ii,u in enumerate(order)}
    D={u:tuple(-q[u][k]-sum(p[v][u][k] for v in order if v!=u) for k in (0,1)) for u in order}
    for u in order:
        assert tuple(sum(p[u][v][k] for v in order) for k in (0,1))==negative(q[u])
        assert q[u][0]>=1 and q[u][1]>=0
        for v in order:
            if u==v:
                continue
            pp=polynomial_product(p[u][v],p[v][u])
            qq=list(polynomial_product(q[u],q[v]))
            qq[0]-=1
            assert pp==tuple(qq)
    assert min(s,z)>0 and min(ds,dz)>=0 and min(U[0],V[0])>0
    assert a[0]%2==b[0]%2==1 and a[1]%2==b[1]%2==0
    assert {str(u):list(v) for u,v in q.items()}==f['q']
    assert {str(u):{str(v):list(x) for v,x in row.items()} for u,row in p.items()}==f['p']
    assert {str(u):list(v) for u,v in D.items()}==f['D']
    return {'p':p,'q':q,'D':D,'typ':f['typ']}


def common_low_denominator(u,v):
    assert u!=0 and v!=0
    if u+v==0:
        return 0
    if u*v<0 or min(abs(u),abs(v))>1:
        return None
    q=abs(u+v)
    assert (q-1)%u==(q-1)%v==0
    assert ((q-1)//u+(q-1)//v)%q==0
    return q


def impose(f,ray,target):
    a,b=f['q'][ray]
    if target==0:
        return {'status':'all','offset':0,'step':1}
    if b==0:
        if a!=target:
            return {'status':'empty','reason':'constant_denominator_mismatch','lhs':a,'rhs':target}
        return {'status':'all','offset':0,'step':1}
    if (target-a)%b:
        return {'status':'empty','reason':'nonintegral_parameter','numerator':target-a,'denominator':b}
    t=(target-a)//b
    if t<0:
        return {'status':'empty','reason':'negative_parameter','parameter':t}
    return {'status':'fixed','offset':t,'step':0}


def run(path):
    raw=json.loads(path.read_text())
    assert raw['status']=='PASS'
    primary_source=path.with_name('verify_g5_11_obstruction_v20.py')
    primary_source_checked=primary_source.is_file()
    if primary_source_checked:
        assert hashlib.sha256(primary_source.read_bytes()).hexdigest()==raw['script_sha256']
    coverage=[check_scale_coverage(cat) for cat in raw['catalogs']]
    cats=[[reconstruct_family(f) for f in cat] for cat in raw['catalogs']]
    records=raw['all_1395_certificates']
    indexed={(r['fi'],r['gj'],tuple(r['n']),tuple(r['m'])):r for r in records}
    assert len(indexed)==len(records)==1395
    nodes=[(a,b,5-a-b) for a in range(6) for b in range(6-a)]
    checked=set()
    counts=Counter()
    residuals=[]
    for fi,f in enumerate(cats[0]):
        for gj,g in enumerate(cats[1]):
            n34=tuple(1-f['p'][4][k][0]-g['p'][3][k][0] for k in (0,1,2))
            if min(n34)<0:
                continue
            assert sum(n34)==5
            counts['node_compatible_cell_pairs']+=1
            for n in nodes:
                R1={k:1-v-g['p'][1][k][0] for k,v in zip((0,2,3),n)}
                if any(v==0 for v in R1.values()) or sum(v>0 for v in R1.values())!=1:
                    continue
                q13=common_low_denominator(f['p'][4][1][0],R1[3])
                if q13 is None:
                    continue
                for m in nodes:
                    R2={k:1-v-f['p'][2][k][0] for k,v in zip((0,1,4),m)}
                    if any(v==0 for v in R2.values()) or sum(v>0 for v in R2.values())!=1:
                        continue
                    q24=common_low_denominator(g['p'][3][2][0],R2[4])
                    if q24 is None:
                        continue
                    key=(fi,gj,n,m)
                    rec=indexed[key]
                    assert key not in checked
                    checked.add(key)
                    counts['reconstructed_node_certificates']+=1
                    assert {str(k):v for k,v in R1.items()}==rec['R1']
                    assert {str(k):v for k,v in R2.items()}==rec['R2']
                    assert (q13,q24)==(rec['q13'],rec['q24'])
                    assert list(n34)==rec['nodes34']
                    fx,gy=impose(f,1,q13),impose(g,2,q24)
                    assert fx==rec['parameter_3'] and gy==rec['parameter_4']
                    cert=rec['certificate']
                    if fx['status']=='empty' or gy['status']=='empty':
                        assert cert=={'kind':'empty_parameter_set','first_core':3 if fx['status']=='empty' else 4}
                        counts['denominator_contradictions']+=1
                        continue
                    d0=f['D'][4][0]+f['D'][4][1]*fx['offset']+g['D'][3][0]+g['D'][3][1]*gy['offset']
                    d1=f['D'][4][1]*fx['step']
                    d2=g['D'][3][1]*gy['step']
                    assert cert['coefficients']==[d0,d1,d2]
                    if cert['kind']=='odd_D_residual':
                        assert d0%2==1 and d1%2==d2%2==0
                        assert cert['modulus']==2 and cert['residue']==1
                        counts['odd_D_residuals']+=1
                    else:
                        assert cert['kind']=='nonzero_constant_D' and d0!=0 and d1==d2==0
                        counts['nonzero_constant_D_residuals']+=1
                    residuals.append({'certificate_key':key,'coefficients':[d0,d1,d2],'kind':cert['kind']})
    assert checked==set(indexed)
    assert counts=={'node_compatible_cell_pairs':3592,'reconstructed_node_certificates':1395,
                   'denominator_contradictions':1309,'odd_D_residuals':72,'nonzero_constant_D_residuals':14}
    return {'status':'PASS','counts':dict(counts),
            'independent_primitive_scale_coverage':[x[0] for x in coverage],
            'primitive_halfline_certificates':[x[1] for x in coverage],
            'all_family_row_and_pair_identities_reconstructed':True,
            'all_1395_node_records_reenumerated':True,
            'D_residual_certificates':residuals,
            'source':str(path),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'primary_script_sha256_recorded':raw['script_sha256'],
            'primary_source_hash_checked':primary_source_checked,
            'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'generator_imported':False,'scale_or_denominator_cutoff':None,
            'scope':'The analytical reverse bounds and positive type-III obstruction are reviewed separately; the full scale union, all recorded matrices, all node profiles and all contradictions are reconstructed here.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    result=run(args.input)
    out=args.output or Path(__file__).with_name('g5_11_certificate_audit_v20.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','counts','independent_primitive_scale_coverage']},ensure_ascii=False))


if __name__=='__main__':
    main()
