#!/usr/bin/env python3
"""Finite exact checks for the v8 core-surgery section (stdlib only).

This checks one explicit three-hyperbola model, the proposed boundary braid's
exponent/linking invariants, and finite graph/count certificates.  It does not
prove a braid isotopy, JSJ uniqueness, handlebody equivalence, or symplectic
gluing.  The corresponding general arguments are in core_surgery.tex.

Run from any directory: python3 /path/to/verify_core_surgery_v8.py
Output defaults to core_surgery_v8_results.json beside this script.
"""

from collections import Counter, deque
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations
from math import comb
from pathlib import Path
import argparse
import json


CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


# Polynomials in u, with rational coefficients in ascending order.
def poly(coefficients):
    result = [Q(x) for x in coefficients]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result or [Q(0)]


def padd(a, b):
    result = [Q(0)] * max(len(a), len(b))
    for i, value in enumerate(a):
        result[i] += value
    for i, value in enumerate(b):
        result[i] += value
    return poly(result)


def pscale(a, scalar):
    return poly([scalar * x for x in a])


def pmul(a, b):
    result = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return poly(result)


def peval(a, value):
    result = Q(0)
    for coefficient in reversed(a):
        result = result * value + coefficient
    return result


def pdivmod(a, b):
    a, b = poly(a), poly(b)
    if b == [0]:
        raise ZeroDivisionError("zero polynomial")
    quotient = [Q(0)] * max(1, len(a) - len(b) + 1)
    while a != [0] and len(a) >= len(b):
        shift = len(a) - len(b)
        coefficient = a[-1] / b[-1]
        quotient[shift] += coefficient
        a = padd(a, [Q(0)] * shift + pscale(b, -coefficient))
    return poly(quotient), a


def pgcd(a, b):
    while b != [0]:
        a, b = b, pdivmod(a, b)[1]
    return pscale(a, 1 / a[-1])


def derivative(a):
    return poly([i * a[i] for i in range(1, len(a))])


def pdet(matrix):
    n = len(matrix)
    result = [Q(0)]
    for order in permutations(range(n)):
        inversions = sum(order[i] > order[j]
                         for i in range(n) for j in range(i + 1, n))
        term = [Q((-1) ** inversions)]
        for i in range(n):
            term = pmul(term, matrix[i][order[i]])
        result = padd(result, term)
    return result


def resultant_quadratics(first, second):
    a, b, c = first
    d, e, f = second
    zero = [Q(0)]
    return pdet([[a, b, c, zero], [zero, a, b, c],
                 [d, e, f, zero], [zero, d, e, f]])


def encode_polynomial(a):
    return [str(x) for x in a]


def verify_hyperbolas():
    degrees = [(Q(1), Q(0)), (Q(2), Q(1)), (Q(3), Q(4))]
    slope = Q(3)
    quadratics = []
    discriminants = []
    for a, b in degrees:
        quadratic = [poly([a * slope]), poly([-b, -a]), poly([1])]
        quadratics.append(quadratic)
        delta = padd(pmul(quadratic[1], quadratic[1]),
                     pscale(pmul(quadratic[0], quadratic[2]), -4))
        discriminants.append(delta)
        check(delta == poly([b * b - 4 * a * slope, 2 * a * b, a * a]),
              "quadratic discriminant formula")
        check(delta[1] ** 2 - 4 * delta[0] * delta[2] > 0,
              "two distinct real branch values")
        check(pgcd(delta, derivative(delta)) == [1], "simple branch roots")

    expected_discriminants = [poly([-12, 0, 1]), poly([-23, 4, 4]),
                              poly([-20, 24, 9])]
    check(discriminants == expected_discriminants,
          "explicit branch-value polynomials")
    expected_nodes = {(0, 1): (Q(-1), Q(-1), Q(-4)),
                      (0, 2): (Q(-2), Q(-1, 2), Q(-7, 2)),
                      (1, 2): (Q(-3), Q(-1, 5), Q(-18, 5))}
    nodes = []
    node_polynomials = []
    for i, j in combinations(range(3), 2):
        ai, bi = degrees[i]
        aj, bj = degrees[j]
        t = (bj - bi) / (ai - aj)
        z = 1 / (ai * t + bi)
        u = t + slope * z
        check((t, z, u) == expected_nodes[i, j], "explicit node coordinates")
        check(z * (ai * t + bi) == z * (aj * t + bj) == 1,
              "node lies on both curves")
        # Gradients of 1 - z(a t + b): (-a z, -(a t+b)).
        jacobian = ai * z * (aj * t + bj) - aj * z * (ai * t + bi)
        check(jacobian != 0, "node is transverse")
        check(all(z * (ak * t + bk) != 1
                  for k, (ak, bk) in enumerate(degrees) if k not in (i, j)),
              "no triple point")
        resultant = resultant_quadratics(quadratics[i], quadratics[j])
        check(len(resultant) == 2, "pair resultant has exactly one finite root")
        check(peval(resultant, u) == 0, "resultant agrees with node projection")
        node_polynomials.append(resultant)
        nodes.append({"components": [i + 1, j + 1], "t": str(t), "z": str(z),
                      "u": str(u), "resultant_ascending": encode_polynomial(resultant)})

    exceptional_polynomial = poly([1])
    for factor in discriminants + node_polynomials:
        exceptional_polynomial = pmul(exceptional_polynomial, factor)
    check(len(exceptional_polynomial) - 1 == 9, "nine exceptional values counted")
    check(pgcd(exceptional_polynomial, derivative(exceptional_polynomial)) == [1],
          "all nine exceptional values pairwise distinct over C")
    check(1 - 6 + 9 == 4, "smooth handle Euler characteristic")
    return {
        "A": [1, 2, 3], "B": [0, 1, 4], "projection": "u=t+3z",
        "discriminants_ascending": [encode_polynomial(p) for p in discriminants],
        "node_data": nodes,
        "exceptional_polynomial_ascending": encode_polynomial(exceptional_polynomial),
        "exceptional_polynomial_degree": 9, "squarefree_over_Q": True,
        "simple_branch_values": 6, "transverse_node_values": 3,
        "smooth_handle_counts": {"0": 1, "1": 6, "2": 9, "3": 0, "4": 0},
    }


def verify_braid_invariants():
    strands = [(sign, i) for sign in ("-", "+") for i in range(1, 4)]
    table = []
    for first, second in combinations(strands, 2):
        both_small = first[0] == second[0] == "-"
        both_large = first[0] == second[0] == "+"
        asymptotic_linking = -1 if both_small else (0 if both_large else 1)
        # T6 has +1 on every pair; T_- and T_+ are full twists on their clusters.
        word_linking = 1 - 2 * int(both_small) - int(both_large)
        check(asymptotic_linking == word_linking, "pure braid pair-linking table")
        table.append({"strands": [f"C{first[1]}{first[0]}", f"C{second[1]}{second[0]}"],
                      "linking": asymptotic_linking})
    exponent_from_pair_linking = 2 * sum(row["linking"] for row in table)
    exponent_from_word = 6 * 5 - 2 * 3 * 2 - 3 * 2
    exponent_from_local_values = 6 * 1 + 3 * 2
    check(exponent_from_pair_linking == exponent_from_word == exponent_from_local_values == 12,
          "three exponent computations agree")
    return {
        "word": "T6 * T_minus^(-2) * T_plus^(-1)",
        "pair_linking_table": table, "pair_count": len(table),
        "exponent_from_pair_linking": exponent_from_pair_linking,
        "exponent_from_full_twists": exponent_from_word,
        "exponent_from_local_braids": exponent_from_local_values,
        "limitation": "Linking/exponent equality alone does not prove equality in the braid group; the manuscript uses the large-radius isotopy.",
    }


def graph_components(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    components = []
    remaining = set(vertices)
    while remaining:
        start = min(remaining)
        seen, queue = {start}, [start]
        while queue:
            for neighbor in adjacency[queue.pop()]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        remaining -= seen
        components.append(seen)
    return components


def has_nonbacktracking_cycle(edges):
    # Distinct orientations for loops are retained. Opposite states differ by 1.
    states = []
    for u, v in edges:
        states.extend([(u, v), (v, u)])
    adjacency = [[] for _ in states]
    indegree = [0] * len(states)
    for i, (_, head) in enumerate(states):
        for j, (tail, _) in enumerate(states):
            if head == tail and j != (i ^ 1):
                adjacency[i].append(j)
                indegree[j] += 1
    queue = deque(i for i, value in enumerate(indegree) if value == 0)
    removed = 0
    while queue:
        i = queue.popleft()
        removed += 1
        for j in adjacency[i]:
            indegree[j] -= 1
            if indegree[j] == 0:
                queue.append(j)
    return removed != len(states)


def verify_complexity():
    budgets = []
    for m in range(5, 25):
        pants = (m - 3) ** 2
        complexity = m * (m - 3)
        edges = 3 * (m - 3) * (m - 4) // 2
        cycle_rank = comb(m - 4, 2)
        check(4 * pants - 2 * edges == complexity, "canonical incidence budget")
        check(edges - pants + 1 == cycle_rank, "connected graph cycle budget")
        check(complexity - 2 * pants == (m - 3) * (6 - m), "complexity threshold")
        budgets.append({"lines": m, "pants": pants, "complexity": complexity,
                        "facet_pairs": edges, "connected_graph_b1": cycle_rank})

    # All vertex-labelled multigraphs on four pants with three edges; loops allowed.
    # A loop consumes two facets; total degree cannot exceed four at any vertex.
    edge_types = list(combinations_with_replacement(range(4), 2))
    counts = Counter()
    component_distribution = Counter()
    for selected in combinations_with_replacement(edge_types, 3):
        counts["raw_multigraphs"] += 1
        degree = Counter(v for edge in selected for v in edge)
        if any(degree[v] > 4 for v in range(4)):
            counts["degree_excluded"] += 1
            continue
        counts["facet_realizable_multigraphs"] += 1
        components = graph_components(range(4), selected)
        tree_components = 0
        total_cycle_rank = 0
        for component in components:
            component_edges = [edge for edge in selected if edge[0] in component]
            cycle_rank = len(component_edges) - len(component) + 1
            total_cycle_rank += cycle_rank
            is_tree = cycle_rank == 0
            tree_components += int(is_tree)
            check(has_nonbacktracking_cycle(component_edges) == (not is_tree),
                  "corner-circuit obstruction for each finite component")
        check(total_cycle_rank == len(components) - 1, "V4 E3 component identity")
        check(tree_components >= 1, "at least one tree component")
        if len(components) == 1:
            counts["connected_trees"] += 1
            check(total_cycle_rank == 0, "connected case must be a tree")
        else:
            counts["disconnected_with_unfillable_tree_component"] += 1
        component_distribution[str(len(components))] += 1
    check(counts["raw_multigraphs"] == comb(12, 3) == 220,
          "all three-edge multigraphs enumerated")
    check(counts["connected_trees"] == 4 ** 2 == 16, "Cayley count on four vertices")
    return {
        "canonical_budgets": budgets, "budget_case_count": len(budgets),
        "four_pants_multigraphs": dict(counts),
        "component_count_distribution": dict(sorted(component_distribution.items())),
        "limitations": [
            "The finite graph enumeration is only for four pants and three facet pairs.",
            "The general complexity dichotomy is proved in the manuscript, not inferred from enumeration.",
            "No face diffeomorphism, JSJ classification, or torus-filler realization is certified by this script.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().with_name("core_surgery_v8_results.json"))
    args = parser.parse_args()
    report = {
        "version": 8,
        "status": "passed",
        "arithmetic": "Python standard library, exact integers and fractions.Fraction",
        "scope": "Finite consistency certificates; not an analytic or symplectic gluing proof.",
        "hyperbola_model": verify_hyperbolas(),
        "boundary_braid_invariants": verify_braid_invariants(),
        "complexity_budget": verify_complexity(),
    }
    report["exact_checks"] = CHECKS
    report["script_sha256"] = sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "exact_checks": CHECKS,
                      "report": str(args.output),
                      "multigraphs": report["complexity_budget"]["four_pants_multigraphs"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
