#!/usr/bin/env python3
"""Independent finite leaf reconstruction for the v15 two-leaf obstruction.

Standard library only. This is an internal computational cross-check, not an
external peer review. It shares the proved seven middle-core models with the
main verifier, but reconstructs every leaf matrix by a different method:

  21 node allocations -> fixed ray-2 row -> fixed ray-2 column ->
  signed divisors in the high row -> original row/pair equations and positivity.

No arbitrary denominator cutoff is used. The one-high normal form and the
node interval bound u=t*h or v=t*(h+1), hence bound the leaf denominator by
max(u_max*(u_max+1)+1, v_max*(v_max-1)+1). For these seven middle cores the
largest proved bound is 91. Equality with the main verifier's entire matrix
sets checks that the canonical C/D reconstruction omitted no q=3 freedom.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import importlib.util
import json


SCRIPT = Path(__file__).resolve()
DIRECTORY = SCRIPT.parent


def locate(candidates, description):
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f'{description} is required: {candidates}')


DEPENDENCY = locate(
    [DIRECTORY / 'verify_two_leaves_v15.py',
     DIRECTORY.parent / 'two_leaves' / 'verify_two_leaves_v15.py'],
    'Main two-leaf verifier')
spec = importlib.util.spec_from_file_location('v15_main_two_leaf_verifier', DEPENDENCY)
assert spec is not None and spec.loader is not None
main_verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_verifier)


def signed_divisors(n):
    assert n > 0
    return [sign * d for d in range(1, n + 1) if n % d == 0 for sign in (-1, 1)]


def positive(labels, matrix, denominators):
    """Independent exact directed-cycle criterion; no canonical weights used."""
    for length in range(2, 5):
        for cycle in permutations(labels, length):
            if cycle[0] != min(cycle):
                continue
            if not all(matrix[cycle[i]][cycle[(i + 1) % length]] > 0
                       for i in range(length)):
                continue
            gain = Fraction(1)
            for i in range(length):
                gain *= Fraction(matrix[cycle[i]][cycle[(i + 1) % length]],
                                 denominators[cycle[i]])
            if gain >= 1:
                return False
    return True


def matrix_key(model):
    labels = sorted(model['p'])
    return (model['q'], tuple(model['p'][i][j] for i in labels for j in labels))


NODE_ALLOCATIONS = [allocation for allocation in product(range(6), repeat=3)
                    if sum(allocation) == 5]
assert len(NODE_ALLOCATIONS) == 21


def independent_leaf_matrices(leaf, core):
    high = {3: 0, 4: 1}[leaf]
    other, other_leaf = 1 - high, 7 - leaf
    labels = sorted((high, other, other_leaf, 2))
    punctures = (high, other, other_leaf)
    reverse, opposite_coefficient = core['p'][leaf][high], core['D'][leaf]

    # C: -u is the reverse entry, u=t*h <= reverse+4.
    # D:  v is the reverse entry, v=t*(h+1) <= 1-reverse.
    # Thus q=uh+u+1 <= u(u+1)+1, or q=vh+1 <= v(v-1)+1.
    u_max, v_max = max(0, reverse + 4), max(0, 1 - reverse)
    q_bound = max(u_max * (u_max + 1) + 1, v_max * (v_max - 1) + 1)
    output = {}

    for nodes in NODE_ALLOCATIONS:
        fixed_row = {j: 1 - core['p'][leaf][j] - n
                     for j, n in zip(punctures, nodes)}
        a, b, c = (fixed_row[j] for j in punctures)
        assert a + b + c == -1
        # The B row (-1,0,0) is excluded directly by the node allocations.
        assert b or c

        for q in range(3, q_bound + 1, 2):
            if not a or (q - 1) % a:
                continue
            high_to_2 = (q - 1) // a
            remaining_column = opposite_coefficient - 1 - high_to_2
            if b and c:
                if remaining_column:
                    continue
                other_to_2 = other_leaf_to_2 = 0
            elif b:
                other_to_2, other_leaf_to_2 = 0, remaining_column
            else:
                other_to_2, other_leaf_to_2 = remaining_column, 0

            for high_to_other in signed_divisors(q - 1):
                high_to_other_leaf = -q - high_to_2 - high_to_other
                if not high_to_other_leaf or (q - 1) % high_to_other_leaf:
                    continue
                other_to_high = (q - 1) // high_to_other
                other_leaf_to_high = (q - 1) // high_to_other_leaf
                other_to_other_leaf = -1 - other_to_2 - other_to_high
                other_leaf_to_other = -1 - other_leaf_to_2 - other_leaf_to_high
                if other_to_other_leaf * other_leaf_to_other:
                    continue

                matrix = {i: {j: 0 for j in labels} for i in labels}
                matrix[2].update(fixed_row)
                matrix[high].update({2: high_to_2, other: high_to_other,
                                     other_leaf: high_to_other_leaf})
                matrix[other].update({2: other_to_2, high: other_to_high,
                                      other_leaf: other_to_other_leaf})
                matrix[other_leaf].update({2: other_leaf_to_2,
                                           high: other_leaf_to_high,
                                           other: other_leaf_to_other})
                denominators = {i: q if i == high else 1 for i in labels}
                assert all(sum(matrix[i].values()) == -denominators[i] for i in labels)
                assert all(matrix[i][j] * matrix[j][i]
                           == denominators[i] * denominators[j] - 1
                           for i, j in combinations(labels, 2))
                coefficients = {i: -denominators[i] - sum(matrix[j][i] for j in labels)
                                for i in labels}
                assert coefficients[2] + opposite_coefficient == 0
                if not positive(labels, matrix, denominators):
                    continue
                model = {'q': q, 'p': matrix, 'D': coefficients, 'qs': denominators}
                output[matrix_key(model)] = model
    return q_bound, output


def main():
    records = []
    for core in main_verifier.negative_small_models()[0]:
        for leaf in (3, 4):
            q_bound, independent = independent_leaf_matrices(leaf, core)
            canonical = {matrix_key(model)
                         for model in main_verifier.leaf_candidates(leaf, core)}
            assert set(independent) == canonical, (core['parameters'], leaf)
            serialized_set = json.dumps(sorted(independent), separators=(',', ':'))
            records.append({
                'middle': core['parameters'],
                'leaf': leaf,
                'proved_leaf_q_bound': q_bound,
                'independent_candidates': len(independent),
                'q3_candidates': sum(key[0] == 3 for key in independent),
                'matches_main_verifier_exactly': True,
                'matrix_set_sha256': sha256(serialized_set.encode('utf-8')).hexdigest(),
            })

    source_names = ['one_high_and_crossed_pairing_v15.tex',
                    'two_leaves_negative_branch_v15.tex']
    sources = {name: locate([DIRECTORY / name,
                            DIRECTORY.parent / 'papers/sections/paper' / name,
                            DEPENDENCY.parent / name], name)
               for name in source_names}
    report = {
        'status': 'PASS',
        'passed': True,
        'version': 'v15',
        'script_sha256': sha256(SCRIPT.read_bytes()).hexdigest(),
        'source_sha256': {name: sha256(path.read_bytes()).hexdigest()
                          for name, path in sources.items()},
        'dependency_sha256': {DEPENDENCY.name: sha256(DEPENDENCY.read_bytes()).hexdigest()},
        'review_status': 'Internal computational cross-check; not an external peer review.',
        'scope': 'The seven middle-core list is shared with the main verifier. All 14 leaf sets are independently reconstructed from 21 node allocations, fixed rows and columns, and signed divisors, then compared as complete matrix sets.',
        'finite_bound_justification': 'The one-high normal form and node intervals give u<=R+4 or v<=1-R. Then q<=u(u+1)+1 or q<=v(v-1)+1. These are proved per-middle bounds, not arbitrary denominator cutoffs.',
        'node_allocations_per_middle_leaf': len(NODE_ALLOCATIONS),
        'leaf_list_count': len(records),
        'total_leaf_candidates': sum(record['independent_candidates'] for record in records),
        'largest_proved_leaf_q_bound': max(record['proved_leaf_q_bound'] for record in records),
        'records': records,
    }
    destination = DIRECTORY / 'two_leaves_independent_certificate_v15.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'leaf_lists': len(records),
                      'candidate_count': report['total_leaf_candidates'],
                      'largest_proved_leaf_q_bound': report['largest_proved_leaf_q_bound'],
                      'certificate': destination.name}, ensure_ascii=False))


if __name__ == '__main__':
    main()
