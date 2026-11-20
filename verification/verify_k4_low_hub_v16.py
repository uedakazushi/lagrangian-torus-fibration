#!/usr/bin/env python3
"""Exact checks for K4 low-hub reduction; no bound on unknown denominators."""
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

VARIABLES = ('A', 'C', 'D', 'u', 'w')
ZERO = (0,) * len(VARIABLES)


class Poly:
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {k: v for k, v in value.items() if v}
        else:
            self.terms = {ZERO: value} if value else {}

    def __add__(self, other):
        result = defaultdict(int, self.terms)
        for key, value in Poly(other).terms.items():
            result[key] += value
        return Poly(dict(result))

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) + (-self)

    def __mul__(self, other):
        result = defaultdict(int)
        for ka, va in self.terms.items():
            for kb, vb in Poly(other).terms.items():
                result[tuple(a + b for a, b in zip(ka, kb))] += va * vb
        return Poly(dict(result))

    __rmul__ = __mul__


def variable(index):
    powers = [0] * len(VARIABLES)
    powers[index] = 1
    return Poly({tuple(powers): 1})


IDENTITIES = []


def identity(name, left, right=0):
    assert not (Poly(left) - right).terms, name
    IDENTITIES.append(name)


def all_exception_symbolics():
    A, C, D, u, w = [variable(i) for i in range(5)]
    R = [[0, 1, -1, -1], [A, 0, 1, -A-2],
         [-D-2, D, 0, 1], [-C, -1, C, 0]]
    V = [[0, 0, u, -1-u], [-A-2-u, 0, 0, A+1+u],
         [D+3-w, w-D-4, 0, 0], [C-1+w+u, 2-w, -C-2-u, 0]]
    N = [[0, 0, 2-u, 3+u], [3+u, 0, 0, 2-u],
         [w, 5-w, 0, 0], [2-w-u, w, 3+u, 0]]
    q = {(0, 1): A+1, (0, 2): D+3, (0, 3): C+1,
         (1, 2): D+1, (1, 3): A+3, (2, 3): C+1}
    for i in range(4):
        identity('R row ' + str(i), sum(R[i]), -1)
        identity('V row ' + str(i), sum(V[i]), -1)
        identity('N row ' + str(i), sum(N[i]), 5)
        identity('N column ' + str(i), sum(N[j][i] for j in range(4)), 5)
        for j in range(4):
            if i != j:
                identity('node relation %d,%d' % (i, j),
                         Poly(R[i][j]) + V[i][j] + N[i][j], 1)
    for i, j in combinations(range(4), 2):
        # For exceptional edges X_ij=R_ji.
        identity('high-low pair %d,%d' % (i, j), Poly(R[i][j]) * R[j][i], q[i, j]-1)
    identity('hub pair 01', Poly(V[0][1]) * V[1][0])
    identity('hub pair 12', Poly(V[1][2]) * V[2][1])
    identity('hub pair 23', Poly(V[2][3]) * V[3][2])
    identity('hub pair 02', Poly(V[0][2]) * V[2][0], u*(D+3-w))
    identity('hub pair 03', Poly(V[0][3]) * V[3][0], (-1-u)*(C-1+w+u))
    identity('hub pair 13', Poly(V[1][3]) * V[3][1], (A+1+u)*(2-w))


def all_exception_orientations():
    edges = list(combinations(range(4), 2))
    records = []
    for directions in product((0, 1), repeat=6):
        small = {e: e[t] for e, t in zip(edges, directions)}
        degree = [sum(small[e] == i for e in edges) for i in range(4)]
        if any(v % 2 != 1 for v in degree):
            continue
        assert sorted(degree) == [1, 1, 1, 3]
        source = degree.index(3)
        others = [i for i in range(4) if i != source]
        assert all(sum(small[e] == i for e in edges if source not in e) == 1
                   for i in others)
        for sign_tuple in product((-1, 1), repeat=6):
            signs = dict(zip(edges, sign_tuple))
            if sum(signs[e] for e in edges if source in e) != -1:
                continue
            if any(sum(signs[e] for e in edges if i in e and small[e] != i) != 0
                   for i in others):
                continue
            positive_neighbor = next(i for i in others
                                     if signs[tuple(sorted((source, i)))] == 1)
            cycle_next = next(j for j in others if j != positive_neighbor
                              and small[tuple(sorted((positive_neighbor, j)))] == positive_neighbor)
            cycle_last = next(i for i in others if i not in (positive_neighbor, cycle_next))
            relabel = [source, positive_neighbor, cycle_next, cycle_last]
            expected = {(0, 1): (0, 1), (0, 2): (0, -1), (0, 3): (0, -1),
                        (1, 2): (1, 1), (1, 3): (3, -1), (2, 3): (2, 1)}
            for (i, j), (unit, sign) in expected.items():
                e = tuple(sorted((relabel[i], relabel[j])))
                assert small[e] == relabel[unit] and signs[e] == sign
            records.append({'source': source, 'canonical_label_order': relabel,
                            'small_endpoints': [small[e] for e in edges], 'signs': list(sign_tuple)})
    assert len(records) == 24
    return records


def complete_uw_cases():
    records = []
    for u in range(-3, 3):
        for w in range(6):
            if u+w > 2:
                continue
            forced = {}
            if u != 0:
                forced['D'] = w-3
            if w != 2:
                forced['A'] = -1-u
            if u != -1:
                forced['C'] = 1-w-u
            bad = {k: v for k, v in forced.items() if v < 2 or v % 2}
            assert bad, (u, w, forced)
            records.append({'u': u, 'w': w, 'forced_even_parameters': forced,
                            'nonpositive_or_odd_contradictions': bad})
    return records


def node_cut_extrema():
    triples = [(a, b, 5-a-b) for a in range(6) for b in range(6-a)]
    assert len(triples) == 21
    rows = []
    for i in range(4):
        slots = [j for j in range(4) if j != i]
        options = []
        for t in triples:
            row = [0]*4
            for j, value in zip(slots, t):
                row[j] = value
            options.append(tuple(row))
        rows.append(options)
    ranges = {size: [100, -100] for size in (1, 2, 3)}
    count = 0
    cuts = [(tuple(i for i in range(4) if mask >> i & 1)) for mask in range(1, 15)]
    for N in product(*rows):
        count += 1
        d = [sum(N[j][i] for j in range(4))-5 for i in range(4)]
        assert sum(d) == 0
        for S in cuts:
            value = sum(d[i] for i in S)
            ranges[len(S)][0] = min(ranges[len(S)][0], value)
            ranges[len(S)][1] = max(ranges[len(S)][1], value)
    assert count == 21**4
    assert ranges == {1: [-5, 10], 2: [-10, 10], 3: [-10, 5]}
    return {'all_node_matrices': count, 'cut_ranges_by_size': ranges}


def bridge_bounds():
    result = {}
    for bound in (5, 10):
        rows = []
        for u in range(1, 5):
            qs = sorted({1+u*v for v in range(1, bound-u+1) if (u*v) % 2 == 0})
            rows.append({'absolute_reverse': u, 'possible_denominators': qs})
        largest = max(q for row in rows for q in row['possible_denominators'])
        assert largest == (7 if bound == 5 else 25)
        result[str(bound)] = {'maximum_W': bound, 'rows': rows, 'maximum_q': largest}
    # Both exceptional denominators are odd; M=P+4 and the proof gives M<=8.
    pairs = [(P+1, P+5) for P in range(2, 5, 2)]
    assert pairs == [(3, 7), (5, 9)]
    return result, pairs


def main():
    all_exception_symbolics()
    orientations = all_exception_orientations()
    uw = complete_uw_cases()
    cuts = node_cut_extrema()
    bounds, exceptional_pairs = bridge_bounds()
    path = Path(__file__).resolve()
    source = path.with_name('k4_low_hub_reduction_v16.tex')
    if not source.exists():
        source = path.parent.parent/'papers/sections/paper'/source.name
    assert source.exists(), source
    result = {
        'version': 'v16', 'passed': True,
        'scope': 'Necessary conditions for K4 high support with an all-low fifth core; no existence or complete exclusion of K4 is claimed.',
        'general_proofs': [
            'Ordinary reverse has absolute value at most four.',
            'Low-hub D opposition is a divergence equation on ordinary edges.',
            'Every ordinary bridge has denominator at most twenty-five.',
            'With four exceptional edges, both ordinary denominators are at most twenty-five, or at most seven if disjoint.',
            'With two exceptional edges their positive/negative denominator pair is (3,7) or (5,9).',
            'Six exceptional edges are impossible, so the exceptional count is two or four.',
        ],
        'assumptions': ['integer row sums and pair products', 'odd high denominators greater than one',
                        'integer clutching at common low puncture', 'D opposition on four hub edges',
                        'nonnegative hub-edge node counts'],
        'not_assumed': ['three-high matching classification', 'positive weights',
                        'artificial denominator cutoff', 'D opposition on high edges'],
        'polynomial_identity_count': len(IDENTITIES), 'polynomial_identities': IDENTITIES,
        'all_exception_signed_orientations': orientations,
        'proof_derived_complete_uw_cases': uw,
        'all_exception_survivors': 0,
        'node_cut_extrema': cuts, 'bridge_bounds': bounds,
        'two_exception_denominator_pairs': exceptional_pairs,
        'two_exception_large_common_endpoint_argument': {
            'P': 'q_positive-1, a positive even integer', 'M': 'P+4>=6',
            'ordinary_reverse_at_common_big_endpoint': 3,
            'all_incoming_hub_entries': 0,
            'D_requires_outgoing_X_sum': -2,
            'actual_outgoing_X_sum': '(q_ordinary-1)/3 > 0',
            'status': 'contradiction in general; no finite P enumeration'},
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'external_peer_review': False, 'formal_proof_assistant': False,
    }
    output = path.with_name('k4_low_hub_verification_v16.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'passed': True, 'polynomial_identities': len(IDENTITIES),
                      'signed_orientations': len(orientations), 'complete_uw_cases': len(uw),
                      'node_matrices': cuts['all_node_matrices'], 'result': str(output)},
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
