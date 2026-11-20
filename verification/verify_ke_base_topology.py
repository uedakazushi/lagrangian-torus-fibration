#!/usr/bin/env python3
"""Finite checks for Lagrangian base B(T) and KE cubical candidate C_d.

Mod 1000003 for d=5..8; numerical regression only, not a proof of
the all-d theorem, metric convergence or symplectic constructions.
Python standard library only.
"""
from itertools import combinations, permutations
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



def check_petersen_factorizations():
    """Exact finite enumeration of the six labelled K6 one-factorizations."""
    vertices = tuple(range(6))
    complete_edges = frozenset(combinations(vertices, 2))

    def matchings(v):
        if not v:
            yield frozenset()
            return
        a, *remaining = v
        for b in remaining:
            for rest in matchings([x for x in remaining if x != b]):
                yield rest | frozenset({tuple(sorted((a, b)))})

    perfect = sorted(set(matchings(list(vertices))), key=lambda m: sorted(m))
    assert len(perfect) == 15
    factorizations = []
    for choice in combinations(range(15), 5):
        blocks = frozenset(perfect[i] for i in choice)
        if frozenset().union(*blocks) == complete_edges:
            factorizations.append(blocks)
    assert len(factorizations) == 6
    reference = factorizations[0]

    def relabel(permutation, system):
        return frozenset(
            frozenset(tuple(sorted((permutation[a], permutation[b])))
                      for a, b in block)
            for block in system
        )

    orbit = {relabel(permutation, reference)
             for permutation in permutations(vertices)}
    assert orbit == set(factorizations)
    stabilizer_order = sum(
        relabel(permutation, reference) == reference
        for permutation in permutations(vertices)
    )
    assert stabilizer_order == 120
    print("K6: 15 matchings, 6 one-factorizations, one S6 orbit, "
          "stabilizer order 120 PASS")


def check_threefold_euler_budget():
    """Check Chern/Euler and complement subtraction; not a fibration existence test."""
    for d in range(6, 13):
        euler_threefold = d * (10 - 10*d + 5*d*d - d**3)
        local_block = -(d - 2) * (d - 5)
        complement = euler_threefold - local_block
        negative_complement = d**4 - 5*d**3 + 9*d*d - 3*d - 10
        assert complement == -negative_complement
        assert negative_complement > 0
        assert (d - 2) * (d - 5) % 2 == 0
        if d == 6:
            assert (euler_threefold, local_block, complement) == (-516, -4, -512)
        print(f"d={d}: chi(X)={euler_threefold}, chi(U)={local_block}, "
              f"chi(V)={complement} PASS")


def check_tubular_and_focus_boundary():
    """Arithmetic checks for the Thom LES and the focus Wang sequence.

    These checks do not prove the underlying geometric identifications
    N(C), K_c or their boundary monodromy.
    """
    monodromy = ((1, 1), (0, 1))
    difference = ((monodromy[0][0] - 1, monodromy[0][1]),
                  (monodromy[1][0], monodromy[1][1] - 1))
    assert difference == ((0, 1), (0, 0))
    # One primitive nonzero invariant factor: coker(M-I)=Z,
    # so H_1(boundary focus)=Z^2 and H_2(boundary focus)=Z^2.
    for d in range(6, 13):
        e = d - 2
        genus = (d - 3) * (d - 4) // 2
        euler_x = d * (10 - 10 * d + 5 * d * d - d ** 3)
        middle_rank = 4 - euler_x
        chi_tubular_complement = 2 - middle_rank + 2 * genus
        chi_focus_complement = euler_x + (d - 2) * (d - 5)
        assert chi_tubular_complement == chi_focus_complement
        # Explicit retract K_c ~ S1 wedge S2 and the relative duality
        # computation predict the ACTUAL focus complement free ranks:
        actual_betti = (1, 1, 2 * genus + 2,
                        middle_rank + 2 * genus + 1, 2 * genus + 1, 0)
        assert sum((-1)**i * b for i, b in enumerate(actual_betti)) \
               == chi_focus_complement
        # The relative H_4(X)->H^2(C x K_c) map is multiplication by e
        # in its first summand; the torsion order remains e, but its
        # representative is {point} x boundary(K_c), not a small S^3.
        if d == 6:
            assert actual_betti == (1, 1, 8, 527, 7, 0)
        # Thom LES: H_4(X)=Z --times e--> H_0(C)=Z,
        # so meridional H_3 torsion order is e.
        assert e > 0
        focus_boundary_betti = (
            1, 2 * genus + 2, 4 * genus + 3,
            4 * genus + 3, 2 * genus + 2, 1,
        )
        assert sum((-1) ** i * b
                   for i, b in enumerate(focus_boundary_betti)) == 0
        if d == 6:
            assert (e, middle_rank, genus, chi_tubular_complement) == (
                4, 520, 3, -512,
            )
            assert focus_boundary_betti == (1, 8, 15, 15, 8, 1)
        print(f"d={d}: tubular H3 torsion=Z/{e}, "
              f"b3(X)={middle_rank}, focus boundary betti="
              f"{focus_boundary_betti} PASS")

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
    check_petersen_factorizations()
    check_threefold_euler_budget()
    check_tubular_and_focus_boundary()
    print("Finite mod-p checks and exact K6 enumeration passed; "
          "general proof and metric collapse are in the manuscripts.")


if __name__ == "__main__":
    main()
