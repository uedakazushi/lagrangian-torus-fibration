#!/usr/bin/env python3
"""Independent graph audit of the v22 four-type support frontier.

This enumerates all labelled graphs, applying the proved edge-count threshold.
It does not prove the arithmetic obstructions and imports no prior verifier.
The v20 certificate is read only to compare the exact 66-to-56 difference.
"""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
EDGES = tuple(combinations(range(5), 2))
PERMS = tuple(permutations(range(5)))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def relabel(edges, perm):
    return tuple(sorted(tuple(sorted((perm[a], perm[b]))) for a, b in edges))

def canonical(edges):
    return min(relabel(edges, p) for p in PERMS)

def connected(edges, removed=None):
    vertices = set(range(5)) - ({removed} if removed is not None else set())
    seen = {min(vertices)}
    while True:
        expanded = seen | {b for a, b in edges if a in seen and b in vertices}
        expanded |= {a for a, b in edges if b in seen and a in vertices}
        if expanded == seen:
            return seen == vertices
        seen = expanded

def main():
    full = set(EDGES)
    representatives = {
        'G5_14': full - {(1, 4), (2, 3)},
        'G5_15': full - {(2, 3), (2, 4)},
        'G5_16': full - {(3, 4)},
        'G5_17': full,
    }
    lookup = {canonical(e): sid for sid, e in representatives.items()}
    expected = {'G5_14': 15, 'G5_15': 30, 'G5_16': 10, 'G5_17': 1}
    complement_types = {'G5_14': '2K2', 'G5_15': 'P3', 'G5_16': 'K2', 'G5_17': 'empty'}
    counts, edge_counts = Counter(), Counter()
    retained, excluded_by_threshold = [], []
    degree_two_checks = 0
    for mask in range(1024):
        edges = tuple(e for j, e in enumerate(EDGES) if mask & (1 << j))
        if len(edges) < 8:
            excluded_by_threshold.append(mask)
            continue
        sid = lookup[canonical(edges)]
        counts[sid] += 1
        edge_counts[len(edges)] += 1
        degrees = [sum(v in e for e in edges) for v in range(5)]
        assert min(degrees) >= 2
        assert connected(edges)
        assert all(connected(edges, v) for v in range(5))
        two = [v for v, d in enumerate(degrees) if d == 2]
        assert len(two) <= 1
        assert bool(two) == (sid == 'G5_15')
        for v in two:
            neighbors = [b if a == v else a for a, b in edges if v in (a, b)]
            assert [degrees[n] for n in neighbors] == [4, 4]
            assert tuple(sorted(neighbors)) in edges
            degree_two_checks += 1
        retained.append({'mask': mask, 'edges': edges, 'shape_id': sid,
                         'degrees': degrees, 'first_betti_number': len(edges)-4,
                         'low_edges': sorted(full-set(edges)),
                         'low_complement_type': complement_types[sid],
                         'connected_after_each_vertex_deletion': True})
    assert dict(counts) == expected
    assert dict(edge_counts) == {8: 45, 9: 10, 10: 1}
    assert len(retained) == 56 and degree_two_checks == 30
    assert len(excluded_by_threshold) == 968
    # The empty graph is the all-unit solution case, not an arithmetic exclusion.
    assert 0 in excluded_by_threshold
    previous = HERE / 'support_agenda_verification_v20.json'
    old = json.loads(previous.read_text())
    assert old['passed'] and old['labelled_nonempty_supports_remaining'] == 66
    old_list = old['all_66_remaining_labelled_supports']
    old_edges = {tuple(tuple(e) for e in x['edges']) for x in old_list}
    new_edges = {tuple(x['edges']) for x in retained}
    removed = [x for x in old_list if tuple(tuple(e) for e in x['edges']) not in new_edges]
    assert new_edges < old_edges
    assert len(removed) == 10 and {x['shape_id'] for x in removed} == {'G5_13'}
    book = canonical([(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4)])
    assert all(canonical(x['edges']) == book for x in removed)
    shapes = []
    for sid, edges in representatives.items():
        aut = sum(set(relabel(edges, p)) == edges for p in PERMS)
        assert 120 // aut == expected[sid]
        shapes.append({'shape_id': sid, 'representative_edges': sorted(edges),
                       'canonical_edges': canonical(edges), 'automorphism_order': aut,
                       'labelled_count': expected[sid], 'low_complement_type': complement_types[sid]})
    proof = HERE.parent / 'paper/quintic_support_frontier_v22.tex'
    book_proof = HERE.parent / 'paper/book_complete_obstruction_v22.tex'
    result = {
        'version': 'v22', 'passed': True,
        'scope': 'Necessary supports for the prescribed quintic K5 arithmetic gluing data; candidate counts are not existence counts.',
        'verification_role': 'Independent exact graph enumeration applying prior arithmetic proofs and the v22 complete book obstruction.',
        'labelled_K5_graphs_checked': 1024,
        'labelled_nonempty_supports_remaining': 56,
        'unlabelled_shapes_remaining': 4,
        'remaining_counts_by_high_edge_number': dict(edge_counts),
        'shape_identifiers_preserved': True,
        'shapes': shapes,
        'all_56_remaining_labelled_supports': retained,
        'all_10_newly_excluded_labelled_supports': removed,
        'new_exclusion_theorem': 'bc22:book-obstruction',
        'structural_corollaries': {
            'minimum_high_edges': 8, 'minimum_first_betti_number': 4,
            'minimum_degree': 2, 'all_five_vertices_active': True,
            'connected_after_each_vertex_deletion': True,
            'maximum_degree_two_vertices': 1,
            'degree_two_vertex_checks': degree_two_checks,
            'degree_two_neighbors_have_degree_four': True,
            'three_distinct_unit_denominator_branches_force_all_unit': True,
            'two_cores_with_at_most_two_high_rays_force_all_unit': True,
        },
        'no_denominator_or_entry_cutoff': True,
        'empty_graph_status': 'All denominators one; not excluded.',
        'previous_certificate': {'file': previous.name, 'sha256': sha(previous)},
        'proof_sha256': sha(proof), 'book_proof_sha256': sha(book_proof),
        'source_sha256': sha(Path(__file__)),
    }
    output = HERE / 'support_agenda_verification_v22.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': True, 'graphs': 1024, 'removed_book_labels': 10,
                      'remaining_shapes': 4, 'remaining_labelled': 56,
                      'degree_two_checks': degree_two_checks}))

if __name__ == '__main__':
    main()
