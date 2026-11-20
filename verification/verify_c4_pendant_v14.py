#!/usr/bin/env python3
"""Exact, proof-derived certificate for the C4 plus pendant-edge obstruction.

There is no denominator cutoff. The finite fixed-denominator calculations use
the previously proved complete divisor factorization in both orientations.
The general node arguments and the exhaustion of cases are in the TeX proof.
"""
from pathlib import Path
from fractions import Fraction
import importlib.util
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
DEP_NAME = 'verify_fixed_denominator_partners_v12.py'
DEP = next(p for p in (HERE/DEP_NAME,
    HERE.parents[1]/'deliverables/general_type_surface_fibration_v13/verification'/DEP_NAME)
    if p.is_file())
spec = importlib.util.spec_from_file_location('cp14_fixed', DEP)
fp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fp)


def negative_catalog():
    cases, accepted = [], []
    for w in range(2, 5):
        # H<2w follows from H(H+1)<2w^2; this is a derived finite range.
        for H in range(1, 2*w):
            if not Fraction(w*w, 2) < H*(H+1) < 2*w*w:
                continue
            E = 1-Fraction(w*w, H*(H+1))
            M, N = E.numerator, E.denominator
            assert M != 0 and N > 0
            K = N*(N-M)
            row = {'w': w, 'H': H, 'E': str(E), 'factor_product': K, 'trials': []}
            for d in fp.positive_divisors(K):
                e = K//d
                u, v = Fraction(N-d, M), Fraction(e-N, M)
                trial = {'d': d, 'e': e, 'u': str(u), 'v': str(v)}
                if min(u, v) <= 0 or u.denominator != 1 or v.denominator != 1:
                    trial['outcome'] = 'u,v are not positive integers.'
                else:
                    s, z = u*Fraction(H+w, H), v*Fraction(H+w+1, H+1)
                    trial.update({'s': str(s), 'z': str(z)})
                    if s.denominator != 1 or z.denominator != 1:
                        trial['outcome'] = 's,z are not integers.'
                    else:
                        s, z = int(s), int(z)
                        a, b = s*w+1, z*w+1
                        assert a % 2 == b % 2 == 1
                        model = fp.model(a, b, H+w, s, z)
                        assert model['S'] == model['T'] == w
                        trial['outcome'] = 'accepted'
                        trial['model_index'] = len(accepted)
                        accepted.append(model)
                row['trials'].append(trial)
            cases.append(row)
    expected = {(4,4,5,2), (5,10,2,3), (6,6,14,3), (7,7,2,4),
                (7,21,4,4), (8,6,9,4), (8,8,27,4)}
    assert {(m['r'],m['s'],m['z'],m['S']) for m in accepted} == expected
    assert len(accepted) == 7 and len(cases) == 6
    return cases, sorted(accepted, key=lambda m: (m['S'], m['r'], m['s']))


def graph_exclusion(edges):
    """Apply established component and v14 local-shape exclusions in order."""
    if not edges:
        return 'empty_support'
    adjacency = {i:set() for i in range(5)}
    for i,j in edges:
        adjacency[i].add(j); adjacency[j].add(i)
    seen = set(); components = []
    for start in range(5):
        if start in seen or not adjacency[start]:
            continue
        comp={start};stack=[start]
        while stack:
            v=stack.pop()
            for u in adjacency[v]-comp:
                comp.add(u);stack.append(u)
        seen |= comp
        components.append(comp)
    if any(sum(len(adjacency[v]) for v in comp)//2 == len(comp)-1 for comp in components):
        return 'tree_component'
    if any(all(len(adjacency[v])==2 for v in comp) for comp in components):
        return 'pure_cycle_component'
    for i,j in edges:
        if len(adjacency[i])==len(adjacency[j])==2 and adjacency[i]-{j}==adjacency[j]-{i}:
            return 'triangle_with_two_degree_two_vertices'
    leaves=[i for i in range(5) if len(adjacency[i])==1]
    if len(leaves)==1:
        leaf=leaves[0]
        remaining=set(range(5))-{leaf}
        if all(len(adjacency[v]&remaining)==2 for v in remaining):
            return 'C4_with_pendant_edge'
    return None


def main():
    identities = []
    def identity(name, left, right):
        assert left == right, name
        identities.append(name)

    names = ('M','N','u','v','s','z','T','S','t','k','h','a','b','c')
    M,N,u,v,s,z,T,S,t,k,h,a,b,c = [fp.Poly.variable(x) for x in names]
    identity('negative E rearrangement', M*u*v-N*(v-u+1), u*(M*v+N)-N*(v+1))
    identity('negative branch factorization',
             (N-M*u)*(N+M*v)-N*(N-M), -M*(M*u*v-N*(v-u+1)))
    identity('middle r1 S2 T5 cleared pair product',
             2*(3*s+1)+7*z*(3*s+1)-2*((2*s+1)*(5*z+1)-1),
             8-(3-s)*(z+2))
    identity('middle r1 S2 T6 pair product',
             (3*s+1)*(4*z+1)-((2*s+1)*(6*z+1)-1), s-2*z+1)
    identity('middle r1 S3 T7 cleared pair product',
             2*(5*s+1)+9*z*(5*s+1)-2*((3*s+1)*(7*z+1)-1),
             z*(3*s-5)+4*s+2)
    identity('r1 z1 T formula',
             (s+1)*T-(2*s*(3*S-2)+4),
             (s+1)*(T-(6*S-4))+(6*S-8))
    identity('r2 z1 S4 T formula',
             (2*s+1)*T-(18*s+6), (2*s+1)*(T-9)+3)
    identity('r3 z1 S4 T formula after s=3k',
             (9*k+1)*T-(56*k+8), (9*k+1)*(T-6)-(2*k+2))
    identity('r3 z1 S4 fractional interval',
             (9*k+1)-(2*k+2), 7*k-1)
    identity('leaf positive reverse violates n24;0', 1-(2+u), -1-u)
    identity('central low node with negative R is at least seven',
             1+(2+u)+(4+v), 7+u+v)
    identity('positive leaf reverse lower bound',
             (1+t)*((1+h)+1)-2, 2*t+h+t*h)

    # The only unbounded central family retained by the written proof.
    aa,bb = 4*t-1, 6*t+1
    rr,ss,zz,SS,TT = 1,2*t-1,t,2,6
    xx,yy,AA,BB = 4*t-2,3*t,6*t-2,4*t+1
    pp = [[0,-AA,xx,-ss],[-BB,0,-yy,zz],
          [1,-2,0,0],[-2,6,-5,0]]
    qq = [aa,bb,1,1]
    for i in range(4):
        identity(f'central family row {i}',sum(pp[i]),-qq[i])
    for i,j in itertools.combinations(range(4),2):
        identity(f'central family crossing {i},{j}',qq[i]*qq[j]-pp[i][j]*pp[j][i],1)
    DD = [-qq[i]-sum(pp[j][i] for j in range(4) if j!=i) for i in range(4)]
    for i,target in enumerate([3,-7,6-t,t-2]):
        identity(f'central family D {i}',DD[i],target)
    identity('terminal s_prime=2t from the first multiple',
             bb-(4*t+1),2*t)
    identity('terminal second multiple exceeds b-1',
             (2*bb-(4*t+1))-(bb-1),2*t+1)
    aprime,bprime,cprime = 7*t+1,6*t+7,7*t+8
    identity('terminal other denominator',aprime*bprime+1,bb*cprime)
    identity('terminal three times z_prime',3*bprime-3*cprime+(cprime-1),4*(t+1))
    identity('terminal four times c_prime minus one',4*(cprime-1),7*4*(t+1))
    identity('terminal D opposition fixes B_prime',-bb+bprime+1,7)

    negative_cases, models = negative_catalog()
    targets = {}
    for model in models:
        for side in (0,1):
            targets.setdefault(model['q'][side],set()).add(-model['D'][side])
    # Extra exact exclusions in the z=1 central family.
    for n,d in [(3,-3),(5,-6),(13,3),(17,9),(29,15)]:
        targets.setdefault(n,set()).add(d)

    catalogs, exclusions = {}, []
    for n in sorted(targets):
        data = fp.partners_for_fixed(n)
        catalogs[str(n)] = data
        coefficients = sorted({m['D'][0 if m['fixed_side']=='A' else 1]
                               for m in data['nonresonant_models']})
        for target in sorted(targets[n]):
            matches = [m for m in data['nonresonant_models']
                       if m['D'][0 if m['fixed_side']=='A' else 1] == target]
            assert not matches,(n,target)
            resonant_trials = []
            for branch in data['resonances']:
                assert n in (7,13)
                offset = 9 if n == 7 else 14
                kval = Fraction(target+offset,n)
                compatible = kval.denominator==1 and kval>=1
                assert not compatible,(n,target,kval)
                resonant_trials.append({'coefficient':f'{n}k-{offset}',
                    'required_k':str(kval),'compatible_positive_integer':False})
            exclusions.append({'q':n,'target_D':target,'nonresonant_matches':[],
                'complete_nonresonant_D_values':coefficients,
                'resonance_checks':resonant_trials})
    assert len(catalogs) == 16
    assert sum(len(d['nonresonant_models']) for d in catalogs.values()) == 482

    # Full finite arithmetic of the small-middle reductions.
    c_pairs = [(ss,tt) for ss in range(2,4) for tt in range(ss,ss+5)
               if tt>2*ss and tt-ss+1<=5]
    assert c_pairs == [(2,5),(2,6),(3,7)]
    c_divisor_trials = []
    for d in fp.positive_divisors(8):
        sv,zv = 3-8//d,d-2
        accepted = sv>=1 and zv>=1
        row={'z_plus_two':d,'s':sv,'z':zv,'accepted':accepted}
        if accepted:row['model']=fp.model(2*sv+1,5*zv+1,1,sv,zv)
        c_divisor_trials.append(row)
    assert [(x['s'],x['z']) for x in c_divisor_trials if x['accepted']] == [(1,2),(2,6)]
    assert (3*7)%2 == 1 # S=3,T=7 would force s=1,z=3, violating divisibility.

    z_one_trials, z_one_models = [], []
    for w in (2,3,4):
        numerator=6*w-8
        for d in fp.positive_divisors(numerator):
            sv=d-1;tv=6*w-4-numerator//d
            accepted=sv>=1 and tv>0 and tv%2==0
            row={'r':1,'S':w,'s_plus_one':d,'s':sv,'T':tv,'accepted':accepted}
            if accepted:
                m=fp.model(sv*w+1,tv+1,1,sv,1)
                row['model']=m;z_one_models.append(m)
            z_one_trials.append(row)
    assert {(m['a'],m['b'],m['r'],m['s'],m['S'],m['T']) for m in z_one_models} == {
        (3,7,1,1,2,6),(13,13,1,4,3,12),(5,13,1,1,4,12),
        (13,17,1,3,4,16),(29,19,1,7,4,18)}
    assert 8%3 != 0 # r=2,S=4,z=1 isolated integer T is8, inadmissible.

    # General symbolic resonance, distinguished from any finite examples.
    res_a,res_b=6*k+1,7
    res_p=[[0,-(7*k+1),3*k,-2*k],[-6,0,-2,1],
           [2,-3,0,0],[-3,6,-4,0]]
    res_q=[res_a,res_b,1,1]
    for i in range(4):identity(f'fixed7 resonance row {i}',sum(res_p[i]),-res_q[i])
    for i,j in itertools.combinations(range(4),2):
        identity(f'fixed7 resonance crossing {i},{j}',res_q[i]*res_q[j]-res_p[i][j]*res_p[j][i],1)
    identity('fixed7 resonance shared coefficient',
             -7-sum(res_p[j][1] for j in (0,2,3)),7*k-9)

    # Graph counts are necessary support candidates, never existence counts.
    graph_counts={k:0 for k in ['empty_support','tree_component','pure_cycle_component',
        'triangle_with_two_degree_two_vertices','C4_with_pendant_edge','remaining']}
    all_edges=list(itertools.combinations(range(5),2))
    for mask in range(1<<len(all_edges)):
        edges=[e for i,e in enumerate(all_edges) if mask&(1<<i)]
        graph_counts[graph_exclusion(edges) or 'remaining'] += 1
    assert graph_counts == {'empty_support':1,'tree_component':300,'pure_cycle_component':37,
        'triangle_with_two_degree_two_vertices':165,'C4_with_pendant_edge':60,'remaining':461}
    old_name='forest_obstruction_verification_v13.json'
    old_path=next(p for p in (HERE/old_name,
        HERE.parents[1]/'deliverables/general_type_surface_fibration_v13/verification'/old_name)
        if p.is_file())
    old_agenda=json.loads(old_path.read_text())['remaining_support_agenda']
    removed_shapes=[];remaining_shapes=[]
    for shape in old_agenda['shapes']:
        exclusion=graph_exclusion(shape['canonical_edges'])
        if exclusion:
            removed_shapes.append({**shape,'v14_exclusion':exclusion})
        else:
            remaining_shapes.append(shape)
    assert [x['shape_id'] for x in removed_shapes] == ['G4_1','G5_1','G5_2','G5_4','G5_8']
    assert len(remaining_shapes)==15
    assert sum(x['labelled_K5_count'] for x in remaining_shapes)==461
    agenda={**old_agenda,
        'scope':'Graph-level necessary candidates after all v14 obstructions, not integer or geometric existence counts.',
        'labelled_nonempty_supports_remaining':461,'unlabelled_shapes_remaining':15,
        'four_vertex_shapes':2,'five_vertex_shapes':13,
        'excluded_counts_in_filter_order':{k:v for k,v in graph_counts.items() if k!='remaining'},
        'intermediate_candidate_counts':[686,521,461],
        'removed_v13_shapes':removed_shapes,'shapes':remaining_shapes}

    source_name='c4_pendant_obstruction_v14.tex'
    source=next(p for p in (HERE/source_name,HERE.parent/'papers/sections/paper'/source_name) if p.is_file())
    result={
        'version':'v14','passed':True,
        'scope':'Exclusion of C4 with a pendant edge in the fixed quintic support, assuming positive integer charts, integer marked clutching, D opposition and nonnegative nodes. No denominator cutoff.',
        'polynomial_identity_count':len(identities),'polynomial_identities':identities,
        'negative_branch_proved_range':'w^2/2 < H(H+1) < 2w^2; w=2,3,4',
        'negative_branch_complete_cases':negative_cases,'negative_branch_models':models,
        'complete_fixed_denominator_count':len(catalogs),
        'complete_nonresonant_model_count':sum(len(d['nonresonant_models']) for d in catalogs.values()),
        'forbidden_coefficients':exclusions,
        'complete_fixed_denominator_catalogs':catalogs,
        'central_C_complete_S_T_cases':c_pairs,
        'central_C_finite_divisor_trials':c_divisor_trials,
        'central_D_z_one_divisor_trials':z_one_trials,
        'central_D_z_one_finite_models':z_one_models,
        'central_D_z_one_other_branches':[
            {'r':2,'S':3,'T':6,'s':'2k','status':'fixed-seven resonance, no two-high continuation by established v13 result'},
            {'r':2,'S':4,'s':1,'T':8,'status':'3 does not divide T'},
            {'r':3,'S':4,'s':'3k','T':'6+(2k+2)/(9k+1)','status':'strictly between6 and7 for all k>=1'},
        ],
        'terminal_infinite_family':{
            'central_q':['4t-1','6t+1',1,1],'t':'every integer t>=1',
            'central_D':[3,-7,'6-t','t-2'],'neighbor_r':2,'neighbor_s':'2t',
            'neighbor_S':3,'neighbor_A':'7t+1','neighbor_B':'6t+7',
            'neighbor_other_q':'7t+8','neighbor_z':'4(t+1)/3','neighbor_T':'21/4',
            'obstruction':'T is not integral, independently of t',
        },
        'remaining_support_agenda':agenda,
        'limitations':[
            'The general node sign argument and exhaustiveness of topological cases are proved in the TeX source; the code supplements that proof.',
            'The fixed-denominator calculation enumerates all proof-derived divisor cases, not a bounded search in q or p.',
            'The maximum partner denominator occurring in the complete finite calculations is a result, not a cutoff.',
            'No other branching cyclic support is excluded by this theorem alone.',
        ],
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'dependency':{'file':DEP.name,'sha256':hashlib.sha256(DEP.read_bytes()).hexdigest()},
        'previous_graph_certificate':{'file':old_path.name,'sha256':hashlib.sha256(old_path.read_bytes()).hexdigest()},
    }
    out=HERE/'c4_pendant_verification_v14.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'polynomial_identities':len(identities),
        'negative_models':len(models),'fixed_denominators':len(catalogs),
        'nonresonant_models':result['complete_nonresonant_model_count'],
        'remaining_support_shapes':15,'remaining_labelled_K5_supports':461,
        'certificate':str(out)}))


if __name__=='__main__':
    main()
