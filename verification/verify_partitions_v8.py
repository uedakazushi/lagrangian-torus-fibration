#!/usr/bin/env python3
"""Exact finite certificates for degree-partition branched bases.

Standard library only.  Reeb multigraphs are made from a labelled trivalent
tree by replacing an arbitrary edge uv with uA, AB, AB, Bv for each handle.
Parallel edges have distinct IDs throughout; they must never be collapsed.

The script verifies every chain-map and integer strong-deformation-retraction
identity on every cellular generator.  It also certifies an integral H2 basis
using exact boundary ranks and a unitriangular coefficient minor, and checks
the numerical polarization and Euler formulas with fractions.

These are finite checks of explicit combinatorial and numerical examples.
They do not prove the general-degree theorem, generic algebraic existence,
analytic gluing, or existence of a Lagrangian fibration.  Those assertions
require the proofs in the paper.

Run: python3 verification/verify_partitions_v8.py
"""

from collections import Counter, deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path
import random


PARTITIONS = (
    (1, 1, 3), (1, 2, 2), (2, 2, 2), (1, 1, 1, 3), (1, 2, 4),
    (3, 3, 3), (2, 3, 4), (1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1), (1, 1, 6),
)
SEEDS = (20261026, 20261027)


class Checks:
    """Checks stay active when Python is run with -O."""

    def __init__(self):
        self.count = 0

    def require(self, condition, message):
        self.count += 1
        if not condition:
            raise AssertionError(message)

    def equal(self, actual, expected, message):
        self.require(actual == expected,
                     f"{message}: actual={actual!r}, expected={expected!r}")


# Sparse integer-chain helpers adapted from verification/verify_v5.py.
def add(*summands):
    out = Counter()
    for scalar, chain in summands:
        for cell, coefficient in chain.items():
            out[cell] += scalar * coefficient
    return {cell: coefficient for cell, coefficient in out.items() if coefficient}


def one(cell):
    return {cell: 1}


def linear(table, chain):
    return add(*[(coefficient, table[cell])
                 for cell, coefficient in chain.items()])


def pg(degree):
    return comb(degree - 1, 3) if degree >= 4 else 0


def surface_euler(degree):
    return degree * (degree * degree - 4 * degree + 6)


def exact_rank(columns, rows):
    """Independent sparse Gaussian elimination over Q, never floating point."""
    row_index = {row: index for index, row in enumerate(rows)}
    pivots = {}
    for column in columns:
        vector = {row_index[row]: F(value)
                  for row, value in column.items() if value}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {row: x / value for row, x in vector.items()}
                break
            for row, x in pivots[pivot].items():
                new = vector.get(row, F(0)) - value * x
                if new:
                    vector[row] = new
                else:
                    vector.pop(row, None)
    return len(pivots)


def connected(vertices, edges):
    adjacency = {vertex: [] for vertex in vertices}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    if not vertices:
        return False
    reached = {vertices[0]}
    pending = [vertices[0]]
    while pending:
        for neighbor in adjacency[pending.pop()]:
            if neighbor not in reached:
                reached.add(neighbor)
                pending.append(neighbor)
    return len(reached) == len(vertices)


def make_reeb_graph(point_labels, genus, rng, check):
    """Leaf vertices are nonnegative; internal vertices are negative integers."""
    n = len(point_labels)
    check.require(n >= 3 and genus >= 0, "valid Reeb graph parameters")
    edges = {}
    next_edge = 0
    next_internal = -2

    def insert(u, v):
        nonlocal next_edge
        edges[next_edge] = (u, v)
        next_edge += 1

    for leaf in range(3):
        insert(-1, leaf)
    for leaf in range(3, n):
        edge = rng.choice(sorted(edges))
        u, v = edges.pop(edge)
        a = next_internal
        next_internal -= 1
        insert(u, a)
        insert(a, v)
        insert(a, leaf)

    for _ in range(genus):
        edge = rng.choice(sorted(edges))
        u, v = edges.pop(edge)
        a, b = next_internal, next_internal - 1
        next_internal -= 2
        insert(u, a)
        insert(a, b)
        insert(a, b)  # A different edge ID, not a duplicate to discard.
        insert(b, v)

    adjacency = {}
    for edge, (u, v) in edges.items():
        check.require(u != v, "handle insertion creates no graph loop")
        adjacency.setdefault(u, []).append((v, edge))
        adjacency.setdefault(v, []).append((u, edge))
    internal = sorted(vertex for vertex in adjacency if vertex < 0)
    check.require(all(len(adjacency[v]) == 3 for v in internal),
                  "all internal Reeb vertices are trivalent with multiplicity")
    check.require(all(len(adjacency[v]) == 1 for v in range(n)),
                  "all labelled leaves are univalent")
    check.equal(len(internal), 2 * genus + n - 2, "internal vertex count")
    check.equal(len(edges), 3 * genus + 2 * n - 3, "total Reeb edge count")
    check.equal(len(edges) - len(adjacency) + 1, genus, "Reeb first Betti number")
    check.require(connected(sorted(adjacency), list(edges.values())),
                  "Reeb graph connected")

    internal_edges = {}
    for edge, (u, v) in sorted(edges.items()):
        if u < 0 and v < 0:
            # Independent orientations exercise signed tree paths, not only +1 paths.
            internal_edges[edge] = (u, v) if rng.randrange(2) else (v, u)
    check.equal(len(internal_edges), 3 * genus + n - 3, "internal edge count")
    check.require(connected(internal, list(internal_edges.values())),
                  "internal graph remains connected after removing leaves")

    root = rng.choice(internal)
    internal_adjacency = {vertex: [] for vertex in internal}
    for edge, (u, v) in internal_edges.items():
        internal_adjacency[u].append((v, edge, 1))
        internal_adjacency[v].append((u, edge, -1))
    for neighbors in internal_adjacency.values():
        rng.shuffle(neighbors)
    paths = {root: {}}
    tree_edges = set()
    pending = deque([root])
    while pending:
        u = pending.popleft()
        for v, edge, sign in internal_adjacency[u]:
            if v not in paths:
                paths[v] = dict(paths[u])
                paths[v][edge] = sign
                tree_edges.add(edge)
                pending.append(v)
    check.equal(len(paths), len(internal), "spanning tree reaches every internal vertex")
    check.equal(len(tree_edges), len(internal) - 1, "spanning tree edge count")
    non_tree = sorted(set(internal_edges) - tree_edges)
    check.equal(len(non_tree), genus, "non-tree edges represent all Reeb cycles")
    return {
        "vertices": internal, "edges": internal_edges, "root": root,
        "tree_edges": tree_edges, "non_tree_edges": non_tree, "paths": paths,
        "leaves": {label: adjacency[index][0][0]
                   for index, label in enumerate(point_labels)},
        "parallel_edge_excess": sum(count - 1 for count in
            Counter(tuple(sorted(edge)) for edge in internal_edges.values()).values()),
    }


def check_partition(degrees, seed):
    check = Checks()
    rng = random.Random(seed)
    d, k = sum(degrees), len(degrees)
    check.require(k >= 3 and d >= 5 and all(e >= 1 for e in degrees),
                  "degree-partition hypotheses")
    labels = list(range(1, k + 1))
    e = dict(zip(labels, degrees))
    pairs, triples = list(combinations(labels, 2)), list(combinations(labels, 3))
    points = {triple: [(*triple, r) for r in range(e[triple[0]] * e[triple[1]] * e[triple[2]])]
              for triple in triples}
    graphs, curve_data = {}, []
    for i, j in pairs:
        genus_numerator = e[i] * e[j] * (e[i] + e[j] - 4)
        check.equal(genus_numerator % 2, 0, "complete-intersection genus is integral")
        genus = 1 + genus_numerator // 2
        leaf_count = e[i] * e[j] * (d - e[i] - e[j])
        point_labels = sorted(point for triple, pp in points.items()
                              if i in triple and j in triple for point in pp)
        check.equal(len(point_labels), leaf_count, "actual triple points label all leaves")
        check.require(leaf_count >= d - 2 >= 3, "at least three leaves")
        graph = make_reeb_graph(point_labels, genus, rng, check)
        graphs[i, j] = graph
        check.equal(len(graph["vertices"]), e[i] * e[j] * (d - 4),
                    "simplified trivalent vertex formula")
        curve_data.append({
            "pair": [i, j], "degrees": [e[i], e[j]], "genus": genus,
            "leaves": leaf_count, "internal_vertices": len(graph["vertices"]),
            "internal_edges": len(graph["edges"]), "root": graph["root"],
            "tree_edges": len(graph["tree_edges"]), "non_tree_edges": genus,
            "parallel_edge_excess": graph["parallel_edge_excess"],
        })

    source, target = [[], [], []], [[], [], []]
    boundary, target_boundary, q, s, h = {}, {}, {}, {}, {}
    D, graph_generators, extra_generators = {}, [], []
    for i in labels:
        vertex = ("v", i)
        source[0].append(vertex)
        target[0].append(vertex)
        boundary[vertex] = target_boundary[vertex] = {}
        q[vertex] = s[vertex] = one(vertex)
        h[vertex] = {}

    for (i, j), graph in graphs.items():
        standard_edge = ("e", i, j)
        target[1].append(standard_edge)
        target_boundary[standard_edge] = {("v", j): 1, ("v", i): -1}
        s[standard_edge] = one(("e", i, j, graph["root"]))
        for p in graph["vertices"]:
            edge = ("e", i, j, p)
            source[1].append(edge)
            boundary[edge] = dict(target_boundary[standard_edge])
            q[edge] = one(standard_edge)
            D[i, j, p] = {("b", i, j, a): sign
                          for a, sign in graph["paths"][p].items()}
            h[edge] = D[i, j, p]
        for a, (p, v) in graph["edges"].items():
            bigon = ("b", i, j, a)
            source[2].append(bigon)
            boundary[bigon] = {("e", i, j, v): 1, ("e", i, j, p): -1}
            h[bigon] = {}
            if a in graph["tree_edges"]:
                q[bigon] = {}
            else:
                generator = ("g", i, j, a)
                graph_generators.append(generator)
                target[2].append(generator)
                target_boundary[generator] = {}
                q[bigon] = one(generator)
                s[generator] = add((1, one(bigon)), (-1, D[i, j, v]), (1, D[i, j, p]))
        for p in graph["vertices"]:
            check.equal(linear(boundary, D[i, j, p]),
                        add((1, one(("e", i, j, p))),
                            (-1, one(("e", i, j, graph["root"])))),
                        "tree path has the required boundary")

    corrected = {}
    for i, j, l in triples:
        standard_triangle = ("t", i, j, l)
        target[2].append(standard_triangle)
        target_boundary[standard_triangle] = {
            ("e", i, j): 1, ("e", j, l): 1, ("e", i, l): -1}
        for point in points[i, j, l]:
            r = point[-1]
            triangle = ("t", *point)
            p = graphs[i, j]["leaves"][point]
            u = graphs[j, l]["leaves"][point]
            v = graphs[i, l]["leaves"][point]
            source[2].append(triangle)
            boundary[triangle] = {
                ("e", i, j, p): 1, ("e", j, l, u): 1, ("e", i, l, v): -1}
            corrected[point] = add((1, one(triangle)), (-1, D[i, j, p]),
                                   (-1, D[j, l, u]), (1, D[i, l, v]))
            h[triangle] = {}
            if r == 0:
                s[standard_triangle] = corrected[point]
                q[triangle] = one(standard_triangle)
            else:
                generator = ("x", *point)
                extra_generators.append(generator)
                target[2].append(generator)
                target_boundary[generator] = {}
                q[triangle] = add((1, one(standard_triangle)), (1, one(generator)))
                s[generator] = add((1, corrected[point]), (-1, corrected[i, j, l, 0]))

    source_degree = {cell: degree for degree, cells in enumerate(source) for cell in cells}
    target_degree = {cell: degree for degree, cells in enumerate(target) for cell in cells}
    for name, table in (("d", boundary), ("d_target", target_boundary),
                        ("q", q), ("s", s), ("H", h)):
        check.require(all(type(coefficient) is int for chain in table.values()
                          for coefficient in chain.values()),
                      f"{name} has integer coefficients, not merely rational coefficients")
    for degree in range(3):
        for cell in source[degree]:
            check.require(all(source_degree[c] == degree - 1 for c in boundary[cell]),
                          "source boundary degree")
            check.require(all(target_degree[c] == degree for c in q[cell]), "q degree")
            check.require(all(source_degree[c] == degree + 1 for c in h[cell]), "H degree")
            check.equal(linear(boundary, boundary[cell]), {}, "source d squared")
            check.equal(linear(target_boundary, q[cell]), linear(q, boundary[cell]),
                        "q is a chain map")
            check.equal(add((1, one(cell)), (-1, linear(s, q[cell]))),
                        add((1, linear(boundary, h[cell])), (1, linear(h, boundary[cell]))),
                        "id - s q = d H + H d over the integers")
            check.equal(linear(q, h[cell]), {}, "q H = 0")
            check.equal(linear(h, h[cell]), {}, "H squared = 0")
        for cell in target[degree]:
            check.require(all(target_degree[c] == degree - 1 for c in target_boundary[cell]),
                          "target boundary degree")
            check.require(all(source_degree[c] == degree for c in s[cell]), "s degree")
            check.equal(linear(target_boundary, target_boundary[cell]), {}, "target d squared")
            check.equal(linear(q, s[cell]), one(cell), "q s = id over the integers")
            check.equal(linear(boundary, s[cell]), linear(s, target_boundary[cell]),
                        "s is a chain map")
            check.equal(linear(h, s[cell]), {}, "H s = 0")

    # Integral H2 basis: tetrahedron boundaries, Reeb cycles, duplicate triples.
    target_cycles, pivot_cells = [], []
    basis_types = Counter({"simplex_tetrahedron_boundaries": 0,
                          "Reeb_cycles": 0, "duplicate_triple_points": 0})
    for i, j, l in combinations(labels[1:], 3):
        target_cycles.append(add((1, one(("t", i, j, l))),
                                 (-1, one(("t", 1, j, l))),
                                 (1, one(("t", 1, i, l))),
                                 (-1, one(("t", 1, i, j)))))
        pivot_cells.append(("t", i, j, l, 0))
        basis_types["simplex_tetrahedron_boundaries"] += 1
    for generator in graph_generators:
        target_cycles.append(one(generator))
        pivot_cells.append(("b", *generator[1:]))
        basis_types["Reeb_cycles"] += 1
    for generator in extra_generators:
        target_cycles.append(one(generator))
        pivot_cells.append(("t", *generator[1:]))
        basis_types["duplicate_triple_points"] += 1
    cycles = [linear(s, cycle) for cycle in target_cycles]
    for column, (cycle, expected) in enumerate(zip(cycles, target_cycles)):
        check.equal(linear(boundary, cycle), {}, "H2 candidate is an integer cycle")
        check.equal(linear(q, cycle), expected, "H2 candidate maps to the target basis")
        check.equal(cycle.get(pivot_cells[column], 0), 1, "unit diagonal of H2 coefficient minor")
        check.require(all(cycle.get(pivot_cells[row], 0) == 0
                          for row in range(column + 1, len(pivot_cells))),
                      "H2 coefficient minor is upper triangular over Z")

    rank_d1 = exact_rank([boundary[cell] for cell in source[1]], source[0])
    rank_d2 = exact_rank([boundary[cell] for cell in source[2]], source[1])
    target_rank_d1 = exact_rank([target_boundary[cell] for cell in target[1]], target[0])
    target_rank_d2 = exact_rank([target_boundary[cell] for cell in target[2]], target[1])
    check.equal(rank_d1, k - 1, "source connected-chain rank")
    check.equal(rank_d2, len(source[1]) - k + 1, "source rational H1 vanishes")
    check.equal(target_rank_d1, k - 1, "target connected-chain rank")
    check.equal(target_rank_d2, comb(k - 1, 2), "simplex two-skeleton boundary rank")
    check.equal(len(source[2]) - rank_d2, len(cycles), "H2 candidates have full kernel rank")
    # The coefficient minor has determinant 1, so the span is primitive.
    # Full kernel rank and primitivity certify an integral basis, not just a Q-basis.
    expected_b2 = pg(d) - sum(pg(degree) for degree in degrees)
    extra_rank = sum(c["genus"] for c in curve_data) + sum(len(pp) - 1 for pp in points.values())
    check.equal(extra_rank, len(graph_generators) + len(extra_generators), "free target summand rank")
    check.equal(len(cycles), comb(k - 1, 3) + extra_rank, "target H2 rank formula")
    check.equal(len(cycles), expected_b2, "geometric-genus subtraction formula")
    check.equal(k - len(source[1]) + len(source[2]), 1 + expected_b2, "base Euler number")
    incidence = Counter()
    for face in source[2]:
        check.require(all(abs(value) == 1 for value in boundary[face].values()),
                      "each cellular incidence has coefficient plus or minus one")
        incidence.update(boundary[face].keys())
    check.equal(set(incidence), set(source[1]), "every branch edge has incident faces")
    check.require(all(incidence[cell] == 3 for cell in source[1]),
                  "every branch edge has exactly three incident faces, with multiplicity")

    links = []
    for i in labels:
        vertices, edges = [], []
        for j in labels:
            if j == i:
                continue
            graph = graphs[tuple(sorted((i, j)))]
            vertices.extend((j, p) for p in graph["vertices"])
            edges.extend(((j, p), (j, v)) for p, v in graph["edges"].values())
        for triple, pp in points.items():
            if i not in triple:
                continue
            j, l = [vertex for vertex in triple if vertex != i]
            for point in pp:
                p = graphs[tuple(sorted((i, j)))]["leaves"][point]
                u = graphs[tuple(sorted((i, l)))]["leaves"][point]
                edges.append(((j, p), (l, u)))
        valences = Counter(vertex for edge in edges for vertex in edge)
        check.equal(set(valences), set(vertices), "all link vertices occur")
        check.require(all(valences[vertex] == 3 for vertex in vertices),
                      "link trivalence counts parallel edges separately")
        check.require(connected(vertices, edges), "core link connected")
        link_b1 = F(1) + F(e[i] * (d - e[i]) * (d - 4), 2)
        check.equal(link_b1.denominator, 1, "link Betti formula integral")
        check.equal(len(edges) - len(vertices) + 1, int(link_b1), "core link Betti formula")
        check.equal(len(vertices), e[i] * (d - e[i]) * (d - 4), "core link vertex formula")
        links.append({"component": i, "degree": e[i], "V": len(vertices),
                      "E": len(edges), "b1": int(link_b1)})

    numerical = check_polarization_and_euler(degrees, seed, check)
    return {
        "degrees": list(degrees), "degree_sum": d, "components": k, "seed": seed,
        "source_cell_dimensions": list(map(len, source)),
        "target_cell_dimensions": list(map(len, target)),
        "source_boundary_ranks_Q": [rank_d1, rank_d2],
        "target_boundary_ranks_Q": [target_rank_d1, target_rank_d2],
        "SDR": {"integer_chain_maps": True, "q_s_identity": True,
                "id_minus_s_q_equals_dH_plus_Hd": True,
                "H_s_zero": True, "q_H_zero": True, "H_squared_zero": True},
        "H2": {"rank": len(cycles), "pg_degree_sum": pg(d),
               "sum_component_pg": sum(pg(degree) for degree in degrees),
               "basis_types": dict(basis_types), "integral_basis_certified": True,
               "coefficient_minor": "upper triangular with diagonal 1",
               "coefficient_minor_determinant": 1},
        "trivalent_incidence_verified": True,
        "curves": curve_data, "links": links, "numerical": numerical,
        "checks_passed": check.count,
    }


def check_polarization_and_euler(degrees, seed, check):
    """All data here are exact rational numbers, independently of the graph."""
    rng = random.Random(seed + 1000003)
    d, k = sum(degrees), len(degrees)
    a = F(d + k + 1, 3)
    prefixes = [sum(degrees[:t]) for t in range(1, k)]
    raw = [F(rng.randint(1, 19), rng.randint(1, 13)) for _ in prefixes]
    fill_fraction = F(rng.randint(1, 8), 10)
    raw_total = sum((prefix * gap for prefix, gap in zip(prefixes, raw)), F(0))
    gaps = [a * fill_fraction * gap / raw_total for gap in raw]
    beta = [F(0)]
    for gap in gaps:
        beta.append(beta[-1] + gap)
    weighted_beta_sum = sum((degree * b for degree, b in zip(degrees, beta)), F(0))
    coefficients = [a + weighted_beta_sum - d * b for b in beta]
    A = coefficients[-1]
    weighted_gap_sum = sum((prefix * gap for prefix, gap in zip(prefixes, gaps)), F(0))
    check.require(all(gap > 0 for gap in gaps), "all weighted-slice gaps positive")
    check.require(weighted_gap_sum < a, "strict weighted simplex inequality")
    check.equal(A, a - weighted_gap_sum, "weighted sharp-slice terminal coefficient")
    check.equal(A, a * (1 - fill_fraction), "normalization of the sample inside the simplex")
    check.require(all(coefficient >= A > 0 for coefficient in coefficients),
                  "all component hyperplane coefficients positive")
    shifted_beta = [b + F(7, 5) for b in beta]
    shifted_sum = sum((degree * b for degree, b in zip(degrees, shifted_beta)), F(0))
    check.equal([a + shifted_sum - d * b for b in shifted_beta], coefficients,
                "common beta translation leaves the vertical class unchanged")

    squares, component_data, pair_areas = [], [], []
    for i, ei in enumerate(degrees):
        higher = range(i + 1, k)
        assigned_nodes = sum(d * ei * degrees[j] for j in higher)
        square = ei * coefficients[i] ** 2 - sum(
            (d * ei * degrees[j] * (beta[j] - beta[i]) ** 2 for j in higher), F(0))
        u = beta[-1] - beta[i]
        lower = ei * (A * A + 2 * d * A * u + d * sum(degrees[:i + 1]) * u * u)
        check.require(square >= lower > 0, "component square and uniform positive lower bound")
        curve_bound = coefficients[i] - sum(
            (degrees[j] * (beta[j] - beta[i]) for j in higher), F(0))
        check.equal(curve_bound, a - sum(
            (degrees[j] * (beta[i] - beta[j]) for j in range(i)), F(0)),
            "weighted Bezout lower-bound identity")
        check.require(curve_bound >= A > 0, "weighted Bezout coefficient positive")
        for j in higher:
            ej = degrees[j]
            exceptional_area = beta[j] - beta[i]
            left = ei * ej * coefficients[i] - d * ei * ej * exceptional_area
            right = ei * ej * coefficients[j]
            check.require(exceptional_area > 0, "all assigned exceptional areas positive")
            check.equal(left, right, "double-curve area agrees on both components")
            check.require(left > 0, "matched double-curve area positive")
            left_normal_degree = ei * ej * ej - d * ei * ej
            right_normal_degree = ej * ei * ei
            marked_points = ei * ej * (d - ei - ej)
            check.equal(left_normal_degree + right_normal_degree + marked_points, 0,
                        "normal degrees plus triple points satisfy the semistable balance")
            pair_areas.append({"pair": [i + 1, j + 1],
                               "nodes": d * ei * ej,
                               "exceptional_area": str(exceptional_area),
                               "left_area": str(left), "right_area": str(right),
                               "left_normal_degree": left_normal_degree,
                               "right_normal_degree": right_normal_degree,
                               "triple_points": marked_points})
        squares.append(square)
        component_data.append({"component": i + 1, "degree": ei,
                               "hyperplane_coefficient": str(coefficients[i]),
                               "assigned_nodes": assigned_nodes,
                               "xi_square": str(square), "square_lower_bound": str(lower),
                               "curve_bound_coefficient": str(curve_bound)})
    check.equal(sum(squares, F(0)), d * a * a, "total component volume equals d a squared")

    # Sample the codimension-one boundary faces exactly; this is not a proof
    # of ampleness for all parameters or of analytic fibration surgery.
    for t in range(k - 1):
        facet_gaps = list(gaps)
        facet_gaps[t] = F(0)
        facet_beta = [F(0)]
        for gap in facet_gaps:
            facet_beta.append(facet_beta[-1] + gap)
        facet_sum = sum((degree * b for degree, b in zip(degrees, facet_beta)), F(0))
        check.equal(facet_beta[t + 1] - facet_beta[t], 0,
                    "gap facet has a zero adjacent exceptional area")
        check.require(a + facet_sum - d * facet_beta[-1] > 0,
                      "other simplex inequality is still strict on a gap facet")
    terminal_gaps = [gap / fill_fraction for gap in gaps]
    terminal_beta = [F(0)]
    for gap in terminal_gaps:
        terminal_beta.append(terminal_beta[-1] + gap)
    terminal_sum = sum((degree * b for degree, b in zip(degrees, terminal_beta)), F(0))
    terminal_coefficient = a + terminal_sum - d * terminal_beta[-1]
    check.equal(terminal_coefficient, 0,
                "terminal facet has zero last component coefficient")
    check.equal(degrees[-1] * terminal_coefficient ** 2, 0,
                "terminal facet has zero last component square")

    S2 = sum(degrees[i] * degrees[j] for i, j in combinations(range(k), 2))
    cores = []
    for i, ei in enumerate(degrees):
        others = [j for j in range(k) if j != i]
        curve_euler_sum = 0
        for j in others:
            genus = 1 + ei * degrees[j] * (ei + degrees[j] - 4) // 2
            curve_euler_sum += 2 - 2 * genus
        triple_count_on_component = sum(
            ei * degrees[j] * degrees[l] for j, l in combinations(others, 2))
        inclusion_exclusion = surface_euler(ei) - curve_euler_sum + triple_count_on_component
        simplified = ei * (d * d - 4 * d + 6 - S2)
        check.equal(inclusion_exclusion, simplified, "core Euler inclusion-exclusion identity")
        cores.append(simplified)
        component_data[i]["core_Euler"] = simplified
        component_data[i]["resolved_open_Euler"] = (
            simplified + component_data[i]["assigned_nodes"])
    node_count = d * S2
    check.equal(sum(c["assigned_nodes"] for c in component_data), node_count,
                "ordered node assignment counts every node once")
    check.equal(sum(cores) + node_count, surface_euler(d), "core Euler plus nodes equals surface Euler")
    check.equal(sum(c["resolved_open_Euler"] for c in component_data), surface_euler(d),
                "resolved open component Euler sum")
    return {
        "arithmetic": "fractions.Fraction and integers only",
        "a": str(a), "prefix_degrees": prefixes, "gaps": [str(x) for x in gaps],
        "beta": [str(x) for x in beta], "weighted_gap_sum": str(weighted_gap_sum),
        "terminal_coefficient_A": str(A), "volume_sum": str(sum(squares, F(0))),
        "expected_volume_d_a_squared": str(d * a * a),
        "gap_facets_checked": k - 1, "terminal_facet_checked": True,
        "components": component_data, "double_curve_areas": pair_areas,
        "core_Euler_sum": sum(cores), "node_count": node_count,
        "surface_Euler": surface_euler(d), "Euler_identity_verified": True,
    }


def main():
    results = [check_partition(degrees, seed) for degrees in PARTITIONS for seed in SEEDS]
    output = Path(__file__).with_name("partitions_v8_results.json")
    report = {
        "scope": (
            "Finite exact combinatorial and numerical checks. This script does not prove "
            "the general-degree theorem, generic algebraic existence, analytic gluing, "
            "or existence of a Lagrangian fibration."
        ),
        "dependencies": "Python standard library only",
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "partitions": [list(degrees) for degrees in PARTITIONS], "seeds": list(SEEDS),
        "runs": len(results), "all_checks_passed": True,
        "total_checks_passed": sum(result["checks_passed"] for result in results),
        "results": results,
    }
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"All {report['total_checks_passed']} exact checks passed in {len(results)} runs.")
    print(f"Results: {output}")


if __name__ == "__main__":
    main()
