#!/usr/bin/env python3
"""Independent stdlib audit of the four-ray path obstruction and sign classification.

The principal verifier is not imported or executed. Raw rows and five pair
equations are reconstructed as rational functions, and the sixth residual is
compared with a separately expanded positive polynomial certificate.
"""
from itertools import combinations, product
from math import gcd
from pathlib import Path
import argparse
import hashlib
import json

NAMES = ('a', 'b', 'c', 'B', 'C', 'q', 't', 's', 'r', 'L', 'D', 'h', 'K')
DIM = len(NAMES)
ZERO = (0,) * DIM


class Poly:
    def __init__(self, terms=None):
        self.terms = {e: c for e, c in (terms or {}).items() if c}
    @classmethod
    def cast(cls, x):
        return x if isinstance(x, cls) else cls({ZERO: x})
    @classmethod
    def var(cls, i):
        e = [0] * DIM; e[i] = 1
        return cls({tuple(e): 1})
    def __add__(self, other):
        ans = self.terms.copy()
        for e, c in Poly.cast(other).terms.items(): ans[e] = ans.get(e, 0) + c
        return Poly(ans)
    __radd__ = __add__
    def __neg__(self): return Poly({e: -c for e, c in self.terms.items()})
    def __sub__(self, other): return self + -Poly.cast(other)
    def __rsub__(self, other): return Poly.cast(other) - self
    def __mul__(self, other):
        ans = {}
        for e, a in self.terms.items():
            for f, b in Poly.cast(other).terms.items():
                g = tuple(x+y for x, y in zip(e, f)); ans[g] = ans.get(g, 0)+a*b
        return Poly(ans)
    __rmul__ = __mul__
    def __pow__(self, exponent):
        assert exponent >= 0
        ans = Poly.cast(1)
        for _ in range(exponent): ans = ans * self
        return ans
    def __bool__(self): return bool(self.terms)
    def substitute(self, mapping):
        ans = Poly()
        for e, c in self.terms.items():
            term = Poly.cast(c)
            for i, power in enumerate(e):
                if power: term = term * mapping.get(i, Poly.var(i)) ** power
            ans = ans + term
        return ans


class RF:
    def __init__(self, numerator, denominator=1):
        p, q = Poly.cast(numerator), Poly.cast(denominator)
        assert q
        if not p:
            self.p, self.q = Poly(), Poly.cast(1)
            return
        # Only cancel provable common integer and monomial factors. No symbolic
        # factorization library or external computer algebra is involved.
        common = 0
        for c in list(p.terms.values()) + list(q.terms.values()): common = gcd(common, abs(c))
        exponents = tuple(min(e[i] for e in list(p.terms)+list(q.terms)) for i in range(DIM))
        def reduce(v):
            return Poly({tuple(a-b for a,b in zip(e,exponents)): c//common
                         for e,c in v.terms.items()})
        self.p, self.q = reduce(p), reduce(q)
    @classmethod
    def cast(cls, x): return x if isinstance(x, cls) else cls(x)
    def __add__(self, other):
        v = RF.cast(other); return RF(self.p*v.q+v.p*self.q, self.q*v.q)
    __radd__ = __add__
    def __neg__(self): return RF(-self.p, self.q)
    def __sub__(self, other): return self + -RF.cast(other)
    def __rsub__(self, other): return RF.cast(other) - self
    def __mul__(self, other):
        v = RF.cast(other); return RF(self.p*v.p, self.q*v.q)
    __rmul__ = __mul__
    def __truediv__(self, other):
        v = RF.cast(other); assert v.p; return RF(self.p*v.q, self.q*v.p)
    def __rtruediv__(self, other): return RF.cast(other) / self
    def __bool__(self): return bool(self.p)


def main(proof, output):
    a,b,c,B,C,q,t,s0,r0,L0,D0,h0,K0 = map(Poly.var, range(DIM))
    s, r, L = b*B+1, c*C+1, B+c
    D, h, K = L+q, a*b-1, B*C-1
    T = (a+t)*s+q*h
    U = t*L+a*D+1
    W = a*C*s+h*(r+C*q)+a*q
    V = t*s*(r+C*q)+q*W
    names = []
    def eq(name, left, right=0):
        assert not (RF.cast(left)-right), name
        names.append(name)
    qq = [RF(t), RF(s,q), RF(q), RF(r,q)]
    big_A = (qq[0]*qq[1]-1)/a
    small_d = (qq[0]*qq[2]-1)/D
    small_e = qq[0]+a-small_d
    small_f = qq[1]+big_A+b
    big_F = (qq[1]*qq[3]-1)/small_f
    big_E = qq[3]+C-big_F
    raw = [[RF(0),RF(a),-small_d,-small_e],
           [big_A,RF(0),RF(b),-small_f],
           [-RF(D),RF(B),RF(0),RF(c)],
           [-big_E,-big_F,RF(C),RF(0)]]
    for i in range(4): eq('raw_row_'+str(i+1), sum(raw[i]), -qq[i])
    for i,j in combinations(range(4),2):
        if (i,j)==(0,3): continue
        eq('raw_pair_'+str(i+1)+str(j+1), raw[i][j]*raw[j][i], qq[i]*qq[j]-1)
    eq('raw_f_equals_T_over_aq', small_f, RF(T,a*q))
    eq('raw_e_equals_U_over_D', small_e, RF(U,D))
    eq('raw_E_equals_V_over_qT', big_E, RF(V,q*T))
    eq('raw_F_equals_a_sr_minus_q2_over_qT', big_F, RF(a*(s*r-q*q),q*T))
    residual = raw[0][3]*raw[3][0]-(qq[0]*qq[3]-1)
    obstruction = U*V-D*T*(t*r-q)
    eq('sixth_pair_original_residual', residual, RF(obstruction,q*D*T))
    eq('key_coefficient_identity', L*(r+C*q)-D*r, q*K)
    formal = (q*s0*K0*t*t
              +(a*q*C*s0*(L0+D0)+q*q*h0*K0+a*L0*q*q+s0*(r0+C*q)+D0*s0*q)*t
              +(a*D0+1)*q*(a*C*s0+h0*(r0+C*q)+a*q)+D0*q*(a*s0+q*h0))
    substituted = formal.substitute({7:s,8:r,9:L,10:D,11:h,12:K})
    eq('positive_certificate_from_original_sixth_pair', obstruction, substituted)
    assert all(coefficient > 0 for coefficient in formal.terms.values())
    positive_indices = {0,4,5,6,7,8,9,10}
    nonnegative_indices = {11,12}
    assert all(not exponent or i in positive_indices|nonnegative_indices
               for e in formal.terms for i,exponent in enumerate(e))
    strict_terms = [e for e in formal.terms if e[11]==e[12]==0]
    assert strict_terms
    # Explicit t*s*r survives h=K=0, including a=b=B=C=1.
    e = [0]*DIM
    for i in (6,7,8): e[i]=1
    assert formal.terms[tuple(e)] == 1
    eq('boundary_h_K_zero_still_positive_polynomial',
       formal.substitute({11:Poly.cast(0),12:Poly.cast(0)}),
       (a*q*C*s0*(L0+D0)+a*L0*q*q+s0*(r0+C*q)+D0*s0*q)*t
       +(a*D0+1)*q*(a*C*s0+a*q)+D0*q*a*s0)
    # Isolated-row calculation: a=qi,b=qh,c=ci,B=pih.
    eq('isolated_vertex_integer_gain_row_identity', a*(b-c)-c*(-a-B), a*b+c*B)
    # Midpoint weights on one matching edge; strict gaps equal positive rational.
    reverse = RF(t*q-1,a)
    lower, upper = RF(a,t), RF(q)/reverse
    midpoint = (lower+upper)/2
    eq('matching_weight_lower_gap', midpoint-lower, 1/(2*RF(t)*reverse))
    eq('matching_weight_upper_gap', upper-midpoint, 1/(2*RF(t)*reverse))

    vertices=range(4); edges=list(combinations(vertices,2)); graph_cases=[]
    for bits in product((0,1),repeat=6):
        graph={e for e,x in zip(edges,bits) if x}
        degrees=[sum(i in e for e in graph) for i in vertices]
        if max(degrees)==3: kind='positive whole row impossible'
        elif min(degrees)==0:
            kind='isolated vertex: integer gain argument forces triangle plus isolated vertex'
        else:
            ds=sorted(degrees)
            kind={ (1,1,1,1):'matching', (1,1,2,2):'P4 excluded by certificate',
                   (2,2,2,2):'C4 excluded by negative diagonal pair' }[tuple(ds)]
        graph_cases.append({'positive_edges':[list(e) for e in sorted(graph)],'degrees':degrees,'classification':kind})
    assert len(graph_cases)==64
    arrow_cases=[]
    for choices in product(*[[j for j in range(3) if j!=i] for i in range(3)]):
        cycles=[]
        for start in range(3):
            seen=[];v=start
            while v not in seen: seen.append(v);v=choices[v]
            cycle=seen[seen.index(v):]
            cycles.append(len(cycle))
        assert len(set(cycles))==1
        length=cycles[0]
        assert length in (2,3)
        if length==3:
            assert {tuple(sorted((i,choices[i]))) for i in range(3)} == {(0,1),(0,2),(1,2)}
        arrow_cases.append({'successors':choices,'cycle_length':length})
    assert sum(x['cycle_length']==3 for x in arrow_cases)==2
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    result={
        'version':'v25','status':'PASS','independent_audit':True,
        'principal_verifier_imported':False,'principal_verifier_executed':False,
        'stdlib_only':True,'bounded_parameter_scan':False,
        'checked_rational_polynomial_identities':len(names),'identity_names':names,
        'raw_row_identities':4,'raw_pair_identities_before_obstruction':5,
        'sixth_pair_residual':'[UV-DT(tr-q)]/(qDT)',
        'positive_certificate_monomials':len(formal.terms),
        'strictly_positive_monomials_independent_of_h_K':len(strict_terms),
        'boundary_h_equals_K_equals_zero':'strict t*s*r monomial survives',
        'nonzero_denominator_justification':'a,q,D,T>0 in the original path chart; no zero denominator stratum is discarded.',
        'all_64_sign_graphs':graph_cases,'all_8_isolated_successor_patterns':arrow_cases,
        'scope':'P4 is impossible for integer four-ray row/pair charts with all pair products positive. With positive basin weights the graph is a complete matching. No global gluing existence is inferred.',
        'proof_file':proof.name,'proof_sha256':sha(proof),
        'audit_file':Path(__file__).name,'audit_sha256':sha(Path(__file__)),
        'formal_proof_assistant':False,
    }
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','checked_rational_polynomial_identities',
                     'positive_certificate_monomials','strictly_positive_monomials_independent_of_h_K',
                     'principal_verifier_imported']},ensure_ascii=False))


if __name__=='__main__':
    here=Path(__file__).resolve().parent
    p=argparse.ArgumentParser()
    p.add_argument('--proof',type=Path,default=here.parent/'four_high'/'four_ray_matching_v25.tex')
    p.add_argument('--output',type=Path,default=here/'four_ray_matching_independent_audit_v25.json')
    a=p.parse_args();main(a.proof,a.output)
