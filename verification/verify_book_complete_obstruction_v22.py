#!/usr/bin/env python3
"""Exact algebraic checks for the v22 complete book-support obstruction.

Only Python's standard library is used.  This checker imports no earlier
generator or verifier, and runs no bounded search over w, scales, or high
denominators.  It checks the new proof's polynomial identities, all finite node
offsets, and parity obstruction.  The prior v21 two-sector reduction, including its
all-scale finite certificate for w <= 134, remains an explicitly stated proof
dependency; this script does not pretend to re-prove that theorem.
"""

from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json


class Poly:
    """A small exact sparse polynomial implementation, independent of SymPy."""

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {m: Fraction(c) for m, c in value.items() if c}
        else:
            c = Fraction(value)
            self.terms = {(): c} if c else {}

    @classmethod
    def variable(cls, name):
        return cls({((name, 1),): 1})

    def __add__(self, other):
        other = Poly(other)
        terms = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            terms[monomial] = terms.get(monomial, 0) + coefficient
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) + (-self)

    def __mul__(self, other):
        other = Poly(other)
        terms = {}
        for m1, c1 in self.terms.items():
            for m2, c2 in other.terms.items():
                powers = dict(m1)
                for name, exponent in m2:
                    powers[name] = powers.get(name, 0) + exponent
                monomial = tuple(sorted(powers.items()))
                terms[monomial] = terms.get(monomial, 0) + c1*c2
        return Poly(terms)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        result = Poly(1)
        for _ in range(exponent):
            result = result*self
        return result

    def substitute(self, replacements):
        result = Poly()
        for monomial, coefficient in self.terms.items():
            term = Poly(coefficient)
            for name, exponent in monomial:
                term *= Poly(replacements.get(name, Poly.variable(name)))**exponent
            result += term
        return result

    def encoded(self):
        return [dict(monomial=dict(m), coefficient=[c.numerator, c.denominator])
                for m, c in sorted(self.terms.items())]


IDENTITIES = []


def identity(name, left, right=0):
    difference = Poly(left)-right
    assert not difference.terms, (name, difference.encoded())
    IDENTITIES.append(name)


def positive_coefficients(name, polynomial, variable, base):
    """Check positivity on variable >= base by a nonnegative-coefficient shift."""
    shifted = Poly(polynomial).substitute({variable: Poly.variable('u')+base})
    assert all(c >= 0 for c in shifted.terms.values()), name
    assert shifted.terms.get((), 0) > 0, name
    return dict(name=name, domain=f'{variable}>={base}',
                shifted_variable=f'u={variable}-{base}',
                coefficients=shifted.encoded())


def local_rigidity():
    r, h, s, a, b, d, n = (Poly.variable(k)
                           for k in ('r', 'h', 's', 'alpha', 'beta', 'd', 'n'))
    F = (2*r+1)*h-r*r*d
    identity('rigidity numerator modulo r*alpha=s*h',
             F*a-h*(r*(2*a-d*s)+a), d*r*(s*h-r*a))
    identity('L3 sign boundary', 2*F.substitute({'d': 1, 'h': (r-1)*Fraction(1, 2)}), -r-1)
    identity('L4 sign boundary', F.substitute({'d': 2, 'h': r-1}), -r-1)
    identity('L3 forbidden positive integer n', r*n+a-h-1,
             r*(n-1)+(r-h-1)+a)
    identity('L4 forbidden positive integer n', 2*r*n+a-h-2,
             2*r*(n-1)+(2*r-h-1)+(a-1))
    R = Poly.variable('R')
    identity('L3 rigid F', F.substitute({'r': 2*R, 'h': R, 'd': 1}), R)
    identity('L4 rigid F', F.substitute({'h': r, 'd': 2}), r)
    identity('negative F scale estimate', a*b-(a+1-b), (b-1)*(a+1))
    # The opposite sign of F has an equally rigid integer beta-side bound.
    rho, k, z = (Poly.variable(name) for name in ('rho', 'k', 'z'))
    Frho = (2*rho-1)*k-rho*rho*d
    identity('F cannot vanish: polynomial Bezout identity',
             4*r*r-(2*r-1)*(2*r+1), 1)
    identity('Fnegative beta numerator modulo rho*beta=z*k',
             -Frho*b-k*(rho*(d*z-2*b)+b), rho*d*(rho*b-z*k))
    identity('L3 Fnegative sign boundary',
             2*Frho.substitute({'d': 1, 'k': (rho+1)*Fraction(1, 2)}), rho-1)
    identity('L4 Fnegative sign boundary',
             Frho.substitute({'d': 2, 'k': rho+1}), rho-1)
    identity('L3 Fnegative rigid F', F.substitute({'r': 2*R-1, 'h': R-1, 'd': 1}), -R)
    identity('L4 Fnegative rigid F', F.substitute({'h': r-1, 'd': 2}), -r-1)
    return dict(
        hypotheses=['r,s,z,h,alpha,beta are positive integers', '0<h<r*d',
                    'd in {1,2}', 'r*alpha=s*h',
                    'F*alpha*beta=(beta-alpha-1)*h*(h+d)'],
        logical_step='For F>0: 0 < Eplus*alpha = [r*(2*alpha-d*s)+alpha]/(h+d) < 1',
        conclusions={'L=3,F>0': 'r=2*R,S=3*R,T=3*R+2',
                     'L=4,F>0': 'S=2*r,T=2*r+3',
                     'L=3,F<0': 'r=2*R-1,S=3*R-2,T=3*R,R>=2',
                     'L=4,F<0': 'S=2*r-1,T=2*r+2,r>=2'},
        negative_F_logical_step='0<Eminus*beta=[(r+1)*(d*z-2*beta)+beta]/h<=1; the nonnegative integer z-2*beta or z-beta must vanish.',
        F_zero_impossible='gcd(r^2,2*r+1)=1, while F=0 would force 2*r+1 to divide d in {1,2}.')


def negative_rigidity():
    w, H, c, e, u, v = (Poly.variable(k) for k in ('w', 'H', 'c', 'e', 'u', 'v'))
    identity('no E=0: lower consecutive square gap', H*(H+1)-H*H, H)
    identity('no E=0: upper consecutive square gap', (H+1)**2-H*(H+1), H+1)
    identity('E>0 scale formula modulo u*H=c*w',
             c*c*w*w-u*u*H*H, (c*w-u*H)*(c*w+u*H))
    identity('E>0 integer endpoint bound',
             c*c-u*u-(2*c-1), (c-1-u)*(c-1+u))
    identity('E<0 scale formula modulo v*(H+1)=e*w',
             e*e*w*w-v*v*(H+1)**2, (e*w-v*(H+1))*(e*w+v*(H+1)))
    identity('E<0 integer endpoint bound',
             v*v-e*e-(2*e+1), (v-e-1)*(v+e+1))
    identity('E at H=w', w*(w+1)-w*w, w)
    identity('E at H=w-1', (w-1)*w-w*w, -w)
    return dict(
        common_hypotheses=['w,H positive integers', 'c>=2,e>=1 positive integers',
                          'E=1-w^2/[H*(H+1)]', 'E*c*e=e-c+1',
                          's=c*(w+H)/H integer', 'z=e*(w+H+1)/(H+1) integer'],
        positive_case=dict(
            excluded_assumption='H>w', integer_gap='u=s-c=c*w/H<=c-1',
            contradiction='1>E*c>c-u^2/c>=2-1/c>1',
            conclusion='H=w,r=2*w,E=1/(w+1)'),
        negative_case=dict(
            excluded_assumption='H<=w-2', integer_gap='v=z-e=e*w/(H+1)>=e+1',
            contradiction='1>(-E)*e>v^2/e-e>=2+1/e>1',
            conclusion='H=w-1,r=2*w-1,E=-1/(w-1)'))


def scale_families():
    """Check useful complete parametrizations recorded in the research notes."""
    ell, t = Poly.variable('ell'), Poly.variable('t')
    records = []
    for family in ('positive_L3', 'positive_L4', 'positive_L3_Fnegative',
                   'positive_L4_Fnegative', 'negative_Epositive', 'negative_Enegative'):
        if family == 'positive_L3':
            L = 3
            R = ell*(t+1)-2
            r, S, T = 2*R, 3*R, 3*R+2
            s, z = 2*(ell*t-1), (2*R+1)*t
            x, y = 3*(ell*t-1), T*t
            p = 2*ell*t*t-3*t+3
            q = 3*ell*t*t-4*t+5
            parity_expression = R*t+2*t
        elif family == 'positive_L4':
            L = 4
            r = ell*(t+1)-3
            S, T = 2*r, 2*r+3
            s, z = ell*t-1, (r+1)*t
            x, y = 2*s, T*t
            p = ell*t*t-2*t+2
            q = 2*ell*t*t-3*t+5
            parity_expression = (r+1)*t+2*t
        elif family == 'positive_L3_Fnegative':
            L = 3
            R = ell*(t+1)+2
            r, S, T = 2*R-1, 3*R-2, 3*R
            s, z = (2*R-1)*t, 2*(ell*t+1)
            x, y = S*t, 3*(ell*t+1)
            p, q = -2*ell*t*t-3*t+3, 5-3*ell*t*t-4*t
            parity_expression = R*t-2*t
        elif family == 'positive_L4_Fnegative':
            L = 4
            r = ell*(t+1)+2
            S, T = 2*r-1, 2*r+2
            s, z = r*t, ell*t+1
            x, y = S*t, 2*(ell*t+1)
            p, q = -ell*t*t-2*t+2, 5-2*ell*t*t-3*t
            parity_expression = r*t-2*t
        elif family == 'negative_Epositive':
            L = 1
            w = ell*(t+1)
            r, S, T = 2*w, w, w
            s, z = 2*(ell*t+1), (2*w+1)*t
            x, y = ell*t+1, w*t
            p, q = 2*ell*t*t+t-1, ell*t*t-1
            parity_expression = w*t
        else:
            L = 1
            w = ell*(t+1)
            r, S, T = 2*w-1, w, w
            s, z = (2*w-1)*t, 2*(ell*t-1)
            x, y = w*t, ell*t-1
            p, q = -2*ell*t*t+t-1, -ell*t*t-1
            parity_expression = w*t
        a, b = s*S+1, z*T+1
        U, V = a+x-s, b-y+z
        matrix = ((0, -U, x, -s), (-V, 0, -y, z),
                  (r, -r-1, 0, 0), (-S, T, -L, 0))
        qs = (a, b, Poly(1), Poly(1))
        identity(f'{family} x integrality formula', r*x, s*S)
        identity(f'{family} y integrality formula', (r+1)*y, z*T)
        for i in range(4):
            identity(f'{family} row {i}', sum(matrix[i]), -qs[i])
        for i in range(4):
            for j in range(i+1, 4):
                identity(f'{family} pair {i},{j}',
                         Poly(matrix[i][j])*matrix[j][i], qs[i]*qs[j]-1)
        identity(f'{family} minus D_D', z+1-s, p)
        identity(f'{family} D_C', L-1-x+y, q)
        transfer = 2*q-3*p if L == 3 else q-2*p if L == 4 else p-2*q
        identity(f'{family} low D transfer', transfer, t+1)
        identity(f'{family} automatic odd high denominators', parity_expression, ell*t*(t+1))
        records.append(dict(family=family, L=L, r=r.encoded(), s=s.encoded(), z=z.encoded(),
                            S=S.encoded(), T=T.encoded(),
                            minus_D_D=p.encoded(), D_C=q.encoded(),
                            parity_reason='t*(t+1) is even for every integer t'))
    return records


def type_I():
    w = Poly.variable('w')
    records = []
    for t1, t2, tn in product((1, 2), (1, 2), (-1, 0, 1, 2)):
        r2 = w-tn
        r1 = (3*r2+4)*Fraction(1, 2)-t2
        rN = (3*r1+4)*Fraction(1, 2)-t1
        H = rN-w
        kappa = 20-4*t1-6*t2-9*tn
        identity(f'I offset {t1},{t2},{tn}', 4*H, 5*w+kappa)
        identity(f'I rigid negative offset {t1},{t2},{tn}',
                 4*(2*w)-(9*w+kappa), -w-kappa)
        records.append(dict(t1=t1, t2=t2, tN=tn, kappa=kappa, forced_w=-kappa))
    assert len(records) == 16
    assert min(p['kappa'] for p in records) == -18
    assert max(p['kappa'] for p in records) == 19
    assert max(p['forced_w'] for p in records) == 18
    return dict(all_offsets=records, kappa_range=[-18, 19],
                forced_w_max=18, conclusion='H=w gives w=-kappa<=18')


def type_II():
    w, r1 = Poly.variable('w'), Poly.variable('r1')
    identity('II first-node forced reverse', (2*r1+3)-2, 2*r1+1)
    residual = 2*w-(2*r1+1)
    identity('II parity residual', residual, 2*(w-r1)-1)
    coefficients_mod_2 = {}
    for monomial, coefficient in residual.terms.items():
        assert coefficient.denominator == 1
        if coefficient.numerator % 2:
            coefficients_mod_2[monomial] = coefficient.numerator % 2
    assert coefficients_mod_2 == {(): 1}
    return dict(forced_first_offset=2,
                forced_reverse_formulas=['rN=2*w', 'rN=2*r1+1'],
                residual=residual.encoded(), residual_mod_2=1,
                conclusion='2*w=2*r1+1 has no integer solution')


def run():
    IDENTITIES.clear()
    rigidity = local_rigidity()
    negative = negative_rigidity()
    families = scale_families()
    first = type_I()
    second = type_II()
    prior_lower_bound = 135
    assert first['kappa_range'] == [-18, 19]
    assert first['forced_w_max'] == 18 < prior_lower_bound
    proof_name = 'book_complete_obstruction_v22.tex'
    proof_path = next(p for p in (Path(__file__).with_name(proof_name),
                                  Path(__file__).parent.parent/'papers/sections/paper'/proof_name)
                      if p.is_file())
    return dict(
        status='PASS',
        mathematical_scope='No book low triangle under the standard K5 integer-chart, odd-denominator, nonnegative-node and opposite-low-D cancellation assumptions.',
        verification_role='Exact algebraic cross-checks and finite offset/parity certificates for the accompanying human proof; no bounded large-w search.',
        prior_proof_dependency='Theorem bs21:two-sectors and its existing all-scale certificate for w<=134; not re-proved by this checker.',
        arbitrary_parameter_cutoff=None,
        new_negative_core_enumeration=False,
        positive_rigidity=rigidity,
        negative_rigidity=negative,
        reusable_scale_families=families,
        companion_scale_classification_file='two_high_rigid_scale_families_v22.tex',
        all_six_scale_families_checked=True,
        exceptional_fixed_reverse_resonances=['(r,s,z,S,T)=(3,3*t,2,4,6), t>=1',
                                             '(r,s,z,S,T)=(2,2*t,1,3,6), t>=1'],
        type_I=first,
        type_II=second,
        prior_residual_w_lower_bound=prior_lower_bound,
        number_of_polynomial_identities=len(IDENTITIES),
        polynomial_identities=IDENTITIES,
        proof_file=proof_name,
        proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('book_complete_obstruction_verification_v22.json'))
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'],
                          number_of_polynomial_identities=result['number_of_polynomial_identities'],
                          all_type_I_offsets=len(result['type_I']['all_offsets']),
                          type_I_w_max=18, type_II_parity_obstruction=True,
                          new_negative_core_enumeration=False), ensure_ascii=False))
