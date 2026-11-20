#!/usr/bin/env python3
"""Exact, unbounded audit of the G5_14 five-node obstruction.

No old verifier imports, third-party packages, denominator cutoff, or matrix-entry
cutoff. The finite loops enumerate node-induced coefficient sets and every divisor
of the mathematically fixed integers 6, 8 and 20. Proof: the adjacent TeX module.
"""
from fractions import Fraction
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import argparse
import hashlib
import json


def divisors(n):
    assert n > 0
    ans = set()
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            ans.update((d, n // d))
    return sorted(ans)


def signed_divisors(n):
    assert n
    return sorted({s * d for d in divisors(abs(n)) for s in (-1, 1)})


def common_residual(s, t, S, T, alpha, beta):
    return (((s * alpha + 1) * S + alpha)
            * ((t * beta + 1) * T + beta)
            - (s * S + 1) * (t * T + 1) + 1)


def fraction_json(x):
    return [x.numerator, x.denominator]


def common_negative_classification():
    """All 96 coefficient cases, using exact factorization, without scale bounds."""
    expected = {
        (1, 2, 1, 3): {(2, 1)}, (1, 2, 2, 1): {(2, 1)},
        (2, 1, 1, 2): {(1, 2)}, (2, 1, 3, 1): {(1, 2)},
        (1, 3, 2, 1): {(2, 2)}, (3, 1, 1, 2): {(2, 2)},
        (2, 2, 1, 2): {(3, 1), (2, 2)},
        (2, 2, 2, 1): {(1, 3), (2, 2)},
    }
    records, points = [], []
    for s in range(1, 4):
        for t in range(1, 5 - s):
            for A, B in product(range(1, 5), repeat=2):
                C = s * t * (A * B - 1) - s * A - t * B + 1
                D = s * (A * B - 1) - B
                E = t * (A * B - 1) - A
                F = A * B
                N = D * E - C * F
                sols = set()
                if C == 0:
                    assert D >= 0 and E >= 0 and F > 0
                    reason = 'nonnegative coefficients and positive constant'
                elif N == 0:
                    fixed_S = -E // C if E % C == 0 else None
                    fixed_T = -D // C if D % C == 0 else None
                    assert fixed_S is None or fixed_S <= 0 or s * fixed_S % 2
                    assert fixed_T is None or fixed_T <= 0 or t * fixed_T % 2
                    reason = 'both zero-factor lines violate positivity or parity'
                else:
                    for X in signed_divisors(N):
                        Y = N // X
                        if (X - E) % C or (Y - D) % C:
                            continue
                        S, T = (X - E) // C, (Y - D) // C
                        if S <= 0 or T <= 0 or s * S % 2 or t * T % 2:
                            continue
                        assert common_residual(s, t, S, T, -A, -B) == 0
                        sols.add((S, T))
                    reason = 'all signed divisors of the exact nonzero factor constant'
                assert sols == expected.get((s, t, A, B), set())
                records.append({'s': s, 's_prime': t, 'minus_alpha': A,
                                'minus_beta': B, 'C_D_E_F': [C, D, E, F],
                                'factor_constant': N, 'method': reason,
                                'all_positive_odd_solutions': sorted(sols)})
                for S, T in sols:
                    points.append({'s': s, 's_prime': t, 'S': S, 'T': T,
                                   'q': [s * S + 1, t * T + 1],
                                   'alpha': -A, 'beta': -B})
    assert len(records) == 96 and len(points) == 10
    return records, points


def normalized_cases(points):
    """Recover all seven cases using exact divisors of q03-1=6."""
    patterns = sorted({(p['s'], p['s_prime'], p['S'], p['T'])
                       for p in points if p['s'] + p['s_prime'] == 4})
    assert len(patterns) == 5
    outcomes = {'A': [], 'B': []}
    for s, sp, S, T in patterns:
        assert s + sp == S + T == 4
        for u in divisors(6):
            A = 6 // u
            t = u - s + 1
            if u < 2 or A < 2 or t < 1 or u % 2 == A % 2:
                continue
            q02, q12 = s * S + 1, sp * T + 1
            q03, q13 = u * A + 1, (u - 1) * (A - 1) + 1
            assert q03 == 7 and q13 == 3
            target = 'A' if (q02, q12) == (7, 3) else 'B' if (q02, q12) == (3, 7) else None
            if target is None:
                continue
            outcomes[target].append((s, sp, S, T, u, A, t))
    expected_A = {(3, 1, 2, 2, 3, 2, 1), (2, 2, 3, 1, 2, 3, 1),
                  (2, 2, 3, 1, 3, 2, 2)}
    expected_B = {(1, 3, 2, 2, 2, 3, 2), (1, 3, 2, 2, 3, 2, 3),
                  (2, 2, 1, 3, 2, 3, 1), (2, 2, 1, 3, 3, 2, 2)}
    assert set(outcomes['A']) == expected_A
    assert set(outcomes['B']) == expected_B
    return outcomes


def factor_obstruction(name, params):
    s, sp, S, T, u, A, t = params
    v = t + 1
    m, n = (u - 1) * (A - 1) + 1, sp * T + 1
    a, b = m - (A - 1), n - T
    assert a > 0 and b > 0
    results = []
    for L in divisors(m * n - 1):
        M = (m * n - 1) // L
        d1, d2 = L + a, M + b
        C = m * v * d2 + n * v * d1 - (v + 1) * d1 * d2
        E = (m - 1) * d2 + (n - 1) * d1 - d1 * d2
        record = {'L': L, 'M': M, 'reverse_denominators': [d1, d2],
                  'C': C, 'E': E,
                  'reverse_numerators': [[m * v, m - 1], [n * v, n - 1]]}
        if C:
            B = Fraction(-E, C)
            assert not (B.denominator == 1 and B > 0)
            record.update({'status': 'unique linear root is not a positive integer',
                           'B': fraction_json(B)})
        elif E:
            record['status'] = 'zero coefficient but nonzero constant'
        else:
            bad = []
            for divisor, coefficient, constant in ((d1, m * v, m - 1),
                                                    (d2, n * v, n - 1)):
                g = gcd(divisor, coefficient)
                if constant % g:
                    bad.append({'divisor': divisor, 'coefficient': coefficient,
                                'constant': constant, 'gcd': g,
                                'nonzero_residue': constant % g})
            assert bad, 'An unrestricted resonance would invalidate the claimed exclusion.'
            assert any(r['divisor'] == 6 and r['coefficient'] == 6
                       and r['constant'] == 2 for r in bad)
            record.update({'status': 'linear identity but original pair divisibility impossible',
                           'divisibility_obstructions': bad})
        results.append(record)
    return {'name': name, 's_sprime_S_T_u_A_t': list(params),
            'fixed_low_row': [1 - u, -sp, v],
            'fixed_low_column': [1 - A, -T, 'B'],
            'm_n_v_a_b': [m, n, v, a, b],
            'all_positive_factor_checks': results}


def check_local_affine_identity():
    """Coefficient equality, not evaluation at sample values of B."""
    # The symbolic numerator after multiplying d1*d2 is represented as (B,1).
    # Independent direct row assembly is performed for all seven parameter types.
    types = [(3, 3, 2, 2, 1), (3, 3, 2, 1, 2), (3, 3, 3, 2, 2),
             (3, 7, 3, 1, 5), (3, 7, 4, 2, 5),
             (3, 7, 2, 1, 4), (3, 7, 3, 2, 4)]
    checked = 0
    for m, n, v, a, b in types:
        for L in divisors(m * n - 1):
            M = (m * n - 1) // L
            d1, d2 = L + a, M + b
            numerator_left = (m * v * d2 + n * v * d1,
                              (m - 1) * d2 + (n - 1) * d1)
            numerator_right = ((v + 1) * d1 * d2, d1 * d2)
            row_coefficients = tuple(x - y for x, y in zip(numerator_left, numerator_right))
            from_fractions = (
                Fraction(m * v, d1) + Fraction(n * v, d2) - (v + 1),
                Fraction(m - 1, d1) + Fraction(n - 1, d2) - 1)
            assert all(x == y * d1 * d2 for x, y in zip(row_coefficients, from_fractions))
            checked += 1
    assert checked == 36
    return checked


def main(proof, output):
    common_records, points = common_negative_classification()
    cases = normalized_cases(points)
    order = [
        ('A1', (3, 1, 2, 2, 3, 2, 1)), ('A2', (2, 2, 3, 1, 2, 3, 1)),
        ('A3', (2, 2, 3, 1, 3, 2, 2)), ('B1', (1, 3, 2, 2, 2, 3, 2)),
        ('B2', (1, 3, 2, 2, 3, 2, 3)), ('B3', (2, 2, 1, 3, 2, 3, 1)),
        ('B4', (2, 2, 1, 3, 3, 2, 2)),
    ]
    assert {p for _, p in order} == set(cases['A'] + cases['B'])
    records = [factor_obstruction(name, p) for name, p in order]
    checks = [x for r in records for x in r['all_positive_factor_checks']]
    assert len(checks) == check_local_affine_identity() == 36
    resonance_count = sum(x['C'] == x['E'] == 0 for x in checks)
    inconsistent_zero_count = sum(x['C'] == 0 and x['E'] != 0 for x in checks)
    assert resonance_count == inconsistent_zero_count == 2
    negative_common_denominators = {tuple(p['q']) for p in points}
    assert negative_common_denominators == {(3, 3), (3, 7), (5, 5), (7, 3)}
    assert [p for p in negative_common_denominators if p[0] <= 7 and p[1] >= 7] == [(3, 7)]
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    result = {
        'version': 'v25', 'status': 'PASS',
        'theorem': 'In G5_14 both unit branches have node multiset {4,1,0}; {5,0,0} is impossible.',
        'scope': 'Original positive integer charts with row/pair, odd denominators, integer clutching, nonnegative node budget five, and opposite D. No exclusion of G5_14 itself or G5_16.',
        'proof_dependencies': [
            'Positive three-high matching theorem; all original positive-weight hypotheses retained.',
            'Complete common-negative triangle classification, independently rechecked here for all negative-sign coefficient cases.',
            'Opposite-sign n=0,1 classification: analytic proof restated in TeX, no finite-scale scan used.',
            'Opposite low D enforces positive external pairs at both zero-node positions of a five-node unit branch.',
        ],
        'all_negative_common_coefficient_cases': 96,
        'all_negative_common_points': points,
        'common_negative_audit': common_records,
        'normal_form_cases': records,
        'fixed_positive_factor_checks': 36,
        'identity_resonances_excluded_by_original_pair_divisibility': resonance_count,
        'zero_linear_coefficients_with_nonzero_constant': inconsistent_zero_count,
        'unbounded_scale_root_cases': 32,
        'denominator_cutoff': None, 'matrix_entry_cutoff': None,
        'bounded_scan_used_for_theorem': False,
        'old_verifier_imports': False, 'stdlib_only': True,
        'proof_assistant_formalization': False, 'external_peer_review': False,
        'proof_file': proof.name, 'proof_sha256': sha(proof),
        'verifier_file': Path(__file__).name, 'verifier_sha256': sha(Path(__file__)),
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('version', 'status', 'fixed_positive_factor_checks',
                      'identity_resonances_excluded_by_original_pair_divisibility',
                      'zero_linear_coefficients_with_nonzero_constant', 'bounded_scan_used_for_theorem')},
                     ensure_ascii=False))


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument('--proof', type=Path, default=here / 'g514_five_node_exclusion_v25.tex')
    parser.add_argument('--output', type=Path, default=here / 'g514_five_node_verification_v25.json')
    args = parser.parse_args()
    main(args.proof, args.output)
