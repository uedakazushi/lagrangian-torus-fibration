#!/usr/bin/env python3
"""Independent local-model-first audit of the all-negative book obstruction.

This imports the already retained v19 local model generator, never the new v20
reverse-type generator. It constructs all complete local models in the proved
w bounds, then tests the original low rows directly, before comparing records.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
import argparse
import hashlib
import json
import sys

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bundle',type=Path,default=Path(__file__).resolve().parents[2])
    ap.add_argument('--primary',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    bundle=args.bundle.resolve()
    helper=bundle/'research/book_low_triangle_completion_v19.py'
    sys.path.insert(0,str(helper.parent))
    from book_low_triangle_completion_v19 import negative_models, canonical
    models=list(negative_models(40))
    groups=[]
    for vertex,order,wbound in [(2,(0,1,3,4),16),(3,(0,1,4,2),40),(4,(1,0,3,2),17)]:
        group=[canonical(*m['canonical'],order=order,vertex=vertex)
               for m in models if m['canonical'][3]<=wbound]
        assert all(group)
        groups.append(group)

    def edge(left,right):
        i,j=left['vertex'],right['vertex']
        n=tuple(1-left['p'][j][k]-right['p'][i][k]
                for k in sorted(set(range(5))-{i,j}))
        assert sum(n)==5
        D=lambda m,k:-m['q'][k]-sum(m['p'][l][k] for l in m['q'] if l!=k)
        return n,D(left,j)+D(right,i)

    pairs=[]
    for first,second in product(groups[0],groups[1]):
        n,d=edge(first,second)
        if min(n)>=0:pairs.append((first,second,n,d))
    records=[]
    for first,second,n,d in pairs:
        for third in groups[2]:
            n2,d2=edge(second,third)
            n3,d3=edge(third,first)
            if min(n2+n3)<0:continue
            assert d!=0
            records.append((tuple(m['canonical'] for m in (first,second,third)),
                            (n,n2,n3),(d,d2,d3)))
    assert len(records)==len(set(records))==64
    primary=args.primary or bundle/'verification/book_all_negative_verification_v20.json'
    c=json.loads(primary.read_text())
    expected={(tuple(tuple(p) for p in x['canonical_models']),
               tuple(tuple(n) for n in x['node_numbers']),
               tuple(x['D_residuals'])) for x in c['D_certificates']}
    assert set(records)==expected
    assert len({(p[0],p[1],d[0]) for p,n,d in records})==26
    assert (Fraction(101,20)+Fraction(17,7))/(Fraction(17,10)**2-Fraction(17,7))==Fraction(5235,323)<17
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    report={'status':'PASS','method':'Enumerate complete local models first using the retained v19 generator, then test all three original low node rows and original D columns; do not import the primary v20 verifier.',
            'proved_w_bounds':[16,40,17], 'local_model_counts':list(map(len,groups)),
            'first_edge_node_compatible_pairs':len(pairs), 'all_three_edge_node_compatible_triples':len(records),
            'nonzero_first_D_residuals':len(records),'distinct_first_edge_pairs':26,
            'full_certificate_equality':True,'primary_generator_imported':False,
            'primary_sha256':sha(primary),'helper_sha256':sha(helper),'audit_script_sha256':sha(Path(__file__)),
            'survivors':0,'scale_or_denominator_cutoff':None}
    out=args.output or Path(__file__).with_name('book_all_negative_independent_audit_v20.json')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
