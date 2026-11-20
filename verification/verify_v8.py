#!/usr/bin/env python3
"""Exact certificates for branched bases and simultaneous Petersen links.

Only the Python standard library is used.  These checks do not prove any
symplectic gluing assertion.  General-degree proofs are in
../paper/base_topology.tex.
Run: python3 verification/verify_v8.py
"""
from collections import Counter, deque
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import random


def add(*summands):
    out = Counter()
    for scalar, chain in summands:
        for cell, value in chain.items():
            out[cell] += scalar * value
    return {cell: value for cell, value in out.items() if value}


def one(cell):
    return {cell: 1}


def linear(table, chain):
    return add(*[(coefficient, table[cell]) for cell, coefficient in chain.items()])


def make_tree(leaves, rng):
    """Insert leaves by splitting arbitrary edges, retaining all leaf labels."""
    edges = {tuple(sorted((-1, k))) for k in leaves[:3]}
    for n, leaf in enumerate(leaves[3:], 2):
        u, v = rng.choice(sorted(edges))
        edges.remove((u, v))
        edges.update(tuple(sorted(edge)) for edge in [(u, -n), (v, -n), (leaf, -n)])
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    assert all(len(adj[k]) == 1 for k in leaves)
    internal = sorted(k for k in adj if k < 0)
    assert all(len(adj[k]) == 3 for k in internal)
    root = -1
    paths = {root: []}
    oriented = []
    pending = deque([root])
    while pending:
        p = pending.popleft()
        for u in sorted(adj[p]):
            if u < 0 and u not in paths:
                oriented.append((p, u))
                paths[u] = paths[p] + [(p, u)]
                pending.append(u)
    assert len(paths) == len(internal)
    return {"vertices": internal, "root": root, "edges": oriented,
            "paths": paths, "leaves": {k: adj[k][0] for k in leaves}}


def check_sdr(d, seed):
    rng = random.Random(seed)
    labels = list(range(1, d + 1))
    pairs = list(combinations(labels, 2))
    trees = {ij: make_tree([k for k in labels if k not in ij], rng) for ij in pairs}
    cells, standard = [[], [], []], [[], [], []]
    boundary, standard_boundary, q, s, h = {}, {}, {}, {}, {}
    for i in labels:
        cell = ("v", i)
        cells[0].append(cell)
        standard[0].append(cell)
        boundary[cell] = standard_boundary[cell] = {}
        q[cell] = s[cell] = one(cell)
        h[cell] = {}
    D = {}
    for (i, j), tree in trees.items():
        se = ("e", i, j)
        standard[1].append(se)
        standard_boundary[se] = {("v", j): 1, ("v", i): -1}
        s[se] = one(("e", i, j, tree["root"]))
        for p in tree["vertices"]:
            cell = ("e", i, j, p)
            cells[1].append(cell)
            boundary[cell] = dict(standard_boundary[se])
            q[cell] = one(se)
            D[i, j, p] = {("b", i, j, u, v): 1 for u, v in tree["paths"][p]}
            h[cell] = D[i, j, p]
        for p, u in tree["edges"]:
            cell = ("b", i, j, p, u)
            cells[2].append(cell)
            boundary[cell] = {("e", i, j, u): 1, ("e", i, j, p): -1}
            q[cell] = h[cell] = {}
    corrected = {}
    for i, j, k in combinations(labels, 3):
        cell = ("t", i, j, k)
        cells[2].append(cell)
        standard[2].append(cell)
        p = trees[i, j]["leaves"][k]
        u = trees[j, k]["leaves"][i]
        v = trees[i, k]["leaves"][j]
        boundary[cell] = {("e", i, j, p): 1, ("e", j, k, u): 1,
                          ("e", i, k, v): -1}
        standard_boundary[cell] = {("e", i, j): 1, ("e", j, k): 1,
                                   ("e", i, k): -1}
        corrected[i, j, k] = add((1, one(cell)), (-1, D[i, j, p]),
                                  (-1, D[j, k, u]), (1, D[i, k, v]))
        s[cell] = corrected[i, j, k]
        q[cell] = one(cell)
        h[cell] = {}

    for dimension in range(3):
        for cell in cells[dimension]:
            assert linear(boundary, boundary[cell]) == {}
            assert linear(standard_boundary, q[cell]) == linear(q, boundary[cell])
            lhs = add((1, one(cell)), (-1, linear(s, q[cell])))
            rhs = add((1, linear(boundary, h[cell])), (1, linear(h, boundary[cell])))
            assert lhs == rhs                         # id - s q = d H + H d
            assert linear(q, h[cell]) == {}           # q H = 0
            assert linear(h, h[cell]) == {}           # H^2 = 0
        for cell in standard[dimension]:
            assert linear(q, s[cell]) == one(cell)    # q s = id
            assert linear(boundary, s[cell]) == linear(s, standard_boundary[cell])
            assert linear(h, s[cell]) == {}           # H s = 0

    cycles = []
    for i, j, k in combinations(range(2, d + 1), 3):
        cycle = add((1, corrected[i, j, k]), (-1, corrected[1, j, k]),
                    (1, corrected[1, i, k]), (-1, corrected[1, i, j]))
        assert linear(boundary, cycle) == {}
        nonroot_triangles = {cell: coefficient for cell, coefficient in cycle.items()
                             if cell[0] == "t" and 1 not in cell[1:]}
        assert nonroot_triangles == one(("t", i, j, k))
        cycles.append(cycle)

    incidence = Counter(cell for face in cells[2] for cell in boundary[face])
    assert set(incidence.values()) == {3}
    assert len(cells[1]) == comb(d, 2) * (d - 4)
    bigons = sum(cell[0] == "b" for cell in cells[2])
    assert bigons == comb(d, 2) * (d - 5)
    assert len(cycles) == comb(d - 1, 3)
    assert d - len(cells[1]) + len(cells[2]) == 1 + len(cycles)
    links = []
    for i in labels:
        vertices = [(j, p) for j in labels if j != i
                    for p in trees[tuple(sorted((i, j)))]["vertices"]]
        edges = []
        for j in labels:
            if j != i:
                edges += [((j, p), (j, u)) for p, u in
                          trees[tuple(sorted((i, j)))]["edges"]]
        for j, k in combinations([j for j in labels if j != i], 2):
            p = trees[tuple(sorted((i, j)))]["leaves"][k]
            u = trees[tuple(sorted((i, k)))]["leaves"][j]
            edges.append(((j, p), (k, u)))
        adjacency = {v: set() for v in vertices}
        for u, v in edges:
            adjacency[u].add(v)
            adjacency[v].add(u)
        assert all(len(neighbors) == 3 for neighbors in adjacency.values())
        reached = {vertices[0]}
        pending = [vertices[0]]
        while pending:
            for vertex in adjacency[pending.pop()]:
                if vertex not in reached:
                    reached.add(vertex)
                    pending.append(vertex)
        assert len(reached) == len(vertices)
        assert len(edges) - len(vertices) + 1 == comb(d - 2, 2)
        links.append({"vertex": i, "V": len(vertices), "E": len(edges),
                      "b1": comb(d - 2, 2)})
    return {"degree": d, "seed": seed, "cell_dimensions": list(map(len, cells)),
            "bigons": bigons, "H2_basis_size": len(cycles),
            "SDR_identities": "all exact integer identities verified", "links": links}


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for b in vertices[1:]:
        for remaining in perfect_matchings([x for x in vertices if x not in (a, b)]):
            yield tuple(sorted(((a, b),) + remaining))


def link_from_partitions(vertex, partitions):
    others = [j for j in range(6) if j != vertex]
    adjacency = {(j, k): set() for j in others for k in range(2)}
    def connect(u, v):
        adjacency[u].add(v)
        adjacency[v].add(u)
    for j in others:
        connect((j, 0), (j, 1))
    for j, k in combinations(others, 2):
        pp = partitions[tuple(sorted((vertex, j)))]
        qq = partitions[tuple(sorted((vertex, k)))]
        connect((j, next(a for a in range(2) if k in pp[a])),
                (k, next(a for a in range(2) if j in qq[a])))
    return adjacency


def canonical_petersen():
    adjacency = {(a, c): set() for a in range(2) for c in range(5)}
    for c in range(5):
        for u, v in [((0, c), (1, c)), ((0, c), (0, (c + 1) % 5)),
                     ((1, c), (1, (c + 2) % 5))]:
            adjacency[u].add(v)
            adjacency[v].add(u)
    return adjacency


def isomorphic(first, second):
    if len(first) != len(second):
        return False
    assigned = {}
    used = set()
    def visit():
        if len(assigned) == len(first):
            return True
        u = max((x for x in first if x not in assigned),
                key=lambda x: sum(y in assigned for y in first[x]))
        for v in second:
            if v in used or len(first[u]) != len(second[v]):
                continue
            if all((x in first[u]) == (y in second[v]) for x, y in assigned.items()):
                assigned[u] = v
                used.add(v)
                if visit():
                    return True
                used.remove(v)
                del assigned[u]
        return False
    return visit()


def check_petersen():
    vertices = list(range(6))
    edges = list(combinations(vertices, 2))
    matchings = list(perfect_matchings(vertices))
    factorizations = [tuple(ff) for ff in combinations(range(len(matchings)), 5)
                     if len({edge for k in ff for edge in matchings[k]}) == 15]
    assert len(matchings) == 15 and len(factorizations) == 6
    assert all(sum(m in ff for ff in factorizations) == 2 for m in range(15))
    lookup = [{edge: k for k in ff for edge in matchings[k]} for ff in factorizations]
    petersen = canonical_petersen()
    for ff in factorizations:
        partitions = {edge: tuple(e for e in matchings[k] if e != edge)
                      for k in ff for edge in matchings[k]}
        assert all(isomorphic(link_from_partitions(i, partitions), petersen)
                   for i in vertices)

    local_count = 0
    i = 5
    options = {}
    for j in range(5):
        a, b, c, d = [x for x in range(5) if x != j]
        options[j] = [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]
    for choices in product(range(3), repeat=5):
        partitions = {(j, i): options[j][choices[j]] for j in range(5)}
        graph = link_from_partitions(i, partitions)
        is_petersen = isomorphic(graph, petersen)
        local_matchings = [tuple(sorted(((j, i),) + partitions[j, i])) for j in range(5)]
        is_factorization = len({edge for m in local_matchings for edge in m}) == 15
        assert is_petersen == is_factorization
        local_count += is_petersen
    assert local_count == 6

    solutions = []
    for assignment in product(range(6), repeat=6):
        if all(lookup[assignment[i]][i, j] == lookup[assignment[j]][i, j]
               for i, j in edges):
            solutions.append(assignment)
    assert solutions == [tuple([i] * 6) for i in range(6)]

    explicit = [tuple(sorted((tuple(sorted((5, c))),
                              tuple(sorted(((c + 1) % 5, (c - 1) % 5))),
                              tuple(sorted(((c + 2) % 5, (c - 2) % 5))))))
                for c in range(5)]
    explicit_set = set(explicit)
    inversion = {5: 0, 0: 5, 1: 1, 2: 3, 3: 2, 4: 4}
    inverted = {tuple(sorted(tuple(sorted((inversion[a], inversion[b]))) for a, b in m))
                for m in explicit}
    assert inverted == explicit_set
    return {"label_infinity": 5, "perfect_matchings": 15, "one_factorizations": 6,
            "local_partition_systems_tested": 3 ** 5,
            "local_Petersen_systems": local_count,
            "global_local_factorization_assignments_tested": 6 ** 6,
            "global_compatible_systems": len(solutions),
            "all_global_solutions_have_one_common_factorization": True,
            "explicit_F5_factorization": explicit,
            "all_six_links_verified_by_graph_isomorphism": True,
            "inversion_symmetry_verified": True}


def main():
    cases = [check_sdr(d, seed) for d in range(5, 13) for seed in (0, 1, 23, 20261027)]
    result = {"scope": "Finite exact certificates supplement the general proofs; no symplectic gluing is checked.",
              "SDR_cases": cases, "Petersen_classification": check_petersen()}
    destination = Path(__file__).with_name("verification_v8_results.json")
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "all checks passed", "integer_SDR_cases": len(cases),
                      "degrees": [5, 12], "simultaneous_Petersen_systems": 6,
                      "results": str(destination)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
