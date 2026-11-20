#!/usr/bin/env python3
"""Exact certificate for the v21 residual one-negative book sectors.

The accompanying proof derives w <= 134 for every additional sector to be
excluded.  It also proves the three smaller sector bounds <=8, <=11 and <=6.
The retained sectors are not claimed to be empty.

This driver reuses the independently written v21 two-negative verifier's
local matrix reconstruction and exact all-scale completion functions without
modifying that verifier.  No earlier v19 generator is imported.  All possible
completions for every negative core with 2<=w<=134 are checked.
"""

from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

import verify_book_two_negative_obstruction_v21 as core_reconstruction


def analytic_constants():
    # On assuming h <= 3r/7-1, subtract the increasing RHS
    # h^2+4rh+(delta+1)h from 2(delta-1)r^2.
    gap_coefficients = {
        2: (Fraction(5, 49), Fraction(25, 7), Fraction(2)),
        3: (Fraction(103, 49), Fraction(22, 7), Fraction(3)),
    }
    assert all(c > 0 for coefficients in gap_coefficients.values() for c in coefficients)
    type_I_negative = (Fraction(221, 49)+1)/(Fraction(100, 49)-2)
    assert type_I_negative == 135
    type_I_positive_with_L4 = {
        '4,3': Fraction(5)/(3-Fraction(17, 7)),
        '3,4': Fraction(9, 2)/(3-Fraction(17, 7)),
        '4,4': Fraction(5)/(4-Fraction(17, 7)),
    }
    assert type_I_positive_with_L4 == {
        '4,3': Fraction(35, 4), '3,4': Fraction(63, 8), '4,4': Fraction(35, 11)}
    type_II_negative = (Fraction(14, 3)-Fraction(1, 2))/(Fraction(17, 10)-Fraction(4, 3))
    type_II_positive_L3 = Fraction(4)/(2-Fraction(7, 5))
    assert type_II_negative == Fraction(125, 11) < 12
    assert type_II_positive_L3 == Fraction(20, 3) < 7
    return dict(
        growth_h_strict_lower_bound='3*r/7-1',
        growth_T_strict_lower_bound='10*r/7+1',
        type_I_negative_tau_strict_w_bound=[135, 1],
        type_I_positive_tau_with_L4_strict_w_bounds={
            k: [v.numerator, v.denominator] for k, v in type_I_positive_with_L4.items()},
        type_II_negative_tau_strict_w_bound=[125, 11],
        type_II_positive_tau_P1_L3_strict_w_bound=[20, 3],
        universal_proved_w_max=134)


def run():
    constants = analytic_constants()
    cores, reverse_count = core_reconstruction.negative_cores(134)
    records, double_nonempty, final_pairs, survivors = [], [], [], []
    total_neighbour_reverse = 0
    total_neighbours = 0
    for fixed in cores:
        left, count_left = core_reconstruction.neighbours(fixed, 3)
        right, count_right = core_reconstruction.neighbours(fixed, 4)
        total_neighbour_reverse += count_left+count_right
        total_neighbours += len(left)+len(right)
        record = dict(fixed=core_reconstruction.short_model(fixed),
                      neighbour_counts=[len(left), len(right)],
                      reverse_counts=[count_left, count_right],
                      neighbours_left=[core_reconstruction.short_model(m) for m in left],
                      neighbours_right=[core_reconstruction.short_model(m) for m in right])
        records.append(record)
        if left and right:
            double_nonempty.append(record)
        for a, b in product(left, right):
            nodes, residual = core_reconstruction.edge_data(a, b)
            result = dict(fixed=fixed['canonical'],
                          left=core_reconstruction.short_model(a),
                          right=core_reconstruction.short_model(b),
                          final_nodes=nodes, final_D_residual=residual)
            final_pairs.append(result)
            if min(nodes) >= 0 and residual == 0:
                survivors.append(result)
    assert len(cores) > 313
    assert len(double_nonempty) == 6
    assert len(final_pairs) == 11
    assert all(record['final_D_residual'] != 0 for record in final_pairs)
    assert not survivors
    proof_name = 'book_one_negative_sector_reduction_v21.tex'
    proof_path = next(p for p in (Path(__file__).with_name(proof_name),
                                  Path(__file__).parent.parent/'paper'/proof_name)
                      if p.is_file())
    return dict(
        status='PASS',
        mathematical_scope='The remaining one-negative book sectors reduce to type I with tau positive and (L1,L2)=(3,3), or type II with tau positive and (L1,L2)=(4,3). Every surviving hypothetical negative core has w>=135.',
        finite_certificate_scope='No book low triangle of any branch pattern contains a negative core with 2<=w<=134.',
        excluded_sectors=['type I, tau negative', 'type I, tau positive, at least one positive L=4',
                          'type II, tau negative', 'type II, tau positive, P1 has L=3'],
        retained_sectors=['type I, tau positive, positive L=(3,3)',
                          'type II, tau positive, positive L=(4,3)'],
        analytic_constants=constants,
        arbitrary_scale_or_denominator_cutoff=None,
        counts=dict(initial_reverse_parameters=reverse_count, initial_cores=len(cores),
                    initial_cores_with_w_at_most_50=sum(m['canonical'][3] <= 50 for m in cores),
                    by_w=dict(sorted(Counter(m['canonical'][3] for m in cores).items())),
                    all_neighbour_models=total_neighbours,
                    neighbour_reverse_parameters=total_neighbour_reverse,
                    with_two_nonempty_neighbour_sets=len(double_nonempty),
                    final_edge_pairs=len(final_pairs), survivors=len(survivors)),
        maximum_initial_high_denominator=max(max(m['q'].values()) for m in cores),
        initial_core_records=records,
        double_nonempty_records=double_nonempty,
        final_edge_certificates=final_pairs,
        reconstruction_dependency=Path(core_reconstruction.__file__).name,
        reconstruction_dependency_sha256=hashlib.sha256(Path(core_reconstruction.__file__).read_bytes()).hexdigest(),
        proof_file=proof_name,
        proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('book_one_negative_sector_reduction_verification_v21.json'))
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'counts', 'analytic_constants',
                                           'maximum_initial_high_denominator')}, ensure_ascii=False))
