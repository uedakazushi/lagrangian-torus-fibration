#!/usr/bin/env python3
"""Exact, standard-library certificate for the v15 two-leaf lemmas.

No denominator cutoff is used.  The small negative branch is exhausted by the
proved bound w^2/2 < H(H+1) < 2w^2 for w=2,3,4 and exact factorization.
For each of these finitely many middle cores, all possible leaf models are
reconstructed from the six-value node intervals and positive divisors.
The unknown center-to-center denominator is never enumerated: contradiction
already occurs on the low triangle 23,24,34.
"""
from fractions import Fraction
from itertools import combinations, permutations, product
from math import isqrt
from pathlib import Path
import hashlib
import json


class Poly:
    """Integer polynomial, optionally reduced modulo the monomial c*d."""
    def __init__(self, value=0):
        self.terms = ({(): value} if isinstance(value, int) else dict(value))
        self.terms = {k: v for k, v in self.terms.items() if v}

    @staticmethod
    def cast(value):
        return value if isinstance(value, Poly) else Poly(value)

    @staticmethod
    def var(name):
        return Poly({(name,): 1})

    def __add__(self, value):
        terms = dict(self.terms)
        for k, v in self.cast(value).terms.items():
            terms[k] = terms.get(k, 0) + v
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.terms.items()})

    def __sub__(self, value):
        return self + (-self.cast(value))

    def __rsub__(self, value):
        return self.cast(value) + (-self)

    def __mul__(self, value):
        terms = {}
        for k, v in self.terms.items():
            for j, w in self.cast(value).terms.items():
                key = tuple(sorted(k+j))
                terms[key] = terms.get(key, 0) + v*w
        return Poly(terms)

    __rmul__ = __mul__

    def zero(self, modulo_cd=False):
        return not {k: v for k, v in self.terms.items()
                    if not (modulo_cd and 'c' in k and 'd' in k)}


def divisors(n):
    assert n > 0
    out = []
    for d in range(1, isqrt(n)+1):
        if n % d == 0:
            out.append(d)
            if d*d != n:
                out.append(n//d)
    return sorted(out)


def simple_cycles(labels, edges):
    result = []
    for n in range(2, len(labels)+1):
        for cycle in permutations(labels, n):
            if cycle[0] != min(cycle):
                continue
            if all((i, j) in edges for i, j in
                   zip(cycle, cycle[1:]+cycle[:1])):
                result.append(cycle)
    return result


def symbolic_checks():
    h, t, c, d = (Poly.var(k) for k in ('h', 't', 'c', 'd'))
    m, u, v = t*h*(h+1), t*h, t*(h+1)
    q = [m+1, 1, 1, 1]
    P = [[0, -m, -h-1, h], [-1, 0, 0, 0],
         [-u, u-1-c, 0, c], [v, -v-1-d, d, 0]]
    D = [-m-t, m+t+1+c+d, h-d, -h-1-c]
    for i in range(4):
        assert Poly.cast(sum(P[i])+q[i]).zero()
        assert Poly.cast(-q[i]-sum(P[j][i] for j in range(4) if j != i)-D[i]).zero()
    for i, j in combinations(range(4), 2):
        assert Poly.cast(q[i]*q[j]-P[i][j]*P[j][i]-1).zero(modulo_cd=True)
    assert (u-1-(D[1]-m-t-1)-(t*(h+1)*(h+1)-D[1])).zero()
    k = Poly.var('kappa')
    assert (m+t+k-v-(t*h*h+k)).zero()
    # Complete positivity audit: use supersets of the positive edges.
    graph_checks = []
    for sign_c, sign_d in ((-1,0),(0,0),(1,0),(0,-1),(0,1)):
        edges = {('A','D'),('D','A'),('C','B'),('D','B')}
        if sign_c > 0:
            edges.add(('C','D'))
        if sign_d > 0:
            edges.add(('D','C'))
        cycles = simple_cycles('ABCD', edges)
        assert cycles == [('A','D')]
        graph_checks.append(dict(sign_c=sign_c, sign_d=sign_d, cycles=cycles))
    # x=1 would force the following impossible identity.
    s, w, k = (Poly.var(k) for k in ('s', 'w', 'k'))
    r = s*w
    a = r+1
    b = k*(r+1)*w+1
    A = r+2-s
    B = 1+k*(r*(w+1)+1)
    residual = 2-s+k*(w*(-s*s+3*s-1)+2-s)
    assert (A*B-a*b+1-residual).zero()
    return dict(row_identities=4, pair_identities_modulo_cd=6,
                coefficient_identities=4, leaf_inequality_identities=2,
                positive_graph_cases=graph_checks,
                only_cycle_gain='t*h*(h+1)/(t*h*(h+1)+1) < 1',
                x_one_residual_identity=True)


def weights_exist(P, qs):
    labels = sorted(P)
    edges = {(i,j) for i in labels for j in labels if i != j and P[i][j] > 0}
    for cycle in simple_cycles(labels, edges):
        gain = Fraction(1)
        for i, j in zip(cycle, cycle[1:]+cycle[:1]):
            gain *= Fraction(P[i][j], qs[i])
        if gain >= 1:
            return False
    return True


def check_model(model):
    P, qs, D = model['p'], model['qs'], model['D']
    labels = sorted(P)
    assert all(sum(P[i].values()) == -qs[i] for i in labels)
    assert all(qs[i]*qs[j]-P[i][j]*P[j][i] == 1
               for i, j in combinations(labels, 2))
    assert all(D[i] == -qs[i]-sum(P[j][i] for j in labels if j != i)
               for i in labels)
    assert weights_exist(P, qs)


def canonical_middle(r, s, z, w):
    a, b = s*w+1, z*w+1
    assert a % 2 == b % 2 == 1
    assert (a-1) % r == (b-1) % (r+1) == 0
    x, y = (a-1)//r, (b-1)//(r+1)
    A, B = a+x-s, b-y+z
    arr = [[0,-A,x,-s],[-B,0,-y,z],[r,-r-1,0,0],[-w,w,-1,0]]
    order = (0,1,4,3)  # The crossed pairing: C=4,D=3.
    P = {i: {j: arr[ii][jj] for jj,j in enumerate(order)}
         for ii,i in enumerate(order)}
    qs = dict(zip(order,(a,b,1,1)))
    D = {i:-qs[i]-sum(P[j][i] for j in order if j != i) for i in order}
    model = dict(p=P, qs=qs, D=D, parameters=dict(r=r,s=s,z=z,S=w,T=w), a=a,b=b)
    check_model(model)
    return model


def negative_small_models():
    found = {}
    factor_records = []
    for w in (2,3,4):
        # H<2w follows from the proved strict quadratic bound.
        for H in range(1,2*w):
            if not w*w < 2*H*(H+1) < 4*w*w:
                continue
            E = 1-Fraction(w*w,H*(H+1))
            M, N = E.numerator, E.denominator
            assert M
            product_value = N*(N-M)
            trials = []
            for f in divisors(product_value):
                g = product_value//f
                if (N-f) % M or (g-N) % M:
                    trials.append(dict(f=f,g=g,accepted=False,reason='nonintegral_u_v'))
                    continue
                u, v = (N-f)//M, (g-N)//M
                if min(u,v) < 1:
                    trials.append(dict(f=f,g=g,accepted=False,reason='nonpositive_u_v'))
                    continue
                sf, zf = Fraction(u*(H+w),H), Fraction(v*(H+w+1),H+1)
                if sf.denominator != 1 or zf.denominator != 1:
                    trials.append(dict(f=f,g=g,accepted=False,reason='nonintegral_s_z'))
                    continue
                s, z, r = int(sf), int(zf), H+w
                if (s*w+1) % 2 != 1 or (z*w+1) % 2 != 1:
                    trials.append(dict(f=f,g=g,accepted=False,reason='nonodd_denominator'))
                    continue
                model = canonical_middle(r,s,z,w)
                found[(r,s,z,w)] = model
                trials.append(dict(f=f,g=g,accepted=True,parameters=model['parameters']))
            factor_records.append(dict(w=w,H=H,E=str(E),factor_product=product_value,trials=trials))
    expected = {(4,4,5,2),(5,10,2,3),(6,6,14,3),(7,7,2,4),
                (7,21,4,4),(8,6,9,4),(8,8,27,4)}
    assert set(found) == expected
    return [found[key] for key in sorted(found)], factor_records


def leaf(high,B,C,D,h,t,c,d):
    assert min(h,t) >= 1 and c*d == 0
    m,u,v = t*h*(h+1),t*h,t*(h+1)
    labels = (high,B,C,D)
    arr = ((0,-m,-h-1,h),(-1,0,0,0),(-u,u-1-c,0,c),(v,-v-1-d,d,0))
    P = {a:{b:arr[i][j] for j,b in enumerate(labels)} for i,a in enumerate(labels)}
    DD = dict(zip(labels,(-m-t,m+t+1+c+d,h-d,-h-1-c)))
    out = dict(q=m+1,p=P,D=DD,qs={a:m+1 if a==high else 1 for a in labels},
               h=h,t=t,c=c,d=d,order=labels)
    check_model(out)
    return out


def edge_reasons(i,j,mi,mj):
    punctures = sorted(set(mi['p'][j])-{j})
    sums = [mi['p'][j][k]+mj['p'][i][k] for k in punctures]
    assert sum(sums) == -2
    reasons=[]
    if not all(-4 <= v <= 1 for v in sums): reasons.append('node_interval')
    if mi['D'][j]+mj['D'][i] != 0: reasons.append('coefficient_opposition')
    return reasons


def leaf_candidates(i,core):
    high = {3:0,4:1}[i]
    other, otherleaf = 1-high,7-i
    row,E = core['p'][i],core['D'][i]
    # No B type is omitted: its entire row would be (-1,0,0).
    B_allowed = all(-4 <= value+(-1 if j==high else 0) <= 1
                    for j,value in row.items() if j != i)
    assert not B_allowed
    out=[]
    # ray 2=C: reverse=-u, u=t*h. Its six-value node interval fixes u.
    for u in range(max(1,row[high]-1),row[high]+5):
        for h in divisors(u):
            t,d = u//h,h+E
            for B,D in permutations((other,otherleaf)):
                possible_c = [0] if d else range(-4-row[D],2-row[D])
                for c in possible_c:
                    model = leaf(high,B,2,D,h,t,c,d)
                    if not edge_reasons(2,i,core,model): out.append(model)
    # ray 2=D: reverse=v, v=t*(h+1). The same argument fixes v.
    for v in range(max(2,-4-row[high]),2-row[high]):
        for hp1 in divisors(v):
            if hp1 < 2: continue
            h,t = hp1-1,v//hp1
            c = E-h-1
            for B,C in permutations((other,otherleaf)):
                possible_d = [0] if c else range(-4-row[C],2-row[C])
                for d in possible_d:
                    model = leaf(high,B,C,2,h,t,c,d)
                    if not edge_reasons(2,i,core,model): out.append(model)
    # At q=3 two negative labels may coincide; remove identical matrices only.
    unique={}
    for model in out:
        key=(model['q'],tuple(model['p'][a][b] for a in sorted(model['p'])
                             for b in sorted(model['p'][a])))
        unique[key]=model
    return list(unique.values())


def compact_leaf(model):
    return {k:model[k] for k in ('q','h','t','c','d','order','p','D')}


def main():
    identities = symbolic_checks()
    cores, factors = negative_small_models()
    records=[]
    for core in cores:
        l3,l4 = leaf_candidates(3,core),leaf_candidates(4,core)
        failed={}
        pair_trials=[]
        for (index3,a),(index4,b) in product(enumerate(l3),enumerate(l4)):
            reasons=edge_reasons(3,4,a,b)
            assert reasons, 'A low-triangle completion survived.'
            key='+'.join(reasons)
            failed[key]=failed.get(key,0)+1
            sums={k:a['p'][4][k]+b['p'][3][k] for k in (0,1,2)}
            pair_trials.append(dict(leaf_3_index_zero_based=index3,
                                    leaf_4_index_zero_based=index4,
                                    node_sums=sums,node_counts={k:1-v for k,v in sums.items()},
                                    D_sum=a['D'][4]+b['D'][3],
                                    rejected_by=reasons,accepted=False))
        records.append(dict(parameters=core['parameters'],middle_denominators=[core['a'],core['b']],
                            middle_P=core['p'],middle_D=core['D'],
                            leaf_3_candidates=[compact_leaf(m) for m in l3],
                            leaf_4_candidates=[compact_leaf(m) for m in l4],
                            candidate_counts=[len(l3),len(l4)],tested_leaf_pairs=len(l3)*len(l4),
                            rejected_pairs_by_reason=failed,leaf_pair_trials=pair_trials,
                            surviving_low_triangles=0))
    script_path=Path(__file__)
    sources=[]
    for filename in ('one_high_and_crossed_pairing_v15.tex','two_leaves_negative_branch_v15.tex'):
        source_path=script_path.with_name(filename)
        if not source_path.is_file():
            source_path=script_path.parent.parent/'paper'/filename
        sources.append(dict(filename=filename,source_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest()))
    report = dict(status='PASS',passed=True,version='v15',
                  script_sha256=hashlib.sha256(script_path.read_bytes()).hexdigest(),sources=sources,
                  scope='Exact identities and complete small-negative-branch leaf reconstruction',
                  no_denominator_cutoff=True,
                  unknown_center_denominator='Irrelevant: contradiction precedes center reconstruction',
                  symbolic_checks=identities,complete_factor_trials=factors,models=records,
                  conclusion='For all seven w<=4 negative-branch models, the crossed low triangle has no completion.')
    dest=Path(__file__).with_name('two_leaves_exact_certificate_v15.json')
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],models=len(records),
                          candidate_counts=[r['candidate_counts'] for r in records],
                          tested_leaf_pairs=sum(r['tested_leaf_pairs'] for r in records),
                          surviving_low_triangles=0,certificate=dest.name),ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
