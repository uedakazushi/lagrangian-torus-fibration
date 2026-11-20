"""Run the five v25 checks and five independent audits (Python standard library)."""
from pathlib import Path
import subprocess
import sys
import json

root = Path(__file__).resolve().parents[1]
out = root / 'build/migration-checks'
out.mkdir(parents=True, exist_ok=True)
checks = [
    ('four-ray', 'verify_four_ray_matching_v25.py', '--source', 'four_ray_matching_v25.tex'),
    ('five-node', 'verify_g514_five_node_v25.py', '--proof', 'g514_five_node_exclusion_v25.tex'),
    ('central', 'verify_g514_central_matching_v25.py', '--proof', 'g514_central_matching_v25.tex'),
    ('axis', 'verify_high_d_axis_endpoints_v25.py', '--proof', 'high_d_axis_endpoints_v25.tex'),
    ('divisor', 'verify_degenerate_divisor_v25.py', '--proof', 'degenerate_divisor_reduction_v25.tex'),
    ('audit-four-ray', 'audits/audit_four_ray_matching_independent_v25.py', '--proof', 'four_ray_matching_v25.tex'),
    ('audit-five-node', 'audits/audit_g514_five_node_independent_v25.py', '--source', 'g514_five_node_exclusion_v25.tex'),
    ('audit-central', 'audits/audit_g514_central_matching_independent_v25.py', '--source', 'g514_central_matching_v25.tex'),
    ('audit-axis', 'audits/audit_axis_endpoints_independent_v25.py', '--root', None),
    ('audit-divisor', 'audits/audit_degenerate_divisor_v25.py', '--proof', 'degenerate_divisor_reduction_v25.tex'),
]
summary = []
for name, script, flag, proof in checks:
    args = [sys.executable, 'verification/' + script, flag, 'papers/sections/paper/' + proof if proof else '.']
    if name == 'audit-divisor':
        args += ['--primary-results', str(out / 'divisor.json')]
    args += ['--output', str(out / (name + '.json'))]
    with (out / (name + '.log')).open('w') as log:
        result = subprocess.run(args, cwd=root, stdout=log, stderr=subprocess.STDOUT)
    summary.append({'name': name, 'exit_code': result.returncode})
    print(name, result.returncode, flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
