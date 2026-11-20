#!/usr/bin/env python3
"""Complete coefficient sets for fixed n=3,5,7,13, with no partner bound.

Uses the previously proved complete divisor factorization, including every
nonresonant branch and both resonances. This is exact finite arithmetic, not
numerator- or partner-denominator-bounded search. It does not test geometric
clutching or assert realizability of any globally compatible atlas.
"""

from pathlib import Path
import hashlib
import importlib.util
import itertools
import json


HERE = Path(__file__).resolve().parent
DEPENDENCY = 'verify_fixed_denominator_partners_v12.py'
for candidate in (
    HERE / DEPENDENCY,
    HERE.parents[1] / 'deliverables/general_type_surface_fibration_v12/verification' / DEPENDENCY,
):
    if candidate.exists():
        spec = importlib.util.spec_from_file_location('fixed_partner_v12', candidate)
        fp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fp)
        DEPENDENCY_PATH = candidate
        break
else:
    raise FileNotFoundError(DEPENDENCY)


FINITE_SETS = {
    3: {3, 6},
    5: {6, 11, 18, 21},
    7: {-7, 0, 3, 7, 9, 16, 21, 23, 44},
    13: {-15, -13, -7, -6, -3, -2, 0, 13, 14, 15, 18, 22, 23,
         26, 27, 28, 31, 41, 44, 52, 57, 58, 80, 83, 92, 161},
}
EXPECTED_COUNTS = {3: 2, 5: 4, 7: 13, 13: 28}
EXPECTED_INTERSECTIONS = {3: set(), 5: set(), 7: {-7, 0, 7},
                          13: {-15, -13, 0, 13, 15}}
EXPECTED_MATCHES = {
    3: set(), 5: set(),
    7: {(3, 13, 7), (3, 19, 7), (7, 7, 0)},
    13: {(5, 25, 15), (7, 21, 13), (13, 13, 0),
         (13, 17, 0), (17, 17, 0)},
}


def coefficient(m):
    return m['D'][0 if m['fixed_side'] == 'A' else 1]


def other_denominator(m):
    return m['b'] if m['fixed_side'] == 'A' else m['a']


def in_resonance(n, d):
    if n not in (7, 13):
        return False
    offset = 9 if n == 7 else 14
    return (d + offset) % n == 0 and (d + offset) // n >= 1


def main():
    catalogs = {n: fp.partners_for_fixed(n) for n in FINITE_SETS}
    summaries = {}
    for n, result in catalogs.items():
        models = result['nonresonant_models']
        assert len(models) == EXPECTED_COUNTS[n]
        assert {coefficient(m) for m in models} == FINITE_SETS[n]
        assert len(result['resonances']) == (1 if n in (7, 13) else 0)

        # Every negative coefficient is captured without truncating k: the
        # resonance sequences are increasing with k, and only k=1 is negative.
        negative = {d for d in FINITE_SETS[n] if d < 0}
        if n in (7, 13):
            negative.add(n - (9 if n == 7 else 14))
            assert 2*n - (9 if n == 7 else 14) > 0
        matching_positive = {d for d in (-e for e in negative)
                             if d in FINITE_SETS[n] or in_resonance(n, d)}
        intersection = matching_positive | {-d for d in matching_positive}
        if 0 in FINITE_SETS[n] or in_resonance(n, 0):
            intersection.add(0)
        assert intersection == EXPECTED_INTERSECTIONS[n]
        assert not any(in_resonance(n, d) for d in intersection)

        matching_models = [m for m in models if coefficient(m) in intersection]
        pairs = set()
        for left, right in itertools.product(matching_models, repeat=2):
            d = coefficient(left)
            if d + coefficient(right) == 0:
                u, v = sorted((other_denominator(left), other_denominator(right)))
                pairs.add((u, v, abs(d)))
        assert pairs == EXPECTED_MATCHES[n]
        summaries[n] = {
            'finite_nonresonant_coefficient_set': sorted(FINITE_SETS[n]),
            'nonresonant_model_count': len(models),
            'all_negative_coefficients': sorted(negative),
            'coefficient_set_intersection_with_its_negative': sorted(intersection),
            'necessary_neighbor_pairs_and_absolute_D': [list(p) for p in sorted(pairs)],
            'matching_models': matching_models,
            'resonance_coefficients': None if n not in (7, 13) else {
                'expression': '7*k-9' if n == 7 else '13*k-14',
                'parameter': 'every integer k>=1',
                'no_value_matches_an_opposite_local_coefficient': True,
            },
        }

    k = fp.Poly.variable('k')
    polynomial_checks = []
    for n, a, r, s, z, S, T, expected in [
        (7, 6*k+1, 2, 2*k, 1, 3, 6, 7*k-9),
        (13, 12*k+1, 3, 3*k, 2, 4, 6, 13*k-14),
    ]:
        x = 3*k if n == 7 else 4*k
        A = a + x - s
        DB = -n + A + r + 1 - T
        assert DB == expected
        polynomial_checks.append(f'fixed {n} resonance D_B identity')

    source_name = 'small_denominator_propagation_v13.tex'
    source = next((p for p in (HERE/source_name, HERE.parent/'paper'/source_name)
                   if p.exists()), None)
    result = {
        'status': 'passed',
        'scope': ('Complete fixed-denominator arithmetic for n=3,5,7,13. '
                  'No bound on partner denominators or numerators. '
                  'All resonances handled symbolically. Necessary local '
                  'D-matching data, not sufficient global clutching conditions.'),
        'dependency': {'file': DEPENDENCY_PATH.name,
                       'sha256': hashlib.sha256(DEPENDENCY_PATH.read_bytes()).hexdigest()},
        'source': None if source is None else {'file': source.name,
                  'sha256': hashlib.sha256(source.read_bytes()).hexdigest()},
        'fixed_denominator_count': 4,
        'nonresonant_model_count': sum(EXPECTED_COUNTS.values()),
        'resonance_count': 2,
        'polynomial_checks': polynomial_checks,
        'summaries': summaries,
        'complete_divisor_catalogs': catalogs,
    }
    target = HERE / 'small_denominator_propagation_verification_v13.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'finite_models': 47,
                      'resonances': 2, 'output': str(target)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
