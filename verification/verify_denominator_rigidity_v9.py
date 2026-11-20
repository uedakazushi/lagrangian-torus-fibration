#!/usr/bin/env python3
"""Exact certificates for paired four-puncture denominators and mixed quintic.

Only Python's standard library is used. Symbolic coefficient comparison proves
the recorded polynomial identities, not the geometric hypotheses that produce
them. No bounded-denominator search is used for a universal conclusion.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


class Poly:
    """Integer polynomials; monomials are sorted tuples of variable names."""

    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @classmethod
    def variable(cls, name):
        return cls({(name,): 1})

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls({(): int(value)})

    def __add__(self, other):
        result = self.terms.copy()
        for monomial, coefficient in self.coerce(other).terms.items():
            result[monomial] = result.get(monomial, 0) + coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        result = {}
        for m, c in self.terms.items():
            for n, d in self.coerce(other).terms.items():
                monomial = tuple(sorted(m + n))
                result[monomial] = result.get(monomial, 0) + c * d
        return Poly(result)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms


checks = 0
certificates = []


def check(name, condition):
    global checks
    assert condition, name
    checks += 1
    certificates.append(name)


def V(name):
    return Poly.variable(name)


qa, qb = V('q_A'), V('q_B')
ei, ej, mi, mj = map(V, ['e_i', 'e_j', 'm_i', 'm_j'])
pa, pb, ppa, ppb, n = map(V, ['P_A', 'P_B', 'Pprime_A', 'Pprime_B', 'N_ext'])
d = qa * qb

# The positive determinant is minus the oriented determinant of the two
# primitive action columns in the (normal, first annular cycle) basis.
matrix_determinant = (-qa) * (ei * qb + pb) - (-qb) * (-pa)
positive_determinant = ei * d + qb * pa + qa * pb
check('oriented_annular_determinant', matrix_determinant == -positive_determinant)

left_annulus = positive_determinant - mi
right_annulus = ej * d + qb * ppa + qa * ppb - mj
summed_puncture_clutching = d * n - 4 * d + qb * (pa + ppa) + qa * (pb + ppb)
rigidity_certificate = d * (4 + ei + ej - n) - mi - mj
check('paired_annulus_polynomial_certificate',
      left_annulus + right_annulus - summed_puncture_clutching == rigidity_certificate)

# The same identity needs only integer clutching k_l, not positivity of n_l.
k = V('K_sum')
summed_integer_clutching = qb * (pa + ppa) + qa * (pb + ppb) + d * k
general_integer_certificate = d * (ei + ej - k) - mi - mj
check('integer_clutching_only_certificate',
      left_annulus + right_annulus - summed_integer_clutching == general_integer_certificate)

# For even q every unit numerator is odd. All choices of arm orientations
# still produce an odd sum. This is the complete calculation over Z/2.
for signs in product([-1, 1], repeat=3):
    check('three_unit_arm_parity_' + '_'.join(map(str, signs)), sum(signs) % 2 == 1)

# Under two unimodular cones the positive integer product divides 2.
positive_divisors_of_two = [1, 2]
odd_divisors = [q for q in positive_divisors_of_two if q % 2]
check('only_odd_positive_divisor_of_two', odd_divisors == [1])
check('positive_product_one_has_two_unit_factors',
      [(a, b) for a in [1] for b in [1] if a * b == 1] == [(1, 1)])

# Mixed plane: both line denominators remain arbitrary. Their slope sums
# are -q_line and cancel identically in the total branch coefficient.
qx, qy, p = map(V, ['q_X', 'q_Y', 'P_A_free'])
line_contribution = -qx - (-qx)
mixed_plane_sum = -qx - qy - 4 - ((-qx) + (-qy) + p + (-3 - p))
quadric_component_sum = -2 - (p + (-1 - p))
check('line_contribution_arbitrary_denominator', line_contribution == 0)
check('mixed_plane_minus_one_with_arbitrary_line_denominators', mixed_plane_sum == -1)
check('quadric_component_minus_one', quadric_component_sum == -1)
check('mixed_global_minus_six', 3 * mixed_plane_sum + 3 * quadric_component_sum == -6)

node_budgets = []
for name, e_left, e_right, total_nodes, expected_external in [
    ('mixed_plane_quadric', 4, 2, 10, 8),
    ('all_plane_sextic', 1, 1, 6, 4),
]:
    external = 4 + e_left + e_right - 2
    internal = total_nodes - external
    check(name + '_external_budget', external == expected_external)
    check(name + '_internal_budget', internal == 2)
    node_budgets.append({
        'model': name, 'e_left': e_left, 'e_right': e_right,
        'total_meridian_nodes': total_nodes, 'external_nodes': external,
        'internal_annulus_nodes': internal,
        'qualification': (
            'Necessary allocation under hypothetical gluing; the mixed global atlas is obstructed.'
            if name == 'mixed_plane_quadric' else
            'Necessary allocation for the stated sextic construction; a global denominator-one atlas has been constructed.'
        )
    })

# A local annular arithmetic pair at denominators 1 and 3 is not globally
# compatible with four integer puncture clutchings.
q_a, q_b = 1, 3
p_a, p_b, pp_a, pp_b = -1, -8, 0, -5
check('local_euler_four_annulus_candidate', 4*q_a*q_b + q_b*p_a + q_a*p_b == 1)
check('local_euler_two_annulus_candidate', 2*q_a*q_b + q_b*pp_a + q_a*pp_b == 1)
external = 4 - Fraction(p_a + pp_a, q_a) - Fraction(p_b + pp_b, q_b)
check('local_candidate_fractional_external_budget', external == Fraction(28, 3))
check('local_candidate_no_integer_clutching', external.denominator != 1)
check('local_candidate_positive_plane_defect', -2*(q_a+q_b)-(p_a+p_b) == 1)

# Nonunimodular cone indices change the divisibility condition. This arithmetic
# fact is not an assertion that such cones arise in the geometric construction.
check('cone_index_scope_example', Fraction(1 + 2, 1 * 3).denominator == 1)

# A coefficientwise certificate for the entire odd-denominator family,
# q=2h+1, h>=1. All weights and basin areas are multiplied by 4h.
# There is no evaluation at sample h values and no denominator bound.
h = V('h')
k4_q = [2*h+1, Poly.coerce(1), Poly.coerce(1), Poly.coerce(1)]
k4_scaled_weights = [4*h*(2*h+1), 4*h*h, 4*h, 4*h+1]
k4_p = [
    [0, -2*h, -2, 1],
    [-1, 0, 0, 0],
    [-h, h-1, 0, 0],
    [2*h, 0, -(2*h+1), 0],
]
k4_scaled_basins = [
    [None, 12*h*h, 12*h, Poly.coerce(1)],
    [4*h*(3*h+1), None, 4*h, 4*h+1],
    [4*h*(3*h+1), 4*h, None, 4*h+1],
    [2*h, 4*h*h, 8*h*h+10*h+1, None],
]


def positive_coefficients(poly):
    poly = Poly.coerce(poly)
    return bool(poly.terms) and all(c > 0 for c in poly.terms.values())


for i in range(4):
    check(f'k4_family_row_sum_{i}', sum(k4_p[i]) == -k4_q[i])
    check(f'k4_family_positive_scaled_weight_{i}', positive_coefficients(k4_scaled_weights[i]))
    for j in range(4):
        if i == j:
            continue
        basin = k4_scaled_basins[i][j]
        check(f'k4_family_basin_identity_{i}_{j}',
              k4_q[i]*basin == k4_q[i]*k4_scaled_weights[j] - k4_scaled_weights[i]*k4_p[i][j])
        check(f'k4_family_positive_scaled_basin_{i}_{j}', positive_coefficients(basin))
    check(f'k4_family_full_component_area_{i}',
          sum(k4_scaled_basins[i][j] for j in range(4) if j != i) == sum(k4_scaled_weights))
for i in range(4):
    for j in range(i+1, 4):
        check(f'k4_family_crossing_unimodularity_{i}_{j}',
              k4_q[i] * k4_q[j] - k4_p[i][j] * k4_p[j][i] == 1)
k4_defects = [-k4_q[i] - sum(k4_p[j][i] for j in range(4) if j != i) for i in range(4)]
for i, expected in enumerate([-3*h, h, 2*h+2, Poly.coerce(-2)]):
    check(f'k4_family_branch_divisor_coefficient_{i}', k4_defects[i] == expected)
check('k4_family_total_branch_divisor_coefficient', sum(k4_defects) == 0)
check('k4_family_scaled_total_area', sum(k4_scaled_weights) == 12*h*h+12*h+1)
# q and 2h are coprime by q-2h=1; q and 2 are coprime by q+h*(-2)=1.
# The third high-row numerator is 1; all remaining branch q values equal 1.
check('k4_family_primitive_high_ray_Bezout', (2*h+1)-2*h == 1)

# The isolated-high-vertex lemma has m=q-1=t*b*(b+1).
# Its incoming numerator sum and strictly negative divisor coefficient are
# polynomial identities, while the classification of signs uses the written
# positive-directed-cycle argument.
b, t = V('b'), V('t')
m = t*b*(b+1)
incoming_sum = -1-t*b+t*(b+1)
isolated_defect = -(m+1)-incoming_sum
check('isolated_high_incoming_sum', incoming_sum == t-1)
check('isolated_high_negative_defect_formula', isolated_defect == -t*(b*(b+1)+1))

result = {
    'version': 9,
    'passed': True,
    'exact_checks': checks,
    'scope': 'Coefficientwise polynomial identities, parity over Z/2, exact node-budget arithmetic, arbitrary-line-denominator mixed defect calculation, and a complete symbolic positive four-line local family for every odd q>=3.',
    'universal_rigidity_certificate': 'q_A q_B (4 + e_i + e_j - N_ext) = m_i + m_j; with m_i=m_j=1 and odd positive q_A,q_B, both denominators equal 1.',
    'weaker_input': 'Integer puncture clutching alone suffices; neither nonnegative node counts nor the total node budget is needed for rigidity.',
    'symbolic_variables': ['q_A','q_B','e_i','e_j','m_i','m_j','P_A','P_B','Pprime_A','Pprime_B','N_ext'],
    'mixed_defects': {'each_mixed_plane': -1, 'each_quadric_component': -1, 'global_total': -6, 'line_denominators': 'arbitrary positive integers'},
    'node_budgets': node_budgets,
    'isolated_annulus_arithmetic_example': {'q_A': 1, 'q_B': 3, 'plane_P': [-1,-8], 'quadric_P': [0,-5], 'external_sum': '28/3', 'global_compatibility': False},
    'local_four_line_odd_denominator_family': {
        'parameter': 'integer h>=1; q=2h+1',
        'q_vector': ['2h+1','1','1','1'],
        'weights': ['2h+1','h','1','1+1/(4h)'],
        'outgoing_numerators': [['0','-2h','-2','1'],['-1','0','0','0'],['-h','h-1','0','0'],['2h','0','-(2h+1)','0']],
        'normalized_basin_areas': [['-','3h','3','1/(4h)'],['3h+1','-','1','1+1/(4h)'],['3h+1','1','-','1+1/(4h)'],['1/2','h','2h+5/2+1/(4h)','-']],
        'component_area': '3h+3+1/(4h)',
        'branch_divisor_coefficients': ['-3h','h','2h+2','-2'],
        'method': 'All identities are compared as polynomials after multiplying weights and basin areas by 4h. Positive coefficients prove positivity for every h>=1. A polynomial Bezout identity proves primitive high-ray actions.',
        'scope': 'Geometric local-chart realization requires the separate relative-Moser argument; no global quintic atlas is claimed.'
    },
    'isolated_high_branch_lemma': {'normal_form': '(-(q-1),-(b+1),b), with b and b+1 dividing q-1', 'parameter': 'q-1=t*b*(b+1)', 'coefficient': '-t*(b*(b+1)+1)<0', 'global_consequence': 'The higher-denominator support graph of a quintic atlas has no connected component consisting of a single edge.', 'qualification': 'The written sign/positive-cycle proof supplies the normal form; the script checks its polynomial coefficient formulas.'},
    'limitations': [
        'The script does not establish the geometric cycle framings, primitive action lattices, positivity of sectors, or constancy of the branch invariant.',
        'The full denominator obstruction and all-degree classification require the geometric proofs and inherited link obstructions in the paper.',
        'The isolated annulus example is not a complete local core chart or a global atlas.',
        'Changing cones, lattices, Reeb trees, or introducing branch singularities requires a new geometric analysis.'
    ],
    'certificates': certificates,
    'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest()
}

destination = Path(__file__).with_name('denominator_rigidity_verification_v9.json')
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'passed': True, 'exact_checks': checks, 'output': str(destination)}))
