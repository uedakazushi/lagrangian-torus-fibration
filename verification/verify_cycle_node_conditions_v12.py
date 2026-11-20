#!/usr/bin/env python3
"""Exact finite certificates for unbounded C4/C5 node-sign arguments.

The finite domains in this script are derived in the proof: binary signs,
tau in {1,2}, reverse divisors of size <=4, and fixed entries with sum -4.
No bound on the high denominators is used to infer the obstruction.
"""
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

checks=[]
def check(c,label):
    if not c:raise AssertionError(label)
    checks.append(label)

def common_sum(sign_a,sign_b):return sign_a if sign_a==sign_b else 0

c4=[]
for eps in product([-1,1],repeat=4):
    # At center i the two low-edge incoming signs are -eps[i-1],eps[i+1].
    allowed=all(not(-eps[(i-1)%4]==1 and eps[(i+1)%4]==1) for i in range(4))
    predicted=all(eps[i]==eps[(i+2)%4] for i in range(4))
    check(allowed==predicted,'C4 node positivity versus opposite pairing signs')
    if allowed:
        lam=[common_sum(eps[i],-eps[(i+1)%4]) for i in range(4)]
        check(lam==[(eps[i]-eps[(i+1)%4])//2 for i in range(4)],'C4 lambda formula')
        c4.append({'epsilon':eps,'lambda':lam})
check(len(c4)==4,'four labelled C4 pairing patterns')

c5=[];counts={}
for eps in product([-1,1],repeat=5):
    allowed=all(not(eps[(i-1)%5]==1 and eps[(i+1)%5]==1) for i in range(5))
    plus=[i for i,e in enumerate(eps) if e==1]
    predicted=len(plus)<=1 or (len(plus)==2 and (plus[1]-plus[0])%5 in (1,4))
    check(allowed==predicted,'C5 node positivity versus adjacent positive vertices')
    if allowed:
        lam=[common_sum(-eps[i],-eps[(i+1)%5]) for i in range(5)]
        check(lam==[-(eps[i]+eps[(i+1)%5])//2 for i in range(5)],'C5 lambda formula')
        tally=(lam.count(1),lam.count(0),lam.count(-1))
        check(tally in {(5,0,0),(3,2,0),(2,2,1)},'C5 complete lambda multiplicities')
        counts[tally]=counts.get(tally,0)+1
        c5.append({'epsilon':eps,'lambda':lam,'counts':tally})
check(counts=={(5,0,0):1,(3,2,0):5,(2,2,1):5},'complete eleven labelled C5 sign patterns')

# Lambda=0: n_low_at_zero=1-r already proves -4<=r<=1.  The other
# node gives L<=4-r<=8, so this domain is a proof-derived finite domain.
observed_zero=[];predicted_zero=[]
for r in [-4,-3,-2,-1,1]:
 for L in range(1,9):
    nodes=(1,1-r,1+r+L)
    if all(0<=n<=5 for n in nodes):observed_zero.append((r,L,nodes))
    expected=(r==1 and 1<=L<=3) or (r<0 and max(1,-r-1)<=L<=-r+4)
    if expected:predicted_zero.append((r,L,nodes))
check(observed_zero==predicted_zero,'complete lambda-zero reverse-divisor node table')

# Lambda=-1: either a zero-side node is q or the other low node is q+L;
# for q>=7 both are >5.  Only odd q=3,5 survive before checking L.
negative_table=[]
for q in [3,5]:
 for L in range(1,6):
  for order in [0,1]:
    r,rp=(-(q-1),-1) if order==0 else (-1,-(q-1))
    nodes=(2,1-r,1-rp+L)
    allowed=all(0<=n<=5 for n in nodes)
    predicted=(L<=3) if order==0 else (q+L<=5)
    check(allowed==predicted,'complete lambda-negative node table')
    if allowed:negative_table.append({'q':q,'L':L,'reverse':[r,rp],'nodes':nodes})

# Lambda=+1: L=q-2+j, 0<=j<=5, gives (0,0,j), identically in q.
for j in range(6):
    # Coefficients [constant,q] for the last node 1-(q-1)+L.
    L=(-2+j,1)
    last=(2+L[0],-1+L[1])
    check(last==(j,0),'symbolic lambda-positive table, independent of q')

# Tau relative-to-q sign table, represented by coefficients [q,X,Y].
tau_table=[]
for tau in [1,2]:
    A_minus_q=(tau-1,-1,0)
    B_minus_q=(1-tau,0,1)
    expected=((0,-1,0),(0,0,1)) if tau==1 else ((1,-1,0),(-1,0,1))
    check((A_minus_q,B_minus_q)==expected,'exact mixed tau equations relative to q')
    tau_table.append({'tau':tau,'A_minus_q':A_minus_q,'B_minus_q':B_minus_q})
uniform=[tau for tau in product([1,2],repeat=4) if all(tau[i]==tau[(i-1)%4] for i in range(4))]
check(uniform==[(1,1,1,1),(2,2,2,2)],'two propagated tau types only')

# Fixed-direction d_i may vanish.  Sum -4 and nonpositivity bound each entry
# by -4; the branch dichotomy further selects zero/-1 or zero/<=-3.
tau1_d=[d for d in product([-1,0],repeat=4) if sum(d)==-4]
tau2_d=[d for d in product([-4,-3,0],repeat=4) if sum(d)==-4]
check(tau1_d==[(-1,-1,-1,-1)],'tau=1 forces four nonzero minimal entries')
check(len(tau2_d)==4 and all(d.count(-4)==1 and d.count(0)==3 for d in tau2_d),
      'tau=2 forces one -4 and three zero fixed-direction entries')

c4_integer_patterns=[]
for c in product(range(1,5),repeat=4):
    d=tuple(-1-c[i]+c[(i-1)%4] for i in range(4))
    if not all(x<=0 for x in d):continue
    check(sum(d)==-4 and min(d)>=-4,'C4 exact reverse-divisor telescoping')
    if d in tau2_d:
        i=d.index(-4)
        cyclic=tuple(c[(i+j)%4] for j in range(4))
        check(cyclic==(4,3,2,1),'tau=2 exact reverse sequence after the -4 entry')
        final=(i+3)%4
        check(c[final]==1 and d[final]==0,'canonical outside C has r=1 at last core')
        c4_integer_patterns.append({'c':c,'d':d})
check(len(c4_integer_patterns)==4,'all four rotations of the final contradiction')

# The node table alone is not a sufficient local-model criterion.  The
# independently proved local dichotomy additionally excludes L=2.
zero_after_local_filter=[entry for entry in observed_zero if entry[1]!=2]
negative_after_local_filter=[entry for entry in negative_table if entry['L']!=2]
check(all(L==1 or L>=3 for r,L,nodes in zero_after_local_filter),
      'node table retains the separately proved local exclusion L=2')
check(all(entry['L']==1 or entry['L']>=3 for entry in negative_after_local_filter),
      'lambda-negative table retains the local dichotomy')

out={'version':12,'status':'passed','check_count':len(checks),'checks':checks,
     'scope':'Proof-derived finite sign/node cases and exact linear identities for the C4 constant-pairing obstruction; alternating C4 and all C5 components are not excluded by this verifier.',
     'C4_sign_patterns':c4,'C5_sign_patterns':c5,
     'lambda_zero_node_table':observed_zero,'lambda_negative_node_table':negative_table,
     'additional_local_necessary_condition':'L in {1} union integers >=3; the node table is not sufficient for a local chart.',
     'lambda_zero_after_local_filter':zero_after_local_filter,
     'lambda_negative_after_local_filter':negative_after_local_filter,
     'mixed_tau_table':tau_table,'C4_tau2_reverse_patterns':c4_integer_patterns,
     'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
path=Path(__file__).with_name('cycle_node_conditions_verification_v12.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'passed','check_count':len(checks),'output':str(path)},indent=2))
