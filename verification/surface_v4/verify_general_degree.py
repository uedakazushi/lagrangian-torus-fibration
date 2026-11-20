#!/usr/bin/env python3
"""Exact consistency checks for d=5,...,12; see progress_04.tex for proofs.

Standard library only. These computations do not check symplectic gluing.
"""
import json
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations
from math import comb, prod
from pathlib import Path


def evaluate(poly, value):
    return sum(coefficient * value**i for i, coefficient in enumerate(poly))


perms = [(p, (-1)**sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4)))
         for p in permutations(range(4))]


def det4(mat):
    return sum(sign * prod(mat[i][p[i]] for i in range(4)) for p, sign in perms)


def integer_rank(columns):
    """Exact sparse elimination. All nonzero pivots must be units in Z."""
    basis = {}
    for source in columns:
        col = {r: c for r, c in source.items() if c}
        while col:
            p = min(col)
            coefficient = col[p]
            if p not in basis:
                assert abs(coefficient) == 1
                basis[p] = {r: c // coefficient for r, c in col.items()}
                break
            for r, c in basis[p].items():
                value = col.get(r, 0) - coefficient * c
                if value:
                    col[r] = value
                else:
                    col.pop(r, None)
    return len(basis)


def tree(leaves):
    """Leaf adjacency for the labelled caterpillar with len(leaves)-2 saddles."""
    n = len(leaves)
    if n == 3:
        return {leaf: 0 for leaf in leaves}
    adj = {leaves[0]: 0, leaves[1]: 0, leaves[-2]: n-3, leaves[-1]: n-3}
    for r in range(2, n-2):
        adj[leaves[r]] = r-1
    return adj


def check_base(d):
    labels = list(range(1, d+1))
    pairs = list(combinations(labels, 2))
    trees = {ij: tree([k for k in labels if k not in ij]) for ij in pairs}
    edges = [(i, j, p) for i, j in pairs for p in range(d-4)]
    index = {edge: r for r, edge in enumerate(edges)}
    b1 = [{i-1: -1, j-1: 1} for i, j, _ in edges]
    bigons = [{index[i, j, p]: 1, index[i, j, p+1]: -1}
              for i, j in pairs for p in range(d-5)]
    triangles = [{index[i, j, trees[i, j][k]]: 1,
                  index[j, k, trees[j, k][i]]: 1,
                  index[i, k, trees[i, k][j]]: -1}
                 for i, j, k in combinations(labels, 3)]
    b2 = bigons + triangles
    incidence = Counter()
    for face in b2:
        boundary = Counter()
        for edge, sign in face.items():
            incidence[edge] += 1
            for vertex, coefficient in b1[edge].items():
                boundary[vertex] += sign * coefficient
        assert all(value == 0 for value in boundary.values())
    assert len(incidence) == len(edges) and set(incidence.values()) == {3}
    assert len(bigons) == comb(d, 2)*(d-5) and len(triangles) == comb(d, 3)
    r1, r2 = integer_rank(b1), integer_rank(b2)
    betti = [d-r1, len(edges)-r1-r2, len(b2)-r2]
    assert betti == [1, 0, comb(d-1, 3)]
    assert integer_rank(bigons) == len(bigons)
    links = []
    for i in labels:
        vertices = [(j, p) for j in labels if j != i for p in range(d-4)]
        link_edges = [((j, p), (j, p+1))
                      for j in labels if j != i for p in range(d-5)]
        for j, k in combinations([j for j in labels if j != i], 2):
            ij, ik = tuple(sorted((i, j))), tuple(sorted((i, k)))
            link_edges.append(((j, trees[ij][k]), (k, trees[ik][j])))
        adjacency = {v: [] for v in vertices}
        for u, v in link_edges:
            adjacency[u].append(v)
            adjacency[v].append(u)
        assert all(len(neighbors) == 3 for neighbors in adjacency.values())
        reached, pending = {vertices[0]}, [vertices[0]]
        while pending:
            for v in adjacency[pending.pop()]:
                if v not in reached:
                    reached.add(v)
                    pending.append(v)
        assert len(reached) == len(vertices)
        assert len(link_edges)-len(vertices)+1 == comb(d-2, 2)
        links.append({'vertex': i, 'V': len(vertices), 'E': len(link_edges),
                      'b1': comb(d-2, 2)})
    return {'vertices': d, 'branch_edges': len(edges), 'triangles': len(triangles),
            'bigons': len(bigons), 'boundary_ranks': [r1, r2], 'betti': betti,
            'face_sectors_per_edge': 3, 'vertex_links': links}


def main():
    for pars in combinations(range(1, 25), 4):
        mat = [[1, z, z*z, z*z*z] for z in pars]
        vandermonde = prod(pars[j]-pars[i] for i in range(4) for j in range(i+1, 4))
        assert det4(mat) == vandermonde > 0
    out = {'scope': 'Finite exact checks; general proofs are in progress_04.tex.',
           'checks': ['Vandermonde determinants', 'node and triple coordinates',
                      'Bezout lower bounds and double-curve areas', 'sum of squares',
                      'three sectors per branch edge', 'integer boundary matrices',
                      'unimodular pivots', 'connected trivalent vertex links',
                      'Euler and geometric-genus identities'], 'degrees': []}
    for d in range(5, 13):
        nodes = []
        for i, j in combinations(range(1, d+1), 2):
            for r in range(d+1, 2*d+1):
                coords = (-i*j*r, i*j+i*r+j*r, -i-j-r, 1)
                assert all(evaluate(coords, s) == 0 for s in (i, j, r))
                assert all(evaluate(coords, k) != 0
                           for k in range(1, 2*d+1) if k not in (i, j, r))
                nodes.append(coords)
        assert len(nodes) == len(set(nodes)) == d*comb(d, 2)
        for i, j, k in combinations(range(1, d+1), 3):
            coords = (-i*j*k, i*j+i*k+j*k, -i-j-k, 1)
            assert all(evaluate(coords, r) != 0 for r in range(d+1, 2*d+1))
        squares = []
        for i in range(1, d+1):
            n = d-i
            linear = d*(d+1)//2-d*i
            square = [1, 2*linear, linear**2-d*sum(r*r for r in range(1, n+1))]
            assert linear-sum(range(1, n+1)) == -comb(i, 2)
            for j in range(i+1, d+1):
                assert linear-d*(j-i) == d*(d+1)//2-d*j
            value = evaluate(square, Q(1, comb(d, 2)))
            assert (value > 0) if i < d else (value == 0)
            coefficient = d*d*n*n-d*sum(r*r for r in range(1, n+1))
            assert coefficient >= d*n*n*(d-n)
            squares.append(square)
        assert [sum(q[k] for q in squares) for k in range(3)] == [d, 0, 0]
        assert comb(d, 2)-sum(range(1, d)) == 0  # area of each compact Q_r is a
        euler = d*(d*d-4*d+6)
        assert d*comb(d-3, 2)+len(nodes) == euler
        out['degrees'].append({
            'd': d, 'double_curves': comb(d, 2), 'triple_points': comb(d, 3),
            'nodes': len(nodes), 'component_blowups': [d*(d-i) for i in range(1, d+1)],
            'core_euler': comb(d-3, 2), 'total_euler': euler,
            'K_squared': d*(d-4)**2, 'pg': comb(d-1, 3),
            'component_square_coefficients_in_epsilon_over_a': squares,
            'base': check_base(d)})
    path = Path(__file__).with_name('general_degree_results.json')
    path.write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'checks': 'all passed', 'degrees': list(range(5, 13)),
                      'output': str(path)}))


if __name__ == '__main__':
    main()
