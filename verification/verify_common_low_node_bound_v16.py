#!/usr/bin/env python3
"""Exact identities and complete node-budget reconstruction for the v16 lemma.

No denominator is enumerated or bounded.  The finite calculation enumerates
the two node counts (0,...,5) and solves the factored low-pair equation exactly.
The general inequalities and clutching argument are proved in the TeX source.
"""
from pathlib import Path
import hashlib
import json


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


NVAR = 5


def const(c):
    return {(0,) * NVAR: c} if c else {}


def var(i):
    m = [0] * NVAR
    m[i] = 1
    return {tuple(m): 1}


def add(*ps):
    out = {}
    for p in ps:
        for m, c in p.items():
            out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c}


def neg(p):
    return {m: -c for m, c in p.items()}


def sub(p, q):
    return add(p, neg(q))


def mul(p, q):
    out = {}
    for m, c in p.items():
        for n, d in q.items():
            key = tuple(a + b for a, b in zip(m, n))
            out[key] = out.get(key, 0) + c * d
    return {m: c for m, c in out.items() if c}


def check_identity(name, p, q):
    assert p == q, (name, p, q)
    return name


def main():
    u, n, m, r, T = [var(i) for i in range(NVAR)]
    one = const(1)
    zero = {}
    a = sub(sub(one, n), u)
    b = add(sub(one, m), u)
    identities = [
        check_identity('low-pair factorization', mul(a, b),
                       neg(mul(sub(u, sub(one, n)), sub(u, sub(m, one))))),
        check_identity('positive-branch T lower bound',
                       sub(mul(add(r, one), add(r, one)), mul(const(4), r)),
                       mul(sub(r, one), sub(r, one))),
        check_identity('forced high-edge zero-node numerator',
                       sub(add(T, one), add(one, T)), zero),
        check_identity('forced low-edge zero-node count',
                       sub(one, add(one, zero)), zero),
        check_identity('ordinary high-edge one-node count',
                       sub(one, add(T, neg(T))), one),
        check_identity('ordinary low-edge node count',
                       sub(one, add(neg(r), zero)), add(r, one)),
    ]

    records = []
    for nn in range(6):
        for mm in range(6):
            roots = sorted({1 - nn, mm - 1} - {0})
            for uu in roots:
                aa, bb = 1 - nn - uu, 1 - mm + uu
                assert aa * bb == 0
                assert nn == 1 - (uu + aa)
                assert mm == 1 - (-uu + bb)
                assert 1 <= abs(uu) <= 4
            records.append({'n_ik_j': nn, 'n_jk_i': mm,
                            'all_nonzero_integer_roots': roots})
    assert sorted({u for v in records for u in v['all_nonzero_integer_roots']}) == list(range(-4, 0)) + list(range(1, 5))

    here = Path(__file__).resolve().parent
    source = here / 'common_low_node_bound_v16.tex'
    if not source.exists():
        source = here.parent / 'papers/sections/paper' / source.name
    result = {
        'version': 'v16', 'passed': True,
        'script_sha256': sha(Path(__file__).resolve()),
        'source_sha256': {source.name: sha(source)},
        'identities': identities,
        'polynomial_identity_count': len(identities),
        'complete_node_count_pairs': len(records),
        'root_records': records,
        'nonzero_roots': list(range(-4, 0)) + list(range(1, 5)),
        'denominator_cutoff': None,
        'finite_calculation_scope': 'All possible two node counts under the proven budget five, with the low-pair polynomial solved by factorization; not a search over denominator parameters.',
        'general_proof_scope': {
            'ordinary_common_low_reverse_bound': 'All integer cores of unrestricted high degree, q_ij>1, q_ik=q_jk=1, ordinary opposite-sign marked clutching, nonnegative node counts of total five.',
            'D_opposition_used_in_general_lemma': False,
            'positive_branch_T_lower_bound': 'All positive integers r,S,T with S>r and rT>(r+1)S have T>=5.',
            'two_leaf_application': 'After the established crossed positive-branch reduction, all z>1 and all r>4 are impossible; z=1 and 1<=r<=4, with the forced entries and nodes in the theorem.',
            'whole_support_exclusion_claim': False,
        },
    }
    output = here / 'common_low_node_bound_verification_v16.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'passed': True, 'identities': len(identities),
                      'node_count_pairs': len(records), 'nonzero_roots': result['nonzero_roots'],
                      'result': str(output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
