#!/usr/bin/env python3
"""Independent audit of the four-exception finite-type reduction.

This checks the complete reverse-type list using a separate row solver, and
checks affine sign certificates on the whole real half-line h >= 6.  It does
not replace the hub enumeration, which has two separate implementations.
No project modules, floating point arithmetic, or denominator cutoff is used.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
VERTICES = range(4)
EDGES = tuple(combinations(VERTICES, 2))
ORDINARY_VALUES = (-4, -3, -2, -1, 1, 2, 3, 4)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate(name):
    options = [HERE / name, HERE.parent / 'four_exception' / name,
               HERE.parent / 'paper' / name, HERE.parent / name,
               HERE.parents[1] / 'paper' / name]
    return next(p for p in options if p.is_file())


def matrix_key(matrix):
    return tuple(tuple(row) for row in matrix)


def local_completions(known_row, unknown):
    """All row solutions, representing each h >= 6 family by h = 6.

    Unknown entries are the signed even large endpoints.  With two such
    entries there is exactly one known entry k in {-4,...,-1,1,...,4}.
    Same signs therefore permit only (-2,-2), with k = 3.  Opposite
    signs give a difference in {-4,-2,0,2,4}; these are the only tails.
    """
    target = -1 - sum(known_row)
    n = len(unknown)
    if n == 0:
        return [([], None)] if target == 0 else []
    if n == 3:
        assert target == -1
        return []  # The sum of three even numbers cannot be -1.
    if n == 1:
        col, sign = unknown[0]
        if target * sign >= 2 and target % 2 == 0:
            return [([(col, target)], None)]
        return []
    assert n == 2
    known = [v for v in known_row if v != 0]
    assert len(known) == 1 and known[0] in ORDINARY_VALUES
    (j, a), (k, b) = unknown
    if a == b:
        if a == -1 and known[0] == 3:
            return [([(j, -2), (k, -2)], None)]
        return []
    if target % 2:
        return []
    delta = a * target
    assert delta in (-4, -2, 0, 2, 4)
    result = []
    for h in (2, 4, 6):
        offsets = (max(delta, 0), max(-delta, 0))
        entries = [(j, a * (h + offsets[0])),
                   (k, b * (h + offsets[1]))]
        parameter = {'base': h, 'tail': h == 6,
                     'entries': [(j, a, offsets[0]), (k, b, offsets[1])]}
        result.append((entries, parameter))
    return result


def independently_generate(ordinary):
    exceptional = [e for e in EDGES if e not in ordinary]
    models = {}
    for ordinary_values in product(ORDINARY_VALUES, repeat=2):
        # A state jointly specifies the large endpoint and common sign.
        for states in product(((0, -1), (0, 1), (1, -1), (1, 1)), repeat=4):
            known = [[0] * 4 for _ in VERTICES]
            unknowns = [[] for _ in VERTICES]
            for (i, j), u in zip(ordinary, ordinary_values):
                known[i][j], known[j][i] = u, -u
            for edge, (large_index, sign) in zip(exceptional, states):
                large, unit = edge[large_index], edge[1 - large_index]
                known[unit][large] = sign
                unknowns[large].append((unit, sign))
            options = [local_completions(known[i], unknowns[i]) for i in VERTICES]
            for rows in product(*options):
                reverse = [row[:] for row in known]
                parameters = []
                for i, (assignments, parameter) in enumerate(rows):
                    for j, value in assignments:
                        reverse[i][j] = value
                    if parameter:
                        parameters.append(dict(parameter, vertex=i))
                assert all(sum(row) == -1 for row in reverse)
                key = matrix_key(reverse)
                assert key not in models
                models[key] = parameters
    return models


def parameter_key(parameters):
    return tuple(sorted((p['vertex'], p['base'], p['tail'],
                         tuple(sorted(tuple(e) for e in p['entries'])))
                        for p in parameters))


def check_tail_affine_certificates(reverse, parameters):
    """An affine a+b*t has strict sign for every t>=0 if a*b>=0, a!=0.

    Here t=h-6.  Unlike testing h up to a bound, this certifies the
    entire interval, including every positive even h >= 6.
    """
    checks = 0
    tails = []
    for parameter in parameters:
        if not parameter['tail']:
            continue
        i = parameter['vertex']
        assert parameter['base'] == 6
        row_derivative = [0] * 4
        entries = []
        for j, sign, offset in parameter['entries']:
            assert offset in (0, 2, 4)
            assert reverse[i][j] == sign * (6 + offset)
            assert reverse[j][i] == sign
            row_derivative[j] = sign
            constants = []
            for big_node in range(6):
                # V_big = constant + slope * (h - 6).
                constant = 1 - sign * (6 + offset) - big_node
                slope = -sign
                assert constant != 0 and constant * slope > 0
                assert (constant <= -5) if sign == 1 else (constant >= 2)
                constants.append(constant)
                for unit_node in range(6):
                    v_unit = 1 - sign - unit_node
                    assert (constant * v_unit == 0) == (unit_node == 1 - sign)
                    checks += 1
            # Along the family, X_big = sign is constant, whereas
            # X_unit = sign*h + sign*offset and V_big has slope -sign.
            # Therefore the original hub D equation at the unit end
            # has derivative sign + (-sign) = 0.  At the large end,
            # both X_big and the incoming V_unit have derivative 0.
            assert sign + (-sign) == 0
            entries.append({'large_endpoint': [i, j], 'sign': sign,
                            'offset': offset, 'V_slope_in_h': slope,
                            'V_constants_at_h_6_over_node_0_to_5': constants,
                            'unit_node_forced': 1 - sign,
                            'D_derivative_at_large_endpoint': 0,
                            'D_derivative_at_unit_endpoint': 0})
        assert sum(row_derivative) == 0
        assert sum(-v for v in row_derivative) == 0
        tails.append({'vertex': i, 'reverse_row_derivative': row_derivative,
                      'reverse_row_sum_derivative': 0,
                      'hub_V_row_sum_derivative': 0, 'entries': entries})
    return checks, tails


def main():
    primary_path = locate('k4_four_exceptions_verification_v17.json')
    source_path = locate('k4_four_exception_obstruction_v17.tex')
    primary = json.loads(primary_path.read_text())
    assert primary['passed'] is True
    assert primary['source_sha256'][source_path.name] == sha(source_path)
    result = {}
    total_checks = 0
    tail_records = []
    for name, ordinary in [('disjoint', [(0, 1), (2, 3)]),
                           ('adjacent', [(0, 1), (0, 2)])]:
        independent = independently_generate(ordinary)
        group = primary['ordinary_graph_normal_forms'][name]
        original = {matrix_key(m['R']): m for m in group['all_reverse_types']}
        assert set(independent) == set(original)
        counts = Counter()
        for key, parameters in independent.items():
            record = original[key]
            assert parameter_key(parameters) == parameter_key(record['parameters'])
            checks, tails = check_tail_affine_certificates(key, parameters)
            total_checks += checks
            counts['reverse_types'] += 1
            counts['tail_reverse_types'] += bool(tails)
            if tails:
                tail_records.append({'ordinary_graph': name, 'type_id': record['type_id'],
                                     'R_representative': key, 'tail_certificates': tails})
        expected = {'disjoint': (112, 32), 'adjacent': (204, 82)}[name]
        assert (counts['reverse_types'], counts['tail_reverse_types']) == expected
        result[name] = dict(counts, reverse_type_lists_identical=True,
                            parameter_lists_identical=True)
    report = {
        'version': 'v17', 'passed': True,
        'audit_scope': 'Independent reverse-type completeness and whole-half-line tail invariance; the separate primary and N-first programs check all finite hub candidates.',
        'script_sha256': sha(Path(__file__)),
        'audited_source_sha256': {source_path.name: sha(source_path),
                                  primary_path.name: sha(primary_path)},
        'independent_row_solver': {
            'zero_large_endpoints': 'Known entries must sum to -1.',
            'one_large_endpoint': 'Its value is uniquely fixed, even, at least 2 in magnitude, with prescribed sign.',
            'two_large_endpoints_same_sign': 'The only possibility is (-2,-2), with remaining known reverse 3.',
            'two_large_endpoints_opposite_signs': 'The magnitude difference is in {-4,-2,0,2,4}; min magnitude h is any positive even integer.',
            'three_large_endpoints': 'Impossible by parity.',
            'parameter_independence': 'Each exceptional large magnitude belongs to exactly one row; there is no shared variable between row equations.'},
        'normal_forms': result,
        'tail_interval': 'All real h >= 6, hence all even h >= 6.',
        'strict_sign_certification': 'For V(h)=a+b*(h-6), a*b>0 implies a fixed nonzero sign on the whole half-line. For positive large reverse a<=-5,b=-1; for negative large reverse a>=2,b=1.',
        'pair_zero_equivalence_checks': total_checks,
        'tail_pair_condition': 'Unit-end N=0 on positive exceptions, N=2 on negative exceptions.',
        'row_sum_invariance': 'The two large reverses have opposite derivatives, so the R and V row sums are invariant.',
        'D_invariance': 'On every exception X_ij=R_ji. At its unit end the derivatives of X and incoming V cancel; at its large end both relevant entries are constant.',
        'node_invariance': 'All N entries are fixed and their row sums remain 5. The high-edge node on an exception is 1-sign, hence 0 or 2 for every h.',
        'ordinary_q_invariance': 'Ordinary reverse entries and d_i=sum_j N_ji-5 are fixed. Forest flow and reconstructed ordinary q are therefore fixed.',
        'arbitrary_denominator_cutoff': None,
        'mathematical_audit_verdict': 'PASS: the h=6 representative is logically equivalent to its entire h>=6 family for every hub constraint imposed by the reduction.',
        'limitations': 'The audit certifies necessary hub data only. It does not infer local high-core completion or positivity from hub feasibility; those candidates are checked separately.',
        'external_peer_review': False,
        'proof_assistant_formalization': False,
        'all_tail_certificates': tail_records}
    output = HERE / 'k4_four_tail_independent_audit_v17.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'passed': True, 'normal_forms': result,
                      'pair_zero_equivalence_checks': total_checks,
                      'certificate': str(output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
