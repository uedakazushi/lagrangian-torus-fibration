#!/usr/bin/env python3
"""Exact all-scale obstruction of ordinary G5_15 by outer-core pairs.

Python standard library only.  No earlier verifier or exploration is imported.
The finite range is the proved node range n=0,...,5, not a denominator cutoff.
Direct node elimination and a distinct signed-divisor reconstruction are
compared for every outer input.  The final point is rejected using original
row/pair equations and, independently, its genuine quadratic residual.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import gcd, isqrt
from pathlib import Path
import argparse
import json


NAMES = ("a", "c", "j", "sigma", "u", "v")
N = len(NAMES)


class Poly:
    """Small sparse exact polynomial ring, used only for identities."""

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {key: Fraction(val) for key, val in value.items() if val}
        else:
            self.terms = {(0,) * N: Fraction(value)} if value else {}

    def __add__(self, other):
        out = defaultdict(Fraction, self.terms)
        for key, val in Poly(other).terms.items():
            out[key] += val
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -val for key, val in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        out = defaultdict(Fraction)
        for left, a in self.terms.items():
            for right, b in Poly(other).terms.items():
                out[tuple(x + y for x, y in zip(left, right))] += a * b
        return Poly(out)

    __rmul__ = __mul__


def polynomial_identities():
    vv = tuple(Poly({tuple(int(i == k) for k in range(N)): 1})
               for i in range(N))
    a, c, j, sigma, u, v = vv
    E, q = a * u - c, 1 + j * sigma
    leading = E * (j * v + 1) - a * j
    constant = a - 1 - E * v
    direct = E * (q * v + sigma) - a * q + 1
    linear = leading * sigma - constant
    identities = {
        "outer_original_pair_equals_linear_residual": direct - linear,
        "divisor_identity_from_linear_equation":
            q * leading - (E - j) - j * linear,
        "resonance_elimination":
            leading - j * (E * v - a + 1) - (E - j),
    }
    for name, residual in identities.items():
        assert not residual.terms, name
    return list(identities)


NODES = tuple((a, b, 5 - a - b)
              for a in range(6) for b in range(6 - a))
NODE_VARIABLES = tuple(range(-4, 2))
CENTERS = ((2, 2, 6, 3, 5), (4, 4, 5, 2, 2),
           (5, 10, 2, 3, 3), (6, 6, 14, 3, 3))


def rational_pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def center_models():
    out = []
    for label, (r, s, z, S, T) in enumerate(CENTERS, 1):
        a, b = 1 + s * S, 1 + z * T
        assert s * S % r == 0 and z * T % (r + 1) == 0
        x, y, L = s * S // r, z * T // (r + 1), T - S + 1
        U, V = a + x - s, b - y + z
        q = (a, b, 1, 1)
        P = ((0, -U, x, -s), (-V, 0, -y, z),
             (r, -r - 1, 0, 0), (-S, T, -L, 0))
        assert all(sum(P[i]) == -q[i] for i in range(4))
        assert all(P[i][j] * P[j][i] == q[i] * q[j] - 1
                   for i, j in combinations(range(4), 2))
        assert a > 1 and b > 1 and a % 2 and b % 2
        D = tuple(-q[i] - sum(P[j][i] for j in range(4) if i != j)
                  for i in range(4))
        assert D[2] == T - S + y - x
        assert D[3] == s - z - 1
        weights = (Fraction(a), Fraction(b),
                   Fraction(x) + Fraction(1, 2 * r),
                   Fraction(z) + Fraction(1, 2 * T))
        assert min(weights) > 0
        gaps = tuple(weights[j] - Fraction(P[i][j], q[i]) * weights[i]
                     for i in range(4) for j in range(4) if i != j)
        assert min(gaps) > 0
        out.append(dict(label=label, parameters=[r, s, z, S, T],
                        ray_order=[0, 1, 3, 4], q=q, P=P, D=D,
                        weights=[rational_pair(w) for w in weights],
                        minimum_basin_gap=rational_pair(min(gaps))))
    assert [(m["q"][:2], m["D"][2:]) for m in out] == [
        ((7, 31), (9, -5)), ((9, 11), (0, -2)),
        ((31, 7), (-5, 7)), ((19, 43), (3, -9))]
    return out


def ordinary_cells(centers):
    out, matching_before_parity = [], 0
    rejected = []
    for center in centers:
        r, s, z, S, T = center["parameters"]
        L = T - S + 1
        for n, m in product(NODES, repeat=2):
            R3 = (1 - r - n[0], r + 2 - n[1], 1 - n[2])
            R4 = (S + 1 - m[0], 1 - T - m[1], L + 1 - m[2])
            if any(0 in R or sum(x > 0 for x in R) != 1
                   for R in (R3, R4)):
                continue
            if R3[2] + R4[2] != 0:
                continue
            matching_before_parity += 1
            d3, d4 = -center["D"][2], -center["D"][3]
            if any(all(x % 2 for x in R) and d % 2 == 0
                   for R, d in ((R3, d3), (R4, d4))):
                rejected.append(dict(center=center["label"], R3=R3,
                                     R4=R4, d3=d3, d4=d4))
                continue
            p = 3 if R3[2] > 0 else 4
            Rp, dp = (R3, d3) if p == 3 else (R4, d4)
            col = center["ray_order"].index(p)
            inputs = tuple((center["q"][i], center["P"][i][col], -Rp[i])
                           for i in (0, 1))
            assert min(-Rp[0], -Rp[1], Rp[2]) > 0
            assert all(a - 1 > j for a, c, j in inputs)
            out.append(dict(center=center["label"], nodes23=n, nodes24=m,
                            R3=R3, R4=R4, d3=d3, d4=d4,
                            positive_core=p, positive_row=Rp,
                            positive_low_D=dp, outer_inputs=inputs))
    assert matching_before_parity == 18 and len(rejected) == 4
    assert len(out) == 14
    return out, rejected


def positive_divisors(value):
    assert value > 0
    result = set()
    for k in range(1, isqrt(value) + 1):
        if value % k == 0:
            result.update((k, value // k))
    return sorted(result)


def direct_node_elimination(a, c, j):
    """Exactly 36 input node pairs, including all zero leading cases."""
    assert a - 1 > j > 0
    result, records = [], []
    for u, v in product(NODE_VARIABLES, repeat=2):
        E = a * u - c
        leading = E * (j * v + 1) - a * j
        constant = a - 1 - E * v
        entry = dict(u=u, v=v, E=E, leading=leading, constant=constant)
        if not leading:
            # A complete check of the proved nonresonance, not a division by 0.
            assert constant != 0
            entry["disposition"] = "zero_leading_nonzero_constant"
        elif constant % leading:
            entry["disposition"] = "noninteger_scale"
        else:
            sigma = constant // leading
            entry["scale"] = sigma
            q = 1 + j * sigma
            if sigma <= 0:
                entry["disposition"] = "nonpositive_scale"
            elif q % 2 == 0:
                entry["disposition"] = "even_denominator"
            else:
                assert q >= 3
                assert E * (q * v + sigma) == a * q - 1
                assert q * leading == E - j and E - j != 0
                entry.update(disposition="retained", q=q)
                result.append((sigma, u, v))
        records.append(entry)
    assert len(records) == 36
    return sorted(result), records


def divisor_reconstruction(a, c, j):
    """Independent finite algorithm: u and divisors of E-j, never scales."""
    assert a - 1 > j > 0
    result, records = [], []
    for u in NODE_VARIABLES:
        E = a * u - c
        entry = dict(u=u, E=E, fixed_integer=E - j)
        if E == 0:
            entry["disposition"] = "zero_original_pair_factor"
            records.append(entry)
            continue
        if E == j:
            assert Fraction(a - 1, j) > 1
            entry["disposition"] = "resonance_requires_v_greater_than_one"
            records.append(entry)
            continue
        candidates = []
        divisors = positive_divisors(abs(E - j))
        entry["all_positive_divisors"] = divisors
        for q in divisors:
            if q < 3 or q % 2 == 0 or (q - 1) % j:
                continue
            sigma = (q - 1) // j
            numerator = (E - j) // q - E + a * j
            denominator = j * E
            if numerator % denominator:
                continue
            v = numerator // denominator
            if v not in NODE_VARIABLES:
                continue
            assert sigma > 0
            assert E * (q * v + sigma) == a * q - 1
            result.append((sigma, u, v))
            candidates.append(dict(q=q, sigma=sigma, v=v))
        entry["retained"] = candidates
        records.append(entry)
    return sorted(result), records


EXPECTED_PROFILES = {
    (1, 4, (-1, -4, 4), 5): (1, [(2, -1, -2)], [(5, 1, 1)]),
    (1, 3, (-1, -1, 1), -9): (1, [(2, 1, 1)], []),
    (2, 4, (-1, -2, 2), 2): (3, [(2, 1, 0)], [(1, -1, -1)]),
    (2, 4, (-2, -1, 2), 2): (3, [], [(4, 1, 1)]),
    (3, 4, (-1, -2, 2), -7): (3, [], [(1, 1, 1)]),
    (4, 4, (-1, -2, 2), 9): (3, [], [(13, 1, 1)]),
}


def last_point_obstruction():
    # High ray order a,b,c.  Direct original data: m=4,S=2,T=5,U=1.
    m, S, T, U = 4, 2, 5, 1
    qa, qb, qc = S + 1, m * T + 1, m * U + 1
    assert (qa, qb, qc) == (3, 21, 5)
    A, C, F = qa * qb - 1, qa * qc - 1, qb * qc - 1
    B, E = (m - 1) * T + 1, (m + 1) * U + 1
    assert (A, C, E) == (62, 14, 6)
    h_divisors = positive_divisors(A)
    admissible = []
    for H in h_divisors:
        if C % (H + 1):
            continue
        K, M = A // H, C // (H + 1)
        N = E - M
        assert N <= 0
        admissible.append(dict(H=H, K=K, M=M, N=N,
                               failure="N must be strictly positive"))
    assert admissible == [dict(H=1, K=62, M=7, N=-1,
                              failure="N must be strictly positive")]
    # Independently eliminate M,N from their exact pairs and row sum.
    coeffs = (F - E * B, C * B + F - E * (A + B), A * (C - E))
    common = gcd(gcd(abs(coeffs[0]), abs(coeffs[1])), abs(coeffs[2]))
    primitive = tuple(c // common for c in coeffs)
    assert primitive == (2, -35, 124)
    disc = primitive[1] ** 2 - 4 * primitive[0] * primitive[2]
    assert disc == 233 and isqrt(disc) ** 2 != disc
    return dict(low_row=[-1, -4, 4], low_column=[-2, -5, 1],
                high_denominators=[qa, qb, qc], H_all_positive_divisors=h_divisors,
                pair_divisibility_candidates=admissible,
                independent_primitive_quadratic=list(primitive),
                discriminant=disc, discriminant_is_square=False,
                integer_positive_models=0)


def isolated_local_witness():
    """Check the useful scope warning: a fixed low-data local chart survives."""
    q = (7, 7, 13, 1)
    P = ((0, 8, -9, -6), (6, 0, -10, -3),
         (-10, -9, 0, 6), (-1, -2, 2, 0))
    weights = (Fraction(7), Fraction(97, 12), Fraction(25, 12), Fraction(1))
    assert all(sum(P[i]) == -q[i] for i in range(4))
    assert all(P[i][j] * P[j][i] == q[i] * q[j] - 1
               for i, j in combinations(range(4), 2))
    assert all(weights[j] - Fraction(P[i][j], q[i]) * weights[i] > 0
               for i in range(4) for j in range(4) if i != j)
    D = tuple(-q[i] - sum(P[j][i] for j in range(4) if j != i)
              for i in range(4))
    assert D == (-2, -4, 4, 2)
    return dict(ray_order=["a", "b", "c", "low"], q=q, P=P, D=D,
                weights=[rational_pair(w) for w in weights],
                low_row=[-1, -2, 2], low_column=[-6, -3, 6],
                point="An isolated positive local chart exists, but cannot be attached in ordinary G5_15")


def find_source(name, subdirectory):
    here = Path(__file__).resolve().parent
    for root in (here, *here.parents):
        for candidate in (root / name, root / subdirectory / name):
            if candidate.is_file():
                return candidate
    raise FileNotFoundError(name)


def run():
    identities = polynomial_identities()
    centers = center_models()
    cells, parity_rejected = ordinary_cells(centers)
    profile_counts = Counter((c["center"], c["positive_core"],
                              c["positive_row"], c["positive_low_D"])
                             for c in cells)
    assert set(profile_counts) == set(EXPECTED_PROFILES)
    cache, profiles = {}, []
    for key, expected in EXPECTED_PROFILES.items():
        multiplicity, expected_S, expected_T = expected
        assert profile_counts[key] == multiplicity
        cell = next(c for c in cells if (c["center"], c["positive_core"],
                                        c["positive_row"], c["positive_low_D"]) == key)
        values = []
        for data in cell["outer_inputs"]:
            if data not in cache:
                direct, direct_records = direct_node_elimination(*data)
                divisors, divisor_records = divisor_reconstruction(*data)
                assert direct == divisors
                cache[data] = dict(a=data[0], c=data[1], j=data[2],
                                   candidates=direct,
                                   complete_node_records=direct_records,
                                   complete_divisor_records=divisor_records)
            values.append(cache[data]["candidates"])
        assert values == [expected_S, expected_T]
        scale_pairs = []
        for s_record, t_record in product(*values):
            S, T = s_record[0], t_record[0]
            U = S + T - cell["positive_low_D"] - 1
            if U <= 0:
                assert key == (2, 4, (-1, -2, 2), 2) and (S, T, U) == (2, 1, 0)
                reason = "shared low-column scale U is not positive"
            else:
                assert key == (1, 4, (-1, -4, 4), 5) and (S, T, U) == (2, 5, 1)
                reason = "last-point original pair/row contradiction"
            scale_pairs.append(dict(S=S, T=T, U=U, exclusion=reason))
        profiles.append(dict(center=key[0], positive_core=key[1], low_row=key[2],
                             low_D=key[3], cells_covered=multiplicity,
                             outer_inputs=cell["outer_inputs"],
                             S_candidates=values[0], T_candidates=values[1],
                             surviving_scale_pairs_before_local_check=scale_pairs,
                             completed_ordinary_models=0))
    assert len(cache) == 11
    final_point = last_point_obstruction()
    source_files = [find_source("g5_15_ordinary_outer_pair_obstruction_v23.tex", "paper"),
                    find_source("notes_g5_15_ordinary_outer_pair_v23.tex", "notes"),
                    Path(__file__).resolve()]
    return dict(
        status="PASS",
        conclusion="All fourteen ordinary G5_15 cells are excluded for all denominators and scales",
        scope="Standard marked quintic integer gluing, five nodes per edge; not a classification of isolated local charts",
        method="Outer-core pair necessary conditions; complete proved node/divisor enumeration; final exact row/pair contradiction",
        arbitrary_cutoffs_used=False,
        earlier_code_imported=False,
        polynomial_identities=identities,
        centers=centers,
        center_node_triples_checked_per_low_edge=len(NODES),
        matching_ordinary_configurations_before_parity=18,
        parity_rejected=parity_rejected,
        ordinary_cell_count=len(cells),
        ordinary_cells=cells,
        positive_profile_count=len(profiles),
        profiles=profiles,
        distinct_outer_inputs=len(cache),
        direct_node_pairs_per_outer_input=36,
        direct_node_pairs_checked=36 * len(cache),
        outer_input_checks=list(cache.values()),
        last_point=final_point,
        isolated_local_scope_witness=isolated_local_witness(),
        completed_ordinary_models=0,
        source_sha256={p.name: sha256(p.read_bytes()).hexdigest() for p in source_files},
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or Path(__file__).with_name(
        "g5_15_ordinary_outer_pair_verification_v23.json")
    result = run()
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(status=result["status"], ordinary_cells=result["ordinary_cell_count"],
                          profiles=result["positive_profile_count"],
                          distinct_outer_inputs=result["distinct_outer_inputs"],
                          exact_node_pairs=result["direct_node_pairs_checked"],
                          completed_ordinary_models=result["completed_ordinary_models"],
                          output=str(output)), ensure_ascii=False))
