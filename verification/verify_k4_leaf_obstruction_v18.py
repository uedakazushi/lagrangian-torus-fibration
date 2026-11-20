"""K4+leaf low-hub node test. The variable c or d is never bounded.
For each fixed node allocation, each variable reverse has either one exact
value or one complete even half-line. All intersections are exact.
"""
from itertools import product, combinations
from math import lcm
from collections import Counter
import json, argparse, hashlib
from pathlib import Path
I=tuple(range(4)); E=tuple(combinations(I,2))
NR={i:[] for i in I}
for i in I:
 for abc in product(range(6),repeat=3):
  if sum(abc)!=5:continue
  row=[0]*4
  for j,a in zip((j for j in I if j!=i),abc):row[j]=a
  NR[i].append(tuple(row))
def center_pair(Q,R,r):
 if R==0 or r==0:return []
 result=[]
 for k in range(-4,2):
  a=Q*r+R-k*R*r;b=R+r
  if not a:
   if not b:result.append({'kind':'unbounded','q_step':lcm(2,abs(r)),'k':k})
  elif b%a==0:
   q=b//a
   if q>=3 and q%2 and (q-1)%r==0 and (Q*q-1)%R==0:
    result.append({'kind':'fixed','q':q,'k':k})
 return result
def low_ok(r,s):
 return bool(r and s and (r==-s or (r*s>0 and min(abs(r),abs(s))==1 and max(abs(r),abs(s))%2==0)))
def possibilities(r,a,b):
 """For fixed r, partner s=a*z+b with a=+/-1, return all z types.
 Types have lower,upper (None for infinity), parity(None or 0/1), sign(s).
 """
 if r==0:return []
 sg=1 if r>0 else -1
 vals=[-r]
 if abs(r)%2==0:vals.append(sg)
 out=[]
 for s in vals:
  z=(s-b)*a;out.append((z,z,None,1 if s>0 else -1,'point'))
 if abs(r)==1:
  # s*sg >=2, s even.
  coefficient=a*sg; threshold=2-sg*b
  lo=threshold if coefficient==1 else None
  hi=-threshold if coefficient==-1 else None
  out.append((lo,hi,b%2,sg,'halfline'))
 return out
def intersect(x,y):
 lowers=[v for v in [x[0],y[0]] if v is not None];uppers=[v for v in [x[1],y[1]] if v is not None]
 lo=max(lowers) if lowers else None;hi=min(uppers) if uppers else None
 par=[v for v in [x[2],y[2]] if v is not None]
 if len(set(par))>1:return None
 p=par[0] if par else None
 if p is not None:
  if lo is not None:lo+=((p-lo)%2)
  if hi is not None:hi-=((hi-p)%2)
 if lo is not None and hi is not None and lo>hi:return None
 return (lo,hi,p)
def run(bound=21):
 counts=Counter();found=[];byparam=[];certificates=[]
 for h in range(1,100):
  if h*(h+1)+1>bound:break
  for t in range(1,(bound-1)//(h*(h+1))+1):
   Q=t*h*(h+1)+1;u=t*h;v=t*(h+1);before=counts.copy()
   V=[[0,1-Q,-h-1,h],[-1,0,0,0],[-u,u-1,0,0],[v,-v-1,0,0]]
   for variable_row in [2,3]:
    j,k=(1,3) if variable_row==2 else (1,2)
    # c at row2: R21 has +c,R23 has -c; d at row3 analogous.
    fixed_rows=[i for i in [1,2,3] if i!=variable_row]
    for N0 in NR[0]:
     R0=[0]+[Q*(1-N0[i])-V[0][i] for i in [1,2,3]]
     if any(R0[i]==0 for i in [1,2,3]):continue
     choices={}
     for i in [1,2,3]:
      arr=[]
      for ni in NR[i]:
       ri=tuple(0 if z==i else 1-ni[z]-V[i][z] for z in I)
       cp=center_pair(Q,R0[i],ri[0])
       if not cp:continue
       if i!=variable_row and (any(ri[z]==0 for z in I if z!=i) or sum(ri[z]>0 for z in I if z!=i)!=1):continue
       arr.append((ni,ri,cp))
      choices[i]=arr
     if any(not choices[i] for i in [1,2,3]):continue
     for combo in product(*(choices[i] for i in [1,2,3])):
      rows={i:combo[i-1] for i in [1,2,3]}
      R=[R0]+[rows[i][1] for i in [1,2,3]]
      f,g=fixed_rows
      if not low_ok(R[f][g],R[g][f]):continue
      counts['fixed_node_configurations']+=1
      # variable row must have exactly one positive entry.
      for x,y in product(possibilities(R[j][variable_row],1,R[variable_row][j]),possibilities(R[k][variable_row],-1,R[variable_row][k])):
       counts['partner_type_pairs']+=1
       if int(R[variable_row][0]>0)+int(x[3]>0)+int(y[3]>0)!=1:
        counts['matching_rejections']+=1;continue
       counts['matching_type_pairs']+=1
       typ=intersect(x,y)
       if typ is None:
        counts['empty_intersections']+=1
        certificates.append({'h':h,'t':t,'Q':Q,'variable_row':variable_row,'node_rows':[N0]+[rows[i][0] for i in [1,2,3]],'fixed_reverse_row':R[variable_row],'partner_types':[x,y],'reason':'incompatible parity' if x[2] is not None and y[2] is not None and x[2]!=y[2] else 'lower endpoint exceeds upper endpoint after parity adjustment'})
        continue
       counts['survivors']+=1
       found.append({'h':h,'t':t,'Q':Q,'variable_row':variable_row,'N':[N0]+[rows[i][0] for i in [1,2,3]],'R_at_zero':R,'types':[x,y],'intersection':typ})
   byparam.append({'h':h,'t':t,'Q':Q,'counts':dict(counts-before)})
 return {'quantification':'All h,t with Q<=bound; all 21^4 node rows; c=0 or d=0 with the other coefficient over ALL integers via exact points and complete parity half-lines. No bound on any other q.','leaf_Q_bound':bound,'counts':dict(counts),'by_parameter':byparam,'survivors':found,'empty_intersection_certificates':certificates}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',type=Path,default=Path(__file__).with_name('k4_leaf_obstruction_verification_v18.json'))
 args=parser.parse_args()
 assert all(len(rows)==21 for rows in NR.values())
 r=run()
 assert len(r['by_parameter'])==15
 assert r['counts']=={'fixed_node_configurations':345,'partner_type_pairs':1192,'matching_rejections':613,'matching_type_pairs':579,'empty_intersections':579}
 assert not r['survivors']
 assert len(r['empty_intersection_certificates'])==579
 r['status']='PASS'
 r['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 r['count_scope']='Branch-labelled node and partner-type choices; c=d=0 occurs in both branches. These are not chart-isomorphism counts.'
 r['dependencies']='Analytic Q<=21 proof: k4_leaf_obstruction_v18.tex, using one-high normal form and mh18:matching. Other denominators and the remaining c/d parameter are never bounded.'
 args.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':r['status'],'parameters':len(r['by_parameter']),'counts':r['counts'],'survivors':len(r['survivors']),'output':str(args.output)},ensure_ascii=False,indent=2))
