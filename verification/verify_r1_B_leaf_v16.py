#!/usr/bin/env python3
"""Complete proof-derived finite check of the exceptional B leaf at r=z=1.

The middle parameter sets are proved finite in r1_exceptional_leaf_v16.tex.
The v15 fixed-middle helper reconstructs every integer leaf, including free
signed entries and q=3 duplicated labels.  Only nodes and known center pair
equations are used for the final exclusion; q01 is never enumerated.
"""
from pathlib import Path
from itertools import combinations
import hashlib
import importlib.util
import json


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


HERE = Path(__file__).resolve().parent
HELPER_NAME = 'exact_fixed_middle_completion_v15.py'
HELPER = next(p for p in [
    HERE.parent / 'research' / HELPER_NAME,
    HERE.parents[1] / 'deliverables/general_type_surface_fibration_v15/research' / HELPER_NAME,
] if p.exists())
spec = importlib.util.spec_from_file_location('fixed_middle_v15', HELPER)
fixed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixed)


def matrix_key(m):
    return (m['q'], tuple(m['p'][i][j] for i in sorted(m['p']) for j in sorted(m['p'][i])))


def verify_leaf(m):
    labels = sorted(m['p'])
    q = {i: m['q'] if i == m['order'][0] else 1 for i in labels}
    assert all(sum(m['p'][i].values()) == -q[i] for i in labels)
    assert all(m['p'][i][j] * m['p'][j][i] == q[i] * q[j] - 1
               for i, j in combinations(labels, 2))
    assert all(m['D'][i] == -q[i] - sum(m['p'][j][i] for j in labels if j != i)
               for i in labels)
    assert fixed.weights_exist({'p': m['p'], 'qs': q})


def main():
    parameters = {(1, 2, 6)}
    trials = []

    def add(h, t, S, branch, alpha=None):
        item = {'branch': branch, 'h': h, 't': t, 'S': S, 'alpha': alpha}
        trials.append(item)
        if S < 2:
            item['rejected'] = 'S<2'
            return
        if (3*S - 4) % (h + 4):
            item['rejected'] = 'k is not integral'
            return
        k = (3*S - 4) // (h + 4)
        if k < 1:
            item['rejected'] = 'k<1'
            return
        s, T = h + 3, 2*(h + 3)*k + 4
        item.update(s=s, k=k, T=T)
        if s*S % 2:
            item['rejected'] = 'a=sS+1 is even'
            return
        fixed.make_middle(1, s, 1, S, T)
        parameters.add((s, S, T))
        item['accepted'] = True

    # Case I: th <= 4, and S-v belongs to {-1,...,4}.
    for h in range(1, 5):
        for t in range(1, 4//h + 1):
            for S in range(t*(h+1)-1, t*(h+1)+5):
                add(h, t, S, 'leaf3 ray4=C')
    # Case II: alpha = S-v; the bounds follow from the coefficient identity.
    for h in range(1, 28):
        for t in range(1, 27//h + 1):
            for alpha in range(5):
                add(h, t, t*(h+1)+alpha, 'leaf3 ray4=B; alpha>=0', alpha)
    for h in range(1, 29):
        for t in range(2, 28//h + 2):
            add(h, t, t*(h+1)-1, 'leaf3 ray4=B; alpha=-1,t>=2', -1)
    for h in (4, 12):
        add(h, 1, h, 'leaf3 ray4=B; alpha=-1,t=1', -1)
    assert len(parameters) == 33

    # Exact finite maxima used in the Case II bound.
    C4_records = []
    for u in range(1, 5):
        choices = []
        for h in fixed.divisors(u):
            t = u//h
            for c in range(u-2, 3):
                m = t*h*(h+1)
                choices.append({'h': h, 't': t, 'c': c,
                                'C4': m+t+h+c+2})
        C4_records.append({'u4': u, 'choices': choices,
                           'maximum': max(v['C4'] for v in choices)})
    assert [v['maximum'] for v in C4_records] == [8, 13, 20, 29]

    # Check the elementary inequality reduction of Case I for all survivors.
    case_I_boundary = []
    for h in range(1, 5):
        A = 4*h*h+15*h+14
        B = 3*h*h+20*h+10
        assert A <= B < 2*A
        if (h+8) % 3 == 0:
            S = (h+8)//3
            ts = list(range(1, (S+1)//(h+1)+1))
            assert all(t*h <= 4 for t in ts)
            case_I_boundary.append({'h': h, 'k': 1, 'S': S, 't': ts})
    assert case_I_boundary == [{'h': 1, 'k': 1, 'S': 3, 't': [1, 2]},
                               {'h': 4, 'k': 1, 'S': 4, 't': [1]}]

    middle_records = []
    surviving = []
    center_checks = []
    for s, S, T in sorted(parameters):
        model = fixed.make_middle(1, s, 1, S, T)
        order = (0, 1, 4, 3)
        core = {
            'p': {a: {b: model['p'][i][j] for j, b in enumerate(order)}
                  for i, a in enumerate(order)},
            'D': {a: model['D'][i] for i, a in enumerate(order)},
        }
        leaves3 = fixed.non_B(3, core)
        unique = {}
        for leaf3 in leaves3:
            verify_leaf(leaf3)
            for leaf4 in fixed.B_models(4, core, leaf3):
                verify_leaf(leaf4)
                assert leaf4['order'][1] == 2
                assert fixed.compatible_edge(2, 3, core, leaf3)
                assert fixed.compatible_edge(2, 4, core, leaf4)
                assert fixed.compatible_edge(3, 4, leaf3, leaf4)
                unique[(matrix_key(leaf3), matrix_key(leaf4))] = (leaf3, leaf4)
        record = {'parameters': {'r': 1, 's': s, 'z': 1, 'S': S, 'T': T},
                  'middle': model, 'leaf3_count': len(leaves3),
                  'low_triangle_count': len(unique), 'low_triangles': []}
        for leaf3, leaf4 in unique.values():
            record['low_triangles'].append({'leaf3': leaf3, 'leaf4': leaf4})
            a, Q, h = model['a'], leaf3['q'], leaf3['h']
            assert h == s-3 and leaf3['order'][3] == 2
            pair_trials = [
                {'n': n, 'm': m, 'p23': a*(1-n)+s, 'p32': Q*(1-m)-h,
                 'product': (a*(1-n)+s)*(Q*(1-m)-h)}
                for n in range(6) for m in range(6)]
            solutions = [v for v in pair_trials if v['product'] == a*Q-1]
            cc = {'s': s, 'S': S, 'T': T, 'a': a, 'Q': Q, 'h': h,
                  'q14': leaf4['q'], 'node_pairs': pair_trials,
                  'node_pair_solutions': solutions}
            if solutions:
                assert (a, Q, h) == (33, 9, 1)
                assert [(v['n'], v['m']) for v in solutions] == [(0, 0)]
                incoming = leaf4['p'][0][2]
                assert incoming in (16, 18)
                sums = [32+incoming, -1+incoming]
                assert all(not -4 <= v <= 1 for v in sums)
                cc.update(final_p4_02=incoming, forced_p0_42=[32, -1],
                          low04_puncture2_sums=sums,
                          exclusion='Both signed-divisor choices violate low-edge 04 node interval')
            else:
                cc['exclusion'] = 'No center0 pair solution for known rays2,3'
            center_checks.append(cc)
        if unique:
            surviving.append((s, S, T, len(unique)))
        middle_records.append(record)
    assert surviving == [(4, 3, 12, 3), (4, 8, 36, 2),
                         (7, 4, 18, 1), (15, 12, 64, 1)]
    assert len(center_checks) == 7

    source = HERE / 'r1_exceptional_leaf_v16.tex'
    if not source.exists():
        source = HERE.parent / 'paper' / source.name
    result = {
        'version': 'v16', 'passed': True,
        'script_sha256': sha(Path(__file__).resolve()),
        'source_sha256': {source.name: sha(source)},
        'research_helper': {'file': 'research/' + HELPER_NAME, 'sha256': sha(HELPER)},
        'scope': 'Complete exclusion of the ray2=B leaf4 branch at r=z=1 after the crossed positive-branch reduction.',
        'denominator_cutoff': None, 'unknown_q01_enumerated': False,
        'proof_derived_parameter_trials': trials,
        'accepted_witnesses': sum(bool(v.get('accepted')) for v in trials),
        'complete_middle_models': 33,
        'C4_maxima': C4_records,
        'case_I_boundary': case_I_boundary,
        'middle_models': middle_records,
        'surviving_low_triangle_models': surviving,
        'surviving_low_triangles': 7,
        'center0_exclusions': center_checks,
        'center0_survivors': 0,
        'center_D_or_unknown_row_used': False,
        'completeness_basis': [
            'Leaf3 ray2=C forces the single middle (s,S,T)=(1,2,6).',
            'Leaf3 ray2=D forces h=s-3 and c=0.',
            'Leaf3 ray4=C forces th<=4 by the two-case inequality in the TeX proof.',
            'Leaf3 ray4=B gives the exact balance th+alpha(h+1)+k+2=C4+beta<=30.',
            'The only unbounded-looking alpha=-1,t=1 case reduces to h+4 dividing16, hence h=4,12.',
            'The fixed-middle helper retains every signed c,d choice and all B/C label duplications; matrix pairs are deduplicated after reconstruction.',
        ],
        'external_peer_review': False,
    }
    output = HERE / 'r1_B_leaf_verification_v16.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'passed': True, 'raw_parameter_trials': len(trials),
                      'accepted_witnesses': result['accepted_witnesses'],
                      'middle_models': 33, 'low_triangles': 7,
                      'center0_survivors': 0, 'output': str(output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
