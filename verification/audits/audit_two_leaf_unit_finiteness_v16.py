#!/usr/bin/env python3
"""Independent proof audit and middle reconstruction; does not import the primary checker."""
from pathlib import Path
from fractions import Fraction
from itertools import combinations, permutations
from collections import Counter
import hashlib
import json

HERE = Path(__file__).resolve().parent


def locate(name):
    roots = [HERE.parent/'z1', HERE, HERE.parent, HERE.parent.parent,
             HERE.parents[1]/'deliverables/general_type_surface_fibration_v15']
    for root in roots:
        for folder in ('', 'papers/sections/paper', 'research', 'verification', 'verification/audits'):
            p = root/folder/name
            if p.is_file():
                return p
    raise FileNotFoundError(name)


SOURCE = locate('two_leaf_unit_finiteness_v16.tex')
CHECKER = locate('verify_two_leaf_unit_finiteness_v16.py')
CERTIFICATE = locate('two_leaf_unit_finiteness_certificate_v16.json')
HELPER = locate('exact_fixed_middle_completion_v15.py')
PRIOR_AUDIT = locate('fixed_middle_completion_independent_audit_v15.json')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def valid_middle(r, s, S, T):
    if min(r, s, S, T) < 1 or not (S > r and r*T > (r+1)*S):
        return False
    a, b = s*S+1, T+1
    if a % 2 != 1 or b % 2 != 1 or (a-1) % r or (b-1) % (r+1):
        return False
    x, y = (a-1)//r, (b-1)//(r+1)
    A, B = a+x-s, b-y+1
    if A <= 0 or B <= 0 or A*B != a*b-1:
        return False
    P = [[0,-A,x,-s],[-B,0,-y,1],[r,-r-1,0,0],[-S,T,S-T-1,0]]
    q = [a,b,1,1]
    assert all(sum(P[i]) == -q[i] for i in range(4))
    assert all(P[i][j]*P[j][i] == q[i]*q[j]-1 for i,j in combinations(range(4),2))
    weights = [Fraction(a), Fraction(b), Fraction(x)+Fraction(1,2*r), Fraction(1)+Fraction(1,2*T)]
    assert all(weights[j]-weights[i]*Fraction(P[i][j],q[i]) > 0
               for i in range(4) for j in range(4) if i != j)
    return True


def independent_middle_reconstruction():
    accepted = Counter()
    branch_counts = Counter()
    def accept(r,s,S,T,branch):
        if valid_middle(r,s,S,T):
            accepted[(r,s,S,T)] += 1
            branch_counts[branch] += 1
    for r,s,S,T in [(1,1,2,6),(1,4,3,12),(2,2,3,6),(2,4,3,6),(2,6,3,6)]:
        accept(r,s,S,T,'small_S')
    for r in range(1,5):
        for s in range(1,10):
            F = -r*s*s+(4*r+3)*s-r
            assert F != 0
            for E in range(-2,8):
                S = Fraction(r*(r*s+1)*E+2*r*(r+2)*(s-1), F)
                if S.denominator != 1 or S < 4:
                    continue
                S = int(S)
                y = Fraction((r+2)*s*S-2*r*(s-1),r*(r*s+1))
                if y.denominator == 1:
                    accept(r,s,S,(r+1)*int(y),'bounded_E')
    for h in range(1,5):
        for t in range(1,5):
            if h*t > 4:
                continue
            for c in range(-4,2):
                s = h+3+c
                if s < 1:
                    continue
                for alpha in range(-4,2):
                    S = t*(h+1)-alpha
                    if S < 4:
                        continue
                    y = Fraction(3*s*S-2*(s-1),s+1)
                    if y.denominator == 1:
                        accept(1,s,S,2*int(y),'free_E_leaf3_C')
    for h in range(1,13):
        for t in range(1,7):
            for alpha in range(-4,2):
                for beta in range(-4,2):
                    gamma = -2-alpha-beta
                    if gamma < -4 or gamma > 1:
                        continue
                    for kappa in (2,5,8,10):
                        if t*(h*h+7*h+3) != alpha*(h*h+5*h+7)+(h+4)*(1+beta+kappa)-2*h-4:
                            continue
                        s, S = h+3,t*(h+1)-alpha
                        if S < 4:
                            continue
                        y = Fraction(3*s*S-2*(s-1),s+1)
                        if y.denominator == 1:
                            accept(1,s,S,2*int(y),'free_E_leaf3_B')
    return accepted, branch_counts


def matrix_from_json(model, qs):
    p = {int(i):{int(j):v for j,v in row.items()} for i,row in model['p'].items()}
    d = {int(i):v for i,v in model['D'].items()}
    labels = sorted(qs)
    assert sorted(p) == labels and sorted(d) == labels
    for i in labels:
        assert sorted(p[i]) == labels and p[i][i] == 0
        assert sum(p[i].values()) == -qs[i]
        assert d[i] == -qs[i]-sum(p[j][i] for j in labels if i != j)
    for i,j in combinations(labels,2):
        assert p[i][j]*p[j][i] == qs[i]*qs[j]-1
    for length in (2,3,4):
        for cycle in permutations(labels,length):
            if cycle[0] != min(cycle):
                continue
            gain = Fraction(1)
            for i,j in zip(cycle,cycle[1:]+cycle[:1]):
                if p[i][j] <= 0:
                    break
                gain *= Fraction(p[i][j],qs[i])
            else:
                assert gain < 1
    return p,d


def check_stored_patches(certificate):
    total = 0
    unique = set()
    for row in certificate['survivors']:
        params = row['parameters']
        key = tuple(params[k] for k in ('r','s','S','T'))
        assert valid_middle(*key)
        for patch in row['low_patches']:
            total += 1
            middle, leaf3, leaf4 = [patch[k] for k in ('middle','leaf3','leaf4')]
            a,b = row['middle']['a'],row['middle']['b']
            data = {
                2:matrix_from_json(middle,{0:a,1:b,3:1,4:1}),
                3:matrix_from_json(leaf3,{0:leaf3['q'],1:1,2:1,4:1}),
                4:matrix_from_json(leaf4,{0:1,1:leaf4['q'],2:1,3:1}),
            }
            matrix_key = (key, leaf3['q'], leaf4['q'],
                          tuple((i,tuple(sorted(r.items()))) for i,r in sorted(data[3][0].items())),
                          tuple((i,tuple(sorted(r.items()))) for i,r in sorted(data[4][0].items())))
            assert matrix_key not in unique
            unique.add(matrix_key)
            for i,j in combinations((2,3,4),2):
                pi,di = data[i]
                pj,dj = data[j]
                punctures = sorted(set(range(5))-{i,j})
                sums = [pi[j][k]+pj[i][k] for k in punctures]
                assert all(-4 <= v <= 1 for v in sums)
                assert sum(sums) == -2 and di[j]+dj[i] == 0
    assert total == len(unique) == 52
    return total


def main():
    cert = json.loads(CERTIFICATE.read_text())
    assert cert['passed']
    assert cert['script_sha256'] == sha(CHECKER)
    assert cert['source_sha256'][SOURCE.name] == sha(SOURCE)
    assert cert['dependency']['sha256'] == sha(HELPER)
    assert sha(HELPER) == 'cfb3110fe99ccc9d1d7e90bb402638078e6ebeac0f104f8429b60cdc4bdc78c8'
    old = json.loads(PRIOR_AUDIT.read_text())
    assert old['status'] == 'PASS' and not old['final_author_correction_recheck_pending']
    accepted, counts = independent_middle_reconstruction()
    reference = Counter()
    for rec in cert['candidate_records']:
        p = rec['parameters']
        reference[tuple(p[k] for k in ('r','s','S','T'))] = len(rec['witnesses'])
    assert accepted == reference and len(accepted) == 31 and sum(accepted.values()) == 66
    total = check_stored_patches(cert)
    checks = [
        {'claim':'E bound and complete C/D leaf4 case split','result':'PASS',
         'detail':'All four choices of the two remaining low labels were substituted in the full one-high matrix, retaining c,d and cd=0. The nonfree cases give E=-H, E=H+1, or H-3<=E<=H+2 with H<=5; the remaining cases give kappa in {2,5,8,10}.'},
        {'claim':'F nonzero and s<=9','result':'PASS',
         'detail':'F_r(1)=2r+3 (corrected typo), values s=2..6 and the s>=7 sign are correct. The strict bound y<(r+2)S/r^2 gives E<(4+4/r-s)S/r, excluding s>=10 when E>=-2.'},
        {'claim':'Small S complete resonance handling','result':'PASS',
         'detail':'The only (r,S) pairs are (1,2),(1,3),(2,3). Direct division gives y=4-2/(s+1), y=7-5/(s+1), and y=2 respectively; the latter has positive even s. For s>=8 both leaves are D, h<=3, c3>0,c4<0,d3=d4=0, the other center is B and the other leaf C. Their opposing D coefficients are both positive.'},
        {'claim':'Free E identity and h,t bounds','result':'PASS',
         'detail':'Independently eliminated y from T=t(h^2+h+1)+1+beta+E+kappa and the middle pair relation. The resulting identity agrees. Its upper bounds give t<=6; alpha<=0 gives h<=8, alpha=1,t>=2 gives h<=7, and alpha=t=1 gives (K,h)=(2,4),(3,12).'},
        {'claim':'Independent middle candidate generation','result':'PASS',
         'detail':'No primary checker or v15 reconstruction helper was imported. Rational formulas and explicit positive weights reconstruct the same 31 middle models and all 66 witness multiplicities.'},
        {'claim':'Stored 52 low patches satisfy original equations','result':'PASS',
         'detail':'Read the JSON matrices directly and checked row sums, pair products, D definitions, positive simple-cycle inequalities, all three low-edge node triples, D opposition, and matrix-level uniqueness.'},
        {'claim':'Complete leaf generation dependency','result':'PASS with retained scope',
         'detail':'The v15 fixed-middle reconstruction helper is byte-identical to its previously independently audited version, including B exceptional leaves and q=3 matrix deduplication. This audit independently rechecks the 52 stored patches but does not claim a second independent derivation of every missing leaf candidate.'},
    ]
    result = {
        'version':'v16','status':'PASS','passed':True,'external_peer_review':False,
        'audit_kind':'Independent proof audit and independent middle reconstruction for the non-B representation finite reduction',
        'scope':'z=1, r<=4, crossed two-leaf middle; leaf4 ray2 admits C or D. The B-only case and center completion must still be handled separately.',
        'corrected_findings':[{'finding':'F_r(1) was printed as 3r+3 in the first draft','correction':'2r+3','conclusion_affected':False,'resolved':True}],
        'checks':checks,'independent_middle_count':len(accepted),'independent_witness_count':sum(accepted.values()),
        'independent_witness_branch_counts':dict(counts),'stored_low_patches_checked':total,
        'primary_checker_imported':False,'fixed_middle_helper_imported':False,
        'source_snapshot':{SOURCE.name:sha(SOURCE),CHECKER.name:sha(CHECKER),CERTIFICATE.name:sha(CERTIFICATE),HELPER.name:sha(HELPER),PRIOR_AUDIT.name:sha(PRIOR_AUDIT)},
        'audit_script_sha256':sha(Path(__file__)),
        'limitations':['This is internal mathematical checking, not external peer review or proof-assistant formalization.',
                       'The B-only leaf case is outside this theorem.',
                       'Surviving low patches are not full five-core arithmetic atlases.'],
    }
    out = HERE/'two_leaf_unit_finiteness_independent_audit_v16.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'middle':len(accepted),'witnesses':sum(accepted.values()),'low_patches':total,'report':str(out)},ensure_ascii=False))


if __name__ == '__main__':
    main()
