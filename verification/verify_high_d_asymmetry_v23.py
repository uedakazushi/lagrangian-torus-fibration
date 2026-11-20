#!/usr/bin/env python3
"""Exact v23 asymmetric high-D lattice verification; standard library only.

The general proofs are in high_d_asymmetry_lattice_obstruction_v23.tex.
Polynomial identities are checked coefficient by coefficient. The four
square obstructions are checked on COMPLETE residue systems, not on an
arbitrary cutoff. Numerical examples are regressions only. No existing
144-low-row scan is rerun and no global nonexistence is inferred.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path

NAMES = ("s", "t", "x", "y", "z", "b", "h", "j", "e", "F", "w", "nu", "p", "n", "R0")
NV = len(NAMES)

class Poly:
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {key: value for key, value in value.items() if value}
        else:
            self.terms = {(0,) * NV: value} if value else {}
    def __add__(self, other):
        out = defaultdict(int, self.terms)
        for key, value in Poly(other).terms.items():
            out[key] += value
        return Poly(out)
    __radd__ = __add__
    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})
    def __sub__(self, other):
        return self + -Poly(other)
    def __rsub__(self, other):
        return Poly(other) + -self
    def __mul__(self, other):
        out = defaultdict(int)
        for key, value in self.terms.items():
            for key2, value2 in Poly(other).terms.items():
                out[tuple(a + b for a, b in zip(key, key2))] += value * value2
        return Poly(out)
    __rmul__ = __mul__
    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError("nonnegative integer powers only")
        result = Poly(1)
        for _ in range(exponent):
            result *= self
        return result

V = {name: Poly({tuple(int(i == j) for i in range(NV)): 1})
     for j, name in enumerate(NAMES)}

def coefficient_checks():
    checks = []
    def check(name, left, right=0):
        left, right = Poly(left), Poly(right)
        difference = left - right
        assert not difference.terms, (name, difference.terms)
        checks.append({"name": name, "status": "PASS",
                       "left_monomials": len(left.terms),
                       "right_monomials": len(right.terms),
                       "difference_monomials": 0})

    s, t, x, y, z, b = (V[name] for name in ("s", "t", "x", "y", "z", "b"))
    u, h, j, ell, B = s+t-1, s-x, t-y, s+t-1+z, b-1
    d, delta = x+y+z, s*y-t*x
    lam, mu = u*x+s*z, u*y+t*z
    F, m = B+lam, (B+lam)**2+(B+lam)+1
    alpha, k = u*d+B+z, s*d+B-x
    E, J = mu*h-ell-j, h+ell-lam*j
    ns = m*h+F*E-J
    nt = m*j+E+(F+1)*J
    nu = ns+nt+(d-1)*m
    nn = m*ell-nu
    check("mu_h_minus_lambda_j", mu*h-lam*j, ell*delta)
    check("E_plus_J", E+J, ell*delta+h-j)
    check("F_plus_delta", F+delta, B+h+s*(d-1))
    check("ell_sum", ell, h+j+d-1)
    check("lattice_T_numerator", nt, m*h+F*nn+m*ell*delta)
    check("lattice_S_numerator", ns, m*j-(F+1)*nn-m*ell*delta)
    check("lattice_U_numerator", nu, m*ell-nn)
    check("inverse_E", (F+1)*(ns-m*h)+(nt-m*j), m*E)
    check("inverse_J", -(ns-m*h)+F*(nt-m*j), m*J)

    a = u*h-B*(F+1)
    K0 = h*(s-1)+1
    A0 = b*K0-s*h
    check("a_second_expression", a, s*ell-b*F)
    check("a_hypersurface", a, u*(s-b*x)-B*(b+s*z))
    check("degenerate_gap_with_exact_remainder",
          b*b*m-s*nt, A0*F+b*b-s*h-(k+b*F)*a)
    check("A0_minus_B", A0-B, h*(B*s-b)+1)
    check("s_ge_2_A0_gap", B*s-b, (b-1)*(s-2)+b-2)
    check("negative_strip_x_ge_2_gap", F+1-j-ell,
          B+u*(x-1)+(s-1)*z+1-t+y)
    check("positive_strip_x_ge_2_gap", F-h-ell,
          B+(u+1)*x-s-u+(s-1)*z)

    # Independent formal variables for the uniform degeneration upper bound.
    hh, ww = V["h"], V["w"]
    KK = hh*(s-1)+1
    FF = B+ww
    AA = b*KK-s*hh
    check("degenerate_upper_gap", (KK+1)*(FF*FF+FF+1)-(AA*FF+b*b-s*hh),
          (KK+1)*ww*ww+(B*KK+2*b-1+s*hh)*ww+KK+1+b*(s*hh-1))

    # delta = 0, S = j, T = h, after mu*h=lambda*j.
    jj, ee = V["j"], V["e"]
    LL = hh+s*ee
    FF = B+LL
    EE = LL*jj-(hh+jj+ee)-jj
    Qzero = ee*(s*hh-1)+hh*(hh-3)+(b+1)*(hh-jj)
    check("proportional_scale_equation", EE-FF*(jj-hh), Qzero)

    # delta = -1, x=1, t=s*y+1, n=1. No remaining residue used.
    tm, um, hm = s*y+1, s+s*y, s-1
    jm, em = tm-y, um+z
    Fm = B+um+s*z
    gm = B+(s-1)*z
    Sm, Tm = jm-gm-1, hm+gm
    Em = (um*y+tm*z)*hm-em-jm
    Qm = Em-(Fm+1)*(Sm-hm)-(Tm-jm)
    certm = ((s-1)*(s-2)+(b-2)+s*(s-1)*z)*y+s*s \
            +(b-2)*(b+2*s-1)+((2*s-1)*b+2*s*s-3*s-1)*z+s*(s-1)*z*z
    check("negative_strip_F_gap", Fm-em, gm)
    check("negative_strip_positive_polynomial", Qm, certm)
    check("negative_strip_z_coefficient_positive", 2*s*s-3*s-1,
          2*(s-2)**2+5*(s-2)+1)

    # delta = +1, x=1, z=0, s=b+nu, p=1. Keep original pair residue.
    vv = V["nu"]
    sp, tp = b+vv, (b+vv)*y-1
    up, hp, jp = sp+tp-1, sp-1, tp-y
    Fp, Sp, Tp = B+up, (sp-1)*y+B, vv
    alphap = up*(1+y)+B
    Ep = up*y*hp-up-jp
    Qp = Ep-(Fp+1)*(Sp-hp)-(Tp-jp)
    qpc = vv*vv+2*b*vv-4*vv-b+2-(b*b-vv*(vv-1))*y
    Rp = -(sp+tp*b)*Sp+(sp*alphap-tp)*Tp-alphap*b
    Np = b*vv*(y**3+y*y-2)+b*(y+1)+vv*vv*(y**3-1) \
         +vv*(vv-1)*y*y+vv*y+4*vv-2
    check("positive_strip_difference_equation", Qp, qpc)
    check("positive_strip_original_residue", y*Rp, (sp*y*(y+1)+1)*Qp+Np)
    check("positive_strip_positive_y_cubic_1", y**3+y*y-2,
          (y-1)*(y*y+2*y+2))
    check("positive_strip_positive_y_cubic_2", y**3-1,
          (y-1)*(y*y+y+1))

    # Degeneracy s=1 and s=2: coefficient and discriminant checks.
    f1 = B+z
    g1 = B*f1+b*b-1
    check("s1_gap", g1, B*(f1+b+1))
    check("s1_upper_gap", 2*(f1*f1+f1+1)-g1,
          2+(3*b-1)*z+2*z*z)
    check("s1_discriminant", (2-b)**2-4*(2-b*b), 5*b*b-4*b-4)
    qq = V["nu"]
    check("s1_pell_identity", (5*b-2)**2-5*qq*qq-24,
          5*(5*b*b-4*b-4-qq*qq))
    f2 = B+2*z
    g2 = (3*b-4)*f2+b*b-4
    check("s2_upper_gap", 4*(f2*f2+f2+1)-g2,
          3*b+4+10*b*z+16*z*z)
    for rr, disc in [(1, 13*b*b-30*b+5),
                     (2, 17*b*b-36*b-12),
                     (3, 21*b*b-42*b-35)]:
        check(f"s2_R{rr}_discriminant", (rr-3*b+4)**2-4*rr*(rr-b*b+4), disc)
    check("s2_R3_factor", 21*b*b-42*b-35, 7*(3*(b-1)**2-8))

    # Further degeneration reductions recorded in the future-useful notes.
    # This exact identity is the b=1 reduction modulo B=b-1; together with
    # uh=0 and s*ell=F modulo B it gives B | h*(s-1)*(R0-1).
    FF, TT = V["F"], V["p"]
    ss0 = FF*TT-ell
    aa0 = FF+t*z
    rr0 = -(s+t)*ss0+(s*aa0-t)*TT-aa0
    check("degenerate_residue_mod_B_identity", hh*(rr0+t*TT),
          hh*(t*TT+1)*(s*ell-FF)+t*(1-s*TT)*u*hh)
    check("degenerate_low_row_mod_B_identity", hh*t, hh*(1-s)+u*hh)
    kap, LL = V["n"], V["w"]
    bb, ff, kk = s*kap+1, s*LL, s*(s-1)+1
    check("exceptional_R1_congruence_identity",
          ff*ff+ff+1-(bb*kk-s*s)*ff-bb*bb+s*s,
          s*(s*(LL*LL+(1-kap*kk)*LL-kap*kap+1)-2*kap))

    # Exact two-variable reconstruction for the remaining delta=1,x=0 branch.
    pp = V["p"]
    f = B+z
    mm = f*f+f+1
    DD = z-1
    tau = DD+mm*pp-f*(z+2)
    sigma = (f+1)*pp-z-1
    theta = tau+DD*(z+1-f*pp)
    anum = (z+1)*tau+f*DD
    PP = -DD*(DD+b*tau)*sigma+(z*tau+f*DD)*theta-b*DD*anum
    Ap = (b*b+b*z+z*z)*mm
    Bp = (-b**3*z*z-2*b**3*z-3*b**3-2*b*b*z**3-3*b*b*z*z-3*b*b*z
          +2*b*b-b*z**4-2*b*z**3-3*b*z*z+b*z-b-z**4+z*z)
    Cp = (b*b*z**3+2*b*b*z*z+5*b*b*z+b*b+b*z**4+2*b*z*z-2*b*z-b
          +z**3-z*z-z+1)
    check("remaining_axis_residual_quadratic", PP, Ap*pp*pp+Bp*pp+Cp)
    check("remaining_axis_difference_E", (tau-DD)*DD,
          (mm*pp-f*(z+2))*DD)
    # tau = (z-1)t, so divisibility is determined by z=1 specialization.
    f_at_one = b
    check("remaining_axis_congruence_remainder",
          (f_at_one*f_at_one+f_at_one+1)*pp-f_at_one*3,
          (b*b+b+1)*pp-3*b)
    check("remaining_axis_z1_positive_gap", (b*b+b+1)-3*b, (b-1)**2)
    return checks


def square_obstructions():
    cases = [
        ("s=1,R0=1", 9, lambda b: 5*b*b-4*b-4),
        ("s=2,R0=1", 25, lambda b: 13*b*b-30*b+5),
        ("s=2,R0=2", 9, lambda b: 17*b*b-36*b-12),
        ("s=2,R0=3", 49, lambda b: 21*b*b-42*b-35),
    ]
    result = []
    for name, modulus, fn in cases:
        squares = {q*q % modulus for q in range(modulus)}
        values = {fn(b) % modulus for b in range(modulus)}
        assert squares.isdisjoint(values), (name, squares & values)
        result.append({"case": name, "modulus": modulus,
                       "all_b_residue_classes_checked": modulus,
                       "square_residues": sorted(squares),
                       "discriminant_residues": sorted(values),
                       "intersection": [], "status": "PASS",
                       "scope": "All integers b, by complete residue classes."})
    return result


def reconstruct(s, t, x, y, z, b):
    u, B, d, h, j, ell = s+t-1, b-1, x+y+z, s-x, t-y, s+t-1+z
    lam, mu = u*x+s*z, u*y+t*z
    F = B+lam
    m = F*F+F+1
    E, J = mu*h-ell-j, h+ell-lam*j
    S = Fraction(h)+Fraction(F*E-J,m)
    T = Fraction(j)+Fraction(E+(F+1)*J,m)
    U = S+T+d-1
    alpha, k = u*d+B+z, s*d+B-x
    q = (1+s*S,1+t*T,1+u*U,Fraction(1))
    P = ((0,t*S+alpha,-(u*S+alpha+1),-S),
         (s*T-b,0,-(u*T-b+1),-T),
         (-(s*U-k),-(t*U+k+1),0,U),
         (-s,-t,u,0))
    rows = [sum(P[i])+q[i] for i in range(4)]
    pairs = [P[i][j]*P[j][i]-q[i]*q[j]+1 for i in range(4) for j in range(i+1,4)]
    actual_D = [-q[i]-sum(P[j][i] for j in range(4)) for i in range(4)]
    residual = -(s+t*b)*S+(s*alpha-t)*T-alpha*b
    signs = [t*S+alpha,s*T-b,u*S+alpha+1,u*T-b+1,s*U-k,t*U+k+1]
    assert all(v == 0 for v in rows)
    assert actual_D == [x,y,z,-d]
    assert pairs[:1]+[pairs[1],pairs[3]] == [residual]*3
    assert [pairs[2],pairs[4],pairs[5]] == [0,0,0]
    delta = s*y-t*x
    n = ell-U
    assert S == j-(F+1)*n-ell*delta
    assert T == h+F*n+ell*delta
    a = u*h-B*(F+1)
    out = dict(parameters=[s,t,x,y,z,b],scales=[S,T,U],q=q,D=actual_D,
               a=a,delta=delta,lattice_n=n,residual=residual,
               pair_residuals=pairs,sign_factors=signs,
               single_congruence=(F*E-J)%m==0)
    if min(S,T,U,*signs)>0:
        weights=(q[0],signs[0]+Fraction(1,2)/signs[1],u+Fraction(1,2)/U,Fraction(1))
        gaps=[weights[j]-Fraction(P[i][j],q[i])*weights[i]
              for i in range(4) for j in range(4) if i!=j]
        out["weights"]=weights
        out["gaps"]=gaps
    return out


def regressions():
    result = []
    # Genuine model remains outside the nonnegative high-D hypothesis.
    mixed = reconstruct(1,2,-1,1,3,2)
    assert mixed["q"] == (5,11,23,1)
    assert mixed["residual"] == 0 and min(mixed["gaps"]) > 0
    result.append({"name":"mixed_D_genuine_model_not_excluded", "status":"PASS", "data":mixed})
    old = reconstruct(1,3,0,4,0,2)
    assert old["scales"] == [3,5,11] and old["residual"] == 3
    result.append({"name":"old_difference_only_false_candidate", "status":"PASS", "data":old})
    plus = reconstruct(5,4,1,1,0,3)
    assert plus["delta"] == 1 and plus["scales"] == [6,2,9]
    assert plus["single_congruence"] and min(plus["sign_factors"]) > 0
    assert plus["residual"] == 16
    result.append({"name":"positive_strip_needs_original_residual", "status":"PASS", "data":plus})
    deg = reconstruct(3,138,0,0,4,16)
    assert deg["a"] == 0 and deg["scales"] == [54,84,141]
    assert deg["single_congruence"] and min(deg["sign_factors"]) > 0
    assert 16**2-3*deg["scales"][1] == 4 and deg["residual"] == 5658
    result.append({"name":"s_ge_3_degeneracy_not_auto_excluded", "status":"PASS", "data":deg})
    prop = reconstruct(3,6,1,2,0,3)
    assert prop["delta"] == 0 and prop["scales"] == [4,2,8]
    assert prop["residual"] == -18
    result.append({"name":"reverse_order_proportional_branch_retained", "status":"PASS", "data":prop})
    for params, residue in [((3,3,0,0,1,3),3),((2,2,1,1,1,2),-8)]:
        data = reconstruct(*params)
        assert data["residual"] == residue
        result.append({"name":"zero_lattice_case_original_residue", "status":"PASS", "data":data})
    return result


def remaining_axis_fixed_b_z(b, z):
    """Complete reconstruction of delta=1,x=0 for a fixed b>=2,z>=2.

    Solves every positive integer p by an exact quadratic; no p or t cutoff.
    Returned models still satisfy all original pair products and positive
    weights. Empty output is a result only for the specified pair (b,z).
    """
    if not isinstance(b,int) or not isinstance(z,int) or b<2 or z<2:
        raise ValueError("b,z must be integers >= 2")
    F, D = b-1+z, z-1
    m = F*F+F+1
    def residue_polynomial(p):
        tau = D+m*p-F*(z+2)
        S = (F+1)*p-z-1
        theta = tau+D*(z+1-F*p)
        return -D*(D+b*tau)*S+(z*tau+F*D)*theta-b*D*((z+1)*tau+F*D)
    C = residue_polynomial(0)
    A = (b*b+b*z+z*z)*m
    B = residue_polynomial(1)-A-C
    assert residue_polynomial(-1)==A-B+C
    disc = B*B-4*A*C
    candidates=[]
    models=[]
    if disc>=0:
        root=isqrt(disc)
        if root*root==disc:
            for numerator in sorted({-B-root,-B+root}):
                if numerator%(2*A):
                    continue
                p=numerator//(2*A)
                if p<1:
                    continue
                tau=D+m*p-F*(z+2)
                if tau%D or tau//D<1:
                    candidates.append({"p":p,"reason":"low-row t not a positive integer"})
                    continue
                t=tau//D
                rec=reconstruct(1,t,0,1,z,b)
                assert rec["lattice_n"]==-p and rec["residual"]==0
                if min(*rec["scales"],*rec["sign_factors"])<=0:
                    candidates.append({"p":p,"t":t,"reason":"scale or sign failure"})
                    continue
                assert rec["single_congruence"] and min(rec["gaps"])>0
                assert all(value==0 for value in rec["pair_residuals"])
                models.append(rec)
    return {"fixed_b_z":[b,z],"coefficients":[A,B,C],"discarded_roots":candidates,
            "models":models,"scope":"All positive p and all t for this fixed b,z."}


def jsonable(value):
    if isinstance(value, Fraction):
        return int(value) if value.denominator==1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {key:jsonable(val) for key,val in value.items()}
    if isinstance(value,(list,tuple)):
        return [jsonable(val) for val in value]
    return value


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("high_d_asymmetry_verification_v23.json"))
    parser.add_argument("--proof", type=Path, default=next(p for p in [Path(__file__).with_name("high_d_asymmetry_lattice_obstruction_v23.tex"), Path(__file__).resolve().parent.parent/"paper/high_d_asymmetry_lattice_obstruction_v23.tex"] if p.is_file()))
    parser.add_argument("--axis", nargs=2, type=int, metavar=("B_PARAMETER","Z"),
                        help="Optionally reconstruct the entire remaining axis for fixed b,z.")
    args = parser.parse_args()
    source = Path(__file__).resolve()
    checks = coefficient_checks()
    modular = square_obstructions()
    examples = regressions()
    result = {"version":"v23", "status":"PASS",
              "source_file":str(source), "source_sha256":sha256(source),
              "proof_file":str(args.proof.resolve()), "proof_sha256":sha256(args.proof),
              "coefficient_identity_count":len(checks), "coefficient_checks":checks,
              "complete_modular_obstructions":modular,
              "total_b_residue_classes":sum(item["all_b_residue_classes_checked"] for item in modular),
              "regression_groups":examples,
              "excluded_sectors":["delta=0 and s>=t", "delta=-1", "delta=1 and x>=1", "a=0 and s<=2"],
              "unresolved_scope":["General nonnegative high-D nonexistence",
                                  "delta=0 and s<t", "delta=1,x=0 (s=y=1,z>=2)",
                                  "abs(delta)>=2", "general a=0,s>=3"],
              "verification_scope":"Exact coefficient identities, complete residue-class obstructions, and explicit regressions. General sign proofs are in the TeX file; no denominator or low-row cutoff is used.",
              "previous_scan_rerun":False, "dependencies":"Python standard library only"}
    if args.axis:
        result["remaining_axis_fixed_data"]=remaining_axis_fixed_b_z(*args.axis)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(jsonable(result),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","coefficient_identities":len(checks),
                      "complete_modular_cases":len(modular),"regression_groups":len(examples),
                      "output":str(args.output)},ensure_ascii=False))

if __name__=="__main__":
    main()
