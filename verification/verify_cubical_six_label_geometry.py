#!/usr/bin/env python3
"""Exact finite checks for the six-label diameter proof (standard library).

The proof of the coordinate retraction and all-degree conclusion is analytic
and remains in the manuscript. This script independently unfolds the four
square galleries from their vertex incidences and checks the PL calibration
on all 120 triangles of C_6. No floating-point optimization is used.
"""

from fractions import Fraction
from itertools import combinations, permutations


def square_vertices(square):
    p, q, r = square
    assert len({p, q, r}) == 3
    return {
        frozenset({p} | ({q} if a else set()) | ({r} if b else set())): (a, b)
        for a in (0, 1)
        for b in (0, 1)
    }


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def center(placement):
    return tuple(sum(p[i] for p in placement.values()) / 4 for i in (0, 1))


def unfold_next(previous, placement, following):
    """Use the shared labelled edge and put the new square on its other side."""
    old_vertices = square_vertices(previous)
    new_vertices = square_vertices(following)
    shared = list(old_vertices.keys() & new_vertices.keys())
    assert len(shared) == 2, (previous, following, shared)
    v0, v1 = shared
    b0, b1 = new_vertices[v0], new_vertices[v1]
    changed = [i for i in (0, 1) if b0[i] != b1[i]]
    assert len(changed) == 1
    variable = changed[0]
    fixed = 1 - variable
    edge = scale(Fraction(1, b1[variable] - b0[variable]), sub(placement[v1], placement[v0]))
    assert dot(edge, edge) == 1
    normal = (-edge[1], edge[0])
    midpoint = scale(Fraction(1, 2), add(placement[v0], placement[v1]))
    old_side = dot(sub(center(placement), midpoint), normal)
    assert old_side != 0
    if old_side > 0:
        normal = scale(-1, normal)
    result = {}
    for vertex, bits in new_vertices.items():
        along = scale(bits[variable] - b0[variable], edge)
        across = scale(abs(bits[fixed] - b0[fixed]), normal)
        result[vertex] = add(placement[v0], add(along, across))
    for vertex in shared:
        assert result[vertex] == placement[vertex]
    for v, w in combinations(new_vertices, 2):
        assert dot(sub(result[v], result[w]), sub(result[v], result[w])) == dot(
            sub(new_vertices[v], new_vertices[w]), sub(new_vertices[v], new_vertices[w])
        )
    return result


GALLERIES = {
    "LLLD": [(1, 2, 3), (1, 3, 4), (4, 1, 3), (4, 3, 6), (4, 5, 6)],
    "LLDL": [(1, 2, 3), (1, 3, 4), (4, 1, 3), (4, 1, 5), (4, 5, 6)],
    "LDLL": [(1, 2, 3), (1, 3, 4), (1, 4, 5), (4, 1, 5), (4, 5, 6)],
    "DLLL": [(1, 2, 3), (1, 2, 5), (1, 4, 5), (4, 1, 5), (4, 5, 6)],
}


def check_galleries():
    expected_words = {"L" * k + "D" + "L" * (3 - k) for k in range(4)}
    assert set(GALLERIES) == expected_words
    for word, gallery in GALLERIES.items():
        placement = {v: tuple(map(Fraction, bits)) for v, bits in square_vertices(gallery[0]).items()}
        for letter, old, new in zip(word, gallery, gallery[1:]):
            previous_center = center(placement)
            placement = unfold_next(old, placement, new)
            assert sub(center(placement), previous_center) == ({"L": (-1, 0), "D": (0, -1)}[letter])
        for vertex, (c, e) in square_vertices(gallery[-1]).items():
            assert placement[vertex] == (-2 - e, -c), (word, vertex, placement[vertex])
    print("PASS: all four shuffles are edge-adjacent isometric galleries, endpoint (-2-e,-c)")


VALUES = {
    (3, 0): -5, (2, 0): -3, (1, 0): -2,
    (2, 1): -1, (1, 1): 0, (1, 2): 1,
    (0, 1): 2, (0, 2): 3, (0, 3): 5,
}


def check_calibration():
    first = {1, 2, 3}
    last = {4, 5, 6}

    def value(vertices):
        return VALUES[(len(vertices & first), len(vertices & last))]

    triangles = 0
    types = set()
    for i, j, k in permutations(range(1, 7), 3):
        v0, v1, v2 = frozenset({i}), frozenset({i, j}), frozenset({i, j, k})
        dx, dy = value(v1) - value(v0), value(v2) - value(v1)
        assert dx * dx + dy * dy == 5, (i, j, k, dx, dy)
        types.add(tuple("A" if v in first else "B" for v in (i, j, k)))
        triangles += 1
    assert triangles == 120 and len(types) == 8
    assert (value(last) - value(first)) ** 2 == 100
    assert Fraction((value(last) - value(first)) ** 2, 5) == 20
    squares = [(p, q, r) for p in range(1, 7) for q, r in combinations(set(range(1, 7)) - {p}, 2)]
    assert len(squares) == 60
    print("PASS: calibration gradient squared is 1 on all 120 triangles (8 label types)")
    print("PASS: endpoint calibration gap squared is 20; C_6 has 60 squares")


if __name__ == "__main__":
    check_galleries()
    check_calibration()
    print("These finite checks do not verify KE estimates, relative core gluing, or global GH convergence.")
