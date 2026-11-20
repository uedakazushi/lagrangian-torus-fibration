#!/usr/bin/env python3
"""Exhaustive support-graph audit after the v15 diamond and K2,3 theorems.

This enumerates all 1024 simple labelled subgraphs of K5, not bounded integer
chart data. It preserves the established v13/v14 shape identifiers and does
not interpret a surviving support as an existing atlas or fibration.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
DEP = HERE / "verify_k23_obstruction_v15.py"
spec = importlib.util.spec_from_file_location("support_v15_k23", DEP)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def is_diamond(edges):
    adj = base.adjacency(edges)
    return len(edges) == 5 and sorted(map(len, adj.values())) == [0, 2, 2, 3, 3]


def triangles(edges):
    es = {tuple(sorted(e)) for e in edges}
    return [list(t) for t in combinations(range(5), 3)
            if all(tuple(e) in es for e in combinations(t, 2))]


def active_connected(adj):
    active = {v for v in range(5) if adj[v]}
    if not active:
        return False
    component, stack = {min(active)}, [min(active)]
    while stack:
        v = stack.pop()
        for u in adj[v] - component:
            component.add(u)
            stack.append(u)
    return component == active


def main():
    previous_name = "c4_pendant_verification_v14.json"
    previous = next(p for p in (
        HERE / previous_name,
        HERE.parents[1] / "deliverables/general_type_surface_fibration_v14/verification" / previous_name,
    ) if p.is_file())
    old_agenda = json.loads(previous.read_text())["remaining_support_agenda"]
    old_shapes = {base.canonical_edges(s["canonical_edges"]): s for s in old_agenda["shapes"]}
    assert len(old_shapes) == 15

    edges_all = list(combinations(range(5), 2))
    counts, shape_counts = Counter(), Counter()
    removed_counts, inherited_shape_counts = Counter(), Counter()
    remaining_labelled = []
    triangle_free_before, triangle_free_after = 0, 0
    for mask in range(1 << len(edges_all)):
        edges = [e for bit, e in enumerate(edges_all) if mask & (1 << bit)]
        reason = base.v14_filter(edges)
        if reason:
            counts[reason] += 1
            continue
        canonical = base.canonical_edges(edges)
        assert canonical in old_shapes
        inherited_shape_counts[canonical] += 1
        triangle_free_before += not bool(triangles(edges))
        if is_diamond(edges):
            counts["diamond"] += 1
            removed_counts["G4_2"] += 1
            assert old_shapes[canonical]["shape_id"] == "G4_2"
        elif base.is_k23(edges):
            counts["K2_3"] += 1
            removed_counts["G5_6"] += 1
            assert old_shapes[canonical]["shape_id"] == "G5_6"
        else:
            adj = base.adjacency(edges)
            active = [v for v in range(5) if adj[v]]
            assert active_connected(adj) and len(active) in (4, 5)
            assert len(edges) >= 5 and max(map(len, adj.values())) >= 3
            triangle_free_after += not bool(triangles(edges))
            if len(active) == 4:
                assert len(edges) == 6 and all(len(adj[v]) == 3 for v in active)
            if len(edges) - len(active) + 1 == 1:
                assert old_shapes[canonical]["shape_id"] == "G5_3"
            counts["remaining"] += 1
            shape_counts[canonical] += 1
            remaining_labelled.append({"edges": edges, "shape_id": old_shapes[canonical]["shape_id"]})
    expected_counts = {
        "empty_support": 1, "tree_component": 300, "pure_cycle_component": 37,
        "triangle_with_two_degree_two_vertices": 165, "C4_with_pendant_edge": 60,
        "diamond": 30, "K2_3": 10, "remaining": 421,
    }
    assert dict(counts) == expected_counts and sum(counts.values()) == 1024
    assert len(shape_counts) == 13 and sum(shape_counts.values()) == 421
    assert dict(removed_counts) == {"G4_2": 30, "G5_6": 10}
    assert triangle_free_before == 10 and triangle_free_after == 0

    shapes = []
    for canonical, old in old_shapes.items():
        assert inherited_shape_counts[canonical] == old["labelled_K5_count"]
        if canonical not in shape_counts:
            continue
        es = [tuple(e) for e in old["canonical_edges"]]
        adj = base.adjacency(es)
        automorphisms = sum(
            set(tuple(sorted((perm[i], perm[j]))) for i, j in es) == set(es)
            for perm in base.ALL_PERMUTATIONS
        )
        assert automorphisms == old["automorphism_order"]
        assert 120 // automorphisms == shape_counts[canonical] == old["labelled_K5_count"]
        forced_positive = []
        for i in range(5):
            if len(adj[i]) == 2:
                j, k = sorted(adj[i])
                if k not in adj[j]:
                    forced_positive.append(i)
        shapes.append({**old, "triangles": triangles(es),
                       "two_high_vertices_forced_positive_by_low_neighbor_edge": forced_positive})
    assert [s["shape_id"] for s in shapes if s["vertices"] == 4] == ["G4_3"]
    assert [s["shape_id"] for s in shapes if s["cycle_rank"] == 1] == ["G5_3"]
    assert [(s["shape_id"], s["two_high_vertices_forced_positive_by_low_neighbor_edge"])
            for s in shapes if s["two_high_vertices_forced_positive_by_low_neighbor_edge"]] == [
                ("G5_5", [3, 4]), ("G5_10", [4])]
    assert len(shapes) == 13

    source_hashes = {}
    for name, folders in {
        "k23_obstruction_v15.tex": (HERE, HERE.parent / "paper"),
        "diamond_obstruction_v15.tex": (HERE.parent / "diamond", HERE.parent / "paper", HERE),
        "quintic_support_frontier_v15.tex": (HERE, HERE.parent / "paper"),
        "notes_support_agenda_v15.tex": (HERE, HERE.parent / "notes"),
    }.items():
        candidates = [folder / name for folder in folders]
        source = next((p for p in candidates if p.is_file()), None)
        assert source is not None, name
        source_hashes[name] = hashlib.sha256(source.read_bytes()).hexdigest()

    result = {
        "version": "v15", "passed": True,
        "scope": "Complete finite graph audit of necessary support conditions; surviving graphs are not asserted to admit integer charts or fibrations.",
        "graph_hypotheses": ["positive integer local charts", "integer marked clutching",
                             "opposing D cancellation", "nonnegative nodes", "standard quintic K5 branch graph"],
        "denominator_or_entry_cutoff": None,
        "labelled_K5_graphs_checked": 1024,
        "labelled_nonempty_supports_remaining": 421,
        "unlabelled_shapes_remaining": 13,
        "four_vertex_shapes": 1, "five_vertex_shapes": 12,
        "canonical_rule": old_agenda["canonical_rule"],
        "shape_identifiers_preserved_from_v13_v14": True,
        "excluded_counts_in_filter_order": {k: v for k, v in expected_counts.items() if k != "remaining"},
        "intermediate_candidate_counts": [686, 521, 461, 431, 421],
        "newly_excluded_shapes": [
            {**s, "v15_exclusion": "diamond" if s["shape_id"] == "G4_2" else "K2_3"}
            for s in old_agenda["shapes"] if s["shape_id"] in ("G4_2", "G5_6")
        ],
        "structural_corollaries": {
            "every_nonempty_support_contains_a_triangle": True,
            "triangle_free_support_forces_all_denominators_one": True,
            "only_four_active_vertex_candidate": "G4_3 = K4",
            "only_unicyclic_candidate": "G5_3",
            "triangle_free_nonempty_candidates_after_v14": 10,
            "triangle_free_nonempty_candidates_after_v15": 0,
        },
        "shapes": shapes,
        "all_421_remaining_labelled_supports": remaining_labelled,
        "research_priorities": [
            {"shape_id": "G5_3", "status": "Open; the central degree-two core must have the crossed placement and lie on the positive branch S>r, rT>(r+1)S, with r<=4 or z=1.",
             "negative_branch_exclusion": "w>=5 is excluded by a general proof; w<=4 is reduced by proof to all seven local models and a complete reconstruction of 485 leaf pairs.",
             "next": "Resolve the remaining positive branches r<=4 or z=1 using both leaf low rows, the degree-two core and the marked center conditions."},
            {"shape_id": "G4_3", "status": "Open; the only four-active-vertex support candidate.",
             "next": "Apply common-low-puncture signed-divisor alternatives and the all-low core balance to four degree-three cores."},
            {"shape_id": "G5_5", "status": "Open; degree-two vertices 3 and 4 must lie on the positive branch.",
             "next": "Combine their adjacent low-ray node conditions with the remaining triangular two-high core."},
        ],
        "limitations": [
            "The exhaustive finite graph audit supplements the analytic obstructions, and does not prove the obstructions by itself.",
            "G5_3 is retained: reducing its central core to a crossed positive branch with r<=4 or z=1 does not exclude the whole support.",
            "The agenda is not a claimed classification of all general-type surfaces or all Lagrangian fibrations.",
        ],
        "previous_certificate": {"file": previous.name, "sha256": hashlib.sha256(previous.read_bytes()).hexdigest()},
        "source_sha256": source_hashes,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency": {"file": DEP.name, "sha256": hashlib.sha256(DEP.read_bytes()).hexdigest()},
    }
    out = HERE / "support_agenda_verification_v15.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"passed": True, "graphs": 1024, "remaining_shapes": 13,
                      "remaining_labelled": 421, "triangle_free_remaining": 0,
                      "certificate": str(out)}))


if __name__ == "__main__":
    main()
