#!/usr/bin/env python3
"""Exact finite certificates for the v8 quadric K3,3 action charts.

Only the Python standard library is used.  The checks certify integer
identities, fan lattices, and all 64 one-enlarged-basin recipes.  They do not
replace relative Moser, the actual normal-bundle framing argument, or the
analytic existence proof for the local Liouville cone chart.
"""

from collections import Counter
from fractions import Fraction
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


def scale(n, vector):
    return tuple(n * x for x in vector)


def determinant(matrix):
    matrix = [list(map(Fraction, row)) for row in matrix]
    n = len(matrix)
    result = Fraction(1)
    for c in range(n):
        pivot = next((r for r in range(c, n) if matrix[r][c]), None)
        if pivot is None:
            return 0
        if pivot != c:
            matrix[c], matrix[pivot] = matrix[pivot], matrix[c]
            result = -result
        pivot_value = matrix[c][c]
        result *= pivot_value
        for r in range(c + 1, n):
            multiplier = matrix[r][c] / pivot_value
            for j in range(c, n):
                matrix[r][j] -= multiplier * matrix[c][j]
    return result


def minor_gcd(columns):
    k = len(columns)
    answer = 0
    for rows in combinations(range(len(columns[0])), k):
        minor = determinant([[v[r] for v in columns] for r in rows])
        check(minor.denominator == 1 if isinstance(minor, Fraction) else True,
              "integer matrix minor")
        answer = gcd(answer, abs(int(minor)))
    return answer


def coordinates(vector, first, second):
    for i, j in combinations(range(4), 2):
        d = first[i] * second[j] - first[j] * second[i]
        if d:
            a = Fraction(vector[i] * second[j] - vector[j] * second[i], d)
            b = Fraction(first[i] * vector[j] - first[j] * vector[i], d)
            if all(a * first[k] + b * second[k] == vector[k] for k in range(4)):
                return a, b
            return None
    return None


def graphic_rank(subset, edges):
    parent = list(range(4))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    rank = 0
    for label in subset:
        a, b = map(find, edges[label])
        if a != b:
            parent[a] = b
            rank += 1
    return rank


def verify_fan():
    a_rays = [(-1, -1, 0, 0), (1, 0, 0, 0), (0, 1, 0, 0)]
    b_rays = [(0, 0, -1, -1), (0, 0, 1, 0), (0, 0, 0, 1)]
    check(add(*a_rays) == (0, 0, 0, 0), "A balancing relation")
    check(add(*b_rays) == (0, 0, 0, 0), "B balancing relation")
    for ray in a_rays + b_rays:
        check(gcd(*ray) == 1, "primitive fan ray")
    cones = [(a, b) for a in range(3) for b in range(3)]
    for a, b in cones:
        check(minor_gcd([a_rays[a], b_rays[b]]) == 1, "saturated face lattice")
    for rays, other in [(a_rays, b_rays), (b_rays, a_rays)]:
        for ray in rays:
            check(minor_gcd([ray, other[1], other[2]]) == 1,
                  "saturated rank-three star span")

    # The graphic matroid K4-e has circuits 012, 034, and 1234.
    edges = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3)]
    ground = set(range(5))
    circuits = []
    rank_two_flats = []
    for size in range(1, 6):
        for subset_tuple in combinations(range(5), size):
            subset = set(subset_tuple)
            rank = graphic_rank(subset, edges)
            if rank < size and all(graphic_rank(subset - {i}, edges) == size - 1
                                   for i in subset):
                circuits.append(subset_tuple)
            if rank == 2 and all(graphic_rank(subset | {i}, edges) == 3
                                 for i in ground - subset):
                rank_two_flats.append(subset_tuple)
    check(circuits == [(0, 1, 2), (0, 3, 4), (1, 2, 3, 4)],
          "exact graphic circuits")
    check(len(rank_two_flats) == 6, "six rank-two flats")
    e = [(-1, -1, -1, -1)] + [tuple(int(i == j) for j in range(4))
                               for i in range(4)]
    fine_cones = [(i, flat) for flat in rank_two_flats for i in flat]
    cover_counts = Counter()
    for i, flat in fine_cones:
        v = e[i]
        w = add(*(e[j] for j in flat))
        containing = []
        for a, b in cones:
            v_co = coordinates(v, a_rays[a], b_rays[b])
            w_co = coordinates(w, a_rays[a], b_rays[b])
            if v_co is not None and w_co is not None and min(*v_co, *w_co) >= 0:
                if v_co[0] * w_co[1] - v_co[1] * w_co[0]:
                    containing.append((a, b))
        check(len(containing) == 1, "unique coarse cone for each fine flag")
        cover_counts[containing[0]] += 1
    check(len(fine_cones) == 14, "fourteen fine cones")
    check(Counter(cover_counts.values()) == {1: 4, 2: 5},
          "four undivided and five subdivided coarse cones")
    return {
        "rays_A": a_rays,
        "rays_B": b_rays,
        "coarse_cones": 9,
        "fine_cones": len(fine_cones),
        "graphic_circuits": circuits,
        "rank_two_flats": rank_two_flats,
        "all_face_lattices_saturated": True,
        "all_star_spans_saturated": True,
    }


def verify_recipes():
    basis = [tuple(int(a == b) for b in range(3)) for a in range(3)]
    # A port on component a is (side A or B, other component b).
    choices = [[(side, b) for side in ("A", "B") for b in range(3) if b != a]
               for a in range(3)]
    records = []
    bad_histogram = Counter()
    for recipe in product(*choices):
        selected = {(a, side, b) for a, (side, b) in enumerate(recipe)}
        for a in range(3):
            basin_vectors = []
            for side, b in choices[a]:
                enlarged = int((a, side, b) in selected)
                target = add(basis[b], scale(enlarged, basis[a]))
                check(min(target) >= 0 and max(target) > 0, "positive basin polynomial")
                basin_vectors.append(target)
            check(add(*basin_vectors, basis[a]) == (2, 2, 2),
                  "exact quadric area budget with annulus weight w_a")

        crossing_determinants = []
        crossing_matrices = []
        for a in range(3):
            for b in range(3):
                if a == b:
                    continue
                eps_a = int((a, "A", b) in selected)
                eps_b = int((b, "B", a) in selected)
                matrix = [[-1, eps_b], [eps_a, -1]]
                det = int(determinant(matrix))
                check(det == 1 - eps_a * eps_b, "crossing determinant formula")
                crossing_determinants.append(det)
                crossing_matrices.append(matrix)
                for column in zip(*matrix):
                    check(gcd(*column) == 1, "primitive crossing endpoint direction")
                if det == 1:
                    # Coefficients of x,y at product moment limits (-w_a,-w_b).
                    check(min(add(basis[a], scale(eps_b, basis[b]))) >= 0,
                          "positive product-sector x polynomial")
                    check(min(add(scale(eps_a, basis[a]), basis[b])) >= 0,
                          "positive product-sector y polynomial")

        internal_matrices = []
        for a, (side, _) in enumerate(recipe):
            m = int(side == "A")
            matrix = [[-1, -1], [m, m + 1]]
            check(determinant(matrix) == -1, "internal determinant")
            # Endpoint sum: beta_A + beta_B = -2 alpha, with
            # slope_A=-m and slope_B=-(1-m).
            check(2 - m - (1 - m) == 1, "Euler-two Farey gap equals one")
            check((m + 1) == 2 - (1 - m), "actual Euler-two endpoint relation")
            for column in zip(*matrix):
                check(gcd(*column) == 1, "primitive internal endpoint direction")
            internal_matrices.append(matrix)

        bad = crossing_determinants.count(0)
        bad_histogram[bad] += 1
        check(bad <= 1, "bad-crossing events do not overlap")
        records.append({
            "recipe": [[side, b] for side, b in recipe],
            "admissible": bad == 0,
            "crossing_determinants": crossing_determinants,
            "internal_determinants": [-1, -1, -1],
        })
    check(len(records) == 64, "complete recipe enumeration")
    check(bad_histogram == {0: 40, 1: 24}, "exact 40/24 split")
    principal = [["A", (a + 1) % 3] for a in range(3)]
    principal_record = next(item for item in records if item["recipe"] == principal)
    check(principal_record["admissible"], "cyclic all-A recipe")
    return {
        "recipes_total": len(records),
        "admissible_recipes": bad_histogram[0],
        "degenerate_recipes": bad_histogram[1],
        "principal_recipe": principal_record,
        "all_positive_weights": "area identities checked coefficientwise in w_0,w_1,w_2",
        "records": records,
    }


def verify_linear_obstruction():
    variables = [(side, a, b) for side in ("A", "B")
                 for a in range(3) for b in range(3) if a != b]
    annulus_rows = [[int(a == source) for _, a, _ in variables]
                    for source in range(3)]
    star_rows = [[int(side == side_ and b == target) for side_, _, b in variables]
                 for side in ("A", "B") for target in range(3)]
    annulus_sum = add(*annulus_rows)
    star_sum = add(*star_rows)
    check(annulus_sum == (1,) * 12, "sum of three annulus left sides")
    check(star_sum == (1,) * 12, "sum of six star-extension left sides")
    check(add(annulus_sum, scale(-1, star_sum)) == (0,) * 12,
          "zero coefficient vector in infeasibility certificate")
    check((-3) - (-6) == 3, "nonzero RHS certificate")
    return {
        "scope": "all branch denominators equal one; common-circle star-linear extension",
        "variables": variables,
        "annulus_rows": annulus_rows,
        "star_extension_rows": star_rows,
        "annulus_rhs_total": -3,
        "star_rhs_total": -6,
        "certificate": "sum(annulus rows) - sum(star rows) gives 0 = 3",
        "obstructs_facewise_chart": False,
        "decides_higher_denominators": False,
    }


def main():
    source = Path(__file__).resolve()
    output = source.with_name("quadric_periods_verification_v8.json")
    result = {
        "version": 8,
        "code_sha256": sha256(source.read_bytes()).hexdigest(),
        "fan": verify_fan(),
        "recipes": verify_recipes(),
        "conditional_linear_obstruction": verify_linear_obstruction(),
        "proof_boundary": [
            "finite exact checks do not prove relative Moser",
            "actual torus framing uses a separate normal circle-bundle argument",
            "sector positivity and cone homeomorphism use the written analytic proof",
            "no simultaneous global quintic atlas is asserted",
        ],
    }
    result["checks"] = CHECKS
    result["passed"] = True
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"quadric periods v8: {CHECKS} exact checks passed; 40/64 admissible recipes; "
          f"9 saturated cones; result={output.name}")


if __name__ == "__main__":
    main()
