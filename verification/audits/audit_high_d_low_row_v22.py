#!/usr/bin/env python3
"""Independent coefficient audit of the v22 fixed-low-row finiteness theorem.

This file imports neither the primary high-D verifier nor any earlier verifier.
The reconstruction starts from the v21 definitions of E,J and all three original
pair-product residuals.  Polynomial coefficients use exact Python integers.
No parameter scan or floating-point arithmetic is used.
"""

from pathlib import Path
import argparse
import hashlib
import json

VARIABLES = ('s', 't', 'x', 'y', 'z', 'B')
ZERO_MONOMIAL = (0,)*len(VARIABLES)


def const(n):
    return {ZERO_MONOMIAL: n} if n else {}


def variable(name):
    powers = [0]*len(VARIABLES)
    powers[VARIABLES.index(name)] = 1
    return {tuple(powers): 1}


def add(*polynomials):
    output = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            output[monomial] = output.get(monomial, 0)+coefficient
    return {m: c for m, c in output.items() if c}


def scale(polynomial, coefficient):
    return {m: c*coefficient for m, c in polynomial.items() if c*coefficient}


def sub(left, right):
    return add(left, scale(right, -1))


def mul(*polynomials):
    output = const(1)
    for polynomial in polynomials:
        next_output = {}
        for monomial1, coefficient1 in output.items():
            for monomial2, coefficient2 in polynomial.items():
                monomial = tuple(a+b for a, b in zip(monomial1, monomial2))
                next_output[monomial] = next_output.get(monomial, 0)+coefficient1*coefficient2
        output = {m: c for m, c in next_output.items() if c}
    return output


def evaluate(polynomial, values):
    return sum(coefficient*product(values[name]**exponent
                                  for name, exponent in zip(VARIABLES, monomial))
               for monomial, coefficient in polynomial.items())


def product(values):
    output = 1
    for value in values:
        output *= value
    return output


CHECKS = []


def optional_source_hash(filename):
    for base in (Path(__file__).parent, Path(__file__).parent.parent,
                 Path(__file__).parent.parent.parent):
        for subdir in ('', 'highd', 'paper', 'verification'):
            path = base/subdir/filename
            if path.is_file():
                return hashlib.sha256(path.read_bytes()).hexdigest()
    return None


def check(name, left, right):
    difference = sub(left, right)
    assert not difference, (name, sorted(difference.items()))
    CHECKS.append(dict(name=name, expanded_left_terms=len(left),
                       expanded_right_terms=len(right), residual_coefficients=[]))


def run():
    CHECKS.clear()
    s, t, x, y, z, B = (variable(name) for name in VARIABLES)
    one = const(1)
    b = add(B, one)
    u = add(s, t, const(-1))
    h = sub(s, x)
    j = sub(t, y)
    ell = add(u, z)
    lam = add(mul(u, x), mul(s, z))
    mu = add(mul(u, y), mul(t, z))
    F = add(B, lam)
    F1 = add(F, one)
    m = add(mul(F, F), F, one)
    d = add(x, y, z)
    alpha = add(mul(u, d), B, z)
    k = sub(add(mul(s, d), B), x)

    # Original v21 reconstruction, prior to the new coefficient separations.
    E = sub(sub(mul(mu, h), ell), j)
    J = sub(add(h, ell), mul(lam, j))
    nS = add(mul(m, h), mul(F, E), scale(J, -1))
    nT = add(mul(m, j), E, mul(F1, J))
    nU = add(mul(m, ell), mul(F1, E), mul(F, J))
    E0 = sub(mul(t, h, z), add(u, z, t))
    J0 = sub(add(h, u, z), mul(lam, t))
    a = sub(mul(u, h), mul(B, F1))
    n0 = add(mul(F1, add(mul(B, t), h)), mul(F, add(u, z)), mul(h, t, z))
    nS0 = add(mul(m, h), mul(F, E0), scale(J0, -1))
    c = add(mul(F, u, h), B)
    check('E affine separation', E, add(E0, mul(add(mul(u, h), one), y)))
    check('J affine separation', J, add(J0, mul(lam, y)))
    check('nT=n0+a*y', nT, add(n0, mul(a, y)))
    check('nS=nS0+c*y', nS, add(nS0, mul(c, y)))
    check('c=B*m+F*a', c, add(mul(B, m), mul(F, a)))
    check('nU=nS+nT+m*(d-1)', nU, add(nS, nT, mul(m, sub(d, one))))

    # The new upper bound uses the original strictly positive entry K=s*T-b.
    st = mul(s, t)
    two_u1 = add(scale(u, 2), one)
    M = add(st, mul(two_u1, h), const(-2))
    Q0 = add(scale(mul(B, F, F), -1),
             mul(add(mul(B, add(st, const(-2))), mul(two_u1, h), const(-1)), F),
             mul(B, add(mul(t, x), const(-1))),
             mul(h, sub(s, mul(u, t, x))), const(-1))
    Q1 = add(scale(mul(B, F, F), -1),
             mul(add(mul(B, sub(st, one)), mul(two_u1, h), const(-1)), F),
             scale(mul(B, add(B, one)), -1), mul(s, h), const(-1))
    Q2 = add(scale(mul(F, F), -1), mul(M, F), mul(s, h), const(-3))
    check('Q0=s*n0-b*m', Q0, sub(mul(s, n0), mul(b, m)))
    check('m*K=Q0+s*a*y', sub(mul(s, nT), mul(b, m)), add(Q0, mul(s, a, y)))
    check('Q1-Q0 nonnegative gap', sub(Q1, Q0),
          add(mul(B, add(mul(sub(s, one), x), mul(s, z))), mul(u, h, t, x)))
    check('Q2-Q1 nonnegative gap', sub(Q2, Q1),
          mul(sub(B, one), add(mul(F, add(F, scale(st, -1), one)), B, const(2))))
    check('a upper bound at F=M+1', sub(mul(u, h), add(M, const(2))),
          scale(add(st, mul(add(u, one), h)), -1))
    check('final strict negative upper bound',
          add(scale(add(M, one), -1), mul(s, h), const(-3)),
          scale(add(st, mul(add(s, scale(t, 2), const(-1)), h), const(2)), -1))

    # Recover the new quadratic from the original first residual.
    alpha0 = add(F, mul(t, z))
    H = add(s, mul(t, b))
    A0 = sub(mul(s, alpha0), t)
    L = add(mul(sub(scale(s, 2), one), F), mul(t, b),
            scale(mul(s, t, z), 2), s, scale(t, -2))
    C = add(mul(F, add(mul(b, sub(t, one)), s)), mul(b, b, t), mul(b, s), scale(b, -1))
    C0 = add(scale(mul(H, nS0), -1), mul(A0, n0), scale(mul(b, alpha0, m), -1))
    C1_direct = add(scale(mul(H, c), -1), mul(A0, a), mul(s, u, n0), scale(mul(b, u, m), -1))
    C1 = sub(mul(a, L), C)
    check('alpha=alpha0+u*y', alpha, add(alpha0, mul(u, y)))
    check('linear coefficient=a*L-C', C1_direct, C1)
    check('L positive factorization', L,
          add(mul(sub(scale(s, 2), one), F), mul(t, sub(b, const(2))),
              scale(mul(s, t, z), 2), s))
    check('C positive factorization', C,
          add(mul(F, add(mul(b, sub(t, one)), s)), mul(b, add(mul(b, t), s, const(-1)))))
    residual1 = add(scale(mul(H, nS), -1),
                    mul(sub(mul(s, alpha), t), nT), scale(mul(alpha, b, m), -1))
    quadratic = add(mul(s, u, a, y, y), mul(C1, y), C0)
    check('quadratic equals original first residual times m', residual1, quadratic)

    # Crucial independent restoration of all three original residuals.
    A = sub(mul(s, alpha), t)
    Cold = add(s, mul(u, k))
    Bold = scale(H, -1)
    residual2 = add(scale(mul(Cold, nS), -1), mul(add(A, one), nU),
                    scale(mul(k, add(alpha, one), m), -1))
    residual3 = add(mul(sub(Cold, one), nT), mul(add(Bold, one), nU),
                    scale(mul(sub(b, one), add(k, one), m), -1))
    check('original residual 2 equals residual 1', residual2, residual1)
    check('original residual 3 equals residual 1', residual3, residual1)
    check('single congruence gives integral T numerator',
          add(E, mul(F1, J)), sub(mul(m, E), mul(F1, sub(mul(F, E), J))))

    # Additional unbounded obstruction: s=t and x=y.
    check('symmetric sector E+J identity', add(E, J),
          add(mul(ell, sub(mul(s, y), mul(t, x))), h, scale(j, -1)))
    check('coprimality identity for m and F+1', sub(m, mul(F, F1)), one)
    check('symmetric sector F lower bound identity',
          sub(F, add(B, h, mul(s, sub(d, one)))), sub(mul(t, x), mul(s, y)))
    check('S numerator after E+J=0', sub(sub(nS, mul(m, h)), mul(F1, E)),
          scale(add(E, J), -1))
    check('T numerator after E+J=0', add(sub(nT, mul(m, j)), mul(F, E)),
          mul(F1, add(E, J)))

    # The affine degeneration actually occurs in the permitted parameter range.
    # Its slope remains nonzero: this fixture checks the subtle a=0 branch.
    fixture = dict(s=2, t=1, x=0, y=0, z=1, B=1)
    fixture_values = {name: evaluate(poly, fixture)
                      for name, poly in [('a', a), ('F', F), ('m', m), ('L', L),
                                         ('C', C), ('C0', C0), ('C1', C1)]}
    assert fixture_values == dict(a=0, F=3, m=13, L=15, C=12, C0=-11, C1=-12)

    return dict(
        status='PASS',
        reviewed_claim='Finite necessary-and-sufficient reconstruction of all nonnegative-three-high-D integer models after fixing only the positive low-row integers s,t.',
        imports_primary_verifier=False,
        finite_parameter_scan=False,
        arithmetic='integer sparse polynomial coefficient comparison',
        number_of_identities=len(CHECKS),
        identities=CHECKS,
        required_hypotheses=['s,t>=1', '0<=x<=s-1', 'h=s-x>=1', 'y,z>=0',
                             'B=b-1>=1', 'F=B+(s+t-1)*x+s*z', 'K=s*T-b>0'],
        bound_logic=['Assume F>=M+1 where M=s*t+(2*u+1)*h-2.',
                     'Then a<=-s*t-(u+1)*h<0; y>=0 gives 0<m*K<=Q0.',
                     'Q1-Q0 and Q2-Q1 are nonnegative under these hypotheses.',
                     'Q2<=-F+s*h-3<=-s*t-(s+2*t-1)*h-2<0, a contradiction.'],
        nonzero_polynomial_logic=['s*u>0 and L,C>0.',
                                  'a!=0 gives nonzero quadratic coefficient s*u*a.',
                                  'a=0 gives strictly negative linear coefficient -C.',
                                  'a<=0 makes the polynomial strictly decreasing for Y>=0.'],
        sufficiency_gates=['d=x+y+z>=1', 'alpha>=k>=b+1', 'm divides F*E-J',
                           'S,T,U>0', 'all six canonical sign factors strictly positive',
                           'original residual r1=0, equivalently the new quadratic equals zero'],
        symmetric_sector_obstruction=dict(
            hypotheses=['s=t', 'x=y'],
            steps=['E+J=0 and m divides (F+1)*E imply m divides E.',
                   'Write n=E/m in Z. Then S=h+(F+1)*n and T=h-F*n.',
                   'F=B+h+s*(d-1)>=h+1, so positivity forces n=0.',
                   'E=J=0 is excluded by the existing v21 zero-norm classification.'],
            conclusion='No model in the entire symmetric sector, with no bound on s,t.'),
        affine_degenerate_fixture=dict(parameters=fixture, values=fixture_values,
                                        residual_polynomial='-12*y-11'),
        reviewed_proof_file='high_d_fixed_low_row_finiteness_v22.tex',
        reviewed_proof_sha256=optional_source_hash('high_d_fixed_low_row_finiteness_v22.tex'),
        reviewed_primary_verifier_sha256=optional_source_hash('verify_high_d_low_row_finiteness_v22.py'),
        scope='No conclusion of general nonexistence; s,t remain unbounded.',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('highd_independent_audit_v22.json'))
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('status', 'number_of_identities',
                                                  'finite_parameter_scan')}, ensure_ascii=False))
