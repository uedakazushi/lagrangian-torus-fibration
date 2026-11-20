#!/usr/bin/env python3
"""Independent audit of the G514 node-five factor obstruction.

No project module or primary verifier is imported.  The seven normal forms are
regenerated from the five common-negative-position possibilities and u*A=6.
For every positive divisor pair of 8 or 20, this audit reconstructs the original
four-row matrix.  Six pair equations and three rows hold identically over Q[B];
the fourth row gives the independently computed obstruction.  Identically-zero
row obstructions are rejected by the original entry integrality requirement.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json


class Polynomial:
    """Univariate rational polynomial, independent of the primary verifier."""

    def __init__(self, coefficients=()):
        self.coefficients = tuple(map(Fraction, coefficients))
        while self.coefficients and self.coefficients[-1] == 0:
            self.coefficients = self.coefficients[:-1]

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls([value])

    def __add__(self, other):
        other = self.coerce(other)
        length = max(len(self.coefficients), len(other.coefficients))
        return Polynomial([self.coefficient(i) + other.coefficient(i)
                           for i in range(length)])

    __radd__ = __add__

    def __neg__(self):
        return Polynomial([-a for a in self.coefficients])

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        if not self.coefficients or not other.coefficients:
            return Polynomial()
        coefficients = [Fraction(0)] * (len(self.coefficients) + len(other.coefficients) - 1)
        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):
                coefficients[i + j] += a * b
        return Polynomial(coefficients)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return Polynomial([a / scalar for a in self.coefficients])

    def __eq__(self, other):
        return self.coefficients == self.coerce(other).coefficients

    def coefficient(self, index):
        return self.coefficients[index] if index < len(self.coefficients) else Fraction(0)


def divisors(n):
    """Exact complete divisor enumeration; n is a forced constant, 8 or 20."""
    answer = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            answer.append(d)
            if d * d != n:
                answer.append(n // d)
        d += 1
    return sorted(answer)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    parser = ArgumentParser()
    parser.add_argument('--source', type=Path)
    parser.add_argument('--output', type=Path,
                        default=here / 'g514_five_node_independent_audit_v25.json')
    args = parser.parse_args()
    candidates = [here.parent / 'unit_gluing/g514_five_node_exclusion_v25.tex',
                  here.parent / 'paper/g514_five_node_exclusion_v25.tex',
                  here / 'g514_five_node_exclusion_v25.tex']
    source = args.source or next(p for p in candidates if p.exists())
    variable = Polynomial([0, 1])

    # These five possibilities are the node-five entries of the proved
    # common-negative-position classification.  Reconstruct all seven cases
    # after the second unit branch has forced q03=7 and q02 in {3,7}.
    five_node_quads = [(1, 3, 2, 2), (2, 2, 1, 3), (2, 2, 2, 2),
                       (2, 2, 3, 1), (3, 1, 2, 2)]
    tags = {
        (3, 1, 2, 2, 3, 2, 1): 'A1',
        (2, 2, 3, 1, 2, 3, 1): 'A2',
        (2, 2, 3, 1, 3, 2, 2): 'A3',
        (1, 3, 2, 2, 2, 3, 2): 'B1',
        (1, 3, 2, 2, 3, 2, 3): 'B2',
        (2, 2, 1, 3, 2, 3, 1): 'B3',
        (2, 2, 1, 3, 3, 2, 2): 'B4',
    }
    generated = {}
    normal_records = []
    for s, sp, S, T in five_node_quads:
        assert s + sp == S + T == 4
        assert s * S % 2 == sp * T % 2 == 0
        for u in divisors(6):
            A = 6 // u
            if min(u, A) < 2:
                continue
            t = u - s + 1
            if t < 1:
                continue
            q02, q12 = s * S + 1, sp * T + 1
            q03, q13 = u * A + 1, (u - 1) * (A - 1) + 1
            if (q02, q03, q12, q13) not in [(7, 7, 3, 3), (3, 7, 7, 3)]:
                continue
            key = (s, sp, S, T, u, A, t)
            assert key in tags
            tag = tags[key]
            generated[key] = tag

            low_row_0 = [u, -t, -s]
            low_row_1 = [1 - u, t + 1, -sp]
            low_col_0 = [Polynomial.coerce(A), 1 - variable, Polynomial.coerce(-S)]
            low_col_1 = [Polynomial.coerce(1 - A), variable, Polynomial.coerce(-T)]
            assert sum(low_row_0) == sum(low_row_1) == -1
            nodes = [1 - x - y for x, y in zip(low_row_0, low_row_1)]
            assert nodes == [0, 0, 5]
            assert -2 - sum(low_col_0) - sum(low_col_1) == 0
            q0 = [Polynomial.coerce(q03), t * (variable - 1) + 1,
                  Polynomial.coerce(q02)]
            q1 = [Polynomial.coerce(q13), (t + 1) * variable + 1,
                  Polynomial.coerce(q12)]
            for row, col, qs in [(low_row_0, low_col_0, q0),
                                 (low_row_1, low_col_1, q1)]:
                assert all(Polynomial.coerce(p) * pp == qq - 1
                           for p, pp, qq in zip(row, col, qs))
            m, n, v = q13, q12, t + 1
            aa, bb = m - (A - 1), n - T
            normal_records.append({'case': tag, 'normal_tuple': key,
                                   'q02_q03_q12_q13': [q02, q03, q12, q13],
                                   'm_n_v_a_b': [m, n, v, aa, bb],
                                   'unit_nodes': nodes,
                                   'low_rows_columns_pairs_and_D_checked': True})
    assert generated == tags
    normal_records.sort(key=lambda record: record['case'])

    expected_table = {
        'A1': ['-1/3', '-1/3', 'identity', '-1/3'],
        'A2': ['-1/3', 'identity', '-1/3', '-1/3'],
        'A3': ['-4/3', '-2/3', '-2/3', '-4/3'],
        'B1': ['-12/67', '-1/6', '0', '0', '3/14', '4/3'],
        'B2': ['7/9', '-3/4', '-1/3', '-3/11', 'inconsistent', '-3/7'],
        'B3': ['-3/7', 'inconsistent', '3/11', '1/3', '3/2', '-31/9'],
        'B4': ['-2/3', '-2/7', '0', '2/5', '-2/3', '-32/67'],
    }
    factor_records = []
    reasons = Counter()
    raw_pair_identities = 0
    raw_row_identities = 0
    for normal in normal_records:
        tag = normal['case']
        s, sp, S, T, u, A, t = normal['normal_tuple']
        m, n, v, aa, bb = normal['m_n_v_a_b']
        N = m * n - 1
        assert N in (8, 20)
        ls = divisors(N)
        assert ls == ([1, 2, 4, 8] if N == 8 else [1, 2, 4, 5, 10, 20])
        actual_table = []
        for L in ls:
            M = N // L
            # Construct the original four-ray matrix in the order (low,3,2,4).
            # Rows 0,1,2 and every pair are imposed directly; no C,E formula
            # from the primary verifier is used to build this matrix.
            last_q = v * variable + 1
            first_to_last = -m + (A - 1) - L
            second_to_last = -n + T - M
            last_to_first = (m * last_q - 1) / first_to_last
            last_to_second = (n * last_q - 1) / second_to_last
            matrix = [
                [0, -(u - 1), -sp, v],
                [-(A - 1), 0, L, first_to_last],
                [-T, M, 0, second_to_last],
                [variable, last_to_first, last_to_second, 0],
            ]
            matrix = [[Polynomial.coerce(x) for x in row] for row in matrix]
            qs = list(map(Polynomial.coerce, [1, m, n, last_q]))
            for i in range(3):
                assert sum(matrix[i]) + qs[i] == 0
                raw_row_identities += 1
            for i, j in combinations(range(4), 2):
                assert matrix[i][j] * matrix[j][i] == qs[i] * qs[j] - 1
                raw_pair_identities += 1
            divisor_1, divisor_2 = -first_to_last, -second_to_last
            assert divisor_1 == L + aa > 0 and divisor_2 == M + bb > 0
            # Derive the row residual from the constructed matrix first.
            cleared_row = (sum(matrix[3]) + qs[3]) * divisor_1 * divisor_2
            assert len(cleared_row.coefficients) <= 2
            C = -cleared_row.coefficient(1)
            E = -cleared_row.coefficient(0)
            assert C.denominator == E.denominator == 1
            C, E = int(C), int(E)
            # Independently compare with the displayed closed formula.
            assert C == m * v * divisor_2 + n * v * divisor_1 - (v + 1) * divisor_1 * divisor_2
            assert E == (m - 1) * divisor_2 + (n - 1) * divisor_1 - divisor_1 * divisor_2
            entry = {'case': tag, 'L': L, 'M': M, 'C': C, 'E': E,
                     'reverse_entry_denominators': [divisor_1, divisor_2],
                     'all_six_original_pairs_verified': True,
                     'three_original_rows_verified': True}
            if C:
                candidate = Fraction(-E, C)
                assert candidate.denominator != 1 or candidate < 1
                assert candidate.denominator != 1 or candidate < 2
                actual_table.append(str(candidate))
                entry.update(candidate_B=str(candidate), reason='no_positive_integer_B')
                reasons['no_positive_integer_B'] += 1
            elif E:
                actual_table.append('inconsistent')
                entry['reason'] = 'nonzero_constant_row_residual'
                reasons['nonzero_constant_row_residual'] += 1
            else:
                # Here the original row and pair equations really do hold as
                # rational functions.  Their integral entries still fail.
                assert sum(matrix[3]) + qs[3] == 0
                bad_entries = []
                for j in (1, 2):
                    reverse = matrix[3][j]
                    if reverse.coefficient(1).denominator == 1 and reverse.coefficient(0).denominator > 1:
                        bad_entries.append({'column': j,
                                            'B_coefficient': str(reverse.coefficient(1)),
                                            'constant': str(reverse.coefficient(0))})
                assert bad_entries
                assert any(record['B_coefficient'] == '-1' and record['constant'] == '-1/3'
                           for record in bad_entries)
                actual_table.append('identity')
                entry.update(reason='nonintegral_reverse_entry_for_every_integer_B',
                             offending_entries=bad_entries)
                reasons['nonintegral_reverse_entry_for_every_integer_B'] += 1
            factor_records.append(entry)
        assert actual_table == expected_table[tag], (tag, actual_table)

    assert len(factor_records) == 3 * 4 + 4 * 6 == 36
    assert reasons == {'no_positive_integer_B': 32,
                       'nonzero_constant_row_residual': 2,
                       'nonintegral_reverse_entry_for_every_integer_B': 2}
    report = {
        'version': 'v25', 'status': 'PASS',
        'auditor': 'independent four-high agent; no primary verifier imported',
        'scope': 'Independent exact audit of all seven node-five normal forms, original '
                 'low rows/columns/unit nodes/D, and all 36 complete divisor cases in '
                 'the fixed-core obstruction. The preceding unit-position classification '
                 'and second-branch sign deductions were also reviewed analytically.',
        'normal_forms_regenerated': normal_records,
        'complete_forced_factor_sets': {'8': divisors(8), '20': divisors(20)},
        'factor_case_count': len(factor_records),
        'raw_pair_polynomial_identity_count': raw_pair_identities,
        'raw_row_polynomial_identity_count_before_last_row': raw_row_identities,
        'exclusion_counts': dict(reasons), 'factor_cases': factor_records,
        'all_paper_table_entries_matched': True,
        'identically_zero_cases_excluded_by_original_integrality': True,
        'denominator_cutoff_or_parameter_sampling_used': False,
        'global_G514_nonexistence_claim': False,
        'external_peer_review': False, 'proof_assistant_formalization': False,
        'proof_file': source.name, 'proof_sha256': sha(source),
        'audit_script_sha256': sha(Path(__file__)),
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in [
        'status', 'factor_case_count', 'raw_pair_polynomial_identity_count',
        'raw_row_polynomial_identity_count_before_last_row', 'exclusion_counts']}))


if __name__ == '__main__':
    main()
