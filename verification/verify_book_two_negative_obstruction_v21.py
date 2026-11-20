#!/usr/bin/env python3
"""Exact certificate for the v21 two-negative-branch book obstruction.

The manuscript proves that every book low triangle with exactly two negative
branches contains a negative canonical core with 2 <= w <= 50.  This program
then enumerates every such core and every completion of its two low edges.
It imposes no upper bound on scales, matrix entries, or high denominators.

This implementation imports no earlier verifier or generator.  Local scale
recovery substitutes a prescribed low D into the original high-high pair
equation using rational arithmetic, rather than the earlier integer F formula.
Only Python's standard library is used.
"""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd, isqrt, lcm
from pathlib import Path
import argparse
import hashlib
import json


def divisors(n):
    assert n > 0
    values = set()
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            values.update((d, n // d))
    return sorted(values)


def matrix(pars, order=(0, 1, 3, 4), vertex=2):
    """Reconstruct and independently check all local equations and positivity."""
    r, s, z, S, T = pars
    if min(pars) <= 0 or (s*S) % r or (z*T) % (r+1):
        return None
    L = T-S+1
    if L not in (1, 3, 4):
        return None
    if L == 1:
        if not (2 <= S == T < r):
            return None
    elif not (r < S < r*(L-1)):
        return None
    a, b = s*S+1, z*T+1
    if a % 2 != 1 or b % 2 != 1:
        return None
    x, y = s*S//r, z*T//(r+1)
    U, V = a+x-s, b-y+z
    if min(U, V) <= 0 or U*V != a*b-1:
        return None
    P = ((0, -U, x, -s), (-V, 0, -y, z),
         (r, -r-1, 0, 0), (-S, T, -L, 0))
    q = (a, b, 1, 1)
    assert all(sum(P[i]) == -q[i] for i in range(4))
    assert all(P[i][j]*P[j][i] == q[i]*q[j]-1
               for i in range(4) for j in range(i+1, 4))
    assert {(i, j) for i in range(4) for j in range(4) if P[i][j] > 0} == {
        (0, 2), (2, 0), (1, 3), (3, 1)}
    # Explicit positive weights validate the strict chart inequalities.
    weights = (Fraction(a), Fraction(b), Fraction(2*a-1, 2*r),
               Fraction(2*b-1, 2*T))
    assert all(weights[j]-Fraction(P[i][j], q[i])*weights[i] > 0
               for i in range(4) for j in range(4) if i != j)
    p = {u: {v: P[i][j] for j, v in enumerate(order)}
         for i, u in enumerate(order)}
    qs = dict(zip(order, q))
    D = {u: -qs[u]-sum(p[v][u] for v in order if v != u) for u in order}
    return dict(canonical=tuple(pars), order=tuple(order), vertex=vertex,
                q=qs, p=p, D=D)


def edge_data(left, right):
    i, j = left['vertex'], right['vertex']
    assert left['q'][j] == right['q'][i] == 1
    nodes = tuple(1-left['p'][j][k]-right['p'][i][k]
                  for k in sorted(set(range(5))-{i, j}))
    assert sum(nodes) == 5
    return nodes, left['D'][j]+right['D'][i]


def negative_cores(bound):
    """All scales, via a nonzero positive factorization, for bounded w only."""
    output = []
    reverse_count = 0
    for w in range(2, bound+1):
        for H in range(2, isqrt(2*w*w)+1):
            if not (w*w < 2*H*(H+1) < 4*w*w):
                continue
            reverse_count += 1
            E = 1-Fraction(w*w, H*(H+1))
            M, N = E.numerator, E.denominator
            assert M != 0 and -1 < E < Fraction(1, 2)
            R = N*(N-M)
            for d in divisors(R):
                if (N-d) % M or (R//d-N) % M:
                    continue
                c, e = (N-d)//M, (R//d-N)//M
                if c < 2 or e < 1:
                    continue
                assert E*c*e == e-c+1
                assert N-M*c > 0 and N+M*e > 0
                r = w+H
                if (r*c) % H or ((r+1)*e) % (H+1):
                    continue
                s, z = r*c//H, (r+1)*e//(H+1)
                core = matrix((r, s, z, w, w))
                if core is not None:
                    output.append(core)
    assert len(output) == len({m['canonical'] for m in output})
    return sorted(output, key=lambda m: (m['canonical'][3], m['canonical'])), reverse_count


def reverse_data(row, other_low):
    """Complete reverse data compatible with one fixed low row."""
    if row[0]*row[1] >= 0 or row[other_low] > 0:
        return
    if row[other_low] == 0:
        A = 0 if row[0] > 0 else 1
        B = 1-A
        r = row[A]
        if row[B] != -r-1:
            return
        for w in range(2, r):
            H = r-w
            if H >= 2 and w*w < 2*H*(H+1) < 4*w*w:
                yield r, w, w, A, B, 'C'
        for delta in (2, 3):
            for S in range(r+1, delta*r):
                yield r, S, S+delta, A, B, 'C'
    else:
        A = 0 if row[0] < 0 else 1
        B = 1-A
        S, T = -row[A], row[B]
        L = T-S+1
        if row[other_low] != -L or L not in (1, 3, 4):
            return
        if L == 1:
            w = S
            if w < 2:
                return
            for H in range(2, isqrt(2*w*w)+1):
                if w*w < 2*H*(H+1) < 4*w*w:
                    yield w+H, w, w, A, B, 'D'
        else:
            delta = L-1
            for r in range(S//delta+1, S):
                yield r, S, T, A, B, 'D'


def rational_polynomial_roots(coefficients):
    denominator = lcm(*(a.denominator for a in coefficients))
    A, B, C = (int(a*denominator) for a in coefficients)
    common = gcd(gcd(abs(A), abs(B)), abs(C))
    A, B, C = A//common, B//common, C//common
    assert A != 0
    discriminant = B*B-4*A*C
    if discriminant < 0:
        return ()
    root = isqrt(discriminant)
    if root*root != discriminant:
        return ()
    return tuple(sorted({n//(2*A) for n in (-B-root, -B+root)
                         if n % (2*A) == 0}))


def scales(r, S, T, fixed_type, target_D):
    """Solve the original pair equation after fixing C or D, including resonance."""
    u = S+Fraction(S, r)-1
    v = T-Fraction(T, r+1)+1
    pair_coefficient = u*v-S*T
    # This nonzero fact has a proof in the v19 finite-completion theorem.
    F = (2*r+1)*(S-r)-r*r*(T-S-1)
    assert pair_coefficient == Fraction(F, r*(r+1)) and F != 0
    if fixed_type == 'C':
        gamma = Fraction((r+1)*S, r*T)
        eta = Fraction((r+1)*(target_D-(T-S)), T)
    else:
        gamma, eta = Fraction(1), Fraction(-target_D-1)
    polynomial = (pair_coefficient*gamma,
                  pair_coefficient*eta+(u-S)+(v-T)*gamma,
                  1+(v-T)*eta)
    for s in rational_polynomial_roots(polynomial):
        z = gamma*s+eta
        if s > 0 and z.denominator == 1 and z > 0:
            assert pair_coefficient*s*z+(u-S)*s+(v-T)*z+1 == 0
            yield s, int(z)


def neighbours(fixed, vertex):
    other_low = next(iter({2, 3, 4}-{fixed['vertex'], vertex}))
    labels = (0, 1, other_low)
    found = {}
    count_reverse = 0
    for n0 in range(6):
        for n1 in range(6-n0):
            nodes = (n0, n1, 5-n0-n1)
            row = {k: 1-n-fixed['p'][vertex][k] for k, n in zip(labels, nodes)}
            assert sum(row.values()) == -1
            for r, S, T, A, B, fixed_type in reverse_data(row, other_low):
                count_reverse += 1
                order = ((A, B, fixed['vertex'], other_low) if fixed_type == 'C'
                         else (A, B, other_low, fixed['vertex']))
                for s, z in scales(r, S, T, fixed_type, -fixed['D'][vertex]):
                    other = matrix((r, s, z, S, T), order, vertex)
                    if other is None:
                        continue
                    assert all(other['p'][fixed['vertex']][k] == row[k] for k in labels)
                    ns, residual = edge_data(fixed, other)
                    assert ns == nodes and residual == 0 and min(ns) >= 0
                    found[(other['canonical'], other['order'])] = other
    return list(found.values()), count_reverse


def short_model(core):
    return {key: core[key] for key in ('canonical', 'order', 'vertex', 'q', 'D')}


def analytic_constants():
    """Check the rational arithmetic used in all orientation cases."""
    low, high = Fraction(17, 10), Fraction(17, 7)
    assert Fraction(7, 10)**2 < Fraction(1, 2)
    assert Fraction(10, 7)**2 > 2
    same_L3 = (Fraction(61, 20)-1+3)/(low*low-2)
    same_L4 = (Fraction(61, 20)-2+4)/(low*low-2)
    assert same_L3 == same_L4 == Fraction(505, 89) < 6
    mixed_A = (Fraction(31, 7)+Fraction(7, 4))/(Fraction(3, 2)*low-high)
    mixed_B = (Fraction(39, 10)+2)/(Fraction(3, 2)*low-high)
    mixed_A_L4 = (Fraction(31, 7)+2)/(2*low-high)
    assert mixed_A == Fraction(865, 17) < 51
    assert mixed_B == Fraction(826, 17) < 49
    assert mixed_A_L4 == Fraction(225, 34) < 7
    # If F<0 and h<=3 (delta=2), r>=8 violates r^2<=6r+15.
    assert 8*8 > 6*8+15
    # If F<0 and h<=2 (delta=3), r>=4 violates 2r^2<=4r+10.
    assert 2*4*4 > 4*4+10
    return dict(same_sigma_strict_bound=[505, 89],
                mixed_A_positive_D_strict_bound=[865, 17],
                mixed_B_positive_D_strict_bound=[826, 17],
                mixed_A_L4_positive_D_strict_bound=[225, 34],
                universal_w_max=50)


def run():
    constants = analytic_constants()
    cores, reverse_count = negative_cores(50)
    records, double_nonempty, all_last_pairs, survivors = [], [], [], []
    reverse_total = 0
    for fixed in cores:
        left, count_left = neighbours(fixed, 3)
        right, count_right = neighbours(fixed, 4)
        reverse_total += count_left+count_right
        record = dict(fixed=short_model(fixed),
                      neighbour_counts=[len(left), len(right)],
                      reverse_counts=[count_left, count_right],
                      neighbours_left=[short_model(m) for m in left],
                      neighbours_right=[short_model(m) for m in right])
        records.append(record)
        if left and right:
            double_nonempty.append(record)
        for a, b in product(left, right):
            nodes, residual = edge_data(a, b)
            result = dict(fixed=fixed['canonical'], left=short_model(a),
                          right=short_model(b), final_nodes=nodes,
                          final_D_residual=residual)
            all_last_pairs.append(result)
            if min(nodes) >= 0 and residual == 0:
                survivors.append(result)
    assert len(cores) == 313
    assert len(double_nonempty) == 6
    assert not survivors
    proof_name = 'book_two_negative_obstruction_v21.tex'
    proof_path = next(p for p in (Path(__file__).with_name(proof_name),
                                  Path(__file__).parent.parent/'paper'/proof_name)
                      if p.is_file())
    return dict(
        status='PASS',
        mathematical_scope='No book low triangle with exactly two negative branches; every such triangle has a negative core with 2<=w<=50 by the proved orientation bounds.',
        stronger_finite_statement='No low triangle of any branch pattern contains a negative core with 2<=w<=50.',
        analytic_constants=constants,
        arbitrary_scale_or_denominator_cutoff=None,
        method='Positive factorization for all initial scales; all 21 nonnegative node triples; complete reverse-data enumeration; rational quadratic recovery from the original pair equation and the fixed low D; direct final-edge checks.',
        counts=dict(initial_reverse_parameters=reverse_count, initial_cores=len(cores),
                    by_w=dict(sorted(Counter(c['canonical'][3] for c in cores).items())),
                    with_two_nonempty_neighbour_sets=len(double_nonempty),
                    neighbour_reverse_parameters=reverse_total,
                    final_edge_pairs=len(all_last_pairs), survivors=len(survivors)),
        maximum_initial_high_denominator=max(max(m['q'].values()) for m in cores),
        initial_core_records=records,
        double_nonempty_records=double_nonempty,
        final_edge_certificates=all_last_pairs,
        proof_file=proof_name,
        proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('book_two_negative_obstruction_verification_v21.json'))
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'counts', 'analytic_constants',
                                           'maximum_initial_high_denominator')}, ensure_ascii=False))
