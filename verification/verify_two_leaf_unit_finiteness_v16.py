#!/usr/bin/env python3
"""Proof-derived finite reduction of the z=1, r<=4 two-leaf triangle.

Scope: leaf 4 admits a one-high normal form in which its ray 2 is C or D.
The B-only case is handled by the companion r1 exceptional-leaf certificate.
No denominator, middle parameter, or matrix entry cutoff is imposed.
All loop limits below follow from the displayed inequalities in the paper.
Only the Python standard library is used.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import importlib.util
import json


HERE = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def locate(name, folder):
    choices = [HERE / name, HERE.parent / folder / name,
               HERE.parents[1] / "deliverables/general_type_surface_fibration_v15" / folder / name]
    for p in choices:
        if p.is_file():
            return p
    raise FileNotFoundError(name)


HELPER = locate("exact_fixed_middle_completion_v15.py", "research")
SOURCE = locate("two_leaf_unit_finiteness_v16.tex", "paper")
spec = importlib.util.spec_from_file_location("fixed_middle_v15", HELPER)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


class Poly:
    def __init__(self, terms=None):
        self.terms = {m:c for m,c in (terms or {}).items() if c}

    @classmethod
    def var(cls, name):
        return cls({(name,):1})

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls({():int(value)})

    def __add__(self, other):
        ans = self.terms.copy()
        for m,c in self.coerce(other).terms.items():
            ans[m] = ans.get(m,0)+c
        return Poly(ans)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m:-c for m,c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other)-self

    def __mul__(self, other):
        ans = {}
        for m,c in self.terms.items():
            for n,d in self.coerce(other).terms.items():
                key = tuple(sorted(m+n))
                ans[key] = ans.get(key,0)+c*d
        return Poly(ans)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms


identities = []


def identity(name, lhs, rhs):
    assert lhs == rhs, name
    identities.append(name)


r,s,S,y = map(Poly.var, ("r","s","S","y"))
a = s*S+1
b = (r+1)*y+1
rA = r*a+s*S-r*s
B = r*y+2
pair = (r+2)*s*S-r*(r*s+1)*y-2*r*(s-1)
identity("Cleared AB=ab-1 is the unit-entry linear relation", rA*B-r*a*b+r, pair)
F = -r*s*s+(4*r+3)*s-r
rE = r*(r+2)*y-(s+r)*S
identity("Elimination of y gives the coefficient identity",
         F*S-(r*s+1)*rE-2*r*(r+2)*(s-1), (r+2)*pair)
for n, value in [(1,2*r+3),(2,3*r+6),(3,2*r+9),(4,12-r),
                 (5,15-6*r),(6,18-13*r)]:
    identity("F_r(%s)" % n, -r*n*n+(4*r+3)*n-r, value)
identity("Sign of F for s>=7", F, s*(r*(4-s)+3)-r)

h,t,alpha,beta,kappa = map(Poly.var, ("h","t","alpha","beta","kappa"))
L = h*h+h+1
middleS = t*(h+1)-alpha
yy = t*(4*h+3)-(h+4)*alpha-1-beta-kappa
finite_equation = (t*(h*h+7*h+3)
                   - alpha*(h*h+5*h+7)
                   - (h+4)*(1+beta+kappa)+2*h+4)
identity("Free-E branch: coefficient opposition determines y",
         yy, (h+4)*middleS-t*L-1-beta-kappa)
identity("Free-E branch: pair equation is the finite polynomial identity",
         3*(h+3)*middleS-(h+4)*yy-2*(h+2), -finite_equation)
AA = h*h+7*h+3
upper = h*h+15*h+51
identity("t is at most six", 7*AA-upper, 6*h*h+34*h-30)
identity("alpha<=0 forces h<=8", AA-(10*h+44), h*h-3*h-41)
identity("alpha=1,t>=2 forces h<=7", 2*AA-upper, h*h-h-45)
K = Poly.var("K")
identity("alpha=t=1 residual",
         (h*h+5*h+7)+(h+4)*K-2*h-4-AA, (K-4)*h+4*K)

NODES = tuple((alpha,beta,-2-alpha-beta)
              for alpha in range(-4,2) for beta in range(-4,2)
              if -4 <= -2-alpha-beta <= 1)
assert len(NODES) == 21
assert all(sum(1-v for v in q)==5 for q in NODES)
assert [(K, 4*K//(4-K)) for K in range(1,4) if 4*K%(4-K)==0] == [(2,4),(3,12)]
for rv in range(1,5):
    assert all(-rv*sv*sv+(4*rv+3)*sv-rv != 0 for sv in range(1,7))


def validate_matrix(model, qs):
    p, D = model["p"], model["D"]
    labels = sorted(qs)
    assert set(p)==set(labels)
    for i in labels:
        assert set(p[i])==set(labels) and p[i][i]==0
        assert sum(p[i].values()) == -qs[i]
        assert D[i] == -qs[i]-sum(p[j][i] for j in labels if j!=i)
    for i,j in combinations(labels,2):
        assert p[i][j]*p[j][i]==qs[i]*qs[j]-1
    for n in (2,3,4):
        for cycle in permutations(labels,n):
            if cycle[0] != min(cycle):
                continue
            gain = Fraction(1)
            for i,j in zip(cycle,cycle[1:]+cycle[:1]):
                if p[i][j] <= 0:
                    break
                gain *= Fraction(p[i][j],qs[i])
            else:
                assert gain < 1


def validate_low_edge(i,j,mi,mj):
    labels = sorted(set(mi["p"][j])-{j})
    sums = [mi["p"][j][k]+mj["p"][i][k] for k in labels]
    assert all(-4<=v<=1 for v in sums)
    assert sum(sums)==-2 and sum(1-v for v in sums)==5
    assert mi["D"][j]+mj["D"][i]==0
    return dict(edge=[i,j],punctures=labels,sums=sums,nodes=[1-v for v in sums],D_sum=0)


candidates = {}
trials = []


def trial(r,s,S,T,source,witness):
    rec = dict(source=source,parameters=dict(r=r,s=s,z=1,S=S,T=T),witness=witness)
    if min(r,s,S,T)<=0 or not (S>r and r*T>(r+1)*S):
        rec["status"]="not_positive_branch"
        trials.append(rec)
        return
    try:
        m = base.make_middle(r,s,1,S,T)
    except AssertionError:
        rec["status"]="not_integral_positive_middle"
        trials.append(rec)
        return
    key = (r,s,S,T)
    candidates.setdefault(key,dict(middle=m,witnesses=[]))["witnesses"].append(
        dict(source=source,**witness))
    rec["status"]="accepted_middle"
    trials.append(rec)


for rv,sv,SS,TT in [(1,1,2,6),(1,4,3,12),(2,2,3,6),(2,4,3,6),(2,6,3,6)]:
    trial(rv,sv,SS,TT,"small_S",{})

for rv in range(1,5):
    for sv in range(1,10):
        ff = -rv*sv*sv+(4*rv+3)*sv-rv
        assert ff != 0
        for EE in range(-2,8):
            num = rv*(rv*sv+1)*EE+2*rv*(rv+2)*(sv-1)
            rec = dict(source="bounded_E",r=rv,s=sv,E=EE,F=ff,S_numerator=num)
            if num%ff:
                rec["status"]="nonintegral_S"
                trials.append(rec)
                continue
            SS = num//ff
            ny = (rv+2)*sv*SS-2*rv*(sv-1)
            dy = rv*(rv*sv+1)
            if ny%dy or SS<4:
                rec["status"]="nonintegral_y_or_S_less_than_four"
                trials.append(rec)
                continue
            trial(rv,sv,SS,(rv+1)*(ny//dy),"bounded_E",dict(E=EE,F=ff))

for hh in range(1,5):
    for tt in range(1,4//hh+1):
        for cc in range(-4,2):
            for aa in range(-4,2):
                ss = hh+3+cc
                SS = tt*(hh+1)-aa
                rec = dict(source="free_E_leaf3_C",h=hh,t=tt,c=cc,alpha=aa,s=ss,S=SS)
                if SS<4 or ss<=0:
                    rec["status"]="small_S_or_nonpositive_s"
                    trials.append(rec)
                    continue
                ny,dy = 3*ss*SS-2*ss+2, ss+1
                if ny%dy:
                    rec["status"]="nonintegral_y"
                    trials.append(rec)
                    continue
                trial(1,ss,SS,2*(ny//dy),"free_E_leaf3_C",dict(h=hh,t=tt,c=cc,alpha=aa))

for kk in (2,5,8,10):
    for hh in range(1,13):
        for tt in range(1,7):
            for aa,bb,gg in NODES:
                lhs = tt*(hh*hh+7*hh+3)
                rhs = aa*(hh*hh+5*hh+7)+(hh+4)*(1+bb+kk)-2*hh-4
                rec = dict(source="free_E_leaf3_B",kappa=kk,h=hh,t=tt,
                           alpha=aa,beta=bb,gamma=gg,lhs=lhs,rhs=rhs)
                if lhs != rhs:
                    rec["status"]="polynomial_identity_fails"
                    trials.append(rec)
                    continue
                ss,SS = hh+3,tt*(hh+1)-aa
                ny,dy = 3*ss*SS-2*ss+2,ss+1
                if SS<4 or ny%dy:
                    rec["status"]="small_S_or_nonintegral_y"
                    trials.append(rec)
                    continue
                trial(1,ss,SS,2*(ny//dy),"free_E_leaf3_B",
                      dict(kappa=kk,h=hh,t=tt,alpha=aa,beta=bb,gamma=gg))

assert len(trials)==5+360+288+6048
assert len(candidates)==31
assert sum(len(v["witnesses"]) for v in candidates.values())==66

survivors = []
candidate_records = []
for key,record in sorted(candidates.items()):
    m = record["middle"]
    lows = base.low_completions(m,True)
    full_patches = []
    for middle,leaf3,leaf4 in lows:
        middle = dict(middle,qs={0:m["a"],1:m["b"],4:1,3:1})
        validate_matrix(middle,middle["qs"])
        validate_matrix(leaf3,{k:leaf3["q"] if k==0 else 1 for k in leaf3["p"]})
        validate_matrix(leaf4,{k:leaf4["q"] if k==1 else 1 for k in leaf4["p"]})
        edges = [validate_low_edge(2,3,middle,leaf3),
                 validate_low_edge(2,4,middle,leaf4),
                 validate_low_edge(3,4,leaf3,leaf4)]
        full_patches.append(dict(middle=middle,leaf3=leaf3,leaf4=leaf4,low_edges=edges))
    candidate_records.append(dict(parameters=m["parameters"],middle=m,
                                  witnesses=record["witnesses"],low_patch_count=len(lows)))
    if lows:
        survivors.append(dict(parameters=m["parameters"],middle=m,
                              low_patches=full_patches,low_patch_count=len(lows)))

expected = {(1,4,3,12):21,(1,7,4,18):3,(1,4,8,36):4,(1,15,12,64):3,
            (2,4,3,6):4,(2,4,12,30):5,(2,5,14,36):1,
            (4,4,18,30):1,(4,4,35,60):8,(4,4,52,90):2}
actual = {tuple(q["parameters"][k] for k in ("r","s","S","T")):q["low_patch_count"]
          for q in survivors}
assert actual == expected
assert sum(actual.values()) == 52

result = dict(
    version="v16",passed=True,
    scope="Proof-derived complete finite necessary set for z=1, r<=4, crossed two-leaf support, when leaf4 ray2 admits a C or D one-high representation. Companion B-only case must be included for a global conclusion.",
    arbitrary_denominator_cutoff=False,
    proof_derived_bounds=dict(bounded_E=[-2,7],bounded_E_s=[1,9],
                             free_E_kappa=[2,5,8,10],free_E_leaf3_C_th_max=4,
                             free_E_leaf3_C_c=[-4,1],free_E_leaf3_B_h_max=12,
                             free_E_leaf3_B_t_max=6,node_sums=[-4,1]),
    small_S_resonance="r=2,S=3,T=6; s even. The written D-opposition argument excludes s>=8, leaving s=2,4,6.",
    polynomial_identities=identities,polynomial_identity_count=len(identities),
    trial_count=len(trials),trial_status_counts=dict(Counter(q["status"] for q in trials)),
    trial_branch_counts=dict(Counter(q["source"] for q in trials)),trials=trials,
    middle_candidates=len(candidates),generation_witness_count=66,
    candidate_records=candidate_records,
    surviving_middle_count=len(survivors),surviving_low_patch_count=52,
    survivors=survivors,
    source_sha256={SOURCE.name:sha(SOURCE)},
    dependency=dict(file=HELPER.name,relative_path="research/"+HELPER.name,sha256=sha(HELPER)),
    script_sha256=sha(Path(__file__)),
    external_peer_review=False,proof_assistant_formalization=False)
target = HERE/"two_leaf_unit_finiteness_certificate_v16.json"
target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ("passed","polynomial_identity_count","trial_count",
                                      "middle_candidates","generation_witness_count",
                                      "surviving_middle_count","surviving_low_patch_count")},indent=2))
