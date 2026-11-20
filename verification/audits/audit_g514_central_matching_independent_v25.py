#!/usr/bin/env python3
"""Independent exact audit of the central-matching restriction in G514.

The primary verifier is not imported.  This file checks all 16 labelled sign
assignments, the unbounded one-positive unit-branch normal form as polynomials,
and both final contradictions using their original row and pair equations.
"""
from argparse import ArgumentParser
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib
import json


class P:
    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @classmethod
    def var(cls, name):
        return cls({(name,): 1})

    @classmethod
    def of(cls, x):
        return x if isinstance(x, cls) else cls({(): x})

    def __add__(self, x):
        result = self.terms.copy()
        for m, c in self.of(x).terms.items():
            result[m] = result.get(m, 0) + c
        return P(result)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.terms.items()})

    def __sub__(self, x):
        return self + (-self.of(x))

    def __rsub__(self, x):
        return self.of(x) - self

    def __mul__(self, x):
        result = {}
        for m, c in self.terms.items():
            for n, d in self.of(x).terms.items():
                key = tuple(sorted(m + n))
                result[key] = result.get(key, 0) + c * d
        return P(result)

    __rmul__ = __mul__

    def __eq__(self, x):
        return self.terms == self.of(x).terms


def apply_labels(f, permutation):
    result = [None] * 4
    for i in range(4):
        result[permutation[i]] = permutation[f[i]]
    return tuple(result)


def normal_chart(i, j, a, b, c, r, h, k):
    R = 2 * h - k
    row_i, row_j = [P.of(2), P.of(-1), P.of(-2)], [P.of(-1), P.of(1), P.of(-1)]
    col_i, col_j = [2 * r, P.of(-k), -R], [-2 * r, 2 * h, P.of(-2)]
    qi = [4 * r + 1, P.of(k + 1), 2 * R + 1]
    qj = [2 * r + 1, 2 * h + 1, P.of(3)]
    q = {}
    local = {}
    outer = {}
    for slot, x in enumerate((a, b, c)):
        q[tuple(sorted((i, x)))] = qi[slot]
        q[tuple(sorted((j, x)))] = qj[slot]
        local[(i, j, x)] = row_i[slot]
        local[(i, x, j)] = col_i[slot]
        local[(j, i, x)] = row_j[slot]
        local[(j, x, i)] = col_j[slot]
        alpha, beta = [(0, -3), (-1, -k), (1, 0)][slot]
        outer[(x, i, j)] = qi[slot] * alpha - col_i[slot]
        outer[(x, j, i)] = qj[slot] * beta - col_j[slot]
    return dict(q=q, local=local, outer=outer, rows=[row_i, row_j],
                columns=[col_i, col_j], R=R)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    parser = ArgumentParser()
    parser.add_argument('--source', type=Path)
    parser.add_argument('--output', type=Path,
                        default=here / 'g514_central_matching_independent_audit_v25.json')
    args = parser.parse_args()
    choices = [here.parent / 'unit_gluing/g514_central_matching_v25.tex',
               here.parents[1] / 'papers/sections/paper/g514_central_matching_v25.tex',
               here / 'g514_central_matching_v25.tex']
    source = args.source or next(path for path in choices if path.exists())
    checks = []

    def check(name, left, right):
        assert left == right, name
        checks.append(name)

    # The full set before using the outside-positive witness consists of 36
    # assignments with different low-positive positions on each unit branch.
    raw = []
    normalized = Counter()
    sign_records = []
    for f0, f1 in product((2, 3, 4), repeat=2):
        for f2, f3 in product((0, 1, 4), repeat=2):
            if f0 == f1 or f2 == f3:
                continue
            raw.append((f0, f1, f2, f3))
            if (f0 == 4) + (f1 == 4) != 1 or (f2 == 4) + (f3 == 4) != 1:
                continue
            labels = list(range(5))
            if f0 == 4:
                labels[0], labels[1] = 1, 0
            if f2 == 4:
                labels[2], labels[3] = 3, 2
            transformed = apply_labels((f0, f1, f2, f3), labels)
            assert transformed[1] == transformed[3] == 4
            kind = (transformed[0], transformed[2])
            normalized[kind] += 1
            sign_records.append({'f': [f0, f1, f2, f3],
                                 'permutation': labels, 'normal_f': transformed})
    assert len(raw) == 36 and len(sign_records) == 16
    assert normalized == {(3, 0): 4, (3, 1): 4, (2, 1): 4, (2, 0): 4}
    exchange = [2, 3, 0, 1, 4]
    assert apply_labels((2, 4, 1, 4), exchange) == (3, 4, 0, 4)

    r, h, rp, hp, q24, p40 = map(P.var, 'r h rp hp q24 p40'.split())
    # Original low rows, six low pairs, three exterior pairs, all clutching
    # coefficients, unit node distribution, and low D are checked for each k.
    normal_records = []
    for k in (2, 4):
        chart = normal_chart(0, 1, 2, 4, 3, r, h, k)
        for index, row in enumerate(chart['rows']):
            check(f'k={k} low row {index}', sum(row), -1)
        check(f'k={k} opposing low D', -2 - sum(chart['columns'][0]) - sum(chart['columns'][1]), 0)
        for slot, x in enumerate((2, 4, 3)):
            check(f'k={k} unit node at {x}',
                  1 - chart['rows'][0][slot] - chart['rows'][1][slot], [0, 1, 4][slot])
            for endpoint, low in [(0, 1), (1, 0)]:
                check(f'k={k} low pair core{endpoint} ray{x}',
                      chart['local'][(endpoint, low, x)] * chart['local'][(endpoint, x, low)],
                      chart['q'][tuple(sorted((endpoint, x)))] - 1)
            check(f'k={k} exterior pair core{x}',
                  chart['outer'][(x, 0, 1)] * chart['outer'][(x, 1, 0)],
                  chart['q'][tuple(sorted((0, x)))] * chart['q'][tuple(sorted((1, x)))] - 1)
        check(f'k={k} E0 first entry', chart['outer'][(2, 0, 1)], -2 * r)
        check(f'k={k} E0 second entry', chart['outer'][(2, 1, 0)], -4 * r - 3)
        check(f'k={k} E3 first entry', chart['outer'][(4, 0, 1)], -1)
        check(f'k={k} E3 second entry', chart['outer'][(4, 1, 0)], -2 * h * (k + 1) - k)
        # Since h is integral and R=2h-k>0, its exact minimum is 2.
        least_h = k // 2 + 1
        assert 2 * least_h - k == 2
        normal_records.append({'k': k, 'R_expression': f'2*h-{k}',
                               'least_admissible_h': least_h, 'minimum_R': 2,
                               'minimum_2R_plus_1': 5,
                               'unit_nodes': [0, 1, 4]})

    # Non-mutual case: the negative opposite-position families, with positive
    # side denominator 3, give negative-side denominator only 3 or 5.
    vV = [(v, 2 // v) for v in (1, 2)]
    opposite_candidates = set()
    for v, V in vV:
        if v % 2 == 0:  # n=1 usual negative family: j=v, J=1
            opposite_candidates.add(v + 1)
        if v == 1 and V % 2 == 0:  # equal n=1 exception
            opposite_candidates.add(V + 1)
        if v == 2 and V == 1:  # small n=1 exception
            opposite_candidates.add(3)
        if v == 1 and V % 2 == 0:
            for J in (2, 4):
                opposite_candidates.add(J + 1)
    assert opposite_candidates == {3, 5}
    assert 4 * 1 + 1 > 3  # n=0 negative family's minimum positive denominator

    # Mutual case, both zero-node positions away from core4.
    first = normal_chart(0, 1, 2, 4, 3, r, h, 2)
    second_free = normal_chart(2, 3, 0, 4, 1, rp, hp, 4)
    check('shared q02 forces r=rp', first['q'][(0, 2)] - second_free['q'][(0, 2)], 4 * (r - rp))
    # Other parameters are irrelevant to this necessary row obstruction.
    second = normal_chart(2, 3, 0, 4, 1, r, hp, 4)
    entry01 = first['outer'][(2, 0, 1)]
    entry03 = second['local'][(2, 0, 3)]
    q02 = first['q'][(0, 2)]
    entry04 = -q02 - entry01 - entry03
    check('mutual-away original row gives p04=-q02', entry04, -q02)
    original_pair_residual = entry04 * p40 - (q02 * q24 - 1)
    check('mutual-away original pair forces q02 to divide 1',
          original_pair_residual + q02 * (p40 + q24), 1)

    # Mutual case, both zero-node positions at core4: shared denominators force
    # k=k'=2.  Verify the required shared values for both discrete choices.
    forced_k = []
    for k in (2, 4):
        first_k = normal_chart(1, 0, 4, 2, 3, r, h, k)
        second_k = normal_chart(3, 2, 4, 0, 1, rp, hp, k)
        if first_k['q'][(1, 2)] == second_k['q'][(1, 2)] == 3:
            forced_k.append(k)
    assert forced_k == [2]
    first = normal_chart(1, 0, 4, 2, 3, r, h, 2)
    second = normal_chart(3, 2, 4, 0, 1, rp, hp, 2)
    entry10 = first['outer'][(2, 1, 0)]
    entry13 = second['local'][(2, 1, 3)]
    q12 = first['q'][(1, 2)]
    check('mutual-at-four q12=3', q12, 3)
    check('mutual-at-four p10=-1', entry10, -1)
    check('mutual-at-four p13=-2', entry13, -2)
    entry14 = -q12 - entry10 - entry13
    check('mutual-at-four original row gives p14=0', entry14, 0)
    check('mutual-at-four original pair residual', entry14 * p40 - (q12 * q24 - 1), 1 - 3 * q24)

    # The mixed node-zero cases require 3=2R+1 with R>=2 and hence fail.
    node_zero_choices = [
        {'unit01': 2, 'unit23': 0, 'type': 'mutual_away_row_divisibility'},
        {'unit01': 2, 'unit23': 4, 'type': 'mixed_q13_3_vs_at_least_5'},
        {'unit01': 4, 'unit23': 0, 'type': 'mixed_q13_at_least_5_vs_3'},
        {'unit01': 4, 'unit23': 4, 'type': 'mutual_at_four_zero_entry'},
    ]
    report = {
        'version': 'v25', 'status': 'PASS',
        'independence': 'No primary verifier or project proof helper imported.',
        'scope': 'Sign-label completeness, original unit rows/columns/pairs/node/D '
                 'and clutching for the one-positive normal form, and both final '
                 'original row/pair obstructions. The normal-form case exclusions '
                 'and inherited unit-position classification were also reviewed analytically.',
        'raw_distinct_low_positive_assignments': len(raw),
        'outside_witness_compatible_assignments': len(sign_records),
        'normalized_sign_counts': {str(k): v for k, v in sorted(normalized.items())},
        'sign_records': sign_records, 'normal_form_records': normal_records,
        'polynomial_identity_count': len(checks), 'polynomial_identities': checks,
        'nonmutual_negative_side_denominators': sorted(opposite_candidates),
        'mutual_node_zero_choices': node_zero_choices,
        'mutual_away_obstruction': 'q02*(p40+q24)=1 with q02=4*r+1>=5',
        'mutual_at_four_obstruction': 'p14=0 but p14*p41=3*q24-1>0',
        'all_parameter_arguments_unbounded': True,
        'global_G514_nonexistence_claim': False,
        'external_peer_review': False, 'proof_assistant_formalization': False,
        'proof_file': source.name, 'proof_sha256': sha(source),
        'audit_script_sha256': sha(Path(__file__)),
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in [
        'status', 'outside_witness_compatible_assignments',
        'normalized_sign_counts', 'polynomial_identity_count']}))


if __name__ == '__main__':
    main()
