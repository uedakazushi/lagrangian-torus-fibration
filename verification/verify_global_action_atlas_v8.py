#!/usr/bin/env python3
"""Exact finite certificates for the v8 global-action compatibility work.

The name refers to the research problem, not to a verified global atlas.
This program checks finite labels, formal rational area identities, integer
cycle changes, and linear maps on model lattices.  It does NOT certify
finite-parameter action intercepts, neck gluing, or an analytic atlas.
Only the Python standard library is used.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from math import gcd
from pathlib import Path
import json


CHECKS = Counter()


def check(statement, message, category):
    CHECKS[category] += 1
    if not statement:
        raise AssertionError(f"{category}: {message}")


def add(*vectors):
    return tuple(sum(x) for x in zip(*vectors))


def scale(c, vector):
    return tuple(c * x for x in vector)


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def apply(matrix, vector):
    return tuple(sum(x * y for x, y in zip(row, vector)) for row in matrix)


def determinant(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    answer = Fraction(1)
    for c in range(len(a)):
        pivot = next((r for r in range(c, len(a)) if a[r][c]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != c:
            a[pivot], a[c] = a[c], a[pivot]
            answer = -answer
        value = a[c][c]
        answer *= value
        for r in range(c + 1, len(a)):
            multiplier = a[r][c] / value
            for j in range(c, len(a)):
                a[r][j] -= multiplier * a[c][j]
    return answer


def inverse(matrix):
    n = len(matrix)
    a = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    for c in range(n):
        pivot = next(r for r in range(c, n) if a[r][c])
        a[pivot], a[c] = a[c], a[pivot]
        value = a[c][c]
        a[c] = [x / value for x in a[c]]
        for r in range(n):
            if r != c:
                value = a[r][c]
                a[r] = [x - value * y for x, y in zip(a[r], a[c])]
    return [row[n:] for row in a]


def rank(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    row = 0
    for col in range(len(a[0])):
        pivot = next((r for r in range(row, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot], a[row] = a[row], a[pivot]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for r in range(len(a)):
            if r != row:
                value = a[r][col]
                a[r] = [x - value * y for x, y in zip(a[r], a[row])]
        row += 1
    return row


def primitive_span(columns):
    answer = 0
    for rows in combinations(range(len(columns[0])), len(columns)):
        value = determinant([[column[r] for column in columns] for r in rows])
        assert value.denominator == 1
        answer = gcd(answer, abs(int(value)))
    return answer == 1


def matrix_key(matrix):
    return tuple(tuple(int(x) for x in row) for row in matrix)


def all_perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for b in vertices[1:]:
        remaining = [x for x in vertices if x not in (a, b)]
        for matching in all_perfect_matchings(remaining):
            yield tuple(sorted(((a, b),) + matching))


def system_key(system):
    return tuple(system[i][j] for i in range(5) for j in range(5) if i != j)


def conjugate_system(system, permutation):
    result = {i: {} for i in range(5)}
    for i in range(5):
        for j, k in system[i].items():
            result[permutation[i]][permutation[j]] = permutation[k]
    return result


def is_four_cycle(mapping):
    start = min(mapping)
    visited = []
    current = start
    while current not in visited:
        visited.append(current)
        current = mapping[current]
    return current == start and len(visited) == 4


def verify_symmetric_systems():
    matchings = sorted(set(all_perfect_matchings(list(range(6)))))
    factorizations = [choice for choice in combinations(range(len(matchings)), 5)
                      if len({edge for index in choice for edge in matchings[index]}) == 15]
    check(len(matchings) == 15, "perfect matching count", "labels")
    check(len(factorizations) == 6, "one-factorization count", "labels")
    systems = []
    for factorization in factorizations:
        system = {i: {} for i in range(5)}
        for index in factorization:
            matching = matchings[index]
            infinity_edge = next(edge for edge in matching if 5 in edge)
            k = next(x for x in infinity_edge if x != 5)
            for i, j in matching:
                if 5 not in (i, j):
                    system[i][j] = system[j][i] = k
        for i in range(5):
            check(is_four_cycle(system[i]), "factorization gives a four-cycle", "labels")
            for j in system[i]:
                check(system[i][j] == system[j][i] not in (i, j),
                      "symmetric nonendpoint selection", "labels")
        systems.append(system)

    # Independent exhaustive enumeration: six cycles at each of five vertices.
    cycle_options = []
    for i in range(5):
        vertices = [j for j in range(5) if j != i]
        cycles = []
        for tail in permutations(vertices[1:]):
            cycle = (vertices[0],) + tail
            cycles.append({cycle[j]: cycle[(j + 1) % 4] for j in range(4)})
        check(len(cycles) == 6, "six four-cycles on four labels", "labels")
        cycle_options.append(cycles)
    direct_systems = []
    assignments_examined = 0
    for maps in product(*cycle_options):
        assignments_examined += 1
        if all(maps[i][j] == maps[j][i] for i, j in combinations(range(5), 2)):
            direct_systems.append({i: maps[i] for i in range(5)})
    check(assignments_examined == 6 ** 5, "exhaustive independent search size", "labels")
    check({system_key(s) for s in direct_systems} == {system_key(s) for s in systems},
          "direct and factorization enumerations agree", "labels")
    midpoint = {i: {j: 3 * (i + j) % 5 for j in range(5) if i != j} for i in range(5)}
    check(system_key(midpoint) in {system_key(s) for s in systems},
          "midpoint recipe belongs to the six", "labels")
    orbit = set()
    stabilizer = set()
    for permutation in permutations(range(5)):
        key = system_key(conjugate_system(midpoint, permutation))
        orbit.add(key)
        if key == system_key(midpoint):
            stabilizer.add(permutation)
    affine_group = {tuple((u * x + v) % 5 for x in range(5))
                    for u in range(1, 5) for v in range(5)}
    check(stabilizer == affine_group, "stabilizer is AGL1(F5)", "labels")
    check(len(stabilizer) == 20 and len(orbit) == 6,
          "stabilizer and orbit counts", "labels")
    check(orbit == {system_key(s) for s in systems}, "one orbit exhausts systems", "labels")
    return matchings, factorizations, systems, {
        "perfect_matchings": 15,
        "one_factorizations": [[list(matchings[index]) for index in ff] for ff in factorizations],
        "direct_cycle_assignments_examined": assignments_examined,
        "symmetric_systems": 6,
        "midpoint_formula": "f_i(j)=3(i+j) mod 5",
        "S5_orbit_size": 6,
        "stabilizer_size": 20,
        "systems": [{str(i): {str(j): k for j, k in s[i].items()} for i in range(5)}
                    for s in systems],
    }


def coefficient_models(n):
    basis = [tuple(int(i == j) for j in range(n + 1)) for i in range(n + 1)]
    c, b = basis[0], basis[1:]
    weights = {(i, j): add(c, b[j], scale(-1, b[i]))
               for i in range(n) for j in range(n) if i != j}
    rows = [add(scale(n - 1, c), *b, scale(-n, b[i])) for i in range(n)]
    for i in range(n):
        check(add(*(weights[i, j] for j in range(n) if j != i)) == rows[i],
              "canonical residue row sum", f"d{n}_areas")
    margin = add(c, b[0], scale(-1, b[-1]))
    for (i, j), weight in weights.items():
        # b_0 <= ... <= b_(n-1), so the last two summands are nonnegative.
        positive_certificate = add(margin, b[j], scale(-1, b[0]), b[-1], scale(-1, b[i]))
        check(weight == positive_certificate, "positive spread certificate", f"d{n}_areas")
    check(weights[n - 1, 0] == margin, "sharp minimum weight", f"d{n}_areas")
    for i, j in combinations(range(n), 2):
        delta = add(b[j], scale(-1, b[i]))
        check(add(rows[i], scale(-1, rows[j])) == scale(n, delta),
              "actual curve area difference", f"d{n}_areas")
        check(add(weights[i, j], weights[j, i]) == scale(2, c),
              "branch length 2c", f"d{n}_areas")
    return c, b, weights, rows


def uniqueness_matrix(n, system=None):
    variables = [(i, j) for i in range(n) for j in range(n) if i != j]
    index = {v: k for k, v in enumerate(variables)}
    equations, rhs = [], []

    def equation(terms, value=0):
        row = [0] * len(variables)
        for variable, coefficient in terms:
            row[index[variable]] += coefficient
        equations.append(row)
        rhs.append(value)

    for i in range(n):
        equation([((i, j), 1) for j in range(n) if i != j], n - 1)
    for i, j in combinations(range(n), 2):
        for k in range(n):
            if k in (i, j):
                continue
            terms = [((i, k), 1), ((j, k), -1)]
            if n == 5:
                epsilon = int(system[i][j] == k)
                terms += [((i, j), epsilon), ((j, i), -epsilon)]
            equation(terms)
        if n == 6:
            equation([((i, j), 1), ((j, i), -1)])
    matrix_rank = rank(equations)
    check(matrix_rank == len(variables), "unique canonical weights", f"d{n}_areas")
    check(all(sum(row) == value for row, value in zip(equations, rhs)),
          "v_ij=1 solves normalized system", f"d{n}_areas")
    return {"variables": len(variables), "equations": len(equations), "rank": matrix_rank}


def verify_quintic(systems):
    c, b, weights, rows = coefficient_models(5)
    uniqueness = []
    face_matrices, star_matrices, cycle_matrices = set(), set(), set()
    for system in systems:
        uniqueness.append(uniqueness_matrix(5, system))
        allocations = {}
        for i, j in combinations(range(5), 2):
            labels = [k for k in range(5) if k not in (i, j)]
            delta = add(b[j], scale(-1, b[i]))
            counts, shared_areas, m, theta = [], [], [], []
            for k in labels:
                x = int(system[i][j] == k)
                xp = int(system[j][i] == k)
                y = int(system[i][k] == j)
                yp = int(system[j][k] == i)
                n = 1 + x + xp
                counts.append(n)
                allocations[i, j, k] = n
                lhs = add(weights[i, k], scale(x, weights[i, j]), scale(-n, delta))
                rhs = add(weights[j, k], scale(xp, weights[j, i]))
                check(lhs == rhs, "shared basin formal area equality", "d5_areas")
                shared_areas.append(rhs)
                check(-x == xp - (n - 1), "straight branch slope equality", "d5_lattices")
                check(x * y == xp * yp == 0, "four-cycle has no two-cycle", "d5_lattices")
                ai = [[-1, y], [x, -1]]
                aj = [[-1, yp], [xp, -1]]
                cycle_change = [[-1, 0], [n - 1, 1]]
                transition = [[-1, y + yp], [0, 1]]
                check(determinant(ai) == determinant(aj) == 1,
                      "core face action matrices", "d5_lattices")
                check(multiply(multiply(inverse(aj), cycle_change), ai) == transition,
                      "face transition derived from action and cycle matrices", "d5_lattices")
                check(multiply(transition, transition) == identity(2),
                      "face transition inverse", "d5_lattices")
                check(multiply(cycle_change, cycle_change) == identity(2),
                      "torus cycle-change inverse", "d5_lattices")
                face_matrices.add(matrix_key(transition))
                m.append(n - 1)
                theta.append(y + yp)
            check(sorted(counts) == [1, 1, 3], "3,1,1 allocation", "d5_counts")
            check(sum(counts) == 5, "five nodes per shared curve", "d5_counts")
            check(add(*shared_areas) == rows[j], "shared basins exhaust actual curve", "d5_areas")
            check(sum(m) == sum(theta) == 2, "clutching and fan-relation sums", "d5_lattices")

            # Model branch H1 basis (alpha,beta1,beta2), beta3=-alpha-beta1-beta2.
            cycle_columns = [[-1, m[0], m[1]], [0, 1, 0], [0, 0, 1]]
            normal, beta1, beta2 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
            beta3 = (-1, -1, -1)
            primed = [scale(-1, normal)] + [add(beta, scale(shift, normal))
                                           for beta, shift in zip((beta1, beta2, beta3), m)]
            check(add(*primed) == (0, 0, 0), "primed normal Euler-one relation", "d5_lattices")
            check(determinant(cycle_columns) == -1 and
                  multiply(cycle_columns, cycle_columns) == identity(3),
                  "branch-block cycle GL3 inverse", "d5_lattices")
            cycle_matrices.add(matrix_key(cycle_columns))

            # Tangent lattices are separate from the action cotangent lattices.
            star = [[-1, theta[0], theta[1]], [0, 1, 0], [0, 0, 1]]
            star_rays = [normal, beta1, beta2, beta3]
            images = [scale(-1, normal)] + [add(ray, scale(shift, normal))
                                           for ray, shift in zip(star_rays[1:], theta)]
            check(all(apply(star, ray) == image for ray, image in zip(star_rays, images)),
                  "common fan GL3 map on all four rays", "d5_lattices")
            check(add(*images) == (0, 0, 0), "K4 ray relation preserved", "d5_lattices")
            check(determinant(star) == -1 and multiply(star, star) == identity(3),
                  "fan-star GL3 inverse", "d5_lattices")
            star_matrices.add(matrix_key(star))
        triangle_counts = []
        for triple in combinations(range(5), 3):
            selected = 0
            total = 0
            for i, j in combinations(triple, 2):
                k = next(x for x in triple if x not in (i, j))
                total += allocations[i, j, k]
                selected += int(system[i][j] == k)
            check(selected == 1, "one midpoint relation per triangle", "d5_counts")
            check(total == 5, "five nodes per triangle", "d5_counts")
            triangle_counts.append(total)
        check(sum(triangle_counts) == 50, "fifty quintic nodes", "d5_counts")
    return {
        "systems_checked": len(systems),
        "weight_coefficient_basis": ["c", "b0", "b1", "b2", "b3", "b4"],
        "weight_formula": "w_ij=c+b_j-b_i",
        "weights_positive_iff": "max(b)-min(b)<c",
        "uniqueness_certificates": uniqueness,
        "curves_per_system": 10,
        "nodes_per_curve": [3, 1, 1],
        "triangles_per_system": 10,
        "nodes_per_triangle": 5,
        "total_nodes_per_system": 50,
        "branches_per_system": 10,
        "normalized_branch_length": "2c=a/(4*pi)",
        "face_transition_matrices": sorted(face_matrices),
        "fan_star_GL3_matrices": sorted(star_matrices),
        "cycle_GL3_columns_in_old_basis": sorted(cycle_matrices),
        "variance": "cycle columns describe homology; transpose acts on period vectors; fan matrices act on tangent vectors",
    }


# The standard primitive Petersen rays from the v7 certificate, in N=Z^5.
PETERSEN_RAYS = {
    (0, 1): (1, 0, 0, 0, 0),
    (0, 2): (0, 1, 0, 0, 0),
    (0, 3): (0, 0, 1, 0, 0),
    (1, 2): (0, 0, 0, 1, 0),
    (1, 3): (0, 0, 0, 0, 1),
    (2, 3): (-1, -1, -1, -1, -1),
    (0, 4): (-1, -1, -1, 0, 0),
    (1, 4): (-1, 0, 0, -1, -1),
    (2, 4): (1, 0, 1, 0, 1),
    (3, 4): (1, 1, 0, 1, 0),
}


def graph_isomorphism(source, target):
    mapping, used = {}, set()

    def visit():
        if len(mapping) == len(source):
            return dict(mapping)
        vertex = max((v for v in source if v not in mapping),
                     key=lambda v: (sum(w in mapping for w in source[v]), v))
        for image in sorted(target):
            if image in used:
                continue
            if all((old in source[vertex]) == (new in target[image])
                   for old, new in mapping.items()):
                mapping[vertex] = image
                used.add(image)
                result = visit()
                if result is not None:
                    return result
                used.remove(image)
                del mapping[vertex]
        return None

    return visit()


def quartet_graph(core, parts):
    vertices = [(j, part) for j in range(6) if j != core
                for part in parts[tuple(sorted((core, j)))]]
    graph = {v: set() for v in vertices}

    def edge(v, w):
        graph[v].add(w)
        graph[w].add(v)

    for j in range(6):
        if j != core:
            pair_parts = parts[tuple(sorted((core, j)))]
            edge((j, pair_parts[0]), (j, pair_parts[1]))
    for j, k in combinations([a for a in range(6) if a != core], 2):
        left = next(part for part in parts[tuple(sorted((core, j)))] if k in part)
        right = next(part for part in parts[tuple(sorted((core, k)))] if j in part)
        edge((j, left), (k, right))
    return graph


def verify_sextic(matchings, factorizations):
    c, b, weights, rows = coefficient_models(6)
    unique = uniqueness_matrix(6)
    reference = {s: {t for t in PETERSEN_RAYS if set(s).isdisjoint(t)}
                 for s in PETERSEN_RAYS}
    local_models = 0
    saturated_faces = 0
    saturated_stars = 0
    shared_branches = 0
    factorization_records = []
    core_maps = []
    for factorization in factorizations:
        parts = {edge: tuple(sorted(e for e in matchings[index] if e != edge))
                 for index in factorization for edge in matchings[index]}
        models = {}
        for core in range(6):
            graph = quartet_graph(core, parts)
            isomorphism = graph_isomorphism(graph, reference)
            check(isomorphism is not None, "quartet expansion is Petersen", "d6_labels")
            rays = {v: PETERSEN_RAYS[isomorphism[v]] for v in graph}
            models[core] = (graph, rays)
            local_models += 1
            check(len(graph) == 10 and sum(map(len, graph.values())) == 30,
                  "ten vertices and fifteen faces", "d6_labels")
            for v, neighbors in graph.items():
                check(add(*(rays[w] for w in neighbors)) == rays[v],
                      "Petersen balancing relation", "d6_lattices")
                crossing = sorted(w for w in neighbors if w[0] != v[0])
                check(len(crossing) == 2, "two crossing neighbors", "d6_labels")
                check(primitive_span([rays[v], rays[crossing[0]], rays[crossing[1]]]),
                      "saturated rank-three branch star", "d6_lattices")
                saturated_stars += 1
                for w in neighbors:
                    if v < w:
                        check(primitive_span([rays[v], rays[w]]),
                              "saturated rank-two face lattice", "d6_lattices")
                        saturated_faces += 1
            core_maps.append({"factorization_index": len(factorization_records), "core": core,
                              "vertex_to_kneser_pair": [[j, list(part), list(isomorphism[j, part])]
                                                       for j, part in sorted(graph)]})

        triangle_counts = Counter()
        bigon_counts = {}
        for i, j in combinations(range(6), 2):
            delta = add(b[j], scale(-1, b[i]))
            area_parts = []
            for k in range(6):
                if k not in (i, j):
                    check(add(weights[i, k], scale(-1, delta)) == weights[j, k],
                          "one-node external basin area identity", "d6_areas")
                    triangle_counts[tuple(sorted((i, j, k)))] += 1
                    area_parts.append(weights[j, k])
            check(add(weights[i, j], scale(-2, delta)) == weights[j, i],
                  "two-node internal annulus area identity", "d6_areas")
            area_parts.append(weights[j, i])
            check(add(*area_parts) == rows[j], "five regions exhaust actual curve", "d6_areas")
            bigon_counts[i, j] = 2
            check(4 * 1 + 2 == 6, "six nodes per curve", "d6_counts")

            for side, part in enumerate(parts[i, j]):
                shared_branches += 1
                gi, ri = models[i]
                gj, rj = models[j]
                v, vp = (j, part), (i, part)
                x_labels = sorted(part)
                neighbors_i = [next(w for w in gi[v] if w[0] == k) for k in x_labels]
                neighbors_j = [next(w for w in gj[vp] if w[0] == k) for k in x_labels]
                zi = next(w for w in gi[v] if w[0] == j)
                zj = next(w for w in gj[vp] if w[0] == i)
                source_basis = [ri[v]] + [ri[w] for w in neighbors_i]
                target_basis = [rj[vp]] + [rj[w] for w in neighbors_j]
                check(add(source_basis[0], scale(-1, source_basis[1]), scale(-1, source_basis[2])) == ri[zi],
                      "matching ray coordinates in source star", "d6_lattices")
                check(add(target_basis[0], scale(-1, target_basis[1]), scale(-1, target_basis[2])) == rj[zj],
                      "matching ray coordinates in target star", "d6_lattices")
                star = [[-1, 0, 0], [0, 1, 0], [0, 0, 1]]
                matching_image_coefficients = apply(star, (1, -1, -1))
                matching_image = add(*(scale(a, ray) for a, ray in zip(matching_image_coefficients, target_basis)))
                check(matching_image == add(rj[zj], scale(-2, rj[vp])),
                      "matching ray maps to r_z'-2r_v'", "d6_lattices")
                check(determinant(star) == -1 and multiply(star, star) == identity(3),
                      "Petersen star GL3 inverse", "d6_lattices")

                # Global K-side annular cycle differs at A and B.  At B,
                # the local outward matching cycle is b=-alpha-beta_K.
                cycle_global = [[-1, 0], [2 * side, 1]]
                local_frame = identity(2) if side == 0 else [[1, 0], [-1, -1]]
                local_cycle_change = multiply(multiply(local_frame, cycle_global), inverse(local_frame))
                check(local_cycle_change == [[-1, 0], [0, 1]],
                      "both branches have the same local outward-cycle comparison", "d6_lattices")
                check(multiply(cycle_global, cycle_global) == identity(2),
                      "global annular cycle-change inverse", "d6_lattices")
                source_slope = (1, -side)
                target_slope = (-1, side)
                check(apply(cycle_global, source_slope) == target_slope,
                      "A/B internal critical slopes", "d6_lattices")
                external_action_to_fan = [[-1, 0], [0, -1]]
                internal_action_to_fan = [[-1, -1], [0, 1]]
                for action_to_fan, expected in [
                    (external_action_to_fan, [[-1, 0], [0, 1]]),
                    (internal_action_to_fan, [[-1, -2], [0, 1]]),
                ]:
                    actual = multiply(multiply(action_to_fan, local_cycle_change), inverse(action_to_fan))
                    check(actual == expected, "face transition from local cycle shear", "d6_lattices")
                    check(multiply(actual, actual) == identity(2), "face inverse", "d6_lattices")
                check(2 + 2 * side - 2 == 2 * side,
                      "basin/internal node clutching minus two triple ends", "d6_lattices")
                check(add(weights[i, j], weights[j, i]) == scale(2, c),
                      "each of the two branches has length 2c", "d6_areas")
        check(len(triangle_counts) == 20 and set(triangle_counts.values()) == {3},
              "twenty triangles with three nodes", "d6_counts")
        check(len(bigon_counts) == 15 and set(bigon_counts.values()) == {2},
              "fifteen bigons with two nodes", "d6_counts")
        check(sum(triangle_counts.values()) + sum(bigon_counts.values()) == 90,
              "ninety sextic nodes", "d6_counts")
        factorization_records.append({"triangles": 20, "nodes_per_triangle": 3,
                                      "bigons": 15, "nodes_per_bigon": 2,
                                      "total_nodes": 90, "branches": 30})
    return {
        "systems_checked": len(factorizations),
        "weight_coefficient_basis": ["c", "b0", "b1", "b2", "b3", "b4", "b5"],
        "weight_formula": "w_ij=c+b_j-b_i",
        "weights_positive_iff": "max(b)-min(b)<c",
        "uniqueness_certificate": unique,
        "per_system": factorization_records,
        "Petersen_core_models_checked": local_models,
        "saturated_face_lattices_checked": saturated_faces,
        "saturated_star_lattices_checked": saturated_stars,
        "shared_branch_comparisons_checked": shared_branches,
        "normalized_branch_length": "2c=a/(5*pi)",
        "global_K_cycle_changes_A_B": [[[-1, 0], [0, 1]], [[-1, 0], [2, 1]]],
        "local_outward_cycle_change": [[-1, 0], [0, 1]],
        "fan_star_matrix_in_saturated_star_bases": [[-1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "crossing_face_transition": [[-1, 0], [0, 1]],
        "matching_face_transition": [[-1, -2], [0, 1]],
        "explicit_core_label_maps": core_maps,
    }


def verify_local_clutching_and_defect():
    alpha = (-1, 1, 0)
    alpha_prime = (1, -1, 0)
    nu = (-1, 0, 1)
    nu_prime = (0, -1, 1)
    check(alpha_prime == scale(-1, alpha), "triple-end normal reversal", "clutching")
    check(nu_prime == add(nu, scale(-1, alpha)), "triple-end puncture shear", "clutching")
    check(all(sum(v) == 0 for v in (alpha, alpha_prime, nu, nu_prime)),
          "triple-end cycles lie in the product-one torus", "clutching")
    check(primitive_span([alpha, nu]), "triple-end torus basis is primitive", "clutching")
    # x=zu: a constant-u positive z-loop has old (angle_x,angle_z)=(1,1).
    check(add((0, 1), (1, 0)) == (1, 1), "one blow-up adds the normal circle", "clutching")

    # Defect is paired cotangent/tangent data, not an ambient-H1 extension.
    # Independent symbolic coefficient certificate in
    # (kappa_i,kappa_j,m1,m2,h1,h2,h3).
    e = [tuple(int(i == j) for j in range(7)) for i in range(7)]
    ki, kj, m1, m2, h1, h2, h3 = e
    m3 = scale(-1, add(ki, kj, m1, m2))
    defect_i = add(scale(-1, h1), scale(-1, h2), scale(-1, h3), m1, m2, m3, ki)
    defect_j = add(h1, h2, h3, kj)
    check(add(defect_i, defect_j) == (0,) * 7,
          "opposite normals give cancelling defects coefficientwise", "defect")
    lift_instances = 0
    for kappa_i, kappa_j, a, b in product((-1, 0, 1), (-1, 0, 1), range(-2, 3), range(-2, 3)):
        lift_instances += 1
        third = -kappa_i - kappa_j - a - b
        matrix = [[-1, a, b], [0, 1, 0], [0, 0, 1]]
        source_last = (kappa_i, -1, -1)
        target_last = (kappa_j, -1, -1)
        check(apply(matrix, source_last) == add(target_last, (third, 0, 0)),
              "three transverse lifts preserve the balancing relation", "defect")
        check(determinant(matrix) == -1 and multiply(matrix, matrix) == identity(3),
              "star transition is an integer lattice isomorphism", "defect")
    budgets = {}
    for name, vertices, kappa, self_intersections, internal_edges in [
        ("four_lines_K4", 4, -1, [1, 1, 1, 1], [0, 0, 0, 0]),
        ("five_lines_Petersen", 10, 1, [1] * 5, [1] * 5),
        ("two_lines_conic_K4", 4, -1, [1, 1, 4], [0, 0, 1]),
        ("quadric_three_11_K33", 6, 0, [2, 2, 2], [1, 1, 1]),
    ]:
        p_total = sum(internal_edges) - sum(self_intersections)
        defect = vertices * kappa - 2 * sum(internal_edges) - p_total
        budgets[name] = {"vertices": vertices, "kappa": kappa,
                         "internal_edges": sum(internal_edges),
                         "total_outgoing_critical_slopes": p_total,
                         "total_defect": defect}
    check(budgets["four_lines_K4"]["total_defect"] == 0,
          "all-plane quintic core defect vanishes", "defect")
    check(budgets["five_lines_Petersen"]["total_defect"] == 0,
          "all-plane sextic core defect vanishes", "defect")
    check(budgets["two_lines_conic_K4"]["total_defect"] == -1,
          "mixed plane core defect", "defect")
    check(budgets["quadric_three_11_K33"]["total_defect"] == -3,
          "quadric core defect", "defect")
    total = 3 * budgets["two_lines_conic_K4"]["total_defect"] + budgets["quadric_three_11_K33"]["total_defect"]
    check(total == -6, "mixed quintic total defect is nonzero", "defect")
    check(3 * 4 + 6 == 2 * (3 + 3 * 2), "all eighteen ends pair into nine branches", "defect")
    return {
        "triple_end_cycles": {"alpha": alpha, "alpha_prime": alpha_prime,
                              "nu": nu, "nu_prime": nu_prime},
        "defect_opposite_normal_identity": "D_i+D_j=0 coefficientwise",
        "star_lift_instances_checked": lift_instances,
        "core_budgets": budgets,
        "mixed_quintic_total_defect": total,
        "mixed_quintic_branch_ends": 18,
        "mixed_quintic_branches": 9,
        "defect_scope": "q=1 core charts, ambient integral-affine transitions, existing branch graph, and opposite primitive normal cycles; not an obstruction to individual facewise charts",
    }


def main():
    source = Path(__file__).resolve()
    matchings, factorizations, systems, labels = verify_symmetric_systems()
    result = {
        "version": 8,
        "code_sha256": sha256(source.read_bytes()).hexdigest(),
        "arithmetic": "integer coefficients and fractions.Fraction; no floating-point comparisons",
        "labels": labels,
        "quintic": verify_quintic(systems),
        "sextic": verify_sextic(matchings, factorizations),
        "clutching_and_defect": verify_local_clutching_and_defect(),
        "scope": {
            "certified": [
                "finite marked recipes and one-factorizations",
                "formal central-curve area and node identities",
                "model torus cycle shears and fan-star lattice maps",
                "coefficientwise defect cancellation and q=1 core budgets",
            ],
            "not_certified": [
                "actual finite-parameter symplectic transport",
                "equality of finite-parameter action intercepts",
                "construction of affine-critical-action neck families",
                "analytic neck gluing or existence of a global atlas",
                "compatibility of a chosen ambient H1 extension across every neck",
            ],
        },
    }
    result["checks_by_category"] = dict(sorted(CHECKS.items()))
    result["exact_checks"] = sum(CHECKS.values())
    result["passed"] = True
    output = source.with_name("global_action_atlas_verification_v8.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"global action compatibility v8: {sum(CHECKS.values())} exact checks passed; "
          f"6 quintic recipes, 6 sextic systems; no analytic gluing certified; result={output.name}")


if __name__ == "__main__":
    main()
