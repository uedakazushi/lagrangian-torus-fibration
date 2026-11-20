#!/usr/bin/env python3
"""Exact finite certificates for the meridian blow-up calculations.

Only standard-library modules are used. These computations verify integral
matrix reductions, root-lattice pairings and Koszul identities. The homotopy
pushout, marked arrangement model, duality, and JSJ proofs are in the paper;
they are not replaced by the finite checks below.
"""
from fractions import Fraction
from itertools import combinations
from math import comb, prod
from pathlib import Path
import hashlib
import json


def matmul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(a):
    return list(map(list, zip(*a)))


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def determinant(a):
    if not a:
        return 1
    b = [list(map(Fraction, row)) for row in a]
    answer = Fraction(1)
    for j in range(len(b)):
        pivot = next((i for i in range(j, len(b)) if b[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            b[pivot], b[j] = b[j], b[pivot]
            answer = -answer
        x = b[j][j]
        answer *= x
        for i in range(j+1, len(b)):
            c = b[i][j]/x
            for k in range(j+1, len(b)):
                b[i][k] -= c*b[j][k]
            b[i][j] = 0
    assert answer.denominator == 1
    return answer.numerator


def rank(a):
    if not a:
        return 0
    b = [list(map(Fraction, row)) for row in a]
    r = 0
    for j in range(len(b[0])):
        p = next((i for i in range(r, len(b)) if b[i][j]), None)
        if p is None:
            continue
        b[r], b[p] = b[p], b[r]
        v = b[r][j]
        b[r] = [x/v for x in b[r]]
        for i in range(len(b)):
            if i != r:
                v = b[i][j]
                b[i] = [x-v*y for x, y in zip(b[i], b[r])]
        r += 1
        if r == len(b):
            break
    return r


def compositions(total, slots):
    if slots == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first, slots-1):
                yield (first,)+rest


checks = 0


def verify_distribution(rs, full=False):
    global checks
    m, r = len(rs), sum(rs)
    assert m >= 4 and 0 in rs
    s = sum(x > 0 for x in rs)
    k = m-1-s
    q = [[1-(rs[i] if i == j else 0) for j in range(m)] for i in range(m)]
    j = rs.index(0)
    left, right = identity(m), identity(m)
    for i in range(m):
        if i != j:
            left[i][j] = -1
            right[j][i] = -1
    d = matmul(matmul(left, q), right)
    expected = [[(1 if i == j else -rs[i]) if i == h else 0
                 for h in range(m)] for i in range(m)]
    assert d == expected
    assert determinant(left) == determinant(right) == 1
    checks += 3
    if full:
        # Ambient H,E basis; divisor rows evaluate intersection with each D_i.
        offsets = []
        for a, count in enumerate(rs):
            offsets.extend([a]*count)
        intersection = [[1]+[int(owner == i) for owner in offsets] for i in range(m)]
        root_columns = []
        cursor = 1
        for count in rs:
            for h in range(count-1):
                v = [0]*(r+1)
                v[cursor+h], v[cursor+h+1] = 1, -1
                root_columns.append(v)
            cursor += count
        if root_columns:
            root_basis = transpose(root_columns)
            assert matmul(intersection, root_basis) == [[0]*(r-s) for _ in range(m)]
            assert rank(intersection) == s+1
            assert rank(root_basis) == r-s
            gram = [[v[0]*w[0]-sum(x*y for x,y in zip(v[1:],w[1:]))
                     for w in root_columns] for v in root_columns]
            expected_gram = [[0]*(r-s) for _ in range(r-s)]
            cursor = 0
            for count in rs:
                for h in range(count-1):
                    expected_gram[cursor+h][cursor+h] = -2
                    if h+1 < count-1:
                        expected_gram[cursor+h][cursor+h+1] = 1
                        expected_gram[cursor+h+1][cursor+h] = 1
                cursor += max(count-1, 0)
            assert gram == expected_gram
            assert abs(determinant(gram)) == prod(x for x in rs if x)
            checks += 5
    t = comb(m-1, 2)-comb(k, 2)+r-s
    b2 = comb(k, 2)+t
    assert b2 == comb(m-1, 2)+r-s
    assert 1-k+b2 == comb(m-2, 2)+r
    checks += 2
    return {
        "m": m, "blowups_per_line": list(rs), "pi1_rank": k,
        "sphere_summands": t, "b2": b2,
        "intersection_radical_rank": comb(m-1,2),
        "signature": -(r-s),
        "boundary_free_rank": comb(m-1,2)+k,
        "boundary_torsion_cyclic_orders": [x for x in rs if x > 1]
    }


small_cases = 0
for m in range(4, 10):
    for r in range(6):
        for rs in compositions(r, m):
            if 0 in rs:
                verify_distribution(rs, full=(r > 0))
                small_cases += 1

canonical = []
for m in range(5, 13):
    s, r, pants = m-4, comb(m-3,2), (m-3)**2
    # Two extreme allocations plus a cyclically permuted balanced allocation.
    balanced = [r//s + int(i < r % s) for i in range(s)] + [0]*(m-s)
    concentrated = [r-s+1]+[1]*(s-1)+[0]*(m-s)
    for rs in {tuple(balanced), tuple(concentrated), tuple(balanced[-1:]+balanced[:-1])}:
        case = verify_distribution(rs, full=True)
        assert case["sphere_summands"] == pants-1
        assert case["signature"] == -comb(m-4,2)
        assert case["pi1_rank"] == 3
        case["pants_budget"] = pants
        case["pi2_free_group_ring_rank"] = pants
        canonical.append(case)
        checks += 3

# Polynomial arithmetic in Z[a,b,c], where a=x1-1 etc. Check d2*d3=0
# coefficientwise, without specializing variables.
zero = {}
a,b,c = ({(1,0,0):1},{(0,1,0):1},{(0,0,1):1})
def neg(p):
    return {m:-v for m,v in p.items()}
def add(p,q):
    out = dict(p)
    for m,v in q.items():
        out[m] = out.get(m,0)+v
        if out[m] == 0:
            del out[m]
    return out
def multiply(p,q):
    out = {}
    for m,v in p.items():
        for n,w in q.items():
            degree = tuple(x+y for x,y in zip(m,n))
            out[degree] = out.get(degree,0)+v*w
    return {m:v for m,v in out.items() if v}
d2poly = [[neg(b),neg(c),zero],[a,zero,neg(c)],[zero,a,b]]
d3poly = [c,neg(b),a]
for row in d2poly:
    value = {}
    for p,q in zip(row,d3poly):
        value = add(value,multiply(p,q))
    assert not value
    checks += 1

twisted = []
for character in [(1,1,1),(2,1,1),(1,3,1),(1,1,-1),(2,3,5),(-1,-1,-1)]:
    av,bv,cv = (x-1 for x in character)
    d1 = [[av,bv,cv]]
    d2 = [[-bv,-cv,0],[av,0,-cv],[0,av,bv]]
    h0 = 1-rank(d1)
    h1 = 3-rank(d1)-rank(d2)
    h2 = 6-rank(d2)  # three torus 2-cells and three sphere cells
    assert (h0,h1,h2) == ((1,3,6) if character==(1,1,1) else (0,0,4))
    twisted.append({"character":character,"homology_dimensions":[h0,h1,h2]})
    checks += 1

sextic_one_node = verify_distribution((1,0,0,0,0),full=True)
report = {
    "version":8,
    "status":"passed",
    "scope":"Finite exact certificates; geometric and homotopy proofs are in the manuscript.",
    "small_distribution_cases":small_cases,
    "canonical_budget_cases":len(canonical),
    "exact_checks":checks,
    "sextic_one_node":sextic_one_node,
    "canonical_examples":canonical,
    "rank_one_local_system_samples":twisted,
    "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
}
destination = Path(__file__).with_name("meridian_topology_v8_results.json")
destination.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:report[k] for k in ["status","small_distribution_cases","canonical_budget_cases","exact_checks"]}))
