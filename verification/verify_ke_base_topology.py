#!/usr/bin/env python3
"""Finite checks for Lagrangian base B(T) and KE cubical candidate C_d.

Mod 1000003 for d=5..8; numerical regression only, not a proof of
the all-d theorem, metric convergence or symplectic constructions.
Python standard library only.
"""
from itertools import combinations
from math import comb

P = 1000003


def rank(columns, nrows):
    matrix = [[0] * len(columns) for _ in range(nrows)]
    for j, column in enumerate(columns):
        for i, value in column.items():
            matrix[i][j] = value % P
    r = 0
    for j in range(len(columns)):
        pivot = next((i for i in range(r, nrows) if matrix[i][j]), None)
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        inverse = pow(matrix[r][j], -1, P)
        matrix[r] = [(x * inverse) % P for x in matrix[r]]
        for i in range(r + 1, nrows):
            if matrix[i][j]:
                x = matrix[i][j]
                matrix[i] = [(y - x * z) % P for y, z in zip(matrix[i], matrix[r])]
        r += 1
        if r == nrows:
            break
    return r


def lagrangian_base(d):
    pairs = list(combinations(range(d), 2))
    edges, faces, attach = [], [], {}
    for i, j in pairs:
        leaves = [z for z in range(d) if z not in (i, j)]
        n = len(leaves) - 2
        edges.extend((i, j, a) for a in range(n))
        faces.extend(("bigon", ((i, j, a), (i, j, a + 1)))
                     for a in range(n - 1))
        attach[i, j] = {
            z: 0 if t < 2 else n - 1 if t >= len(leaves) - 2 else t - 1
            for t, z in enumerate(leaves)
        }
    for i, j, k in combinations(range(d), 3):
        faces.append(("triangle", ((i, j, attach[i, j][k]),
                                   (j, k, attach[j, k][i]),
                                   (i, k, attach[i, k][j]))))
    index = {e: t for t, e in enumerate(edges)}
    d1 = [{i: -1, j: 1} for i, j, _ in edges]
    d2 = []
    for typ, cells in faces:
        if typ == "bigon":
            a, b = cells
            d2.append({index[a]: -1, index[b]: 1})
        else:
            a, b, c = cells
            d2.append({index[a]: 1, index[b]: 1, index[c]: -1})
    for col in d2:
        boundary = {}
        for edge, value in col.items():
            for vertex, coeff in d1[edge].items():
                boundary[vertex] = boundary.get(vertex, 0) + value * coeff
        assert all(x == 0 for x in boundary.values()), "d1*d2 != 0"
    r1, r2 = rank(d1, d), rank(d2, len(edges))
    return len(edges), len(faces), len(edges) - r1 - r2, len(faces) - r2


def simplex_2_skeleton(d):
    edges = list(combinations(range(d), 2))
    triangles = list(combinations(range(d), 3))
    index = {e: k for k, e in enumerate(edges)}
    d1 = [{i: -1, j: 1} for i, j in edges]
    d2 = [{index[j, k]: 1, index[i, k]: -1, index[i, j]: 1}
          for i, j, k in triangles]
    r1, r2 = rank(d1, d), rank(d2, len(edges))
    return len(edges) - r1 - r2, len(triangles) - r2


def main():
    for d in range(5, 9):
        e, f, b1, b2 = lagrangian_base(d)
        v_c = sum(comb(d, k) for k in (1, 2, 3))
        e_c, f_c = d * comb(d, 2), d * comb(d - 1, 2)
        h1, h2 = simplex_2_skeleton(d)
        assert (e, f) == (comb(d, 2) * (d - 4),
                          comb(d, 3) + comb(d, 2) * (d - 5))
        assert (b1, b2, h1, h2) == (0, comb(d - 1, 3), 0, comb(d - 1, 3))
        assert v_c - e_c + f_c == 1 + comb(d - 1, 3)
        print(f"d={d}: B=(V={d}, E={e}, F={f}, b1={b1}, b2={b2}), "
              f"C=(V={v_c}, E={e_c}, F={f_c}, b1={h1}, b2={h2}) PASS")
    print("Finite mod-p checks passed; general proof is in the manuscripts.")


if __name__ == "__main__":
    main()
