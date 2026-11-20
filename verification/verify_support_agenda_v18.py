#!/usr/bin/env python3
"""Complete v18 audit of all 1024 high-support graphs.

Old graph obstructions are re-applied independently. The new exclusions are
exact whole-support isomorphism types G5_5, G5_10 and G5_12, never merely
subgraph-containment conditions. Stable IDs are checked against v17 data.
No denominator or matrix-entry cutoff occurs. Standard library only.
"""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ALL_PERMUTATIONS = tuple(permutations(range(5)))
ALL_EDGES = tuple(combinations(range(5), 2))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def adjacency(edges):
    adj = {v: set() for v in range(5)}
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    return adj


def canonical_edges(edges):
    return min(tuple(sorted(tuple(sorted((p[i], p[j]))) for i, j in edges))
               for p in ALL_PERMUTATIONS)


def triangles(edges):
    es = {tuple(sorted(e)) for e in edges}
    return [list(t) for t in combinations(range(5), 3)
            if all(e in es for e in combinations(t, 2))]


def active_components(adj):
    active = {v for v in range(5) if adj[v]}
    components = []
    while active:
        start = min(active)
        found, stack = {start}, [start]
        while stack:
            v = stack.pop()
            for w in adj[v] - found:
                found.add(w)
                stack.append(w)
        active -= found
        components.append(found)
    return components


def prior_filter(edges):
    """Previously proved exclusions, in the unchanged v16 ledger order."""
    if not edges:
        return 'empty_support'
    adj = adjacency(edges)
    comps = active_components(adj)
    if any(sum(len(adj[v]) for v in c) // 2 == len(c) - 1 for c in comps):
        return 'tree_component'
    if any(all(len(adj[v]) == 2 for v in c) for c in comps):
        return 'pure_cycle_component'
    for i, j in edges:
        if len(adj[i]) == len(adj[j]) == 2 and adj[i] - {j} == adj[j] - {i}:
            return 'triangle_with_two_degree_two_vertices'
    leaves = [v for v in range(5) if len(adj[v]) == 1]
    if len(leaves) == 1:
        square = set(range(5)) - set(leaves)
        if all(len(adj[v] & square) == 2 for v in square):
            return 'C4_with_pendant_edge'
    if len(edges) == 5 and sorted(map(len, adj.values())) == [0, 2, 2, 3, 3]:
        return 'diamond'
    centers = {v for v in range(5) if len(adj[v]) == 3}
    legs = {v for v in range(5) if len(adj[v]) == 2}
    if (len(centers) == 2 and len(legs) == 3
            and all(adj[v] == legs for v in centers)
            and all(adj[v] == centers for v in legs)):
        return 'K2_3'
    ts = triangles(edges)
    if len(edges) == 5 and len(ts) == 1:
        cycle = set(ts[0])
        outside = set(range(5)) - cycle
        if all(len(adj[v]) == 1 for v in outside):
            neighbors = [next(iter(adj[v])) for v in sorted(outside)]
            if len(set(neighbors)) == 2 and set(neighbors) <= cycle:
                return 'two_leaf_triangle'
    return None


def exact_four_active_vertex_K4(edges):
    # The equality of the whole support is essential here.
    return (len(edges) == 6
            and sorted(map(len, adjacency(edges).values())) == [0, 3, 3, 3, 3])


def contains_K4(edges):
    es = set(edges)
    return any(all(e in es for e in combinations(vertices, 2))
               for vertices in combinations(range(5), 4))


def common_low_punctures(edges):
    adj = adjacency(edges)
    return [dict(high_edge=[i, j], common_low_core=k)
            for i, j in sorted(edges) for k in range(5)
            if k not in (i, j) and k not in adj[i] and k not in adj[j]]


def degree_two_triangles(adj):
    result = []
    for v in range(5):
        if len(adj[v]) != 2:
            continue
        i, j = sorted(adj[v])
        result.append({'vertex': v, 'neighbors': [i, j],
                       'neighbor_edge_high': j in adj[i],
                       'triangle': sorted((v, i, j)) if j in adj[i] else None})
    return result


def main():
    previous = HERE / 'support_agenda_verification_v17.json'
    old = json.loads(previous.read_text())
    assert old['passed'] and old['version'] == 'v17'
    assert old['unlabelled_shapes_remaining'] == 11
    assert old['labelled_nonempty_supports_remaining'] == 356
    old_shapes = {canonical_edges(s['canonical_edges']): s for s in old['shapes']}
    assert len(old_shapes) == 11
    new_definitions = {
        'G5_5': {'edges': [(0,1),(0,2),(0,3),(1,2),(1,4),(3,4)],
                 'theorem': 'hs18:no-house', 'labelled_count': 60},
        'G5_10': {'edges': [(0,1),(0,2),(0,3),(1,2),(1,3),(2,4),(3,4)],
                  'theorem': 'gten18:no-support', 'labelled_count': 30},
        'G5_12': {'edges': [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(2,3)],
                  'theorem': 'lh18:no-K4-leaf', 'labelled_count': 20}}
    new_by_canonical = {canonical_edges(v['edges']): key
                        for key,v in new_definitions.items()}
    assert len(new_by_canonical) == 3
    for can, key in new_by_canonical.items():
        assert old_shapes[can]['shape_id'] == key
    expected_remaining = {'G5_7':60, 'G5_9':60, 'G5_11':60, 'G5_13':10,
                          'G5_14':15, 'G5_15':30, 'G5_16':10, 'G5_17':1}
    ledger, old_counts, remaining_counts, removed_counts = Counter(), Counter(), Counter(), Counter()
    removed, remaining = [], []
    degree_two_checks = 0
    for mask in range(1 << len(ALL_EDGES)):
        edges = [e for bit,e in enumerate(ALL_EDGES) if mask & (1 << bit)]
        reason = prior_filter(edges)
        if reason:
            ledger[reason] += 1
            continue
        if exact_four_active_vertex_K4(edges):
            ledger['K4_with_isolated_vertex'] += 1
            continue
        can = canonical_edges(edges)
        assert can in old_shapes
        shape_id = old_shapes[can]['shape_id']
        old_counts[can] += 1
        if can in new_by_canonical:
            assert new_by_canonical[can] == shape_id
            ledger[shape_id + '_v18_exclusion'] += 1
            removed_counts[shape_id] += 1
            removed.append({'edges':edges, 'shape_id':shape_id,
                            'theorem':new_definitions[shape_id]['theorem']})
            continue
        adj = adjacency(edges)
        comps = active_components(adj)
        assert len(comps) == 1 and comps[0] == set(range(5))
        assert len(edges) >= 6 and len(edges)-4 >= 2 and triangles(edges)
        d2 = degree_two_triangles(adj)
        assert all(x['neighbor_edge_high'] for x in d2)
        degree_two_checks += len(d2)
        leaves = [v for v in range(5) if len(adj[v]) == 1]
        assert (len(edges) == 6) == bool(leaves)
        if leaves:
            assert len(leaves) == 1 and shape_id in ('G5_7','G5_9')
        else:
            assert len(edges) >= 7
        ledger['remaining'] += 1
        remaining_counts[can] += 1
        remaining.append({'edges':edges, 'shape_id':shape_id,
                          'active_vertices':list(range(5)), 'cycle_rank':len(edges)-4,
                          'degree_two_triangle_checks':d2, 'leaves':leaves})

    expected_ledger = {
        'empty_support':1, 'tree_component':300, 'pure_cycle_component':37,
        'triangle_with_two_degree_two_vertices':165, 'C4_with_pendant_edge':60,
        'diamond':30, 'K2_3':10, 'two_leaf_triangle':60,
        'K4_with_isolated_vertex':5,
        'G5_5_v18_exclusion':60, 'G5_10_v18_exclusion':30,
        'G5_12_v18_exclusion':20, 'remaining':246}
    assert dict(ledger) == expected_ledger and sum(ledger.values()) == 1024
    assert len(old_counts) == 11 and sum(old_counts.values()) == 356
    assert len(remaining_counts) == 8 and sum(remaining_counts.values()) == 246
    assert dict(removed_counts) == {k:v['labelled_count'] for k,v in new_definitions.items()}
    assert len(removed) == 110

    shapes, excluded = [], []
    for can, shape in old_shapes.items():
        assert old_counts[can] == shape['labelled_K5_count']
        es = [tuple(e) for e in shape['canonical_edges']]
        aut = sum({tuple(sorted((p[i],p[j]))) for i,j in es} == set(es)
                  for p in ALL_PERMUTATIONS)
        assert aut == shape['automorphism_order']
        assert 120 // aut == shape['labelled_K5_count']
        if can not in remaining_counts:
            key = shape['shape_id']
            assert key in new_definitions
            excluded.append({**shape, 'v18_exclusion':'exact_whole_support_type',
                             'theorem':new_definitions[key]['theorem']})
            continue
        adj = adjacency(es)
        d2 = degree_two_triangles(adj)
        leaves = [v for v in range(5) if len(adj[v]) == 1]
        assert all(x['neighbor_edge_high'] for x in d2)
        assert shape['labelled_K5_count'] == expected_remaining[shape['shape_id']]
        shapes.append({**shape, 'triangles':triangles(es),
                       'degree_two_triangle_checks':d2,
                       'two_high_vertices_forced_positive_by_low_neighbor_edge':[],
                       'common_low_puncture_triples':common_low_punctures(es),
                       'contains_K4_as_subgraph':contains_K4(es), 'leaves':leaves,
                       'six_edges_iff_leaf': (len(es)==6)==bool(leaves)})
    assert len(shapes) == 8 and len(excluded) == 3
    by_id = {s['shape_id']:s for s in shapes}
    assert set(by_id) == set(expected_remaining)
    assert {s['shape_id'] for s in shapes if s['edges_count']==6} == {'G5_7','G5_9'}
    assert {s['shape_id'] for s in shapes if s['leaves']} == {'G5_7','G5_9'}
    assert {s['shape_id'] for s in shapes if s['contains_K4_as_subgraph']} == {'G5_15','G5_16','G5_17'}
    assert Counter(len(s['edges']) for s in remaining) == {6:120,7:70,8:45,9:10,10:1}
    # Recheck the local obstruction that has disappeared from the frontier.
    previous_forced = [(s['shape_id'], s['two_high_vertices_forced_positive_by_low_neighbor_edge'])
                       for s in old['shapes'] if s['two_high_vertices_forced_positive_by_low_neighbor_edge']]
    assert previous_forced == [('G5_5',[3,4]),('G5_10',[4])]
    expected_common = {
        'G5_7': [([0,1],4),([0,3],4),([1,3],4),([2,4],3)],
        'G5_9': [([1,2],4),([1,3],4)],
        'G5_11':[([1,3],4),([2,4],3)],
        'G5_13':[], 'G5_14':[], 'G5_15':[([2,3],4)], 'G5_16':[], 'G5_17':[]}
    for key, pairs in expected_common.items():
        assert by_id[key]['common_low_puncture_triples'] == [
            {'high_edge':edge,'common_low_core':k} for edge,k in pairs]

    sources = {
        'quintic_support_frontier_v18.tex': HERE.parent/'papers/sections/paper/quintic_support_frontier_v18.tex',
        'notes_support_agenda_v18.tex': HERE.parent/'papers/sections/notes/notes_support_agenda_v18.tex',
        'three_high_matching_v18.tex': HERE.parent/'papers/sections/paper/three_high_matching_v18.tex',
        'house_support_obstruction_v18.tex': HERE.parent/'papers/sections/paper/house_support_obstruction_v18.tex',
        'g5_10_obstruction_v18.tex': HERE.parent/'papers/sections/paper/g5_10_obstruction_v18.tex',
        'k4_leaf_obstruction_v18.tex': HERE.parent/'papers/sections/paper/k4_leaf_obstruction_v18.tex'}
    result = {
        'version':'v18', 'passed':True,
        'scope':'Complete finite graph audit of necessary support conditions. Remaining graphs are not asserted to admit simultaneous integer charts, atlases, or fibrations.',
        'graph_hypotheses':['positive local integer charts','integer marked clutching',
                            'opposing D cancellation','nonnegative nodes','standard quintic K5 branch graph'],
        'denominator_or_entry_cutoff':None,
        'labelled_K5_graphs_checked':1024,
        'labelled_nonempty_supports_remaining':246,
        'unlabelled_shapes_remaining':8,
        'four_vertex_shapes':0, 'five_vertex_shapes':8,
        'canonical_rule':old['canonical_rule'],
        'shape_identifiers_preserved_from_prior_versions':True,
        'excluded_counts_in_filter_order':{k:v for k,v in expected_ledger.items() if k!='remaining'},
        'intermediate_candidate_counts':[686,521,461,431,421,361,356,296,266,246],
        'newly_excluded_shapes':excluded,
        'new_exclusion_labelled_counts':dict(removed_counts),
        'all_110_newly_excluded_labelled_supports':removed,
        'remaining_counts_by_high_edge_number':{str(k):v for k,v in sorted(Counter(len(s['edges']) for s in remaining).items())},
        'structural_corollaries':{
            'every_nonempty_support_connected_on_all_five_vertices':True,
            'one_all_low_core_forces_all_denominators_one':True,
            'every_nonempty_support_contains_a_triangle':True,
            'triangle_free_support_forces_all_denominators_one':True,
            'minimum_first_betti_number':2, 'minimum_high_edges':6,
            'every_degree_two_vertex_lies_on_triangle':True,
            'degree_two_vertex_checks_across_all_labelled_candidates':degree_two_checks,
            'six_high_edges_iff_a_leaf_exists':True,
            'leaf_exists_implies_exactly_one_leaf':True,
            'six_edge_shape_ids':['G5_7','G5_9'],
            'minimum_high_edges_without_leaf':7,
            'previous_forced_positive_degree_two_shapes_now_excluded':previous_forced},
        'shapes':shapes,
        'all_246_remaining_labelled_supports':remaining,
        'research_priorities':[
            {'shape_ids':['G5_7','G5_9'],
             'next':'Extend the full one-high-leaf normal form and marked coefficient transfer to its three-high or four-high neighbor. The existing leaf-to-degree-two transfer theorem does not apply directly. Retain all low-low freedoms and both branches at remaining degree-two cores.'},
            {'shape_ids':['G5_11','G5_13'],
             'next':'Compare all positive and negative two-high branches using low-edge nodes. G5_11 has common-low triples (13;4),(24;3); G5_13 has none, so no blanket ordinary reverse bound is imposed.'},
            {'shape_ids':['G5_14','G5_15','G5_16','G5_17'],
             'next':'Use three-high matching only at degree-three cores, fixed-low quadratic reconstruction, and dense prime-support lifting. The degree-two core in G5_15 may be on the negative branch.'}],
        'resolved_do_not_reopen':[
            'G5_5 house support', 'G5_10 support', 'G5_12 K4 plus high leaf',
            'G4_3 exact K4 support', 'G5_3 two-leaf triangle', 'G4_2 diamond', 'G5_6 K2,3'],
        'local_conditions':{
            'ordinary_common_low_reverse_absolute_value_at_most':4,
            'ordinary_bound_uses_D_opposition':False,
            'general_three_high_positive_sign_graph':'perfect_matching; theorem mh18:matching',
            'general_nonnegative_high_D_question':'open',
            'remaining_degree_two_negative_branches_must_be_retained':True},
        'limitations':[
            'The graph audit applies proved arithmetic obstructions; enumeration is not a replacement for those proofs.',
            'New removals concern equality of the whole high-support graph. The remaining G5_15, G5_16, G5_17 contain K4 subgraphs and are not removed for that reason.',
            'Every remaining degree-two vertex lies on a high triangle; this does not prove that its negative local branch can be globally realized.',
            'Local matrix families or surviving support graphs are not simultaneous five-core charts or geometric atlases.',
            'The scope is the specified standard quintic model, not all surfaces of general type or all Lagrangian torus fibrations.'],
        'previous_certificate':{'file':previous.name,'sha256':sha(previous)},
        'source_sha256':{name:sha(path) for name,path in sources.items()},
        'script_sha256':sha(Path(__file__))}
    output = HERE/'support_agenda_verification_v18.json'
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'graphs':1024,'newly_removed_labelled':110,
                      'remaining_shapes':8,'remaining_labelled':246,
                      'degree_two_triangle_checks':degree_two_checks,
                      'six_edges_iff_leaf':True,'certificate':str(output)},ensure_ascii=False))

if __name__=='__main__':
    main()
