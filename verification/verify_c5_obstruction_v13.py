#!/usr/bin/env python3
"""Exact finite bookkeeping for the unbounded C5 obstruction in v13.

This verifies all 32 pairing sign patterns, the two propagation cases, the
canonical ray labels, and the polynomial negative-node certificates.  It does
not search bounded denominators and does not replace the general proof of the
two-high canonical form or the divisor lemmas used in the paper.
"""

from itertools import product
from pathlib import Path
import hashlib
import json


def sign_at(core, high, low, epsilon):
    """Two-high pairing signs in the fixed C5 labels."""
    forward = (core + 1) % 5
    backward = (core - 1) % 5
    low_forward = (core + 2) % 5
    low_backward = (core - 2) % 5
    assert high in (forward, backward)
    assert low in (low_forward, low_backward)
    return epsilon if ((high == forward) == (low == low_forward)) else -epsilon


def canonical_labels(core, a_direction):
    """For epsilon=-1, return the labels (A,B,C,D)."""
    if a_direction == "previous":
        return ((core - 1) % 5, (core + 1) % 5,
                (core + 2) % 5, (core - 2) % 5)
    assert a_direction == "next"
    return ((core + 1) % 5, (core - 1) % 5,
            (core - 2) % 5, (core + 2) % 5)


def main():
    checks = 0
    patterns = []
    for eps in product((-1, 1), repeat=5):
        positive = [i for i in range(5) if eps[i] == 1]
        adjacent = any(eps[i] == eps[(i + 1) % 5] == 1 for i in range(5))
        distance_two = any(eps[i] == eps[(i + 2) % 5] == 1 for i in range(5))
        survives = not adjacent and not distance_two
        assert survives == (len(positive) <= 1)
        checks += 1
        row = {"epsilon": eps, "positive_vertices": positive,
               "adjacent_positive_forbidden_by_clutching": adjacent,
               "distance_two_positive_forbidden_by_nodes": distance_two,
               "survives_sign_tests": survives}
        if survives:
            start = positive[0] if positive else 0
            normalized = tuple(eps[(start + i) % 5] for i in range(5))
            assert normalized[1:] == (-1, -1, -1, -1)
            lam = tuple(-(normalized[i] + normalized[(i + 1) % 5]) // 2
                        for i in range(5))
            assert lam[1:4] == (1, 1, 1)
            checks += 2
            row["normalizing_rotation"] = start
            row["lambda_after_rotation"] = lam
        patterns.append(row)
    assert sum(p["survives_sign_tests"] for p in patterns) == 6
    checks += 1

    propagation = []
    for a2, a3 in product(("previous", "next"), repeat=2):
        edge23_full_ends = int(a2 == "next") + int(a3 == "previous")
        compatible = edge23_full_ends == 1
        assert compatible == (a2 == a3)
        checks += 1
        propagation.append({"core2_A": a2, "core3_A": a3,
                            "edge23_full_end_count": edge23_full_ends,
                            "compatible": compatible})

    cases = []
    for direction, cores, expected_table, puncture, q_index in (
        ("previous", (2, 3, 4),
         ((1, 3, 4, 0), (2, 4, 0, 1), (3, 0, 1, 2)), 2, 1),
        ("next", (1, 2, 3),
         ((2, 0, 4, 3), (3, 1, 0, 4), (4, 2, 1, 0)), 3, 3),
    ):
        table = tuple(canonical_labels(i, direction) for i in cores)
        assert table == expected_table
        checks += 1
        for core, (a, b, c, d) in zip(cores, table):
            assert set((a, b, c, d)) == set(range(5)) - {core}
            assert sign_at(core, a, c, -1) == 1
            assert sign_at(core, a, d, -1) == -1
            assert sign_at(core, b, c, -1) == -1
            assert sign_at(core, b, d, -1) == 1
            checks += 5

        if direction == "previous":
            # The full endpoint of edge34 forces core4 A=3,C=1,D=2.
            assert table[-1][2:] == (1, 2)
            # The unit entry at core1 is high2 -> low4.
            assert sign_at(1, 2, 4, -1) == 1
            zero_entry = {"core": 4, "row": 1, "column": 2}
            unit_entry = {"core": 1, "row": 2, "column": 4}
            reverse_entry = {"core": 1, "row": 4, "column": 2}
        else:
            assert table[0][2:] == (4, 3)
            assert sign_at(4, 3, 1, -1) == 1
            zero_entry = {"core": 1, "row": 4, "column": 3}
            unit_entry = {"core": 4, "row": 3, "column": 1}
            reverse_entry = {"core": 4, "row": 1, "column": 3}
        checks += 2

        # Polynomial pairs (constant, q coefficient), exact without sampling.
        zero = (0, 0)
        reverse = (-1, 1)  # q-1
        node = (1 - zero[0] - reverse[0], -zero[1] - reverse[1])
        assert node == (2, -1)
        # q=3+2k, k>=0, transforms n to -1-2k, strictly negative.
        node_in_k = (node[0] + 3 * node[1], 2 * node[1])
        assert node_in_k == (-1, -2)
        assert node_in_k[0] < 0 and node_in_k[1] <= 0
        checks += 3
        cases.append({"direction": direction, "cores": cores,
                      "canonical_table_ABCD": table,
                      "unit_entry": unit_entry, "reverse_entry": reverse_entry,
                      "zero_entry": zero_entry, "contradiction_edge": [1, 4],
                      "puncture": puncture, "denominator_index": q_index,
                      "node_polynomial_in_q": node,
                      "negative_polynomial_in_k": node_in_k})

    here = Path(__file__).resolve().parent
    possible_sources = (here / "quintic_c5_obstruction_v13.tex",
                        here.parent / "papers/sections/paper" / "quintic_c5_obstruction_v13.tex")
    source = next((p for p in possible_sources if p.exists()), None)
    result = {
        "version": "v13", "status": "passed", "exact_assertion_count": checks,
        "pairing_patterns_checked": 32, "patterns_surviving_prior_sign_lemmas": 6,
        "propagation_assignments_checked": 4, "negative_node_certificates": 2,
        "denominator_bound": None, "D_opposition_used": False,
        "scope": "Finite combinatorial and polynomial certificate for the written general C5 proof; not a bounded-denominator search.",
        "patterns": patterns, "propagation": propagation, "cases": cases,
        "proof_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest() if source else None,
    }
    target = here / "c5_obstruction_verification_v13.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "version", "status", "exact_assertion_count", "pairing_patterns_checked",
        "patterns_surviving_prior_sign_lemmas", "negative_node_certificates",
        "D_opposition_used")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
