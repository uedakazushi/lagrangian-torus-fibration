#!/usr/bin/env python3
"""Exact v12 checks for proved Schur identities and a rational counterexample.
No assertion of the unresolved integral three-high sign principle is made.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[2]

def check_model(q,p,w=None):
    assert all(sum(p[i])==-q[i] for i in range(4))
    assert all(p[i][j]*p[j][i]==q[i]*q[j]-1 for i in range(4) for j in range(i+1,4))
    D=[-q[i]-sum(p[j][i] for j in range(4)) for i in range(4)]
    assert sum(D)==0
    if w is not None:
        assert all(w[j]-w[i]*p[i][j]/q[i]>0 for i in range(4) for j in range(4) if i!=j)
    lo=q.index(1);hi=[i for i in range(4) if i!=lo]
    r=[p[lo][i] for i in hi];x=[p[i][lo] for i in hi]
    B=[[(q[i] if i==j else p[i][j])-p[i][lo]*p[lo][j] for j in hi] for i in hi]
    assert sum(r)==-1
    assert all(B[i][i]==1 and sum(B[i])==0 for i in range(3))
    assert all(q[hi[i]]==1+r[i]*x[i] for i in range(3))
    assert all(x[i]*(r[i]-B[j][i]*r[j])+x[j]*(r[j]-B[i][j]*r[i])==B[i][j]*B[j][i] for i in range(3) for j in range(i+1,3))
    assert D[lo]==-1-sum(x)
    assert all(D[hi[i]]==-sum(B[j][i] for j in range(3))+r[i]*D[lo] for i in range(3))
    return D,B

q=[F(79,25),F(128,25),F(274,25),F(1)]
p=[[F(x) for x in row] for row in [[0,F(179,25),F(-231,25),F(-27,25)],[F(53,25),0,F(-259,50),F(-103,50)],[F(-91,25),F(-266,25),0,F(83,25)],[-2,-2,3,0]]]
w=[F(1),F(7,3),F(13,4),F(1)]
D,B=check_model(q,p,w)
assert D==[F(9,25),F(9,25),F(23,50),F(-59,50)]
assert B==[[1,5,-6],[-2,1,1],[3,-4,1]]
gaps=[w[j]-w[i]*p[i][j]/q[i] for i,j in [(0,1),(1,0),(2,3),(3,2)]]
assert gaps==[F(16,237),F(13,384),F(17,1096),F(1,4)]

catalog_path=Path(__file__).with_name('quintic_denominators_verification_v10.json')
if not catalog_path.exists():
    catalog_path=ROOT/'v10_work/arithmetic/quintic_denominators_verification_v10.json'
records=json.loads(catalog_path.read_text())['catalog_models']
checked=0;nonzero_determinants=0;high_all_nonnegative=0
for m in records:
    if m['kind']!='complete_fixed_q_positive_model' or sum(x>1 for x in m['q'])!=3:continue
    qq=list(map(F,m['q']));pp=[list(map(F,row)) for row in m['p']]
    DD,BB=check_model(qq,pp,[F(x) for x in m['weights']])
    assert DD==m['D'];checked+=1
    lo=qq.index(1);c=next(i for i in range(4) if i!=lo and pp[lo][i]>0)
    a,b=[i for i in range(4) if i not in (lo,c)]
    assert all(sum(pp[i][j]>0 for j in range(4) if i!=j)==1 for i in range(4))
    s,t=-pp[lo][a],-pp[lo][b];S,T=-pp[a][lo],-pp[b][lo];U=pp[c][lo]
    k=s*U+pp[c][a]
    if k<0:
        a,b=b,a;s,t=t,s;S,T=T,S;k=s*U+pp[c][a]
    u=s+t-1;al=pp[a][b]-S*t;be=pp[b][a]-T*s
    AA=s*al-t;BB=t*be-s;CC=s+u*k
    assert k>=0 and al>=1 and AA>=0
    assert BB*S+AA*T==-al*be
    assert -CC*S+(AA+1)*U==k*(al+1)
    assert (CC-1)*T+(BB+1)*U==-(be+1)*(k+1)
    d=U+1-S-T
    assert [DD[a],DD[b],DD[c]]==[s*d-be-k-1,t*d-al+k,al+be+1-u*d]
    de=-BB*(AA+1)*(CC-1)+AA*CC*(BB+1)
    if de:nonzero_determinants+=1
    if min(DD[a],DD[b],DD[c])>=0:high_all_nonnegative+=1
assert checked==352 and nonzero_determinants==352 and high_all_nonnegative==0

out={'version':'v12','passed':True,'claims_checked':['General unit-diagonal Schur identities on all 352 three-high catalog models','Conditional matching linear system and defect identities on those models','Exact rational counterexample to all-high-positive exclusion after removing integrality of q and numerators'],
     'rational_counterexample':{'q':list(map(str,q)),'p':[[str(x) for x in row] for row in p],'weights':list(map(str,w)),'D':list(map(str,D)),'schur_B':[[str(x) for x in row] for row in B],'positive_edge_area_gaps':list(map(str,gaps))},
     'catalog_scope':{'source':str(catalog_path),'source_sha256':hashlib.sha256(catalog_path.read_bytes()).hexdigest(),'q_bound':101,'three_high_models':checked,'matching_models':checked,'nonzero_linear_system_determinants':nonzero_determinants,'all_high_D_nonnegative_models':high_all_nonnegative},
     'limitations':['Does not prove that arbitrary positive integral models have matching signs.','Does not prove either integral three-high sign conjecture.','The counterexample has rational nonintegral q and rational nonintegral numerators; it is not an integral geometric chart.'],
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
output=Path(__file__).with_name('three_high_schur_verification_v12.json')
output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'passed':True,'catalog_models_checked':checked,'output':str(output)},ensure_ascii=False))
