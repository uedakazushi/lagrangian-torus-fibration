#!/usr/bin/env python3
"""Exact finite certificates for the G5_15 reduction, version 21.

The reverse ranges are mathematical consequences proved in the accompanying
paper.  They are not cutoffs on denominators.  Every scale is recovered by
signed-divisor factorization, including complete affine half-lines.  The
positive-exception branch is excluded for all denominators.  The ordinary
branch is reduced to fourteen cells, not declared impossible.  The negative
exception remains open with shared denominator 3 or 5.

Python standard library only.  The script does not import a previous version.
"""
from itertools import product
from math import isqrt, lcm
from pathlib import Path
import argparse
import hashlib
import json

NODES = tuple((a, b, 5-a-b) for a in range(6) for b in range(6-a))
ORDINARY_REVERSES = ((2, 3, 5), (4, 2, 2), (5, 3, 3), (6, 3, 3))
POSITIVE_REVERSES = tuple(
    [(1, 2, T) for T in range(5, 8)]
    + [(1, 3, T) for T in range(7, 14)]
    + [(2, 3, T) for T in range(5, 7)])


def egcd(a, b):
    if b == 0:
        return 1, 0, a
    x, y, g = egcd(b, a % b)
    return y, x-(a//b)*y, g


def signed_divisors(n):
    assert n > 0
    return sorted({v for d in range(1, isqrt(n)+1) if n % d == 0
                   for v in (d, n//d, -d, -n//d)})


def ceildiv(a, b):
    assert b > 0
    return -((-a)//b)


def coefficients(r, S, T):
    h, delta = S-r, T-S
    F = (2*r+1)*h-r*r*(delta-1)
    A, B, C = h*(r+1), -r*(h+delta-1), r*(r+1)
    return F, A, B, C


def all_scale_cells(r, S, T):
    """All (s,z) as (s0,z0)+n(ds,dz), n>=0, with odd q and divisibility.

    The linear and zero-factor cases are retained without a cutoff in n.
    The output may split one geometric half-line into arithmetic residues.
    """
    F, A, B, C = coefficients(r, S, T)
    K = A*B-F*C
    cells, lines = [], []
    if F and K:
        for u in signed_divisors(abs(K)):
            if K % u:
                continue
            v = K//u
            if (u-B) % F or (v-A) % F:
                continue
            s, z = (u-B)//F, (v-A)//F
            if min(s, z) < 1 or s*S % r or z*T % (r+1):
                continue
            if s*S % 2 or z*T % 2:
                continue
            cells.append((s, 0, z, 0))
    elif F:
        if (-B) % F == 0 and -B//F > 0:
            lines.append((-B//F, 0, 0, 1))
        if (-A) % F == 0 and -A//F > 0:
            lines.append((0, 1, -A//F, 0))
    else:
        # Every F=0 reverse triple in the proved range has A>0>B.
        assert A > 0 > B
        x, y, g = egcd(A, -B)
        if C % g:
            return []
        lines.append((-x*C//g, -B//g, y*C//g, A//g))
    for s, ds, z, dz in lines:
        period = lcm(2*r, 2*(r+1))
        assert ds >= 0 and dz >= 0 and ds+dz > 0
        for residue in range(period):
            ss, zz = s+ds*residue, z+dz*residue
            if ss*S % r or zz*T % (r+1) or ss*S % 2 or zz*T % 2:
                continue
            if (ds == 0 and ss < 1) or (dz == 0 and zz < 1):
                continue
            first = max(ceildiv(1-ss, ds*period) if ds else 0,
                        ceildiv(1-zz, dz*period) if dz else 0)
            cells.append((ss+ds*period*first, ds*period,
                          zz+dz*period*first, dz*period))
    out = sorted(set(cells))
    for s, ds, z, dz in out:
        assert min(s, z) >= 1 and min(ds, dz) >= 0
        assert [F*s*z+A*s+B*z+C,
                F*(s*dz+z*ds)+A*ds+B*dz, F*ds*dz] == [0, 0, 0]
        assert s*S % r == ds*S % r == z*T % (r+1) == dz*T % (r+1) == 0
        assert s*S % 2 == ds*S % 2 == z*T % 2 == dz*T % 2 == 0
    return out


def canonical(r, s, z, S, T):
    assert min(r, s, z, S, T) > 0
    assert s*S % r == z*T % (r+1) == 0
    a, b = s*S+1, z*T+1
    assert a % 2 == b % 2 == 1
    x, y, L = s*S//r, z*T//(r+1), T-S+1
    U, V = a+x-s, b-y+z
    assert U*V == a*b-1
    P = [[0, -U, x, -s], [-V, 0, -y, z],
         [r, -r-1, 0, 0], [-S, T, -L, 0]]
    q = [a, b, 1, 1]
    D = [-q[j]-sum(P[k][j] for k in range(4) if k != j)
         for j in range(4)]
    assert all(sum(P[j]) == -q[j] for j in range(4))
    assert all(P[i][j]*P[j][i] == q[i]*q[j]-1
               for i in range(4) for j in range(i+1, 4))
    assert {(i, j) for i in range(4) for j in range(4) if P[i][j] > 0} == {
        (0, 2), (2, 0), (1, 3), (3, 1)}
    assert D[2] == T-S+y-x and D[3] == s-z-1
    return dict(parameters=[r, s, z, S, T], order=[0, 1, 3, 4],
                q=q, P=P, D=D)


def affine_matrix_identity_check(r, S, T, scale):
    """Check coefficients, rather than finitely sampled parameter values."""
    s, ds, z, dz = scale
    first = canonical(r, s, z, S, T)
    second = canonical(r, s+ds, z+dz, S, T)
    q = [(first['q'][i], second['q'][i]-first['q'][i]) for i in range(4)]
    P = [[(first['P'][i][j],second['P'][i][j]-first['P'][i][j])
          for j in range(4)] for i in range(4)]
    def mul(a,b):
        return [a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[1]*b[1]]
    for i in range(4):
        assert [sum(P[i][j][k] for j in range(4)) for k in (0,1)] == [-v for v in q[i]]
        for j in range(i+1,4):
            left,right = mul(P[i][j],P[j][i]),mul(q[i],q[j])
            right[0] -= 1
            assert left == right
    return dict(all_row_identity_coefficients_zero=True,
                all_pair_identity_coefficients_zero=True,
                parameter_scope='every integer t>=0')


def low_rows(center, n, m):
    r, s, z, S, T = center['parameters']
    L = T-S+1
    R3 = (1-n[0]-r, r+2-n[1], 1-n[2])
    R4 = (S+1-m[0], 1-T-m[1], L+1-m[2])
    assert sum(R3) == sum(R4) == -1
    return R3, R4


def matching_row(row):
    return 0 not in row and sum(x > 0 for x in row) == 1


def ordinary_stage():
    catalog = []
    for r, S, T in ORDINARY_REVERSES:
        scale_cells = all_scale_cells(r, S, T)
        assert len(scale_cells) == 1
        s, ds, z, dz = scale_cells[0]
        assert ds == dz == 0
        model = canonical(r, s, z, S, T)
        catalog.append(model)
    assert [c['parameters'] for c in catalog] == [
        [2, 2, 6, 3, 5], [4, 4, 5, 2, 2],
        [5, 10, 2, 3, 3], [6, 6, 14, 3, 3]]
    cells, parity_exclusions = [], []
    for index, c in enumerate(catalog, 1):
        for n, m in product(NODES, repeat=2):
            R3, R4 = low_rows(c, n, m)
            if not matching_row(R3) or not matching_row(R4):
                continue
            if R3[2]+R4[2] != 0:
                continue
            assert 1 <= abs(R3[2]) <= 4
            rec = dict(center=index, nodes23=n, nodes24=m,
                       low_row3=R3, low_row4=R4,
                       low_D3=-c['D'][2], low_D4=-c['D'][3],
                       common_reverse_magnitude=abs(R3[2]))
            bad = [i for i, row, d in (
                (3, R3, rec['low_D3']), (4, R4, rec['low_D4']))
                if all(v % 2 for v in row) and d % 2 == 0]
            if bad:
                rec['certificate'] = dict(kind='odd_low_D_required', cores=bad,
                    reason='All three low-row entries are odd. Odd denominators make all low-column entries even, hence low D is odd.')
                parity_exclusions.append(rec)
            else:
                cells.append(rec)
    assert len(cells) == 14 and len(parity_exclusions) == 4
    return dict(status='complete necessary reduction, not an exclusion',
                reverse_triples=ORDINARY_REVERSES, centers=catalog,
                factor_data=[dict(reverse=[r, S, T], coefficients=coefficients(r, S, T),
                                 factor_constant=coefficients(r, S, T)[1]*coefficients(r, S, T)[2]
                                 -coefficients(r, S, T)[0]*coefficients(r, S, T)[3],
                                 scale_cells=all_scale_cells(r, S, T))
                             for r, S, T in ORDINARY_REVERSES],
                cells_before_parity=18, parity_exclusions=parity_exclusions,
                remaining_cells=cells, denominator_scope='q34 is not bounded; odd q34 and m | (q34-1) are required.')


def positive_exception_stage():
    scale_catalog, central = [], {}
    for r, S, T in POSITIVE_REVERSES:
        for scale in all_scale_cells(r, S, T):
            s, ds, z, dz = scale
            rec = dict(reverse=[r, S, T], scale_cell=scale,
                       parameter_scope='all integers t>=0 before imposing s<=z',
                       matrix_identity_check=affine_matrix_identity_check(r,S,T,scale))
            if ds == dz == 0:
                ts = [0] if s <= z else []
                rec['intersection_s_le_z'] = ts
            else:
                # Every actual half-line in this proof range has ds>dz.
                assert ds > dz
                upper = (z-s)//(ds-dz)
                ts = range(upper+1) if upper >= 0 else []
                rec['intersection_s_le_z'] = dict(lower=0, upper=upper)
            for t in ts:
                params = (r, s+ds*t, z+dz*t, S, T)
                central[params] = canonical(*params)
            scale_catalog.append(rec)
    assert len(central) == 8
    rejected = []
    for params in sorted(central):
        c = central[params]
        for n, m in product(NODES, repeat=2):
            R3, R4 = low_rows(c, n, m)
            if R3 != (-1, -1, 1) or not matching_row(R4):
                continue
            u, v = R3[2], R4[2]
            if u != 1 or v <= 1:
                continue
            Q = u+v
            if Q % 2 == 0:
                continue
            assert max(R4[:2]) < 0
            assert R4[0]+R4[1] == -Q
            value = Q-c['D'][2]
            assert value < 4
            rejected.append(dict(parameters=params, nodes23=n, nodes24=m,
                                 low_row3=R3, low_row4=R4, q34=Q,
                                 D_C=c['D'][2], D_D=c['D'][3],
                                 certificate=dict(kind='two_odd_denominators_at_core3',
                                     required_sum= 'q03-1 + q13-1 = q34-D_C >= 4',
                                     actual_q34_minus_D_C=value)))
    assert len(rejected) == 8
    assert sorted(r['certificate']['actual_q34_minus_D_C'] for r in rejected) == [
        -96, -12, -9, -4, -1, 0, 2, 2]
    return dict(status='unbounded exclusion proved',
                reverse_range=POSITIVE_REVERSES,
                scale_catalog_including_all_half_lines=scale_catalog,
                mathematical_scale_constraint='s<=z follows from low D at core4 and odd high denominators; no numerical scale cutoff.',
                centers_after_scale_constraint=[central[k] for k in sorted(central)],
                complete_final_certificates=rejected,
                final_survivors=0)


def resolve_proof_path(override=None):
    if override is not None:
        path = Path(override)
        assert path.is_file()
        return path
    candidates = (Path(__file__).with_name('g5_15_reduction_v21.tex'),
                  Path(__file__).parent.parent/'papers/sections/paper'/'g5_15_reduction_v21.tex')
    return next(path for path in candidates if path.is_file())


def main_data(proof_path=None):
    ordinary = ordinary_stage()
    positive = positive_exception_stage()
    proof = resolve_proof_path(proof_path)
    return dict(status='PASS', theorem_label='g51521:reduction',
        support=dict(high_edges=['01','02','03','04','12','13','14','34'],
                     low_edges=['23','24'], bivalent_core=2),
        assumptions=['positive integral local charts', 'all denominators odd',
                     'marked integer clutching', 'each node triple nonnegative with total five',
                     'opposite D coefficients cancel'],
        scope='Only the stated full G5_15 support. No argument is applied merely to a contained subgraph.',
        no_denominator_cutoff=True,
        ordinary=ordinary, positive_exception=positive,
        negative_exception=dict(status='open; completely reduced to two templates',
            shared_denominators=[3,5],
            template_A=dict(q34=3,u=-1,v=-2,branch='negative only: S=T=w, r=w+H',
                nodes23='(a,3-a,2), 0<=a<=3', nodes24='(b,1-b,4), 0<=b<=1',
                low_row3='(-j,j,-1), j=r+a-1',low_row4='(k+1,-k,-2), k=w-b'),
            template_B=dict(q34=[3,5],u='-(q34-1)',v=-1,
                branch='L=1 negative branch or L=3 positive branch',
                nodes23='(a,5-q34-a,q34), 0<=a<=5-q34',
                nodes24='(b,3-L-b,L+2), 0<=b<=3-L',
                low_row3='(-j,j+q34-2,-(q34-1)), j=r+a-1>=1',
                low_row4='(k,-k,-1), k=S+1-b>=1'),
            central_branch_constraints=dict(
                negative='S=T=w>=2, r=w+H, w*w < 2*H*(H+1) < 4*w*w',
                positive='T=S+2 and r<S<2*r')),
        corollary='If q34>=7, the central two-high core is one of the four ordinary models. Its two high denominators are at most 43 in the canonical orientation.',
        not_claimed=['G5_15 exclusion', 'a global arithmetic lift', 'a Lagrangian torus fibration existence or nonexistence result beyond the arithmetic setting'],
        proof_file='papers/sections/paper/g5_15_reduction_v21.tex',
        proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest(),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default=str(Path(__file__).with_name('g5_15_reduction_verification_v21.json')))
    parser.add_argument('--proof', help='Optional path to the associated TeX proof.')
    args = parser.parse_args()
    result = main_data(args.proof)
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'], ordinary_centers=4,
                          ordinary_cells_before_parity=18, ordinary_cells_remaining=14,
                          positive_exception_final_certificates=8,
                          positive_exception_survivors=0,
                          negative_exception_q=[3,5]),ensure_ascii=False))
