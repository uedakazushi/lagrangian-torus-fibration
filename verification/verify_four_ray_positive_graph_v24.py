"""Exact checks for the integer-gap proof; graph counts are not an existence claim."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from fractions import Fraction
import hashlib
import json


def add(*polys):
    out={}
    for p in polys:
        for m,c in p.items():out[m]=out.get(m,0)+c
    return {m:c for m,c in out.items() if c}


def neg(p):return {m:-c for m,c in p.items()}


def mul(p,q):
    out={}
    for m,c in p.items():
        for n,d in q.items():
            key=tuple(a+b for a,b in zip(m,n))
            out[key]=out.get(key,0)+c*d
    return {m:c for m,c in out.items() if c}


def variable(i,n=8):return {tuple(int(j==i) for j in range(n)):1}


def cycle_of(mapping,start=0):
    path=[];i=start
    while i not in path:
        path.append(i);i=mapping[i]
    return path[path.index(i):]


def check_local(q,P):
    assert all(sum(row)==-qi for row,qi in zip(P,q))
    assert all(P[i][j]*P[j][i]==q[i]*q[j]-1>0 for i,j in combinations(range(4),2))
    return [(i,j) for i,j in combinations(range(4),2) if P[i][j]>0]


def run():
    # The displayed identity is a combination of row and pair residuals.
    qi,qh,ci,cj,ck,pij,pik,pih=[variable(i) for i in range(8)]
    one={(0,)*8:1}
    lhs=add(mul(qi,add(cj,ck)),neg(mul(ci,add(pij,pik))),neg(one))
    rhs=add(mul(qi,add(ci,cj,ck,neg(qh))),
            neg(mul(ci,add(pij,pik,pih,qi))),
            mul(qi,qh),mul(ci,pih),neg(one))
    assert add(lhs,neg(rhs))=={}

    # Every choice of one edge from each of three vertices contains a cycle;
    # the exponent vector of product(c_j/c_i) on it is exactly zero.
    cycle_records=[]
    for targets in product(*[[j for j in range(3) if j!=i] for i in range(3)]):
        cyc=cycle_of(targets);exp=[0,0,0]
        for i in cyc:exp[targets[i]]+=1;exp[i]-=1
        assert len(cyc) in [2,3] and exp==[0,0,0]
        cycle_records.append({'mapping':targets,'cycle':cyc,'telescoping_exponents':exp})

    edges=list(combinations(range(4),2));graph_counts=Counter();graph_records=[]
    for mask in range(64):
        es=[e for i,e in enumerate(edges) if mask>>i&1]
        deg=[sum(v in e for e in es) for v in range(4)]
        if min(deg)<1 or max(deg)>2:continue
        if deg==[2,2,2,2]:kind='C4 excluded by the complementary negative pair'
        elif len(es)==2:kind='2K2'
        else:
            assert len(es)==3 and sorted(deg)==[1,1,2,2]
            kind='P4'
        graph_counts[kind]+=1
        graph_records.append({'mask':mask,'edges':es,'degrees':deg,'type':kind})
    assert graph_counts=={'2K2':3,'P4':12,'C4 excluded by the complementary negative pair':3}

    q=[3,5,5,17]
    P=[[0,-14,-14,25],[-1,0,3,-7],[-1,8,0,-12],[2,-12,-7,0]]
    pos=check_local(q,P)
    w=[Fraction(1),Fraction(1),Fraction(49,80),Fraction(101,12)]
    basins=[w[j]-Fraction(P[i][j],q[i])*w[i] for i in range(4) for j in range(4) if i!=j]
    assert min(basins)>0 and pos==[(0,3),(1,2)]

    q_bad=[1,5,19,31]
    bad=[[0,1,1,-3],[4,0,2,-11],[18,47,0,-84],[-10,-14,-7,0]]
    check_local(q_bad,bad)
    c=[10,14,7]
    gaps=[[0 if i==j else q_bad[i]*c[j]-c[i]*bad[i][j] for j in range(3)] for i in range(3)]
    assert all(sum(row)==1 for row in gaps)
    chosen=tuple(next(j for j in range(3) if j!=i and gaps[i][j]<=0) for i in range(3))
    cyc=cycle_of(chosen);gain=Fraction(1)
    for i in cyc:gain*=Fraction(bad[i][chosen[i]],q_bad[i])
    assert gain==Fraction(188,95)>1

    here=Path(__file__).resolve().parent
    proof=next(p for p in [here/'four_ray_positive_graph_v24.tex',here.parent/'paper/four_ray_positive_graph_v24.tex'] if p.exists())
    result={
        'version':'v24','status':'PASS',
        'scope':'Local four-ray integral row/pair data with all pair products strictly positive. No gluing existence or four-high P4 existence claim.',
        'unbounded_proof':'Integer gap identity plus directed-cycle positivity; no denominator cutoff.',
        'coefficient_identity_count':1,'all_three_vertex_outgoing_maps':len(cycle_records),
        'cycle_certificates':cycle_records,'all_labelled_graphs_checked':64,
        'graph_counts':dict(graph_counts),'graph_records':graph_records,
        'positive_fixture':{'q':q,'P':P,'weights':[str(x) for x in w],'positive_edges':pos,'minimum_basin':str(min(basins))},
        'nonpositive_fixture':{'q':q_bad,'P':bad,'isolated_vertex':3,'c':c,'gaps':gaps,'chosen_cycle':cyc,'gain':str(gain)},
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'proof_file':proof.name,'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
        'arbitrary_parameter_scan_used':False,'external_peer_review':False,'proof_assistant_formalization':False,
    }
    out=here/'four_ray_positive_graph_verification_v24.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','coefficient_identity_count','all_three_vertex_outgoing_maps','all_labelled_graphs_checked','graph_counts']}))


if __name__=='__main__':run()
