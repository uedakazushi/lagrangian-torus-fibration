#!/usr/bin/env python3
"""Exact standard-library algebra certificates for leaf escalation.

The general proof uses the established one-high row sign theorem and the
low-low puncture lemma.  This script checks the full sign-pairing table and
the unbounded polynomial identities, not a denominator-bounded search.
"""
from pathlib import Path
from hashlib import sha256
from itertools import permutations,product
import json

checks=[]
def check(c,label):
    if not c:raise AssertionError(label)
    checks.append(label)

# Each sign pair contributes +1,-1,0 in units of the shared denominator.
def pair_sum(a,b):return a if a==b else 0
sign_table=[]
for sign_x,leaf_signs in [(1,(-1,-1)),(-1,(1,-1))]:
 for middle_signs in sorted(set(permutations((1,-1)))):
  for leaf in sorted(set(permutations(leaf_signs))):
   total=sum(pair_sum(a,b) for a,b in zip(leaf,middle_signs))
   expected=-1 if sign_x>0 else 0
   check(total==expected,'complete common-puncture sign pairing')
   sign_table.append({'sign_x':sign_x,'leaf':leaf,'middle':middle_signs,'Lambda':total})

# Sparse multivariate integer polynomials in s,S,c.
def add(a,b):
    out=dict(a)
    for m,c in b.items():out[m]=out.get(m,0)+c
    return {m:c for m,c in out.items() if c}
def neg(a):return {m:-c for m,c in a.items()}
def mul(a,b):
    out={}
    for m,c in a.items():
      for n,d in b.items():
        p=tuple(x+y for x,y in zip(m,n));out[p]=out.get(p,0)+c*d
    return {m:c for m,c in out.items() if c}
def scale(a,c):return {m:v*c for m,v in a.items() if v*c}
one={(0,0,0):1};s={(1,0,0):1};S={(0,1,0):1};c={(0,0,1):1}
a=add(mul(s,S),one)
for sign in [1,-1]:
 x=scale(s,sign);inv=scale(S,sign)
 alpha=add(mul(c,a),x);beta=add(mul(c,a),inv)
 b=add(add(mul(mul(c,c),a),mul(c,add(x,inv))),one)
 check(mul(alpha,beta)==add(mul(a,b),neg(one)),
       'full determinant elimination for either sign of x')
bnegative=add(add(scale(a,4),scale(add(s,S),-2)),one)
check(add(bnegative,neg(add(scale(a,2),one)))==scale(mul(add(s,neg(one)),add(S,neg(one))),2),
      'negative-x lower bound b-(2a+1)=2(s-1)(S-1)')
bpositive=add(add(a,s),add(S,one))
check(add(bpositive,neg(a))==add(add(s,S),one),'positive-x strict increase')

out={'version':12,'status':'passed','check_count':len(checks),'checks':checks,
     'scope':'Unbounded symbolic leaf-escalation identities and all sign pairings; no node positivity or node budget is used.',
     'sign_table':sign_table,'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
path=Path(__file__).with_name('path_escalation_verification_v12.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'passed','check_count':len(checks),'output':str(path)},indent=2))
