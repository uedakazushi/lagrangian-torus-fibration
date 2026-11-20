#!/usr/bin/env python3
"""Independent audit of the v25 degenerate divisor reduction.

Standard library only; does not import the primary verifier.  The independent
finite reconstruction solves the old scale equation as a quadratic in F and
never uses the new L enumeration or the gcd obstruction to prune candidates.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import isqrt
from pathlib import Path
import argparse
import json

class Poly:
    def __init__(self, n, terms=None):
        self.n = n
        self.terms = {tuple(e): c for e, c in (terms or {}).items() if c}
        assert all(len(e) == n and min(e) >= 0 for e in self.terms)

    @classmethod
    def const(cls, n, value):
        return cls(n, {(0,) * n: value})

    @classmethod
    def variables(cls, n):
        return tuple(cls(n, {tuple(int(i == j) for i in range(n)): 1}) for j in range(n))

    def coerce(self, other):
        if isinstance(other, (int, Fraction)):
            return Poly.const(self.n, other)
        assert isinstance(other, Poly) and other.n == self.n
        return other

    def __add__(self, other):
        other = self.coerce(other)
        result = defaultdict(int, self.terms)
        for exp, value in other.terms.items():
            result[exp] += value
        return Poly(self.n, result)
    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n, {exp: -c for exp, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        other = self.coerce(other)
        result = defaultdict(int)
        for exp, value in self.terms.items():
            for exp2, value2 in other.terms.items():
                result[tuple(a + b for a, b in zip(exp, exp2))] += value * value2
        return Poly(self.n, result)
    __rmul__ = __mul__

    def __truediv__(self, other):
        assert isinstance(other, int) and other
        return self * Fraction(1, other)

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        result, power = Poly.const(self.n, 1), self
        while exponent:
            if exponent & 1:
                result = result * power
            exponent //= 2
            power = power * power
        return result

    def substitute(self, values):
        assert len(values) == self.n
        values = [self.coerce(v) for v in values]
        result = Poly.const(self.n, 0)
        cache = [{0: Poly.const(self.n, 1)} for _ in values]
        for exp, value in self.terms.items():
            term = Poly.const(self.n, value)
            for i, degree in enumerate(exp):
                if degree not in cache[i]:
                    cache[i][degree] = values[i] ** degree
                term = term * cache[i][degree]
            result = result + term
        return result

    def coefficient(self, variable, degree):
        result = {}
        for exp, value in self.terms.items():
            if exp[variable] == degree:
                exp2 = list(exp)
                exp2[variable] = 0
                result[tuple(exp2)] = value
        return Poly(self.n, result)

    def records(self):
        result = []
        for exp, value in sorted(self.terms.items()):
            assert Fraction(value).denominator == 1
            result.append({'exponents': list(exp), 'coefficient': int(value)})
        return result


def identity(name, left, right, checks):
    difference = left - right
    assert not difference.terms, (name, difference.records())
    checks.append({'name': name, 'status': 'PASS', 'difference_terms': 0,
                   'left_terms': len(left.terms), 'right_terms': len(right.terms)})



def audit_identities():
    checks = []
    s, h, b, F, u, T, ell, y = Poly.variables(8)
    B = b - 1
    A = B*s - b
    R = b*b - s*T
    m = F*F + F + 1
    a = u*h - B*(F + 1)
    L = (F + 1)*R - h*A
    M = u*R - B*A
    Q = R*m - (h*A + b)*F - b*b + s*h
    t = u - s + 1
    C = F*(b*(t - 1) + s) + b*b*t + b*s - b
    identity('independent_hM_minus_BL_equals_Ra', h*M - B*L, R*a, checks)
    identity('independent_FL_identity', F*L - b*F - s*(T-h), Q, checks)
    identity('independent_positive_M_identity', m*M - C,
             u*Q + (F*A - s)*a, checks)
    z = ell - u
    S = F*T - B*(t-y) - ell
    alpha = F + t*z + u*y
    original = -(s + t*b)*S + (s*alpha - t)*T - alpha*b
    claimed = M*(t-y) - t*T + (s*ell - b*F)*(t*T + 1)
    identity('independent_original_pair_identity', original, claimed, checks)
    identity('quadratic_in_F_from_Q', Q,
             R*F*F + (R-h*A-b)*F + s*(h-T), checks)
    K0 = h*(s-1) + 1
    identity('prior_scale_equation_coefficient', b*K0-s*h, h*A+b, checks)
    identity('h_ge_b_elementary_gap', b*(s-b)-(s-1), (b-1)*(s-b-1), checks)
    # In this substitution, independent formal variables h,ell stand for x,z.
    x, zz = h, ell
    Fc = B + u*x + s*zz
    ac = u*(s-x) - B*(Fc+1)
    identity('canonical_a_equals_s_ell_minus_bF', ac,
             s*(u+zz)-b*Fc, checks)
    identity('canonical_s_minus_bx_relation', ac,
             u*(s-b*x)-B*(b+s*zz), checks)
    # Prove C>0 on the entire needed domain, not on sampled parameters.
    # Here u is an independent t_minus_1; s,b,F are nonnegative shift variables.
    Cp = (F+1)*((b+2)*u+s+1)+(b+2)**2*(u+1)+(b+2)*(s+1)-(b+2)
    assert Cp.terms and all(value > 0 for value in Cp.terms.values())
    assert Cp.terms.get((0,)*8, 0) > 0
    positivity = {'name': 'C_positive_for_s_t_at_least_1_b_at_least_2_F_at_least_1',
                  'variables': ['s_minus_1', 'unused', 'b_minus_2', 'F_minus_1',
                                't_minus_1', 'unused', 'unused', 'unused'],
                  'all_nonzero_coefficients_positive': True,
                  'constant': int(Cp.terms[(0,)*8]), 'full_coefficients': Cp.records()}
    return checks, positivity


def independent_f_quadratic_reconstruction(b):
    counts = {'b': b, 's_x_pairs': 0, 's_x_T': 0, 'square_discriminants': 0,
              'positive_integer_F_roots': 0, 'integer_u': 0, 'integer_ell': 0,
              'canonical_geometry_candidates': 0}
    roots, candidates = [], []
    for s in range(b+1, b*b):
        for x in range(1, (s-1)//b+1):
            counts['s_x_pairs'] += 1
            h = s-x
            B, A = b-1, (b-1)*s-b
            # No new T<=b-2 or gcd/L restrictions are used by this reconstruction.
            for T in range(1, (b*b-1)//s+1):
                counts['s_x_T'] += 1
                R = b*b-s*T
                q1, q0 = R-h*A-b, s*(h-T)
                assert R >= 1
                disc = q1*q1-4*R*q0
                if disc < 0:
                    continue
                rd = isqrt(disc)
                if rd*rd != disc:
                    continue
                counts['square_discriminants'] += 1
                for numerator in sorted(set((-q1-rd, -q1+rd))):
                    if numerator % (2*R):
                        continue
                    F = numerator//(2*R)
                    if F <= 0:
                        continue
                    counts['positive_integer_F_roots'] += 1
                    assert R*F*F+q1*F+q0 == 0
                    u_fraction = Fraction(B*(F+1), h)
                    root_record = {'b': b, 's': s, 'x': x, 'T': T, 'F': F,
                                   'u': str(u_fraction)}
                    roots.append(root_record)
                    if u_fraction.denominator != 1:
                        continue
                    counts['integer_u'] += 1
                    u = int(u_fraction)
                    if b*F % s:
                        continue
                    counts['integer_ell'] += 1
                    ell = b*F//s
                    t, z = u-s+1, ell-u
                    if t < 1 or z < 0 or F != B+u*x+s*z:
                        continue
                    counts['canonical_geometry_candidates'] += 1
                    # This stage is already stronger than required for comparing
                    # the empty primary outputs through b=20. No false model is
                    # accepted; further checks would be required if it is nonempty.
                    candidates.append([b, s, x, T, F, u, ell, t, z])
    return {'counts': counts, 'positive_integer_F_roots': roots,
            'geometry_candidates_requiring_full_pair_checks': candidates}


def negative_fixture():
    s,t,x,y,z,b = 3,138,0,0,4,16
    u, B, h, j = s+t-1,b-1,s-x,t-y
    ell = u+z
    lam,mu = u*x+s*z,u*y+t*z
    F = B+lam
    m = F*F+F+1
    E,J = mu*h-ell-j,h+ell-lam*j
    S = Fraction(h)+Fraction(F*E-J,m)
    T = Fraction(j)+Fraction(E+(F+1)*J,m)
    U = S+T+x+y+z-1
    alpha,k = u*(x+y+z)+B+z,s*(x+y+z)+B-x
    r = -(s+t*b)*S+(s*alpha-t)*T-alpha*b
    A=B*s-b;R=b*b-s*T;L=(F+1)*R-h*A;M=u*R-B*A
    assert S==54 and T==84 and U==141 and r==5658
    assert u*h==B*(F+1) and s*ell==b*F
    assert h*M==B*L and F*L==b*F+s*(T-h) and r==M*j-t*T
    assert M==125 and L==25
    return {'parameters':[s,t,x,y,z,b], 'scales':[int(S),int(T),int(U)],
            'M':int(M),'L':int(L),'original_pair_residual':int(r),
            'difference_equations_and_scale_integrality_pass':True,
            'original_pair_rejects':True}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--proof', type=Path, required=True)
    ap.add_argument('--primary-results', type=Path, required=True)
    ap.add_argument('--output', type=Path,
                    default=Path(__file__).with_name('audit_degenerate_divisor_v25.json'))
    args=ap.parse_args()
    checks,positive=audit_identities()
    # The prior positive-R lemma was read and checked: A0>=B and BF>=sh-B
    # imply Rm=A0 F+b^2-sh>=b^2-B>0. Integrality gives R>=1.
    implications=[
      'Prior canonical identities give a=s*ell-b*F=u*(s-b*x)-B*(b+s*z).',
      'a=0 implies s-b*x>0; x>=1 implies s>=b+1 and x< s/b.',
      'The prior scale equation proves R=b^2-sT>=1 independently of the pair residual.',
      'C>0 and mM-C=uQ+(FA-s)a imply M>0; hM=BL implies L>0.',
      'The original pair residual r=M(t-y)-tT=0 implies 1<=j<=t and M>=T.',
      'h>=b and s>=h imply T<b^2/s<=h, hence FL=bF+s(T-h) gives 1<=L<=b-1.',
      'h divides BL implies h/gcd(h,B) divides L; gcd=1 is impossible when h>=b.',
      'M=BL/h<=B^2/h<B implies M<=b-2, and thus 1<=T<=b-2.',
      'x<=floor((s-1)/b) and s>=b+1 imply x<=s-b and h>=b.',
      'R>=1 and T>=1 give s<=b^2-1; thus fixed b has finite s,x,T,L.',
      'F=s(h-T)/(b-L) has positive denominator since L<=b-1; u,ell,t,z are then unique.',
      'The required L definition and geometric equalities recover both a=0 and Q=0.',
      'M divides tT gives the unique y=t-tT/M; final original equations and signs ensure sufficiency.'
    ]
    primary=json.loads(args.primary_results.read_text())
    targets=primary['fixed_b_reconstructions']
    independent=[]
    for target in targets:
        row=independent_f_quadratic_reconstruction(target['b'])
        assert row['counts']['s_x_pairs']==target['s_x_pairs']
        # Every genuine primary model would occur in this broader F-quadratic
        # reconstruction. For the reported b values it has no geometric candidate.
        assert not row['geometry_candidates_requiring_full_pair_checks']
        assert target['models']==[]
        independent.append(row)
    result={
      'version':25,'status':'PASS','audit_target':'degenerate_divisor_reduction_v25',
      'primary_verifier_imported':False,'dependencies':'Python standard library only',
      'coefficient_identity_count':len(checks),'coefficient_identities':checks,
      'positive_C_certificate':positive,
      'mathematical_scope_and_completeness_audit':implications,
      'independent_fixed_b_method':'Solve Q=0 as a quadratic in F with the broader old T range; no gcd or L pruning.',
      'finite_comparison_only':True,'independent_reconstructions':independent,
      'negative_fixture':negative_fixture(),'issues_found':[],
      'source_file':str(Path(__file__).resolve()),
      'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
      'proof_file':str(args.proof.resolve()),'proof_sha256':sha256(args.proof.read_bytes()).hexdigest(),
      'primary_results_file':str(args.primary_results.resolve()),
      'primary_results_sha256':sha256(args.primary_results.read_bytes()).hexdigest(),
      'external_peer_review':False,'proof_assistant_formalization':False}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','identities':len(checks),
                      'fixed_b_values':[r['counts']['b'] for r in independent],
                      'F_roots_before_u_integrality':sum(r['counts']['positive_integer_F_roots'] for r in independent),
                      'geometry_candidates':0,'issues_found':[], 'output':str(args.output)},ensure_ascii=False))


if __name__=='__main__':
    main()
