#!/usr/bin/env python3
"""Unbounded endpoint certificates and complete fixed-s reconstruction, stdlib only.

No old producer/verifier imports.  Coefficient identities are exact; finite
reconstruction results are explicitly separate from infinite-domain theorems.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import isqrt
from pathlib import Path
import argparse
import json


class Poly:
    def __init__(self, n, terms=None):
        self.n = n
        self.terms = {tuple(e): c for e, c in (terms or {}).items() if c}
        assert all(len(e) == n and min(e) >= 0 for e in self.terms)

    @classmethod
    def const(cls, n, value):
        return cls(n, {(0,) * n: value})

    @classmethod
    def variables(cls, n):
        return tuple(cls(n, {tuple(int(i == j) for i in range(n)): 1}) for j in range(n))

    def coerce(self, other):
        if isinstance(other, (int, Fraction)):
            return Poly.const(self.n, other)
        assert isinstance(other, Poly) and other.n == self.n
        return other

    def __add__(self, other):
        other = self.coerce(other)
        result = defaultdict(int, self.terms)
        for exp, value in other.terms.items():
            result[exp] += value
        return Poly(self.n, result)
    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n, {exp: -c for exp, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        other = self.coerce(other)
        result = defaultdict(int)
        for exp, value in self.terms.items():
            for exp2, value2 in other.terms.items():
                result[tuple(a + b for a, b in zip(exp, exp2))] += value * value2
        return Poly(self.n, result)
    __rmul__ = __mul__

    def __truediv__(self, other):
        assert isinstance(other, int) and other
        return self * Fraction(1, other)

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        result, power = Poly.const(self.n, 1), self
        while exponent:
            if exponent & 1:
                result = result * power
            exponent //= 2
            power = power * power
        return result

    def substitute(self, values):
        assert len(values) == self.n
        values = [self.coerce(v) for v in values]
        result = Poly.const(self.n, 0)
        cache = [{0: Poly.const(self.n, 1)} for _ in values]
        for exp, value in self.terms.items():
            term = Poly.const(self.n, value)
            for i, degree in enumerate(exp):
                if degree not in cache[i]:
                    cache[i][degree] = values[i] ** degree
                term = term * cache[i][degree]
            result = result + term
        return result

    def coefficient(self, variable, degree):
        result = {}
        for exp, value in self.terms.items():
            if exp[variable] == degree:
                exp2 = list(exp)
                exp2[variable] = 0
                result[tuple(exp2)] = value
        return Poly(self.n, result)

    def records(self):
        result = []
        for exp, value in sorted(self.terms.items()):
            assert Fraction(value).denominator == 1
            result.append({'exponents': list(exp), 'coefficient': int(value)})
        return result


def identity(name, left, right, checks):
    difference = left - right
    assert not difference.terms, (name, difference.records())
    checks.append({'name': name, 'status': 'PASS', 'difference_terms': 0,
                   'left_terms': len(left.terms), 'right_terms': len(right.terms)})


def positive_certificate(name, polynomial, variables):
    assert polynomial.terms and all(c > 0 for c in polynomial.terms.values()), name
    constant = polynomial.terms.get((0,) * polynomial.n, 0)
    assert constant > 0, (name, constant)
    records = polynomial.records()
    return {'name': name, 'status': 'PASS', 'variables': variables,
            'nonzero_coefficients': len(records), 'constant': int(constant),
            'minimum_coefficient': int(min(polynomial.terms.values())),
            'all_nonzero_coefficients_positive': True,
            'coefficients_sha256': sha256(json.dumps(records, sort_keys=True).encode()).hexdigest(),
            'full_coefficients': records}


def original_residual(s, b, z, n, t):
    F = b - 1 + s * z
    S = t - (F + 1) * n
    T = s + F * n
    alpha = (s + t) * z + b - 1
    return -(s + t * b) * S + (s * alpha - t) * T - alpha * b


def axis_quartic(s, b, z, n):
    F = b - 1 + s * z
    m = F * F + F + 1
    K = s * (F - 1) - z + 1
    V = m * n + K
    return (-b * V * V + (b + 1) * (s*s*z - 2*s - b*z) * V
            + (b + 1)**2 * F * (s*s - b)
            + n * (s*m*(b + 1)**2 + (F*F + b) * V * (b + 1)))


def c_value(s, z, n):
    return n * ((s*z)**2 - 3*s*z + 3) + (s*s - 1)*z - 3*s + 1


def endpoint_r_coefficients(s, z):
    C = s*s*z*(z*z + 1) - 3*s*(z*z + 1) + 2*z + 1
    A = 3*s*(z*z + 1) - 4*z - 1
    B = 3*s*s*(z*z + 1)**2 - 2*s*(z*z + 1)*(4*z + 1) + 5*z*z + 4*z - 2
    H = s*z*(z*z + 1) - z*z - z + 3
    return C, A, B, H


def endpoint_R(s, z, e):
    C, A, B, H = endpoint_r_coefficients(s, z)
    return e**4 + A*e**3 + B*e*e + C*H*e - C*C


def symbolic_certificates():
    checks, positive = [], []
    s, b, z, n, e = Poly.variables(5)
    F = b - 1 + s*z
    m = F*F + F + 1
    K = s*(F - 1) - z + 1
    V = m*n + K
    den = b + 1
    Snum = V - (F + 1)*n*den
    T = s + F*n
    anum = (s*den + V)*z + (b - 1)*den
    direct_numerator = -(s*den + b*V)*Snum + (s*anum - V)*T*den - anum*b*den
    P = axis_quartic(s, b, z, n)
    identity('quartic_from_original_pair_residual', P, direct_numerator, checks)
    Cn = c_value(s, z, n)
    identity('positive_integer_quotient_identity', V,
             den*(s + n*(b + 2*s*z - 2)) + Cn, checks)
    t = s + n*(b + 2*s*z - 2) + e
    residual = original_residual(s, b, z, n, t)
    assert max(exp[1] for exp in residual.terms) == 2
    identity('b_squared_coefficient_after_quotient', residual.coefficient(1, 2),
             -e*n + n*n - n*z - 1, checks)
    Rgeneral = sum((residual.coefficient(1, i) * (Cn - e)**i * e**(2-i)
                    for i in range(3)), Poly.const(5, 0))
    identity('general_quotient_polynomial_is_monic_quartic',
             Rgeneral.coefficient(4, 4), Poly.const(5, 1), checks)
    assert max(exp[4] for exp in Rgeneral.terms) == 4
    Ag = 3*n*s*z - 6*n + 3*s + 2*z - 1
    Bg = (4*n*n*s*s*z*z - 15*n*n*s*z + 15*n*n - n*s*s*z**3 + 7*n*s*s*z
          + 7*n*s*z*z - 2*n*s*z - 15*n*s - 11*n*z + 5*n
          - s*s*z*z + 3*s*s + 7*s*z - 2*s + z*z - z - 2)
    Hg = 3*n*n*s*z - 6*n*n - 2*n*s*z*z + 3*n*s + 5*n*z - n - 2*s*z + 3
    Dg = 1 + n*(z - n)
    identity('general_quotient_coefficients_recorded_in_notes', Rgeneral,
             e**4 + Ag*e**3 + Bg*e*e + Cn*Hg*e - Dg*Cn*Cn, checks)
    R = Rgeneral.substitute([s, b, z, z, e])
    C, A, B, H = endpoint_r_coefficients(s, z)
    identity('endpoint_R_from_original_pair_residual', R,
             e**4 + A*e**3 + B*e*e + C*H*e - C*C, checks)

    P0 = P.substitute([s, b, z, 0, e])
    A2 = (s*s - 1)*(s*s - b*b)
    A1 = (b - 1)*(-2*b*b*s - b*s - b + 3*s**3 - s*s - 2*s)
    A0 = -b**4 - b**3 + 3*b*b*s*s - 2*b*b*s + b*b - 3*b*s*s + 2*b*s + 3*s*s - 2*s
    identity('n_zero_quadratic_in_z', P0, A2*z*z + A1*z + A0, checks)
    identity('n_zero_s2_b2', P0.substitute([2, 2, z, 0, 0]), -2*(3*z - 2), checks)
    identity('n_zero_s2_b3', P0.substitute([2, 3, z, 0, 0]), -(z + 1)*(15*z + 43), checks)
    lower_expansion = (z*z*n**4 + z*(4*b*z + 3*b - 3)*n**3
        + ((5*b*b - 1)*z*z + (9*b*b - 10*b + 1)*z + 3*b*b - 3*b + 3)*n*n
        + (2*b*(b*b - 1)*z*z + (7*b**3 - 10*b*b + b + 2)*z
           + 6*b**3 - 8*b*b + 8*b - 2)*n
        + b*(b - 1)*((b - 3)*(b + 1)*z + 2*(b - 1)**2))
    identity('n_zero_lower_b_expansion', P0.substitute([b + n, b, z, 0, 0]),
             lower_expansion, checks)
    positive.append(positive_certificate('n_zero_s_greater_b',
        P0.substitute([s + b + 3, b + 2, z + 1, 0, 0]),
        ['s_minus_b_minus_1', 'b_minus_2', 'z_minus_1', 'unused', 'unused']))
    positive.append(positive_certificate('n_zero_s_equals_b_at_least_3',
        P0.substitute([s + 3, s + 3, z + 1, 0, 0]),
        ['s_minus_3', 'unused', 'z_minus_1', 'unused', 'unused']))

    L4 = Poly.const(5, 16)
    L3 = 16*(2*s*z + 6*s + 1)
    L2 = 8*(2*(s*s - 1)*z*z + (18*s*s - 2*s + 2)*z + 21*s*s + 13*s - 2)
    L1 = 4*(12*s*(s*s - 1)*z*z + (42*s**3 - 8*s*s + 16*s - 4)*z
            + 18*s**3 + 63*s*s - 20*s)
    L0 = s*(20*s*(s*s - 1)*(z - 1)**2
            + (76*s**3 + 36*s*s + 4*s - 56)*(z - 1)
            + 29*s**3 + 234*s*s - 108*s - 24)
    L = L4*b**4 + L3*b**3 + L2*b*b + L1*b + L0
    identity('n_zero_b_ge_three_s_over_two',
             -16*P0.substitute([s, 3*s/2 + b, z, 0, 0]), L, checks)
    positive.append(positive_certificate('n_zero_b_ge_three_s_over_two',
        L.substitute([s + 3, b, z + 1, 0, 0]),
        ['s_minus_3', 'b_minus_3s_over_2', 'z_minus_1', 'unused', 'unused']))

    J2 = 4*(b + 1)*(s*s - 1)*(b + 2*s + 1)
    J1 = 4*(2*s*b**3 + (s**3 + 6*s*s + 4*s + 1)*b*b
            + (2*s**4 + 5*s**3 + 9*s*s + 5*s + 1)*b + s*s*(s*s + 7*s + 4))
    J0 = (4*b**4 + 4*(s*s + 4*s + 5)*b**3
          + (s**4 + 12*s**3 + 21*s*s + 70*s + 32)*b*b
          + 2*(s**5 + 4*s**4 + 6*s**3 + 38*s*s + 37*s + 10)*b
          + 5*s**4 + 26*s**3 + 29*s*s + 28*s + 4)
    J = J2*z*z + J1*z + J0
    identity('n_zero_z_ge_s_over_two',
             -4*P0.substitute([s, s + 1 + b, s/2 + z, 0, 0]), J, checks)
    positive.append(positive_certificate('n_zero_z_ge_s_over_two',
        J.substitute([s + 3, b, z, 0, 0]),
        ['s_minus_3', 'b_minus_s_minus_1', 'z_minus_s_over_2', 'unused', 'unused']))

    for name, poly in [('A', A), ('B', B), ('H', H)]:
        positive.append(positive_certificate('n_equals_z_s_ge_2_' + name,
            poly.substitute([s + 2, 0, z + 1, 0, 0]),
            ['s_minus_2', 'unused', 'z_minus_1', 'unused', 'unused']))
    Qs = [16*z**5 + 8*z**4 + 28*z**3 + 38*z*z + 6*z + 25,
          24*z**5 + 52*z**4 + 18*z**3 + 171*z*z - 31*z + 117,
          12*z**5 + 58*z**4 + 2*z**3 + 177*z*z - 30*z + 130,
          2*z**5 + 23*z**4 + 69*z*z - 6*z + 53,
          3*z**4 + 9*z*z + 7]
    identity('n_equals_z_R_at_s', R.substitute([s, 0, z, 0, s]),
             sum((q*(s - 2)**i for i, q in enumerate(Qs)), Poly.const(5, 0)), checks)
    positive.append(positive_certificate('n_equals_z_R_at_s_positive',
        R.substitute([s + 2, 0, z + 1, 0, s + 2]),
        ['s_minus_2', 'unused', 'z_minus_1', 'unused', 'unused']))
    Es = [(s - 1)**2*(s**3 + 2*s*s + s - 1)*(s**4 + s**3 - 4*s + 1),
          (s - 1)*(6*s**7 + 14*s**6 + 14*s**5 + 4*s**4 + 4*s**3 - 4*s*s - 24*s + 13),
          15*s**7 + 22*s**6 + 8*s**5 - 15*s**4 - 34*s**3 - 15*s*s + 38*s - 10,
          2*(10*s**6 + 14*s**5 + 2*s**4 - 14*s**3 - 13*s*s + 11*s - 1),
          s*(15*s**4 + 17*s**3 - 6*s*s - 16*s + 5),
          2*s*s*(3*s*s + 2*s - 2), s**3]
    gap = -R.substitute([s, 0, s + 1 + z, 0, s - 1])
    identity('n_equals_z_root_gap_expansion', gap,
             sum((q*z**i for i, q in enumerate(Es)), Poly.const(5, 0)), checks)
    positive.append(positive_certificate('n_equals_z_no_root_when_z_ge_s_plus_1',
        gap.substitute([s + 2, 0, z, 0, 0]),
        ['s_minus_2', 'unused', 'z_minus_s_minus_1', 'unused', 'unused']))
    identity('n_equals_z_s_one_C', C.substitute([1, 0, z, 0, 0]), (z - 1)**3 - 1, checks)
    for name, poly in [('A', A), ('B', B), ('H', H)]:
        positive.append(positive_certificate('n_equals_z_s_one_' + name,
            poly.substitute([1, 0, z + 2, 0, 0]),
            ['unused', 'unused', 'z_minus_2', 'unused', 'unused']))
    R1 = 2*z**5 + 14*z**4 + 44*z**3 + 72*z*z + 61*z + 18
    identity('n_equals_z_s_one_R_at_one', R.substitute([1, 0, z + 2, 0, 1]), R1, checks)
    positive.append(positive_certificate('n_equals_z_s_one_R_at_one_positive', R1,
        ['unused', 'unused', 'z_minus_2', 'unused', 'unused']))
    return {'status': 'PASS', 'identities': checks, 'positive_certificates': positive}


def exact_model(s, b, z, n, t):
    assert original_residual(s, b, z, n, t) == 0
    F = b - 1 + s*z
    S, T = t - (F + 1)*n, s + F*n
    u = s + t - 1
    U = u + z - n
    if min(S, T, U) <= 0:
        return None
    alpha, k = (s + t)*z + b - 1, F
    q = (1 + s*S, 1 + t*T, 1 + u*U, 1)
    P = ((0, t*S + alpha, -u*S - alpha - 1, -S),
         (s*T - b, 0, -u*T + b - 1, -T),
         (-s*U + k, -t*U - k - 1, 0, U), (-s, -t, u, 0))
    signs = (P[0][1], P[1][0], -P[0][2], -P[1][2], -P[2][0], -P[2][1])
    if min(signs) <= 0:
        return None
    rows = [sum(P[i]) + q[i] for i in range(4)]
    pairs = [P[i][j]*P[j][i] - q[i]*q[j] + 1 for i in range(4) for j in range(i+1, 4)]
    defects = [-q[i] - sum(P[j][i] for j in range(4)) for i in range(4)]
    assert rows == [0]*4 and pairs == [0]*6 and defects == [0, 0, z, -z]
    weights = (Fraction(q[0]), Fraction(P[0][1]) + Fraction(1, 2*P[1][0]),
               Fraction(u) + Fraction(1, 2*U), Fraction(1))
    gaps = [weights[j] - Fraction(P[i][j], q[i])*weights[i]
            for i in range(4) for j in range(4) if i != j]
    assert min(gaps) > 0
    return {'s': s, 'b': b, 'z': z, 'n': n, 't': t, 'scales': [S, T, U],
            'q': q, 'P': P, 'D': defects, 'original_pair_residual': 0,
            'all_six_pair_residuals': pairs, 'weights': [str(w) for w in weights],
            'minimum_weight_gap': str(min(gaps))}


def quadratic_integer_roots(A, B, C):
    assert A
    discriminant = B*B - 4*A*C
    if discriminant < 0:
        return []
    root = isqrt(discriminant)
    if root*root != discriminant:
        return []
    result = set()
    for numerator in (-B - root, -B + root):
        if numerator % (2*A) == 0:
            result.add(numerator // (2*A))
    return sorted(result)


def reconstruct_fixed_s(s):
    stats = {'s': s, 'n_zero_b_tested': 0, 'n_zero_integer_quadratic_roots': 0,
             'n_zero_quotient_pass': 0, 'n_equals_z_pairs_covered': s*(s-1),
             'n_equals_z_z_tested': 0, 'n_equals_z_R_evaluations': 0,
             'n_equals_z_integer_R_roots': 0, 'n_equals_z_quotient_pass': 0,
             'models': []}
    if s >= 3:
        for b in range(s + 1, (3*s - 1)//2 + 1):
            stats['n_zero_b_tested'] += 1
            A = (s*s - 1)*(s*s - b*b)
            B = (b - 1)*(-2*b*b*s - b*s - b + 3*s**3 - s*s - 2*s)
            C = -b**4 - b**3 + 3*b*b*s*s - 2*b*b*s + b*b - 3*b*s*s + 2*b*s + 3*s*s - 2*s
            for z in quadratic_integer_roots(A, B, C):
                if not 1 <= z <= (s-1)//2:
                    continue
                stats['n_zero_integer_quadratic_roots'] += 1
                F = b - 1 + s*z
                K = s*(F - 1) - z + 1
                if K % (b+1):
                    continue
                t = K//(b+1)
                if t <= s:
                    continue
                stats['n_zero_quotient_pass'] += 1
                assert axis_quartic(s, b, z, 0) == 0
                assert original_residual(s, b, z, 0, t) == 0
                model = exact_model(s, b, z, 0, t)
                if model:
                    stats['models'].append(model)
    if s >= 2:
        for z in range(1, s+1):
            stats['n_equals_z_z_tested'] += 1
            C, A, B, H = endpoint_r_coefficients(s, z)
            if C <= 0:
                continue
            assert A > 0 and B > 0 and H > 0
            # Monotonicity is proved above. Binary search covers all e in [1,s-1].
            lo, hi = 0, s
            while hi - lo > 1:
                mid = (lo + hi)//2
                value = endpoint_R(s, z, mid)
                stats['n_equals_z_R_evaluations'] += 1
                if value < 0:
                    lo = mid
                else:
                    hi = mid
            if hi == s:
                continue
            value = endpoint_R(s, z, hi)
            stats['n_equals_z_R_evaluations'] += 1
            if value:
                continue
            stats['n_equals_z_integer_R_roots'] += 1
            if C % hi:
                continue
            b = C//hi - 1
            if b < 2:
                continue
            stats['n_equals_z_quotient_pass'] += 1
            t = s + z*(b + 2*s*z - 2) + hi
            F = b - 1 + s*z
            assert (b+1)*t == (F*F + F + 1)*z + s*(F - 1) - z + 1
            assert t > s and original_residual(s, b, z, z, t) == 0
            model = exact_model(s, b, z, z, t)
            if model:
                stats['models'].append(model)
    return stats


def negative_control():
    # Within the newly finite n=z domain. Q, the quotient and all signs pass,
    # but the original pair residual does not. This must never be a model.
    s, b, z, n, t, e = 3, 2, 1, 1, 10, 1
    F = b - 1 + s*z
    S, T, u = t - (F+1)*n, s + F*n, s + t - 1
    U = u + z - n
    alpha = (s+t)*z + b - 1
    signs = [t*S + alpha, s*T - b, u*S + alpha + 1,
             u*T - b + 1, s*U - F, t*U + F + 1]
    assert min(S, T, U, *signs) > 0
    assert (b+1)*e == c_value(s, z, n)
    assert (b+1)*t == (F*F + F + 1)*n + s*(F - 1) - z + 1
    r = original_residual(s, b, z, n, t)
    assert r == 81 and endpoint_R(s, z, e) == 81
    return {'parameters': {'s': s, 'b': b, 'z': z, 'n': n, 't': t, 'e': e},
            'difference_equation_pass': True, 'integer_quotient_pass': True,
            'scales_and_all_signs_positive': True, 'original_pair_residual': r,
            'rejected_as_required': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--s-cap', type=int, default=400)
    parser.add_argument('--output', type=Path,
        default=Path(__file__).with_name('high_d_axis_endpoints_v25_results.json'))
    parser.add_argument('--proof', type=Path)
    args = parser.parse_args()
    if args.proof is None:
        candidates = [Path(__file__).with_name('high_d_axis_endpoints_v25.tex'),
                      Path(__file__).parent.parent / 'paper' / 'high_d_axis_endpoints_v25.tex']
        args.proof = next((path for path in candidates if path.exists()), None)
    if args.proof is None or not args.proof.is_file():
        parser.error('The complete proof TeX must be supplied using --proof.')
    assert args.s_cap >= 1
    symbolic = symbolic_certificates()
    rows = [reconstruct_fixed_s(s) for s in range(1, args.s_cap+1)]
    count_keys = [key for key in rows[0] if key not in ('s', 'models')]
    totals = {key: sum(row[key] for row in rows) for key in count_keys}
    models = [model for row in rows for model in row['models']]
    result = {'version': 25, 'status': 'PASS', 'scope': 'three-high proportional zero axis: endpoints n=0,z',
              'unbounded_theorem': {'n_zero': 's>=3, s<b<3s/2, 1<=z<s/2',
                                   'n_equals_z': 's>=2, 1<=z<=s, 1<=e=C_z/(b+1)<=s-1',
                                   'fixed_s_endpoints_completely_finite': True,
                                   'global_nonexistence_claimed': False,
                                   'interior_0_lt_n_lt_z_resolved': False},
              'symbolic_verification': symbolic,
              'finite_reconstruction': {'label': 'FINITE RESULT, not an all-s theorem',
                                        's_min': 1, 's_max': args.s_cap,
                                        'high_row_or_scale_cutoff': None,
                                        'totals': totals, 'models_count': len(models),
                                        'models': models, 'per_s': rows},
              'negative_control': negative_control(),
              'source_file': str(Path(__file__).resolve()),
              'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'proof_file': str(args.proof.resolve()),
              'proof_sha256': sha256(args.proof.read_bytes()).hexdigest(),
              'external_peer_review': False,
              'proof_assistant_formalization': False}

    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'identities': len(symbolic['identities']),
                      'positive_certificates': len(symbolic['positive_certificates']),
                      's_cap': args.s_cap, 'totals': totals, 'models_count': len(models),
                      'output': str(args.output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
