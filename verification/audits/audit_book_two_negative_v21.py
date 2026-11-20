#!/usr/bin/env python3
"""Independent v21 certificate audit using only the unchanged v19 generator.

The v21 primary implementation is never imported. All 313 initial cores,
both complete neighbour sets of every core, and all final-edge residuals are
recomputed from the older integer-coefficient quadratic reconstruction.
"""
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys

here = Path(__file__).resolve()
root = here.parents[2]
if not (root/'research/book_low_triangle_completion_v19.py').is_file():
    root = root/'deliverables/general_type_surface_fibration_v21'
sys.path.insert(0, str(root/'research'))
from book_low_triangle_completion_v19 import negative_models, neighbours, low_edge

certificate_path = root/'verification/book_two_negative_obstruction_verification_v21.json'
certificate = json.loads(certificate_path.read_text())
assert certificate['status'] == 'PASS'
assert certificate['analytic_constants']['universal_w_max'] == 50


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def short_model(model):
    # JSON normalization converts the integer label keys to strings.
    return json.loads(json.dumps({key: model[key] for key in
                                 ('canonical', 'order', 'vertex', 'q', 'D')}))


cores = list(negative_models(50))
records = {tuple(record['fixed']['canonical']): record
           for record in certificate['initial_core_records']}
assert len(records) == len(cores) == 313
assert set(records) == {model['canonical'] for model in cores}
computed_final, neighbour_total, double_nonempty = [], 0, 0
for core in cores:
    record = records[core['canonical']]
    assert short_model(core) == record['fixed']
    left, right = neighbours(core, 3), neighbours(core, 4)
    assert [len(left), len(right)] == record['neighbour_counts']
    for side, expected_name in [(left, 'neighbours_left'), (right, 'neighbours_right')]:
        assert {canonical_json(short_model(model)) for model in side} == {
            canonical_json(model) for model in record[expected_name]}
    neighbour_total += len(left)+len(right)
    double_nonempty += bool(left and right)
    for a, b in product(left, right):
        nodes = [1-a['p'][4][k]-b['p'][3][k] for k in (0, 1, 2)]
        residual = a['D'][4]+b['D'][3]
        assert sum(nodes) == 5
        assert residual != 0
        assert low_edge(a, b) is None
        computed_final.append(dict(fixed=list(core['canonical']),
                                   left=short_model(a), right=short_model(b),
                                   final_nodes=nodes, final_D_residual=residual))
assert double_nonempty == 6 and len(computed_final) == 11
assert {canonical_json(model) for model in computed_final} == {
    canonical_json(model) for model in certificate['final_edge_certificates']}
primary = root/'verification/verify_book_two_negative_obstruction_v21.py'
assert sha256(primary.read_bytes()).hexdigest() == certificate['source_sha256']
proof = root/'paper/book_two_negative_obstruction_v21.tex'
if 'proof_sha256' in certificate:
    assert sha256(proof.read_bytes()).hexdigest() == certificate['proof_sha256']

report = dict(status='PASS', version='v21',
              method='Recomputed with the unchanged v19 generator; v21 primary code not imported.',
              initial_cores=len(cores), checked_neighbour_sets=2*len(cores),
              total_neighbours=neighbour_total,
              double_nonempty_cores=double_nonempty, final_pairs=len(computed_final),
              final_D_residuals=sorted(x['final_D_residual'] for x in computed_final),
              arbitrary_scale_or_denominator_cutoff=None,
              all_complete_neighbour_sets_equal=True,
              external_peer_review=False, proof_assistant_formalization=False,
              audit_script_sha256=sha256(here.read_bytes()).hexdigest(),
              certificate_sha256=sha256(certificate_path.read_bytes()).hexdigest(),
              previous_generator_sha256=sha256((root/'research/book_low_triangle_completion_v19.py').read_bytes()).hexdigest())
output = here.with_name('book_two_negative_independent_audit_v21.json')
output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report, ensure_ascii=False))
