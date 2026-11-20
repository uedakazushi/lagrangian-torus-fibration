#!/usr/bin/env python3
"""Apply proved quintic support exclusions to all 1024 labelled graphs.

The graph audit uses the retained graph predicates and v19 stable identifiers.
It is not a substitute for the G5_11 arithmetic obstruction theorem.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json
from verify_support_agenda_v19 import (
    ALL_EDGES, ALL_PERMUTATIONS, adjacency, canonical_edges, triangles,
    active_components, prior_filter, exact_four_active_vertex_K4,
    degree_two_triangles, connected_after_deletion, complement_type)

HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    previous=HERE/'support_agenda_verification_v19.json'
    old=json.loads(previous.read_text())
    assert old['passed'] and old['unlabelled_shapes_remaining']==6
    assert old['labelled_nonempty_supports_remaining']==126
    old_shapes={canonical_edges(s['canonical_edges']):s for s in old['shapes']}
    prior={
        canonical_edges([(0,1),(0,2),(0,3),(1,2),(1,4),(3,4)]):'G5_5_v18_exclusion',
        canonical_edges([(0,1),(0,2),(0,3),(1,2),(1,3),(2,4),(3,4)]):'G5_10_v18_exclusion',
        canonical_edges([(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(2,3)]):'G5_12_v18_exclusion',
        canonical_edges([(0,1),(0,2),(0,3),(1,2),(1,3),(2,4)]):'G5_7_v19_exclusion',
        canonical_edges([(0,1),(0,2),(0,3),(0,4),(1,2),(1,3)]):'G5_9_v19_exclusion'}
    expected={'G5_13':10,'G5_14':15,'G5_15':30,'G5_16':10,'G5_17':1}
    expected_low={'G5_13':'K3','G5_14':'2K2','G5_15':'P3','G5_16':'K2','G5_17':'empty'}
    ledger=Counter();counts=Counter();remaining=[];removed=[];degree_two_count=0
    for mask in range(1024):
        edges=[e for b,e in enumerate(ALL_EDGES) if mask>>b&1]
        reason=prior_filter(edges)
        if reason:ledger[reason]+=1;continue
        if exact_four_active_vertex_K4(edges):ledger['K4_with_isolated_vertex']+=1;continue
        can=canonical_edges(edges)
        if can in prior:ledger[prior[can]]+=1;continue
        assert can in old_shapes
        sid=old_shapes[can]['shape_id']
        if sid=='G5_11':
            ledger['G5_11_v20_exclusion']+=1
            removed.append({'edges':edges,'shape_id':sid,'theorem':'g51120:no-support'})
            continue
        adj=adjacency(edges)
        assert active_components(adj)==[set(range(5))]
        assert min(map(len,adj.values()))>=2 and len(edges)>=7
        assert all(connected_after_deletion(edges,{v}) for v in range(5))
        checks=degree_two_triangles(adj)
        assert all(c['neighbor_edge_high'] for c in checks)
        for c in checks:
            c['neighbor_degrees']=[len(adj[j]) for j in c['neighbors']]
            assert c['neighbor_degrees']==[4,4]
        degree_two_count+=len(checks)
        assert len(checks) in (0,1,3)
        assert (len(edges)==7)==(sid=='G5_13')
        assert (len(checks)==3)==(sid=='G5_13')
        assert (len(checks)==1)==(sid=='G5_15')
        lowtype,lowedges=complement_type(edges)
        assert lowtype==expected_low[sid]
        ledger['remaining']+=1;counts[sid]+=1
        remaining.append({'edges':edges,'shape_id':sid,'low_edges':lowedges,
            'complement_type_omitting_isolated_vertices':lowtype,
            'degree_two_triangle_checks':checks,'connected_after_each_vertex_deletion':True})
    expected_ledger={**old['excluded_counts_in_filter_order'],'G5_11_v20_exclusion':60,'remaining':66}
    assert dict(ledger)==expected_ledger
    assert sum(ledger.values())==1024 and len(removed)==60
    assert dict(counts)==expected and degree_two_count==60
    old_labelled={tuple(tuple(e) for e in x['edges']) for x in old['all_126_remaining_labelled_supports']}
    assert {tuple(tuple(e) for e in x['edges']) for x in remaining+removed}==old_labelled
    shapes=[]
    for s in old['shapes']:
        if s['shape_id'] not in expected:continue
        edges=[tuple(e) for e in s['canonical_edges']]
        aut=sum({tuple(sorted((p[i],p[j]))) for i,j in edges}==set(edges) for p in ALL_PERMUTATIONS)
        assert aut==s['automorphism_order'] and 120//aut==expected[s['shape_id']]
        shapes.append(s | {'degree_two_neighbors_all_degree_four':True})
    by_edges=Counter(len(x['edges']) for x in remaining)
    assert dict(by_edges)=={7:10,8:45,9:10,10:1}
    source_paths=[HERE.parent/'papers/sections/paper'/n for n in (
        'g5_11_obstruction_v20.tex','book_all_negative_obstruction_v20.tex',
        'book_low_D_cycle_v20.tex','quintic_support_frontier_v20.tex')]
    source_paths.append(HERE.parent/'papers/sections/notes/notes_support_agenda_v20.tex')
    report={'version':'v20','passed':True,
        'scope':'Necessary support graphs under the prescribed quintic K5 arithmetic gluing assumptions. Candidate counts are not existence or geometric-isomorphism counts.',
        'labelled_K5_graphs_checked':1024,'labelled_nonempty_supports_remaining':66,
        'unlabelled_shapes_remaining':5,'newly_excluded_labelled_supports':60,
        'new_exclusion_labelled_counts':{'G5_11':60},
        'excluded_counts_in_filter_order':{k:v for k,v in ledger.items() if k!='remaining'},
        'canonical_rule':old['canonical_rule'],'shape_identifiers_preserved_from_prior_versions':True,
        'remaining_counts_by_high_edge_number':dict(sorted(by_edges.items())),
        'structural_corollaries':{
            'all_five_vertices_active':True,'minimum_degree':2,'two_vertex_connected':True,
            'minimum_high_edges':7,'minimum_first_betti_number':3,
            'one_core_with_at_most_one_high_ray_forces_all_denominators_one':True,
            'every_degree_two_vertex_lies_on_triangle':True,
            'every_neighbor_of_a_degree_two_vertex_has_degree_four':True,
            'degree_two_vertex_checks_across_all_labelled_candidates':60,
            'possible_degree_two_vertex_counts':[0,1,3],
            'seven_high_edges_iff_book':True,
            'remaining_low_complement_types':['K3','2K2','P3','K2','empty']},
        'shapes':shapes,'all_66_remaining_labelled_supports':remaining,
        'all_60_newly_excluded_labelled_supports':removed,
        'new_exclusion_theorems':{'G5_11':'g51120:no-support'},
        'denominator_or_entry_cutoff':None,
        'book_status':'Open. All-positive and all-negative low triangles are excluded. Every surviving low triangle must mix branches and carry a nonzero directed cycle of low D signs. Completion is finite for each fixed core.',
        'general_three_high_nonnegative_D_status':'Open in the nonsingular Schur region; the fully nonnegative high-D hypothesis excludes all singular systems.',
        'previous_certificate':{'file':previous.name,'sha256':sha(previous)},
        'source_sha256':{str(p.relative_to(HERE.parent)):sha(p) for p in source_paths},
        'script_sha256':sha(Path(__file__)),
        'limitations':['Whole-support exclusions must not be applied to arbitrary containing subgraphs.',
                       'Graph enumeration applies preceding arithmetic proofs; it does not prove those obstructions.',
                       'The remaining supports do not imply existence of integer charts, atlases, or fibrations.']}
    out=HERE/'support_agenda_verification_v20.json'
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'graphs':1024,'newly_removed':60,'remaining_shapes':5,
                      'remaining_labelled':66,'two_high_neighbor_checks':degree_two_count,'output':str(out)},ensure_ascii=False))

if __name__=='__main__':main()
