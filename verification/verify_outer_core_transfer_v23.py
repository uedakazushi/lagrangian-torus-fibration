#!/usr/bin/env python3
"""Exact algebra and regression certificates for the third-core transfer lemma.

The unbounded resonance classification is proved in the accompanying text.
The bounded a regression below is not used as a substitute for that proof.
Only Python's standard library is required.
"""
from collections import Counter
from hashlib import sha256
from itertools import product
from math import isqrt
from pathlib import Path
import argparse
import json


class Poly:
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {k: v for k, v in value.items() if v}
        else:
            self.terms = {(): int(value)} if value else {}

    @classmethod
    def variable(cls, name):
        return cls({(name,): 1})

    def __add__(self, other):
        out = Counter(self.terms)
        for k, v in Poly(other).terms.items():
            out[k] += v
        return Poly(dict(out))

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) + (-self)

    def __mul__(self, other):
        out = Counter()
        for k, v in self.terms.items():
            for l, w in Poly(other).terms.items():
                out[tuple(sorted(k+l))] += v*w
        return Poly(dict(out))

    __rmul__ = __mul__


def coefficients():
    a, p, j, s, u, v = map(Poly.variable, ['a', 'p', 'j', 'S', 'u', 'v'])
    checks = []
    for eps in [-1, 1]:
        E = a*u-p
        D = E*(j*v-eps)-a*j
        N = a-1-E*v
        original = E*((j*s+1)*v-eps*s)-a*(j*s+1)+1
        identities = [
            ('original pair equals linear residual', original-(D*s-N)),
            ('resonance elimination', D+j*N+eps*E+j),
            ('resonance converse', (-eps*j)*(j*v-eps)-a*j+j*(a-1+eps*j*v)),
            ('denominator divisibility on solutions', (j*s+1)*D+eps*E+j-j*(D*s-N)),
        ]
        for name, difference in identities:
            assert not difference.terms, (eps, name, difference.terms)
            checks.append({'epsilon': eps, 'identity': name, 'all_coefficients_zero': True})
    return checks


def divisors(n):
    out = set()
    for d in range(1, isqrt(n)+1):
        if n % d == 0:
            out.update([d, n//d])
    return sorted(out)


def classified_resonances(a):
    # Rows are (epsilon,j,p,u,v), from the closed classification in the proof.
    out = {(-1, a-1, 1, 1, 1), (-1, a-1, -(a-1), 0, 1),
           (1, a-1, -1, -1, -1)}
    for h in range(1, 5):
        if (a-1) % h == 0:
            out.add((1, (a-1)//h, (a-1)//h, 0, -h))
    if a in [3, 5]:
        out.add((1, 1, -(a-1), -1, -(a-1)))
    return out


def regression():
    rows = []
    checked = 0
    for a in range(3, 62, 2):
        expected = classified_resonances(a)
        actual = set()
        for eps, j, p, u, v in product([-1, 1], range(1, 2*a+1),
                                       [s*d for d in divisors(a-1) for s in [-1, 1]],
                                       range(-4, 2), range(-4, 2)):
            E = a*u-p
            # Two distinct scale values characterize vanishing of this affine residual.
            r1 = E*((j+1)*v-eps)-a*(j+1)+1
            r2 = E*((2*j+1)*v-2*eps)-a*(2*j+1)+1
            checked += 1
            if r1 == r2 == 0:
                actual.add((eps, j, p, u, v))
                for s in [1, 2, 17, 101]:
                    assert E*((j*s+1)*v-eps*s) == a*(j*s+1)-1
        assert actual == expected, (a, actual ^ expected)
        triangle = {row for row in actual if -4 <= (a-1)//row[2]+row[0]*row[1] <= 1}
        triangle_expected = {(-1, a-1, 1, 1, 1), (1, a-1, -1, -1, -1)}
        if a == 3:
            triangle_expected.add((-1, 2, -2, 0, 1))
        if a in [3, 5]:
            triangle_expected.add((1, 1, -(a-1), -1, -(a-1)))
        assert triangle == triangle_expected, (a, triangle ^ triangle_expected)
        rows.append({'a': a, 'all_resonances': sorted(actual), 'classification_matches': True,
                     'resonances_after_low_edge_node': sorted(triangle),
                     'full_triangle_classification_matches': True})
    return {'a_range': [3, 61], 'odd_a_count': len(rows), 'j_range_at_each_a': '1..2*a',
            'all_signed_divisors_of_a_minus_1': True, 'all_36_node_pairs': True,
            'tested_parameter_tuples': checked, 'rows': rows,
            'role': 'Bounded regression against the original pair equation; not the unbounded proof.'}


def fixed_candidates(a, p, j, eps):
    out, resonances = [], []
    for u, v in product(range(-4, 2), repeat=2):
        E = a*u-p
        D, N = E*(j*v-eps)-a*j, a-1-E*v
        if D == 0:
            if N == 0:
                resonances.append([u, v])
            continue
        if N % D == 0 and N//D > 0:
            s = N//D
            assert E*((j*s+1)*v-eps*s) == a*(j*s+1)-1
            q = j*s+1
            assert q*D == -eps*E-j != 0
            assert (-eps*E-j) % q == 0
            if (a-1) % p == 0 and -4 <= (a-1)//p+eps*j <= 1:
                assert q <= 6*a+2
            out.append({'u': u, 'v': v, 'scale': s})
    return {'a': a, 'p': p, 'j': j, 'epsilon': eps,
            'all_positive_integer_single_pair_candidates': out, 'resonant_node_pairs': resonances}


def run():
    here = Path(__file__).resolve().parent
    proof_name = 'outer_core_linear_transfer_v23.tex'
    proof = next(p for p in [here/proof_name, here.parent/'papers/sections/paper'/proof_name] if p.is_file())
    examples = [fixed_candidates(*data) for data in [
        (7, -2, 1, -1), (31, 6, 4, -1), (9, 2, 4, -1),
        (7, -1, 6, 1), (5, -4, 1, 1), (7, 3, 3, 1)]]
    return {'version': 'v23', 'status': 'PASS', 'coefficient_checks': coefficients(),
            'resonance_classification_regression': regression(), 'exact_fixtures': examples,
            'node_range': [-4, 1], 'node_pairs_per_fixed_input': 36,
            'single_pair_condition_only': True,
            'unbounded_classification_in_proof': True,
            'global_existence_claim': False, 'proof_assistant_formalization': False,
            'proof_file': proof_name, 'proof_sha256': sha256(proof.read_bytes()).hexdigest(),
            'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('outer_core_transfer_verification_v23.json'))
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'coefficient_identities': len(result['coefficient_checks']),
                      'regression_tuples': result['resonance_classification_regression']['tested_parameter_tuples'],
                      'exact_fixtures': len(result['exact_fixtures'])}))
