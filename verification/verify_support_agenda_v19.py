#!/usr/bin/env python3
"""Complete graph audit for v19: no leaf, six necessary support types.

Apply the proved whole-support exclusions to all 1024 labelled graphs.
The old graph predicates are imported unchanged, without running the old main.
No denominator, numerator, or free-parameter cutoff occurs here.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json
from verify_support_agenda_v18 import (
    ALL_EDGES, ALL_PERMUTATIONS, adjacency, canonical_edges, triangles,
    active_components, prior_filter, exact_four_active_vertex_K4,
    common_low_punctures, degree_two_triangles, contains_K4)

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def connected_after_deletion(edges, removed):
    vertices = set(range(5)) - set(removed)
    if not vertices:
        return True
    adj = adjacency(edges)
    seen, stack = {min(vertices)}, [min(vertices)]
    while stack:
        for j in adj[stack.pop()] & vertices - seen:
            seen.add(j)
            stack.append(j)
    return seen == vertices


def complement_type(edges):
    low = sorted(set(ALL_EDGES)-set(edges))
    degrees = sorted((len(s) for s in adjacency(low).values()), reverse=True)
    types = {(0, (0,0,0,0,0)): 'empty', (1, (1,1,0,0,0)): 'K2',
             (2, (2,1,1,0,0)): 'P3', (2, (1,1,1,1,0)): '2K2',
             (3, (2,2,2,0,0)): 'K3', (3, (2,2,1,1,0)): 'P4'}
    return types[len(low), tuple(degrees)], low


def main():
    previous = HERE/'support_agenda_verification_v18.json'
    old = json.loads(previous.read_text())
    assert old['passed'] and old['unlabelled_shapes_remaining'] == 8
    assert old['labelled_nonempty_supports_remaining'] == 246
    old_shapes = {canonical_edges(s['canonical_edges']):s for s in old['shapes']}
    prior = {
        canonical_edges([(0,1),(0,2),(0,3),(1,2),(1,4),(3,4)]):'G5_5',
        canonical_edges([(0,1),(0,2),(0,3),(1,2),(1,3),(2,4),(3,4)]):'G5_10',
        canonical_edges([(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(2,3)]):'G5_12'}
    new = {'G5_7':'g719:no-G5-7', 'G5_9':'dl19:no-G5-9'}
    expected = {'G5_11':60, 'G5_13':10, 'G5_14':15,
                'G5_15':30, 'G5_16':10, 'G5_17':1}
    expected_low = {'G5_11':'P4', 'G5_13':'K3', 'G5_14':'2K2',
                    'G5_15':'P3', 'G5_16':'K2', 'G5_17':'empty'}
    ledger, remaining_counts, removed_counts = Counter(), Counter(), Counter()
    removed, remaining = [], []
    degree_two_count = 0
    for mask in range(1024):
        edges = [e for b,e in enumerate(ALL_EDGES) if mask & (1 << b)]
        reason = prior_filter(edges)
        if reason:
            ledger[reason] += 1
            continue
        if exact_four_active_vertex_K4(edges):
            ledger['K4_with_isolated_vertex'] += 1
            continue
        can = canonical_edges(edges)
        if can in prior:
            ledger[prior[can]+'_v18_exclusion'] += 1
            continue
        assert can in old_shapes
        sid = old_shapes[can]['shape_id']
        if sid in new:
            ledger[sid+'_v19_exclusion'] += 1
            removed_counts[sid] += 1
            removed.append({'edges':edges, 'shape_id':sid, 'theorem':new[sid]})
            continue
        adj = adjacency(edges)
        assert active_components(adj) == [set(range(5))]
        assert min(map(len, adj.values())) >= 2
        assert len(edges) >= 7 and len(edges)-4 >= 3 and triangles(edges)
        checks = degree_two_triangles(adj)
        assert all(c['neighbor_edge_high'] for c in checks)
        assert all(connected_after_deletion(edges, {v}) for v in range(5))
        degree_two_count += len(checks)
        lowtype, lowedges = complement_type(edges)
        assert lowtype == expected_low[sid]
        ledger['remaining'] += 1
        remaining_counts[sid] += 1
        remaining.append({'edges':edges, 'shape_id':sid, 'low_edges':lowedges,
                          'complement_type_omitting_isolated_vertices':lowtype,
                          'degree_two_triangle_checks':checks,
                          'connected_after_each_vertex_deletion':True})
    expected_ledger = {**old['excluded_counts_in_filter_order'],
                       'G5_7_v19_exclusion':60, 'G5_9_v19_exclusion':60,
                       'remaining':126}
    assert dict(ledger) == expected_ledger
    assert sum(ledger.values()) == 1024 and len(removed) == 120
    assert dict(remaining_counts) == expected and degree_two_count == 180
    assert dict(removed_counts) == {'G5_7':60, 'G5_9':60}
    shapes = []
    for can, s in old_shapes.items():
        if s['shape_id'] not in expected:
            continue
        edges = [tuple(e) for e in s['canonical_edges']]
        aut = sum({tuple(sorted((p[i],p[j]))) for i,j in edges} == set(edges)
                  for p in ALL_PERMUTATIONS)
        assert aut == s['automorphism_order']
        assert 120//aut == expected[s['shape_id']] == s['labelled_K5_count']
        lowtype, lowedges = complement_type(edges)
        # Recompute structural fields rather than inheriting the old leaf wording.
        shapes.append({k:v for k,v in s.items() if k not in
                       ('six_edges_iff_leaf','leaves')} | {
            'low_edges':lowedges, 'complement_type_omitting_isolated_vertices':lowtype,
            'leaves':[], 'minimum_degree':min(map(len, adjacency(edges).values())),
            'two_vertex_connected':True})
    assert len(shapes) == 6
    by_edges = Counter(len(x['edges']) for x in remaining)
    assert dict(by_edges) == {7:70,8:45,9:10,10:1}
    source_paths = [HERE.parent/'paper'/name for name in (
        'g5_7_obstruction_v19.tex','g5_9_obstruction_v19.tex',
        'book_low_triangle_finiteness_v19.tex','quintic_support_frontier_v19.tex')]
    source_paths.append(HERE.parent/'notes/notes_support_agenda_v19.tex')
    result = {
        'version':'v19', 'passed':True,
        'scope':'Necessary support graphs for the specified quintic K5 integer gluing problem; no existence or geometric classification claim.',
        'labelled_K5_graphs_checked':1024,
        'labelled_nonempty_supports_remaining':126, 'unlabelled_shapes_remaining':6,
        'newly_excluded_labelled_supports':120, 'new_exclusion_labelled_counts':dict(removed_counts),
        'excluded_counts_in_filter_order':{k:v for k,v in ledger.items() if k!='remaining'},
        'canonical_rule':old['canonical_rule'],
        'shape_identifiers_preserved_from_prior_versions':True,
        'remaining_counts_by_high_edge_number':dict(sorted(by_edges.items())),
        'structural_corollaries':{
            'all_five_vertices_active':True, 'minimum_degree':2,
            'two_vertex_connected':True, 'minimum_high_edges':7,
            'minimum_first_betti_number':3,
            'one_core_with_at_most_one_high_ray_forces_all_denominators_one':True,
            'every_degree_two_vertex_lies_on_triangle':True,
            'degree_two_vertex_checks_across_all_labelled_candidates':degree_two_count,
            'remaining_low_complement_types':['P4','K3','2K2','P3','K2','empty']},
        'shapes':shapes, 'all_126_remaining_labelled_supports':remaining,
        'all_120_newly_excluded_labelled_supports':removed,
        'new_exclusion_theorems':new,
        'denominator_or_entry_cutoff':None,
        'book_status':'open; only finite exact completion for each fixed bivalent core is proved',
        'general_three_high_nonnegative_D_status':'open',
        'previous_certificate':{'file':previous.name,'sha256':sha(previous)},
        'source_sha256':{str(p.relative_to(HERE.parent)):sha(p) for p in source_paths},
        'script_sha256':sha(Path(__file__)),
        'limitations':['Whole-support exclusions are not subgraph exclusions.',
                       'Graph enumeration applies mathematical proofs and is not their replacement.',
                       'Remaining graphs do not imply integer charts, atlases, or fibrations.']}
    output = HERE/'support_agenda_verification_v19.json'
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'graphs':1024,'newly_removed':120,
                      'remaining_shapes':6,'remaining_labelled':126,
                      'two_vertex_connected':True,'output':str(output)},ensure_ascii=False))


if __name__ == '__main__':
    main()
