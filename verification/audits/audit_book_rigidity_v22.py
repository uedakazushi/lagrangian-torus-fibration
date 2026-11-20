#!/usr/bin/env python3
"""Independent companion checks for the human book/frontier review in v22.

No earlier verifier or generator is imported or executed.  The negative family
comparison uses exactly the analytically required v21 certificate range 2<=w<=134;
it is a provenance cross-check, not the proof of the unbounded rigidity theorem.
Parity is verified in the finite ring Z/2, hence universally.  Graphs and node
offsets are genuinely finite objects and are exhausted.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
candidates = []
for parent in (HERE, *HERE.parents):
    candidates.extend((parent, parent/"deliverables/general_type_surface_fibration_v22"))
BUNDLE = next(p for p in candidates
              if (p/"papers/sections/paper/two_high_rigid_scale_families_v22.tex").is_file())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


class Polynomial:
    """Independent rational polynomial ring in ell,t,z,beta."""
    def __init__(self, value=0):
        if isinstance(value, Polynomial):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {m: Fraction(c) for m, c in value.items() if c}
        else:
            self.terms = {(0, 0, 0, 0): Fraction(value)} if value else {}

    def __add__(self, other):
        out = dict(self.terms)
        for m, c in Polynomial(other).terms.items():
            out[m] = out.get(m, 0)+c
        return Polynomial(out)

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self+-Polynomial(other)

    def __rsub__(self, other):
        return Polynomial(other)+-self

    def __mul__(self, other):
        out = {}
        for m, c in self.terms.items():
            for n, d in Polynomial(other).terms.items():
                key = tuple(a+b for a, b in zip(m, n))
                out[key] = out.get(key, 0)+c*d
        return Polynomial(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        result = Polynomial(1)
        for _ in range(exponent):
            result *= self
        return result


def universal_six_family_review():
    ell, t, zz, beta = [Polynomial({tuple(int(i == j) for j in range(4)): 1})
                        for i in range(4)]
    identities, strict_signs = [], []

    def identity(name, left, right=0):
        assert not (Polynomial(left)-right).terms, name
        identities.append(name)

    def positive(name, polynomial):
        assert all(c >= 0 for c in polynomial.terms.values())
        assert polynomial.terms.get((0, 0, 0, 0), 0) > 0
        strict_signs.append(name)

    # Here ell and t temporarily denote rho and k.  These are identities,
    # not finite substitutions for the unbounded parameters.
    rho, k = ell, t
    for d in (1, 2):
        r, h = rho-1, k-d
        F = (2*r+1)*h-r*r*d
        identity(f"F rewrite d={d}", F, (2*rho-1)*k-rho*rho*d)
        identity(f"Eminus beta numerator d={d}",
                 -F*beta-k*(rho*(d*zz-2*beta)+beta),
                 rho*d*(rho*beta-k*zz))
    identity("L3 forbidden k boundary", (2*rho-1)*(rho+1)*Fraction(1, 2)-rho*rho,
             (rho-1)*Fraction(1, 2))
    identity("L4 forbidden k boundary", (2*rho-1)*(rho+1)-2*rho*rho, rho-1)

    family_names = ("positive_L3_Fpositive", "positive_L4_Fpositive",
                    "positive_L3_Fnegative", "positive_L4_Fnegative",
                    "negative_Epositive", "negative_Enegative")
    for family in family_names:
        if family == "positive_L3_Fpositive":
            R = ell*(t+1)-2
            r, S, T = 2*R, 3*R, 3*R+2
            s, z, x, y = 2*(ell*t-1), (2*R+1)*t, 3*(ell*t-1), (3*R+2)*t
            DC, DD = 3*ell*t*t-4*t+5, -2*ell*t*t+3*t-3
            L, F_expected = 3, R
        elif family == "positive_L4_Fpositive":
            r = ell*(t+1)-3
            S, T = 2*r, 2*r+3
            s, z = ell*t-1, (r+1)*t
            x, y = 2*s, T*t
            DC, DD = 2*ell*t*t-3*t+5, -ell*t*t+2*t-2
            L, F_expected = 4, r
        elif family == "positive_L3_Fnegative":
            R = ell*(t+1)+2
            r, S, T = 2*R-1, 3*R-2, 3*R
            s, z, x, y = (2*R-1)*t, 2*(ell*t+1), (3*R-2)*t, 3*(ell*t+1)
            DC, DD = 5-3*ell*t*t-4*t, 2*ell*t*t+3*t-3
            L, F_expected = 3, -R
        elif family == "positive_L4_Fnegative":
            r = ell*(t+1)+2
            S, T = 2*r-1, 2*r+2
            s, z = r*t, ell*t+1
            x, y = S*t, 2*z
            DC, DD = 5-2*ell*t*t-3*t, ell*t*t+2*t-2
            L, F_expected = 4, -r-1
        elif family == "negative_Epositive":
            w = ell*(t+1)
            r, S, T = 2*w, w, w
            s, z, x, y = 2*(ell*t+1), (2*w+1)*t, ell*t+1, w*t
            DC, DD, L = ell*t*t-1, -2*ell*t*t-t+1, 1
        else:
            w = ell*(t+1)
            r, S, T = 2*w-1, w, w
            s, z, x, y = (2*w-1)*t, 2*(ell*t-1), w*t, ell*t-1
            DC, DD, L = -ell*t*t-1, 2*ell*t*t-t+1, 1
        a, b = s*S+1, z*T+1
        U, V = a+x-s, b-y+z
        matrix = [[0, -U, x, -s], [-V, 0, -y, z],
                  [r, -r-1, 0, 0], [-S, T, -L, 0]]
        q = [a, b, Polynomial(1), Polynomial(1)]
        identity(f"{family}: x", r*x, s*S)
        identity(f"{family}: y", (r+1)*y, z*T)
        for i in range(4):
            identity(f"{family}: row {i}", sum(matrix[i]), -q[i])
        for i, j in combinations(range(4), 2):
            identity(f"{family}: pair {i},{j}", Polynomial(matrix[i][j])*matrix[j][i], q[i]*q[j]-1)
        identity(f"{family}: DC", T-S+y-x, DC)
        identity(f"{family}: DD", s-z-1, DD)
        relation = 2*DC+3*DD if L == 3 else DC+2*DD if L == 4 else -DD-2*DC
        identity(f"{family}: low-D transfer", relation, t+1)
        if L > 1:
            identity(f"{family}: strict F", (2*r+1)*(S-r)-r*r*(L-2), F_expected)

    # Exhaustive sign proof outside the three exceptional endpoints.
    # ell,t in these shifted polynomials range over all nonnegative integers.
    positive("L3 Fnegative: -DC for original t>=2", 3*ell*(t+2)**2+4*(t+2)-5)
    positive("L3 Fnegative: DD for original t>=2", 2*ell*(t+2)**2+3*(t+2)-3)
    positive("L3 Fnegative: -DC for t=1,ell>=1", 3*(ell+1)-1)
    positive("L3 Fnegative: DD for t=1,ell>=1", 2*(ell+1))
    positive("L4 Fnegative: -DC for original t>=2", 2*ell*(t+2)**2+3*(t+2)-5)
    positive("L4 Fnegative: DD for original t>=2", ell*(t+2)**2+2*(t+2)-2)
    positive("L4 Fnegative: -DC for t=1,ell>=2", 2*(ell+2)-2)
    positive("L4 Fnegative: DD for t=1,ell>=2", ell+2)
    return dict(polynomial_identity_count=len(identities), polynomial_identities=identities,
                sign_regions_verified_by_positive_coefficients=strict_signs,
                all_six_families=list(family_names),
                Fnegative_exceptions=[dict(L=3, ell=0, t=1, DC=1, DD=0),
                                      dict(L=4, ell=0, t=1, DC=2, DD=0),
                                      dict(L=4, ell=1, t=1, DC=0, DD=1)],
                resonant_ell_zero_retained_for_all_positive_t=True)


six_family_coefficient_review = universal_six_family_review()


def model(parameters):
    r, s, z, S, T = parameters
    assert s*S % r == 0 and z*T % (r+1) == 0
    x, y = s*S//r, z*T//(r+1)
    a, b, L = s*S+1, z*T+1, T-S+1
    U, V = a+x-s, b-y+z
    q = [a, b, 1, 1]
    P = [[0, -U, x, -s], [-V, 0, -y, z],
         [r, -r-1, 0, 0], [-S, T, -L, 0]]
    assert all(sum(row) == -q[i] for i, row in enumerate(P))
    assert all(P[i][j]*P[j][i] == q[i]*q[j]-1
               for i, j in combinations(range(4), 2))
    assert all(value % 2 for value in q)
    weights = [Fraction(a), Fraction(b), Fraction(x)+Fraction(1, 2*r),
               Fraction(z)+Fraction(1, 2*T)]
    assert min(weights) > 0
    assert all(weights[j]-Fraction(P[i][j], q[i])*weights[i] > 0
               for i in range(4) for j in range(4) if i != j)
    D = [-q[i]-sum(P[j][i] for j in range(4) if i != j) for i in range(4)]
    return q, D


old_certificate = BUNDLE/"verification/book_one_negative_sector_reduction_verification_v21.json"
previous = json.loads(old_certificate.read_text())
assert previous["status"] == "PASS"
old_models = {tuple(r["fixed"]["canonical"]): r["fixed"]
              for r in previous["initial_core_records"]}
assert len(old_models) == len(previous["initial_core_records"]) == 1089

new_models = {}
family_counts = Counter()
for w in range(2, 135):
    # 134 is the inherited proved finite-certificate bound, not a new cutoff.
    for ell in range(1, w):
        if w % ell:
            continue
        t = w//ell-1
        assert t >= 1
        positive = (2*w, 2*(w+1-ell), (2*w+1)*t, w, w)
        assert positive not in new_models
        new_models[positive] = ("E_positive", ell, t)
        family_counts["E_positive"] += 1
        if ell <= w-2:
            negative = (2*w-1, (2*w-1)*t, 2*(w-1-ell), w, w)
            assert negative not in new_models
            new_models[negative] = ("E_negative", ell, t)
            family_counts["E_negative"] += 1
assert set(new_models) == set(old_models)
zero_low_D = []
for parameters, (family, ell, t) in new_models.items():
    q, D = model(parameters)
    old = old_models[parameters]
    assert old["order"] == [0, 1, 3, 4]
    assert q == [old["q"][str(k)] for k in old["order"]]
    assert D == [old["D"][str(k)] for k in old["order"]]
    expected_low = ([ell*t*t-1, -2*ell*t*t-t+1] if family == "E_positive"
                    else [-ell*t*t-1, 2*ell*t*t-t+1])
    assert D[2:] == expected_low
    assert -D[3]-2*D[2] == t+1
    if 0 in D[2:]:
        zero_low_D.append(parameters)
assert zero_low_D == [(4, 4, 5, 2, 2)]

# Universal parity: evaluate each parametrizing polynomial in F_2.
parity_rows = []
for family in ("positive_L3", "positive_L4", "positive_L3_Fnegative", "positive_L4_Fnegative",
               "negative_Epositive", "negative_Enegative"):
    for ell, t in product((0, 1), repeat=2):
        if family == "positive_L3":
            R = ell*(t+1)-2
            S, T = 3*R, 3*R+2
            s, z = 2*(ell*t-1), (2*R+1)*t
            assert R*t == ell*t*(t+1)-2*t
        elif family == "positive_L4":
            r = ell*(t+1)-3
            S, T = 2*r, 2*r+3
            s, z = ell*t-1, (r+1)*t
            assert (r+1)*t == ell*t*(t+1)-2*t
        elif family == "positive_L3_Fnegative":
            R = ell*(t+1)+2
            S, T = 3*R-2, 3*R
            s, z = (2*R-1)*t, 2*(ell*t+1)
            assert R*t == ell*t*(t+1)+2*t
        elif family == "positive_L4_Fnegative":
            r = ell*(t+1)+2
            S, T = 2*r-1, 2*r+2
            s, z = r*t, ell*t+1
            assert r*t == ell*t*(t+1)+2*t
        elif family == "negative_Epositive":
            w = ell*(t+1)
            S = T = w
            s, z = 2*(ell*t+1), (2*w+1)*t
            assert w*t == ell*t*(t+1)
        else:
            w = ell*(t+1)
            S = T = w
            s, z = (2*w-1)*t, 2*(ell*t-1)
            assert w*t == ell*t*(t+1)
        assert (s*S+1) % 2 == (z*T+1) % 2 == 1
        parity_rows.append(dict(family=family, ell_mod_2=ell, t_mod_2=t,
                                a_mod_2=1, b_mod_2=1))

# Every allowed node offset, with exact affine coefficients in w.
offsets = []
for t1, t2, tn in product((1, 2), (1, 2), (-1, 0, 1, 2)):
    # r2=w-tn, r1=(3*r2+4)/2-t2, rN=(3*r1+4)/2-t1.
    r1_coefficient, r1_constant = Fraction(3, 2), Fraction(4-3*tn, 2)-t2
    rN_coefficient = Fraction(3, 2)*r1_coefficient
    rN_constant = Fraction(3, 2)*r1_constant+2-t1
    kappa = 20-4*t1-6*t2-9*tn
    assert 4*rN_coefficient == 9 and 4*rN_constant == kappa
    offsets.append(dict(t1=t1, t2=t2, tN=tn, kappa=kappa, forced_w=-kappa))
assert len(offsets) == 16
assert min(r["kappa"] for r in offsets) == -18
assert max(r["kappa"] for r in offsets) == 19
assert max(r["forced_w"] for r in offsets) == 18 < 135
# Type II residual is 2*w-2*r1-1, identically 1 mod 2.
type_II_mod_2 = {"w": 2 % 2, "r1": -2 % 2, "constant": -1 % 2}
assert type_II_mod_2 == dict(w=0, r1=0, constant=1)

# The complement supplies an implementation independent of canonical labelling.
edges = tuple(combinations(range(5), 2))
all_edges = set(edges)
frontier = set()
counts = Counter()
degree_two = 0
for mask in range(1 << len(edges)):
    high = {e for index, e in enumerate(edges) if mask & (1 << index)}
    if len(high) < 8:
        continue
    low = all_edges-high
    if not low:
        shape = "G5_17"
    elif len(low) == 1:
        shape = "G5_16"
    else:
        first, second = tuple(low)
        shape = "G5_14" if set(first).isdisjoint(second) else "G5_15"
    counts[shape] += 1
    degrees = [sum(v in e for e in high) for v in range(5)]
    assert min(degrees) >= 2
    twos = [v for v in range(5) if degrees[v] == 2]
    assert len(twos) <= 1
    for v in twos:
        neighbours = {other for e in high if v in e for other in e if other != v}
        assert len(neighbours) == 2 and all(degrees[n] == 4 for n in neighbours)
        degree_two += 1
    for removed in range(5):
        remaining = set(range(5))-{removed}
        reached = {min(remaining)}
        while True:
            extended = reached | {v for e in high if set(e) <= remaining and set(e) & reached
                                  for v in e}
            if reached == extended:
                break
            reached = extended
        assert reached == remaining
    frontier.add(tuple(sorted(high)))
assert counts == dict(G5_14=15, G5_15=30, G5_16=10, G5_17=1)
assert len(frontier) == 56 and degree_two == 30
old_support_path = BUNDLE/"verification/support_agenda_verification_v20.json"
old_support = json.loads(old_support_path.read_text())
old_frontier = {tuple(tuple(e) for e in row["edges"]): row["shape_id"]
                for row in old_support["all_66_remaining_labelled_supports"]}
assert frontier < set(old_frontier)
removed = set(old_frontier)-frontier
assert len(removed) == 10 and {old_frontier[e] for e in removed} == {"G5_13"}

source_names = [
    "papers/sections/paper/book_complete_obstruction_v22.tex",
    "papers/sections/paper/two_high_rigid_scale_families_v22.tex",
    "papers/sections/notes/notes_book_completion_v22.tex",
    "verification/verify_book_complete_obstruction_v22.py",
    "papers/sections/paper/quintic_support_frontier_v22.tex",
    "verification/verify_support_agenda_v22.py",
    "papers/sections/paper/book_one_negative_sector_reduction_v21.tex",
    "papers/sections/paper/book_two_negative_obstruction_v21.tex",
]
source_hashes = {name: digest(BUNDLE/name) for name in source_names}
result = dict(
    status="PASS", reviewer="independent dense-v22 agent", scope="New v22 book proofs, reusable scale classification, and support frontier",
    proof_method="Human review of the unbounded inequalities and parameter quantifiers, supplemented by the exact checks recorded here",
    no_new_arbitrary_denominator_or_scale_cutoff=True,
    old_negative_certificate_range=dict(minimum_w=2, maximum_w=134,
                                        reason="Range already justified in theorem bs21:two-sectors; used only to compare independent parametrizations"),
    new_negative_parameter_count=len(new_models), negative_family_counts=dict(family_counts),
    old_negative_parameter_count=len(old_models), exact_canonical_tuple_sets_equal=True,
    all_old_q_and_D_records_equal=True, all_1089_matrices_row_pair_and_positive_weights_checked=True,
    unique_zero_low_D_model=list(zero_low_D[0]),
    six_family_coefficient_review=six_family_coefficient_review,
    parity_universal_mod_2_checks=parity_rows, type_I_all_offsets=offsets,
    type_I_forced_w_max=18, type_II_residual_mod_2=type_II_mod_2,
    support_graphs_checked=1024, support_counts=dict(counts), removed_book_labels=10,
    support_degree_two_neighbour_checks=degree_two,
    source_hashes=source_hashes,
    inherited_certificates={old_certificate.name: digest(old_certificate),
                            old_support_path.name: digest(old_support_path)},
    review_script_sha256=digest(Path(__file__)),
    limits=["The prior finite neighbour-completion certificate is an explicit inherited proof dependency; this review does not regenerate every neighbour set.",
            "The graph enumeration applies the proved arithmetic obstruction; it does not prove that obstruction.",
            "The result concerns the prescribed K5 arithmetic gluing model, not arbitrary Lagrangian torus fibrations."])
output = HERE/"book_independent_review_verification_v22.json"
output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
print(json.dumps(dict(status="PASS", negative_tuple_sets_equal=1089,
                      six_family_polynomial_identities=six_family_coefficient_review["polynomial_identity_count"],
                      universal_parity_cases=len(parity_rows), type_I_offsets=16,
                      support_counts=dict(counts), output=str(output))))
