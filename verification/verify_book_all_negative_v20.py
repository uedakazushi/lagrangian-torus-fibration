#!/usr/bin/env python3
"""Complete exclusion of an all-negative book low triangle.

The reverse-parameter bounds are proved in the accompanying manuscript:
w1 <= 16, w3 <= 17, w2 <= 40 after orientation normalization (++-).
These are mathematical bounds, not exploratory cutoffs.  For each reverse
parameter, every scale is recovered by a finite nonzero factorization; no
upper bound is imposed on scales or high denominators.

This verifier imports no earlier generator.  It reconstructs all local
matrices, node numbers and opposing D residuals from the defining equations.
"""

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json


def positive_divisors(n):
    assert n > 0
    result = set()
    for d in range(1, isqrt(n)+1):
        if n % d == 0:
            result.update((d, n//d))
    return sorted(result)


def negative_bound(w, H):
    return w >= 2 and H >= 2 and w*w < 2*H*(H+1) < 4*w*w


@lru_cache(None)
def all_scales(w, H):
    """All positive integral odd-denominator canonical negative models."""
    assert negative_bound(w, H)
    r = w+H
    E = 1-Fraction(w*w, H*(H+1))
    M, N = E.numerator, E.denominator
    assert -1 < E < Fraction(1, 2) and M != 0
    out = []
    for d in positive_divisors(N*(N-M)):
        cn = N-d
        en = N*(N-M)//d-N
        if cn % M or en % M:
            continue
        c, e = cn//M, en//M
        if c < 2 or e < 1:
            continue
        assert E*c*e == e-c+1
        if (r*c) % H or ((r+1)*e) % (H+1):
            continue
        s, z = r*c//H, (r+1)*e//(H+1)
        if (s*w) % 2 or (z*w) % 2:
            continue
        out.append((r, s, z, w, w))
    assert len(out) == len(set(out))
    return tuple(sorted(out))


def matrix(parameters, order, vertex):
    r, s, z, w, T = parameters
    assert T == w and 0 < w < r
    assert (s*w) % r == 0 and (z*w) % (r+1) == 0
    a, b = s*w+1, z*w+1
    x, y = s*w//r, z*w//(r+1)
    U, V = a+x-s, b-y+z
    assert min(a, b) > 1 and a % 2 == b % 2 == 1
    assert min(U, V) > 0
    P = ((0, -U, x, -s), (-V, 0, -y, z),
         (r, -r-1, 0, 0), (-w, w, -1, 0))
    q = (a, b, 1, 1)
    assert all(sum(P[i]) == -q[i] for i in range(4))
    assert all(P[i][j]*P[j][i] == q[i]*q[j]-1
               for i in range(4) for j in range(i+1, 4))
    assert {(i, j) for i in range(4) for j in range(4) if P[i][j] > 0} == {
        (0, 2), (2, 0), (1, 3), (3, 1)}
    weights = (Fraction(a), Fraction(b),
               Fraction(2*(a-1)+1, 2*r), Fraction(2*z*w+1, 2*w))
    assert all(weights[j]-Fraction(P[i][j], q[i])*weights[i] > 0
               for i in range(4) for j in range(4) if i != j)
    p = {u: {v: P[i][j] for j, v in enumerate(order)}
         for i, u in enumerate(order)}
    qs = dict(zip(order, q))
    D = {u: -qs[u]-sum(p[v][u] for v in order if v != u) for u in order}
    return {'vertex': vertex, 'canonical': parameters, 'order': order, 'p': p, 'q': qs, 'D': D}


def edge(left, right):
    i, j = left['vertex'], right['vertex']
    assert left['q'][j] == right['q'][i] == 1
    nodes = [1-left['p'][j][k]-right['p'][i][k]
             for k in sorted(set(range(5))-{i, j})]
    assert sum(nodes) == 5
    return nodes, left['D'][j]+right['D'][i]


def run():
    # The strict rational estimates prove w1 < 5235/323 < 17.
    lower_slope = Fraction(17, 10)**2
    upper_slope = Fraction(17, 7)
    lower_constant = Fraction(101, 20)
    analytic_bound = (lower_constant+upper_slope)/(lower_slope-upper_slope)
    assert analytic_bound == Fraction(5235, 323) < 17
    assert Fraction(17, 7)*16+2 < 41

    reverse_records = []
    triples = []
    first_pairs = {}
    nonempty_reverse_count = 0
    for w1 in range(2, 17):
        for H1 in range(2, isqrt(2*w1*w1)+1):
            if not negative_bound(w1, H1):
                continue
            r1 = w1+H1
            for t1, t2, t3 in product(range(-1, 2), range(-1, 3), range(-2, 3)):
                w2, w3 = r1+t2, w1-t1
                if min(w2, w3) < 2:
                    continue
                assert w2 <= 40 and w3 <= 17
                for H2 in range(2, isqrt(2*w2*w2)+1):
                    if not negative_bound(w2, H2):
                        continue
                    H3 = w2+H2+t3-w3
                    if not negative_bound(w3, H3):
                        continue
                    pars = ((w1, H1), (w2, H2), (w3, H3))
                    lists = [all_scales(*p) for p in pars]
                    record = {'reverse_w_H': pars, 'node_offsets_t1_t2_t3': (t1, t2, t3),
                              'scale_lists': lists}
                    reverse_records.append(record)
                    if not all(lists):
                        continue
                    nonempty_reverse_count += 1
                    for canonical in product(*lists):
                        models = [matrix(p, order, vertex) for p, order, vertex in zip(
                            canonical, ((0, 1, 3, 4), (0, 1, 4, 2), (1, 0, 3, 2)), (2, 3, 4))]
                        checks = [edge(models[i], models[(i+1) % 3]) for i in range(3)]
                        assert all(min(n) >= 0 for n, _ in checks)
                        residuals = [d for _, d in checks]
                        # Already the (++ ) low edge contradicts D cancellation.
                        assert residuals[0] != 0
                        first_pairs[canonical[:2]] = residuals[0]
                        triples.append({'canonical_models': canonical,
                                        'node_numbers': [n for n, _ in checks],
                                        'D_residuals': residuals})
    assert len(reverse_records) == 91
    assert nonempty_reverse_count == 25
    assert len(triples) == 64
    assert len(first_pairs) == 26
    compressed = defaultdict(set)
    for (first, second), residual in first_pairs.items():
        compressed[first].add(residual)
    assert len(compressed) == 5
    assert all(0 not in values for values in compressed.values())
    return {
        'status': 'PASS',
        'mathematical_scope': 'No all-negative book low triangle under positive integral local charts, odd high denominators, nonnegative low nodes and opposite low-D cancellation.',
        'normalization': 'The nonconstant high orientation is (++-) after high-ray exchange and cyclic relabelling; constant orientation was already excluded by node inequalities.',
        'proved_bounds': {'w1_strict_rational_bound': [5235, 323], 'w1_max': 16, 'w2_max': 40, 'w3_max': 17},
        'scale_or_denominator_cutoff': None,
        'complete_scale_factorization': '(N-Mc)(N+Me)=N(N-M)>0; all positive divisors, E=M/N!=0; c=sH/r, e=z(H+1)/(r+1).',
        'counts': {'node_reverse_types': 91, 'types_with_all_three_local_scale_sets_nonempty': 25,
                   'local_scale_triples': 64, 'distinct_first_edge_scale_pairs': 26,
                   'first_edge_nonzero_residuals': 64, 'survivors': 0},
        'reverse_records': reverse_records,
        'D_certificates': triples,
        'distinct_first_edge_certificates': [{'first': first, 'second': second, 'D_residual': d}
                                           for (first, second), d in sorted(first_pairs.items())],
        'compressed_first_core_table': [{'canonical': first, 'nonzero_D_residual_set': sorted(values)}
                                       for first, values in sorted(compressed.items())],
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'generator_imported': False,
        'limitations': ['This theorem does not exclude mixed positive/negative book triples.',
                        'No high-center completion or global geometric classification is claimed.']
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    out = args.output or Path(__file__).with_name('book_all_negative_verification_v20.json')
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status', 'proved_bounds', 'counts', 'scale_or_denominator_cutoff']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
