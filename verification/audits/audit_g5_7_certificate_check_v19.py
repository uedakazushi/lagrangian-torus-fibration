"""Independent algebraic recheck of G5_7's exported 212 hub obstructions.
Does not import the implementation being audited. No bounded denominator search.
"""
import json
import argparse
import hashlib
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
def audit(source_path):
    data=json.loads(source_path.read_text())
    counts=Counter()
    for cert in data['hub_D_certificates']:
        rec=data['partner_records'][cert['partner_record']]
        Q,t,m=rec['Q'],rec['t'],rec['m']
        R=rec['R_at_zero'][0]
        # D^0_4+D^4_0=0, and V_B0+V_C0+V_D0=-1+t.
        target=-2*Q+1-t
        alpha=F(0); beta=F(0); free_count=0
        for i,ty in enumerate(cert['center'],1):
            if i==m:
                assert ty['kind']=='low' and ty['q']==1
                beta+=F(Q-1,R[i])
            elif ty['kind']=='fixed':
                beta+=F(Q*ty['q']-1,R[i])
            else:
                assert ty['kind']=='progression'
                assert ty['step']>=2
                # Work in the actual denominator q, q>=3, not an enumeration.
                free_count+=1
                alpha+=F(Q,R[i]);beta-=F(1,R[i])
        assert free_count<=1
        ob=cert['obstruction']
        if free_count:
            assert alpha
            forced=(target-beta)/alpha
            assert forced<3
            assert forced==F(*ob['forced_q'])
            counts['entire_q_progression_excluded']+=1
        else:
            residual=beta-target
            assert residual
            assert residual==F(*ob['residual'])
            counts['fixed_q_residual_nonzero']+=1
    assert counts=={'entire_q_progression_excluded':71,'fixed_q_residual_nonzero':141}
    assert sum(r['multiplicity'] for r in data['hub_summary'])==212
    return {'status':'PASS','counts':dict(counts),
            'certificate_count':212,
            'source':str(source_path),
            'source_kind':'input certificate JSON',
            'source_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),
            'solver_source_sha256':data.get('source_sha256'),
            'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,help='G5_7 main verification certificate JSON')
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('g5_7_certificate_audit_v19.json'))
    args=parser.parse_args()
    result=audit(args.input)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
