#!/usr/bin/env python3
"""G5_7 obstruction: a proof-derived finite table, with no cutoff on c/d or q.

Dependencies are the analytic placement theorem in g5_7_obstruction_v19.tex,
three-high positive matching, the two-high low-row sign theorem, and the
one-high full normal form.  Vertex 0 is the leaf hub, vertex 4 the leaf;
1,2,3 are the leaf-normal-form labels B,C,D.  The missing diamond edge is
0m, m in {1,2,3}; every edge among 1,2,3 is high.

The free leaf coefficient is represented by exact points and complete
parity half-lines.  A degenerate central-edge equation represents the
ENTIRE progression q=1+step*n, n>=1.  Leaf-edge D cancellation then gives
its unique possible rational value.  No other denominator is truncated.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import lcm
from pathlib import Path
import argparse
import hashlib
import json

I = tuple(range(4))
LOW = (1, 2, 3)
NODE_ROWS = {}
for i in I:
    NODE_ROWS[i] = []
    for abc in product(range(6), repeat=3):
        if sum(abc) != 5:
            continue
        row = [0] * 4
        for j, value in zip((j for j in I if j != i), abc):
            row[j] = value
        NODE_ROWS[i].append(tuple(row))


def placement_allowed(m, h, t, N0):
    """Exactly the four rows of the analytically proved placement table."""
    Q = t*h*(h+1)+1
    if m == 1:
        return N0[1] == 2 and Q <= 5
    if m == 2:
        return (N0[2] == 1 and t*h <= 4) or (N0[2] == 2 and h == t == 1)
    return N0[3] == 1 and t*(h+1) <= 4


def central_high_pair(Q, R, r):
    """Solve q*(Q*r+R-kappa*R*r)=R+r for ALL odd q>=3."""
    if R == 0 or r == 0:
        return []
    out = []
    for kappa in range(-4, 2):
        a, b = Q*r+R-kappa*R*r, R+r
        if a == 0:
            if b == 0:
                # Then r=-R and Q-1=-kappa*r.  Both divisibilities
                # reduce to r | q-1; oddness gives the lcm below.
                assert r == -R and Q-1 == -kappa*r
                out.append({'kind': 'progression', 'step': lcm(2, abs(r)), 'kappa': kappa})
        elif b % a == 0:
            q = b//a
            if q >= 3 and q % 2 == 1 and (q-1) % r == 0 and (Q*q-1) % R == 0:
                out.append({'kind': 'fixed', 'q': q, 'kappa': kappa})
    return out


def central_low_pair(Q, R, r):
    """q=1; both low-to-low entries at the two-high core are nonpositive."""
    if R == 0 or r > 0 or (Q-1) % R:
        return []
    x = (Q-1)//R
    out = []
    for kappa in range(-4, 2):
        y = kappa-x
        if y <= 0 and r*y == 0:
            out.append({'kind': 'low', 'q': 1, 'kappa': kappa, 'X0m': x, 'Xm0': y})
    return out


def common_low_ok(r, s):
    return bool(r and s and (r == -s or (r*s > 0 and min(abs(r), abs(s)) == 1 and max(abs(r), abs(s)) % 2 == 0)))


def partner_types(r, a, b):
    """All z with s=a*z+b a common-low partner of r (a is +/-1).

    Tuples: (lower, upper, parity, sign(s), description).
    None is an unbounded endpoint, or absence of a parity condition.
    """
    assert a in (-1, 1)
    if r == 0:
        return []
    sg = 1 if r > 0 else -1
    values = [-r]
    if abs(r) % 2 == 0:
        values.append(sg)
    out = []
    for s in values:
        z = (s-b)*a
        out.append((z, z, None, 1 if s > 0 else -1, 'point'))
    if abs(r) == 1:
        coefficient, threshold = a*sg, 2-sg*b
        lo = threshold if coefficient == 1 else None
        hi = -threshold if coefficient == -1 else None
        out.append((lo, hi, b % 2, sg, 'halfline'))
    return out


def intersection(x, y):
    lowers = [v for v in (x[0], y[0]) if v is not None]
    uppers = [v for v in (x[1], y[1]) if v is not None]
    lo, hi = max(lowers) if lowers else None, min(uppers) if uppers else None
    parities = [v for v in (x[2], y[2]) if v is not None]
    if len(set(parities)) > 1:
        return None
    parity = parities[0] if parities else None
    if parity is not None:
        if lo is not None:
            lo += (parity-lo) % 2
        if hi is not None:
            hi -= (hi-parity) % 2
    if lo is not None and hi is not None and lo > hi:
        return None
    return (lo, hi, parity)


def rational_pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def hub_obstruction(Q, t, m, R0, center):
    """Use sum_i (Q*q_i-1)/R0_i = 1-2Q-t, with q_m=1."""
    target = 1-2*Q-t
    qs = {m: 1}
    unknown = []
    for i in LOW:
        if i == m:
            continue
        if center[i-1]['kind'] == 'fixed':
            qs[i] = center[i-1]['q']
        else:
            assert center[i-1]['kind'] == 'progression'
            unknown.append(i)
    # This is an exhaustive output property of the finite preceding table;
    # it is not imposed as an extra mathematical hypothesis.
    assert len(unknown) <= 1
    if unknown:
        i = unknown[0]
        fixed_sum = sum(Fraction(Q*q-1, R0[j]) for j, q in qs.items())
        q = ((target-fixed_sum)*R0[i]+1)/Q
        step = center[i-1]['step']
        valid = q.denominator == 1 and q >= 3 and (q-1) % step == 0
        return {'reason': 'progression_forced_below_three' if q < 3 else 'progression_integrality_failure',
                'variable': i, 'forced_q': rational_pair(q), 'step': step,
                'target': target, 'valid': valid}
    total = sum(Fraction(Q*q-1, R0[i]) for i, q in qs.items())
    return {'reason': 'nonzero_hub_D_residual', 'total': rational_pair(total),
            'target': target, 'residual': rational_pair(total-target), 'valid': total == target}


def run():
    counts, parameters, survivors, certificates = Counter(), [], [], []
    summary = {}
    for m in LOW:
        for h in range(1, 5):  # h(h+1)+1<=21 implies h<=4, analytically.
            for t in range(1, 20//(h*(h+1))+1):
                Q, u, v = t*h*(h+1)+1, t*h, t*(h+1)
                before = counts.copy()
                V = [[0, 1-Q, -h-1, h], [-1, 0, 0, 0],
                     [-u, u-1, 0, 0], [v, -v-1, 0, 0]]
                for variable in (2, 3):
                    # c=z,d=0 for row C, or c=0,d=z for row D.
                    j, k = (1, 3) if variable == 2 else (1, 2)
                    fixed = [i for i in LOW if i != variable]
                    for N0 in NODE_ROWS[0]:
                        if not placement_allowed(m, h, t, N0):
                            continue
                        R0 = [0]+[Q*(1-N0[i])-V[0][i] for i in LOW]
                        if any(R0[i] == 0 for i in LOW) or sum(x > 0 for x in R0) != 1:
                            continue
                        choices = {}
                        for i in LOW:
                            arr = []
                            for Ni in NODE_ROWS[i]:
                                Ri = tuple(0 if z == i else 1-Ni[z]-V[i][z] for z in I)
                                cp = (central_low_pair if i == m else central_high_pair)(Q, R0[i], Ri[0])
                                if not cp:
                                    continue
                                if i != variable:
                                    required = [z for z in I if z != i and (i != m or z != 0)]
                                    if any(Ri[z] == 0 for z in required) or sum(Ri[z] > 0 for z in I if z != i) != 1:
                                        continue
                                arr.append((Ni, Ri, cp))
                            choices[i] = arr
                        if any(not choices[i] for i in LOW):
                            continue
                        for combo in product(*(choices[i] for i in LOW)):
                            R = [R0]+[combo[i-1][1] for i in LOW]
                            f, g = fixed
                            if not common_low_ok(R[f][g], R[g][f]):
                                continue
                            counts['fixed_node_configurations'] += 1
                            for x, y in product(partner_types(R[j][variable], 1, R[variable][j]),
                                                partner_types(R[k][variable], -1, R[variable][k])):
                                counts['partner_type_pairs'] += 1
                                if int(R[variable][0] > 0)+int(x[3] > 0)+int(y[3] > 0) != 1:
                                    counts['matching_rejections'] += 1
                                    continue
                                counts['matching_type_pairs'] += 1
                                typ = intersection(x, y)
                                if typ is None:
                                    counts['empty_intersections'] += 1
                                    continue
                                counts['nonempty_partner_types'] += 1
                                record = {'m': m, 'h': h, 't': t, 'Q': Q, 'variable_row': variable,
                                          'N': [N0]+[combo[i-1][0] for i in LOW], 'R_at_zero': R,
                                          'partner_types': [x, y], 'intersection': typ,
                                          'center_options': [combo[i-1][2] for i in LOW]}
                                survivors.append(record)
                                for center in product(*(combo[i-1][2] for i in LOW)):
                                    counts['center_types'] += 1
                                    result = hub_obstruction(Q, t, m, R0, center)
                                    assert not result['valid'], (record, center, result)
                                    counts['hub_D_rejections'] += 1
                                    certificates.append({'partner_record': len(survivors)-1,
                                                         'center': center, 'obstruction': result})
                                    descriptor = tuple(c.get('q', 'z') for c in center)
                                    key = (m, h, t, tuple(R0[1:]), descriptor)
                                    if key not in summary:
                                        summary[key] = {'m': m, 'h': h, 't': t, 'Q': Q, 'R0': R0[1:],
                                                        'q0_BCD': descriptor, 'obstruction': result, 'multiplicity': 0}
                                    else:
                                        assert summary[key]['obstruction'] == result
                                    summary[key]['multiplicity'] += 1
                parameters.append({'m': m, 'h': h, 't': t, 'Q': Q, 'counts': dict(counts-before)})
    return {'status': 'PASS', 'quantification': 'All positive integers h,t in the proved Q<=21 table; all nonnegative node rows of sum five; c=0 or d=0 with the other coefficient over ALL integers; every remaining high denominator is fixed or a COMPLETE congruence progression.',
            'counts': dict(counts), 'by_parameter': parameters,
            'partner_records': survivors, 'hub_D_certificates': certificates,
            'hub_summary': list(summary.values()), 'survivors': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('g5_7_obstruction_verification_v19.json'))
    args = parser.parse_args()
    assert all(len(rows) == 21 for rows in NODE_ROWS.values())
    result = run()
    assert len(result['by_parameter']) == 45
    assert result['counts'] == {'fixed_node_configurations': 529, 'partner_type_pairs': 1988,
                               'matching_type_pairs': 910, 'empty_intersections': 750,
                               'matching_rejections': 1078, 'nonempty_partner_types': 160,
                               'center_types': 212, 'hub_D_rejections': 212}
    assert len(result['hub_summary']) == 13
    assert len(result['partner_records']) == 160
    assert len(result['hub_D_certificates']) == 212
    assert not result['survivors']
    result['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['count_scope'] = 'Branch-labelled node/partner choices, not chart isomorphism classes; c=d=0 occurs in both free-coefficient branches.'
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'counts': result['counts'], 'summary_rows': 13,
                      'survivors': 0, 'output': str(args.output)}, ensure_ascii=False, indent=2))
