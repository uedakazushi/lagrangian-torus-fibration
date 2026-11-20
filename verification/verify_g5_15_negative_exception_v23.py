#!/usr/bin/env python3
"""Exact coefficient proof for both G5_15 negative exceptional templates.

Only the Python standard library is used. No denominator, scale, or parameter
search cutoff is used. The finite symbolic node cases and coefficient signs
cover all positive integer scales, including the explicitly excluded resonance.
"""
from fractions import Fraction
from itertools import product,permutations
from pathlib import Path
from math import gcd,isqrt
from functools import reduce
import argparse,hashlib,json

class Poly:
    """A small exact sparse polynomial implementation, independent of SymPy."""

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {m: Fraction(c) for m, c in value.items() if c}
        else:
            c = Fraction(value)
            self.terms = {(): c} if c else {}

    @classmethod
    def variable(cls, name):
        return cls({((name, 1),): 1})

    def __add__(self, other):
        other = Poly(other)
        terms = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            terms[monomial] = terms.get(monomial, 0) + coefficient
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) + (-self)

    def __mul__(self, other):
        other = Poly(other)
        terms = {}
        for m1, c1 in self.terms.items():
            for m2, c2 in other.terms.items():
                powers = dict(m1)
                for name, exponent in m2:
                    powers[name] = powers.get(name, 0) + exponent
                monomial = tuple(sorted(powers.items()))
                terms[monomial] = terms.get(monomial, 0) + c1*c2
        return Poly(terms)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        result = Poly(1)
        for _ in range(exponent):
            result = result*self
        return result

    def substitute(self, replacements):
        result = Poly()
        for monomial, coefficient in self.terms.items():
            term = Poly(coefficient)
            for name, exponent in monomial:
                term *= Poly(replacements.get(name, Poly.variable(name)))**exponent
            result += term
        return result

    def encoded(self):
        return [dict(monomial=dict(m), coefficient=[c.numerator, c.denominator])
                for m, c in sorted(self.terms.items())]


ell,t=Poly.variable('ell'),Poly.variable('t')


def center_poly(fam):
    if fam=='N+':
        w=ell*(t+1)
        r,S,T=2*w,w,w
        x,y,s,z=ell*t+1,w*t,2*(ell*t+1),(2*w+1)*t
    elif fam=='N-':
        w=ell*(t+1)
        r,S,T=2*w-1,w,w
        x,y,s,z=w*t,ell*t-1,(2*w-1)*t,2*(ell*t-1)
    elif fam=='P+':
        R=ell*(t+1)-2
        r,S,T=2*R,3*R,3*R+2
        x,y,s,z=3*(ell*t-1),T*t,2*(ell*t-1),(2*R+1)*t
    elif fam=='P-':
        R=ell*(t+1)+2
        r,S,T=2*R-1,3*R-2,3*R
        x,y,s,z=S*t,3*(ell*t+1),(2*R-1)*t,2*(ell*t+1)
    else:raise ValueError(fam)
    return dict(r=r,S=S,T=T,x=x,y=y,s=s,z=z)


def residual(j,m,U,A,B,X):
    Q=m*U+1
    W=X+Q-U
    return ((Q*j*A+Q-1+X*((j-1)*A+1))
            *(W*((j+m)*B+1)-Q*(j+m-1)*B-Q+1)
            -X*W*(j*(j+m-1)*A*B+j*A+(j+m-1)*B))


def coefficients(j,m,U,A,B,shift=0):
    c=residual(j,m,U,A,B,-shift)
    p=residual(j,m,U,A,B,1-shift)
    n=residual(j,m,U,A,B,-1-shift)
    a=(p+n-2*c)*Fraction(1,2)
    b=(p-n)*Fraction(1,2)
    assert not (residual(j,m,U,A,B,2-shift)-(4*a+2*b+c)).terms
    return a,b,c


def resultant(f,g):
    a,b,c=f
    d,e,z=g
    return (a*z-c*d)**2-(a*e-b*d)*(b*z-c*e)


def all_resultants():
    for fam in ('N+','N-'):
        v=center_poly(fam)
        r,w,x,y,s,z=(v[n] for n in ('r','S','x','y','s','z'))
        for e,h,node in product((-1,1),(-1,1),range(4)):
            Q=3
            delta=Q+1-Q*node
            R1=coefficients(r+e,2,1,x+e,y+e)
            R2=coefficients(w+h,1,2,z+h,s+h,delta)
            yield (fam,e,h,node),resultant(R1,R2)
    for fam in ('P+','P-'):
        v=center_poly(fam)
        r,S,x,y,s,z=(v[n] for n in ('r','S','x','y','s','z'))
        for node in range(4):
            Q=5
            delta=Q+1-Q*node
            R1=coefficients(r-1,4,1,x-1,y+1)
            R2=coefficients(S+1,1,4,z-1,s+1,delta)
            yield (fam,node),resultant(R1,R2)


def nonnegative(p):
    return all(c>=0 for c in p.terms.values())


def strict_sign(p):
    if p.terms.get((),0)>0 and nonnegative(p):return 1
    if p.terms.get((),0)<0 and nonnegative(-p):return -1
    return 0


def certify(C,N,expected=None,resonance=False):
    if expected is not None and not (N-C*expected).terms:
        return 'specified scale'
    if not C.terms:
        if not N.terms:return 'resonance' if resonance else 'UNEXPECTED_RESONANCE'
        if strict_sign(N):return 'inconsistent constant'
        return 'FAIL_CZERO'
    sc,sn=strict_sign(C),strict_sign(N)
    if sc and not N.terms:return 'zero scale'
    if sc and sc*sn<0:return 'opposite signs'
    if sc:
        for k in range(8):
            a=(N-k*C)*sc
            b=((k+1)*C-N)*sc
            if strict_sign(a)==1 and strict_sign(b)==1:
                return 'strict integer gap '+str(k)
    return 'FAIL'


def transfer_table_checks():
    a,b=Poly.variable('a'),Poly.variable('b')
    posregions=[('R>=5,X>=2',a+5,b+2),('R3,X>=3',Poly(3),b+3),
                ('R4,X>=3',Poly(4),b+3),('R3,X2',Poly(3),Poly(2)),('R4,X2',Poly(4),Poly(2))]
    negregions=[('R>=5,Y>=2',a+5,b+2),('R4,Y>=2',Poly(4),b+2),('R>=5,Y1',a+5,Poly(1))]
    negvariant=[('R2,Y>=2',Poly(2),b+2),('R3,Y>=2',Poly(3),b+2)]
    fails=[];passed=0
    for name,R,X in posregions:
        den=R*X+1
        for n,u,v in product(range(4),range(-4,2),range(-4,2)):
            j=R+n-1;E=den*u-X
            C=E*(j*v+1)-den*j;N=den-1-E*v
            ex= X-1 if (n,u,v)==(0,1,1) else (Poly(1) if (n,u,v)==(1,-1,-1) else (X+1 if (n,u,v)==(2,-1,-1) else None))
            s=certify(C,N,ex)
            if 'FAIL' in s or 'UNEXPECTED' in s:fails.append(('positive',name,n,u,v,s))
            else:passed+=1
    for name,R,Y in negregions+negvariant:
        den=(R+1)*Y+1
        hs=range(3) if 'R2,' in name or 'R3,' in name else range(-1,3)
        for h,u,v in product(hs,range(-4,2),range(-4,2)):
            k=R+h;E=den*u+Y
            C=E*(k*v-1)-den*k;N=den-1-E*v
            ex=Y-1 if (h,u,v)==(0,-1,-1) else (Poly(1) if (h,u,v)==(1,1,1) else (Y+1 if (h,u,v)==(2,1,1) else None))
            res=(not (Y-1).terms and (h,u,v)==(1,-1,-1))
            s=certify(C,N,ex,res)
            if 'FAIL' in s or 'UNEXPECTED' in s:fails.append(('negative',name,h,u,v,s))
            else:passed+=1
    return passed,fails


IDENTITIES=[]


def identity(name,left,right=0):
    difference=Poly(left)-right
    assert not difference.terms,(name,difference.encoded())
    IDENTITIES.append(name)


def value(poly,**kwargs):
    p=Poly(poly).substitute(kwargs)
    assert all(not m for m in p.terms)
    q=p.terms.get((),Fraction(0))
    assert q.denominator==1
    return q.numerator


def universal_identities():
    A,B,X,j,m,U=(Poly.variable(k) for k in ('A','B','X','j','m','U'))
    Q=m*U+1
    W=X+Q-U
    # Original row equations express the remaining two off-diagonal magnitudes.
    kn=Q*(j*A+1)-1
    nn=Q*((j+m-1)*B+1)-1
    zn=kn+X*((j-1)*A+1)
    vn=W*((j+m)*B+1)-nn
    original=zn*vn-X*W*((j*A+1)*((j+m-1)*B+1)-1)
    identity('cleared_original_external_pair',residual(j,m,U,A,B,X),original)
    f=X*(X+m)-(m+1)*(j-X)*(j-X-1)
    simplified=f*A*B+X*(j-X)*A+(X+m)*(X+1-j)*B+X*(X+m)
    identity('unit_reverse_column_residual',residual(j,m,1,A,B,X),simplified)
    aa,bb,cc,dd,ee,ff=(Poly.variable(k) for k in ('aa','bb','cc','dd','ee','ff'))
    syl=[[aa,bb,cc,Poly()],[Poly(),aa,bb,cc],[dd,ee,ff,Poly()],[Poly(),dd,ee,ff]]
    determinant=Poly()
    for perm in permutations(range(4)):
        inv=sum(perm[i]>perm[k] for i in range(4) for k in range(i+1,4))
        term=Poly((-1)**inv)
        for i,col in enumerate(perm):term*=syl[i][col]
        determinant+=term
    identity('quadratic_resultant_is_Sylvester_determinant',resultant((aa,bb,cc),(dd,ee,ff)),determinant)
    fpoly=aa*X*X+bb*X+cc
    gpoly=dd*X*X+ee*X+ff
    P0,Q0=aa*ee-bb*dd,aa*ff-cc*dd
    identity('division_free_Bezout_common_root_necessity',
             resultant((aa,bb,cc),(dd,ee,ff)),
             (Q0-P0*X)*(aa*gpoly-dd*fpoly)-P0*(bb*gpoly-ee*fpoly))
    for family in ('N+','N-','P+','P-'):
        c=center_poly(family)
        r,S,T,x,y,s,z=(c[k] for k in ('r','S','T','x','y','s','z'))
        identity(family+'_first_denominator',r*x,s*S)
        identity(family+'_second_denominator',(r+1)*y,z*T)
        a,b=r*x+1,(r+1)*y+1
        identity(family+'_central_high_pair',(a+x-s)*(b-y+z),a*b-1)
    return IDENTITIES


def parity_certificates():
    records=[]
    for family in ('N+','N-','P+','P-'):
        c=center_poly(family)
        r,S,x,y,s,z=(c[k] for k in ('r','S','x','y','s','z'))
        shifts=product((-1,1),repeat=2) if family[0]=='N' else [(None,None)]
        for eps,eta in shifts:
            if family[0]=='N':
                products=[(r+eps)*(x+eps),(r+eps+1)*(y+eps),(S+eta)*(z+eta),(S+eta)*(s+eta)]
            else:
                products=[(r-1)*(x-1),(r+2)*(y+1),(S+1)*(z-1),(S+1)*(s+1)]
            rows=[]
            allowed=[]
            for e0,t0 in product(range(2),repeat=2):
                residues=[value(p,ell=e0,t=t0)%2 for p in products]
                if not any(residues):allowed.append([e0,t0])
                rows.append({'ell_mod_2':e0,'t_mod_2':t0,'high_products_mod_2':residues})
            assert allowed==[[1,0]],(family,eps,eta,allowed)
            records.append({'family':family,'epsilon':eps,'eta':eta,'rows':rows,'allowed':allowed})
    # The F<0 fixed-denominator-13 resonance is retained for every t, then excluded.
    c=center_poly('P-')
    qk=1+(c['S']+1)*(c['z']-1)
    identity('full_Pnegative_resonance_has_even_high_denominator',qk.substitute({'ell':0}),6)
    return records


def first_template_boundary():
    # Four centers follow analytically from x=3 or y=1 and the complete v22 scales.
    cases=[('N+',1,2,6,1,5),('N+',2,1,8,1,3),('N-',1,2,6,7,3),('N-',2,1,8,5,3)]
    expected=[(0,3,-20),(0,34,-299),(3,-97,544),(4,-184,1403)]
    out=[]
    for (fam,e,t0,k,A,B),target in zip(cases,expected):
        C=coefficients(Poly(k),1,2,Poly(A),Poly(B))
        nums=[value(p) for p in C]
        g=reduce(gcd,(abs(v) for v in nums if v))
        nums=[v//g for v in nums]
        if next(v for v in nums if v)<0:nums=[-v for v in nums]
        assert tuple(nums)==target
        a,b,c=nums
        if a:
            disc=b*b-4*a*c
            lo=isqrt(disc)
            assert lo*lo<disc<(lo+1)*(lo+1)
            reason={'discriminant':disc,'lower_square':lo*lo,'upper_square':(lo+1)*(lo+1)}
        else:
            assert -c%b
            reason={'linear_numerator':-c,'linear_denominator':b,'remainder':-c%b}
        out.append({'family':fam,'ell':e,'t':t0,'unit_side_low_data':[k,A,B],'primitive_polynomial':nums,'exclusion':reason})
    return out


TAIL_SIGNS={
 ('N+',-1,-1):[1,1,-1,-1],('N+',-1,1):[-1,-1,-1,-1],
 ('N+',1,-1):[1,-1,-1,-1],('N+',1,1):[-1,1,-1,-1],
 ('N-',-1,-1):[-1,-1,1,-1],('N-',-1,1):[-1,-1,-1,1],
 ('N-',1,-1):[-1,-1,-1,-1],('N-',1,1):[-1,-1,1,1],
 ('P+',):[1,1,1,1],('P-',):[1,1,1,1]}


def coefficient_certificates():
    u,v=Poly.variable('u'),Poly.variable('v')
    regions=[('ell>=3,t>=4',{'ell':2*v+3,'t':2*u+4}),
             ('t=2,ell>=5',{'ell':2*v+5,'t':2}),
             ('ell=1,t>=8',{'ell':1,'t':2*u+8})]
    endpoints=[(1,2),(3,2),(1,4),(1,6)]
    records=[];zeros=[];count=0;finite=0
    for key,p in all_resultants():
        sign=TAIL_SIGNS[key[:-1]][key[-1]]
        tail=[]
        for name,sub in regions:
            shifted=p.substitute(sub)*sign
            assert nonnegative(shifted) and shifted.terms.get((),0)>0,(key,name)
            assert all(c.denominator==1 for c in shifted.terms.values())
            count+=1
            tail.append({'region':name,'normalizing_sign':sign,'coefficient_count':len(shifted.terms),
                         'strict_positive_constant':value(shifted,u=0,v=0),
                         'all_coefficients':shifted.encoded()})
        boundary=[]
        for e,t0 in endpoints:
            val=value(p,ell=e,t=t0)
            finite+=1
            if val==0:
                assert key==('N-',-1,-1,2) and (e,t0)==(1,2)
                c=center_poly('N-')
                assert value(c['y']-1,ell=e,t=t0)==0
                zeros.append({'case':key,'ell':e,'t':t0,'reason':'J-side positive low column B=y-1 is zero'})
            boundary.append({'ell':e,'t':t0,'resultant':val})
        records.append({'case':key,'raw_resultant_coefficients':p.encoded(),
                        'tails':tail,'finite_boundary':boundary})
    assert len(records)==40 and count==120 and finite==160 and len(zeros)==1
    return records,zeros


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('g5_15_negative_exception_verification_v23.json'))
    args=parser.parse_args()
    universal_identities()
    transfer_count,failures=transfer_table_checks()
    assert transfer_count==1368 and not failures
    boundary=first_template_boundary()
    parity=parity_certificates()
    certificates,zeros=coefficient_certificates()
    here=Path(__file__).resolve().parent
    proof=next((p for p in (here/'g5_15_negative_exception_obstruction_v23.tex',here.parent/'paper/g5_15_negative_exception_obstruction_v23.tex') if p.exists()),None)
    report={
      'version':'v23','status':'PASS','scope':'Both G5_15 negative exceptional templates, with all positive integer scales and no numerical search cutoff.',
      'proof_dependency':'v21 negative templates, v22 complete two-high L=1,3,4 scale families, and the v23 outer-core single-pair transfer identity.',
      'global_claim':'No G5_15 negative exceptional branch satisfies the stated necessary conditions.',
      'arithmetic':'Python standard library, exact integers and Fraction coefficients only',
      'arbitrary_parameter_cutoff':None,'old_verifier_imports':False,
      'polynomial_identity_count':len(IDENTITIES),'polynomial_identities':IDENTITIES,
      'symbolic_outer_transfer_cases':transfer_count,'symbolic_outer_transfer_failures':failures,
      'symbolic_outer_transfer_method':'Every node pair in [-4,1]^2 and each offset is covered on explicit nonnegative-coordinate domains; exact coefficient signs place every unlisted ratio below zero or strictly between consecutive integers. The Y=1 resonance is kept.',
      'first_template_four_complete_cases':boundary,'parity_certificates':parity,
      'parameter_cover':{'interior':'ell odd >=3, t even >=4','horizontal_tail':'t=2, ell odd >=5','vertical_tail':'ell=1, t even >=8','finite_points':[[1,2],[3,2],[1,4],[1,6]],'all_remaining_scales_covered':True},
      'resultant_case_count':40,'coefficient_sign_checks':120,'finite_resultant_evaluations':160,
      'finite_zero_exclusions':zeros,'resultant_certificates':certificates,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'proof_file':None if proof is None else proof.name,
      'proof_sha256':None if proof is None else hashlib.sha256(proof.read_bytes()).hexdigest(),
      'proof_assistant_formalization':False,'external_peer_review':False}
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','symbolic_outer_cases':transfer_count,'identities':len(IDENTITIES),
                      'resultants':40,'signed_coefficient_regions':120,'finite_points_checked':160,
                      'zero_endpoints_excluded_by_positivity':1,'output':str(args.output)},ensure_ascii=False))


if __name__=='__main__':main()
