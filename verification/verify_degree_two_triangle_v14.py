#!/usr/bin/env python3
"""Exact certificate for a triangle with two degree-two high-support vertices.

The proof bounds reverse numerators by four using node conditions.  This code
checks the resulting complete finite cases and the coefficient identities,
not a denominator-bounded search. Opposing-D cancellation is not used.
"""

from fractions import Fraction
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json

HERE = Path(__file__).resolve().parent
DEP_NAME = 'verify_fixed_denominator_partners_v12.py'
for dep in (HERE/DEP_NAME,
            HERE.parents[1]/'deliverables/general_type_surface_fibration_v13/verification'/DEP_NAME):
    if dep.exists():
        spec = importlib.util.spec_from_file_location('tn14_fixed_partner', dep)
        fp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fp)
        break
else:
    raise FileNotFoundError(DEP_NAME)


def motif(edges, vertices=range(5)):
    """Witnesses (i,j,k): ij high, both degrees two, same other neighbor k."""
    adjacency = {i:set() for i in vertices}
    for i,j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    result = []
    for i,j in edges:
        if len(adjacency[i]) == len(adjacency[j]) == 2:
            a = adjacency[i]-{j}
            if a == adjacency[j]-{i}:
                result.append((i,j,next(iter(a))))
    return result


def previous_filter(edges):
    """v13 component exclusions, implemented without geometric assumptions."""
    if not edges:
        return False
    adjacency = {i:set() for i in range(5)}
    for i,j in edges:
        adjacency[i].add(j); adjacency[j].add(i)
    seen = set()
    for start in range(5):
        if start in seen or not adjacency[start]:
            continue
        comp = {start}; stack = [start]
        while stack:
            v = stack.pop()
            for u in adjacency[v]-comp:
                comp.add(u); stack.append(u)
        seen |= comp
        edge_count = sum(len(adjacency[v]) for v in comp)//2
        if edge_count == len(comp)-1:
            return False
        if all(len(adjacency[v]) == 2 for v in comp):
            return False
    return True


def main():
    identities = []
    def identity(name, left, right):
        assert left == right, name
        identities.append(name)

    u,v,l,z,T = [fp.Poly.variable(x) for x in ('u','v','ell','z','T')]
    identity('reverse positive zero-side bound',1-(5+u),-4-u)
    identity('reverse negative zero-side bound',1+(5+u),6+u)
    identity('negative branch r3 S2 rearrangement',
             -u*v-(v-u+1),u*(1-v)-(v+1))
    identity('negative branch r4 S3 rearrangement',
             -7*u*v-2*(v-u+1),u*(2-7*v)-2*(v+1))
    identity('negative branch r4 S2 divisor equation',
             u*l-3*l+u-1,2-(3-u)*(l+1))
    # At a=9,r=2,S=4,s=2, A=11 and 3B=2zT+3z+3.
    identity('terminal cleared high-high pair product',
             11*(2*z*T+3*z+3)-3*(9*(z*T+1)-1),
             9-z*(5*T-33))

    negative_cases = []
    for rr in range(1,5):
        for SS in range(2,5):
            if SS >= rr:
                continue
            H = rr-SS
            E = 1-Fraction(SS*SS,H*(H+1))
            negative_cases.append({'r':rr,'S':SS,'T':SS,'E':str(E)})
    assert [(x['r'],x['S']) for x in negative_cases] == [(3,2),(4,2),(4,3)]
    assert [x['E'] for x in negative_cases] == ['-1','1/3','-7/2']

    # The positive B branch is impossible throughout the proven bounded box.
    B_positive = [(rr,SS,TT) for rr in range(1,4)
                  for SS in range(max(2,rr+1),5) for TT in range(SS,5)
                  if rr*TT > (rr+1)*SS]
    assert B_positive == []
    B_negative = [(rr,SS,SS) for rr in range(1,4) for SS in range(2,rr)]
    assert B_negative == [(3,2,2)]

    # Full divisor equation (3-u)*(ell+1)=2, ell>=1, u>=1.
    small_divisor_trials = []
    for d in fp.positive_divisors(2):
        ell = d-1
        uu = 3-2//d
        small_divisor_trials.append({'ell_plus_one':d,'ell':ell,'u':uu,
                                     'accepted':ell>=1 and uu>=1})
    accepted = [x for x in small_divisor_trials if x['accepted']]
    assert [(x['ell'],x['u']) for x in accepted] == [(1,2)]
    model = fp.model(9,11,4,4,5)
    assert model['S'] == model['T'] == 2
    assert model['p'] == [[0,-7,2,-4],[-14,0,-2,5],[4,-5,0,0],[-2,2,-1,0]]

    terminal_trials = []
    for zz in fp.positive_divisors(9):
        TT = Fraction(33+9//zz,5)
        terminal_trials.append({'z':zz,'T':str(TT),'integral':TT.denominator==1})
    assert not any(t['integral'] for t in terminal_trials)

    # Graph effects are independent of the local coefficient identity checks.
    all_edges = list(itertools.combinations(range(5),2))
    old_count = new_count = motif_count = 0
    for mask in range(1<<len(all_edges)):
        edges = [e for i,e in enumerate(all_edges) if mask & (1<<i)]
        witnesses = motif(edges)
        motif_count += bool(witnesses)
        if previous_filter(edges):
            old_count += 1
            new_count += not bool(witnesses)
    assert old_count == 686

    old_name = 'forest_obstruction_verification_v13.json'
    old_path = next(p for p in (HERE/old_name,
        HERE.parents[1]/'deliverables/general_type_surface_fibration_v13/verification'/old_name)
        if p.exists())
    old = json.loads(old_path.read_text())['remaining_support_agenda']
    removed, retained = [], []
    for shape in old['shapes']:
        witnesses = motif(shape['canonical_edges'])
        row = {**shape,'degree_two_triangle_witnesses':witnesses}
        (removed if witnesses else retained).append(row)
    assert [x['shape_id'] for x in removed] == ['G4_1','G5_1','G5_4','G5_8']
    assert len(retained) == 16
    assert sum(s['labelled_K5_count'] for s in retained) == new_count

    source_name = 'degree_two_triangle_obstruction_v14.tex'
    source = next(p for p in (HERE/source_name,HERE.parent/'paper'/source_name) if p.exists())
    result = {
        'version':'v14','passed':True,
        'scope':'No high-support triangle has two degree-two vertices in the fixed quintic standard model, assuming positive integer charts, integer marked clutching and nonnegative nodes. No D opposition or denominator cutoff is used.',
        'polynomial_identity_count':len(identities),'polynomial_identities':identities,
        'reverse_bound':4,
        'negative_branch_cases':negative_cases,
        'shared_B_positive_cases':B_positive,
        'shared_B_negative_cases':B_negative,
        'small_divisor_trials':small_divisor_trials,
        'unique_negative_branch_model':model,
        'terminal_divisor_trials':terminal_trials,
        'all_labelled_K5_graphs':1<<len(all_edges),
        'all_graphs_containing_motif':motif_count,
        'previous_labelled_candidates':old_count,
        'remaining_labelled_candidates_after_this_theorem':new_count,
        'removed_previous_shapes':removed,
        'remaining_unlabelled_candidates_after_this_theorem':len(retained),
        'remaining_previous_shapes':retained,
        'limitations':['The finite checks supplement the written general proof.',
                       'The graph list records necessary candidates only, not local integer or global geometric existence.',
                       'Other v14 theorems may further reduce this graph list.'],
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'dependency':{'file':dep.name,'sha256':hashlib.sha256(dep.read_bytes()).hexdigest()},
        'previous_graph_certificate':{'file':old_path.name,'sha256':hashlib.sha256(old_path.read_bytes()).hexdigest()},
    }
    out = HERE/'degree_two_triangle_verification_v14.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'identities':len(identities),
                      'removed_graph_types':[x['shape_id'] for x in removed],
                      'remaining_graph_types':len(retained),'remaining_labelled_graphs':new_count,
                      'certificate':str(out)}))


if __name__ == '__main__':
    main()
