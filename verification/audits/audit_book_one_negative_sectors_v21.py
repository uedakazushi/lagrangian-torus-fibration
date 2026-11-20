#!/usr/bin/env python3
"""Independently audit the one-negative sector certificate with the v19 generator.

Neither new v21 primary verifier nor its v21 reconstruction dependency is
imported.  The unchanged v19 generator recomputes every initial core, both
complete neighbour sets, and all final-edge comparisons.  Reading the new
source files below is solely for checking certificate hashes.

Run without arguments inside the completed v21 bundle.  Explicit source
paths allow an audit during staging, before those files are copied in place.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import isqrt
from pathlib import Path
from _legacy_provenance import matches_archived_source

import argparse
import json
import sys


HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
GENERATOR = ROOT / "research/book_low_triangle_completion_v19.py"
assert GENERATOR.is_file(), GENERATOR
sys.path.insert(0, str(GENERATOR.parent))
from book_low_triangle_completion_v19 import negative_models, neighbours, low_edge


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def short_model(model):
    # JSON normalization turns the integer vertex keys into strings.
    return json.loads(json.dumps({key: model[key] for key in
                                 ("canonical", "order", "vertex", "q", "D")}))


def as_set(models):
    result = {canonical_json(model) for model in models}
    assert len(result) == len(models), "duplicate complete model record"
    return result


def analytic_checks(certificate):
    """Recompute the rational constants, without calling either v21 verifier."""
    slope, intercept = Fraction(3, 7), Fraction(-1)
    gaps = {}
    for delta in (2, 3):
        coefficients = (
            2 * (delta - 1) - slope * slope - 4 * slope,
            -(2 * slope * intercept + 4 * intercept + (delta + 1) * slope),
            -(intercept * intercept + (delta + 1) * intercept),
        )
        assert min(coefficients) > 0
        gaps[delta] = [[value.numerator, value.denominator] for value in coefficients]
    assert gaps == {2: [[5, 49], [25, 7], [2, 1]],
                    3: [[103, 49], [22, 7], [3, 1]]}
    growth = Fraction(10, 7)
    # Type I, negative tau: lower T1 > growth^2*(w-2)+1-growth.
    strict_I_negative = (1 + 2 * growth * growth - 1 + growth) / (growth * growth - 2)
    assert strict_I_negative == 135
    # Positive tau, L=(4,3),(3,4),(4,4), respectively.
    strict_I_positive = {
        "4,3": Fraction(5) / (3 - Fraction(17, 7)),
        "3,4": Fraction(9, 2) / (3 - Fraction(17, 7)),
        "4,4": Fraction(5) / (4 - Fraction(17, 7)),
    }
    assert strict_I_positive == {"4,3": Fraction(35, 4),
                                 "3,4": Fraction(63, 8),
                                 "4,4": Fraction(35, 11)}
    strict_II_negative = (Fraction(14, 3) - Fraction(1, 2)) / (Fraction(17, 10) - Fraction(4, 3))
    strict_II_positive = Fraction(4) / (2 - Fraction(7, 5))
    assert strict_II_negative == Fraction(125, 11)
    assert strict_II_positive == Fraction(20, 3)
    actual = certificate["analytic_constants"]
    assert actual["universal_proved_w_max"] == 134
    assert actual["type_I_negative_tau_strict_w_bound"] == [135, 1]
    assert actual["type_I_positive_tau_with_L4_strict_w_bounds"] == {
        key: [value.numerator, value.denominator] for key, value in strict_I_positive.items()}
    assert actual["type_II_negative_tau_strict_w_bound"] == [125, 11]
    assert actual["type_II_positive_tau_P1_L3_strict_w_bound"] == [20, 3]
    return dict(status="PASS", growth_difference_coefficients=gaps,
                universal_proved_w_max=134,
                sector_integer_w_bounds=[134, 8, 11, 6])


def audit(certificate_path, primary, dependency, proof, quiet=False):
    certificate = json.loads(certificate_path.read_text())
    assert certificate["status"] == "PASS"
    assert certificate["arbitrary_scale_or_denominator_cutoff"] is None
    analytic = analytic_checks(certificate)
    bound = 134

    # This finite reverse-pair count uses the v19 loop's exact integer condition.
    reverse_count = sum(
        w * w < 2 * H * (H + 1) < 4 * w * w
        for w in range(2, bound + 1)
        for H in range(1, isqrt(2 * w * w) + 1)
    )
    assert reverse_count == 6392 == certificate["counts"]["initial_reverse_parameters"]

    cores = list(negative_models(bound))
    core_keys = {model["canonical"] for model in cores}
    assert len(core_keys) == len(cores) == 1089
    raw_records = certificate["initial_core_records"]
    records = {tuple(record["fixed"]["canonical"]): record for record in raw_records}
    assert len(records) == len(raw_records) == len(cores)
    assert set(records) == core_keys

    computed_final = []
    neighbour_total = 0
    double_nonempty = []
    checked_sets = 0
    for number, core in enumerate(cores, 1):
        record = records[core["canonical"]]
        assert short_model(core) == record["fixed"]
        left = neighbours(core, 3)
        right = neighbours(core, 4)
        assert [len(left), len(right)] == record["neighbour_counts"]
        for side, expected_name in ((left, "neighbours_left"), (right, "neighbours_right")):
            assert as_set([short_model(model) for model in side]) == as_set(record[expected_name])
            checked_sets += 1
        neighbour_total += len(left) + len(right)
        if left and right:
            double_nonempty.append(core["canonical"])
        for a, b in product(left, right):
            nodes = [1 - a["p"][4][k] - b["p"][3][k] for k in (0, 1, 2)]
            residual = a["D"][4] + b["D"][3]
            assert sum(nodes) == 5
            assert residual != 0
            assert low_edge(a, b) is None
            computed_final.append(dict(fixed=list(core["canonical"]),
                                       left=short_model(a), right=short_model(b),
                                       final_nodes=nodes, final_D_residual=residual))
        if not quiet and number % 200 == 0:
            print(json.dumps({"audit_progress": number, "initial_cores": len(cores),
                              "checked_neighbour_sets": checked_sets,
                              "total_neighbours_so_far": neighbour_total}), flush=True)

    assert checked_sets == 2178
    assert neighbour_total == 169 == certificate["counts"]["all_neighbour_models"]
    assert len(double_nonempty) == 6
    assert {tuple(record["fixed"]["canonical"]) for record in certificate["double_nonempty_records"]} == set(double_nonempty)
    assert len(computed_final) == 11
    assert as_set(computed_final) == as_set(certificate["final_edge_certificates"])
    counts = certificate["counts"]
    assert counts["initial_cores"] == len(cores)
    assert counts["with_two_nonempty_neighbour_sets"] == len(double_nonempty)
    assert counts["final_edge_pairs"] == len(computed_final)
    assert counts["survivors"] == 0
    assert counts["initial_cores_with_w_at_most_50"] == sum(core["canonical"][3] <= 50 for core in cores) == 313
    by_w = {str(key): value for key, value in sorted(Counter(core["canonical"][3] for core in cores).items())}
    assert by_w == counts["by_w"]
    maximum_denominator = max(max(model["q"].values()) for model in cores)
    assert maximum_denominator == certificate["maximum_initial_high_denominator"] == 4794119

    # Check the exact provenance, but NEVER import these v21 implementations.
    assert matches_archived_source(primary, certificate["source_sha256"])
    assert matches_archived_source(dependency, certificate["reconstruction_dependency_sha256"])
    assert sha256(proof.read_bytes()).hexdigest() == certificate["proof_sha256"]
    assert certificate["proof_file"] == proof.name
    assert certificate["reconstruction_dependency"] == dependency.name
    assert "verify_book_one_negative_sector_reduction_v21" not in sys.modules
    assert "verify_book_two_negative_obstruction_v21" not in sys.modules

    return dict(
        status="PASS", version="v21",
        method="All initial models and complete neighbour sets recomputed with the unchanged v19 generator; no v21 primary or dependency imported.",
        mathematical_scope="Independent audit of the derived finite range 2<=w<=134; supports the two residual one-negative sectors, without claiming their existence or nonexistence.",
        initial_reverse_parameters=reverse_count,
        initial_cores=len(cores), checked_neighbour_sets=checked_sets,
        total_neighbours=neighbour_total,
        double_nonempty_cores=len(double_nonempty), final_pairs=len(computed_final),
        final_D_residuals=sorted(record["final_D_residual"] for record in computed_final),
        survivors=0, maximum_initial_high_denominator=maximum_denominator,
        all_initial_model_data_equal=True,
        all_complete_neighbour_sets_equal=True,
        all_final_edge_data_equal=True,
        per_w_counts_equal=True,
        analytic_constant_audit=analytic,
        arbitrary_scale_or_denominator_cutoff=None,
        external_peer_review=False, proof_assistant_formalization=False,
        audit_script_sha256=sha256(HERE.read_bytes()).hexdigest(),
        certificate_file=certificate_path.name,
        certificate_sha256=sha256(certificate_path.read_bytes()).hexdigest(),
        primary_source_sha256=sha256(primary.read_bytes()).hexdigest(),
        reconstruction_dependency_sha256=sha256(dependency.read_bytes()).hexdigest(),
        proof_file=proof.name, proof_sha256=sha256(proof.read_bytes()).hexdigest(),
        previous_generator_file=GENERATOR.name,
        previous_generator_sha256=sha256(GENERATOR.read_bytes()).hexdigest(),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=ROOT / "verification/book_one_negative_sector_reduction_verification_v21.json")
    parser.add_argument("--primary", type=Path, default=ROOT / "verification/verify_book_one_negative_sector_reduction_v21.py")
    parser.add_argument("--dependency", type=Path, default=ROOT / "verification/verify_book_two_negative_obstruction_v21.py")
    parser.add_argument("--proof", type=Path, default=ROOT / "papers/sections/paper/book_one_negative_sector_reduction_v21.tex")
    parser.add_argument("--output", type=Path, default=HERE.with_name("book_one_negative_sectors_independent_audit_v21.json"))
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    report = audit(args.certificate, args.primary, args.dependency, args.proof, args.quiet)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
