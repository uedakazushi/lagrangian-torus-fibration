#!/usr/bin/env python3
"""Exact checks for the unbounded four-ray P4 obstruction (stdlib only).

This verifier reconstructs the original four rows and five pair equations as
formal rational functions.  The remaining pair residual is then compared with
the positive polynomial identity in four_ray_matching_v25.tex.  Neither a
bounded denominator search nor sampling is used to prove nonexistence.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib
import json


class Poly:
    """Integer sparse polynomials; a monomial is a sorted tuple of names."""

    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @classmethod
    def var(cls, name):
        return cls({(name,): 1})

    @classmethod
    def coerce(cls, value):
        if isinstance(value, cls):
            return value
        if not isinstance(value, int):
            raise TypeError(type(value))
        return cls({(): value})

    def __add__(self, other):
        answer = self.terms.copy()
        for monomial, coefficient in self.coerce(other).terms.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
        return Poly(answer)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        answer = {}
        for m, c in self.terms.items():
            for n, d in self.coerce(other).terms.items():
                key = tuple(sorted(m + n))
                answer[key] = answer.get(key, 0) + c * d
        return Poly(answer)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms

    def substitute(self, values):
        answer = Poly()
        for monomial, coefficient in self.terms.items():
            term = Poly.coerce(coefficient)
            for variable in monomial:
                term = term * values.get(variable, Poly.var(variable))
            answer += term
        return answer


class Rat:
    """Formal rational functions checked by polynomial cross multiplication.

    Only common monomial factors are cancelled; a polynomial gcd or external
    computer algebra system is unnecessary for this certificate.
    """

    def __init__(self, numerator, denominator=1):
        numerator, denominator = Poly.coerce(numerator), Poly.coerce(denominator)
        if denominator == 0:
            raise ZeroDivisionError
        if numerator == 0:
            self.n, self.d = Poly(), Poly.coerce(1)
            return
        common = None
        for monomial in list(numerator.terms) + list(denominator.terms):
            factors = Counter(monomial)
            common = factors if common is None else common & factors
        def cancel(polynomial):
            answer = {}
            for monomial, coefficient in polynomial.terms.items():
                reduced = Counter(monomial) - common
                answer[tuple(sorted(reduced.elements()))] = coefficient
            return Poly(answer)
        self.n, self.d = cancel(numerator), cancel(denominator)

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls(value)

    def __add__(self, other):
        other = self.coerce(other)
        return Rat(self.n * other.d + other.n * self.d, self.d * other.d)

    __radd__ = __add__

    def __neg__(self):
        return Rat(-self.n, self.d)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return Rat(self.n * other.n, self.d * other.d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        return Rat(self.n * other.d, self.d * other.n)

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __eq__(self, other):
        other = self.coerce(other)
        return self.n * other.d == other.n * self.d


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def positive_expression(v):
    q, t, a, C, s, r, L, D, h, K = (
        v[name] for name in 'q t a C s r L D h K'.split())
    return (
        q * s * K * t * t
        + (a * q * C * s * (L + D) + q * q * h * K
           + a * L * q * q + s * (r + C * q) + D * s * q) * t
        + (a * D + 1) * q * (a * C * s + h * (r + C * q) + a * q)
        + D * q * (a * s + q * h)
    )


def fixture(name, q, matrix, weights):
    assert all(sum(row) == -qi for row, qi in zip(matrix, q)), name
    pairs = list(combinations(range(4), 2))
    assert all(matrix[i][j] * matrix[j][i] == q[i] * q[j] - 1 > 0
               for i, j in pairs), name
    margins = [weights[j] - Fraction(matrix[i][j], q[i]) * weights[i]
               for i in range(4) for j in range(4) if i != j]
    assert min(margins) > 0, name
    positive_edges = [(i, j) for i, j in pairs if matrix[i][j] > 0]
    assert all(sum(i in edge for edge in positive_edges) == 1
               for i in range(4)), name
    return {'name': name, 'q': q, 'P': matrix,
            'weights': [str(w) for w in weights],
            'positive_edges': positive_edges,
            'minimum_basin_margin': str(min(margins)),
            'all_four_rows_and_six_pairs_verified': True,
            'all_twelve_basin_inequalities_verified': True,
            'new_example': False}


def main():
    here = Path(__file__).resolve().parent
    parser = ArgumentParser()
    parser.add_argument('--source', type=Path)
    parser.add_argument('--output', type=Path,
                        default=here / 'four_ray_matching_verification_v25.json')
    args = parser.parse_args()
    candidates = [here / 'four_ray_matching_v25.tex',
                  here.parent / 'paper/four_ray_matching_v25.tex']
    source = args.source or next(p for p in candidates if p.exists())
    identities = []

    def check(name, left, right):
        assert left == right, name
        identities.append(name)

    # Route 1: start with the abbreviations in the proof and certify the
    # coefficient identity.  This calculation is purely polynomial.
    t, a, b, c, B, C, q = map(Poly.var, 't a b c B C q'.split())
    s, r, L = b * B + 1, c * C + 1, B + c
    D, h, K = L + q, a * b - 1, B * C - 1
    T = (a + t) * s + q * h
    U = t * L + a * D + 1
    V = t * s * (r + C * q) + q * (a * C * s + h * (r + C * q) + a * q)
    obstruction = U * V - D * T * (t * r - q)
    values = dict(q=q, t=t, a=a, C=C, s=s, r=r, L=L, D=D, h=h, K=K)
    certificate = positive_expression(values)
    check('key identity L(r+Cq)-Dr=qK', L * (r + C * q) - D * r, q * K)
    check('positive certificate equals UV-DT(tr-q)', certificate, obstruction)

    # Positivity is checked before substituting h=ab-1 and K=BC-1.
    # h,K are nonnegative; all other formal variables are strictly positive.
    formal = {name: Poly.var(name) for name in values}
    positive_formal = positive_expression(formal)
    assert all(coefficient > 0 for coefficient in positive_formal.terms.values())
    assert positive_formal.terms.get(tuple(sorted(('s', 'r', 't')))) == 1
    check('formal positive sum substitutes to certificate',
          positive_formal.substitute(values), certificate)

    # Route 2: reconstruct directly from the raw four rows and five pairs,
    # independently of T,U,V.  All identities are rational-function equalities.
    qt, qa, qb, qc, qB, qC, qq = map(Rat, (t, a, b, c, B, C, q))
    q1, q3 = qt, qq
    q2 = (qb * qB + 1) / q3
    q4 = (qc * qC + 1) / q3
    AA = (q1 * q2 - 1) / qa
    DD = q3 + qB + qc
    dd = (q1 * q3 - 1) / DD
    ee = q1 + qa - dd
    ff = q2 + AA + qb
    FF = (q2 * q4 - 1) / ff
    EE = q4 + qC - FF
    matrix = [[Rat(0), qa, -dd, -ee],
              [AA, Rat(0), qb, -ff],
              [-DD, qB, Rat(0), qc],
              [-EE, -FF, qC, Rat(0)]]
    qraw = [q1, q2, q3, q4]
    for i in range(4):
        check(f'original row {i + 1}', sum(matrix[i]) + qraw[i], 0)
    for i, j in combinations(range(4), 2):
        if (i, j) != (0, 3):
            check(f'original pair {i + 1}{j + 1}',
                  matrix[i][j] * matrix[j][i] - qraw[i] * qraw[j] + 1, 0)
    check('T=aqf from original equations', qa * q3 * ff, T)
    check('U=De from original equations', DD * ee, U)
    check('V=qTE from original equations', q3 * Rat(T) * EE, V)
    residual = ee * EE - (q1 * q4 - 1)
    check('remaining pair residual times q^2 a D f',
          q3 * q3 * qa * DD * ff * residual, obstruction)

    # Independent integer-gap identity for the no-weights sign classification.
    qi, qh, ci, cj, ck, pij, pik, pih = map(
        Poly.var, 'qi qh ci cj ck pij pik pih'.split())
    gap_minus_one = qi * (cj + ck) - ci * (pij + pik) - 1
    combination_of_raw_residuals = (
        qi * (ci + cj + ck - qh)
        - ci * (pij + pik + pih + qi)
        + qi * qh + ci * pih - 1)
    check('integer-gap sum=1 from raw row and pair residuals',
          gap_minus_one, combination_of_raw_residuals)
    cycle_records = []
    for targets in product(*[[j for j in range(3) if j != i] for i in range(3)]):
        walk, vertex = [], 0
        while vertex not in walk:
            walk.append(vertex)
            vertex = targets[vertex]
        cycle = walk[walk.index(vertex):]
        powers = [0, 0, 0]
        for vertex in cycle:
            powers[targets[vertex]] += 1
            powers[vertex] -= 1
        assert len(cycle) in (2, 3) and powers == [0, 0, 0]
        cycle_records.append({'targets': targets, 'cycle': cycle,
                              'telescoping_exponents': powers})

    # Every labelled sign graph is accounted for.  This is finite graph
    # combinatorics, not a scan over q or the p entries.
    edges = list(combinations(range(4), 2))
    graph_counts = Counter()
    for mask in range(64):
        selected = [edge for i, edge in enumerate(edges) if mask >> i & 1]
        degrees = [sum(v in edge for edge in selected) for v in range(4)]
        if max(degrees) > 2:
            graph_counts['excluded_by_negative_row_sum'] += 1
        elif min(degrees) == 0:
            if sorted(degrees) == [0, 2, 2, 2]:
                assert len(selected) == 3
                graph_counts['triangle_and_isolated'] += 1
            else:
                graph_counts['excluded_by_integer_gap_cycle'] += 1
        elif degrees == [2, 2, 2, 2]:
            graph_counts['C4_excluded_by_negative_pair'] += 1
        elif len(selected) == 2:
            assert degrees == [1, 1, 1, 1]
            graph_counts['matching'] += 1
        else:
            assert len(selected) == 3 and sorted(degrees) == [1, 1, 2, 2]
            graph_counts['P4_excluded_by_positive_certificate'] += 1
    assert sum(graph_counts.values()) == 64
    assert graph_counts['matching'] == 3
    assert graph_counts['triangle_and_isolated'] == 4
    assert graph_counts['P4_excluded_by_positive_certificate'] == 12
    assert graph_counts['C4_excluded_by_negative_pair'] == 3

    # Inherited triangle fixture: all raw equations hold, but a directed
    # triangle has gain >1.  This demonstrates why weights matter.
    bad_q = [1, 5, 19, 31]
    bad_P = [[0, 1, 1, -3], [4, 0, 2, -11],
             [18, 47, 0, -84], [-10, -14, -7, 0]]
    assert all(sum(row) == -qi for row, qi in zip(bad_P, bad_q))
    assert all(bad_P[i][j] * bad_P[j][i] == bad_q[i] * bad_q[j] - 1 > 0
               for i, j in edges)
    bad_c = [-bad_P[3][i] for i in range(3)]
    bad_g = [[0 if i == j else bad_q[i] * bad_c[j] - bad_c[i] * bad_P[i][j]
              for j in range(3)] for i in range(3)]
    assert all(sum(row) == 1 for row in bad_g)
    bad_gain = Fraction(bad_P[0][2] * bad_P[2][1] * bad_P[1][0],
                        bad_q[0] * bad_q[2] * bad_q[1])
    assert bad_gain == Fraction(188, 95) > 1

    fixtures = [
        fixture('inherited four-high matching', [3, 5, 5, 17],
                [[0, -14, -14, 25], [-1, 0, 3, -7],
                 [-1, 8, 0, -12], [2, -12, -7, 0]],
                list(map(Fraction, [1, 1])) + [Fraction(49, 80), Fraction(101, 12)]),
        fixture('inherited three-high matching', [1, 5, 5, 3],
                [[0, -1, -2, 2], [-4, 0, 6, -7],
                 [-2, 4, 0, -7], [1, -2, -2, 0]],
                [Fraction(1), Fraction(1), Fraction(49, 40), Fraction(5, 2)]),
    ]
    monomial_record = [{'monomial': list(m), 'coefficient': coefficient}
                       for m, coefficient in sorted(obstruction.terms.items())]
    canonical = json.dumps(monomial_record, sort_keys=True, separators=(',', ':'))
    report = {
        'version': 'v25', 'status': 'PASS',
        'theorem_scope': 'Four positive integer q_i, integral p_ij, four row equations, '
                         'and six strictly positive pair products q_i*q_j-1. '
                         'The positive sign graph P4 is impossible without assuming weights.',
        'corollary': 'Together with the integer-gap lemma, positive basin weights exist '
                     'if and only if the positive sign graph is a perfect matching. '
                     'Both three-high and four-high strict-pair cores are covered.',
        'full_sign_classification_without_weights':
            'The positive graph is either 2K2 or K3 disjoint union K1. '
            'The latter has a directed triangle of gain at least 1.',
        'proof_method': 'Unbounded positive polynomial identity derived from all raw equations.',
        'identity_count': len(identities), 'identities': identities,
        'expanded_obstruction_monomial_count': len(obstruction.terms),
        'expanded_obstruction_sha256': hashlib.sha256(canonical.encode()).hexdigest(),
        'positive_formal_monomial_count': len(positive_formal.terms),
        'positive_formal_all_coefficients_positive': True,
        'nonnegative_variables': ['h=ab-1', 'K=BC-1'],
        'strictly_positive_variables': ['q', 't', 'a', 'C', 's', 'r', 'L', 'D'],
        'strictly_positive_monomial': 's*r*t, with coefficient 1',
        'all_divisors_positive_in_original_model': ['a', 'q', 'D', 'T=aqf'],
        'four_rows_and_five_pairs_symbolically_verified': True,
        'sixth_pair_residual_identity_symbolically_verified': True,
        'low_denominator_one_assumption_used': False,
        'labelled_graphs_checked': 64, 'graph_counts': dict(graph_counts),
        'all_three_vertex_outgoing_maps': cycle_records,
        'inherited_matching_fixtures': fixtures,
        'inherited_triangle_fixture': {'q': bad_q, 'P': bad_P,
                                      'isolated_vertex': 3, 'gaps': bad_g,
                                      'positive_cycle': [0, 2, 1],
                                      'cycle_gain': str(bad_gain),
                                      'all_four_rows_and_six_pairs_verified': True},
        'arbitrary_parameter_scan_used': False,
        'global_clutching_or_atlas_existence_claim': False,
        'external_peer_review': False, 'proof_assistant_formalization': False,
        'proof_file': source.name, 'proof_sha256': digest(source),
        'verifier_sha256': digest(Path(__file__)),
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in [
        'status', 'identity_count', 'expanded_obstruction_monomial_count',
        'positive_formal_monomial_count', 'graph_counts']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
