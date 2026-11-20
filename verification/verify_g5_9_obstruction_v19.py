#!/usr/bin/env python3
"""Unbounded obstruction for G5_9 (diamond with a leaf at its degree-four vertex).

Canonical leaf labels are 0=A, 1=B, 2=C, 3=D, 4=leaf; T is the unique
three-high vertex. Its values 1,2,3 cover all canonical leaf assignments.
The mathematical proof supplies Q<=13. Only this PROVED bound is used.
All other denominators are exact fixed values or entire arithmetic rays.
The remaining leaf coefficient c or d ranges over ALL integers, represented
by points and complete parity half-lines, without any truncation.

Stage 1 enumerates 21^4 node allocations and exact necessary local row types.
Stage 2 rejects all 18 surviving half-lines by the canonical b=3 obstruction,
and treats all 908 surviving points by exact linear algebra on the entire
free-denominator families. Every rejected linear system has an independently
checked rational linear-combination certificate. Standard library only.
"""
from itertools import product
from math import lcm
from collections import Counter
import json, argparse, hashlib
from fractions import Fraction
from pathlib import Path
I=range(4)
NR={i:[] for i in I}
for i in I:
 for abc in product(range(6),repeat=3):
  if sum(abc)!=5:continue
  a=[0]*4
  for j,x in zip([j for j in I if j!=i],abc):a[j]=x
  NR[i].append(tuple(a))
def center(Q,R,r):
 if not R or not r:return []
 out=[]
 for k in range(-4,2):
  A=Q*r+R-k*R*r; B=R+r
  if not A:
   if not B:out.append(dict(kind='free',step=lcm(2,abs(r)),k=k))
  elif B%A==0:
   q=B//A
   if q>=3 and q%2 and (q-1)%r==0 and (Q*q-1)%R==0:out.append(dict(kind='fixed',q=q,k=k))
 return out
# Types (lo,hi,parity) are exact z sets.
def inter(*terms):
 lo=max((x[0] for x in terms if x[0] is not None),default=None)
 hi=min((x[1] for x in terms if x[1] is not None),default=None)
 pp={x[2] for x in terms if x[2] is not None}
 if len(pp)>1:return
 p=next(iter(pp)) if pp else None
 if p is not None:
  if lo is not None:lo+=(p-lo)%2
  if hi is not None:hi-=(hi-p)%2
 if lo is not None and hi is not None and lo>hi:return
 return (lo,hi,p)
def sset(a,b,lo=None,hi=None,p=None):
 # lo<=a*z+b<=hi; a=+-1.
 if a==1:return (None if lo is None else lo-b,None if hi is None else hi-b,None if p is None else (p-b)%2)
 return (None if hi is None else b-hi,None if lo is None else b-lo,None if p is None else (b-p)%2)
def partners(r,a,b):
 if not r:return []
 out=[sset(a,b,-r,-r)]
 sg=1 if r>0 else -1
 if abs(r)%2==0:out.append(sset(a,b,sg,sg))
 if abs(r)==1:out.append(sset(a,b,2,None,0) if sg>0 else sset(a,b,None,-2,0))
 return out
def lowok(r,s):return bool(r and s and (r==-s or r*s>0 and min(abs(r),abs(s))==1 and max(abs(r),abs(s))%2==0))
def two_row(r,s,z):
 if not r or not s or r*s>=0 or z>0 or r+s+z!=-1:return False
 if z==0:return True
 S=-min(r,s);T=max(r,s)
 return S>=2 and T>=S and T!=S+1

def rowok(row,i,T):
 if i==T:return all(row[j] for j in I if j!=i) and sum(row[j]>0 for j in I if j!=i)==1
 e=next(j for j in [1,2,3] if j not in [i,T])
 return two_row(row[0],row[T],row[e])
def varlocal(row,i,T):
 # Return exact sets satisfying lowrow necessary conditions.
 if i==T:
  j,k=(1,3) if i==2 else (1,2)
  out=[]
  for sj,sk in product([-1,1],repeat=2):
   if int(row[0]>0)+int(sj>0)+int(sk>0)!=1:continue
   typ=inter(sset(1,row[j],1,None) if sj>0 else sset(1,row[j],None,-1),sset(-1,row[k],1,None) if sk>0 else sset(-1,row[k],None,-1))
   if typ:out.append(typ)
  return out
 # s=R_iT is the other high entry.
 a=1 if T==1 else -1;b=row[T];r=row[0]
 if r>0:
  return [sset(a,b,s,s) for s in range(-r-1,0) if two_row(r,s,-1-r-s)]
 S=-r
 if S<2:return []
 return [sset(a,b,S-1,S-1),sset(a,b,S,S),sset(a,b,S+2,None)]
def first_stage():
 out=[];cnt=Counter()
 for h in range(1,4):
  for t in range(1,13//(h*(h+1))+1):
   Q=t*h*(h+1)+1
   if Q>13:continue
   u=t*h;v=t*(h+1)
   V=[[0,1-Q,-h-1,h],[-1,0,0,0],[-u,u-1,0,0],[v,-v-1,0,0]]
   for T in [1,2,3]:
    for vr in [2,3]:
     fixed=[i for i in [1,2,3] if i!=vr]
     for N0 in NR[0]:
      R0=[0]+[Q*(1-N0[i])-V[0][i] for i in [1,2,3]]
      if not all(R0[1:]):continue
      choices={}
      for i in [1,2,3]:
       cs=[]
       for ni in NR[i]:
        ri=tuple(0 if j==i else 1-ni[j]-V[i][j] for j in I)
        cp=center(Q,R0[i],ri[0])
        if not cp:continue
        if i!=vr and not rowok(ri,i,T):continue
        cs.append((ni,ri,cp))
       choices[i]=cs
      if any(not cs for cs in choices.values()):continue
      for combo in product(*(choices[i] for i in [1,2,3])):
       R=[R0]+[item[1] for item in combo]
       f,g=fixed
       if T in [f,g] and not lowok(R[f][g],R[g][f]):continue
       cnt['fixed_configurations']+=1
       hp=[j for j in [1,2,3] if j!=vr and (T in [j,vr])]
       psets=[partners(R[j][vr],1 if j==1 else -1,R[vr][j]) for j in hp]
       for terms in product(varlocal(R[vr],vr,T),*psets):
        typ=inter(*terms)
        if typ is None:continue
        cnt['surviving_types']+=1
        if typ[0] is None or typ[1] is None:cnt['unbounded_z_types']+=1
        out.append(dict(h=h,t=t,Q=Q,T=T,vr=vr,N=[N0]+[x[0] for x in combo],R0=R,z=typ,cp=[x[2] for x in combo]))
 return dict(counts=dict(cnt),cases=out)

def gaussian_certificate(equations, n):
 """RREF with a row-operation matrix U. Verify U*A=RREF exactly."""
 a=[[Fraction(x) for x in row] for row in equations]
 original=[row[:] for row in a]
 U=[[Fraction(i==j) for j in range(4)] for i in range(4)]
 pivots=[]; rr=0
 for j in range(n):
  p=next((k for k in range(rr,4) if a[k][j]),None)
  if p is None:continue
  a[rr],a[p]=a[p],a[rr];U[rr],U[p]=U[p],U[rr]
  d=a[rr][j];a[rr]=[x/d for x in a[rr]];U[rr]=[x/d for x in U[rr]]
  for k in range(4):
   if k==rr:continue
   d=a[k][j]
   if d:
    a[k]=[x-d*y for x,y in zip(a[k],a[rr])]
    U[k]=[x-d*y for x,y in zip(U[k],U[rr])]
  pivots.append(j);rr+=1
 assert all(sum(U[i][k]*original[k][j] for k in range(4))==a[i][j]
            for i in range(4) for j in range(n+1))
 for i,row in enumerate(a):
  if not any(row[:n]) and row[n]:
   return {'reason':'inconsistent','weights':[str(x) for x in U[i]],
           'combined_row':[str(x) for x in row],'nullity':n-len(pivots)}
 # In every consistent system, the original D0 equation is
 # 3*a + 3*b = -6 with a,b>=1. Check this directly, without solving
 # or bounding either free denominator.
 row=original[0]
 assert sorted(x for x in row[:n] if x)==[Fraction(3),Fraction(3)]
 assert all(x>=0 for x in row[:n]) and row[n]==-6
 assert row[n]<sum(row[:n])
 return {'reason':'positive_parameters_impossible','weights':['1','0','0','0'],
         'combined_row':[str(x) for x in row],'nullity':n-len(pivots)}

def verify_combination(equations, certificate):
 n=len(equations[0])-1
 w=list(map(Fraction,certificate['weights']))
 c=list(map(Fraction,certificate['combined_row']))
 assert all(sum(w[k]*Fraction(equations[k][j]) for k in range(4))==c[j]
            for j in range(n+1))
 if certificate['reason']=='inconsistent':
  assert not any(c[:n]) and c[n]
 else:
  assert all(x>=0 for x in c[:n]) and c[n]<sum(c[:n])

def final_stage(stage):
 counts=Counter();certificates=[];by_position=Counter();halfline_certificates=[]
 for ci,case in enumerate(stage['cases']):
  if case['z'][0]!=case['z'][1]:
   # Here T=2, variable d, R_12=-2, R_21=-1, so q_12=3.
   # Core 1 has row p^1_{4,*}=(1,-2,0), hence 4 is canonical C,
   # 0 is canonical A, and 2 is canonical B. A positive two-high
   # chart with canonical b=3 does not exist (proof in TeX).
   assert case['T']==2 and case['vr']==3
   assert tuple(case['R0'][1])==(1,0,-2,0)
   assert case['R0'][2][1]==-1
   counts['halfline_b3_rejections']+=1
   halfline_certificates.append({'case_id':ci,'canonical_b':3,
      'zero_low_row':[1,-2,0],'reverse_partner':-1,
      'complete_parameter_set':case['z']})
   continue
  z=case['z'][0];h=case['h'];t=case['t'];Q=case['Q'];T=case['T'];vr=case['vr']
  u=t*h;v=t*(h+1);c=z if vr==2 else 0;d=z if vr==3 else 0
  V=[[0,1-Q,-h-1,h],[-1,0,0,0],[-u,u-1-c,0,c],[v,-v-1-d,d,0]]
  R=[list(row) for row in case['R0']]
  j,k=(1,3) if vr==2 else (1,2)
  R[vr][j]+=z;R[vr][k]-=z
  assert all(sum(R[i])==-(Q if i==0 else 1) for i in I)
  assert all(rowok(R[i],i,T) for i in [1,2,3])
  E,F=tuple(i for i in [1,2,3] if i!=T)
  qtypes={}
  for i in [1,2,3]:
   assert len(case['cp'][i-1])==1
   qtypes[0,i]=case['cp'][i-1][0]
  for i in [E,F]:
   pair=tuple(sorted([T,i]));r=R[T][i];s=R[i][T]
   if r==-s:qtypes[pair]={'kind':'free','step':lcm(2,abs(r))}
   else:
    assert lowok(r,s)
    qtypes[pair]={'kind':'fixed','q':max(abs(r),abs(s))+1}
  variables=[p for p in qtypes if qtypes[p]['kind']=='free'];n=len(variables)
  def constant(x):return [Fraction(0)]*n+[Fraction(x)]
  def add(a,b):return [x+y for x,y in zip(a,b)]
  def scale(a,b):return [x*b for x in a]
  q_affine={}
  for pair,ty in qtypes.items():
   a=constant(ty.get('q',1))
   if ty['kind']=='free':a[variables.index(pair)]=Fraction(ty['step'])
   q_affine[pair]=a
  X={}
  for (i,j),q in q_affine.items():
   for a,b in [(i,j),(j,i)]:
    ell=Q if a==0 else 1
    X[a,b]=scale(add(scale(q,ell),constant(-1)),Fraction(1,R[a][b]))
  low_choices=[]
  for a,b in [(E,F),(F,E)]:
   assert R[a][b]<=0
   low_choices.append([0] if R[a][b]<0 else [-1,-3,-4])
  for xe,xf in product(*low_choices):
   if xe+xf < -4:continue
   counts['linear_systems']+=1
   X[E,F]=constant(xe);X[F,E]=constant(xf)
   equations=[]
   for i in I:
    a=constant(sum(V[j][i] for j in I if j!=i)+2*(Q if i==0 else 1))
    for j in I:
     if j!=i:a=add(a,X[i,j])
    equations.append(a[:-1]+[-a[-1]])
   certificate=gaussian_certificate(equations,n)
   verify_combination(equations,certificate)
   counts[certificate['reason']]+=1
   by_position[(T,vr,certificate['reason'])]+=1
   certificates.append({'case_id':ci,'variables':[list(x) for x in variables],
      'variable_domain':'Every variable is a positive integer; no upper bound.',
      'denominator_types':{str(k):v for k,v in qtypes.items()},
      'low_X':[xe,xf],'equations':[[str(x) for x in row] for row in equations],
      **certificate})
 return {'counts':dict(counts),'by_position':[{'T':k[0],'variable_row':k[1],
         'reason':k[2],'count':v} for k,v in sorted(by_position.items())],
         'halfline_certificates':halfline_certificates,'linear_certificates':certificates}


def negative_r_factor_check():
 """Exact unbounded cross-check of the analytic r=-2 lemma.
 No Q or x search bound: factor each bilinear equation into divisors
 of a constant, or retain its whole zero-factor/linear locus.
 """
 from math import isqrt
 def signed_divisors(n):
  for d in range(1,isqrt(abs(n))+1):
   if n%d==0:
    yield d;yield -d
    if d*d!=abs(n):yield abs(n)//d;yield -abs(n)//d
 points=[];degenerate=[]
 for a in range(-3,3):
  for k in range(-4,2):
   A=a*(2*k+1)-2;B=a*k-1;C=-(2*k+1);D=1-k
   if not A:
    # (a,k)=(-2,-1) gives Q+x+2=0;
    # (a,k)=(2,0) gives -Q-x+1=0. Both impossible.
    assert (a,k,B,C,D) in [(-2,-1,1,1,2),(2,0,-1,-1,1)]
    degenerate.append({'a':a,'k':k,'kind':'linear_impossible'})
    continue
   determinant=B*C-A*D
   if not determinant:
    assert (a,k,A,B,C,D) in [(-3,-1,1,2,1,2),(-1,-2,1,1,3,3),(1,1,1,0,-3,0)]
    # Factors: (Q+1)(x+2), (Q+3)(x+1), (Q-3)x.
    degenerate.append({'a':a,'k':k,'kind':'Q=3_any_x' if a==1 else 'positive_product_impossible'})
    continue
   for f in signed_divisors(determinant):
    g=determinant//f
    if (f-C)%A or (g-B)%A:continue
    Q=(f-C)//A;x=(g-B)//A
    if Q>=3 and Q%2 and x>=1:
     assert Q==3
     points.append({'a':a,'k':k,'Q':Q,'q':2*x+1})
 assert points==[{'a':-1,'k':-1,'Q':3,'q':3},{'a':0,'k':-3,'Q':3,'q':3}]
 return {'finite_points':points,'degenerate_loci':degenerate}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',type=Path,default=Path(__file__).with_name('g5_9_obstruction_verification_v19.json'))
 args=parser.parse_args()
 assert all(len(rows)==21 for rows in NR.values())
 stage=first_stage()
 assert stage['counts']=={'fixed_configurations':1388,'surviving_types':926,'unbounded_z_types':18}
 assert sum(c['z'][0]==c['z'][1] for c in stage['cases'])==908
 final=final_stage(stage)
 assert final['counts']=={'linear_systems':2596,'inconsistent':2563,
       'positive_parameters_impossible':33,'halfline_b3_rejections':18}
 output={'status':'PASS','support':'G5_9: {01,02,03,04,12,13}',
         'canonical_labelling':'0=A,1=B,2=C,3=D,4=leaf; T=1,2,3 is the unique three-high vertex.',
         'proof_dependencies':['one-high complete normal form','three-high matching',
           'two-high signs and low-low dichotomy, retaining the negative branch',
           'analytic leaf Q<=13 proof in g5_9_obstruction_v19.tex'],
         'quantification':'Nine (h,t); all 21^4 node rows; both cd=0 branches over all integers; all free q arithmetic rays over every positive integer.',
         'count_scope':'Canonical branch-labelled records, with c=d=0 duplicated. Not chart-isomorphism counts.',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'negative_r_factor_check':negative_r_factor_check(),
         'stage1':stage,'stage2':final,'survivors':[]}
 args.output.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':output['status'],'stage1':stage['counts'],'stage2':final['counts'],
                   'survivors':0,'output':str(args.output)},ensure_ascii=False,indent=2))
