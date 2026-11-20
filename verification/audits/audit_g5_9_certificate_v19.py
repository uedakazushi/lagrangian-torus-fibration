#!/usr/bin/env python3
"""Independent reconstruction of the G5_9 final linear certificates.

Reads the original certificate, but imports none of the generating verifier.
Reconstructs leaf rows and all affine D equations from their definitions.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('certificate',type=Path,help='G5_9 JSON certificate to audit')
parser.add_argument('--output',type=Path,
                    default=Path(__file__).with_name('audit_g5_9_certificate_v19.json'))
args=parser.parse_args()
source_bytes=args.certificate.read_bytes()
data=json.loads(source_bytes)
cases=data['stage1']['cases']
count=0
for cert in data['stage2']['linear_certificates']:
    case=cases[cert['case_id']]
    h,t,Q=case['h'],case['t'],case['Q']
    z=case['z'][0]
    assert z==case['z'][1]
    c,d=(z,0) if case['vr']==2 else (0,z)
    u,v=t*h,t*(h+1)
    V=((0,1-Q,-h-1,h),(-1,0,0,0),(-u,u-1-c,0,c),(v,-v-1-d,d,0))
    ell=(Q,1,1,1)
    N=case['N']
    R=[[0 if i==j else ell[i]*(1-N[i][j])-V[i][j]
        for j in range(4)] for i in range(4)]
    variables=[tuple(p) for p in cert['variables']]
    types={tuple(map(int,k.strip('()').split(','))):v
           for k,v in cert['denominator_types'].items()}
    T=case['T']
    E,F=[i for i in (1,2,3) if i!=T]
    xe,xf=cert['low_X']
    assert R[E][F]<=0 and R[F][E]<=0
    assert xe in ({0} if R[E][F]<0 else {-1,-3,-4})
    assert xf in ({0} if R[F][E]<0 else {-1,-3,-4})
    assert xe+xf>=-4
    def residual(values):
        X={(E,F):Fraction(xe),(F,E):Fraction(xf)}
        for pair,ty in types.items():
            q=ty['q'] if ty['kind']=='fixed' else 1+ty['step']*values[variables.index(pair)]
            i,j=pair
            X[i,j]=Fraction(ell[i]*q-1,R[i][j])
            X[j,i]=Fraction(ell[j]*q-1,R[j][i])
        return [sum(X[i,j] for j in range(4) if j!=i)
                +sum(V[j][i] for j in range(4) if j!=i)+2*ell[i]
                for i in range(4)]
    n=len(variables)
    constant=residual([0]*n)
    columns=[]
    for j in range(n):
        e=[0]*n;e[j]=1
        columns.append([a-b for a,b in zip(residual(e),constant)])
    equations=[[columns[j][i] for j in range(n)]+[-constant[i]] for i in range(4)]
    assert equations==[list(map(Fraction,row)) for row in cert['equations']]
    w=list(map(Fraction,cert['weights']))
    combined=[sum(w[i]*equations[i][j] for i in range(4)) for j in range(n+1)]
    assert combined==list(map(Fraction,cert['combined_row']))
    if cert['reason']=='inconsistent':
        assert all(x==0 for x in combined[:-1]) and combined[-1]!=0
    else:
        assert all(x>=0 for x in combined[:-1]) and combined[-1]<sum(combined[:-1])
    count+=1

halflines=0
for cert in data['stage2']['halfline_certificates']:
    case=cases[cert['case_id']]
    assert case['T']==2 and case['vr']==3
    # The variable d changes only row3, so these exact rows persist on the
    # entire parity halfline. Their same-negative reverse pair forces q12=3.
    assert case['R0'][1]==[1,0,-2,0]
    assert case['R0'][2][1]==-1
    assert case['z'][0] is None
    assert cert['canonical_b']==3
    halflines+=1

output=dict(status='PASS',independently_reconstructed_D_certificates=count,
            halfline_canonical_b3_certificates=halflines,
            source=args.certificate.name,
            source_sha256=hashlib.sha256(source_bytes).hexdigest(),
            auditor_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            generator_imported=False)
args.output.write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output))
