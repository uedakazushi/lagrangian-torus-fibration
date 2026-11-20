#!/usr/bin/env python3
"""Exact arithmetic for the quintic note; does not verify symplectic gluing."""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
import json
from pathlib import Path

def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p

def remainder(a, b):
    a, b = trim(list(map(Q, a))), trim(list(map(Q, b)))
    while len(a) >= len(b):
        shift, factor = len(a) - len(b), a[-1] / b[-1]
        for j, value in enumerate(b):
            a[shift + j] -= factor * value
        a = trim(a)
    return a

def gcd(a, b):
    while b:
        a, b = b, remainder(a, b)
    return [x / a[-1] for x in a]

def rank(matrix):
    a = [list(map(Q, row)) for row in matrix]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        factor = a[row][col]
        a[row] = [x / factor for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                factor = a[i][col]
                a[i] = [x - factor * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row

def check_polynomial(edge, coefficients):
    p = list(map(Q, coefficients))
    derivative = [k * p[k] for k in range(1, len(p))]
    assert gcd(p, derivative) == [Q(1)]
    values = [p[0], sum(v * (-1)**k for k, v in enumerate(p)), p[-1]]
    assert all(values)
    return {
        "edge": edge,
        "coefficients_low_to_high": [int(x) for x in coefficients],
        "gcd_with_derivative": "1",
        "values_at_three_triple_points_in_chosen_trivializations": list(map(str, values)),
    }

def main():
    weights = [1, 2, 3, 4]
    lines = []
    for i, j in combinations(range(4), 2):
        k, ell = [n for n in range(4) if n not in (i, j)]
        p = [weights[ell], 0, 0, 0, 0, weights[k]]
        lines.append(check_polynomial([i+1, j+1], p))
    for i in range(4):
        j, k, ell = [n for n in range(4) if n != i]
        p = [-weights[ell] * comb(5, n) for n in range(6)]
        p[0] += weights[k]
        p[5] += weights[j]
        lines.append(check_polynomial([i+1, 5], p))
    assert len(lines) == 10

    # Normalize the area of a projective line in the nearby fiber to one.
    eps = Q(1, 100)
    heights = [(i-2)*eps for i in range(5)]
    a = [1 - 5*x for x in heights]
    counts = [5*(4-i) for i in range(5)]
    squares = [
        a[i]**2 - 5*sum((heights[j]-heights[i])**2 for j in range(i+1, 5))
        for i in range(5)
    ]
    bezout_bounds = [a[i] - eps*sum(range(1, 5-i)) for i in range(5)]
    assert all(x > 0 for x in squares + a + bezout_bounds)
    edge_areas = []
    for i, j in combinations(range(5), 2):
        exceptional_area = heights[j] - heights[i]
        from_i, from_j = a[i] - 5*exceptional_area, a[j]
        assert exceptional_area > 0 and from_i == from_j
        assert (1-5) + 1 + 3 == 0
        edge_areas.append({
            "edge": [i+1, j+1],
            "double_curve_area": str(from_i),
            "area_of_each_of_five_exceptional_curves": str(exceptional_area),
            "self_intersections": [-4, 1],
            "triple_points": 3,
        })
    assert sum(squares) == 5
    assert sum(1+n for n in counts) == 55
    compact_curve_area = 5*a[0] - 5*sum(heights[j]-heights[0] for j in range(1, 5))
    assert compact_curve_area == 5

    # Exact positivity certificates on 0 < u = epsilon/a < 1/10.
    # With x=10u, the degree-two Bernstein basis is
    # (1-x)^2, 2x(1-x), x^2. Nonnegative coefficients and b0>0
    # imply strict positivity for 0<=x<1.
    parameter_squares = []
    bernstein_certificates = []
    parameter_bezout = []
    for i in range(5):
        slope = -5*(i-2)
        quadratic = slope**2 - 5*sum(k*k for k in range(1, 5-i))
        coefficients = [Q(1), Q(2*slope), Q(quadratic)]
        parameter_squares.append(coefficients)
        c0, c1, c2 = coefficients[0], coefficients[1]/10, coefficients[2]/100
        bernstein = [c0, c0+c1/2, c0+c1+c2]
        assert bernstein[0] > 0 and all(b >= 0 for b in bernstein)
        bernstein_certificates.append(bernstein)
        parameter_bezout.append(slope-sum(range(1, 5-i)))
    assert [sum(p[k] for p in parameter_squares) for k in range(3)] == [5, 0, 0]
    assert parameter_bezout == [0, -1, -3, -6, -10]

    four_line_intersection_rank = rank([[1]*4 for _ in range(4)])
    four_line_graph_b1 = 6-4+1
    assert four_line_intersection_rank == 1
    assert four_line_graph_b1 + 4-four_line_intersection_rank == 6

    vertices = list(range(5))
    edges = list(combinations(vertices, 2))
    faces = list(combinations(vertices, 3))
    d1 = [[(1 if v == e[1] else -1 if v == e[0] else 0) for e in edges] for v in vertices]
    d2 = [[0 for _ in faces] for _ in edges]
    for c, face in enumerate(faces):
        for k in range(3):
            edge = face[:k] + face[k+1:]
            d2[edges.index(edge)][c] = (-1)**k
    r1, r2 = rank(d1), rank(d2)
    betti = [5-r1, 10-r1-r2, 10-r2]
    assert betti == [1, 0, 4]
    assert all(sum(e in set(combinations(f, 2)) for f in faces) == 3 for e in edges)

    # A purely combinatorial (1,2,2) distribution, not an affine realization.
    preferred = {}
    for i in range(5):
        preferred[tuple(sorted((i, (i+1) % 5)))] = tuple(sorted((i, (i+1) % 5, (i+2) % 5)))
        preferred[tuple(sorted((i, (i+2) % 5)))] = tuple(sorted((i, (i+2) % 5, (i+3) % 5)))
    assert len(preferred) == 10 and len(set(preferred.values())) == 10
    allocation = [[0 for _ in faces] for _ in edges]
    for r, edge in enumerate(edges):
        for c, face in enumerate(faces):
            if set(edge) <= set(face):
                allocation[r][c] = 1 if preferred[edge] == face else 2
    assert all(sum(row) == 5 for row in allocation)
    assert all(sum(row[c] for row in allocation) == 5 for c in range(10))

    report = {
        "status": "Exact consistency checks only; global Lagrangian gluing is unproved.",
        "family": "x0*x1*x2*x3*(x0+x1+x2+x3)+t*(x0^5+2*x1^5+3*x2^5+4*x3^5)=0",
        "line_polynomials": lines,
        "total_space_nodes": 50,
        "kahler_class": {
            "epsilon": str(eps),
            "component_line_coefficients": list(map(str, a)),
            "blowup_counts": counts,
            "component_squares": list(map(str, squares)),
            "bezout_lower_bounds_per_degree": list(map(str, bezout_bounds)),
            "total_square": str(sum(squares)),
            "double_curves": edge_areas,
            "compact_genus_six_curve_area": str(compact_curve_area),
        },
        "base": {
            "vertices": 5, "edges": 10, "faces": 10,
            "boundary_ranks": [r1, r2], "rational_betti_numbers": betti,
        },
        "epsilon_interval_certificates": {
            "parameter": "u=epsilon/a in (0,1/10)",
            "squares_coefficients_low_to_high": [list(map(str,p)) for p in parameter_squares],
            "bernstein_coefficients_in_x_equals_10u": [list(map(str,p)) for p in bernstein_certificates],
            "bezout_bound_coefficients_of_u": parameter_bezout,
            "sum_polynomial": [5, 0, 0],
        },
        "four_line_plumbing_linear_algebra": {
            "intersection_matrix_rank": four_line_intersection_rank,
            "meridian_subspace_dimension": 4-four_line_intersection_rank,
            "graph_cycle_dimension": four_line_graph_b1,
            "boundary_first_betti_number_from_pair_sequence": 6,
        },
        "combinatorial_node_allocation_only": {
            "edges": [[v+1 for v in e] for e in edges],
            "faces": [[v+1 for v in f] for f in faces],
            "matrix": allocation,
            "row_sums": [sum(r) for r in allocation],
            "column_sums": [sum(row[c] for row in allocation) for c in range(10)],
        },
    }
    destination = Path(__file__).with_name("verification_results.json")
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("10 square-free line polynomials; 50 nodes; triple points avoided.")
    print("5 ample component classes checked; all double-curve areas agree.")
    print("Sum of squares = 5; sum of open-component Euler numbers = 55.")
    print("B5 rational Betti numbers = [1, 0, 4].")
    print("Positive-square certificates verified for all 0 < epsilon/a < 1/10.")
    print("Four-line plumbing: meridian dimension 3; graph cycles 3; boundary b1=6.")
    print("Combinatorial allocation has 5 nodes per edge and per face.")
    print("These checks do not prove the global gluing theorem.")
    print(destination)

if __name__ == "__main__":
    main()

