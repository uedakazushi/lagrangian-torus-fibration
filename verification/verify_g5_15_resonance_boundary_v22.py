#!/usr/bin/env python3
"""Exact v22 verification: G5_15 ordinary resonance and T=1 boundaries.

Standard library only.  No import from, write to, or execution of v21 files.
All finite lists are derived from proved bounds or divisors of fixed integers.
There is no denominator scan and no numerical root tolerance.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import isqrt
from pathlib import Path
import json


NAMES = ("m", "S", "T", "U", "H", "j", "X", "h", "d", "x", "y")
N = len(NAMES)


class Poly:
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {key: Fraction(val) for key, val in value.items() if val}
        else:
            self.terms = {(0,) * N: Fraction(value)} if value else {}

    def __add__(self, other):
        out = defaultdict(Fraction, self.terms)
        for key, val in Poly(other).terms.items():
            out[key] += val
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -val for key, val in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        out = defaultdict(Fraction)
        for left, a in self.terms.items():
            for right, b in Poly(other).terms.items():
                out[tuple(x+y for x, y in zip(left, right))] += a*b
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert type(exponent) is int and exponent >= 0
        result = Poly(1)
        for _ in range(exponent):
            result *= self
        return result


v = {name: Poly({tuple(int(i == j) for j in range(N)): 1})
     for i, name in enumerate(NAMES)}
m, S, T, U, H, j, X, h, d, x, y = (v[name] for name in NAMES)
identities = []


def zero(name, expression):
    assert not Poly(expression).terms, name
    identities.append(name)


# Direct positive-side reconstruction; this H-quadratic degenerates at T=1.
A = (S+1)*(m*T+1)-1
B = (m-1)*T+1
C = (S+1)*(m*U+1)-1
D = (m*T+1)*(m*U+1)-1
E = (m+1)*U+1
cleared = C*(A+B*H)+D*H*(H+1)-E*(H+1)*(A+B*H)
quadratic = (D-E*B)*H**2+(C*B+D-E*(A+B))*H+A*(C-E)
zero("positive_side_quadratic_from_original_rows", cleared-quadratic)
zero("positive_side_leading_coefficient", D-E*B-(T-1)*(U+1))

# T=1 is handled before division by the vanished leading coefficient.
A1 = (m+1)*S+m
C1 = (S+1)*(m*U+1)-1
D1 = (m+1)*(m*U+1)-1
F = ((2*m+1)*S+m)*U+S+m
G = (m*S-1)*U+S-1
zero("T1_constant_factor", C1-E-G)
zero("T1_linear_factor", m*C1+D1-E*(A1+m)+F)
zero("T1_ratio_is_linear_equation",
     C1*(A1+m*H)+D1*H*(H+1)-E*(H+1)*(A1+m*H)-(A1*G-H*F))
zero("T1_K_greater_than_two", F-2*G-((S+m+2)*U-S+m+2))
zero("T1_K_minus_three", F-3*G-(((1-m)*S+m+3)*U-2*S+m+3))
zero("T1_positive_gap_U_at_least_one",
     (S+m+2)*(1+y)-S+m+2-(2*m+4+(S+m+2)*y))
zero("T1_m2_S_at_least_six_negative",
     (5-(6+x))*(1+y)-2*(6+x)+5-(-8-3*x-y-x*y))
zero("T1_m4_S_at_least_four_negative",
     (7-3*(4+x))*(1+y)-2*(4+x)+7-(-6-5*x-5*y-3*x*y))

# The shared D coefficient and the node implications.
Q = m*U+1
W = X+Q-U
zero("shared_D_linear_coefficient_numerator",
     -j*W+(j+m-1)*X-((m-1)*X-j*(Q-U)))
Mnode = X-Q*(1-h)
Nnode = Q+U-Mnode
zero("shared_node_other_leg", W+Nnode-Q*(3-h))
Q2 = 2*U+1
X2 = j*(U+1)
W2 = (j+1)*(U+1)
M2 = (j-2+2*h)*U+j-1+h
N2 = (5-j-2*h)*U+2-j-h
zero("resonant_M", X2-Q2*(1-h)-M2)
zero("resonant_N", Q2+U-M2-N2)
zero("resonant_W", X2+Q2-U-W2)

# Original shared D, with the A coefficient cancelled, cleared by J(U+1).
J = j*(j+1)
original_shared_numerator = (2-Q2)*J*(U+1)-2*U*(j+1)+2*U*j+Q2*(U-1-d)*J
formula_shared_numerator = (-2*d-2)*J*(U+1)-2*(U+1)+J*(d+2)+2
zero("resonant_D_integer_divisor_identity",
     original_shared_numerator-formula_shared_numerator)


def divisors(number):
    assert number > 0
    answer = set()
    for value in range(1, isqrt(number)+1):
        if number % value == 0:
            answer.update((value, number//value))
    return sorted(answer)


def shared_D(jj, dd, uu):
    qq, xx, ww = 2*uu+1, jj*(uu+1), (jj+1)*(uu+1)
    # Evaluate the direct pair/column expression, not the simplified formula.
    return (2-qq-Fraction(qq-1, xx)+Fraction(qq-1, ww)
            +Fraction(qq*(jj+1)*(uu-1-dd), ww))


# Metadata independently restates the complete 14-cell table.
cells = [dict(center=1, m=4, j=1, dminus=-9, dplus=5, swapped=False),
         dict(center=1, m=1, j=4, dminus=5, dplus=-9, swapped=False)]
for jj in (3, 4, 5):
    for swapped in (False, True):
        cells.append(dict(center=2, m=2, j=jj, dminus=0, dplus=2,
                          swapped=swapped))
for center, js, dm, dp in ((3, (4, 5, 6), 5, -7),
                          (4, (5, 6, 7), -3, 9)):
    for jj in js:
        cells.append(dict(center=center, m=2, j=jj, dminus=dm,
                          dplus=dp, swapped=False))
assert len(cells) == 14

resonance_checks = []
excluded_by_coefficient_or_node = []
for cell_index, cell in enumerate(cells):
    mm, jj = cell["m"], cell["j"]
    if mm == 1:
        excluded_by_coefficient_or_node.append(
            dict(cell=cell_index, reason="m=1 coefficient numerator is -j"))
        continue
    if mm == 4:
        assert jj == 1
        excluded_by_coefficient_or_node.append(
            dict(cell=cell_index, reason="3X=3U+1 has no integer solution"))
        continue
    assert mm == 2 and jj >= 3
    for hh in (0, 1, 2):
        coefficient, rhs = 5-jj-2*hh, jj-1+hh
        if coefficient <= 0:
            assert rhs > 0
            excluded_by_coefficient_or_node.append(
                dict(cell=cell_index, h=hh,
                     reason="N>=1 requires nonpositive coefficient times U >= positive RHS"))
            continue
        assert hh == 0 and jj in (3, 4)
        lower = (rhs+coefficient-1)//coefficient
        dm, dp = cell["dminus"], cell["dplus"]
        fixed_integer = jj*(jj+1)*(dm+2)+2
        candidate_U = [r-1 for r in divisors(fixed_integer)
                       if r-1 >= lower and shared_D(jj, dm, r-1).denominator == 1]
        assert len(candidate_U) == 1
        for uu in candidate_U:
            qq, MM, NN = 2*uu+1, (jj-2)*uu+jj-1, (5-jj)*uu+2-jj
            total = uu+1+dp
            first_survivors, both_survivors = [], []
            # This finite range is forced by the low D equation, not a cutoff.
            for ss in range(2, total, 2):
                tt = total-ss
                if cell["swapped"]:
                    first, second = qq*(1+2*tt)-1, qq*(1+ss)-1
                else:
                    first, second = qq*(1+ss)-1, qq*(1+2*tt)-1
                if first % MM:
                    continue
                record = dict(S=ss, T=tt, first_numerator=first,
                              first_divisor=MM, first_quotient=first//MM,
                              second_numerator=second, second_divisor=NN,
                              second_remainder=second % NN)
                first_survivors.append(record)
                if second % NN == 0:
                    both_survivors.append(record)
            assert not both_survivors
            resonance_checks.append(dict(
                cell=cell_index, **cell, h=hh, minimum_U=lower,
                fixed_divisor_integer=fixed_integer,
                complete_divisor_list=divisors(fixed_integer),
                surviving_U=candidate_U, U=uu, Q=qq, M=MM, N=NN,
                shared_D=int(shared_D(jj, dm, uu)), scale_sum=total,
                first_pair_survivors=first_survivors,
                both_pair_survivors=both_survivors))
assert len(resonance_checks) == 5
assert {(r["j"], r["dminus"], r["U"]) for r in resonance_checks} == {
    (3, 0, 12), (4, 0, 20), (4, 5, 70)}
assert [(r["S"], r["T"]) for c in resonance_checks
        for r in c["first_pair_survivors"]] == [(8, 7), (4, 11), (20, 3)]


# Boundary finite sets, derived analytically above, with exact fractions.
t1_checks = []
for mm, dd in ((4, 5), (1, -9), (2, 2), (2, -7), (2, 9)):
    if mm == 1:
        t1_checks.append(dict(m=mm, d=dd, status="excluded", reason="q_b=2 is even"))
        continue
    permitted_S = (2, 4) if mm == 2 else (2,)
    records = []
    for ss in permitted_S:
        uu = ss-dd
        record = dict(S=ss, U=uu)
        if uu <= 0:
            record.update(status="excluded", reason="U<=0")
        else:
            ff = ((2*mm+1)*ss+mm)*uu+ss+mm
            gg = (mm*ss-1)*uu+ss-1
            kk = Fraction(ff, gg)
            record.update(K=str(kk))
            if kk.denominator != 1:
                record.update(status="excluded", reason="K is nonintegral")
            else:
                aa = (mm+1)*ss+mm
                hh = Fraction(aa, kk)
                assert hh.denominator == 1
                cc = (ss+1)*(mm*uu+1)-1
                assert cc % (int(hh)+1) != 0
                record.update(H=int(hh), pair_numerator=cc, pair_divisor=int(hh)+1,
                              pair_remainder=cc % (int(hh)+1), status="excluded",
                              reason="remaining pair integrality fails")
        records.append(record)
    t1_checks.append(dict(m=mm, d=dd, analytically_permitted_S=list(permitted_S),
                         records=records, status="excluded"))


# A counterexample prevents reintroduction of the false general low-D sign claim.
q_example = [5, 59, 293, 1]
P_example = [[0, 7, -8, -4], [42, 0, -43, -58],
             [-183, -402, 0, 292], [-1, -1, 1, 0]]
weights_example = [Fraction(5), Fraction(589, 84), Fraction(585, 584), Fraction(1)]
assert all(sum(row) == -q_example[i] for i, row in enumerate(P_example))
assert all(P_example[i][j]*P_example[j][i] == q_example[i]*q_example[j]-1
           for i in range(4) for j in range(i+1, 4))
assert all(weights_example[j]-Fraction(P_example[i][j], q_example[i])*weights_example[i] > 0
           for i in range(4) for j in range(4) if i != j)
D_example = [-q_example[i]-sum(P_example[j][i] for j in range(4) if j != i)
             for i in range(4)]
assert D_example[-1] == -231

script = Path(__file__).resolve()
proof_candidates = [script.with_name("g5_15_resonance_boundary_v22.tex"),
                    script.parent.parent/"papers/sections/paper/g5_15_resonance_boundary_v22.tex"]
proof = next(path for path in proof_candidates if path.is_file())
report = dict(
    version="v22", status="PASS", method="Exact polynomial coefficient identities and finite divisor certificates",
    arbitrary_denominator_cutoff=None, polynomial_identity_count=len(identities),
    polynomial_identities=identities, ordinary_cells=14,
    all_ordinary_D_resonances_excluded=True,
    T1_boundary_excluded_for_all_five_fixed_low_data=True,
    excluded_by_coefficient_or_node=excluded_by_coefficient_or_node,
    resonance_divisor_and_pair_certificates=resonance_checks,
    T1_certificates=t1_checks,
    low_D_sign_counterexample=dict(q=q_example, P=P_example, D=D_example,
                                  positive_weights=[str(w) for w in weights_example]),
    conclusions_not_established=[
        "unbounded exclusion or complete classification of nonresonant ordinary branches",
        "exclusion of the negative exceptional Q=3,5 branches",
        "completion of four-high cores 0,1 or a global fibration"],
    proof_file=proof.name, proof_sha256=sha256(proof.read_bytes()).hexdigest(),
    script_sha256=sha256(script.read_bytes()).hexdigest(),
    proof_assistant_formalization=False, external_peer_review=False)
output = script.with_name("g5_15_resonance_boundary_verification_v22.json")
output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
print(json.dumps(dict(status="PASS", polynomial_identities=len(identities),
                      complete_resonance_cases=5, remaining_resonances=0,
                      fixed_low_data_T1_cases=5, remaining_T1_cases=0,
                      output=str(output)), ensure_ascii=False))
