#!/usr/bin/env python3
"""Independent node-first reconstruction of four-exception K4 hub data.

No primary enumeration or local-completion routine is imported. All 21^4 node
matrices are considered. The ordinary forest flow is fixed by its divergence.
Exceptional denominators are eliminated by separate linear equations at their
large endpoints; mixed-sign equations, if present, are explicitly recorded as
unbounded, never truncated.
"""
from itertools import combinations, permutations, product
from pathlib import Path
from collections import Counter
import hashlib
import json

HERE=Path(__file__).resolve().parent
EDGES=tuple(combinations(range(4),2))
TRIPLES=tuple((a,b,5-a-b) for a in range(6) for b in range(6-a))
ROWS=[]
for i in range(4):
    js=[j for j in range(4) if i!=j]
    rows=[]
    for t in TRIPLES:
        row=[0]*4
        for j,n in zip(js,t):row[j]=n
        rows.append(tuple(row))
    ROWS.append(rows)

def compositions(total,count):
    if count==0:
        if total==0:yield ()
    elif count==1:
        if total>=1:yield (total,)
    else:
        for a in range(1,total-count+2):
            for rest in compositions(total-a,count-1):yield (a,)+rest

def ordinary_values(i,j,signed_flow,N):
    if signed_flow==0:return []
    sign=1 if signed_flow>0 else -1
    W=abs(signed_flow)
    result=[]
    for u in range(1,5):
        v=W-u
        if v<1 or u*v%2:continue
        rij=sign*u
        if (1-rij-N[i][j])*(1+rij-N[j][i])!=0:continue
        result.append((rij,sign*v,1+u*v))
    return result

def exception_choices(i,j,N):
    result=[]
    for unit,big in [(i,j),(j,i)]:
        nu,nb=N[unit][big],N[big][unit]
        if nu==0:
            result.append((unit,big,1,None))
        if nu==2:
            result.append((unit,big,-1,None))
        elif nb in (3,5):
            result.append((unit,big,-1,nb-1))
    return result

def solve_row(base,unknown):
    b=-1-base
    if b%2:return None
    if not unknown:return ([()],False) if b==0 else None
    signs=[s for _,s in unknown]
    if min(signs)<0<max(signs):
        # This is a complete feasibility test, with an explicit witness.
        witness=[2]*len(signs)
        residual=b-sum(s*m for s,m in zip(signs,witness))
        k=signs.index(1 if residual>=0 else -1)
        witness[k]+=abs(residual)
        assert sum(s*m for s,m in zip(signs,witness))==b
        return ([tuple(witness)],True)
    sign=signs[0]
    total=sign*b//2
    answers=[tuple(2*x for x in xs) for xs in compositions(total,len(signs))]
    return (answers,False) if answers else None

def original_check(R,N,ordinary_q,ordinary_X):
    V=[[0 if i==j else 1-R[i][j]-N[i][j] for j in range(4)] for i in range(4)]
    Q=[[1]*4 for _ in range(4)]
    X=[[0]*4 for _ in range(4)]
    for i,j in EDGES:
        if (i,j) in ordinary_q:
            q=ordinary_q[i,j]
            X[i][j]=ordinary_X[i,j]
            X[j][i]=-ordinary_X[i,j]
        else:
            q=1+R[i][j]*R[j][i]
            X[i][j]=R[j][i];X[j][i]=R[i][j]
        Q[i][j]=Q[j][i]=q
        assert q>1 and q%2==1
        assert R[i][j]*X[i][j]==R[j][i]*X[j][i]==q-1
        assert V[i][j]*V[j][i]==0
        assert (X[i][j]+X[j][i])%q==0
        nh=1-(X[i][j]+X[j][i])//q
        assert 0<=nh<=5
    for i in range(4):
        assert sum(R[i])==sum(V[i])==-1
        assert sum(N[i])==5 and all(n>=0 for n in N[i])
        assert sum(X[i])+sum(V[j][i] for j in range(4))==-2
    return V,Q,X

def bad_core_witness(R,Q,X):
    for i in range(4):
        for js in permutations([j for j in range(4) if i!=j]):
            rr=[R[i][j] for j in js]
            xx=[X[i][j] for j in js]
            qq=[Q[i][j] for j in js]
            if (rr,xx,qq)==([-4,1,2],[-1,2,1],[5,3,3]):
                s=[-q-x for q,x in zip(qq,xx)]
                Q12,Q13,Q23=qq[0]*qq[1]-1,qq[0]*qq[2]-1,qq[1]*qq[2]-1
                a=Q23-s[1]*s[2]
                b=s[1]*(s[2]*s[0]-Q13)+Q12*s[2]-Q23*s[0]
                c=-Q12*(s[2]*s[0]-Q13)
                assert (a,b,c)==(-12,-34,-28)
                assert 17**2-4*6*14==-47
                return {'core':i,'ray_order':list(js),'q':qq,'R':rr,'X':xx,
                        'primitive_polynomial':[6,17,14],'discriminant':-47}
    raise AssertionError(('no universal bad core',R,Q,X))

def run(shape):
    O=((0,1),(2,3)) if shape=='disjoint' else ((0,1),(0,2))
    E=[e for e in EDGES if e not in O]
    counts=Counter();survivors=[];keys=set();infinite=[]
    for N in product(*ROWS):
        counts['node_matrices']+=1
        d=[sum(N[j][i] for j in range(4))-5 for i in range(4)]
        if shape=='disjoint':
            if d[0]+d[1] or d[2]+d[3]:continue
            flows=(d[0],d[2])
        else:
            if d[3]!=0:continue
            flows=(-d[1],-d[2])
        counts['forest_component_balance']+=1
        opts=[ordinary_values(i,j,f,N) for (i,j),f in zip(O,flows)]
        if any(not t for t in opts):continue
        exopts=[exception_choices(i,j,N) for i,j in E]
        if any(not t for t in exopts):continue
        for oo in product(*opts):
            counts['ordinary_data_with_exception_options']+=1
            for ee in product(*exopts):
                counts['exception_orientation_sign_trials']+=1
                R=[[0]*4 for _ in range(4)]
                qs={};xs={}
                for (i,j),(rv,xv,q) in zip(O,oo):
                    R[i][j]=rv;R[j][i]=-rv;qs[i,j]=q;xs[i,j]=xv
                unknown=[[] for _ in range(4)]
                for unit,big,sign,M in ee:
                    R[unit][big]=sign
                    if M is None:unknown[big].append((unit,sign))
                    else:R[big][unit]=sign*M
                rowanswers=[solve_row(sum(R[i]),unknown[i]) for i in range(4)]
                if any(t is None for t in rowanswers):continue
                mixed=any(t[1] for t in rowanswers)
                for chosen in product(*(t[0] for t in rowanswers)):
                    RR=[row[:] for row in R]
                    for i in range(4):
                        for (j,sign),M in zip(unknown[i],chosen[i]):RR[i][j]=sign*M
                    V,Q,X=original_check(RR,N,qs,xs)
                    record={'R':RR,'N':[list(row) for row in N],'V':V,'Q':Q,'X':X}
                    if mixed:
                        infinite.append(record)
                    else:
                        key=tuple(x for row in RR for x in row)+tuple(x for row in N for x in row)+tuple(qs[e] for e in O)
                        assert key not in keys
                        keys.add(key);record['real_local_obstruction']=bad_core_witness(RR,Q,X)
                        survivors.append(record)
    assert counts['node_matrices']==21**4
    assert not infinite
    assert len(survivors)==(0 if shape=='disjoint' else 6)
    return {'ordinary_edges':[list(e) for e in O],'counts':dict(counts),'unbounded_surviving_families':len(infinite),'survivors':survivors}

def main():
    results={shape:run(shape) for shape in ['disjoint','adjacent']}
    # Only after completing the independent enumeration, compare certificates.
    primary_path=HERE.parent/'k4_four_exceptions_verification_v17.json'
    primary=json.loads(primary_path.read_text())
    comparison={}
    def key(record):
        return tuple(x for name in ('R','N','V','Q','X') for row in record[name] for x in row)
    for shape in ('disjoint','adjacent'):
        expected=[]
        for model in primary['ordinary_graph_normal_forms'][shape]['survivors']:
            R=model['R']
            for hub in model['hub_candidates']:
                Q=[[1]*4 for _ in range(4)]
                X=[[0]*4 for _ in range(4)]
                for i,j in EDGES:
                    q=hub['q'][str(i)+str(j)]
                    Q[i][j]=Q[j][i]=q
                    assert (q-1)%R[i][j]==(q-1)%R[j][i]==0
                    X[i][j]=(q-1)//R[i][j]
                    X[j][i]=(q-1)//R[j][i]
                expected.append(key({'R':R,'N':hub['N'],'V':hub['V'],'Q':Q,'X':X}))
        actual=[key(rec) for rec in results[shape]['survivors']]
        assert len(actual)==len(expected) and set(actual)==set(expected)
        comparison[shape]={'all_R_N_V_q_X_entries_identical':True,'candidates':len(actual)}
    result={'version':'v17','passed':True,'audit_kind':'Independent node-first, variable-elimination reconstruction of all four-exception K4 hub data',
            'arbitrary_denominator_cutoff':None,'unbounded_variables_truncated':False,
            'primary_enumerator_imported':False,'node_row_allocations':21,
            'ordinary_flow_bounds':'Derived exactly from node divergences and the forest; |R|<=4 is a proved bound.',
            'exception_variable_elimination':'Positive unit endpoint must have N=0. Negative unit endpoint N=2 leaves any positive even M; otherwise M=N_big-1 must be 2 or 4. Each free M enters only its big-end row. Mixed signs permit every even residual and are recorded as unbounded; same-sign rows use complete positive compositions.',
            'external_peer_review':False,'proof_assistant_formalization':False,
            'primary_comparison_performed_after_independent_reconstruction':comparison,
            'compared_primary_json_sha256':hashlib.sha256(primary_path.read_bytes()).hexdigest(),
            'audit_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'results':results}
    p=HERE/'k4_four_hub_independent_audit_v17.json'
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'counts':{s:results[s]['counts'] for s in results},'survivors':{s:len(results[s]['survivors']) for s in results},'file':str(p)}))

if __name__=='__main__':main()
