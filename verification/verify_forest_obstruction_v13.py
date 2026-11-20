#!/usr/bin/env python3
"""Exact checks supporting the v13 forest obstruction.

This verifies polynomial identities and all labelled forests on five vertices.
It does not replace the unbounded classification proof for a continuing leaf.
It does not claim the unresolved arbitrary three-high sign conjecture.
Only Python's standard library is required.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json


class Poly(dict):
    """Integer multivariate polynomials, represented by exponent tuples."""
    nvars = 5

    @staticmethod
    def const(value):
        return Poly({(0,) * Poly.nvars: value}) if value else Poly()

    @staticmethod
    def var(index):
        return Poly({tuple(int(i == index) for i in range(Poly.nvars)): 1})

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Poly) else Poly.const(value)

    def __add__(self, other):
        out = Counter(self)
        for monomial, coefficient in self.coerce(other).items():
            out[monomial] += coefficient
        return Poly({key: value for key, value in out.items() if value})

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        out = Counter()
        for left, a in self.items():
            for right, b in self.coerce(other).items():
                out[tuple(i + j for i, j in zip(left, right))] += a * b
        return Poly({key: value for key, value in out.items() if value})

    __rmul__ = __mul__

    def __pow__(self, exponent):
        out = self.const(1)
        for _ in range(exponent):
            out = out * self
        return out


def remaining_support_agenda_v13():
    """Exact finite graph agenda after no-tree and no-pure-cycle theorems.

    Return the 20 unlabelled nonempty support shapes not eliminated by those
    graph-level theorems.  The word `remaining` does not assert integer or
    geometric realizability.  All 1024 labelled subgraphs of K5 are checked.
    This function is intended for inclusion in verify_forest_obstruction_v13.py.
    """
    from itertools import combinations, permutations
    from math import factorial

    vertices = tuple(range(5))
    all_edges = tuple(combinations(vertices, 2))
    classes = {}
    excluded = {"empty_support": 0, "tree_component": 0,
                "pure_cycle_component": 0}
    for mask in range(1 << len(all_edges)):
        edges = tuple(e for k, e in enumerate(all_edges) if (mask >> k) & 1)
        adjacency = {i: set() for i in vertices}
        for a, b in edges:
            adjacency[a].add(b)
            adjacency[b].add(a)
        seen = set()
        components = []
        for i in vertices:
            if i in seen:
                continue
            stack = [i]
            seen.add(i)
            component = []
            while stack:
                v = stack.pop()
                component.append(v)
                for w in adjacency[v]:
                    if w not in seen:
                        seen.add(w)
                        stack.append(w)
            if len(component) > 1:
                components.append(tuple(component))
        if not components:
            excluded["empty_support"] += 1
            continue
        if any(sum(len(adjacency[v]) for v in c) // 2 == len(c) - 1
               for c in components):
            excluded["tree_component"] += 1
            continue
        if any(all(len(adjacency[v]) == 2 for v in c) for c in components):
            excluded["pure_cycle_component"] += 1
            continue
        assert len(components) == 1
        active_vertices = sorted(components[0])
        n = len(active_vertices)
        assert n in (4, 5)
        relabel = {v: i for i, v in enumerate(active_vertices)}
        active_edges = tuple((relabel[a], relabel[b]) for a, b in edges)
        canonical = min(
            tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in active_edges))
            for p in permutations(range(n)))
        key = (n, canonical)
        classes[key] = classes.get(key, 0) + 1

    rows = []
    for (n, edges), labelled_count in classes.items():
        degree = [sum(v in e for e in edges) for v in range(n)]
        leaf_edges = []
        transfer_paths = []
        for v in range(n):
            if degree[v] != 1:
                continue
            w = next(u for e in edges if v in e for u in e if u != v)
            leaf_edges.append([v, w])
            if degree[w] == 2:
                k = next(u for e in edges if w in e for u in e
                         if u != w and u != v)
                transfer_paths.append([v, w, k])
        automorphisms = sum(
            tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in edges)) == edges
            for p in permutations(range(n)))
        assert labelled_count == factorial(5) // (automorphisms * factorial(5-n))
        rows.append({
            "vertices": n, "edges_count": len(edges),
            "degree_sequence": sorted(degree, reverse=True),
            "canonical_edges": [list(e) for e in edges],
            "cycle_rank": len(edges)-n+1,
            "leaf_count": len(leaf_edges), "leaf_edges": leaf_edges,
            "exact_transfer_paths": transfer_paths,
            "labelled_K5_count": labelled_count,
            "automorphism_order": automorphisms,
        })
    rows.sort(key=lambda r: (r["vertices"], r["edges_count"],
                             r["degree_sequence"], r["canonical_edges"]))
    counters = {4: 0, 5: 0}
    for row in rows:
        n = row["vertices"]
        counters[n] += 1
        row["shape_id"] = f"G{n}_{counters[n]}"
    assert counters == {4: 3, 5: 17}
    assert len(rows) == 20
    assert sum(r["labelled_K5_count"] for r in rows) == 686
    assert sum(excluded.values()) + 686 == 1024
    assert [r["shape_id"] for r in rows if r["exact_transfer_paths"]] == ["G5_1"]
    return {
        "scope": "Graph-level necessary shapes only, not integer or geometric realizations.",
        "labelled_K5_graphs_checked": 1024,
        "labelled_nonempty_supports_remaining": 686,
        "unlabelled_shapes_remaining": 20,
        "four_vertex_shapes": 3, "five_vertex_shapes": 17,
        "excluded_counts_in_filter_order": excluded,
        "canonical_rule": "Lexicographically smallest sorted edge tuple on active labels 0,...,n-1.",
        "shapes": rows,
    }


checks = []


def identity(name, left, right=0):
    assert Poly.coerce(left) - Poly.coerce(right) == {}, name
    checks.append(name)


def verify_family(name, q, p, expected_D):
    for i in range(4):
        identity(f"{name}: row {i}", sum(p[i]), -q[i])
    for i, j in combinations(range(4), 2):
        identity(f"{name}: pair {i},{j}", p[i][j] * p[j][i], q[i] * q[j] - 1)
    defect = [-q[i] - sum(p[j][i] for j in range(4)) for i in range(4)]
    for i, expected in enumerate(expected_D):
        if expected is not None:
            identity(f"{name}: defect {i}", defect[i], expected)
    identity(f"{name}: total defect", sum(defect))


h, t, q_other, loss_1, loss_2 = [Poly.var(i) for i in range(5)]
# The negative entry is -t with t >= 1. The other two deficits loss_i
# are nonnegative because every signed divisor x_i is <= q_i - 1.
high_sum = 1 - t + (h - 1 - loss_1) + (q_other - 1 - loss_2)
identity("center bound gap", h + q_other - 2 - high_sum,
         t - 1 + loss_1 + loss_2)

# Positive outgoing leaf puncture: the complete continuing family.
a = h * (h + 1) + 1
b = (h + 1) * (h + 2) + 1
p = [
    [0, -(h + 1) ** 2, h + 1, -1],
    [-(h ** 2 + 2 * h + 2), 0, -h - 2, 1],
    [h, -h - 1, 0, 0],
    [-h * (h + 1), (h + 1) * (h + 2), -2 * h - 3, 0],
]
verify_family("positive leaf", [a, b, 1, 1], p, [a, -b, None, None])
identity("positive leaf continuation divisor", b - 1, (h + 1) * (h + 2))
identity("positive leaf continuation congruence",
         -(h + 1) - (h ** 2 + 2 * h + 2), -b)

# Negative outgoing leaf puncture, h = 1.
a = 2 * t + 1
b = 6 * t + 1
p = [
    [0, -4 * t, 2 * t, -1],
    [-3 * t - 2, 0, -3 * t, 1],
    [1, -2, 0, 0],
    [-2 * t, 6 * t, -4 * t - 1, 0],
]
verify_family("negative leaf h=1", [a, b, 1, 1], p,
              [3 * t, 1 - 8 * t, None, None])
identity("negative h=1 positive residue remainder", b - 1, 2 * (3 * t + 2) - 4)
identity("negative h=1 negative residue remainder", b - 1, 2 * (3 * t - 1) + 2)
identity("negative h=1 burden gap", -(1 - 8 * t) - b, 2 * (t - 1))

# Negative outgoing leaf puncture, h = 2: exact local family which cannot
# continue across its other high edge, by the displayed divisor remainders.
a = 6 * t + 1
b = 20 * t - 1
p = [
    [0, -12 * t + 1, 6 * t, -2],
    [-10 * t - 2, 0, -10 * t + 1, 2],
    [1, -2, 0, 0],
    [-3 * t, 10 * t - 1, -7 * t, 0],
]
verify_family("negative leaf h=2", [a, b, 1, 1], p,
              [7 * t, 3 - 18 * t, None, None])
identity("negative h=2 positive residue remainder", b - 1, 2 * (10 * t + 2) - 6)
identity("negative h=2 negative residue remainder", b - 1, 2 * (10 * t - 3) + 4)
identity("negative h=2 burden deficit", b + 3 - 18 * t, 2 * t + 2)


def components_on_five(edges):
    parent = list(range(5))

    def find(x):
        while x != parent[x]:
            x = parent[x]
        return x

    for a, b in edges:
        a, b = find(a), find(b)
        if a == b:
            return None
        parent[a] = b
    components = {}
    for vertex in range(5):
        components.setdefault(find(vertex), []).append(vertex)
    return list(components.values())


all_edges = list(combinations(range(5), 2))
forest_count = 0
connected_tree_count = 0
shape_counts = Counter()
for mask in range(1 << len(all_edges)):
    edges = [edge for i, edge in enumerate(all_edges) if mask & (1 << i)]
    components = components_on_five(edges)
    if components is None:
        continue
    forest_count += 1
    if len(components) == 1:
        connected_tree_count += 1
    degree = Counter(vertex for edge in edges for vertex in edge)
    for component in components:
        if len(component) == 1:
            continue
        signature = tuple(sorted(degree[v] for v in component))
        if max(signature) <= 2:
            shape = f"path_on_{len(component)}_vertices"
        elif signature == (1, 1, 1, 3):
            shape = "three_leaf_star"
        elif signature == (1, 1, 1, 1, 4):
            shape = "four_leaf_star"
        elif signature == (1, 1, 1, 2, 3):
            shape = "once_subdivided_three_leaf_star"
        else:
            raise AssertionError((edges, signature))
        shape_counts[shape] += 1
assert forest_count == 291
assert connected_tree_count == 125

# A genuine integral local example invalidates the stronger claim that
# every leaf-compatible pair already transfers a coefficient <= -b.
q = [19, 1, 1, 7]
p = [[0, -9, 2, -12], [-2, 0, 0, 1], [9, -7, 0, -3], [-11, 6, -2, 0]]
w = [Fraction(19), Fraction(1), Fraction(37, 18), Fraction(13, 12)]
assert all(sum(p[i]) == -q[i] for i in range(4))
assert all(p[i][j] * p[j][i] == q[i] * q[j] - 1 for i, j in combinations(range(4), 2))
assert all(w[j] - w[i] * p[i][j] / q[i] > 0
           for i in range(4) for j in range(4) if i != j)
defect = [-q[i] - sum(p[j][i] for j in range(4)) for i in range(4)]
assert defect == [-15, 9, -1, 7]
assert all((q[0] - 1) % abs(x) != 0 for x in (12, -7))

result = {
    "remaining_support_agenda": remaining_support_agenda_v13(),
    "version": "v13",
    "passed": True,
    "polynomial_identities": len(checks),
    "identity_names": checks,
    "labelled_graphs_inspected": 1024,
    "labelled_forests": forest_count,
    "labelled_connected_trees": connected_tree_count,
    "nontrivial_tree_component_instances": dict(sorted(shape_counts.items())),
    "noncontinuing_local_example": {
        "q": q, "p": p, "D": defect, "weights": list(map(str, w)),
        "possible_continuation_residues": [12, -7],
        "continuation_numerator_product": 18,
    },
    "limitations": [
        "The complete unbounded leaf classification is a separate written proof.",
        "The graph enumeration only checks the finite K5 tree shapes.",
        "No arbitrary three-high all-positive exclusion is claimed.",
        "No exclusion of all tree subgraphs inside a cyclic component is claimed.",
    ],
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
output = Path(__file__).with_name("forest_obstruction_verification_v13.json")
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"passed": True, "polynomial_identities": len(checks),
                  "labelled_forests": forest_count, "output": str(output)},
                 ensure_ascii=False))
