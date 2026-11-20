#!/usr/bin/env python3
"""Exact finite-field checks for the v11 dense prime-support theorem.

The unbounded-prime proof is in dense_prime_support_v11.tex.  This program
checks the explicit F_5 witnesses, exhausts all F_5 completions of K_1 join
P_4, and checks the rational seven-edge formulas in selected prime fields.
It asserts neither integral lifting nor geometric realizability.
Only the Python standard library is used.
"""

from itertools import combinations, product
from math import gcd
import hashlib
import json
from pathlib import Path

V = tuple(range(5))
EDGES = tuple(combinations(V, 2))


def edge(i, j):
    return tuple(sorted((i, j)))


def inverse(x, prime):
    assert x % prime
    return pow(x, -1, prime)


def matrix_from_rows(labels, rows, scale, prime):
    return {(i, j): (scale * rows[a][b]) % prime
            for a, i in enumerate(labels) for b, j in enumerate(labels)
            if i != j}


def verify_global(q, cores, prime, check_defects=False):
    """Clutching modulo prime is required only on prime-divisible q edges."""
    for i in V:
        others = [j for j in V if j != i]
        p = cores[i]
        for j in others:
            assert (sum(p[j, k] for k in others if k != j)
                    + q[edge(i, j)]) % prime == 0
        for j, k in combinations(others, 2):
            assert (p[j, k] * p[k, j]
                    - q[edge(i, j)] * q[edge(i, k)] + 1) % prime == 0
    for i, j in EDGES:
        if q[i, j] % prime == 0:
            for k in V:
                if k not in (i, j):
                    assert (cores[i][j, k] + cores[j][i, k]) % prime == 0
        if check_defects:
            di = -q[i, j] - sum(cores[i][k, j] for k in V if k not in (i, j))
            dj = -q[i, j] - sum(cores[j][k, i] for k in V if k not in (i, j))
            assert (di + dj) % prime == 0


BASE_O = [[0, -2, 1, 1], [-2, 0, 1, 1],
          [-1, -1, 0, 2], [-1, -1, 2, 0]]
BASE_OUTER = [[0, 2, -1, -1], [2, 0, 2, 2],
              [1, 2, 0, 2], [1, 2, 2, 0]]


def k221_witness(o, left, right, sign):
    a, b = left
    c, d = right
    q = {ij: 0 for ij in EDGES}
    q[edge(a, b)] = -sign % 5
    q[edge(c, d)] = sign % 5
    cores = {o: matrix_from_rows((a, b, c, d), BASE_O, sign, 5)}
    for x, partner in ((a, b), (b, a)):
        cores[x] = matrix_from_rows((o, partner, c, d), BASE_OUTER, sign, 5)
    for x, partner in ((c, d), (d, c)):
        cores[x] = matrix_from_rows((o, partner, a, b), BASE_OUTER, -sign, 5)
    return q, cores


def encode(q, cores):
    return {'q': {f'{i}{j}': q[i, j] for i, j in EDGES},
            'cores': {str(i): {f'{j}{k}': cores[i][j, k]
                              for j, k in sorted(cores[i])} for i in V}}


def local_completions(core, q, p_o, prime=5):
    """Exhaust every local matrix, with its row at branch o=0 fixed.

    At core i, all entries incident to local branch 0 are forced by
    clutching with core 0 and the determinant -1.  The other three
    unordered pairs are enumerated over all prime^2 residue pairs with
    their prescribed product, including both zero orientations.
    """
    rest = [j for j in V if j not in (0, core)]
    fixed = {}
    for j in rest:
        fixed[0, j] = -p_o[core, j] % prime
        fixed[j, 0] = -inverse(fixed[0, j], prime) % prime
    pairs = list(combinations(rest, 2))
    choices = []
    for j, k in pairs:
        target = (q[edge(core, j)] * q[edge(core, k)] - 1) % prime
        choices.append([(a, b) for a in range(prime) for b in range(prime)
                        if a * b % prime == target])
    result = []
    for values in product(*choices):
        p = dict(fixed)
        for (j, k), (a, b) in zip(pairs, values):
            p[j, k], p[k, j] = a, b
        if all((sum(p[j, k] for k in V if k not in (core, j))
                + q[edge(core, j)]) % prime == 0
               for j in V if j != core):
            result.append(p)
    return result


def all_path_completions():
    # o=0; path a-b-c-d = 1-2-3-4.  The core-o matrix follows from
    # the triangle signs and row sums.  q_ac and q_bd are nonzero by K4.
    rows = [[0, 1, 3, 1], [4, 0, 4, 2],
            [3, 1, 0, 1], [4, 2, 4, 0]]
    records = []
    tested = 0
    locally_nonempty = 0
    for sign in (1, -1):
        p_o = matrix_from_rows((1, 2, 3, 4), rows, sign, 5)
        for x, y, z in product(range(1, 5), range(5), range(1, 5)):
            tested += 1
            q = {ij: 0 for ij in EDGES}
            q[1, 3], q[1, 4], q[2, 4] = x, y, z
            lists = [local_completions(i, q, p_o) for i in range(1, 5)]
            if not all(lists):
                continue
            locally_nonempty += 1
            for rest in product(*lists):
                cores = {0: p_o, **{i: p for i, p in zip(range(1, 5), rest)}}
                compatible = all(
                    (cores[i][j, k] + cores[j][i, k]) % 5 == 0
                    for i, j in EDGES if q[i, j] == 0
                    for k in V if k not in (i, j))
                if compatible:
                    verify_global(q, cores, 5, check_defects=True)
                    records.append({'sign': sign, **encode(q, cores)})
    assert tested == 160
    assert len(records) == 2
    assert all(record['q']['14'] == 0 for record in records)
    return {'tested_q_and_sign_assignments': tested,
            'assignments_with_all_local_completions': locally_nonempty,
            'global_mod5_solutions': len(records),
            'exact_seven_edge_solutions': 0,
            'solutions': records}


def seven_edge_field_check(prime):
    # H = K_{2,3}+cd with (a,b,c,d,e)=(0,1,2,3,4), sign normalized to 1.
    inv = lambda x: inverse(x, prime)
    half = inv(2)
    records = []
    for u, v in product(range(1, prime), repeat=2):
        if any(t % prime == 0 for t in (1-u, 1+u, 1-v, 1+v, u+v)):
            continue
        # Core-e pair ab is equivalent to (uv+1)^2=0.
        if ((u+v)**2 + (1-u*u)*(1-v*v)) % prime:
            continue
        xa = -(inv(u)+inv(v)+(1-u)*(1+v)*inv(u+v)) % prime
        xb = (u+v-(1+u)*(1-v)*inv(u+v)) % prime
        if xa != xb:
            continue
        y = (inv(1-u) + u*inv(1+u) - half) % prime
        z = (-inv(1+v) + v*inv(1-v) + half) % prime
        assert v == u and u*u % prime == prime-1
        assert (xa-3*u) % prime == 0
        assert (y-u-half) % prime == 0 and (z-u+half) % prime == 0
        residual = ((u-5*half)*(u+5*half) - (y*z-1)) % prime
        assert residual == -5 % prime
        if residual:
            continue
        q = {ij: 0 for ij in EDGES}
        q[0, 1], q[2, 4], q[3, 4] = xa, y, z
        assert prime == 5 and (y == 0) != (z == 0)
        records.append({'u': u, 'v': v, 'q_ab': xa, 'q_ce': y, 'q_de': z})
    return {'prime': prime, 'solutions_before_exact_support_requirement': records,
            'exact_seven_edge_solutions': 0}


def seven_edge_mod25_check():
    """Retain nonzero square-zero elements; do not infer r=0 from r^2=0."""
    modulus = 25
    inv = lambda a: pow(a, -1, modulus)
    half = inv(2)
    records = []
    for u, v in product(range(modulus), repeat=2):
        if any(gcd(t, modulus) != 1 for t in
               (u, v, 1-u, 1+u, 1-v, 1+v, u+v)):
            continue
        r = (u*v+1) % modulus
        if r*r % modulus:
            continue
        xa = -(inv(u)+inv(v)+(1-u)*(1+v)*inv(u+v)) % modulus
        xb = (u+v-(1+u)*(1-v)*inv(u+v)) % modulus
        if xa != xb:
            continue
        a = 2*u*inv(1-u*u) % modulus
        b = 2*v*inv(1-v*v) % modulus
        c = (u-inv(u)-a) % modulus
        d = (v-inv(v)-b) % modulus
        assert a == b == c == d
        y, z = (a+half) % modulus, (b-half) % modulus
        residual = ((c-5*half)*(d+5*half)-y*z+1) % modulus
        assert residual == 20
        records.append({'u': u, 'v': v, 'square_zero_r': r,
                        'q_ab': xa, 'q_ce': y, 'q_de': z,
                        'last_determinant_residual': residual})
    assert len(records) == 10
    assert any(record['square_zero_r'] != 0 for record in records)
    return {'modulus': 25, 'candidates_before_last_determinant': len(records),
            'solutions': 0, 'candidates': records,
            'nonzero_square_zero_elements_retained': True}


def main():
    witnesses = []
    for o in V:
        rest = [i for i in V if i != o]
        a = rest[0]
        for b in rest[1:]:
            right = tuple(i for i in rest if i not in (a, b))
            for sign in (1, -1):
                q, cores = k221_witness(o, (a, b), right, sign)
                verify_global(q, cores, 5, check_defects=True)
                witnesses.append({'singleton': o, 'left': [a, b],
                                  'right': list(right), 'sign': sign,
                                  **encode(q, cores)})
    assert len(witnesses) == 30
    assert len({json.dumps(w['q'], sort_keys=True) for w in witnesses}) == 30
    report = {
        'status': 'passed',
        'scope': 'Exact finite-field verification only; no integral or geometric lifting claim.',
        'unbounded_prime_proof': 'dense_prime_support_v11.tex',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'k221_labelled_supports': 15,
        'k221_signed_witnesses': len(witnesses),
        'k221_all_rows_determinants_zero_edge_clutching_and_defects_verified': True,
        'path_completion_exhaustion': all_path_completions(),
        'seven_edge_field_checks': [seven_edge_field_check(p) for p in
                                   (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)],
        'seven_edge_mod25_check': seven_edge_mod25_check(),
        'witnesses': witnesses,
    }
    output = Path(__file__).with_name('dense_prime_support_verification_v11.json')
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'output': str(output),
                      'witnesses': len(witnesses),
                      'path_solutions': report['path_completion_exhaustion']['global_mod5_solutions']},
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
