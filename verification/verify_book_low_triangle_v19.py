#!/usr/bin/env python3
"""Independent exact checks for the book low-triangle reduction.

The bounded catalog comparison verifies the implementation, not the theorem's
unbounded quantifier. The latter is proved in the accompanying TeX file.
"""
from fractions import Fraction
from itertools import permutations, product
from math import isqrt
from pathlib import Path
import json
import sys
import hashlib
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'research'))
import book_low_triangle_completion_v19 as book


def sd(n):
    values = set()
    for d in range(1, isqrt(n)+1):
        if n % d == 0:
            values.update((d, -d, n//d, -n//d))
    return sorted(values)


def independent_models(a, b, vertex):
    # Direct signed divisors, with high rays in positions 0 and 3. No use of
    # the canonical parametrization or the finite-completion algorithm.
    q = (a, 1, 1, b)
    N = [[q[i]*q[j]-1 for j in range(4)] for i in range(4)]
    order = (0,) + tuple(sorted({2, 3, 4}-{vertex})) + (1,)
    for ab in sd(N[0][1]):
        ba = N[0][1]//ab
        for ac in sd(N[0][2]):
            ca = N[0][2]//ac
            ad = -q[0]-ab-ac
            if not ad or N[0][3] % ad:
                continue
            da = N[0][3]//ad
            for bd in sd(N[1][3]):
                db = N[1][3]//bd
                dc = -q[3]-da-db
                if not dc or N[2][3] % dc:
                    continue
                cd = N[2][3]//dc
                bc = -q[1]-ba-bd
                cb = -q[2]-ca-cd
                if bc*cb != N[1][2]:
                    continue
                P = ((0,ab,ac,ad),(ba,0,bc,bd),(ca,cb,0,cd),(da,db,dc,0))
                positive = True
                for length in (2,3,4):
                    for cyc in permutations(range(4), length):
                        if cyc[0] != min(cyc):
                            continue
                        gain = Fraction(1)
                        for i,j in zip(cyc,cyc[1:]+cyc[:1]):
                            if P[i][j] <= 0:
                                break
                            gain *= Fraction(P[i][j],q[i])
                        else:
                            if gain >= 1:
                                positive = False
                if not positive:
                    continue
                p = {i:{j:P[ii][jj] for jj,j in enumerate(order)}
                     for ii,i in enumerate(order)}
                qs = dict(zip(order,q))
                D = {i:-qs[i]-sum(p[j][i] for j in order if j!=i) for i in order}
                yield dict(vertex=vertex,q=qs,p=p,D=D)


checks = 0


def check(statement):
    global checks
    checks += 1
    assert statement


# Coefficient identity of the determinant, checked as an exact polynomial in
# s,z via its four coefficients for an independent grid of reverse parameters.
for r,S,T in product(range(1,12), range(1,15), range(1,15)):
    h,delta = S-r,T-S
    F = (2*r+1)*h-r*r*(delta-1)
    A,B,C = h*(r+1),-r*(h+delta-1),r*(r+1)
    ur,vr = Fraction((r+1)*S-r,r),Fraction(r*T+r+1,r+1)
    computed = (r*(r+1),r*(r+1)*(ur-S),r*(r+1)*(vr-T),r*(r+1)*(ur*vr-S*T))
    check(computed == (C,A,B,F))
    if delta in (0,2,3):
        check(F != 0)

# The 7 and 13 resonance lines retain all of their positive integral scale
# parameters when the appropriate fixed D value is specified.
resonance_checks = []
for r,S,T,z,step in ((2,3,6,1,2),(3,4,6,2,3)):
    for k in (1,2,3,10,101):
        s=step*k
        model=book.canonical(r,s,z,S,T)
        check(model is not None)
        for low_type,ray in (('C',3),('D',4)):
            solutions=list(book.scales_from_low_D(r,S,T,low_type,model['D'][ray]))
            check((s,z) in solutions)
            check(len(solutions)<=2)
        resonance_checks.append(dict(canonical=model['canonical'],q=model['q']))

# Complete independent signed-divisor catalogs at all odd a,b <= 21.
bound=21
catalog = {v:[] for v in (2,3,4)}
for a,b in product(range(3,bound+1,2),repeat=2):
    for v in catalog:
        catalog[v].extend(independent_models(a,b,v))

first = {book.key(m):m for m in catalog[2]}
# Include fixed models with denominators well outside the independent catalog,
# and examples from both resonance lines.
for m in book.negative_models(15):
    first[book.key(m)]=m
for values in ((2,2,1,3,6),(2,20,1,3,6),(3,3,2,4,6),(3,30,2,4,6)):
    m=book.canonical(*values)
    first[book.key(m)]=m

comparisons=0
for fixed in first.values():
    low_entries=[fixed['p'][i][j] for i in (3,4) for j in (3,4) if i!=j]
    if min(low_entries)<-4:
        continue
    for vertex in (3,4):
        lows=sorted({2,3,4}-{vertex})
        expected={book.key(m) for m in catalog[vertex]
                  if book.low_edge(fixed,m) is not None
                  and min(m['p'][lows[0]][lows[1]],m['p'][lows[1]][lows[0]])>=-4}
        actual={book.key(m) for m in book.neighbours(fixed,vertex)
                if m['q'][0]<=bound and m['q'][1]<=bound}
        check(expected==actual)
        comparisons+=1

# Known seven negative canonical models for w<=4 (a prior complete classification).
small=[m['canonical'] for m in book.negative_models(4)]
check(set(small)=={(4,4,5,2,2),(5,10,2,3,3),(6,6,14,3,3),
                   (7,7,2,4,4),(7,21,4,4,4),(8,6,9,4,4),(8,8,27,4,4)})
for m in book.negative_models(4):
    check(not book.completions(m))

result=dict(status='PASS',exact_checks=checks,
            script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            helper_sha256=hashlib.sha256(Path(book.__file__).read_bytes()).hexdigest(),
            independent_catalog_bound=bound,
            independent_positive_models={v:len(c) for v,c in catalog.items()},
            fixed_core_edge_comparisons=comparisons,
            resonance_tests=resonance_checks,
            mathematical_scope='unbounded finite completion for each fixed core; no global book exclusion',
            bounded_verification_scope='independent odd denominators <=21; negative branch w<=4')
path=Path(__file__).with_name('book_low_triangle_verification_v19.json')
path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='resonance_tests'},ensure_ascii=False))
