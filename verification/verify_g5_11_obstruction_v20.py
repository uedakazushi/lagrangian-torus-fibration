#!/usr/bin/env python3
"""Exact finite-type certificate for G5_11, with all scale half-lines.

The proof supplies reverse bounds r<=9, S<=7, T<=13 after the separate
positive type-III obstruction. These are not denominator search cutoffs.
The two scale parameters are solved completely by signed factorization or
linear Diophantine equations. Every surviving free parameter ranges over
all nonnegative integers. Only Python's standard library is required.
"""

from itertools import product
from math import gcd,isqrt,lcm
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json

def egcd(a,b):
    if b==0:return 1,0,a
    x,y,g=egcd(b,a%b)
    return y,x-(a//b)*y,g
def ceildiv(a,b):return -((-a)//b)
def divs(n):
    return sorted({v for d in range(1,isqrt(n)+1) if n%d==0 for v in (d,n//d,-d,-n//d)})
def scales(r,S,T):
    h,delta=S-r,T-S
    F=(2*r+1)*h-r*r*(delta-1)
    A=h*(r+1);B=-r*(h+delta-1);C=r*(r+1)
    N=A*B-F*C
    points=[];lines=[]
    if F and N:
        for u in divs(abs(N)):
            if N%u:continue
            v=N//u
            if (u-B)%F or (v-A)%F:continue
            s,z=(u-B)//F,(v-A)//F
            if min(s,z)<1 or s*S%r or z*T%(r+1) or s*S%2 or z*T%2:continue
            points.append((s,0,z,0))
    elif F:
        if -B%F==0 and -B//F>0:lines.append((-B//F,0,0,1))
        if -A%F==0 and -A//F>0:lines.append((0,1,-A//F,0))
    else:
        assert A>0 and B<0
        x,y,g=egcd(A,-B)
        if C%g:return []
        lines.append((-x*C//g,-B//g,y*C//g,A//g))
    for s,ds,z,dz in lines:
        period=lcm(2*r,2*(r+1))
        for t in range(period):
            ss,zz=s+ds*t,z+dz*t
            if ss*S%r or zz*T%(r+1) or ss*S%2 or zz*T%2:continue
            lo=max(ceildiv(1-ss,ds*period) if ds else 0,ceildiv(1-zz,dz*period) if dz else 0)
            if (not ds and ss<1) or (not dz and zz<1):continue
            points.append((ss+ds*period*lo,ds*period,zz+dz*period*lo,dz*period))
    return sorted(set(points))

def model(r,s,z,S,T,vertex,typ):
    other=7-vertex;exclusive=vertex-2;othertri=3-exclusive
    if typ==1:order=(0,exclusive,other,othertri)
    if typ==2:order=(exclusive,0,other,othertri)
    if typ==3:order=(0,exclusive,othertri,other)
    if typ==4:order=(exclusive,0,othertri,other)
    a,b=s*S+1,z*T+1;x=s*S//r;y=z*T//(r+1);L=T-S+1
    U=a+x-s;V=b-y+z
    assert U*V==a*b-1
    M=((0,-U,x,-s),(-V,0,-y,z),(r,-r-1,0,0),(-S,T,-L,0))
    p={i:{j:M[ii][jj] for jj,j in enumerate(order)} for ii,i in enumerate(order)}
    q=dict(zip(order,(a,b,1,1)))
    D={i:-q[i]-sum(p[j][i] for j in order if j!=i) for i in order}
    return dict(p=p,q=q,D=D,order=order)
def family(r,S,T,scale,vertex,typ):
    s,ds,z,dz=scale
    m0=model(r,s,z,S,T,vertex,typ);m1=model(r,s+ds,z+dz,S,T,vertex,typ)
    dd=lambda a,b:(a,b-a)
    return dict(r=r,S=S,T=T,scale=scale,vertex=vertex,typ=typ,
        p={i:{j:dd(m0['p'][i][j],m1['p'][i][j]) for j in m0['q']} for i in m0['q']},
        q={i:dd(m0['q'][i],m1['q'][i]) for i in m0['q']},
        D={i:dd(m0['D'][i],m1['D'][i]) for i in m0['q']})
def catalog(vertex):
    out=[]
    for r in range(1,10):
      for S in range(2,8):
       for T in range(S,14):
        if not ((S>r and r*T>(r+1)*S) or (S==T<r and S*S<2*(r-S)*(r-S+1)<4*S*S)):continue
        for scale in scales(r,S,T):
         for typ in range(1,5):
          if typ==3 and S>r:continue # proved obstruction
          if typ in (1,2) and r>(3 if typ==1 else 4):continue
          if typ==4 and S>4:continue
          out.append(family(r,S,T,scale,vertex,typ))
    return out
NODES=[(a,b,5-a-b) for a in range(6) for b in range(6-a)]
def eq_q(f,ray,target,which):
    a,b=f['q'][ray]
    return [b if which==0 else 0,b if which==1 else 0,target-a]
def partner(u,v):
    if u+v==0:return 0
    if u*v>0 and min(abs(u),abs(v))==1:return abs(u+v)
    return None
def polynomial_product(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def check_family(f):
    r,S,T=f['r'],f['S'],f['T']
    s,ds,z,dz=f['scale'];h=S-r;delta=T-S
    F=(2*r+1)*h-r*r*(delta-1)
    A=h*(r+1);B=-r*(h+delta-1);C=r*(r+1)
    coefficients=[F*s*z+A*s+B*z+C,
                  F*(s*dz+z*ds)+A*ds+B*dz,F*ds*dz]
    assert coefficients==[0,0,0]
    assert min(s,z)>0 and min(ds,dz)>=0
    assert s*S%r==ds*S%r==z*T%(r+1)==dz*T%(r+1)==0
    assert s*S%2==ds*S%2==z*T%2==dz*T%2==0
    labels=sorted(f['q'])
    for i in labels:
        assert tuple(sum(f['p'][i][j][k] for j in labels) for k in (0,1))==tuple(-v for v in f['q'][i])
        assert f['q'][i][0]>=1 and f['q'][i][1]>=0
        for j in labels:
            if i==j:continue
            pp=polynomial_product(f['p'][i][j],f['p'][j][i])
            qq=polynomial_product(f['q'][i],f['q'][j]);qq[0]-=1
            assert pp==qq
    return {'bilinear_coefficients':[F,A,B,C],
            'factor_constant':A*B-F*C,
            'identity_coefficients':coefficients,
            'all_pair_identities_in_the_free_parameter':True}

def impose_q(f,ray,q):
    """Parameter t remains all of Z_{≥0}, or is fixed exactly."""
    a,b=f['q'][ray]
    if q==0:
        return {'status':'all','offset':0,'step':1}
    if b==0:
        if a!=q:return {'status':'empty','reason':'constant_denominator_mismatch','lhs':a,'rhs':q}
        return {'status':'all','offset':0,'step':1}
    if (q-a)%b:
        return {'status':'empty','reason':'nonintegral_parameter','numerator':q-a,'denominator':b}
    t=(q-a)//b
    if t<0:return {'status':'empty','reason':'negative_parameter','parameter':t}
    return {'status':'fixed','offset':t,'step':0}

def stage():
    cats=[catalog(3),catalog(4)]
    family_checks=[[check_family(f) for f in cat] for cat in cats]
    counts=Counter();records=[];summary=Counter();empty_reasons=Counter()
    for fi,f in enumerate(cats[0]):
     for gj,g in enumerate(cats[1]):
      nodes34=tuple(1-f['p'][4][k][0]-g['p'][3][k][0] for k in (0,1,2))
      if min(nodes34)<0:continue
      assert sum(nodes34)==5
      counts['reverse_pairs']+=1
      for n in NODES:
       R1={k:1-v-g['p'][1][k][0] for k,v in zip((0,2,3),n)}
       if 0 in R1.values() or sum(v>0 for v in R1.values())!=1:continue
       q13=partner(f['p'][4][1][0],R1[3])
       if q13 is None:continue
       for m in NODES:
        R2={k:1-v-f['p'][2][k][0] for k,v in zip((0,1,4),m)}
        if 0 in R2.values() or sum(v>0 for v in R2.values())!=1:continue
        q24=partner(g['p'][3][2][0],R2[4])
        if q24 is None:continue
        counts['row_candidates']+=1
        rec=dict(fi=fi,gj=gj,n=n,m=m,R1=R1,R2=R2,q13=q13,q24=q24,nodes34=nodes34)
        fx,gy=impose_q(f,1,q13),impose_q(g,2,q24)
        rec['parameter_3']=fx;rec['parameter_4']=gy
        if fx['status']=='empty' or gy['status']=='empty':
            counts['common_puncture_denominator_rejections']+=1
            first=fx if fx['status']=='empty' else gy
            empty_reasons[first['reason']]+=1
            rec['certificate']={'kind':'empty_parameter_set','first_core':3 if fx['status']=='empty' else 4}
        else:
            counts['after_common_puncture_denominators']+=1
            d0=f['D'][4][0]+f['D'][4][1]*fx['offset']+g['D'][3][0]+g['D'][3][1]*gy['offset']
            d1=f['D'][4][1]*fx['step'];d2=g['D'][3][1]*gy['step']
            if d0%2 and d1%2==d2%2==0:
                counts['odd_D_residual_rejections']+=1
                rec['certificate']={'kind':'odd_D_residual','coefficients':[d0,d1,d2],'modulus':2,'residue':1}
                summary[(f['typ'],g['typ'],'odd')]+=1
            else:
                assert d1==d2==0 and d0!=0,(f,g,rec,(d0,d1,d2))
                counts['nonzero_constant_D_rejections']+=1
                rec['certificate']={'kind':'nonzero_constant_D','coefficients':[d0,0,0]}
                summary[(f['typ'],g['typ'],str(d0))]+=1
        records.append(rec)
    assert counts['reverse_pairs']==3592
    assert counts['row_candidates']==len(records)==1395
    assert counts['common_puncture_denominator_rejections']==1309
    assert counts['after_common_puncture_denominators']==86
    assert counts['odd_D_residual_rejections']==72
    assert counts['nonzero_constant_D_rejections']==14
    return dict(status='PASS',
        theorem_label='g51120:no-support',
        scope='Positive integral local charts for the fixed G5_11 support, marked clutching, nonnegative node budgets five, and opposing D. Positive type III is excluded analytically; all remaining reverse data are bounded by a proof, not by a search assumption.',
        proof_bounds={'r':9,'S':7,'T':13},
        scale_parameter_range='Every half-line parameter is an arbitrary integer t>=0; denominators and scales have no upper cutoff.',
        orientation_definitions={'I':'A=0,B=exclusive,C=other bivalent,D=other trivalent','II':'A=exclusive,B=0,C=other bivalent,D=other trivalent','III':'A=0,B=exclusive,C=other trivalent,D=other bivalent','IV':'A=exclusive,B=0,C=other trivalent,D=other bivalent'},
        catalogs=cats,family_identity_checks=family_checks,
        counts={**dict(counts),'local_cells_per_core':len(cats[0]),
                'point_cells_per_core':sum(f['scale'][1]==f['scale'][3]==0 for f in cats[0]),
                'halfline_cells_per_core':sum(bool(f['scale'][1] or f['scale'][3]) for f in cats[0]),
                'survivors':0},
        empty_parameter_reasons=dict(empty_reasons),
        final_D_summary=[{'types':[a,b],'certificate':c,'count':n} for (a,b,c),n in sorted(summary.items())],
        all_1395_certificates=records,
        unbounded_reverse_triples=sorted(set((f['r'],f['S'],f['T']) for f in cats[0] if f['scale'][1] or f['scale'][3])),
        count_scope='Cell and certificate counts include arithmetic-residue splitting; they are not geometric existence or isomorphism counts.',
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=str(Path(__file__).with_name('g5_11_obstruction_verification_v20.json')))
    args=parser.parse_args()
    out=stage()
    Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','counts','empty_parameter_reasons','final_D_summary','unbounded_reverse_triples']},ensure_ascii=False))
