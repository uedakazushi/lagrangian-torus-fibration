#!/usr/bin/env python3
"""Exact finite certificates for the v8 matroidal-link and lattice statements.

Python standard library only.  The rank bound and the general proofs are in
the public paper in ../paper/.  This script does not construct an action-compatible
tropical atlas or verify a symplectic gluing theorem.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb, gcd
from pathlib import Path
import json


def pairset(block):
    return frozenset(combinations(block, 2))


def connected_from_circuits(n, triples):
    """All circuits of a simple rank-three sparse paving matroid have size 3/4."""
    blocks = {frozenset(t) for t in triples}
    circuits = list(blocks)
    circuits += [frozenset(q) for q in combinations(range(n), 4)
                 if not any(t <= frozenset(q) for t in blocks)]
    parent = list(range(n))
    def root(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for circuit in circuits:
        a = min(circuit)
        for b in circuit:
            parent[root(b)] = root(a)
    return len({root(i) for i in range(n)}) == 1


def verify_basis_exchange(n, triples):
    blocks = {frozenset(t) for t in triples}
    bases = {frozenset(t) for t in combinations(range(n), 3)} - blocks
    assert bases
    for a in bases:
        for b in bases:
            for x in a - b:
                assert any((a - {x}) | {y} in bases for y in b - a)


def enumerate_triple_systems(n):
    """Exhaustive ordered backtracking, with safe incidence/capacity pruning.

    All two-point flats are implicit.  A three-point flat uses its three
    unordered pairs exactly once.  The cubic-link condition says that the
    number t_i of triples through i satisfies n-4 <= t_i <= floor((n-1)/2).
    Every linear triple system satisfying these bounds occurs once.
    """
    triples = list(combinations(range(n), 3))
    pairs = [pairset(t) for t in triples]
    lower, upper = max(0, n - 4), (n - 1) // 2
    result = []
    states = 0
    def visit(start, chosen, used_pairs, degrees):
        nonlocal states
        states += 1
        if all(degrees[i] >= lower for i in range(n)):
            result.append(tuple(chosen))
        candidates = [k for k in range(start, len(triples))
                      if not (pairs[k] & used_pairs)
                      and all(degrees[i] < upper for i in triples[k])]
        capacity = Counter(i for k in candidates for i in triples[k])
        if any(degrees[i] + capacity[i] < lower for i in range(n)):
            return
        for k in candidates:
            new_degrees = list(degrees)
            for i in triples[k]:
                new_degrees[i] += 1
            visit(k + 1, chosen + [triples[k]], used_pairs | pairs[k], new_degrees)
    visit(0, [], frozenset(), [0] * n)
    assert len(result) == len(set(result))
    return result, states


def nested_graph(n, triples):
    graph = {("p", i): set() for i in range(n)}
    used = set()
    def edge(a, b):
        graph[a].add(b)
        graph[b].add(a)
    for k, triple in enumerate(triples):
        node = ("F", k)
        graph[node] = set()
        for i in triple:
            edge(node, ("p", i))
        used.update(combinations(triple, 2))
    for i, j in combinations(range(n), 2):
        if (i, j) not in used:
            edge(("p", i), ("p", j))
    return graph


def suppress_bivalent(graph):
    graph = {v: set(neighbors) for v, neighbors in graph.items()}
    while any(len(neighbors) == 2 for neighbors in graph.values()):
        v = next(v for v in graph if len(graph[v]) == 2)
        a, b = graph[v]
        # In the four connected rank-three cases no parallel edge is created.
        assert a != b and b not in graph[a]
        graph[a].remove(v)
        graph[b].remove(v)
        graph[a].add(b)
        graph[b].add(a)
        del graph[v]
    return graph


def isomorphic(first, second):
    if len(first) != len(second):
        return False
    assignment, used = {}, set()
    def visit():
        if len(assignment) == len(first):
            return True
        u = max((x for x in first if x not in assignment),
                key=lambda x: sum(y in assignment for y in first[x]))
        for v in second:
            if v in used or len(first[u]) != len(second[v]):
                continue
            if all((x in first[u]) == (y in second[v])
                   for x, y in assignment.items()):
                assignment[u] = v
                used.add(v)
                if visit():
                    return True
                used.remove(v)
                del assignment[u]
        return False
    return visit()


def kneser_graph():
    vertices = list(combinations(range(1, 6), 2))
    return {s: {t for t in vertices if set(s).isdisjoint(t)} for s in vertices}


def check_classification():
    fano = [(0, 1, 2), (0, 3, 4), (0, 5, 6),
            (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
    references = {
        4: {i: set(range(4)) - {i} for i in range(4)},
        5: {i: {j for j in range(6) if (i < 3) != (j < 3)} for i in range(6)},
        6: kneser_graph(),
        7: nested_graph(7, fano),
    }
    expected = {4: (1, 3, "K4"), 5: (15, 4, "K3,3"),
                6: (30, 6, "Petersen"), 7: (30, 8, "Heawood")}
    reports = []
    for n in range(4, 8):
        systems, states = enumerate_triple_systems(n)
        connected = []
        for system in systems:
            verify_basis_exchange(n, system)
            if connected_from_circuits(n, system):
                connected.append(system)
        count, genus, name = expected[n]
        assert len(connected) == count
        for system in connected:
            graph = suppress_bivalent(nested_graph(n, system))
            assert all(len(neighbors) == 3 for neighbors in graph.values())
            edges = sum(map(len, graph.values())) // 2
            assert edges - len(graph) + 1 == genus
            assert isomorphic(graph, references[n])
        reports.append({
            "simplified_ground_set_size": n,
            "backtracking_states": states,
            "all_admissible_labelled_triple_systems": len(systems),
            "connected_labelled_systems": count,
            "homeomorphism_type": name,
            "link_b1": genus,
            "all_basis_exchange_axioms_verified": True,
            "all_graph_isomorphisms_verified": True,
            "connected_systems_zero_based": connected,
        })
    return reports


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    pivot = 0
    for col in range(len(a[0])):
        rows = [i for i in range(pivot, len(a)) if a[i][col]]
        if not rows:
            continue
        i = rows[0]
        a[pivot], a[i] = a[i], a[pivot]
        divisor = a[pivot][col]
        a[pivot] = [x / divisor for x in a[pivot]]
        for i in range(len(a)):
            if i != pivot:
                multiple = a[i][col]
                a[i] = [x - multiple * y for x, y in zip(a[i], a[pivot])]
        pivot += 1
    return pivot


def determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    answer = Fraction(1)
    for col in range(len(a)):
        rows = [i for i in range(col, len(a)) if a[i][col]]
        if not rows:
            return 0
        i = rows[0]
        if i != col:
            a[col], a[i] = a[i], a[col]
            answer *= -1
        divisor = a[col][col]
        answer *= divisor
        for i in range(col + 1, len(a)):
            multiple = a[i][col] / divisor
            a[i] = [x - multiple * y for x, y in zip(a[i], a[col])]
    assert answer.denominator == 1
    return int(answer)


def petersen_rays():
    k4_edges = list(combinations(range(1, 5), 2))
    coordinates = {edge: [int(k == j) for k in range(5)]
                   for j, edge in enumerate(k4_edges[:5])}
    coordinates[k4_edges[5]] = [-1] * 5
    rays = dict(coordinates)
    for a in range(1, 5):
        edges = list(combinations([b for b in range(1, 5) if b != a], 2))
        rays[a, 5] = [sum(coordinates[e][k] for e in edges) for k in range(5)]
    return rays


def check_ray_lattice():
    rays = petersen_rays()
    graph = kneser_graph()
    vertices = sorted(graph)
    assert all(gcd(*ray) == 1 for ray in rays.values())
    cones = []
    for s, t in combinations(vertices, 2):
        if t not in graph[s]:
            continue
        minors = [rays[s][i] * rays[t][j] - rays[s][j] * rays[t][i]
                  for i, j in combinations(range(5), 2)]
        index = gcd(*minors)
        assert index == 1
        cones.append({"rays": [s, t], "gcd_of_rank_two_minors": index})
    assert len(cones) == 15
    for s in vertices:
        assert [sum(rays[t][k] for t in graph[s]) for k in range(5)] == rays[s]
    q = [[int(t in graph[s]) - int(s == t) for t in vertices] for s in vertices]
    assert rank(q) == 5
    ids = [vertices.index((a, 5)) for a in range(1, 5)] + [vertices.index((1, 2))]
    minor = [[q[i][j] for j in ids] for i in ids]
    assert determinant(minor) == 1
    return {"rank_of_ambient_lattice": 5,
            "coordinates_basis": ["e12", "e13", "e14", "e23", "e24"],
            "rays": {str(s): rays[s] for s in vertices},
            "cones": cones,
            "all_balancing_equalities_sum_neighbors_equals_ray": True,
            "rank_A_minus_I": 5,
            "unimodular_maximal_minor_indices": [vertices[i] for i in ids],
            "unimodular_maximal_minor": minor,
            "minor_determinant": 1,
            "cokernel_A_minus_I": "Z^5"}


def check_six_stars():
    infinity = 5
    factorization = [frozenset((tuple(sorted((infinity, c))),
                               tuple(sorted(((c + 1) % 5, (c - 1) % 5))),
                               tuple(sorted(((c + 2) % 5, (c - 2) % 5)))))
                     for c in range(5)]
    partitions = {edge: tuple(sorted(matching - {edge}))
                  for matching in factorization for edge in matching}
    assert len(partitions) == 15
    result = []
    for i in range(6):
        def f(x):
            if i == infinity:
                return x
            if x == i:
                return infinity
            if x == infinity:
                return 0
            return pow((x - i) % 5, -1, 5)
        transformed = {frozenset(tuple(sorted((f(a), f(b)))) for a, b in matching)
                       for matching in factorization}
        assert transformed == set(factorization)
        graph, labels = {}, {}
        for j in range(6):
            if j == i:
                continue
            c = f(j)
            for k, block in enumerate(partitions[tuple(sorted((i, j)))]):
                image = {f(x) for x in block}
                node = (j, k)
                if image == {(c - 1) % 5, (c + 1) % 5}:
                    pair = {(2 * c) % 5, (2 * c + 1) % 5}
                else:
                    assert image == {(c - 2) % 5, (c + 2) % 5}
                    pair = {(2 * c + 2) % 5, (2 * c + 4) % 5}
                labels[node] = tuple(sorted(x + 1 for x in pair))
                graph[node] = set()
        def connect(a, b):
            graph[a].add(b)
            graph[b].add(a)
        for j in range(6):
            if j != i:
                connect((j, 0), (j, 1))
        for j, k in combinations([j for j in range(6) if j != i], 2):
            a = next(a for a, block in enumerate(partitions[tuple(sorted((i, j)))]) if k in block)
            b = next(b for b, block in enumerate(partitions[tuple(sorted((i, k)))]) if j in block)
            connect((j, a), (k, b))
        assert len(set(labels.values())) == 10
        for a, b in combinations(graph, 2):
            assert (b in graph[a]) == set(labels[a]).isdisjoint(labels[b])
        result.append({"core": i, "infinity_label": infinity,
                       "graph_to_Kneser_labels": {str(k): v for k, v in labels.items()},
                       "zero_delta_edges": 5, "unit_delta_edges": 10,
                       "factorization_symmetry_and_all_edges_verified": True})
    return result


def check_plumbing_and_period_conditions():
    j5 = [[1] * 5 for _ in range(5)]
    assert rank(j5) == 1
    assert (5 - rank(j5)) + (comb(5, 2) - 5 + 1) == 10
    assert 5 + (15 - 10 + 1) == 11
    parity = []
    for q in range(1, 25):
        units = [p for p in range(q) if gcd(p, q) == 1]
        pairs = [(a, b) for a in units for b in units if gcd(a + b, q) == 1]
        assert bool(pairs) == bool(q % 2)
        parity.append({"denominator": q, "admissible_ordered_residue_pairs": len(pairs)})
    # Rational endpoint slopes alone do not imply unimodularity.
    first, second = (1, 0), (3, -2)
    det = abs(first[0] * second[1] - second[0] * first[1])
    assert det == 2
    return {"W5_boundary_H1": "Z^10", "standard_M05_boundary_H1": "Z^11",
            "zero_delta_edges_generic_m_line": {str(m): m * (m - 4) for m in range(4, 11)},
            "unit_delta_edges_generic_m_line": {str(m): comb(m, 2) for m in range(4, 11)},
            "branch_denominator_parity_checks": parity,
            "nonunimodular_rational_sector_example": {"rays": [first, second], "index": det}}


def main():
    result = {
        "scope": "Finite combinatorial and integral-lattice checks; no global affine or symplectic gluing assertion.",
        "cubic_rank_three_classification": check_classification(),
        "Petersen_integral_fan": check_ray_lattice(),
        "six_explicit_star_identifications": check_six_stars(),
        "plumbing_and_period_checks": check_plumbing_and_period_conditions(),
        "general_degree_obstruction": {str(d): {"core_link_b1": comb(d - 2, 2),
                                                "exceeds_matroidal_cubic_bound_8": comb(d - 2, 2) > 8}
                                       for d in range(5, 13)},
    }
    destination = Path(__file__).with_name("verification_petersen_affine_v8_results.json")
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "all checks passed", "classification_counts": [1, 15, 30, 30],
                      "Petersen_unimodular_cones": 15, "explicit_core_charts": 6,
                      "results": str(destination)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
