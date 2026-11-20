#!/usr/bin/env python3
"""Exact graph and mod-five consequences of the v23 support theorems.

This applies the arithmetic obstructions proved in the referenced text.
No earlier verification program is imported. Finite graph counts do not
assert existence of integral gluing or geometric atlases.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import json

EDGES = tuple(combinations(range(5), 2))
PERMS = tuple(permutations(range(5)))

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def relabel(edges, perm):
    return tuple(sorted(tuple(sorted((perm[a], perm[b]))) for a,b in edges))

def canonical(edges):
    return min(relabel(edges,p) for p in PERMS)

def connected(edges, removed):
    vertices=set(range(5))-set(removed)
    seen={min(vertices)}
    while True:
        expanded=seen|{b for a,b in edges if a in seen and b in vertices}
        expanded|={a for a,b in edges if b in seen and a in vertices}
        if expanded==seen:return seen==vertices
        seen=expanded

def mod_five_consequences():
    # These are the two complete residue patterns from ps11:dense.
    records=[]
    full=set(EDGES)
    for missing in combinations(EDGES,2):
        if set(missing[0])&set(missing[1]):continue
        for sign in [-1,1]:
            residues={e:0 for e in EDGES}
            residues[missing[0]]=(-sign)%5
            residues[missing[1]]=sign%5
            unit_positions=[e for e in EDGES if residues[e]==1]
            assert len(unit_positions)==1
            other=next(e for e in missing if e!=unit_positions[0])
            assert not set(other)&set(unit_positions[0])
            assert residues[other]==4 and (sum(residues[e] for e in missing)%5)==0
            assert (1+1)%5 !=0
            assert [q for q in range(1,10,2) if q%5==4]==[9]
            records.append({'missing_edges':missing,'sign':sign,
                            'residues':[[list(e),residues[e]] for e in EDGES],
                            'unique_possible_actual_unit_edge':unit_positions[0],
                            'other_edge_residue_mod_10':9})
    assert len(records)==30
    return {'all_labelled_dense_patterns':30,'records':records,
            'two_actual_unit_denominators_impossible':True,
            'one_actual_unit_forces_disjoint_other_nonmultiple_q_congruent_9_mod_10':True,
            'all_high_denominators_gcd_one_uses_unbounded_dense_prime_theorem':True,
            'any_seven_gcd_one_with_two_units_uses_unbounded_dense_prime_theorem':True,
            'finite_prime_search_used':False,'integral_lifting_claim':False}

def main():
    here=Path(__file__).resolve().parent
    full=set(EDGES)
    reps={'G5_14':full-{(1,4),(2,3)},'G5_16':full-{(3,4)},'G5_17':full}
    lookup={canonical(e):sid for sid,e in reps.items()}
    expected={'G5_14':15,'G5_16':10,'G5_17':1}
    retained=[];counts=Counter();checks=0
    for mask in range(1024):
        edges=tuple(e for i,e in enumerate(EDGES) if mask&(1<<i))
        degrees=[sum(v in e for e in edges) for v in range(5)]
        if min(degrees)<3:continue
        missing=sorted(full-set(edges))
        assert len(edges)>=8 and len(missing)<=2
        assert len({v for e in missing for v in e})==2*len(missing)
        sid=lookup[canonical(edges)];counts[sid]+=1
        for n in range(3):
            for removed in combinations(range(5),n):
                assert connected(edges,removed)
                checks+=1
        retained.append({'mask':mask,'edges':edges,'shape_id':sid,'degrees':degrees,
                         'low_edges':missing,'first_betti_number':len(edges)-4,
                         'connected_after_any_at_most_two_vertex_deletions':True})
    assert dict(counts)==expected and len(retained)==26 and checks==416
    prior=here/'support_agenda_verification_v22.json'
    old=json.loads(prior.read_text())
    assert old['passed'] and old['labelled_nonempty_supports_remaining']==56
    new_edges={tuple(x['edges']) for x in retained}
    old_edges={tuple(tuple(e) for e in x['edges']) for x in old['all_56_remaining_labelled_supports']}
    assert new_edges<old_edges
    removed=[x for x in old['all_56_remaining_labelled_supports']
             if tuple(tuple(e) for e in x['edges']) not in new_edges]
    assert len(removed)==30 and {x['shape_id'] for x in removed}=={'G5_15'}
    g515=canonical(full-{(2,3),(2,4)})
    assert all(canonical(x['edges'])==g515 for x in removed)
    shapes=[]
    for sid,edges in reps.items():
        aut=sum(set(relabel(edges,p))==edges for p in PERMS)
        assert 120//aut==expected[sid]
        shapes.append({'shape_id':sid,'representative_edges':sorted(edges),
                       'canonical_edges':canonical(edges),'automorphism_order':aut,
                       'labelled_count':expected[sid]})
    proofs=['quintic_support_frontier_v23.tex','g5_15_ordinary_outer_pair_obstruction_v23.tex',
            'g5_15_negative_exception_obstruction_v23.tex','global_primitive_denominators_v23.tex',
            'g5_15_reduction_v21.tex','book_complete_obstruction_v22.tex',
            'quintic_dense_prime_support_v11.tex']
    proof_hashes={name:digest(here.parent/'paper'/name) for name in proofs}
    result={
        'version':'v23','status':'PASS','labelled_K5_graphs_checked':1024,
        'labelled_nonempty_supports_remaining':26,'unlabelled_shapes_remaining':3,
        'shapes':shapes,'all_26_remaining_labelled_supports':retained,
        'all_30_newly_excluded_labelled_supports':removed,
        'structural_corollaries':{'minimum_degree':3,'minimum_high_edges':8,
            'minimum_first_betti_number':4,'all_five_vertices_active':True,
            'three_vertex_connected':True,'vertex_deletion_checks':checks,
            'unit_denominator_edges_form_matching_if_high_support_nonempty':True,
            'two_unit_branches_at_one_core_force_all_unit':True,
            'one_core_with_at_most_two_high_rays_forces_all_unit':True,
            'three_unit_branches_force_all_unit':True},
        'primitive_denominator_corollaries':mod_five_consequences(),
        'arithmetic_obstructions_applied_not_proved_by_graph_enumeration':True,
        'existence_claim':False,'no_denominator_or_entry_cutoff':True,
        'previous_certificate':{'file':prior.name,'sha256':digest(prior)},
        'proof_sha256':proof_hashes[proofs[0]],'proof_source_sha256':proof_hashes,
        'source_sha256':digest(Path(__file__)),
        'empty_graph_status':'All unit denominators; not excluded.'}
    out=here/'support_agenda_verification_v23.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','graphs':1024,'remaining_types':3,
                      'remaining_labels':26,'removed_G5_15_labels':30,
                      'vertex_deletion_checks':checks,'dense_mod_5_patterns':30}))

if __name__=='__main__':main()
