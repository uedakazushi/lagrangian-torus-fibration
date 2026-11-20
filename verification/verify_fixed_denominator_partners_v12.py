#!/usr/bin/env python3
"""Complete fixed-denominator partner calculation and exact resonance checks.

There is no upper bound on the other denominator.  For every fixed denominator,
the written factorization theorem reduces all nonresonant possibilities to the
positive divisors of explicitly computed nonzero integers.  The only resonant
branches are proved in the source to be the b=7 and b=13 families.

The reusable partners_for_fixed(n) function returns all finite nonresonant
models and the resonant branches, including their free parameter.  Importing
this module does not run or overwrite the certificate.
"""

from fractions import Fraction
from pathlib import Path
from math import isqrt
import hashlib
import itertools
import json


class Poly:
    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @classmethod
    def variable(cls, name):
        return cls({(name,): 1})

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls({(): int(value)})

    def __add__(self, other):
        terms = self.terms.copy()
        for m, c in self.coerce(other).terms.items():
            terms[m] = terms.get(m, 0) + c
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        terms = {}
        for m, c in self.terms.items():
            for n, d in self.coerce(other).terms.items():
                monomial = tuple(sorted(m + n))
                terms[monomial] = terms.get(monomial, 0) + c * d
        return Poly(terms)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms


def positive_divisors(n):
    if n <= 0:
        raise ValueError('Positive divisors require n>0.')
    low, high = [], []
    for d in range(1, isqrt(n)+1):
        if n % d == 0:
            low.append(d)
            if d*d != n:
                high.append(n//d)
    return low+high[::-1]


def model(a, b, r, s, z):
    assert min(a, b) > 1 and a % 2 == b % 2 == 1
    assert min(r, s, z) > 0
    assert (a-1) % r == (a-1) % s == 0
    assert (b-1) % (r+1) == (b-1) % z == 0
    x, y, S, T = (a-1)//r, (b-1)//(r+1), (a-1)//s, (b-1)//z
    A, B = a+x-s, b-y+z
    assert A*B == a*b-1 and A > 0 and B > 0
    p = [[0, -A, x, -s], [-B, 0, -y, z],
         [r, -r-1, 0, 0], [-S, T, S-T-1, 0]]
    q = [a, b, 1, 1]
    assert all(sum(p[i]) == -q[i] for i in range(4))
    assert all(q[i]*q[j]-p[i][j]*p[j][i] == 1
               for i, j in itertools.combinations(range(4), 2))
    weights = [Fraction(a), Fraction(b),
               Fraction(x)+Fraction(1, 2*r), Fraction(z)+Fraction(1, 2*T)]
    assert all(weights[j]-weights[i]*Fraction(p[i][j], q[i]) > 0
               for i in range(4) for j in range(4) if i != j)
    D = [-q[i]-sum(p[j][i] for j in range(4) if j != i) for i in range(4)]
    return {'a': a, 'b': b, 'r': r, 's': s, 'z': z, 'S': S, 'T': T,
            'd': S-T-1, 'q': q, 'p': p, 'D': D,
            'weights': [str(w) for w in weights]}


def partners_for_fixed(n):
    """All nonresonant models and all resonance branches, without a q bound."""
    if n <= 1 or n % 2 != 1:
        raise ValueError('The fixed denominator must be odd and greater than 1.')
    divs = positive_divisors(n-1)
    models, seeds, resonances = [], [], []

    # Fixed denominator is canonical a.  The C_A=0 branch has no solutions.
    for r, s in itertools.product(divs, repeat=2):
        x = (n-1)//r
        A, M = n+x-s, 1+r*s
        C = (r+1)*(s-x-1)
        seed = {'side': 'A', 'r': r, 's': s, 'C': C, 'trials': []}
        if C == 0:
            assert s == x+1 and s >= 2 and r % s == 0
            t = r//s
            remainder = t*(2*s-1)+1
            assert (r+1)**2 == t*M+remainder and 0 < remainder < M
            seed['zero_branch'] = 'Impossible by the proved strictly positive remainder.'
        else:
            for z in positive_divisors(abs(C)):
                T = Fraction(A*(r+1)-C//z, M)
                trial = {'z': z, 'T': str(T)}
                if T.denominator != 1 or T <= 0:
                    trial['outcome'] = 'T is not a positive integer.'
                else:
                    T = int(T)
                    b = z*T+1
                    if z*T % (r+1):
                        trial['outcome'] = 'r+1 does not divide b-1.'
                    elif b % 2 == 0:
                        trial['outcome'] = 'The other denominator is even.'
                    else:
                        trial['outcome'] = 'accepted'
                        trial['other_denominator'] = b
                        models.append({'fixed_side': 'A', **model(n, b, r, s, z)})
                seed['trials'].append(trial)
        seeds.append(seed)

    # Fixed denominator is canonical b.  C_B=0 is handled separately.
    for rp1 in divs:
        if rp1 == 1:
            continue
        r, y = rp1-1, (n-1)//rp1
        for z in divs:
            B, N = n-y+z, 1+rp1*z
            C = r*(y-z-1)
            seed = {'side': 'B', 'r': r, 'z': z, 'C': C, 'trials': []}
            if C == 0:
                S = Fraction(r*B, N)
                seed['S_at_zero_branch'] = str(S)
                if S.denominator == 1 and S > 0:
                    S = int(S)
                    assert (n, r, z, S) in ((7, 2, 1, 3), (13, 3, 2, 4))
                    branch = {'b': n, 'r': r, 'z': z, 'S': S,
                              'T': (n-1)//z, 'k': 'every integer k>=1',
                              's': '2k' if n == 7 else '3k',
                              'a': '6k+1' if n == 7 else '12k+1'}
                    resonances.append(branch)
                    seed['zero_branch'] = 'A resonance with the recorded free parameter.'
                else:
                    seed['zero_branch'] = 'S is not a positive integer.'
            else:
                for s in positive_divisors(abs(C)):
                    S = Fraction(r*B+C//s, N)
                    trial = {'s': s, 'S': str(S)}
                    if S.denominator != 1 or S <= 0:
                        trial['outcome'] = 'S is not a positive integer.'
                    else:
                        S = int(S)
                        a = s*S+1
                        if s*S % r:
                            trial['outcome'] = 'r does not divide a-1.'
                        elif a % 2 == 0:
                            trial['outcome'] = 'The other denominator is even.'
                        else:
                            trial['outcome'] = 'accepted'
                            trial['other_denominator'] = a
                            models.append({'fixed_side': 'B', **model(a, n, r, s, z)})
                    seed['trials'].append(trial)
            seeds.append(seed)
    models.sort(key=lambda m: (m['a'], m['b'], m['r'], m['s'], m['z']))
    partners = sorted({m['b'] if m['fixed_side'] == 'A' else m['a'] for m in models})
    return {'fixed_denominator': n, 'nonresonant_partners': partners,
            'nonresonant_models': models, 'resonances': resonances,
            'complete_divisor_seeds_and_trials': seeds}


def main():
    identities = []

    def identity(name, left, right):
        if left != right:
            raise AssertionError(name)
        identities.append(name)

    r, s, z, x, y, S, T, t, k = [Poly.variable(n) for n in
                                 ('r', 's', 'z', 'x', 'y', 'S', 'T', 't', 'k')]
    a = r*x+1
    b = z*T+1
    A, M = a+x-s, 1+r*s
    CA = (r+1)*(s-x-1)
    identity('canonical A factorization after clearing r+1',
             A*((r+1)+r*z*T+(r+1)*z)-(r+1)*(a*b-1),
             z*(A*(r+1)-M*T)-CA)
    b = (r+1)*y+1
    a = s*S+1
    B, N = b-y+z, 1+(r+1)*z
    CB = r*(y-z-1)
    identity('canonical B factorization after clearing r',
             (r*a+s*S-r*s)*B-r*(a*b-1), s*(N*S-r*B)-CB)

    M0 = t*s*s+1
    identity('canonical A zero-branch remainder',
             (t*s+1)*(t*s+1)-t*M0, t*(2*s-1)+1)
    identity('canonical A remainder is strictly below M',
             M0-(t*(2*s-1)+1), t*(s-1)*(s-1))
    N0 = t*z*z+1
    C0 = t*(2*z+1)-1
    identity('canonical B zero-branch divisibility',
             (t*z-1)*(t*z-1)-t*N0, -C0)
    u = Poly.variable('u')
    identity('canonical B z>=3 remainder bound with z=u+3',
             t*(u+3)*(u+3)+1-(t*(2*(u+3)+1)-1),
             t*(u*u+4*u+2)+2)
    identity('canonical B z=1 reduces to divisibility of four',
             3*(t+1)-(3*t-1), 4)
    identity('canonical B z=2 lower comparison',
             (5*t-1)-(4*t+1), t-2)
    identity('canonical B z=2 upper comparison',
             2*(4*t+1)-(5*t-1), 3*t+3)

    families = []
    for n, rr, ss, zz, SS, TT, xx, yy, aa, AA, BB in [
        (7, 2, 2*k, 1, 3, 6, 3*k, 2, 6*k+1, 7*k+1, 6),
        (13, 3, 3*k, 2, 4, 6, 4*k, 3, 12*k+1, 13*k+1, 12),
    ]:
        pp = [[0, -AA, xx, -ss], [-BB, 0, -yy, zz],
              [rr, -rr-1, 0, 0], [-SS, TT, SS-TT-1, 0]]
        qs = [aa, n, 1, 1]
        for i in range(4):
            identity(f'b={n} resonance row {i}', sum(pp[i]), -qs[i])
        for i, j in itertools.combinations(range(4), 2):
            identity(f'b={n} resonance crossing {i},{j}',
                     qs[i]*qs[j]-pp[i][j]*pp[j][i], 1)
        assert all(coefficient % 2 == 0 for coefficient in (aa-1).terms.values())
        identity(f'b={n} resonance sS equals a-1', ss*SS, aa-1)
        identity(f'b={n} resonance rx equals a-1', rr*xx, aa-1)
        families.append({'b': n, 'a': '6k+1' if n == 7 else '12k+1',
                         'r': rr, 's': '2k' if n == 7 else '3k',
                         'z': zz, 'S': SS, 'T': TT, 'd': SS-TT-1,
                         'parameter': 'Every integer k>=1.',
                         'verification': 'All rows and crossings are polynomial identities in k; u=-s<0<v=z gives positive weights.'})

    small = {n: partners_for_fixed(n) for n in (3, 5)}
    assert small[3]['nonresonant_partners'] == [7, 11]
    assert small[5]['nonresonant_partners'] == [13, 21, 31, 37]
    assert not small[3]['resonances'] and not small[5]['resonances']
    assert all(m['fixed_side'] == 'A' for result in small.values()
               for m in result['nonresonant_models'])
    expected = {
        (3, 7, 1, 1, 1, 2, 6), (3, 11, 1, 1, 2, 2, 5),
        (5, 13, 1, 1, 1, 4, 12), (5, 21, 1, 1, 2, 4, 10),
        (5, 31, 1, 2, 6, 2, 5), (5, 37, 1, 1, 4, 4, 9),
    }
    actual = {tuple(m[key] for key in ('a', 'b', 'r', 's', 'z', 'S', 'T'))
              for result in small.values() for m in result['nonresonant_models']}
    assert actual == expected
    negative_entries = {n: sorted({-m['s'] for m in small[n]['nonresonant_models']})
                        for n in (3, 5)}
    assert negative_entries == {3: [-1], 5: [-2, -1]}
    assert all(-(n-1) not in entries for n, entries in negative_entries.items())
    # A direct exact sample of each unbounded family, separate from its symbolic proof.
    family_examples = [model(13, 7, 2, 4, 1), model(25, 13, 3, 6, 2)]

    here = Path(__file__).resolve().parent
    candidates = [here/'quintic_fixed_denominator_partners_v12.tex',
                  here.parent/'paper'/'quintic_fixed_denominator_partners_v12.tex']
    source = next((p for p in candidates if p.is_file()), None)
    if source is None:
        raise FileNotFoundError('quintic_fixed_denominator_partners_v12.tex')
    result = {
        'version': 12, 'passed': True,
        'method': 'Exact polynomial coefficient comparison, complete positive-divisor enumeration in both canonical orientations for fixed n=3,5, and Fraction verification of accepted models. No bound on the partner denominator is used.',
        'polynomial_identity_count': len(identities),
        'polynomial_identities': identities,
        'general_written_theorem': 'The fixed odd denominator n>1 has infinitely many odd partners if and only if n is 7 or 13. The resonant families are exactly the two displayed arithmetic progressions; other branches form a finite set.',
        'resonant_families': families,
        'family_exact_examples': family_examples,
        'complete_small_denominator_calculations': small,
        'small_denominator_negative_low_entries': negative_entries,
        'consequence': 'For q=3 or q=5 a two-high endpoint never has the negative low outgoing entry -(q-1); two such endpoints cannot have lambda=-1 at a common low puncture.',
        'proof_dependencies': ['The complete two-high standard form.', 'The equivalence of positivity with u<0<v.'],
        'limitations': [
            'The script checks the algebra and the complete finite calculations; general completeness and resonance exclusion are proved in the TeX source.',
            'For n=7,13 the resonant family is not asserted to exhaust every model or every partner; there are finitely many nonresonant branches as well.',
            'These are local models and their partner relation, not a construction of a global atlas.',
        ],
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output = here/'fixed_denominator_partners_verification_v12.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'passed': True, 'polynomial_identities': len(identities),
                      'partners': {n: r['nonresonant_partners'] for n, r in small.items()},
                      'accepted_small_models': len(actual), 'output': str(output)}))


if __name__ == '__main__':
    main()
