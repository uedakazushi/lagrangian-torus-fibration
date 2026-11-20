#!/usr/bin/env python3
"""Independent known-row obstruction for all 52 proof-derived low patches.

The input certificate contains the finite leaf reconstruction, whose completeness
is proved in two_leaf_unit_finiteness_v16.tex and r1_exceptional_leaf_v16.tex.
This checker does not import the leaf generator or its center reconstruction.
It recomputes original core/edge conditions and all 21^3 known-row candidates
at each center. Neither q01 nor the missing row nor center D is used.
"""
from pathlib import Path
from itertools import combinations, permutations, product
from fractions import Fraction
import hashlib
import json

HERE = Path(__file__).resolve().parent
NODES = tuple((a, b, 5-a-b) for a in range(6) for b in range(6-a))
EXPECTED = {
    (1,4,1,3,12): (21,0), (1,7,1,4,18): (3,0),
    (1,4,1,8,36): (4,0), (1,15,1,12,64): (3,0),
    (2,4,1,3,6): (4,0), (2,4,1,12,30): (5,0),
    (2,5,1,14,36): (1,0), (4,4,1,18,30): (1,1),
    (4,4,1,35,60): (8,0), (4,4,1,52,90): (2,0),
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def locate(name, source=False):
    choices = ([HERE/name, HERE.parent/'paper'/name, HERE.parent/'z1'/name,
                HERE.parent/'small_r'/name] if source else
               [HERE/name, HERE.parent/'z1'/name, HERE.parent/'small_r'/name])
    return next(p for p in choices if p.is_file())


def normalize(raw, core):
    P = {int(i): {int(j): x for j,x in row.items()} for i,row in raw['p'].items()}
    labels = sorted(set(range(5))-{core})
    assert sorted(P) == labels and all(sorted(row)==labels for row in P.values())
    if core == 2:
        q = {int(i): x for i,x in raw['qs'].items()}
    else:
        high = 0 if core == 3 else 1
        q = {i: raw['q'] if i == high else 1 for i in labels}
    assert all(type(x) is int for row in P.values() for x in row.values())
    assert all(type(x) is int and x > 0 and x % 2 == 1 for x in q.values())
    for i in labels:
        assert P[i][i] == 0 and sum(P[i].values()) == -q[i]
    for i,j in combinations(labels,2):
        assert P[i][j]*P[j][i] == q[i]*q[j]-1
    D = {i: -q[i]-sum(P[j][i] for j in labels if j!=i) for i in labels}
    assert D == {int(i): x for i,x in raw['D'].items()}
    cycle_count = 0
    for n in (2,3,4):
        for cyc in permutations(labels,n):
            if cyc[0] != min(cyc):
                continue
            gain = Fraction(1)
            for i,j in zip(cyc,cyc[1:]+cyc[:1]):
                if P[i][j] <= 0:
                    break
                gain *= Fraction(P[i][j],q[i])
            else:
                assert gain < 1
                cycle_count += 1
    return {'p':P,'q':q,'D':D,'positive_simple_cycles_checked':cycle_count}


def edge_check(i,j,cores):
    a,b = cores[i],cores[j]
    q = a['q'][j]
    assert q == b['q'][i] == 1
    ks = sorted(set(range(5))-{i,j})
    sums = [a['p'][j][k]+b['p'][i][k] for k in ks]
    nodes = [1-s for s in sums]
    assert sum(nodes)==5 and all(0<=n<=5 for n in nodes)
    assert a['D'][j]+b['D'][i]==0
    return {'edge':[i,j],'punctures':ks,'nodes':nodes,'D_sum':0}


def known_rows(center,cores):
    labels = sorted(set(range(5))-{center})
    q = {j: cores[j]['q'][center] for j in (2,3,4)}
    options = {}
    for j in (2,3,4):
        ks = [k for k in labels if k!=j]
        options[j] = []
        for nt in NODES:
            row = {j:0}
            row.update({k:q[j]*(1-n)-cores[j]['p'][center][k] for k,n in zip(ks,nt)})
            assert sum(row.values()) == -q[j]
            options[j].append(row)
    rejected = {'23':0,'24':0,'34':0}
    compatible = []
    for indices in product(range(21),repeat=3):
        rows = {j:options[j][indices[j-2]] for j in (2,3,4)}
        for j,k in ((2,3),(2,4),(3,4)):
            if rows[j][k]*rows[k][j] != q[j]*q[k]-1:
                rejected[str(j)+str(k)] += 1
                break
        else:
            compatible.append(list(indices))
    assert sum(rejected.values())+len(compatible)==21**3
    return {'center':center,'known_denominators':q,'tested_node_row_triples':21**3,
            'rejected_by_first_failed_pair':rejected,
            'compatible_count':len(compatible),'compatible_node_indices':compatible}


def main():
    primary = locate('two_leaf_unit_finiteness_certificate_v16.json')
    primary_script = locate('verify_two_leaf_unit_finiteness_v16.py')
    data = json.loads(primary.read_text())
    assert data['passed'] and data['script_sha256']==sha(primary_script)
    assert data['surviving_middle_count']==10 and data['surviving_low_patch_count']==52
    for name,digest in data['source_sha256'].items():
        assert sha(locate(name,source=True))==digest
    assert len(NODES)==21
    seen_parameters=set()
    records=[]
    center_choices={0:0,1:0}
    for survivor in data['survivors']:
        params=survivor['parameters']
        key=tuple(params[k] for k in ('r','s','z','S','T'))
        assert key in EXPECTED and key not in seen_parameters
        seen_parameters.add(key)
        count,chosen=EXPECTED[key]
        patches=survivor['low_patches']
        assert len(patches)==count
        fingerprints=set()
        for index,patch in enumerate(patches):
            cores={2:normalize(patch['middle'],2),3:normalize(patch['leaf3'],3),
                   4:normalize(patch['leaf4'],4)}
            assert cores[2]['q'][0]==params['s']*params['S']+1
            assert cores[2]['q'][1]==params['T']+1
            fingerprint=tuple((i,tuple(sorted(cores[i]['q'].items())),
                               tuple((a,b,cores[i]['p'][a][b]) for a in sorted(cores[i]['p'])
                                     for b in sorted(cores[i]['p'][a]))) for i in (3,4))
            assert fingerprint not in fingerprints
            fingerprints.add(fingerprint)
            low_edges=[edge_check(i,j,cores) for i,j in ((2,3),(2,4),(3,4))]
            checks=[known_rows(i,cores) for i in (0,1)]
            assert checks[chosen]['compatible_count']==0
            center_choices[chosen]+=1
            records.append({'parameters':params,'low_patch_index':index,
                            'leaf_denominators':[cores[3]['q'][0],cores[4]['q'][1]],
                            'local_original_conditions':'passed','low_edges':low_edges,
                            'obstructing_center':chosen,'centers':checks})
    assert seen_parameters==set(EXPECTED) and len(records)==52
    assert center_choices=={0:51,1:1}
    source=locate('two_leaf_global_obstruction_v16.tex',source=True)
    result={
        'version':'v16','passed':True,'script_sha256':sha(Path(__file__)),
        'source_sha256':{source.name:sha(source)},
        'dependency_sha256':{primary.name:sha(primary),primary_script.name:sha(primary_script)},
        'independence':'No import of the leaf generator or its center solver. Leaf list completeness relies on the cited proved finite reduction; original local/low-edge conditions and all center node allocations are checked directly.',
        'middle_models':10,'low_patches':52,'node_allocations_per_row':21,
        'node_row_triples_per_center':21**3,'obstructing_center_counts':center_choices,
        'unknown_center_denominator_used':False,'center_D_opposition_used':False,
        'center_positive_weights_used':False,'arbitrary_denominator_cutoff':None,
        'external_peer_review':False,'proof_assistant_formalization':False,'records':records
    }
    target=HERE/'two_leaf_center_obstruction_v16.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'middle_models':10,'low_patches':52,
                      'obstructing_center_counts':center_choices,'result':str(target)}))


if __name__=='__main__':
    main()
