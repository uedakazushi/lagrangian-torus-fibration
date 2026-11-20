#!/usr/bin/env python3
"""Exact finite supplement to the general two-exception low-hub obstruction.

The general proof does not enumerate denominators. This supplement uses the
already proved two exceptional denominator pairs (3,7) and (5,9), lists every
possible reverse matrix, and prunes only failed hub pair equations while
listing all node allocations. All survivors violate a positive-flow source
inequality before any unspecified ordinary denominator is chosen.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
import hashlib
import json

HERE = Path(__file__).resolve().parent
EDGES = tuple(combinations(range(4), 2))
REVERSES = (-4, -3, -2, -1, 1, 2, 3, 4)
NODE_TRIPLES = tuple((a, b, 5-a-b) for a in range(6) for b in range(6-a))
EXPECTED = {
    (2, (0,2)):(7,165), (2, (0,3)):(7,165),
    (2, (1,2)):(8,147), (2, (1,3)):(8,147), (2, (2,3)):(6,246),
    (4, (0,2)):(2,0), (4, (0,3)):(2,0),
    (4, (1,2)):(7,42), (4, (1,3)):(7,42), (4, (2,3)):(4,0),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reverse_matrices():
    trials = 0
    records = []
    for P in (2, 4):
        M = P+4
        for negative in EDGES[1:]:
            ordinary = tuple(e for e in EDGES if e not in ((0,1), negative))
            for neg_order in ((-1,-M), (-M,-1)):
                for u in product(REVERSES, repeat=4):
                    trials += 1
                    R = [[0]*4 for _ in range(4)]
                    R[0][1], R[1][0] = 1, P
                    a,b = negative
                    R[a][b], R[b][a] = neg_order
                    for (a,b),v in zip(ordinary,u):
                        R[a][b], R[b][a] = v, -v
                    if any(sum(row) != -1 for row in R):
                        continue
                    records.append({'P':P,'M':M,'positive_edge':[0,1],
                                    'negative_edge':list(negative),
                                    'ordinary_edges':[list(e) for e in ordinary],'R':R})
    assert trials == 81920
    return trials,records


def all_hub_nodes(R):
    options=[]
    for i in range(4):
        labels=[j for j in range(4) if j!=i]
        rows=[]
        for nt in NODE_TRIPLES:
            n=[0]*4;v=[0]*4
            for j,x in zip(labels,nt):
                n[j]=x;v[j]=1-R[i][j]-x
            assert sum(n)==5 and sum(v)==-1
            rows.append((n,v))
        options.append(rows)

    def descend(N,V):
        i=len(N)
        if i==4:
            assert all(V[a][b]*V[b][a]==0 for a,b in EDGES)
            yield N,V
            return
        for n,v in options[i]:
            if any(v[j]*V[j][i]!=0 for j in range(i)):
                continue
            yield from descend(N+[n],V+[v])
    yield from descend([],[])


def source_obstruction(R,ordinary,N):
    d=[sum(N[j][i] for j in range(4))-5 for i in range(4)]
    assert sum(d)==0
    for i in range(4):
        adjacent=[j if i==k else k for j,k in ordinary if i in (j,k)]
        if not adjacent or not all(R[i][j]>0 for j in adjacent):
            continue
        terms=[{'target':j,'reverse':R[i][j],
                'minimum_X':2 if R[i][j]%2 else 1,
                'minimum_W':R[i][j]+(2 if R[i][j]%2 else 1)} for j in adjacent]
        minimum=sum(t['minimum_W'] for t in terms)
        if d[i]<minimum:
            return {'vertex':i,'d':d,'ordinary_edges_all_outgoing':True,
                    'lower_bound_terms':terms,'minimum_outgoing_weight':minimum,
                    'deficit':minimum-d[i]}
    raise AssertionError('A hub candidate without a source obstruction was found')


def main():
    assert len(NODE_TRIPLES)==21
    trials,reverses=reverse_matrices()
    groups=Counter();node_groups=Counter();sources=Counter();records=[]
    for index,rec in enumerate(reverses):
        key=(rec['P'],tuple(rec['negative_edge']))
        groups[key]+=1
        node_count=0
        for N,V in all_hub_nodes(rec['R']):
            node_count+=1
            obstruction=source_obstruction(rec['R'],rec['ordinary_edges'],N)
            sources[obstruction['vertex']]+=1
            records.append({'reverse_index':index,'N':N,'V':V,'obstruction':obstruction})
        rec['compatible_hub_node_count']=node_count
        node_groups[key]+=node_count
    assert len(reverses)==58 and len(records)==954
    assert {k:(groups[k],node_groups[k]) for k in groups}==EXPECTED
    assert sources=={0:120,1:168,2:333,3:333}
    source=HERE/'k4_two_exception_obstruction_v17.tex'
    if not source.is_file():source=HERE.parent/'papers/sections/paper'/source.name
    result={
        'version':'v17','passed':True,
        'scope':'Complete finite supplement to the general exclusion of exactly two exceptional edges in K4 high support with an all-low hub.',
        'general_proof':'Three cases according to whether the positive exceptional edge misses the large negative endpoint, meets it in the large reverse, or meets it in the unit reverse.',
        'assumptions':['Integer local row sums and high-low pair products',
                       'Odd high denominators', 'Common-low-puncture marked clutching',
                       'Hub low-low pair products', 'Nonnegative node triples of sum five',
                       'D opposition on the four edges joining the hub'],
        'not_assumed':['Positive weights','Classification of three-high local cores',
                       'D opposition on high edges','An arbitrary denominator or numerator cutoff'],
        'normalization':'The positive exceptional edge is 01, with its unit reverse at 0; the remaining labels are kept.',
        'finite_supplement_uses_prior_exceptional_pairs':[[3,7],[5,9]],
        'general_proof_requires_prior_pair_list':False,
        'reverse_assignment_trials':trials,'reverse_matrices':len(reverses),
        'node_allocations_per_row':21,'logical_node_allocation_space_per_reverse':21**4,
        'node_enumeration_pruning':'Only an already failed low-low hub pair product prunes a partial row assignment.',
        'compatible_hub_node_allocations':len(records),'source_obstruction_counts':dict(sources),
        'arbitrary_denominator_cutoff':None,'ordinary_denominators_enumerated':False,
        'group_counts':[{'P':P,'negative_edge':list(e),'reverse_count':groups[P,e],
                         'hub_count':node_groups[P,e]} for P,e in EXPECTED],
        'reverse_data':reverses,'hub_data':records,
        'source_sha256':{source.name:sha(source)},'script_sha256':sha(Path(__file__)),
        'external_peer_review':False,'proof_assistant_formalization':False,
    }
    target=HERE/'k4_two_exception_obstruction_verification_v17.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'reverse_matrices':58,'hub_allocations':954,
                      'all_excluded_by_source_flow':True,'result':str(target)}))


if __name__=='__main__':
    main()
