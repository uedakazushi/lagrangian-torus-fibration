#!/usr/bin/env python3
"""All 1024 support graphs after the v17 exact-K4 obstruction.

The only new removal from v16 is K4 on four active vertices with the fifth
vertex isolated.  Containing a K4 subgraph is not a removal criterion.
Stable shape IDs are taken from the v16 certificate and never renumbered.
This finite graph audit is not a bounded denominator or chart search.
Only the Python standard library is used; no project module is imported.
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


def locate(name, folder='verification'):
    choices = [HERE / name, HERE.parent / folder / name,
               HERE.parent / 'root' / name,
               HERE.parent / 'four_exception' / name,
               HERE.parents[1] / 'deliverables/general_type_surface_fibration_v17' / folder / name,
               HERE.parents[1] / 'deliverables/general_type_surface_fibration_v16' / folder / name]
    return next(p for p in choices if p.is_file())


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


def main():
    previous = locate('support_agenda_verification_v16.json')
    old = json.loads(previous.read_text())
    assert old['passed'] and old['version'] == 'v16'
    assert old['unlabelled_shapes_remaining'] == 12
    assert old['labelled_nonempty_supports_remaining'] == 361
    old_shapes = {canonical_edges(s['canonical_edges']): s for s in old['shapes']}
    assert len(old_shapes) == 12

    ledger, old_counts, remaining_counts = Counter(), Counter(), Counter()
    removed, remaining = [], []
    for mask in range(1 << len(ALL_EDGES)):
        edges = [e for bit, e in enumerate(ALL_EDGES) if mask & (1 << bit)]
        reason = prior_filter(edges)
        if reason:
            ledger[reason] += 1
            continue
        canonical = canonical_edges(edges)
        assert canonical in old_shapes
        old_counts[canonical] += 1
        shape_id = old_shapes[canonical]['shape_id']
        if exact_four_active_vertex_K4(edges):
            assert shape_id == 'G4_3'
            ledger['K4_with_isolated_vertex'] += 1
            removed.append(dict(edges=edges, shape_id=shape_id,
                                isolated_vertex=next(v for v, ns in adjacency(edges).items() if not ns)))
            continue
        adj = adjacency(edges)
        comps = active_components(adj)
        assert len(comps) == 1 and comps[0] == set(range(5))
        rank = len(edges) - 4
        assert rank >= 2 and len(edges) >= 6 and max(map(len, adj.values())) >= 3
        assert triangles(edges)
        ledger['remaining'] += 1
        remaining_counts[canonical] += 1
        remaining.append(dict(edges=edges, shape_id=shape_id,
                              active_vertices=list(range(5)), cycle_rank=rank))

    expected = {
        'empty_support': 1, 'tree_component': 300, 'pure_cycle_component': 37,
        'triangle_with_two_degree_two_vertices': 165, 'C4_with_pendant_edge': 60,
        'diamond': 30, 'K2_3': 10, 'two_leaf_triangle': 60,
        'K4_with_isolated_vertex': 5, 'remaining': 356}
    assert dict(ledger) == expected and sum(ledger.values()) == 1024
    assert len(old_counts) == 12 and sum(old_counts.values()) == 361
    assert len(remaining_counts) == 11 and sum(remaining_counts.values()) == 356
    assert len(removed) == 5 and {r['isolated_vertex'] for r in removed} == set(range(5))

    shapes, excluded = [], []
    for canonical, shape in old_shapes.items():
        assert old_counts[canonical] == shape['labelled_K5_count']
        es = [tuple(e) for e in shape['canonical_edges']]
        automorphisms = sum({tuple(sorted((p[i], p[j]))) for i, j in es} == set(es)
                            for p in ALL_PERMUTATIONS)
        assert automorphisms == shape['automorphism_order']
        assert 120 // automorphisms == shape['labelled_K5_count']
        if canonical not in remaining_counts:
            assert shape['shape_id'] == 'G4_3' and automorphisms == 24
            excluded.append({**shape, 'v17_exclusion': 'exact_K4_with_isolated_vertex',
                             'theorem': 'kg17:no-K4'})
            continue
        assert remaining_counts[canonical] == shape['labelled_K5_count']
        adj = adjacency(es)
        forced = []
        for i in range(5):
            if len(adj[i]) == 2:
                j, k = sorted(adj[i])
                if k not in adj[j]:
                    forced.append(i)
        shapes.append({**shape, 'triangles': triangles(es),
                       'two_high_vertices_forced_positive_by_low_neighbor_edge': forced,
                       'common_low_puncture_triples': common_low_punctures(es),
                       'contains_K4_as_subgraph': contains_K4(es)})
    assert len(shapes) == 11 and len(excluded) == 1
    assert all(s['vertices'] == 5 and s['cycle_rank'] >= 2 and s['edges_count'] >= 6 for s in shapes)
    assert {s['shape_id'] for s in old['shapes']} - {s['shape_id'] for s in shapes} == {'G4_3'}
    assert [(s['shape_id'], s['two_high_vertices_forced_positive_by_low_neighbor_edge'])
            for s in shapes if s['two_high_vertices_forced_positive_by_low_neighbor_edge']] == [
                ('G5_5', [3, 4]), ('G5_10', [4])]
    by_id = {s['shape_id']: s for s in shapes}
    assert by_id['G5_5']['common_low_puncture_triples'] == [
        dict(high_edge=[0, 2], common_low_core=4),
        dict(high_edge=[1, 2], common_low_core=3),
        dict(high_edge=[3, 4], common_low_core=2)]
    assert by_id['G5_10']['common_low_puncture_triples'] == [dict(high_edge=[0, 1], common_low_core=4)]
    assert by_id['G5_12']['contains_K4_as_subgraph']
    assert by_id['G5_12']['labelled_K5_count'] == 20
    assert set(map(tuple, by_id['G5_12']['canonical_edges'])) == {
        (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 3)}

    source_names = [
        ('quintic_support_frontier_v17.tex', 'papers/sections/paper'),
        ('notes_support_agenda_v17.tex', 'papers/sections/notes'),
        ('k4_two_exception_obstruction_v17.tex', 'papers/sections/paper'),
        ('k4_four_exception_obstruction_v17.tex', 'papers/sections/paper'),
        ('k4_global_obstruction_v17.tex', 'papers/sections/paper'),
        ('k4_low_hub_reduction_v16.tex', 'papers/sections/paper'),
        ('common_low_node_bound_v16.tex', 'papers/sections/paper')]
    sources = {name: locate(name, folder) for name, folder in source_names}
    result = {
        'version': 'v17', 'passed': True,
        'scope': 'Complete finite graph audit of necessary support conditions. Surviving graphs are not asserted to admit integer charts, atlases, or fibrations.',
        'graph_hypotheses': ['positive integer local charts', 'integer marked clutching',
                             'opposing D cancellation', 'nonnegative nodes',
                             'standard quintic K5 branch graph'],
        'denominator_or_entry_cutoff': None,
        'labelled_K5_graphs_checked': 1024,
        'labelled_nonempty_supports_remaining': 356,
        'unlabelled_shapes_remaining': 11,
        'four_vertex_shapes': 0, 'five_vertex_shapes': 11,
        'canonical_rule': old['canonical_rule'],
        'shape_identifiers_preserved_from_v13_v14_v15_v16': True,
        'excluded_counts_in_filter_order': {k: v for k, v in expected.items() if k != 'remaining'},
        'intermediate_candidate_counts': [686, 521, 461, 431, 421, 361, 356],
        'newly_excluded_shapes': excluded,
        'all_5_newly_excluded_labelled_supports': removed,
        'structural_corollaries': {
            'every_nonempty_support_connected_on_all_five_vertices': True,
            'every_nonempty_support_has_no_isolated_vertex': True,
            'one_all_low_core_forces_all_denominators_one': True,
            'every_nonempty_support_contains_a_triangle': True,
            'triangle_free_support_forces_all_denominators_one': True,
            'minimum_first_betti_number': 2, 'minimum_high_edges': 6,
            'four_active_vertex_candidates_remaining': 0,
            'unicyclic_candidates_remaining': 0,
            'triangle_free_nonempty_candidates_remaining': 0},
        'shapes': shapes,
        'all_356_remaining_labelled_supports': remaining,
        'research_priorities': [
            {'shape_id': 'G5_5',
             'status': 'Open; degree-two vertices 3 and 4 are on the positive branch; vertex 2 may remain negative.',
             'next': 'Apply the ordinary common-low reverse bound at (02;4),(12;3),(34;2), retaining maximal-divisor exceptions and combining node data with fixed-low-row/column local completion.'},
            {'shape_id': 'G5_10',
             'status': 'Open; degree-two vertex 4 is on the positive branch.',
             'next': 'Apply the ordinary common-low reverse bound at (01;4), then the positive degree-two chart and marked adjacent edges.'},
            {'shape_id': 'G5_12',
             'status': 'Open; this is K4 plus one leaf and is outside the all-low-hub theorem.',
             'next': 'Use the one-high hub chart with q_04>1. Three hub pair products become q_04-1; incorporate the three low hub edges and the unique high hub edge without importing all-low pair-zero conditions.'},
            {'shape_ids': ['G5_7', 'G5_9'], 'status': 'Open leaf-containing supports.',
             'next': 'Transfer the one-high-core and leaf-adjacency constraints to the neighboring core.'}],
        'resolved_do_not_reopen': [
            'G4_3 exact K4 support, including its two-exception and four-exception branches',
            'G5_3 two-leaf triangle, including crossed positive z=1 branches and B-label exceptions',
            'G4_2 diamond', 'G5_6 K2,3'],
        'local_conditions': {
            'ordinary_common_low_reverse_absolute_value_at_most': 4,
            'ordinary_bound_uses_D_opposition': False,
            'ordinary_bound_restricts_neighbor_high_degrees': False,
            'general_three_high_matching_classification': 'open',
            'general_nonnegative_high_D_question': 'open'},
        'limitations': [
            'The finite graph audit applies previously proved obstructions; it does not prove those integer or geometric obstructions by graph enumeration.',
            'The new exclusion requires that the entire high support be K4 on four active vertices. Containing a K4 subgraph is not an exclusion criterion; G5_12 remains.',
            'A local integer family or a surviving graph is not a simultaneous five-core chart or a geometric atlas.',
            'The agenda does not classify all general-type surfaces or all Lagrangian torus fibrations.'],
        'previous_certificate': {'file': previous.name, 'sha256': sha(previous)},
        'source_sha256': {name: sha(path) for name, path in sources.items()},
        'script_sha256': sha(Path(__file__))}
    output = HERE / 'support_agenda_verification_v17.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'passed': True, 'graphs': 1024, 'newly_removed_labelled': 5,
                      'remaining_shapes': 11, 'remaining_labelled': 356,
                      'all_nonempty_candidates_connected_on_five_vertices': True,
                      'certificate': str(output)}))


if __name__ == '__main__':
    main()
