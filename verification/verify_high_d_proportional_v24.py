#!/usr/bin/env python3
"""Exact coefficient certificates and complete fixed-(s,z) proportional-axis reconstruction.

Standard library only. No producer or inherited verifier imports. Infinite-domain
claims use full integer polynomial coefficients, not bounded numerical scans.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import isqrt
from pathlib import Path
import argparse
import json


class Poly:
    def __init__(self, n, terms=None):
        self.n = n
        self.terms = {tuple(e): c for e, c in (terms or {}).items() if c}
        assert all(len(e) == n and all(k >= 0 for k in e) for e in self.terms)
        assert all(isinstance(c, int) for c in self.terms.values())

    @classmethod
    def const(cls, n, c):
        return cls(n, {(0,)*n: c})

    @classmethod
    def variables(cls, n):
        return tuple(cls(n, {tuple(int(i == j) for i in range(n)): 1}) for j in range(n))

    def coerce(self, other):
        if isinstance(other, int):
            return Poly.const(self.n, other)
        assert other.n == self.n
        return other

    def __add__(self, other):
        other = self.coerce(other)
        d = defaultdict(int, self.terms)
        for e, c in other.terms.items():
            d[e] += c
        return Poly(self.n, d)
    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n, {e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        other = self.coerce(other)
        d = defaultdict(int)
        for e, c in self.terms.items():
            for f, a in other.terms.items():
                d[tuple(x+y for x, y in zip(e, f))] += c*a
        return Poly(self.n, d)
    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        out, base = Poly.const(self.n, 1), self
        while exponent:
            if exponent & 1:
                out = out * base
            base = base * base
            exponent //= 2
        return out

    def substitute(self, values):
        values = [self.coerce(v) for v in values]
        assert len(values) == self.n
        out = Poly.const(self.n, 0)
        cache = [{0: Poly.const(self.n, 1)} for _ in values]
        for e, c in self.terms.items():
            term = Poly.const(self.n, c)
            for i, exponent in enumerate(e):
                if exponent not in cache[i]:
                    cache[i][exponent] = values[i]**exponent
                term = term * cache[i][exponent]
            out = out + term
        return out

    def evaluate(self, values):
        return sum(c * product_int(v**e for v,e in zip(values,exp)) for exp,c in self.terms.items())

    def coefficient(self, variable, degree):
        out = {}
        for e, c in self.terms.items():
            if e[variable] == degree:
                f = list(e); f[variable] = 0
                out[tuple(f)] = c
        return Poly(self.n, out)

    def coefficients_record(self):
        return [{'exponents': list(e), 'coefficient': c} for e, c in sorted(self.terms.items())]


def product_int(values):
    result = 1
    for value in values:
        result *= value
    return result


def identity(name, left, right, out):
    diff = left-right
    assert not diff.terms, (name, diff.terms)
    out.append({'name': name, 'status': 'PASS', 'left_terms': len(left.terms),
                'right_terms': len(right.terms), 'difference_terms': 0})


def positive_certificate(name, poly, variables):
    assert poly.terms
    assert all(c > 0 for c in poly.terms.values()), name
    constant = poly.terms.get((0,)*poly.n, 0)
    assert constant > 0, name
    records = poly.coefficients_record()
    groups = {}
    for i, var in enumerate(variables):
        grouping = {}
        for exp,c in poly.terms.items():
            d = grouping.setdefault(str(exp[i]), {'count': 0, 'minimum_coefficient': c})
            d['count'] += 1; d['minimum_coefficient'] = min(d['minimum_coefficient'], c)
        groups[var] = grouping
    return {'name': name, 'status': 'PASS', 'variables': variables,
            'nonzero_coefficient_count': len(records), 'constant': constant,
            'all_nonzero_coefficients_positive': True, 'degree_groups': groups,
            'coefficients_sha256': sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),
            'full_coefficients': records}


def axis_polynomial():
    s,b,z,n = Poly.variables(4)
    F=b-1+s*z; m=F*F+F+1; K=s*(F-1)-z+1; V=m*n+K
    P=-b*V*V+(b+1)*(s*s*z-2*s-b*z)*V+(b+1)**2*F*(s*s-b)
    P=P+n*(s*m*(b+1)**2+(F*F+b)*V*(b+1))
    return P


def symbolic_certificates():
    checks=[]
    h,x,w,z = Poly.variables(4)
    s=h+x; j=h+w; q=s*h-1
    D=x*(h+j)+h*(z-1); L=h*h+s*D
    C=D*q+h*h*(h-3)-h*w
    A=h*C-h*h*w+w*(h+j)*L
    N=-A*(s*h*h*w-C)+2*s*j*h**3*w*w+C*s*j*j*h*w
    # Independent clearing of the original residual, expanded first in b.
    A0=(h+j)*L-h*h
    r0=A0*s*h*h-2*s*j*h**3
    r1=s*h**4-A0*h-s*j*j*h*h
    r2=-h**3
    cleared=(h*w)**2*r0+(h*w)*C*r1+C*C*r2
    identity('original_residual_after_linear_Q_elimination',cleared,-h*h*N,checks)
    cert_x2=positive_certificate('x>=2, h>=1, w>=1, z>=0',
                                 N.substitute([h+1,x+2,w+1,z]),['h_minus_1','x_minus_2','w_minus_1','z'])

    h,z,k=Poly.variables(3)
    q=h*h+h-1; D=h*k+1; C=q*z+2*h*h-2*h-1
    s=h+1; b=h+k; Lnum=h*D+s*(C+(z+1)*D)
    alpha_num=(b-1)*D*D+(C+2*D)*Lnum
    R=alpha_num*(s*h-b)-2*s*(C+D)*h*D-b*s*h*(C+D)**2
    R0=h*h*(h+1)*q*z*z+h*(4*h**4+h**3-6*h*h+2)*z+h*h*(4*h**3-6*h*h+3)
    R1=-(2*h*h*(h**3+2*h*h-1)*z*z+h*(7*h**4-10*h*h+h+2)*z+6*h**4*(h-2)+3*h**3+3*h*h-1)
    R2=-(h*(h**3+2*h*h-1)*z*z+h*h*(8*h*h+7*h-2)*z+10*h**4-6*h**3-h+1)
    R3=-h*(2*h*(h+1)*z+6*h*h+h+2); R4=-h*h
    identity('x_one_residual_coefficients',R,R0+R1*k+R2*k*k+R3*k**3+R4*k**4,checks)
    identity('x_one_at_k_zero',R.substitute([h,z,0]),R0,checks)
    at_one=-h*(h+1)**2*(q*z*z+h*(3*h+1)*z+2*h*h+1)
    identity('x_one_at_k_one',R.substitute([h,z,1]),at_one,checks)
    h_one_positive=k**4+13*k**3+37*k*k+38*k+12+(4*k**3+25*k*k+38*k+16)*z+(2*k*k+8*k+4)*z*z
    identity('x_one_h_one_all_k_ge_one',-R.substitute([1,z,k+1]),h_one_positive,checks)
    small_certificates=[]
    small_certificates.append(positive_certificate('x=1, h>=2, k=0',R0.substitute([h+2,z,k]),['h_minus_2','z','unused']))
    for i, coefficient in enumerate([R1,R2,R3,R4],1):
        small_certificates.append(positive_certificate('negative k coefficient '+str(i),(-coefficient).substitute([h+2,z,k]),['h_minus_2','z','unused']))
    small_certificates.append(positive_certificate('x=1, h=1, k>=1',h_one_positive,['unused','z','k_minus_1']))

    P=axis_polynomial(); s,b,z,n=Poly.variables(4)
    F=b-1+s*z; m=F*F+F+1;K=s*(F-1)-z+1
    expected_leading=n*n-z*n-1
    identity('axis_quartic_leading_coefficient',P.coefficient(1,4),expected_leading,checks)
    # Direct expansion of r in t first yields these three coefficients in n.
    N0=F*F-b*F+b*b
    L=s*s*z-2*s-b*z
    c2=m*N0
    c1=-2*b*m*K+(b+1)*L*m+s*m*(b+1)**2+(F*F+b)*K*(b+1)
    c0=-b*K*K+(b+1)*L*K+(b+1)**2*F*(s*s-b)
    identity('axis_quadratic_in_lattice_integer',P,c2*n*n+c1*n+c0,checks)
    cert_width=positive_certificate('n>=z+1, s>=1, b>=2, z>=1',
        P.substitute([s+1,b+2,z+1,n+z+2]),['s_minus_1','b_minus_2','z_minus_1','n_minus_z_minus_1'])
    M0=(s*z)**2-3*s*z+3
    Cn=n*M0+(s*s-1)*z-3*s+1
    identity('axis_divisor_remainder',m*n+K,(b+1)*(s+n*(b+2*s*z-2))+Cn,checks)
    identity('axis_zero_remainder_resonance',P.substitute([1,b,2,2]),
             (b+1)**2*(-b*b+5*b+17),checks)
    identity('axis_divisor_uniform_bound_at_n_equals_z',Cn.substitute([s,b,z,z]),
             s*s*z**3-3*s*z*z+(s*s+2)*z-3*s+1,checks)
    return checks,cert_x2,small_certificates,cert_width


def positive_divisors(value):
    value=abs(value)
    assert value
    values=[]
    for a in range(1,isqrt(value)+1):
        if value%a==0:
            values.append(a)
            if a*a!=value:values.append(value//a)
    return sorted(values)


def integer_roots(coefficients):
    c=list(coefficients)
    while c and c[-1]==0:c.pop()
    assert c
    while len(c)>1 and c[0]==0:c.pop(0)
    if len(c)==1:return []
    assert c[0]
    return [a for a in positive_divisors(c[0]) if a>=2 and sum(v*a**i for i,v in enumerate(c))==0]


def exact_model(s,t,z,b,n):
    F=b-1+s*z; m=F*F+F+1
    S=t-(F+1)*n;T=s+F*n;u=s+t-1;U=u+z-n
    alpha=(s+t)*z+b-1; k=F
    if min(S,T,U)<=0:return None
    q=(1+s*S,1+t*T,1+u*U,1)
    P=((0,t*S+alpha,-u*S-alpha-1,-S),
       (s*T-b,0,-u*T+b-1,-T),
       (-s*U+k,-t*U-k-1,0,U),(-s,-t,u,0))
    signed=(P[0][1],P[1][0],-P[0][2],-P[1][2],-P[2][0],-P[2][1])
    if min(signed)<=0:return None
    rows=[sum(P[i])+q[i] for i in range(4)]
    pairs=[P[i][j]*P[j][i]-q[i]*q[j]+1 for i in range(4) for j in range(i+1,4)]
    defect=[-q[i]-sum(P[j][i] for j in range(4)) for i in range(4)]
    assert rows==[0]*4 and pairs==[0]*6 and defect==[0,0,z,-z]
    weights=(Fraction(q[0]),Fraction(P[0][1])+Fraction(1,2*P[1][0]),Fraction(u)+Fraction(1,2*U),Fraction(1))
    gaps=[weights[j]-Fraction(P[i][j],q[i])*weights[i] for i in range(4) for j in range(4) if i!=j]
    assert all(g>0 for g in gaps)
    return {'parameters':[s,t,0,0,z,b], 'lattice_n':n, 'scales':[S,T,U], 'q':q, 'P':P,
            'D':defect,'weights':[str(a) for a in weights],'all_weight_gaps_positive':True}


def reconstruct_axis(s,z):
    assert s>=1 and z>=1
    poly=axis_polynomial()
    rows=[];models=[]
    for n in range(z+1):
        coeff=[0]*5
        for exp,c in poly.terms.items():
            coeff[exp[1]]+=c*s**exp[0]*z**exp[2]*n**exp[3]
        assert coeff[4]==n*n-z*n-1<0
        roots=integer_roots(coeff)
        Cn=n*((s*z)**2-3*s*z+3)+(s*s-1)*z-3*s+1
        row={'n':n,'quartic_coefficients_ascending':coeff,'divisor_remainder_Cn':Cn,
             'all_integer_roots_b_ge_2':roots,'tested':[]}
        for b in roots:
            F=b-1+s*z;m=F*F+F+1;K=s*(F-1)-z+1
            numerator=m*n+K
            if numerator%(b+1):
                row['tested'].append({'b':b,'exclusion':'t is not integral'});continue
            t=numerator//(b+1)
            if t<=s:
                row['tested'].append({'b':b,'t':t,'exclusion':'s>=t sector already excluded'});continue
            model=exact_model(s,t,z,b,n)
            if model is None:
                row['tested'].append({'b':b,'t':t,'exclusion':'positive scale or six-sign condition fails'})
            else:
                row['tested'].append({'b':b,'t':t,'status':'exact model'});models.append(model)
        rows.append(row)
    return {'fixed_s':s,'fixed_z':z,'lattice_integers_exhausted':list(range(z+1)),
            'b_or_t_cutoff':None,'candidate_bound':4*(z+1),'quartics':rows,'models':models,
            'scope':'Complete for this fixed (s,z) in the proportional sector; no global claim from finite fixtures.'}


def regressions():
    P=axis_polynomial(); out=[]
    for s,t,z,b,n in [(1,1,1,2,0),(2,10,3,4,1),(3,15,2,5,0),(5,30,4,7,2)]:
        F=b-1+s*z;m=F*F+F+1;K=s*(F-1)-z+1
        derived_t=Fraction(m*n+K,b+1)
        alpha=(s+derived_t)*z+b-1
        SS=derived_t-(F+1)*n;TT=s+F*n
        residual=-(s+derived_t*b)*SS+(s*alpha-derived_t)*TT-alpha*b
        assert (b+1)**2*residual==P.evaluate([s,b,z,n])
        out.append({'parameters_s_b_z_n':[s,b,z,n],'derived_t':str(derived_t),
                    'exact_original_residual':str(residual),'cleared_polynomial':P.evaluate([s,b,z,n])})
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--axis',nargs=2,type=int,metavar=('S','Z'))
    parser.add_argument('--proof',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.axis:
        print(json.dumps(reconstruct_axis(*args.axis),ensure_ascii=False,indent=2));return
    checks,cert_x2,small,cert_width=symbolic_certificates()
    root=Path(__file__).resolve().parent
    proof=args.proof or next(p for p in [root/'high_d_proportional_reduction_v24.tex',root.parent/'papers/sections/paper/high_d_proportional_reduction_v24.tex'] if p.is_file())
    fixtures=[reconstruct_axis(s,z) for s,z in [(1,1),(1,2),(2,1),(3,2),(4,3),(8,4)]]
    data={'version':'v24','status':'PASS','scope':'Unbounded proportional-sector reduction: x=y=0 and 0<=n<=z; complete fixed-(s,z) axis reconstruction.',
          'global_three_high_nonexistence_claim':False,'global_proportional_nonexistence_claim':False,
          'coefficient_identity_count':len(checks),'coefficient_identities':checks,
          'off_axis_positive_certificate':cert_x2,'x_one_sign_certificates':small,
          'zero_axis_lattice_width_certificate':cert_width,'direct_residual_regressions':regressions(),
          'finite_axis_fixtures':fixtures,'finite_fixtures_not_used_as_unbounded_proof':True,
          'old_scan_repeated':False,'old_verifier_imports':False,'dependencies':'Python standard library only',
          'proof_sha256':sha256(proof.read_bytes()).hexdigest(),'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
          'external_peer_review':False,'proof_assistant_formalization':False}
    output=args.output or root/'high_d_proportional_verification_v24.json'
    output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','coefficient_identities':len(checks),
                      'off_axis_coefficients':cert_x2['nonzero_coefficient_count'],
                      'off_axis_constant':cert_x2['constant'],
                      'axis_width_coefficients':cert_width['nonzero_coefficient_count'],
                      'axis_width_constant':cert_width['constant'],
                      'axis_fixtures':len(fixtures),'models_in_fixtures':sum(len(f['models']) for f in fixtures)}))

if __name__=='__main__':main()
