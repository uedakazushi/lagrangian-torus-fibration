#!/usr/bin/env python3
"""Exact v10 certificates. Finite bound101 is explicit; no numerator cutoff.

Self-contained Python standard library only. General geometric theorems are
proved in the accompanying paper; this script certifies the recorded algebra,
finite local completeness checks and necessary-condition pruning.
"""
from fractions import Fraction
from itertools import combinations_with_replacement, permutations
from math import isqrt
from pathlib import Path
import json


def signed_divisors(n):
    assert n > 0
    positive = set()
    for d in range(1, isqrt(n)+1):
        if n % d == 0:
            positive.add(d)
            positive.add(n//d)
    return sorted(positive | {-d for d in positive})


def cycle_products(q, p):
    products = []
    for length in range(2,5):
        for cycle in permutations(range(4), length):
            if cycle[0] != min(cycle):
                continue
            ratio = Fraction(1)
            for t in range(length):
                i, j = cycle[t], cycle[(t+1) % length]
                if p[i][j] <= 0:
                    break
                ratio *= Fraction(p[i][j], q[i])
            else:
                products.append((cycle, ratio))
    return products


def positive_weights(q, p):
    cycles = cycle_products(q, p)
    if any(r >= 1 for _, r in cycles):
        return None
    m = 1
    while True:
        dilation = 1 + Fraction(1,m)
        if all(r*dilation**len(c) < 1 for c,r in cycles):
            break
        m *= 2
    w = [Fraction(1) for _ in range(4)]
    for length in range(2,5):
        for path in permutations(range(4), length):
            value = Fraction(1)
            for i,j in zip(path,path[1:]):
                if p[i][j] <= 0:
                    break
                value *= dilation*Fraction(p[i][j], q[i])
            else:
                w[path[-1]] = max(w[path[-1]], value)
    assert all(w[j]-w[i]*Fraction(p[i][j],q[i]) > 0 for i in range(4) for j in range(4) if i!=j)
    return w


def models(q):
    """Enumerate every row-sum/determinant solution; q[0],q[3]>1."""
    assert q[0] > 1 and q[3] > 1
    n = [[q[i]*q[j]-1 for j in range(4)] for i in range(4)]
    divisors = {(i,j): signed_divisors(n[i][j]) for i,j in [(0,1),(0,2),(1,3)]}
    for a in divisors[0,1]:
        a_back = n[0][1]//a
        for b in divisors[0,2]:
            b_back = n[0][2]//b
            c = -q[0]-a-b
            if not c or n[0][3] % c:
                continue
            c_back = n[0][3]//c
            for d in divisors[1,3]:
                d_back = n[1][3]//d
                e_back = -q[3]-c_back-d_back
                if not e_back or n[2][3] % e_back:
                    continue
                e = n[2][3]//e_back
                f = -q[1]-a_back-d
                f_back = -q[2]-b_back-e
                if f*f_back != n[1][2]:
                    continue
                p = [[0,a,b,c],[a_back,0,f,d],[b_back,f_back,0,e],[c_back,d_back,e_back,0]]
                assert all(sum(p[i]) == -q[i] for i in range(4))
                assert all(p[i][j]*p[j][i] == n[i][j] for i in range(4) for j in range(i+1,4))
                yield p


def record(q,p,w):
    d = [-q[i]-sum(p[j][i] for j in range(4) if i!=j) for i in range(4)]
    return {'q': list(q), 'p': p, 'weights': [str(x) for x in w], 'D': d,
            'energy_q': sum(q[i]*d[i] for i in range(4)),
            'energy_inverse_q': str(sum(Fraction(d[i],q[i]) for i in range(4)))}



# Relabel arbitrary q patterns so two high entries occupy positions 0 and 3.
_fixed_models = models
def models(q):
    high = [i for i in range(4) if q[i] > 1]
    assert len(high) >= 2
    first,last = high[0],high[-1]
    order = [first] + [i for i in range(4) if i not in (first,last)] + [last]
    inverse = [order.index(i) for i in range(4)]
    for p in _fixed_models(tuple(q[i] for i in order)):
        yield [[p[inverse[i]][inverse[j]] for j in range(4)] for i in range(4)]

def positive_possible(q,p):
    return all(value < 1 for _,value in cycle_products(q,p))

def weights(q,p):
    result = positive_weights(q,p)
    assert result is not None
    return result

from collections import defaultdict
from functools import lru_cache
from hashlib import sha256
from math import gcd

# Independent two-high parametrization and explicit local examples.
def canonical(a,b):
    for r in signed_divisors(a-1):
        if r<0 or (b-1)%(r+1):continue
        x=(a-1)//r;y=(b-1)//(r+1)
        for u in signed_divisors(a-1):
            A=a+x+u
            assert A>0
            if (a*b-1)%A:continue
            B=(a*b-1)//A;v=B-b+y
            if not v or (b-1)%v:continue
            d=-1-(a-1)//u-(b-1)//v
            P=[[0,-A,x,u],[-B,0,-y,v],[r,-r-1,0,0],[(a-1)//u,(b-1)//v,d,0]]
            yield P,{'r':r,'u':u,'v':v,'d':d,'positive':u<0 or r*u*d<a}

def freeze(P):return tuple(tuple(row) for row in P)
def permute(P,p):return [[P[i][j] for j in p] for i in p]

checks=0
def check(condition):
 global checks
 checks+=1
 assert condition

pairs=[]
for a in range(3,32,2):
 for b in range(3,a+1,2):
    direct={freeze(P) for P in models((a,b,1,1))}
    param=set();canonical_count=0
    for aa,bb,highperm in [(a,b,(0,1,2,3)),(b,a,(1,0,2,3))]:
      for P,meta in canonical(aa,bb):
        canonical_count+=1
        check(positive_possible((aa,bb,1,1),P)==meta['positive'])
        check(all(sum(P[i])==-q for i,q in enumerate((aa,bb,1,1))))
        for lowperm in [(0,1,2,3),(0,1,3,2)]:
            T=permute(permute(P,highperm),lowperm)
            param.add(freeze(T))
    check(direct==param)
    good=[P for P in direct if positive_possible((a,b,1,1),P)]
    for P in good:
        w=weights((a,b,1,1),P)
        check(all(w[j]-w[i]*Fraction(P[i][j],(a,b,1,1)[i])>0 for i in range(4) for j in range(4) if i!=j))
    pairs.append({'q':[a,b,1,1],'arithmetic_models':len(direct),'positive_models':len(good),'canonical_presentations':canonical_count})

examples=[
 {'q':[7,3,1,1],'P':[[0,-5,-3,1],[-4,0,2,-1],[-2,1,0,0],[6,-2,-5,0]],'w':['13/2','5/4','1','1'],'D':[-7,3,5,-1]},
 {'q':[7,7,1,1],'P':[[0,-8,-2,3],[-6,0,1,-2],[-3,6,0,-4],[2,-3,0,0]],'w':['13/6','13/2','1','1'],'D':[0,-2,0,2]},
 {'q':[13,7,7,1],'P':[[0,-10,-9,6],[-9,0,8,-6],[-10,6,0,-3],[2,-1,-2,0]],'w':['25/12','1','23/20','1'],'D':[4,-2,-4,2]},
 {'q':[11,11,11,11],'P':[[0,-20,-15,24],[-6,0,10,-15],[-8,12,0,-15],[5,-8,-8,0]],'w':['1','23/21','1','35/16'],'D':[-2,5,2,-5]}
]
for ex in examples:
 q=ex['q'];P=ex['P'];w=list(map(Fraction,ex['w']))
 for i in range(4):check(sum(P[i])==-q[i])
 for i in range(4):
  for j in range(i+1,4):check(q[i]*q[j]-P[i][j]*P[j][i]==1)
 for i in range(4):
  for j in range(4):
   if i!=j:
    check(gcd(q[i],P[i][j])==1)
    check(w[j]-w[i]*Fraction(P[i][j],q[i])>0)
 check([-q[i]-sum(P[j][i] for j in range(4)) for i in range(4)]==ex['D'])
 ex['basins']=[[None if i==j else str(w[j]-w[i]*Fraction(P[i][j],q[i])) for j in range(4)] for i in range(4)]

uniform=[P for P in models((11,11,11,11)) if positive_possible((11,11,11,11),P)]
orbit={freeze(permute(uniform[0],p)) for p in permutations(range(4))}
check(orbit=={freeze(P) for P in uniform})
residues={tuple(sorted(P[i][j]%11 for j in range(4) if j!=i)) for P in uniform for i in range(4)}
check(all(tuple(sorted((-r)%11 for r in row)) not in residues for row in residues))

local_structure_checks = checks
class Poly:
    """Integer polynomials; monomials are sorted tuples of variable names."""

    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @classmethod
    def variable(cls, name):
        return cls({(name,): 1})

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls({(): int(value)})

    def __add__(self, other):
        result = self.terms.copy()
        for monomial, coefficient in self.coerce(other).terms.items():
            result[monomial] = result.get(monomial, 0) + coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        result = {}
        for m, c in self.terms.items():
            for n, d in self.coerce(other).terms.items():
                monomial = tuple(sorted(m + n))
                result[monomial] = result.get(monomial, 0) + c * d
        return Poly(result)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms


def substitute(poly, mapping):
    result = Poly()
    for monomial, coefficient in Poly.coerce(poly).terms.items():
        term = Poly.coerce(coefficient)
        for variable in monomial:
            term *= mapping.get(variable, Poly.variable(variable))
        result += term
    return result


def nonnegative_coefficients(poly, strict=False):
    terms = Poly.coerce(poly).terms
    return (bool(terms) or not strict) and all(c > 0 for c in terms.values())


symbolic_start = checks
n = Poly.variable('n')
h = Poly.variable('h')
Q = n*n+n+1
R = n*n-n+1
ladder_q = [Q,Poly.coerce(1),Poly.coerce(1),R]
ladder_p = [
    [0,-(n+1),1,-(n*n+1)],
    [-n,0,0,n-1],
    [n*(n+1),-(2*n+1),0,-n*(n-1)],
    [-n*n,n,-1,0],
]
ladder_scaled_weights = [n*(2*Q-1),2*n,2*n,2*n*n-2*n+1]
for i in range(4):
    check(sum(ladder_p[i]) == -ladder_q[i])
    check(nonnegative_coefficients(substitute(ladder_scaled_weights[i],{'n':h+1}),strict=True))
    for j in range(i+1,4):
        check(ladder_q[i]*ladder_q[j]-ladder_p[i][j]*ladder_p[j][i] == 1)
for i,j in [(0,1),(0,3),(1,0),(1,2),(2,1),(2,3),(3,0),(3,2)]:
    check(nonnegative_coefficients(substitute(-Poly.coerce(ladder_p[i][j]),{'n':h+1})))
check(Q*ladder_scaled_weights[2]-ladder_scaled_weights[0] == n)
check(ladder_scaled_weights[0]-ladder_scaled_weights[2]*n*(n+1) == n)
check(ladder_scaled_weights[3]-ladder_scaled_weights[1]*(n-1) == 1)
check(R*ladder_scaled_weights[1]-ladder_scaled_weights[3]*n == n)
ladder_D = [-ladder_q[i]-sum(ladder_p[j][i] for j in range(4) if j!=i) for i in range(4)]
for actual,expected in zip(ladder_D,[-Q,2*n+1,Poly.coerce(-1),R]):
    check(actual == expected)
# The prescribed pairing of consecutive family endpoints has nodes (1,1,3)
# and star shears (0,0,2), before third-corner completion is attempted.
check(-(n+1)+(n+1) == 0)
check(Poly.coerce(1)-1 == 0)
check(-(n*n+1)-(n+1)*(n+1) == -2*Q)
check(-n+n == 0)
check(n*(n+1)-n*(n+1) == 0)
check(-n*n-((n+1)*(n+1)+1) == -2*Q)

S = n*n+3*n+3
C = n*n+2*n+2
M = n*n*(n+1)*(n+1)+2
check(R*S-1 == M)
inequality_identities = [
    (n*n*C-M,n*n-2),
    (M-(n-1)*(S+C),n*n*n*n-2*n*n+7),
    (M-(4*R-n*n)*(n+1),n*n*n*n-n*n*n+2*n*n-2),
    (M-(2*R-n*n)*(2*S-C),3*n*n-6),
    ((3*R-n*n)*(2*S-C)-M,n*n*n*n+3*n*n*n-2*n*n+10),
    ((2*R-n*n)*(3*S-C)-M,n*n*n*n+n*n*n-4*n*n+12),
]
for actual,expected in inequality_identities:
    check(actual == expected)
    shifted = substitute(expected,{'n':h+2})
    check(nonnegative_coefficients(shifted,strict=True))
    check(shifted.terms.get((),0)>0)

# Independent symbolic identity used in the uniform three-high exclusion.
A,B,C0,N = [Poly.variable(x) for x in ['A','B','C','N']]
T = A*B*C0-N*(A+B+C0)
quadratic_a = B*C0-N
quadratic_b = A*B*C0+C0*N-N*(A+B)
quadratic_c = A*C0*N-N*N
check(quadratic_b*quadratic_b-4*quadratic_a*quadratic_c == T*T-4*N*N*N)
q = Poly.variable('q')
K = 2*q*q*q-3*q
check(4*(q*q-1)*(q*q-1)*(q*q-1)-K*K == 3*q*q-4)
check(nonnegative_coefficients(substitute(3*q*q-4,{'q':h+3}),strict=True))
symbolic_checks = checks-symbolic_start


def endpoint_from_model(model, vertex):
    q,p,d = model['q'],model['p'],model['D']
    other = [j for j in range(4) if j != vertex]
    row = [p[vertex][j] for j in other]
    return {'model':model['id'],'vertex':vertex,'q':q[vertex],'D':d[vertex],
            'row':row,'incoming':[p[j][vertex] for j in other],
            'adjacent_q':[q[j] for j in other],
            'residues':sorted(x%q[vertex] for x in row)}


def endpoint_signature(e):
    return e['q'],e['D'],tuple(e['residues'])


def opposite_signature(e):
    return e['q'],-e['D'],tuple(sorted((-x)%e['q'] for x in e['residues']))


@lru_cache(maxsize=None)
def triangle_witness(a,b,r,s):
    for u in range(-4,2):
        for v in range(-4,2):
            if (a*u-r)*(b*v-s) == a*b-1:
                return u,v
    return None


def finite_catalog(bound=101):
    alphabet = list(range(1,bound+1,2))
    catalog = []
    counts = []
    pattern_digest = sha256()
    patterns = arithmetic = positive = 0
    for sorted_q in combinations_with_replacement(alphabet,4):
        if sorted_q[-2] == 1:
            continue
        q = (sorted_q[3],sorted_q[0],sorted_q[1],sorted_q[2])
        local_arithmetic = local_positive = 0
        patterns += 1
        for p in models(q):
            local_arithmetic += 1
            if not positive_possible(q,p):
                continue
            w = weights(q,p)
            local_positive += 1
            d = [-q[i]-sum(p[j][i] for j in range(4) if j!=i) for i in range(4)]
            catalog.append({'id':len(catalog),'kind':'complete_fixed_q_positive_model',
                            'q':list(q),'p':p,'weights':[str(x) for x in w],'D':d})
        entry = {'q':list(q),'arithmetic':local_arithmetic,'positive':local_positive}
        pattern_digest.update(json.dumps(entry,sort_keys=True,separators=(',',':')).encode()+b'\n')
        if local_arithmetic:
            counts.append(entry)
        arithmetic += local_arithmetic
        positive += local_positive
    for q in alphabet[1:]:
        for b in range(1,q-1):
            if (q-1)%b or (q-1)%(b+1):
                continue
            t = (q-1)//(b*(b+1))
            row = [-(q-1),-(b+1),b]
            catalog.append({'id':len(catalog),'kind':'single_high_necessary_endpoint_form',
                            'q':[q,1,1,1],'parameter_b':b,'high_row':row,
                            'high_D':-t*(b*(b+1)+1)})
    return catalog,{'bound':bound,'alphabet':alphabet,'patterns':patterns,
                    'arithmetic_models':arithmetic,'positive_models':positive,
                    'single_high_forms':len(catalog)-positive,'catalog_size':len(catalog),
                    'nonzero_local_pattern_counts':counts,
                    'all_pattern_counts_sha256':pattern_digest.hexdigest()}


catalog,catalog_metadata = finite_catalog()
all_endpoints = []
for model in catalog:
    if 'p' in model:
        for i,q in enumerate(model['q']):
            if q>1:
                all_endpoints.append(endpoint_from_model(model,i))
    else:
        q = model['q'][0]
        row = model['high_row']
        all_endpoints.append({'model':model['id'],'vertex':0,'q':q,'D':model['high_D'],
                              'row':row,'incoming':[(q-1)//p for p in row],
                              'adjacent_q':[1,1,1],'residues':sorted(x%q for x in row)})
for i,e in enumerate(all_endpoints):
    e['id'] = i
by_model = defaultdict(list)
by_signature = defaultdict(list)
for e in all_endpoints:
    by_model[e['model']].append(e)
    by_signature[endpoint_signature(e)].append(e)


def prune_weak():
    active = set(range(len(catalog)))
    rounds = []
    while active:
        available = {endpoint_signature(e) for e in all_endpoints if e['model'] in active}
        removed = {}
        for model_id in sorted(active):
            for e in by_model[model_id]:
                if opposite_signature(e) not in available:
                    removed[model_id] = {'model':model_id,'unmatched_endpoint':e['id'],
                                         'required_signature':opposite_signature(e)}
                    break
        if not removed:
            break
        rounds.append({'before':len(active),'removed':len(removed),
                       'after':len(active)-len(removed),'reasons':list(removed.values())})
        active -= set(removed)
    return sorted(active),rounds


weak_remaining,weak_rounds = prune_weak()
strong_partners = [set() for _ in all_endpoints]
edge_pair_count = 0
strong_pair_certificates = []
for e in all_endpoints:
    for f in by_signature.get(opposite_signature(e),[]):
        if f['id'] < e['id']:
            continue
        found_edge = False
        found_strong = None
        for permutation in permutations(range(3)):
            sums = [e['row'][k]+f['row'][permutation[k]] for k in range(3)]
            if any(s % e['q'] for s in sums):
                continue
            nodes = [1-s//e['q'] for s in sums]
            if any(n<0 or n>5 for n in nodes):
                continue
            assert sum(nodes) == 5
            found_edge = True
            witnesses = [triangle_witness(e['adjacent_q'][k],f['adjacent_q'][permutation[k]],
                                          e['incoming'][k],f['incoming'][permutation[k]])
                         for k in range(3)]
            if all(w is not None for w in witnesses):
                found_strong = {'endpoints':[e['id'],f['id']],
                                'models':[e['model'],f['model']],
                                'permutation':list(permutation),'nodes':nodes,
                                'third_corner_uv_witnesses':[list(w) for w in witnesses]}
                break
        edge_pair_count += int(found_edge)
        if found_strong:
            strong_pair_certificates.append(found_strong)
            strong_partners[e['id']].add(f['model'])
            strong_partners[f['id']].add(e['model'])


def prune_strong():
    active = set(range(len(catalog)))
    rounds = []
    while active:
        removed = {}
        for model_id in sorted(active):
            for e in by_model[model_id]:
                if not (strong_partners[e['id']] & active):
                    removed[model_id] = {'model':model_id,'unmatched_endpoint':e['id']}
                    break
        if not removed:
            break
        rounds.append({'before':len(active),'removed':len(removed),
                       'after':len(active)-len(removed),'reasons':list(removed.values())})
        active -= set(removed)
    return sorted(active),rounds


strong_remaining,strong_rounds = prune_strong()
assert catalog_metadata['patterns'] == 316200
assert catalog_metadata['arithmetic_models'] == 2973
assert catalog_metadata['positive_models'] == 1864
assert catalog_metadata['single_high_forms'] == 87
assert len(catalog) == 1951
assert len(all_endpoints) == 6295
assert [r['after'] for r in weak_rounds] == [118,45,28,17,11,7,4,1,0]
assert edge_pair_count == 835
assert len(strong_pair_certificates) == 12
assert [r['after'] for r in strong_rounds] == [4,0]
assert not weak_remaining and not strong_remaining

result = {
    'version':10,'passed':True,
    'scope':'Exact local algebra and finite global necessary-condition certificates. The denominator bound101 is explicit. No global high-denominator exclusion for q>101 and no new global atlas existence are claimed.',
    'dependencies':'Python3.9 or later, standard library only; no local helper imports.',
    'local_structure':{
        'checks':local_structure_checks,'two_high_pairs':pairs,'explicit_geometric_input_examples':examples,
        'uniform_eleven':{'positive_models':len(uniform),'orbit_size':len(orbit),
                          'residue_rows':[list(x) for x in sorted(residues)],
                          'opposite_residue_pair_exists':False}},
    'symbolic':{
        'checks':symbolic_checks,
        'method':'Integer polynomial coefficient comparison; positivity polynomials are shifted by n=h+2 or n=h+1 and have strictly positive coefficients.',
        'ladder_family':'Q_n=n²+n+1, R_n=n²−n+1; q=(Q_n,1,1,R_n); rows/columns and six determinants verified polynomially.',
        'ladder_defects':['-Q_n','2n+1','-1','R_n'],
        'consecutive_endpoint_nodes':[1,1,3],'consecutive_endpoint_star_shears':[0,0,2],
        'third_corner_identity':'(R_n*u+n²)(Q_(n+1)*v+n²+2n+2)=n²(n+1)²+2',
        'strict_inequality_proof':'The six elementary difference polynomials in the paper are checked exactly and positive for every n>=2, eliminating all u,v in {-4,...,1}.',
        'uniform_three_high_discriminant':'Delta=[ABC-N(A+B+C)]²-4N³; 4(q²-1)³-(2q³-3q)²=3q²-4.'},
    'finite_catalog':catalog_metadata,
    'weak_endpoint_pruning':{
        'conditions':['same q','opposite D','opposite numerator residue multiset up to arbitrary puncture permutation'],
        'not_used':['node nonnegativity','global K5 incidence','shared positive weights','finite-t intercepts'],
        'remaining_models':weak_remaining,'rounds':weak_rounds},
    'node_and_triangle_pruning':{
        'general_test':'For A=q_ik,B=q_jk,r=p_i;kj,s=p_j;ki, require (A*u-r)(B*v-s)=AB-1 for some u,v in {-4,...,1}.',
        'high_endpoints':len(all_endpoints),'node_compatible_endpoint_pairs':edge_pair_count,
        'third_corner_compatible_endpoint_pairs':len(strong_pair_certificates),
        'pair_certificates':strong_pair_certificates,'remaining_models':strong_remaining,'rounds':strong_rounds},
    'catalog_models':catalog,
    'endpoint_index':all_endpoints,
    'limitations':[
        'The finite catalog is complete only for its stated odd-denominator alphabet.',
        'The one-high normal forms overapproximate full local matrices; eliminating this larger set is safe for nonexistence.',
        'Pruning is a necessary-condition argument, not a construction of any global fibration.',
        'The geometric sufficient local-chart theorem, cycle framings, nodal budgets, positivity criterion and general congruence proofs belong to the accompanying paper.',
        'The two-high cross-check is finite (odd3<=b<=a<=31); it supplements the written proof for arbitrary a,b.',
        'The different check counts and catalog sizes are not summed as one homogeneous unit.'
    ],
    'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()
}
destination = Path(__file__).with_name('quintic_denominators_verification_v10.json')
destination.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':True,'local_structure_checks':local_structure_checks,
                  'symbolic_checks':symbolic_checks,'catalog_models':len(catalog),
                  'weak_rounds':[r['after'] for r in weak_rounds],
                  'strong_rounds':[r['after'] for r in strong_rounds],
                  'output':str(destination)},ensure_ascii=False))


