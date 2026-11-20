#!/usr/bin/env python3
"""Finite, standard-library verification of the quintic graph classification.

This enumerates abstract leaf-labelled Reeb graph data, not embedded marked
isotopy classes or measured/symplectic foliations. The general induced-block
and girth obstructions are proved in quintic_links.tex, not by this program.
"""

from collections import Counter
from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path


def splits(labels):
    """The three unordered 2+2 splits, with canonical ordering of their parts."""
    labels = tuple(sorted(labels))
    answer = set()
    for pair in combinations(labels, 2):
        complement = tuple(x for x in labels if x not in pair)
        answer.add(tuple(sorted((tuple(pair), complement))))
    return tuple(sorted(answer))


def endpoint(split, label):
    return 0 if label in split[0] else 1


def vertices(edges):
    return sorted({v for edge in edges for v in edge})


def adjacency(edges):
    vs = vertices(edges)
    adj = {v: set() for v in vs}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def is_simple(edges):
    canonical = [tuple(sorted(edge)) for edge in edges]
    return (all(a != b for a, b in edges)
            and len(canonical) == len(set(canonical)))


def is_connected(edges):
    adj = adjacency(edges)
    if not adj:
        return False
    reached = {next(iter(adj))}
    todo = list(reached)
    while todo:
        v = todo.pop()
        for w in adj[v] - reached:
            reached.add(w)
            todo.append(w)
    return len(reached) == len(adj)


def is_bipartite(edges):
    adj = adjacency(edges)
    color = {}
    for first in adj:
        if first in color:
            continue
        color[first] = 0
        todo = [first]
        while todo:
            v = todo.pop()
            for w in adj[v]:
                if w not in color:
                    color[w] = 1 - color[v]
                    todo.append(w)
                elif color[w] == color[v]:
                    return False
    return True


def classify(edges):
    degrees = Counter(v for edge in edges for v in edge)
    assert is_connected(edges)
    assert all(d == 3 for d in degrees.values()), degrees
    if not is_simple(edges):
        return "cubic_multigraph"
    size = len(degrees)
    if size == 4:
        return "K4"
    if size == 6 and is_bipartite(edges):
        return "K3,3"
    if size == 6:
        # A connected simple cubic graph on six vertices has one of these two
        # types. Check the prism by a direct isomorphism, independently of this
        # classification fact.
        prism = {(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5),
                 (0, 3), (1, 4), (2, 5)}
        vs = vertices(edges)
        for ordering in permutations(vs):
            numbering = {v: i for i, v in enumerate(ordering)}
            relabelled = {tuple(sorted((numbering[a], numbering[b])))
                          for a, b in edges}
            if relabelled == prism:
                return "triangular_prism"
        raise AssertionError("Unexpected simple cubic six-vertex graph")
    return "other"


def planar_core(split_first, split_second, labels):
    edges = [("u0", "u1"), ("v0", "v1")]
    edges += [(f"u{endpoint(split_first, p)}",
               f"v{endpoint(split_second, p)}") for p in labels]
    return edges


def elliptic_quadric_core(split, cycle):
    edges = [("u0", "u1")]
    edges += [(f"c{cycle[i]}", f"c{cycle[(i + 1) % 4]}")
              for i in range(4)]
    edges += [(f"u{endpoint(split, p)}", f"c{p}") for p in cycle]
    return edges


def enumerate_122():
    labels = (0, 1, 2, 3)
    qs = splits(labels)
    cycles = tuple((0,) + p for p in permutations((1, 2, 3)) if p[0] < p[-1])
    assert len(qs) == len(cycles) == 3
    records = []
    by_number = Counter()
    pairs_seen = set()
    for ab, ac, cycle in product(qs, qs, cycles):
        tau = tuple(sorted((tuple(sorted((cycle[0], cycle[2]))),
                            tuple(sorted((cycle[1], cycle[3]))))))
        types = [classify(planar_core(ab, ac, labels)),
                 classify(elliptic_quadric_core(ab, cycle)),
                 classify(elliptic_quadric_core(ac, cycle))]
        good = [types[0] == "K4", types[1] == "K3,3", types[2] == "K3,3"]
        assert good == [ab != ac, ab == tau, ac == tau]
        assert not all(good)
        by_number[sum(good)] += 1
        if sum(good) == 2:
            pairs_seen.add(tuple(i for i, value in enumerate(good) if value))
        records.append({"sigma_AB": ab, "sigma_AC": ac, "cycle": cycle,
                        "bipartition_tau": tau, "core_types": types,
                        "matroidal_core_count": sum(good)})
    assert by_number == Counter({2: 15, 1: 6, 0: 6})
    assert pairs_seen == {(0, 1), (0, 2), (1, 2)}
    return {
        "scope": "All 27 two-quartet plus labelled elliptic C4 systems. "
                 "Other elliptic graph types cannot give a matroidal quadric "
                 "by the induced-block proof.",
        "systems": len(records),
        "by_matroidal_core_count": dict(sorted(by_number.items())),
        "simultaneous_all": 0,
        "any_prescribed_pair_realized": True,
        "records": records,
    }


def plane_1112(split, first, second):
    edges = [("x", "y"), ("u0", "u1")]
    edges += [("x", f"u{endpoint(split, p)}") for p in first]
    edges += [("y", f"u{endpoint(split, p)}") for p in second]
    return edges


def quadric_1112(sa, sb, sc, pab, pac, pbc):
    edges = [("a0", "a1"), ("b0", "b1"), ("c0", "c1")]
    edges += [(f"a{endpoint(sa, p)}", f"b{endpoint(sb, p)}") for p in pab]
    edges += [(f"a{endpoint(sa, p)}", f"c{endpoint(sc, p)}") for p in pac]
    edges += [(f"b{endpoint(sb, p)}", f"c{endpoint(sc, p)}") for p in pbc]
    return edges


def crossed_bit(split, first, second):
    part = split[endpoint(split, first[0])]
    if first[1] in part:
        return None
    return 0 if second[0] in part else 1


def enumerate_1112():
    pab, pac, pbc = (0, 1), (2, 3), (4, 5)
    choices = [splits(pab + pac), splits(pab + pbc), splits(pac + pbc)]
    records = []
    by_number = Counter()
    solutions = []
    for sa, sb, sc in product(*choices):
        bits = [crossed_bit(sa, pab, pac), crossed_bit(sb, pab, pbc),
                crossed_bit(sc, pac, pbc)]
        types = [classify(plane_1112(sa, pab, pac)),
                 classify(plane_1112(sb, pab, pbc)),
                 classify(plane_1112(sc, pac, pbc)),
                 classify(quadric_1112(sa, sb, sc, pab, pac, pbc))]
        good = [value == "K4" for value in types[:3]] + [types[3] == "K3,3"]
        assert good[:3] == [bit is not None for bit in bits]
        odd = all(bit is not None for bit in bits) and sum(bits) % 2 == 1
        assert good[3] == odd
        by_number[sum(good)] += 1
        if all(good):
            solutions.append(bits)
        records.append({"sigma_A": sa, "sigma_B": sb, "sigma_C": sc,
                        "crossed_bits": bits, "core_types": types,
                        "matroidal_core_count": sum(good)})
    assert by_number == Counter({4: 4, 3: 4, 2: 12, 1: 6, 0: 1})
    assert sorted(solutions) == [[0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
    # Independent check of the orbit under swapping a pair of triple labels.
    flips = ((1, 1, 0), (1, 0, 1), (0, 1, 1))
    orbit = {tuple(solutions[0])}
    todo = list(orbit)
    while todo:
        old = todo.pop()
        for flip in flips:
            new = tuple(a ^ b for a, b in zip(old, flip))
            if new not in orbit:
                orbit.add(new)
                todo.append(new)
    assert orbit == {tuple(s) for s in solutions}
    return {"scope": "All 27 leaf-labelled quartet systems; not embedded "
                     "marked isotopy or symplectic-conjugacy classes.",
            "systems": len(records),
            "by_matroidal_core_count": dict(sorted(by_number.items())),
            "simultaneous_all": 4,
            "odd_parity_solutions": solutions,
            "orbits_under_pair_label_swaps": 1,
            "records": records}


def enumerate_113_triangle_identifications():
    base = [(f"a{i}", f"a{(i + 1) % 3}") for i in range(3)]
    base += [(f"b{i}", f"b{(i + 1) % 3}") for i in range(3)]
    records = []
    for identification in permutations(range(3)):
        edges = base + [(f"a{i}", f"b{identification[i]}") for i in range(3)]
        graph_type = classify(edges)
        assert graph_type == "triangular_prism"
        records.append({"triangle_vertex_identification": identification,
                        "cubic_core_type": graph_type})
    return {"scope": "The six matchings between two triangles with their "
                     "vertex coordinates fixed; these are presentations "
                     "of one abstract leaf-labelled triangle system, not "
                     "six marked-isotopy classes. The obstruction for "
                     "arbitrary genus-one graphs is the girth proof.",
            "presentations": 6,
            "all_cubic_core_types": "triangular_prism",
            "records": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("quintic_links_v8_verification.json"))
    args = parser.parse_args()
    result = {
        "version": 8,
        "verification_kind": "Exact finite graph enumeration using Python standard library",
        "distinction": "Counts concern finite leaf-labelled graph/split data only. "
                       "They do not count embedded marked isotopy classes, measured "
                       "foliations, action-compatible atlases or symplectic fillings.",
        "partition_113": enumerate_113_triangle_identifications(),
        "partition_122": enumerate_122(),
        "partition_1112": enumerate_1112(),
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    summary = {key: {field: value for field, value in data.items() if field != "records"}
               for key, data in result.items() if key.startswith("partition_")}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
