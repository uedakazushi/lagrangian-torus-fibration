#!/usr/bin/env python3
"""Exact algebra and finite combinatorics supporting the v15 K2,3 theorem.

This is a supplementary audit of the written proof, not a formal proof checker.
All parameter identities are polynomial identities over Z.  The only finite
enumerations are the eight arrow/sign choices on three vertices and the 1024
simple labelled supports on five vertices.  No denominator or entry is bounded.
Only the Python standard library is used; there are no module dependencies.
"""

from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json


class Poly:
    """Sparse integer polynomials, with sorted variable tuples as monomials."""
    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @classmethod
    def var(cls, name):
        return cls({(name,): 1})

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls({(): int(value)})

    def __add__(self, other):
        terms = self.terms.copy()
        for m, c in self.coerce(other).terms.items():
            terms[m] = terms.get(m, 0) + c
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        terms = {}
        for m, c in self.terms.items():
            for n, d in self.coerce(other).terms.items():
                monomial = tuple(sorted(m + n))
                terms[monomial] = terms.get(monomial, 0) + c * d
        return Poly(terms)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms


def adjacency(edges):
    out = {i: set() for i in range(5)}
    for i, j in edges:
        out[i].add(j)
        out[j].add(i)
    return out


def v14_filter(edges):
    """Previously proved graph filters, in their v14 certificate order.

    Some earlier obstructions use D opposition. This baseline's hypotheses
    must not be confused with the weaker hypotheses of the new K2,3 theorem.
    """
    if not edges:
        return "empty_support"
    adj = adjacency(edges)
    seen, components = set(), []
    for start in range(5):
        if start in seen or not adj[start]:
            continue
        component, stack = {start}, [start]
        while stack:
            v = stack.pop()
            for u in adj[v] - component:
                component.add(u)
                stack.append(u)
        seen |= component
        components.append(component)
    if any(sum(len(adj[v]) for v in c) // 2 == len(c) - 1 for c in components):
        return "tree_component"
    if any(all(len(adj[v]) == 2 for v in c) for c in components):
        return "pure_cycle_component"
    for i, j in edges:
        if len(adj[i]) == len(adj[j]) == 2 and adj[i] - {j} == adj[j] - {i}:
            return "triangle_with_two_degree_two_vertices"
    leaves = [i for i in range(5) if len(adj[i]) == 1]
    if len(leaves) == 1:
        remaining = set(range(5)) - set(leaves)
        if all(len(adj[v] & remaining) == 2 for v in remaining):
            return "C4_with_pendant_edge"
    return None


def is_k23(edges):
    adj = adjacency(edges)
    centers = {i for i in range(5) if len(adj[i]) == 3}
    legs = {i for i in range(5) if len(adj[i]) == 2}
    return (len(centers) == 2 and len(legs) == 3
            and all(adj[i] == legs for i in centers)
            and all(adj[i] == centers for i in legs))


ALL_PERMUTATIONS = tuple(permutations(range(5)))


def canonical_edges(edges):
    return min(tuple(sorted(tuple(sorted((perm[i], perm[j]))) for i, j in edges))
               for perm in ALL_PERMUTATIONS)


def main():
    identities = []

    def identity(name, lhs, rhs):
        if lhs != rhs:
            raise AssertionError(name)
        identities.append(name)

    H, w, c, e, E, s, z, x, y = map(Poly.var, "H w c e E s z x y".split())
    r, N = H + w, H * (H + 1)
    # a and b, after multiplication by their respective denominators H,H+1.
    an, bn = c * r * w + H, e * (r + 1) * w + H + 1
    identity("pair product gives Ece=e-c+1 after clearing H(H+1)",
             (an - c * H) * (bn + e * (H + 1)) - an * bn + N,
             N * (e - c + 1) - (N - w * w) * c * e)
    identity("negative E rearrangement", E * c * e - (e - c + 1),
             c * (1 + E * e) - (e + 1))
    identity("positive E upper-bound rearrangement", E * c * e - (e - c + 1),
             e * (E * c - 1) + (c - 1))
    identity("c=1 would imply E=1", E * e - e, (E - 1) * e)
    identity("e=1 gives cE=2-c", E * c - (2 - c), c * (E + 1) - 2)
    identity("H(H+1) lies above H squared", N - H * H, H)
    identity("H(H+1) lies below (H+1) squared", (H + 1) * (H + 1) - N, H + 1)
    identity("w=1 gives E>=1/2 after clearing 2N", 2 * (N - 1) - N,
             (H - 1) * (H + 2))

    a, b = s * w + 1, z * w + 1
    cc, ee = s - x, z - y
    identity("X=-c satisfies the clutching residue", -cc - (a - cc), -a)
    identity("X=a-c satisfies the clutching residue", (a - cc) - (a - cc), 0)
    identity("Y=e satisfies the clutching residue", ee - (b + ee), -b)
    identity("Y=e-b satisfies the clutching residue", (ee - b) - (b + ee), -2 * b)
    identity("a-c is strictly above half of a-1",
             2 * (a - cc) - (a - 1), s * (w - 2) + 2 * x + 2)
    identity("a-c is a proper candidate divisor", (a - 1) - (a - cc), cc - 1)
    identity("b-e is strictly above half of b-1",
             2 * (b - ee) - (b - 1), z * (w - 2) + 2 * y + 2)
    identity("b-e is a proper candidate divisor when e>=2",
             (b - 1) - (b - ee), ee - 1)
    identity("reverse entry sum is E-1 after clearing H(H+1)",
             -r * w * (H + 1) + (r + 1) * w * H, -w * w)
    identity("exceptional node after clearing H", H + r * w + H, 2 * H + r * w)
    identity("rw/H exceeds 2w when w>H", r * w - 2 * w * H, w * (w - H))

    # This is the finite combinatorics of arrows, not a bound on parameters.
    arrows = []
    choices = [[j for j in range(3) if j != i] for i in range(3)]
    for targets in product(*choices):
        mutual = any(targets[j] == i for i, j in enumerate(targets))
        if not mutual:
            assert all(targets[targets[targets[i]]] == i for i in range(3))
            arrows.append(list(targets))
    assert arrows == [[1, 2, 0], [2, 0, 1]]

    rr, S, T, rr2, S2, T2 = map(Poly.var, "r S T r_next S_next T_next".split())
    L, L2 = T - S + 1, T2 - S2 + 1

    def oriented_data(sign, r0, s0, t0):
        l0 = t0 - s0 + 1
        return (r0, s0, r0 + 1, t0, 0, -l0) if sign == "+" else (
            t0, r0 + 1, s0, r0, -l0, 0)

    expected_nodes = {
        "++": (1 - rr + S2, 2 + rr - T2, 1 + L2),
        "+-": (2 - rr + rr2, 2 + rr - rr2, 1),
        "-+": (1 - T + S2, 1 + S - T2, 1 + L + L2),
        "--": (2 - T + rr2, 1 + S - rr2, 1 + L),
    }
    for signs, targets in expected_nodes.items():
        aa, bb, cc, dd, uu, vv = oriented_data(signs[0], rr, S, T)
        aa2, bb2, cc2, dd2, uu2, vv2 = oriented_data(signs[1], rr2, S2, T2)
        actual = (1 - aa + bb2, 1 + cc - dd2, 1 - uu - vv2)
        for index in range(3):
            identity(f"{signs} low-edge node at puncture {index}", actual[index], targets[index])
        identity(f"{signs} three low-edge nodes total five", sum(actual), 5)
    identity("positive branch forces T>=r+3", rr * (rr + 2) - (rr + 1) * (rr + 1), -1)
    u, v, t = map(Poly.var, ("u", "v", "t"))
    identity("mixed minus-plus positive branches exceed five nodes", 1 + (3 + u) + (3 + v),
             7 + u + v)
    r3, T3 = map(Poly.var, ("r_third", "T_third"))
    identity("constant plus assignment node sum",
             (2 + rr - T2) + (2 + rr2 - T3) + (2 + r3 - T),
             6 + (rr - T) + (rr2 - T2) + (r3 - T3))
    identity("constant minus assignment node sum",
             (2 - T + rr2) + (2 - T2 + r3) + (2 - T3 + rr),
             6 + (rr - T) + (rr2 - T2) + (r3 - T3))
    identity("either constant assignment has negative node sum",
             6 - (3 + u) - (3 + v) - (3 + t), -3 - u - v - t)
    sign_cases = []
    for signs in product("+-", repeat=3):
        if len(set(signs)) > 1:
            pairs = [[i, (i + 1) % 3] for i in range(3)
                     if signs[i] == "-" and signs[(i + 1) % 3] == "+"]
            assert pairs
            reason = "A listed minus-plus pair has third node at least seven."
        else:
            pairs = []
            reason = "The sum of three center-puncture nodes is at most minus three."
        sign_cases.append({"signs": list(signs), "minus_plus_pairs": pairs,
                           "exclusion": reason})
    assert len(sign_cases) == 8
    assert sum(bool(case["minus_plus_pairs"]) for case in sign_cases) == 6

    # Graph counting is fully exhaustive, but is not an existence assertion.
    edge_set = list(combinations(range(5), 2))
    graph_counts, baseline_shapes, remaining_shapes, removed_shapes = Counter(), set(), set(), set()
    removed_labelled = []
    for mask in range(1 << len(edge_set)):
        edges = [edge for bit, edge in enumerate(edge_set) if mask & (1 << bit)]
        old_reason = v14_filter(edges)
        if old_reason:
            graph_counts[old_reason] += 1
            continue
        shape = canonical_edges(edges)
        baseline_shapes.add(shape)
        if is_k23(edges):
            graph_counts["K2_3"] += 1
            removed_shapes.add(shape)
            removed_labelled.append(edges)
        else:
            graph_counts["remaining"] += 1
            remaining_shapes.add(shape)
    assert dict(graph_counts) == {
        "empty_support": 1, "tree_component": 300, "pure_cycle_component": 37,
        "triangle_with_two_degree_two_vertices": 165, "C4_with_pendant_edge": 60,
        "K2_3": 10, "remaining": 451,
    }
    assert len(baseline_shapes) == 15 and len(remaining_shapes) == 14 and len(removed_shapes) == 1
    assert sum(graph_counts.values()) == 1024

    here = Path(__file__).resolve().parent
    source_name = "k23_obstruction_v15.tex"
    source = next(p for p in (here / source_name, here.parent / "paper" / source_name) if p.is_file())
    out = here / "k23_obstruction_verification_v15.json"
    result = {
        "version": "v15", "passed": True,
        "scope": "A negative two-high branch requires a high edge between its high neighbors; K2,3 high support is impossible.",
        "assumptions": ["standard quintic K5 branch graph", "positive integer local charts",
                        "integer marked-puncture clutching", "nonnegative node counts"],
        "neighbor_high_support_degrees_restricted": False,
        "D_opposition_used_in_new_theorems": False,
        "denominator_or_entry_cutoff": None,
        "q3_degenerate_low_core_classification_used": False,
        "polynomial_identity_count": len(identities), "polynomial_identities": identities,
        "proof_case_exhaustion": [
            {"case": "X=a-c", "reason": "Strictly between (a-1)/2 and a-1, hence not a divisor."},
            {"case": "X=-c, Y=e", "reason": "The integer reverse-entry sum equals E-1, but -1<E<1/2 and E is nonzero."},
            {"case": "X=-c, Y=e-b, e>=2", "reason": "The magnitude b-e is strictly between (b-1)/2 and b-1."},
            {"case": "X=-c, Y=1-b, e=1", "reason": "The low-edge node is 2+rw/H>6, while every node is at most five."},
        ],
        "directed_cycles": arrows, "canonical_assignment_cases": sign_cases,
        "graph_count_update_from_v14_using_only_this_new_theorem": {
            "scope": "Necessary support candidates, not atlas or geometric existence counts; the v14 baseline includes earlier D-dependent exclusions.",
            "labelled_before": 461, "unlabelled_before": 15,
            "labelled_after": 451, "unlabelled_after": 14,
            "newly_excluded_shape_id": "G5_6", "newly_excluded_name": "K2,3",
            "all_1024_support_filter_counts": dict(graph_counts),
            "newly_excluded_canonical_edges": [list(e) for e in next(iter(removed_shapes))],
            "all_ten_excluded_labelled_supports": removed_labelled,
        },
        "limitations": [
            "The inequalities, signed-divisor exhaustiveness, and use of nonnegative nodes are proved in the companion TeX; this script audits identities and finite combinatorics.",
            "No bounded denominator or entry search is performed or used as a proof.",
            "The graph count is the effect of this theorem alone relative to v14; independent v15 theorems may further reduce it.",
            "This is a nonexistence theorem within the specified quintic branch-graph model, not an unrestricted classification of all Lagrangian fibrations on general-type surfaces.",
        ],
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"passed": True, "identities": len(identities), "sign_cases": 8,
                      "remaining_v14_support_shapes": 14, "remaining_labelled_supports": 451,
                      "certificate": str(out)}))


if __name__ == "__main__":
    main()
