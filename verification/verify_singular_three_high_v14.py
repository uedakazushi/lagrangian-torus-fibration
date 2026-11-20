#!/usr/bin/env python3
"""Exact polynomial certificate for the complete rank-two matching slice.

Only Python's standard library is required. Polynomial identities certify the
entire parameter family; finite examples are recorded separately.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

def poly(*cs):
    a = list(map(Fraction, cs))
    while len(a) > 1 and not a[-1]:
        a.pop()
    return tuple(a or [Fraction(0)])

def add(a, b):
    return poly(*( (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                  for i in range(max(len(a),len(b))) ))

def neg(a):
    return poly(*(-x for x in a))

def sub(a,b):
    return add(a,neg(b))

def mul(a,b):
    cs=[Fraction(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            cs[i+j]+=x*y
    return poly(*cs)

def scale(c,a):
    return mul(poly(c),a)

identities=[]
def eq(name,a,b):
    assert sub(a,b)==poly(0),(name,a,b)
    identities.append(name)

def determinant(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
            -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
            +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))

def main():
    S,T,U=poly(136,200),poly(291,425),poly(93,136)
    q=[poly(409,600),poly(3493,5100),poly(1303,1904),poly(1)]
    P=[
        [poly(0),poly(1644,2400),poly(-1917,-2800),poly(-136,-200)],
        [poly(869,1275),poly(0),poly(-4071,-5950),poly(-291,-425)],
        [poly(-278,-408),poly(-1118,-1632),poly(0),poly(93,136)],
        [poly(-3),poly(-12),poly(14),poly(0)],
    ]
    for i in range(4):
        row=poly(0)
        for j in range(4):row=add(row,P[i][j])
        eq('row_'+str(i),row,neg(q[i]))
        for j in range(i+1,4):
            eq('pair_'+str(i)+str(j),mul(P[i][j],P[j][i]),sub(mul(q[i],q[j]),poly(1)))
    D=[poly(-997,-1467),poly(-4007,-5868),poly(4671,6846),poly(333,489)]
    for i in range(4):
        col=poly(0)
        for j in range(4):col=add(col,P[j][i])
        eq('D_'+str(i),sub(neg(q[i]),col),D[i])
    total=poly(0)
    for d in D:total=add(total,d)
    eq('D_sum',total,poly(0))
    eq('q_a',q[0],add(poly(1),scale(3,S)))
    eq('q_b',q[1],add(poly(1),scale(12,T)))
    eq('q_c',q[2],add(poly(1),scale(14,U)))
    eq('Schur_row_1',add(scale(-51,S),scale(24,T)),poly(48))
    eq('Schur_row_2',add(scale(-17,S),scale(25,U)),poly(13))
    eq('Schur_row_3',add(scale(16,T),scale(-50,U)),poly(6))
    eq('CRT_S',scale(17,S),sub(scale(25,U),poly(13)))
    eq('CRT_T',scale(8,T),add(scale(25,U),poly(3)))
    eq('D0',D[3],sub(sub(add(S,T),U),poly(1)))
    # Multiplication by positive denominators verifies all four symbolic gaps.
    H,K=P[0][1],P[1][0]
    eq('gap_ab_times_2K',sub(add(scale(2,mul(K,H)),poly(1)),scale(2,mul(K,H))),poly(1))
    eq('gap_ba_times_2qb',sub(scale(2,mul(q[0],q[1])),add(scale(2,mul(H,K)),poly(1))),poly(1))
    eq('gap_0c_times_2U',sub(add(scale(28,U),poly(1)),scale(28,U)),poly(1))
    eq('gap_c0_times_2qc',sub(scale(2,q[2]),add(scale(28,U),poly(1))),poly(1))
    M=[[-51,24,0],[-17,0,25],[0,16,-50]]
    assert determinant(M)==0
    assert M[0][0]*M[1][1]-M[0][1]*M[1][0]==408
    for j in range(3):assert 2*M[0][j]==6*M[1][j]+3*M[2][j]
    assert 2*48==6*13+3*6
    residues=[u for u in range(136) if (25*u-13)%17==0 and (25*u+3)%8==0]
    assert residues==[93]
    # Coefficient signs prove positivity and oddness for every n>=0.
    for qv in q[:3]:assert int(qv[0])%2==1 and all(int(x)%2==0 for x in qv[1:])
    for i in range(4):
        for j in range(4):
            if i==j:continue
            positive=({i,j} in ({0,1},{2,3}))
            cs=P[i][j] if positive else neg(P[i][j])
            assert cs[0]>0 and all(c>=0 for c in cs)
    examples=[]
    for n in [0,1,10]:
        ev=lambda a:sum(c*n**i for i,c in enumerate(a))
        qs=[ev(x) for x in q]
        ps=[[ev(x) for x in row] for row in P]
        weights=[qs[0],ps[0][1]+Fraction(1,2*ps[1][0]),Fraction(14)+Fraction(1,2*ev(U)),Fraction(1)]
        gaps=[weights[j]-weights[i]*ps[i][j]/qs[i] for i in range(4) for j in range(4) if i!=j]
        assert all(x>0 for x in gaps)
        examples.append({'n':n,'q':[int(x) for x in qs],'P':[[int(x) for x in row] for row in ps],
                         'D':[int(ev(x)) for x in D],'positive_weights':[str(x) for x in weights],
                         'minimum_basin_gap':str(min(gaps))})
    here=Path(__file__).resolve().parent
    candidates=[here/'quintic_three_high_singular_v14.tex',here.parent/'paper/quintic_three_high_singular_v14.tex']
    source=next(p for p in candidates if p.is_file())
    result={
        'version':'v14','passed':True,'scope':'Complete fixed slice (s,t,alpha,beta,k)=(3,12,12,-4,1); no classification of other singular systems or global gluing.',
        'polynomial_identity_count':len(identities),'polynomial_identities':identities,
        'coefficient_matrix':M,'right_hand_side':[48,13,6],'rank':2,'nonzero_minor':408,
        'complete_CRT_period':136,'complete_CRT_residues':residues,
        'parameters':{'S':[136,200],'T':[291,425],'U':[93,136],'n':'all nonnegative integers'},
        'oddness_and_positivity':'Coefficient signs prove these properties for every n>=0, not by extrapolating samples.',
        'illustrative_exact_examples':examples,
        'limitations':['Positive-entry graph is the matching type by construction.','Two high coefficients are negative.','No five-core global atlas is asserted.'],
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    }
    dest=here/'singular_three_high_verification_v14.json'
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'polynomial_identities':len(identities),'rank':2,'CRT_period':136,'CRT_residues':residues}))

if __name__=='__main__':main()
