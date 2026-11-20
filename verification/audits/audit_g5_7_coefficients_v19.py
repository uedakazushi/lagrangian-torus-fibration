#!/usr/bin/env python3
"""Exact polynomial-coefficient checks for the G5_7 proof (stdlib only)."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

NAMES = ('h', 't', 'z', 'Q', 'R', 'r', 'k', 'q', 's')
ZERO = (0,)*len(NAMES)


def const(c):
    return {} if c == 0 else {ZERO: Fraction(c)}


def var(name):
    exponents = [0]*len(NAMES)
    exponents[NAMES.index(name)] = 1
    return {tuple(exponents): Fraction(1)}


def add(*terms):
    out = {}
    for term in terms:
        for powers, coefficient in term.items():
            out[powers] = out.get(powers, 0)+coefficient
    return {p: c for p, c in out.items() if c}


def scale(c, p):
    return {e: c*v for e, v in p.items() if c*v}


def mul(*factors):
    out = const(1)
    for factor in factors:
        new = {}
        for a, ca in out.items():
            for b, cb in factor.items():
                powers = tuple(i+j for i, j in zip(a, b))
                new[powers] = new.get(powers, 0)+ca*cb
        out = {p: c for p, c in new.items() if c}
    return out


def sub(a, b):
    return add(a, scale(-1, b))


checks = []

def check(name, p):
    assert not p, (name, p)
    checks.append(name)


h, t, z, Q, R, r, k, q, s = (var(n) for n in NAMES)
one, zero = const(1), {}
M = mul(t, h, add(h, one))
leaf_Q, u, v = add(M, one), mul(t, h), mul(t, add(h, one))
for branch, c, d in (('c', z, zero), ('d', zero, z)):
    V = [[zero, scale(-1, M), scale(-1, add(h, one)), h],
         [const(-1), zero, zero, zero],
         [scale(-1, u), sub(sub(u, one), c), zero, c],
         [v, scale(-1, add(v, one, d)), d, zero]]
    qs = [leaf_Q, one, one, one]
    for i in range(4):
        check(f'leaf_{branch}_row_{i}', add(*V[i], qs[i]))
    for i in range(4):
        for j in range(i+1, 4):
            check(f'leaf_{branch}_pair_{i}{j}', add(mul(V[i][j], V[j][i]),
                                                  scale(-1, mul(qs[i], qs[j])), one))
    expected_D = [scale(-1, add(M, t)), add(M, t, one, c, d),
                  sub(h, d), scale(-1, add(h, one, c))]
    for i in range(4):
        actual = scale(-1, add(qs[i], *(V[j][i] for j in range(4) if j != i)))
        check(f'leaf_{branch}_D_{i}', sub(actual, expected_D[i]))

A = add(one, scale(Fraction(1, 2), s))
B = add(one, scale(Fraction(5, 3), z))
a, b = add(s, one), add(z, one)
check('small_negative_branch_factorization',
      add(scale(6, add(mul(A, B), scale(-1, mul(a, b)), one)),
          mul(sub(s, const(4)), add(z, const(3))), const(6)))

left = add(mul(r, sub(mul(Q, q), one)), mul(R, sub(q, one)),
           scale(-1, mul(k, q, R, r)))
right = sub(mul(add(mul(Q, r), R, scale(-1, mul(k, R, r))), q), add(r, R))
check('central_edge_linear_identity', sub(left, right))

for index, a, b, H, K, expected in (
    (1, Q, scale(Fraction(1, 2), sub(scale(3, Q), const(5))),
     sub(Q, const(2)), scale(Fraction(1, 2), sub(scale(3, Q), one)),
     sub(const(4), scale(2, Q))),
    (2, add(scale(2, Q), one), scale(Fraction(1, 2), sub(Q, one)),
     sub(scale(2, Q), const(2)), scale(Fraction(1, 2), sub(Q, one)),
     sub(const(5), scale(3, Q)))
):
    check(f'D_positive_branch_k_{index}',
          sub(scale(2, add(mul(H, K), scale(-1, mul(a, b)), one)), expected))

result = {'status': 'PASS', 'method': 'Exact multivariate polynomial coefficients over rational numbers, no substitution scan.',
          'identity_count': len(checks), 'identities': checks,
          'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
output = Path(__file__).with_name('g5_7_coefficient_verification_v19.json')
output.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'identities': len(checks), 'output': str(output)}, indent=2))
