#!/usr/bin/env python3
"""Exact checks for the nonzero low-D cycle of a book low triangle.

The general sign statements are proved in the TeX module. This script checks
the algebraic identity coefficientwise and independently completes the unique
negative-zero core. It imports no earlier completion generator. All 21 node
rows and all reverse data are retained, without a scale or denominator cutoff.
"""

from fractions import Fraction as Q
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import argparse
import hashlib
import json


def add(*polys):
    out = {}
    for poly in polys:
        for exponents, coefficient in poly.items():
            out[exponents] = out.get(exponents, 0)+coefficient
    return {k:v for k,v in out.items() if v}


def mul(a, b):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x+y for x,y in zip(ea, eb))
            out[e] = out.get(e, 0)+ca*cb
    return {k:v for k,v in out.items() if v}


def neg(p):
    return {e:-c for e,c in p.items()}


def identity_check():
    one = {(0,0,0,0):1}
    r = {(1,0,0,0):1}
    z = {(0,1,0,0):1}
    delta = {(0,0,1,0):1}
    S = {(0,0,0,1):1}
    rp, zp = add(r, one), add(z, one)
    # Multiply D_C=delta-(z+1)S/r+z(S+delta)/(r+1)
    # by r(r+1) and compare with (r+z+1)(r delta-S).
    lhs = add(mul(delta,mul(r,rp)), neg(mul(zp,mul(S,rp))), mul(z,mul(add(S,delta),r)))
    rhs = mul(add(r,z,one), add(mul(r,delta),neg(S)))
    assert lhs == rhs
    return {'identity': 'r(r+1) D_C=(r+z+1)(r delta-S) when s=z+1',
            'method': 'coefficientwise equality in Z[r,z,delta,S]',
            'nonzero_coefficients': len(lhs)}


def roots(coefficients):
    scale = 1
    for c in coefficients:
        scale = scale*c.denominator//gcd(scale,c.denominator)
    A,B,C = [int(c*scale) for c in coefficients]
    assert A != 0
    disc = B*B-4*A*C
    if disc < 0:
        return ()
    d = isqrt(disc)
    if d*d != disc:
        return ()
    return tuple(sorted({n//(2*A) for n in (-B-d,-B+d) if n%(2*A)==0}))


def matrix(r,s,z,S,T,order,vertex):
    if min(r,s,z,S,T) < 1 or (s*S)%r or (z*T)%(r+1):
        return None
    a,b = s*S+1,z*T+1
    if a%2 != 1 or b%2 != 1:
        return None
    L = T-S+1
    if L not in (1,3,4):
        return None
    if not (S==T<r or (S>r and r*T>(r+1)*S)):
        return None
    x,y=s*S//r,z*T//(r+1)
    U,V=a+x-s,b-y+z
    if min(U,V)<=0 or U*V!=a*b-1:
        return None
    P=((0,-U,x,-s),(-V,0,-y,z),(r,-r-1,0,0),(-S,T,-L,0))
    qs=(a,b,1,1)
    assert all(sum(P[i])==-qs[i] for i in range(4))
    assert all(P[i][j]*P[j][i]==qs[i]*qs[j]-1 for i in range(4) for j in range(i+1,4))
    weights=(Q(a),Q(b),Q(2*(a-1)+1,2*r),Q(2*z*T+1,2*T))
    assert all(weights[j]-Q(P[i][j],qs[i])*weights[i]>0
               for i in range(4) for j in range(4) if i!=j)
    p={u:{v:P[i][j] for j,v in enumerate(order)} for i,u in enumerate(order)}
    q=dict(zip(order,qs))
    D={u:-q[u]-sum(p[v][u] for v in order if v!=u) for u in order}
    return {'canonical':(r,s,z,S,T),'vertex':vertex,'order':order,'p':p,'q':q,'D':D}


def reconstruct_scales(r,S,T,low_type,target):
    # Recover z(s) from the column sum, then substitute into the high pair.
    # This uses direct matrix coefficients, not the old F,A,B,C formulas.
    if low_type=='C':
        za=Q((r+1)*S,r*T)
        zb=Q((r+1)*(target-(T-S)),T)
    else:
        za,zb=Q(1),Q(-target-1)
    u,v=Q(S)+Q(S,r)-1,Q(T)-Q(T,r+1)+1
    quad=(u*v-S*T)*za
    linear=(u*v-S*T)*zb+(u-S)+(v-T)*za
    constant=(v-T)*zb+1
    for s in roots((quad,linear,constant)):
        z=za*s+zb
        if s>0 and z.denominator==1 and z>0:
            yield s,int(z)


def reverse_data(row, remaining):
    """All reverse data, bounded by the fixed row and L<=4."""
    if row[0]*row[1]>=0 or row[remaining]>0:
        return
    if row[remaining]==0:
        A=0 if row[0]>0 else 1
        r=row[A]
        if row[1-A]!=-r-1:
            return
        for w in range(2,r):
            H=r-w
            if w*w<2*H*(H+1)<4*w*w:
                yield r,w,w,A,'C'
        for delta in (2,3):
            for S in range(r+1,r*delta):
                yield r,S,S+delta,A,'C'
    else:
        A=0 if row[0]<0 else 1
        S,T=-row[A],row[1-A]
        L=T-S+1
        if L not in (1,3,4) or row[remaining]!=-L:
            return
        if L==1:
            w=S
            if w<2:
                return
            for H in range(2,isqrt(2*w*w)+1):
                if w*w<2*H*(H+1)<4*w*w:
                    yield w+H,w,w,A,'D'
        else:
            for r in range(S//(L-1)+1,S):
                yield r,S,T,A,'D'


def key(m):
    return tuple(m['q'][i] for i in sorted(m['q']))+tuple(
        m['p'][i][j] for i in sorted(m['q']) for j in sorted(m['q']))


def edge(m,n):
    i,j=m['vertex'],n['vertex']
    nodes=tuple(1-m['p'][j][k]-n['p'][i][k] for k in sorted(set(range(5))-{i,j}))
    assert sum(nodes)==5
    return nodes,m['D'][j]+n['D'][i]


def neighbours(fixed,vertex):
    remaining=({2,3,4}-{fixed['vertex'],vertex}).pop()
    labels=(0,1,remaining)
    out={}
    rows=[]
    for n0 in range(6):
        for n1 in range(6-n0):
            nodes=(n0,n1,5-n0-n1)
            row={k:1-n-fixed['p'][vertex][k] for k,n in zip(labels,nodes)}
            data=list(reverse_data(row,remaining))
            result=[]
            for r,S,T,A,low_type in data:
                order=(A,1-A,fixed['vertex'],remaining) if low_type=='C' else (
                    A,1-A,remaining,fixed['vertex'])
                for s,z in reconstruct_scales(r,S,T,low_type,-fixed['D'][vertex]):
                    m=matrix(r,s,z,S,T,order,vertex)
                    if m is None:
                        continue
                    assert all(m['p'][fixed['vertex']][k]==row[k] for k in labels)
                    nn,d=edge(fixed,m)
                    assert nn==nodes and min(nn)>=0 and d==0
                    out[key(m)]=m
                    result.append({'canonical':m['canonical'],'order':m['order']})
            rows.append({'nodes':nodes,'row':row,'reverse_data':data,'surviving_scales':result})
    return list(out.values()),rows


def report(m):
    return {k:m[k] for k in ['canonical','order','vertex','q','p','D']}


def run():
    polynomial=identity_check()
    fixed=matrix(4,4,5,2,2,(0,1,3,4),2)
    assert (fixed['D'][3],fixed['D'][4])==(0,-2)
    left,left_rows=neighbours(fixed,3)
    right,right_rows=neighbours(fixed,4)
    assert len(left)==4 and len(right)==1
    expected_left={
        ((2,2,1,3,6),(0,1,4,2)),
        ((3,3,2,4,6),(0,1,4,2)),
        ((4,4,5,2,2),(1,0,2,4)),
        ((4,4,2,7,10),(1,0,2,4))}
    assert {(m['canonical'],m['order']) for m in left}==expected_left
    assert (right[0]['canonical'],right[0]['order'])==((2,2,1,3,6),(0,1,2,3))
    finals=[]
    for m,n in product(left,right):
        nodes,d=edge(m,n)
        assert d!=0
        finals.append({'left':report(m),'right':report(n),
                       'last_edge_nodes':nodes,'last_edge_D_residual':d})
    assert sorted(c['last_edge_D_residual'] for c in finals)==[-2,1,1,2]
    # A vertex has the incident pair (-t_previous,t_next). Once two negative
    # entries, negative-zero and zero-zero are excluded, only two cycles remain.
    sign_patterns=[]
    for t in product((-1,0,1),repeat=3):
        pairs=[(-t[(i-1)%3],t[i]) for i in range(3)]
        if any(x<0 and y<0 for x,y in pairs):
            continue
        if any(min(x,y)<0 and max(x,y)==0 for x,y in pairs):
            continue
        if any(x==y==0 for x,y in pairs):
            continue
        sign_patterns.append(t)
    assert sign_patterns==[(-1,-1,-1),(1,1,1)]
    return {'status':'PASS','polynomial_identity':polynomial,
        'scope':'General sign lemma is proved in the text; exact completion of the unique negative-zero core has no denominator cutoff.',
        'fixed':report(fixed),'neighbour_counts':{'3':4,'4':1},
        'all_node_row_certificates':{'3':left_rows,'4':right_rows},
        'last_edge_certificates':finals,'low_triangle_completions':0,
        'allowed_nonzero_flow_patterns':sign_patterns,
        'generator_imported':False,'scale_or_denominator_cutoff':None,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    result=run()
    out=args.output or Path(__file__).with_name('book_low_D_cycle_verification_v20.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','neighbour_counts',
          'low_triangle_completions','allowed_nonzero_flow_patterns']},ensure_ascii=False))


if __name__=='__main__':
    main()
