#!/usr/bin/env python3
"""Complete four-exception K4 hub reduction, including every unbounded tail.

No numerical denominator cutoff is used. Opposite-sign large reverse pairs are
represented by their smaller even magnitude h=2, h=4, or the entire tail h>=6.
The tail replacement is proved in k4_four_exception_obstruction_v17.tex.
Only the standard library and exact integer arithmetic are used.
"""
from itertools import combinations, product, permutations
from collections import Counter
from pathlib import Path
import json, hashlib

I=range(4); EDGES=list(combinations(I,2)); NODES=list((a,b,5-a-b) for a in range(6) for b in range(6-a))

def R_models(ordinary):
 E=[e for e in EDGES if e not in ordinary]
 counts=Counter();seen=set()
 for vals in product([-4,-3,-2,-1,1,2,3,4],repeat=2):
  for bigbits in product((0,1),repeat=4):
   for signs in product((-1,1),repeat=4):
    R=[[0]*4 for i in I]; big=[[] for i in I]
    for (i,j),v in zip(ordinary,vals):R[i][j]=v;R[j][i]=-v
    for idx,((i,j),bit,sgn) in enumerate(zip(E,bigbits,signs)):
     b=(i,j)[bit];unit=(j,i)[bit];R[unit][b]=sgn;big[b].append((unit,sgn))
    opts=[]
    for i in I:
     target=-1-sum(R[i]); entries=big[i]
     if len(entries)==0: local=[([],None)] if target==0 else []
     elif len(entries)==1:
      j,s=entries[0];m=s*target;local=[([(j,s*m)],None)] if m>=2 and m%2==0 else []
     elif len(entries)==2:
      (j,s),(k,t)=entries
      local=[]
      if s==t:
       total=s*target
       if total>=4 and total%2==0:
        local=[([(j,s*m),(k,t*(total-m))],None) for m in range(2,total-1,2)]
      elif target%2==0:
       # s*m+t*n = target, let the smaller of m,n equal h.
       diff=s*target
       for h in (2,4,6):
        m=h+max(diff,0);n=h+max(-diff,0)
        local.append(([(j,s*m),(k,t*n)],{'vertex':i,'base':h,'tail':h==6,'entries':[(j,s,max(diff,0)),(k,t,max(-diff,0))]}))
     else:
      assert len(entries)==3 and target%2!=0
      local=[]
     opts.append(local)
    if any(not x for x in opts):continue
    for choice in product(*opts):
     RR=[row[:] for row in R];par=[]
     for i,(entries,p) in enumerate(choice):
      for j,v in entries:RR[i][j]=v
      if p:par.append(p)
     key=tuple(tuple(row) for row in RR)
     assert all(sum(row)==-1 for row in RR)
     if key in seen:raise AssertionError('duplicate')
     seen.add(key)
     counts['models']+=1;counts['tail_models']+=any(p['tail'] for p in par)
     yield {'R':RR,'parameters':par,'ordinary':ordinary,'exceptional':E,'signs':signs,'bigbits':bigbits}

def hub_candidates(model):
 R=model['R'];O=model['ordinary']; E=model['exceptional']
 forced={};diag={};rays={i:[j for j in I if j!=i] for i in I}
 for i,j in EDGES:
  a,b=R[i][j],R[j][i]
  if 1-a<0 or 1-a>5:forced[j,i]=1-b
  if 1-b<0 or 1-b>5:forced[i,j]=1-a
 options={}
 for i in I:
  options[i]=[{j:n for j,n in zip(rays[i],ns)} for ns in NODES
              if all(ns[rays[i].index(j)]==v for (ii,j),v in forced.items() if ii==i)]
 order=sorted(I,key=lambda i:len(options[i])); chosen={};counts=Counter();results=[]
 def rec(pos):
  if pos<4:
   i=order[pos]
   for row in options[i]:
    if any((1-R[i][j]-row[j])*(1-R[j][i]-chosen[j][i]) for j in chosen):continue
    chosen[i]=row;rec(pos+1);del chosen[i]
   return
  counts['hub_pair']+=1
  N=[[0 if i==j else chosen[i][j] for j in I] for i in I]
  d=[sum(N[j][i] for j in I)-5 for i in I]
  # Forest flow, signed relative to the canonical ordered ordinary edge.
  degree=[sum(i in e for e in O) for i in I]
  flow={};remaining=list(O);dd=d[:]
  while remaining:
   leaves=[i for i in I if sum(i in e for e in remaining)==1]
   i=leaves[0];e=next(e for e in remaining if i in e);j=e[0]+e[1]-i
   flow[e]=dd[i] if e[0]==i else -dd[i]
   dd[j]+=dd[i];dd[i]=0;remaining.remove(e)
  if any(dd):counts['component_balance_fail']+=1;return
  counts['component_balance']+=1
  qs={};ok=True
  for i,j in O:
   f=flow[i,j];u=R[i][j]
   if u*f<=0:ok=False;break
   x=f-u;q=1+u*x
   if q<3 or q%2==0 or u*x<=0:ok=False;break
   qs[i,j]=q
  if not ok:counts['positive_odd_flow_fail']+=1;return
  counts['admissible']+=1
  V=[[0 if i==j else 1-R[i][j]-N[i][j] for j in I] for i in I]
  qq={str(i)+str(j):(qs[i,j] if (i,j) in O else 1+R[i][j]*R[j][i]) for i,j in EDGES}
  results.append({'N':N,'V':V,'q':qq,'flow':{str(i)+str(j):v for (i,j),v in flow.items()}})
 rec(0)
 return counts,results


HERE=Path(__file__).resolve().parent
def sha(p):
 return hashlib.sha256(p.read_bytes()).hexdigest()

def source_file(name):
 return next(p for p in [HERE/name,HERE.parent/'paper'/name,
                        HERE.parents[1]/'deliverables/general_type_surface_fibration_v16/paper'/name]
             if p.is_file())

def validate_model(m):
 R=m['R']; O=m['ordinary']; E=m['exceptional']
 assert len(O)==2 and len(E)==4 and set(O+E)==set(EDGES)
 assert all(sum(row)==-1 and row[i]==0 for i,row in enumerate(R))
 for i,j in O:
  assert R[i][j]==-R[j][i] and 1<=abs(R[i][j])<=4
 for i,j in E:
  assert R[i][j]*R[j][i]>0
  assert sorted([abs(R[i][j]),abs(R[j][i])])[0]==1
  assert sorted([abs(R[i][j]),abs(R[j][i])])[1]%2==0
 tail_checks=0
 for param in m['parameters']:
  i=param['vertex'];h=param['base'];entries=param['entries']
  assert h in (2,4,6) and (h==6)==param['tail']
  assert len(entries)==2 and sum(s for _,s,_ in entries)==0
  for j,s,offset in entries:
   assert offset>=0 and offset%2==0 and R[i][j]==s*(h+offset)
   if param['tail']:
    assert R[j][i]==s
    for ni,nj in product(range(6),repeat=2):
     # V_big has a fixed strict sign for all even h>=6; hence its
     # product vanishes iff the opposing unit-end entry vanishes.
     vb=1-s*(6+offset)-ni;vu=1-s-nj
     assert vb!=0
     assert (vb*vu==0)==(nj==1-s)
     assert vb<0 if s==1 else vb>0
     tail_checks+=1
 return tail_checks

def original_hub_check(m,h):
 R=m['R'];N=h['N'];V=h['V'];O=m['ordinary'];E=m['exceptional'];Q=h['q']
 X=[[0]*4 for i in I]
 for i,j in EDGES:
  q=Q[str(i)+str(j)]
  assert type(q) is int and q>=3 and q%2==1
  if (i,j) in O:
   f=h['flow'][str(i)+str(j)];X[i][j]=f-R[i][j];X[j][i]=-X[i][j]
  else:X[i][j],X[j][i]=R[j][i],R[i][j]
  assert R[i][j]*X[i][j]==R[j][i]*X[j][i]==q-1
  assert (X[i][j]+X[j][i])%q==0
  assert 0<=1-(X[i][j]+X[j][i])//q<=5
  assert V[i][j]*V[j][i]==0
 for i in I:
  assert sum(R[i])==sum(V[i])==-1
  assert sum(N[i])==5 and all(0<=n<=5 for n in N[i])
  for j in I:
   assert V[i][j]==(0 if i==j else 1-R[i][j]-N[i][j])
  assert sum(X[i])+sum(V[j][i] for j in I)==-2
 # No positivity of weights is needed or asserted here.
 return X

def common_real_obstruction(m,h):
 R=m['R'];X=original_hub_check(m,h);Q=h['q'];found=[]
 for i in I:
  for js in permutations([j for j in I if j!=i]):
   q=[Q[''.join(map(str,sorted((i,j))))] for j in js]
   rr=[R[i][j] for j in js];xx=[X[i][j] for j in js]
   if (q,rr,xx)==([5,3,3],[-4,1,2],[-1,2,1]):
    s=[-a-b for a,b in zip(q,xx)];assert s==[-4,-5,-4]
    # Coefficients of (s2 A-Q12)(s3(s1-A)-Q13)-Q23 A(s1-A).
    Q12,Q13,Q23=q[0]*q[1]-1,q[0]*q[2]-1,q[1]*q[2]-1
    c2=-s[1]*s[2]+Q23
    c1=s[1]*(s[2]*s[0]-Q13)+Q12*s[2]-Q23*s[0]
    c0=-Q12*(s[2]*s[0]-Q13)
    assert [c2,c1,c0]==[-12,-34,-28]
    primitive=[-a//2 for a in [c2,c1,c0]]
    assert primitive==[6,17,14]
    discriminant=primitive[1]**2-4*primitive[0]*primitive[2]
    assert discriminant==-47
    found.append({'core':i,'ordered_high_rays':list(js),'q':q,'reverse_row':rr,
                  'outgoing_column':xx,'high_row_sums':s,
                  'primitive_polynomial_coefficients':primitive,
                  'discriminant':discriminant,'real_completion_exists':False})
 assert found
 return {'all_common_obstructions':found,'selected':found[0],
         'high_core_row_pair_system_inconsistent_over_reals':True}

def swap12(matrix):
 perm=[0,2,1,3]
 return tuple(tuple(matrix[perm[i]][perm[j]] for j in I) for i in I)

def main():
 result={};tail_checks=0;total_survivors=[]
 expected={
  'disjoint':{'R_models':112,'tail_R_models':32,'hub_pair':3552,
              'component_balance_fail':3232,'component_balance':320,
              'positive_odd_flow_fail':320},
  'adjacent':{'R_models':204,'tail_R_models':82,'hub_pair':4922,
              'component_balance_fail':4364,'component_balance':558,
              'positive_odd_flow_fail':552,'admissible':6,
              'surviving_R_models':6,'surviving_tail_R_models':0}
 }
 for name,O in [('disjoint',[(0,1),(2,3)]),('adjacent',[(0,1),(0,2)])]:
  count=Counter();records=[];survivors=[]
  for index,m in enumerate(R_models(O)):
   tail_checks+=validate_model(m)
   count['R_models']+=1;tail=any(p['tail'] for p in m['parameters']);count['tail_R_models']+=tail
   c,res=hub_candidates(m);count.update(c)
   records.append(dict(m,type_id=index,counts=dict(c),admissible_hub_candidates=res))
   if res:
    count['surviving_R_models']+=1;count['surviving_tail_R_models']+=tail
    assert not tail
    annotated=[]
    for h in res:
     check=common_real_obstruction(m,h)
     annotated.append(dict(h,local_obstruction=check))
    survivor=dict(m,type_id=index,hub_candidates=annotated)
    survivors.append(survivor);total_survivors.append(survivor)
  assert dict(count)==expected[name],(name,count)
  result[name]={'ordinary_edges':O,'normal_form_schemes_checked':8**2*2**4*2**4,
                'counts':dict(count),'all_reverse_types':records,'survivors':survivors}
 assert len(total_survivors)==6
 keys={tuple(map(tuple,m['R'])) for m in total_survivors}
 assert all(swap12(m['R']) in keys for m in total_survivors)
 orbits={min(tuple(map(tuple,m['R'])),swap12(m['R'])) for m in total_survivors}
 assert len(orbits)==3
 assert max(q for m in total_survivors for h in m['hub_candidates'] for q in h['q'].values())==13
 source=source_file('k4_four_exception_obstruction_v17.tex')
 prior=source_file('k4_low_hub_reduction_v16.tex')
 output={
  'version':'v17','passed':True,'script_sha256':sha(Path(__file__)),
  'source_sha256':{source.name:sha(source),prior.name:sha(prior)},
  'scope':'Complete exclusion of four-exception K4 high support using hub constraints and a real local row/pair obstruction. No positivity of weights, high-edge D opposition, general three-high classification or denominator cutoff is used.',
  'arbitrary_denominator_cutoff':None,
  'large_reverse_free_parameters':'In each mixed-sign two-big row, the smaller positive even magnitude h is 2, 4, or belongs to the entire tail h>=6. The tail representative h=6 is exact for all hub conditions, by the proved nonvanishing of both large-end V entries.',
  'tail_representatives_are_numerical_cutoff':False,
  'tail_entry_pair_zero_equivalences_checked':tail_checks,
  'node_allocations_per_row':21,'ordinary_graph_normal_forms':result,
  'remaining_hub_candidates':6,'remaining_hub_candidates_up_to_swap_1_2':3,
  'remaining_infinite_tails':0,'maximum_surviving_denominator_as_result':13,
  'all_surviving_candidates_have_common_real_obstruction':True,
  'common_obstruction':{'q':[5,3,3],'reverse_row':[-4,1,2],'outgoing_column':[-1,2,1],
                         'polynomial_coefficients':[6,17,14],'discriminant':-47},
  'four_exception_global_survivors':0,
  'external_peer_review':False,'proof_assistant_formalization':False}
 target=HERE/'k4_four_exceptions_verification_v17.json'
 target.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'passed':True,'reverse_types':[112,204],
                   'hub_candidates':[0,6],'infinite_tails_surviving':0,
                   'common_discriminant':-47,'global_survivors':0,
                   'certificate':str(target)},ensure_ascii=False))

if __name__=='__main__':main()

