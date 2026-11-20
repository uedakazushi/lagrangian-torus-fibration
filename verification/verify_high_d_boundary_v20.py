#!/usr/bin/env python3
"""Exact coefficient verification for the v20 high-D boundary reduction.

All general identities are checked in a sparse rational polynomial ring.
The verification does not enumerate denominators or infer a general theorem
from finite substitutions.  Matrix examples are separate regression checks.
Python 3.9+, standard library only.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import json

NAMES = ('s', 't', 'b', 'd', 'a', 'k', 'S', 'T', 'U')
N = len(NAMES)


class Poly:
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {k: Fraction(v) for k, v in value.items() if v}
        else:
            self.terms = {(0,) * N: Fraction(value)} if value else {}

    def __add__(self, other):
        other = Poly(other)
        result = defaultdict(Fraction, self.terms)
        for key, value in other.terms.items():
            result[key] += value
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        other = Poly(other)
        result = defaultdict(Fraction)
        for key, value in self.terms.items():
            for key2, value2 in other.terms.items():
                result[tuple(a + b for a, b in zip(key, key2))] += value * value2
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert type(exponent) is int and exponent >= 0
        result = Poly(1)
        for _ in range(exponent):
            result = result * self
        return result


variables = {name: Poly({tuple(int(i == j) for j in range(N)): 1})
             for i, name in enumerate(NAMES)}
s, t, b, d, a, k, SS, TT, UU = (variables[name] for name in NAMES)
identities = []


def zero(name, polynomial):
    assert not Poly(polynomial).terms, name
    identities.append(name)


def determinant(matrix):
    size = len(matrix)
    result = Poly()
    for order in permutations(range(size)):
        inversions = sum(order[i] > order[j]
                         for i in range(size) for j in range(i + 1, size))
        term = Poly((-1) ** inversions)
        for i, j in enumerate(order):
            term *= matrix[i][j]
        result += term
    return result


def linear_data(sv, tv, av, bv, kv):
    uv = sv + tv - 1
    avar, bvar, cvar = sv * av - tv, -sv - tv * bv, sv + uv * kv
    matrix = [[bvar, avar, Poly(0)],
              [-cvar, Poly(0), avar + 1],
              [Poly(0), cvar - 1, bvar + 1]]
    rhs = [av * bv, kv * (av + 1), (bv - 1) * (kv + 1)]
    delta = determinant(matrix)
    numerators = [determinant([[rhs[i] if col == index else matrix[i][col]
                               for col in range(3)] for i in range(3)])
                  for index in range(3)]
    return delta, numerators


u = s + t - 1
m = b * b - b + 1
K = s * s + s * t + t * t - s - t
r = [-s, -t, u]
B0 = [[Poly(1), b - 1, -b],
      [-b, Poly(1), b - 1],
      [b - 1, -b, Poly(1)]]
Br = [sum((B0[i][j] * r[j] for j in range(3)), Poly()) for i in range(3)]
for i in range(3):
    zero('cyclic_row_sum_' + str(i), sum(B0[i], Poly()))
    zero('cyclic_column_sum_' + str(i), sum((B0[j][i] for j in range(3)), Poly()))
    for j in range(3):
        inner = sum((B0[z][i] * B0[z][j] for z in range(3)), Poly())
        zero('cyclic_gram_' + str(i) + str(j), inner - m * (3 * int(i == j) - 1))
zero('low_row_sum', sum(r, Poly()) + 1)
zero('low_row_norm', sum((x * x for x in r), Poly()) - (2 * K + 1))
zero('cyclic_norm', sum((x * x for x in Br), Poly()) - m * (6 * K + 2))
zero('norm_remainder_mod_K', m * (6 * K + 2) - m * (6 * m - 4) - 6 * m * (K - m + 1))

delta, (ns, nt, nu) = linear_data(s, t, b - 1, b, b - 1)
zero('zero_D_determinant', delta - m * K)
zero('zero_D_Cramer_S', ns - (m - 1) * (m * s + Br[0]))
zero('zero_D_Cramer_T', nt - (m - 1) * (m * t + Br[1]))
zero('zero_D_Cramer_U', nu - (m - 1) * (m * u - Br[2]))
zero('zero_D_Cramer_sum', nu + delta - ns - nt - m * (K - m + 1))

# The general three pair products independently recover the linear rows.
qa, qb, qc = 1 + s * SS, 1 + t * TT, 1 + u * UU
A0, Bscalar, C0 = s * a - t, -s - t * b, s + u * k
Hab, Kba = t * SS + a, s * TT - b
Lac, Mca = u * SS + a + 1, s * UU - k
Nbc, Ocb = u * TT - b + 1, t * UU + k + 1
zero('pair_ab_to_linear_row', Hab * Kba - qa * qb + 1 - (Bscalar * SS + A0 * TT - a * b))
zero('pair_ac_to_linear_row', Lac * Mca - qa * qc + 1 - (-C0 * SS + (A0 + 1) * UU - k * (a + 1)))
zero('pair_bc_to_linear_row', Nbc * Ocb - qb * qc + 1 - ((C0 - 1) * TT + (Bscalar + 1) * UU - (b - 1) * (k + 1)))

# k=b-1, s=1: the third original row is already contradictory.
Cfirst, Bfirst = 1 + t * (b - 1), -1 - t * b
Rfirst = (Cfirst - 1) * TT + (Bfirst + 1) * UU - b * (b - 1)
zero('boundary_k_bminusone_third_row', Rfirst - (t * (b - 1) * TT - t * b * UU - b * (b - 1)))
zero('boundary_k_bminusone_negative_after_U_substitution',
     (Cfirst - 1) * TT + (Bfirst + 1) * (SS + TT + d - 1) - b * (b - 1)
     + t * (b * SS + TT + b * (d - 1)) + b * (b - 1))

# k=b, s=1: again the third original row alone suffices.
Cnext, Bnext = 1 + t * b, -1 - t * b
zero('boundary_k_b_s1_third_row',
     (Cnext - 1) * TT + (Bnext + 1) * UU - (b - 1) * (b + 1)
     - (t * b * (TT - UU) - (b * b - 1)))
zero('boundary_k_b_s1_negative_after_U_substitution',
     (Cnext - 1) * TT + (Bnext + 1) * (SS + TT + d - 1) - (b - 1) * (b + 1)
     + t * b * (SS + d - 1) + b * b - 1)

# k=b, s=2, d=1, alpha=b+t, U=S+T.
Abound, Bbound, Cbound = 2 * (b + t) - t, -2 - t * b, 2 + (t + 1) * b
Efirst = -(2 + t * b) * SS + (2 * b + t) * TT - b * (b + t)
Ethird = b * TT - (1 + t * b) * SS - (b * b - 1)
zero('boundary_k_b_s2_first_row', Bbound * SS + Abound * TT - b * (b + t) - Efirst)
zero('boundary_k_b_s2_third_row',
     (Cbound - 1) * TT + (Bbound + 1) * (SS + TT) - (b - 1) * (b + 1) - Ethird)
positive_residual = t * (1 + b * b + t * b) * SS - (t + 2 * b - b ** 3)
zero('boundary_k_b_s2_row_combination', b * Efirst - (2 * b + t) * Ethird - positive_residual)
zero('boundary_k_b_s2_positive_residual',
     positive_residual - (t * (1 + b * b + t * b) * (SS - 1) + t * b * b + t * t * b + b ** 3 - 2 * b))
zero('boundary_k_b_s2_positive_gap_coefficients',
     b ** 3 - 2 * b - ((b - 2) ** 3 + 6 * (b - 2) ** 2 + 10 * (b - 2) + 4))

A, bb, C = s * a - t, s + t * b, s + u * k
delta, _ = linear_data(s, t, a, b, k)
zero('general_determinant', delta - (C * (A + bb) - bb * (A + 1)))
zero('positive_determinant_remainder', delta - bb * (bb - 1) - (C - bb) * (A + bb))
zero('C_minus_bb_nonnegative_coefficients', C - bb - ((s - 1) * b + u * (k - b)))
Da, Db, Dc = s * d + b - k - 1, t * d - a + k, a - b + 1 - u * d
zero('high_D_sum', Da + Db + Dc - d)
zero('k_lower_bound_from_Da', k - ((s - 1) * d + b - 1) - (d - Da))
zero('alpha_minus_k_bound', a - k - (t - 1) * d - Da - Dc)


def check_example(parameters, scales):
    sv, tv, av, bv, kv = parameters
    Sv, Tv, Uv = map(Fraction, scales)
    uv = sv + tv - 1
    q = [1 + sv * Sv, 1 + tv * Tv, 1 + uv * Uv, Fraction(1)]
    P = [[0, tv * Sv + av, -(uv * Sv + av + 1), -Sv],
         [sv * Tv - bv, 0, -(uv * Tv - bv + 1), -Tv],
         [-(sv * Uv - kv), -(tv * Uv + kv + 1), 0, Uv],
         [-sv, -tv, uv, 0]]
    P = [list(map(Fraction, row)) for row in P]
    assert all(sum(P[i]) == -q[i] for i in range(4))
    assert all(P[i][j] * P[j][i] == q[i] * q[j] - 1
               for i, j in combinations(range(4), 2))
    DD = [-q[i] - sum(P[j][i] for j in range(4) if j != i) for i in range(4)]
    weights = [q[0], P[0][1] + 1 / (2 * P[1][0]), uv + 1 / (2 * Uv), Fraction(1)]
    gaps = [weights[j] - P[i][j] * weights[i] / q[i]
            for i in range(4) for j in range(4) if i != j]
    assert all(value > 0 for value in gaps)
    return {'parameters_s_t_alpha_minusbeta_k': list(parameters),
            'scales': [str(value) for value in scales],
            'q': [str(value) for value in q], 'P': [[str(value) for value in row] for row in P],
            'D': [str(value) for value in DD], 'weights': [str(value) for value in weights],
            'positive_basin_gaps': [str(value) for value in gaps]}


integer_example = check_example((1, 2, 10, 2, 5), (4, 5, 11))
assert integer_example['D'] == ['-1', '1', '3', '-3']
rational_zero_example = check_example((3, 4, 5, 6, 5),
                                      (Fraction(34, 31), Fraction(168, 31), Fraction(171, 31)))
assert rational_zero_example['D'] == ['0', '0', '0', '0']
known_singular_example = check_example((3, 12, 12, 4, 1), (136, 291, 93))
assert known_singular_example['D'] == ['-997', '-4007', '4671', '333']

script = Path(__file__).resolve()
proof_candidates = [script.with_name('high_d_nonsingular_reduction_v20.tex'),
                    script.parent.parent/'paper/high_d_nonsingular_reduction_v20.tex']
proof = next(path for path in proof_candidates if path.is_file())
report = {
    'version': 'v20', 'status': 'PASS',
    'method': 'Sparse rational polynomial coefficient identities; exact rational matrix regressions separately recorded.',
    'polynomial_identities': len(identities), 'identity_names': identities,
    'identity_groups': {
        'cyclic_row_column_and_Gram_identities': 15,
        'low_row_and_norm_identities': 4,
        'zero_D_Cramer_identities': 5,
        'general_pair_products_to_linear_rows': 3,
        'k_bminusone_boundary': 2,
        'k_b_s1_boundary': 2,
        'k_b_s2_boundary': 5,
        'general_positive_determinant': 3,
        'high_D_sum_and_parameter_bounds': 3
    },
    'script_sha256': sha256(script.read_bytes()).hexdigest(),
    'proof_sha256': sha256(proof.read_bytes()).hexdigest(),
    'proof_file': proof.name,
    'conclusions': {
        'zero_D_vector_excluded_for_all_positive_integer_three_high_models': True,
        'k_equals_minus_beta_minus_one_or_minus_beta_excluded_under_high_D_nonnegativity': True,
        'all_nonnegative_high_D_requires': ['b=-beta>=2', 'd>=1', 'alpha>=k>=b+1', 'Delta>=(-B)(-B-1)>0'],
        'all_singular_Schur_systems_excluded_from_high_D_nonnegative_candidates': True,
        'general_nonsingular_high_D_nonnegativity_status': 'OPEN',
        'arbitrary_denominator_cutoff': None,
        'odd_denominator_assumption_used': False,
        'clutching_or_node_assumptions_used': False
    },
    'regressions': {'integer_model_in_remaining_sector': integer_example,
                    'rational_zero_D_model_not_an_integer_chart': rational_zero_example,
                    'known_singular_family_n0': known_singular_example},
    'external_peer_review': False, 'proof_assistant_formalization': False
}
output = script.with_name('high_d_boundary_verification_v20.json')
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': report['status'], 'polynomial_identities': len(identities),
                  'exact_matrix_regressions': 3, 'output': str(output)}, ensure_ascii=False))
