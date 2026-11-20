#!/usr/bin/env python3
"""Exact finite certificates for two lines plus a conic, version 8.

Checks only the integer fan/action data and all 36 specified area recipes.
Relative Moser, actual normal framing, and local cone homeomorphism are
proved in mixed_plane_periods.tex rather than certified by this program.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from math import gcd
from pathlib import Path
import json


CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def add(*vectors):
    return tuple(sum(c) for c in zip(*vectors))


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def verify():
    vertices = ("X", "Y", "U", "V")
    rays = {"X": (1, 0, 0), "Y": (0, 1, 0), "U": (0, 0, 1),
            "V": (-1, -1, -1)}
    check(add(*(rays[v] for v in vertices)) == (0, 0, 0), "K4 balancing")
    for v, w in combinations(vertices, 2):
        minors = [rays[v][i] * rays[w][j] - rays[v][j] * rays[w][i]
                  for i, j in combinations(range(3), 2)]
        check(gcd(*minors) == 1, "saturated K4 face lattice")

    weights = {"X": (1, 0, 0), "Y": (0, 1, 0),
               "U": (0, 0, 1), "V": (0, 0, 1)}
    component_weight = {"X": (1, 0, 0), "Y": (0, 1, 0), "C": (0, 0, 1)}
    ports = {"X": (("X", "Y"), ("X", "U"), ("X", "V")),
             "Y": (("Y", "X"), ("Y", "U"), ("Y", "V")),
             "C": (("U", "X"), ("U", "Y"), ("V", "X"), ("V", "Y"))}
    crossing_edges = (("X", "Y"), ("X", "U"), ("X", "V"),
                      ("Y", "U"), ("Y", "V"))
    records = []
    histogram = Counter()
    for selected_x, selected_y, omitted_c in product(ports["X"], ports["Y"], ports["C"]):
        selected = {selected_x, selected_y} | (set(ports["C"]) - {omitted_c})
        check(len(selected) == 5, "five enlarged basins")
        for component, its_ports in ports.items():
            targets = []
            for v, w in its_ports:
                target = weights[w]
                if (v, w) in selected:
                    target = add(target, component_weight[component])
                check(min(target) >= 0 and max(target) > 0, "positive target polynomial")
                targets.append(target)
            total = add(*targets)
            if component == "C":
                check(add(total, (0, 0, 1)) == (2, 2, 4),
                      "conic area equals basin areas plus one annulus weight")
            else:
                check(total == (1, 1, 2), "line area budget")

        matrices = []
        determinants = []
        for v, w in crossing_edges:
            eps_v = int((v, w) in selected)
            eps_w = int((w, v) in selected)
            matrix = [[-1, eps_w], [eps_v, -1]]
            det = determinant(matrix)
            check(det == 1 - eps_v * eps_w, "crossing determinant")
            for column in zip(*matrix):
                check(gcd(*column) == 1, "primitive crossing endpoint")
            matrices.append(matrix)
            determinants.append(det)
        m = sum(("U", w) in selected for w in ("X", "Y"))
        n = sum(("V", w) in selected for w in ("X", "Y"))
        check(m + n == 3, "three enlarged conic basins")
        check(m in (1, 2), "conic saddle split")
        check(4 - n == m + 1, "Euler-four actual endpoint relation")
        internal_matrix = [[-1, -1], [m, m + 1]]
        check(determinant(internal_matrix) == -1, "internal unimodularity")
        for column in zip(*internal_matrix):
            check(gcd(*column) == 1, "primitive internal endpoint")
        admissible = all(d == 1 for d in determinants)
        bad = determinants.count(0)
        histogram[bad] += 1
        if admissible:
            check(all(int((v, w) in selected) + int((w, v) in selected) == 1
                      for v, w in crossing_edges), "each crossing chosen exactly once")
        records.append({
            "selected_half_edges": [list(edge) for edge in sorted(selected)],
            "admissible": admissible,
            "crossing_determinants": determinants,
            "internal_matrix": internal_matrix,
            "internal_determinant": -1,
        })
    admissible_records = [record for record in records if record["admissible"]]
    check(len(records) == 36, "complete enumeration")
    check(len(admissible_records) == 4, "four admissible marked recipes")
    principal = sorted([("X", "Y"), ("Y", "U"), ("U", "X"),
                        ("V", "X"), ("V", "Y")])
    check(any(record["selected_half_edges"] == [list(edge) for edge in principal]
              for record in admissible_records), "principal orientation occurs")
    return {
        "fan_rays": rays,
        "saturated_fan_cones": 6,
        "recipes_total": len(records),
        "admissible_recipes": len(admissible_records),
        "bad_crossing_count_histogram": dict(sorted(histogram.items())),
        "admissible_records": admissible_records,
        "records": records,
        "all_positive_weights": "area identities verified coefficientwise in u_X,u_Y,u_C",
    }


def main():
    source = Path(__file__).resolve()
    result = {"version": 8, "code_sha256": sha256(source.read_bytes()).hexdigest(),
              "data": verify()}
    result["checks"] = CHECKS
    result["passed"] = True
    result["proof_boundary"] = [
        "does not replace relative Moser or normal Euler-four framing",
        "local cone homeomorphism is proved in the text",
        "all cores are realized individually; shared-curve compatibility is not asserted",
        "does not impose common-circle ambient-linear extension",
    ]
    output = source.with_name("mixed_plane_periods_verification_v8.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"mixed plane periods v8: {CHECKS} exact checks passed; "
          f"4/36 admissible recipes; result={output.name}")


if __name__ == "__main__":
    main()
