#!/usr/bin/env python3
"""Supplementary exact checks for the K2,3 node reduction, no q cutoff."""
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json

HERE=Path(__file__).resolve().parent
DEP_NAME='verify_fixed_denominator_partners_v12.py'
dep=next(p for p in (HERE/DEP_NAME,
    HERE.parents[1]/'deliverables/general_type_surface_fibration_v13/verification'/DEP_NAME)
    if p.exists())
spec=importlib.util.spec_from_file_location('kn14_fixed_partner',dep)
fp=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fp)


def main():
    identities=[]
    def identity(name,left,right):
        assert left==right,name
        identities.append(name)

    cycles=[]
    choices=[[j for j in range(3) if j!=i] for i in range(3)]
    for targets in itertools.product(*choices):
        if any(targets[j]==i for i,j in enumerate(targets)):
            continue
        assert all(targets[targets[targets[i]]]==i for i in range(3))
        cycles.append(targets)
    assert cycles==[(1,2,0),(2,0,1)]

    a,b,c,d,a2,b2,c2,d2=[fp.Poly.variable(x) for x in
        ['alpha','beta','gamma','delta','alpha_next','beta_next','gamma_next','delta_next']]
    u,v=c-a-1,b-d-1
    u2,v2=c2-a2-1,b2-d2-1
    identity('three low-edge node counts sum to five',
             (1-a+b2)+(1+c-d2)+(1-u-v2),5)

    r,S,T,r2,S2,T2=[fp.Poly.variable(x) for x in ['r','S','T','r_next','S_next','T_next']]
    L,L2=T-S+1,T2-S2+1
    def data(sign,rr,SS,TT):
        LL=TT-SS+1
        return (rr,SS,rr+1,TT,0,-LL) if sign=='+' else (TT,rr+1,SS,rr,-LL,0)
    expected={
        '++':(1-r+S2,2+r-T2,1+L2),
        '+-':(2-r+r2,2+r-r2,1),
        '-+':(1-T+S2,1+S-T2,1+L+L2),
        '--':(2-T+r2,1+S-r2,1+L),
    }
    for pattern in expected:
        aa,bb,cc,dd,uu,vv=data(pattern[0],r,S,T)
        aa2,bb2,cc2,dd2,uu2,vv2=data(pattern[1],r2,S2,T2)
        actual=(1-aa+bb2,1+cc-dd2,1-uu-vv2)
        for k in range(3):
            identity(f'{pattern}: node {k}',actual[k],expected[pattern][k])
        identity(f'{pattern}: total node count',sum(actual),5)

    # This derives the integer lower bound T>=r+3 on the positive branch:
    # at T=r+2 and S>=r+1, rT-(r+1)S<=-1.
    identity('positive branch rejects T<=r+2',r*(r+2)-(r+1)*(r+1),-1)
    x,y,z=[fp.Poly.variable(n) for n in ['x','y','z']]
    identity('constant A-assignment center-node sum',
             (2+r-T2)+(2+r2-x)+(2+y-T),
             6+(r-T)+(r2-T2)+(y-x))
    identity('uniform positive-branch node sum is negative',
             6-(3+x)-(3+y)-(3+z),-3-x-y-z)
    xx,yy,ss,zz=[fp.Poly.variable(n) for n in ['x_entry','y_entry','s','z_entry']]
    identity('canonical low coefficient C',-1-xx+yy-(S-T-1),yy-xx-S+T)
    identity('canonical low coefficient D',-1+ss-zz,ss-zz-1)
    identity('constant assignment all-negative node sum',
             3-(2+x)-(2+y)-(2+z),-3-x-y-z)

    # Proven finite L-box and the complete discrete consequences of the third
    # node count, plus the theorem that at least one L=1.
    surviving=[]
    for signs in itertools.product('+-',repeat=3):
        if len(set(signs))>1:
            assert any(signs[i]=='-' and signs[(i+1)%3]=='+' for i in range(3))
        for ls in itertools.product([1,3,4],repeat=3):
            third=[]
            for i in range(3):
                j=(i+1)%3
                third.append(1+(ls[i] if signs[i]=='-' else 0)
                               +(ls[j] if signs[j]=='+' else 0))
            if max(third)>5 or 1 not in ls:
                continue
            if len(set(signs))==1 and ls==(1,1,1):
                continue
            if len(set(signs))>1:
                assert sum(ls)<=8
                for i in range(3):
                    j=(i+1)%3
                    if signs[i]=='-' and signs[j]=='+':
                        assert (ls[i],ls[j]) in [(1,1),(1,3),(3,1)]
            surviving.append({'A_assignments':list(signs),'L':list(ls),'third_nodes':third})
    assert len(surviving)==90

    # A mixed canonical assignment with all L=1 passes the three low-edge
    # node tests. Compute from the actual three local P matrices, not the
    # scalar node table above. Centers are not constructed in this example.
    example_models=[fp.model(9,11,4,4,5),fp.model(31,7,5,10,2),fp.model(31,7,5,10,2)]
    example_signs=['+','+','-']
    marked=[]
    for i,(m,sign) in enumerate(zip(example_models,example_signs)):
        nxt,prev=str((i+1)%3),str((i-1)%3)
        labels=['a','b',nxt,prev] if sign=='+' else ['b','a',prev,nxt]
        pp={labels[u]:{labels[v]:m['p'][u][v] for v in range(4)} for u in range(4)}
        qq=dict(zip(labels,m['q']))
        dd={c:-qq[c]-sum(pp[d][c] for d in labels if d!=c) for c in labels}
        assert m['d']==-1
        marked.append({'canonical_model':m,'A_assignment':sign,'labels':labels,'P':pp,'q':qq,'D':dd})
    node_triples=[];D_sums=[]
    for i in range(3):
        j=(i+1)%3;k=str((i+2)%3)
        pp,pp2=marked[i]['P'],marked[j]['P']
        nodes=[1-pp[str(j)][c]-pp2[str(i)][c] for c in ['a','b',k]]
        assert all(0<=n<=5 for n in nodes) and sum(nodes)==5
        node_triples.append(nodes)
        D_sums.append(marked[i]['D'][str(j)]+marked[j]['D'][str(i)])
    assert node_triples==[[0,3,2],[2,2,1],[0,2,3]]
    assert D_sums==[7,-10,5]
    assert all(d!=0 for d in D_sums)
    source_name='k23_node_reduction_v14.tex'
    source=next(p for p in (HERE/source_name,HERE.parent/'notes'/source_name) if p.exists())
    result={
        'version':'v14','passed':True,
        'scope':'Necessary node constraints for K2,3 high support; no complete K2,3 exclusion or geometric existence is claimed.',
        'denominator_bound':None,'D_opposition_used':False,
        'directed_cycle_choices':cycles,
        'polynomial_identity_count':len(identities),'polynomial_identities':identities,
        'each_low_low_magnitude':[1,3,4],
        'at_least_one_negative_branch':True,
        'constant_assignment_all_negative_branch_impossible':True,
        'mixed_assignment_minus_plus_pairs':[[1,1],[1,3],[3,1]],
        'finite_scalar_assignments_remaining':surviving,
        'finite_scalar_assignment_count':len(surviving),
        'count_caveat':'The 90 assignments satisfy only the displayed discrete necessary conditions; they are not integer local models or atlas isomorphism classes.',
        'all_negative_mixed_assignment_counterconfiguration':{
            'scope':'Three positive integer two-high local charts satisfying the node tests on the three edges between the degree-two vertices only. The center cores are not constructed; this is not a global node-compatible or D-compatible configuration.',
            'models':marked,'low_edge_node_triples':node_triples,'low_edge_D_sums':D_sums,
            'D_opposition_satisfied':False,
        },
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'dependency':{'file':dep.name,'sha256':hashlib.sha256(dep.read_bytes()).hexdigest()},
    }
    out=HERE/'k23_node_reduction_verification_v14.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'polynomial_identities':len(identities),
                     'directed_cycles':len(cycles),'discrete_necessary_assignments':len(surviving),
                     'certificate':str(out)}))


if __name__=='__main__':
    main()
