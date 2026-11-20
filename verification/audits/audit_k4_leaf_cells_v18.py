#!/usr/bin/env python3
"""Independent N-first, parity-cell audit of the K4+leaf finite-type step.

No import from the primary verifier. Instead of intersecting its point/halfline
objects, partition the complete integer c- or d-axis at all predicate changes,
then test each entire parity cell via the original pair/clutching equations.
Infinite tails are retained. Every h,t with analytically proved Q<=21 is used.
"""
from pathlib import Path
from itertools import combinations,product
from math import lcm
from functools import lru_cache
from collections import Counter
import hashlib,json,argparse

VERTICES=range(4)
NROWS={i:[tuple(0 if j==i else ns[[k for k in VERTICES if k!=i].index(j)]
        for j in VERTICES) for ns in product(range(6),repeat=3) if sum(ns)==5]
    for i in VERTICES}
assert all(len(v)==21 for v in NROWS.values())

@lru_cache(None)
def mixed_pair(Q,R,r):
    """Solve original pair/clutching for any odd q>=3, including all q families."""
    if R==0 or r==0:return False
    for kappa in range(-4,2):
        den=Q*r+R-kappa*R*r;num=R+r
        if den==0:
            if num==0:
                assert R==-r and (Q-1)%r==0
                step=lcm(2,abs(r));q=1+step
                assert (Q*q-1)%R==(q-1)%r==0
                assert (Q*q-1)//R+(q-1)//r==kappa*q
                return True
            continue
        if num%den:continue
        q=num//den
        if q<3 or q%2!=1 or (Q*q-1)%R or (q-1)%r:continue
        assert (Q*q-1)//R+(q-1)//r==kappa*q
        return True
    return False

@lru_cache(None)
def low_pair(r,s):
    """Original equations, independent of the primary signed-divisor predicate."""
    if r==0 or s==0:return False
    for kappa in range(-4,2):
        den=r+s-kappa*r*s;num=r+s
        if den==0:
            if num==0:
                assert r==-s
                return True
            continue
        if num%den:continue
        q=num//den
        if q<3 or q%2!=1 or (q-1)%r or (q-1)%s:continue
        assert (q-1)//r+(q-1)//s==kappa*q
        return True
    return False

def partition_tests(r1,a1,b1,r2,a2,b2,fixed0):
    """All integer points and parity cells over the entire free-variable axis."""
    cuts=set()
    for r,a,b in [(r1,a1,b1),(r2,a2,b2)]:
        assert r!=0 and a in (-1,1)
        sg=1 if r>0 else -1
        # Zero for matching; ordinary point; unit exceptional point;
        # start of same-sign even halfline. Superset cuts are harmless.
        for s in (0,-r,sg,2*sg):cuts.add(a*(s-b))
    cuts=sorted(cuts)
    cells=[(c,c,None,c) for c in cuts]
    boundaries=[None]+cuts+[None]
    for left,right in zip(boundaries,boundaries[1:]):
        lo=left+1 if left is not None else None
        hi=right-1 if right is not None else None
        if lo is not None and hi is not None and lo>hi:continue
        for parity in (0,1):
            if lo is not None:
                rep=lo+(parity-lo)%2
                if hi is not None and rep>hi:continue
            else:
                assert hi is not None
                rep=hi-(hi-parity)%2
            cells.append((lo,hi,parity,rep))
    survivors=[];reason=Counter();details=[]
    for lo,hi,par,rep in cells:
        s1=a1*rep+b1;s2=a2*rep+b2
        test1=low_pair(r1,s1);test2=low_pair(r2,s2)
        matching=(fixed0!=0 and s1!=0 and s2!=0 and
            int(fixed0>0)+int(s1>0)+int(s2>0)==1)
        if not test1:reject='first_original_pair'
        elif not test2:reject='second_original_pair'
        elif not matching:reject='one_positive_two_negative'
        else:
            reject=None;survivors.append({'lower':lo,'upper':hi,'parity':par,'representative':rep})
        reason[reject or 'survivor']+=1
        details.append({'lower':lo,'upper':hi,'parity':par,'representative':rep,'rejection':reject})
    return cuts,details,dict(reason),survivors

def run():
    result=[];allconfigs=[];globalcounts=Counter()
    params=[(h,t) for h in range(1,5) for t in range(1,11) if t*h*(h+1)+1<=21]
    assert len(params)==15
    for h,t in params:
        Q=t*h*(h+1)+1;u=t*h;v=t*(h+1);counts=Counter()
        V0=[[0,1-Q,-h-1,h],[-1,0,0,0],[-u,u-1,0,0],[v,-v-1,0,0]]
        for variable in (2,3):
            # c=d=0 appears in both complete axes and is deliberately retained.
            other=3 if variable==2 else 2
            fixed=(1,other)
            lowopts={}
            for i in (1,2,3):
                opts=[]
                for ns in NROWS[i]:
                    R=tuple(0 if j==i else 1-ns[j]-V0[i][j] for j in VERTICES)
                    if R[0]==0:continue
                    if i!=variable and (any(R[j]==0 for j in VERTICES if j!=i)
                        or sum(R[j]>0 for j in VERTICES if j!=i)!=1):continue
                    opts.append((ns,R))
                lowopts[i]=opts
            # Independent N-first order: all lower node rows before row0.
            for lower in product(*(lowopts[i] for i in (1,2,3))):
                RR={i:lower[i-1][1] for i in (1,2,3)}
                if not low_pair(RR[fixed[0]][fixed[1]],RR[fixed[1]][fixed[0]]):continue
                for ns0 in NROWS[0]:
                    R0=tuple(0 if j==0 else Q*(1-ns0[j])-V0[0][j] for j in VERTICES)
                    if any(R0[j]==0 for j in (1,2,3)):continue
                    if not all(mixed_pair(Q,R0[i],RR[i][0]) for i in (1,2,3)):continue
                    counts['fixed_node_configurations']+=1
                    # Variable entry to1 has coefficient+1; toother has-1.
                    cuts,cells,reasons,survivors=partition_tests(
                        RR[1][variable],1,RR[variable][1],
                        RR[other][variable],-1,RR[variable][other],RR[variable][0])
                    counts['integer_parity_cells']+=len(cells)
                    counts['infinite_cells']+=sum(c['lower'] is None or c['upper'] is None for c in cells)
                    counts['survivors']+=len(survivors)
                    for k,val in reasons.items():counts['rejected_'+k]+=val
                    allconfigs.append({'h':h,'t':t,'Q':Q,'free_coefficient':'c' if variable==2 else 'd',
                        'node_rows':[ns0]+[x[0] for x in lower],
                        'reverse_rows_at_zero':[R0]+[RR[i] for i in (1,2,3)],
                        'critical_integer_points':cuts,'complete_cells':cells,
                        'surviving_cells':survivors})
        result.append({'h':h,'t':t,'Q':Q,'counts':dict(counts)});globalcounts.update(counts)
    assert globalcounts['survivors']==0
    assert globalcounts['fixed_node_configurations']==345
    return {'status':'PASS','method':'independent N-first enumeration and full parity-cell decomposition',
        'free_integer_cutoff':None,'other_denominator_cutoff':None,'leaf_Q_bound_proved_in_paper':21,
        'counts':dict(globalcounts),'by_parameter':result,'configurations':allconfigs}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--primary',type=Path)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('k4_leaf_parity_cell_independent_audit_v18.json'))
    args=parser.parse_args()
    r=run()
    if args.primary:
        primary=json.loads(args.primary.read_text())
        assert primary['counts']['fixed_node_configurations']==r['counts']['fixed_node_configurations']
        def counts(data):return {(x['h'],x['t']):x['counts'].get('fixed_node_configurations',0) for x in data['by_parameter']}
        assert counts(primary)==counts(r)
        assert len(primary['survivors'])==r['counts']['survivors']==0
        r['after_independent_enumeration_primary_comparison']={'all15_parameter_counts_agree':True,
            'survivors_agree_zero':True,'primary_filename':args.primary.name,
            'primary_sha256':hashlib.sha256(args.primary.read_bytes()).hexdigest()}
    r['audit_script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('configurations','by_parameter')},indent=2))

if __name__=='__main__':main()
