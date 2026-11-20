#!/usr/bin/env python3
"""Independent review of the global two-leaf obstruction.

No research helper or primary checker is imported. Candidate center rows are
reconstructed from two entry residues and their row sum. The three pair
equations are then checked by intersections of pairwise compatibility sets.
"""
from pathlib import Path
from itertools import combinations, permutations
from fractions import Fraction
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent


def locate(name, folder):
    """Resolve both the work tree and bundle verification/audits layout."""
    choices = [
        HERE / name,
        HERE.parent / name,
        HERE.parents[1] / folder / name,
        HERE.parent / 'root' / name,
        HERE.parent / 'z1' / name,
        HERE.parent / 'small_r' / name,
    ]
    for path in choices:
        if path.is_file():
            return path
    raise FileNotFoundError(name)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return json.loads(p.read_text())


def normalize(raw, core, params):
    p = {int(i): {int(j): v for j, v in row.items()} for i, row in raw['p'].items()}
    labels = sorted(set(range(5)) - {core})
    if core == 2:
        q = {0: params['s']*params['S']+1, 1: params['T']+1, 3: 1, 4: 1}
    else:
        q = {j: raw['q'] if j == (0 if core == 3 else 1) else 1 for j in labels}
    assert sorted(p) == labels
    assert all(sorted(p[j]) == labels and p[j][j] == 0 for j in labels)
    assert all(type(v) is int for row in p.values() for v in row.values())
    assert all(type(v) is int and v > 0 and v % 2 for v in q.values())
    for i in labels:
        assert sum(p[i].values()) == -q[i]
    for i, j in combinations(labels, 2):
        assert p[i][j]*p[j][i] == q[i]*q[j]-1
    D = {i: -q[i]-sum(p[j][i] for j in labels if j != i) for i in labels}
    assert D == {int(i): v for i, v in raw['D'].items()}
    for length in (2, 3, 4):
        for cycle in permutations(labels, length):
            if not all(p[cycle[j]][cycle[(j+1) % length]] > 0 for j in range(length)):
                continue
            gain = Fraction(1)
            for j in range(length):
                gain *= Fraction(p[cycle[j]][cycle[(j+1) % length]], q[cycle[j]])
            assert gain < 1
    return {'p': p, 'q': q, 'D': D}


def patch_key(params, cores):
    return (tuple(params[k] for k in ('r', 's', 'z', 'S', 'T')),
            tuple((j, tuple(cores[j]['q'][a] for a in sorted(cores[j]['q'])),
                   tuple(cores[j]['p'][a][b] for a in sorted(cores[j]['p'])
                         for b in sorted(cores[j]['p'][a]))) for j in (3, 4)))


def center_candidates(center, cores):
    labels = sorted(set(range(5)) - {center})
    qs = {j: cores[j]['q'][center] for j in (2, 3, 4)}
    choices = {}
    for j in (2, 3, 4):
        a, b, c = sorted(set(labels) - {j})
        q = qs[j]
        other = cores[j]['p'][center]
        first_values = [q*(1-n)-other[a] for n in range(6)]
        second_values = [q*(1-n)-other[b] for n in range(6)]
        rows = []
        for x in first_values:
            for y in second_values:
                z = -q-x-y
                if (z+other[c]) % q:
                    continue
                nc = 1-(z+other[c])//q
                if not 0 <= nc <= 5:
                    continue
                row = {j: 0, a: x, b: y, c: z}
                nodes = [1-(row[k]+other[k])//q for k in (a, b, c)]
                assert sum(nodes) == 5 and min(nodes) >= 0 and max(nodes) <= 5
                rows.append({'entries': row, 'nodes': nodes})
        assert len(rows) == 21
        assert len({tuple(r['entries'][k] for k in labels) for r in rows}) == 21
        choices[j] = rows

    compat = {}
    for j, k in ((2, 3), (2, 4), (3, 4)):
        pairs = set()
        for a, row_j in enumerate(choices[j]):
            for b, row_k in enumerate(choices[k]):
                if row_j['entries'][k]*row_k['entries'][j] == qs[j]*qs[k]-1:
                    pairs.add((a, b))
        compat[(j, k)] = pairs
    triples = []
    for i2, i3 in sorted(compat[(2, 3)]):
        candidates24 = {i4 for j2, i4 in compat[(2, 4)] if j2 == i2}
        candidates34 = {i4 for j3, i4 in compat[(3, 4)] if j3 == i3}
        for i4 in sorted(candidates24 & candidates34):
            triples.append([choices[2][i2]['nodes'], choices[3][i3]['nodes'],
                            choices[4][i4]['nodes']])
    return {'center': center, 'row_choice_counts': [len(choices[j]) for j in (2, 3, 4)],
            'pairwise_compatible_counts': {str(j)+str(k): len(v) for (j, k), v in compat.items()},
            'compatible_row_triple_count': len(triples), 'compatible_node_triples': triples}


def main():
    primary_data = locate('two_leaf_unit_finiteness_certificate_v16.json', 'verification')
    primary_code = locate('verify_two_leaf_centers_v16.py', 'verification')
    primary_result = locate('two_leaf_center_obstruction_v16.json', 'verification')
    source = locate('two_leaf_global_obstruction_v16.tex', 'paper')
    B_data = locate('r1_B_leaf_verification_v16.json', 'verification')
    data, reference, b_data = map(load, (primary_data, primary_result, B_data))
    assert data['passed'] and reference['passed'] and b_data['passed']
    assert reference['script_sha256'] == sha(primary_code)
    assert reference['source_sha256'][source.name] == sha(source)
    assert reference['dependency_sha256'][primary_data.name] == sha(primary_data)
    expected = {
        (1, 4, 1, 3, 12): (21, 0), (1, 7, 1, 4, 18): (3, 0),
        (1, 4, 1, 8, 36): (4, 0), (1, 15, 1, 12, 64): (3, 0),
        (2, 4, 1, 3, 6): (4, 0), (2, 4, 1, 12, 30): (5, 0),
        (2, 5, 1, 14, 36): (1, 0), (4, 4, 1, 18, 30): (1, 1),
        (4, 4, 1, 35, 60): (8, 0), (4, 4, 1, 52, 90): (2, 0),
    }
    ref_records = {(tuple(r['parameters'][k] for k in ('r', 's', 'z', 'S', 'T')),
                    r['low_patch_index']): r for r in reference['records']}
    fingerprints = set()
    records = []
    q3_records = []
    for group in data['survivors']:
        params = group['parameters']
        par = tuple(params[k] for k in ('r', 's', 'z', 'S', 'T'))
        count, obstruction = expected[par]
        assert len(group['low_patches']) == count
        for idx, patch in enumerate(group['low_patches']):
            cores = {2: normalize(patch['middle'], 2, params),
                     3: normalize(patch['leaf3'], 3, params),
                     4: normalize(patch['leaf4'], 4, params)}
            key = patch_key(params, cores)
            assert key not in fingerprints
            fingerprints.add(key)
            low_edges = []
            for i, j in ((2, 3), (2, 4), (3, 4)):
                assert cores[i]['q'][j] == cores[j]['q'][i] == 1
                ks = sorted(set(range(5)) - {i, j})
                nodes = [1-cores[i]['p'][j][k]-cores[j]['p'][i][k] for k in ks]
                assert sum(nodes) == 5 and min(nodes) >= 0
                assert cores[i]['D'][j]+cores[j]['D'][i] == 0
                low_edges.append({'edge': [i, j], 'nodes': nodes})
            checks = [center_candidates(i, cores) for i in (0, 1)]
            ref = ref_records[(par, idx)]
            assert [c['compatible_row_triple_count'] for c in checks] == [c['compatible_count'] for c in ref['centers']]
            assert checks[obstruction]['compatible_row_triple_count'] == 0
            record = {'parameters': params, 'low_patch_index': idx,
                      'leaf_denominators': [patch['leaf3']['q'], patch['leaf4']['q']],
                      'low_edges': low_edges, 'centers': checks,
                      'obstructing_center': obstruction,
                      'primary_counts_match': True}
            records.append(record)
            if 3 in record['leaf_denominators']:
                q3_records.append({'parameters': params, 'low_patch_index': idx,
                                   'leaf_denominators': record['leaf_denominators']})
    assert len(fingerprints) == len(records) == 52

    b_fingerprints = set()
    b_subset_records = []
    for group in b_data['middle_models']:
        params = group['parameters']
        for patch in group['low_triangles']:
            cores = {3: normalize(patch['leaf3'], 3, params),
                     4: normalize(patch['leaf4'], 4, params)}
            key = patch_key(params, cores)
            assert key not in b_fingerprints and key in fingerprints
            b_fingerprints.add(key)
            b_subset_records.append({'parameters': params,
                                     'leaf_denominators': [patch['leaf3']['q'], patch['leaf4']['q']],
                                     'belongs_to_52': True})
    assert len(b_fingerprints) == 7
    center_counts = {i: sum(r['obstructing_center'] == i for r in records) for i in (0, 1)}
    assert center_counts == {0: 51, 1: 1}

    report = {
        'version': 'v16', 'status': 'PASS', 'passed': True,
        'audit_kind': 'Independent original-equation recheck and completeness-composition review of the global two-leaf obstruction',
        'captured_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'external_peer_review': False, 'proof_assistant_formalization': False,
        'audit_script_sha256': sha(Path(__file__).resolve()),
        'source_snapshot': {p.name: sha(p) for p in (source, primary_code, primary_result, primary_data, B_data)},
        'method': 'No primary checker or leaf generator imported. Rows are independently reconstructed from two entry residues and the row sum; all three pair equations are checked by intersections of pairwise compatibility sets.',
        'middle_models': 10, 'distinct_low_patches': 52,
        'all_original_core_and_low_edge_conditions_rechecked': True,
        'all_104_center_counts_match_primary': True,
        'rows_per_known_ray': 21, 'center_obstruction_counts': center_counts,
        'unknown_q01_or_missing_row_used': False,
        'center_D_or_weights_used_for_obstruction': False,
        'q3_low_patches': q3_records,
        'B_patch_count': 7, 'all_B_patches_are_a_subset_of_52': True,
        'B_subset_records': b_subset_records,
        'counts_are_not_added': True,
        'completeness_composition_review': [
            {'step': 'Crossed positive-branch reduction', 'status': 'PASS',
             'reason': 'The established v15 theorem excludes the uncrossed and all negative branches before the v16 positive-branch argument is applied.'},
            {'step': 'z=1 and r<=4', 'status': 'PASS',
             'reason': 'The new common-low pair/node bound forces both conditions. Its source was independently proved and audited in this work.'},
            {'step': 'All normal-form labels of leaf4 ray2', 'status': 'PASS',
             'reason': 'The full one-high normal form gives B,C,D. Its high ray is1, hence ray2 is always among these three low labels.'},
            {'step': 'B representation implies r=1', 'status': 'PASS',
             'reason': 'For ray2=B, p4_20=0. The low-edge24 node at puncture0 has sum r, requiring r<=1. Positive r then equals1.'},
            {'step': 'B branch completeness', 'status': 'PASS',
             'reason': 'The separate proof derives a complete 33-middle set and seven low patches, all excluded. Its finite parameter bound does not assume any denominator cutoff.'},
            {'step': 'C/D branch completeness', 'status': 'PASS',
             'reason': 'The non-B proof derives 31 middles from bounded-E, free-E and small-S cases. The free-E bound was independently rederived by this reviewer; the other two branches are covered by the separate review.'},
            {'step': 'q=3 multiple representations', 'status': 'PASS',
             'reason': 'The case split requires coverage, not disjoint representations. Every full integer one-high matrix has a B/C/D representation, and identical labelled matrix pairs are counted only once. The seven B patches are checked directly as a subset of the52.'},
            {'step': 'Center reconstruction is necessary and complete at the known-row level', 'status': 'PASS',
             'reason': 'Each shared edge has three nonnegative node counts summing to5. The original node equation uniquely determines the known row, and its row sum follows automatically. Any global completion supplies one of the 21 choices for each of the three known rows.'},
            {'step': 'Global contradiction', 'status': 'PASS',
             'reason': 'Every one of the52 low patches fails the three known-ray pair equations at a center. No choice of q01, the missing fourth row, or center D/weights can repair that necessary-condition failure.'},
        ],
        'records': records,
        'remaining_findings': [],
    }
    output = HERE / 'two_leaf_global_independent_audit_v16.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'low_patches': 52,
                      'matched_center_counts': 104, 'B_subset': 7,
                      'q3_patch_count': len(q3_records),
                      'obstructing_centers': center_counts,
                      'output': str(output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
