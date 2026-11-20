"""Independent exact audit: Kronecker-encoded polynomials, original residuals.

No producer program is imported or executed. The radix encoding is injective
because every checked expression has total degree strictly less than RADIX.
"""
from pathlib import Path
from fractions import Fraction
from math import comb
import hashlib
import json

RADIX=64


class KPoly:
    def __init__(self, terms=0, degree=0):
        if isinstance(terms,KPoly):
            self.c=dict(terms.c);self.degree=terms.degree
        elif isinstance(terms,dict):
            self.c={k:Fraction(v) for k,v in terms.items() if v};self.degree=degree
        else:self.c={0:Fraction(terms)} if terms else {};self.degree=0
    def __add__(self,other):
        other=KPoly(other);d=dict(self.c)
        for e,c in other.c.items():d[e]=d.get(e,0)+c
        return KPoly(d,max(self.degree,other.degree))
    __radd__=__add__
    def __neg__(self):return KPoly({e:-c for e,c in self.c.items()},self.degree)
    def __sub__(self,other):return self+-KPoly(other)
    def __rsub__(self,other):return KPoly(other)+-self
    def __mul__(self,other):
        other=KPoly(other);d={}
        assert self.degree+other.degree<RADIX
        for e,c in self.c.items():
            for f,v in other.c.items():d[e+f]=d.get(e+f,0)+c*v
        return KPoly(d,self.degree+other.degree)
    __rmul__=__mul__
    def __pow__(self,n):
        result=KPoly(1)
        for _ in range(n):result=result*self
        return result


def V(i):return KPoly({RADIX**i:1},1)


def quadratic_resultant(f,g):
    a,b,c=f;d,e,h=g
    return (a*h-c*d)**2-(a*e-b*d)*(b*h-c*e)


def shifted_coefficients(poly,shift):
    assert all(0<=e<RADIX for e in poly.c)
    out={}
    for e,c in poly.c.items():
        for j in range(e+1):out[j]=out.get(j,0)+c*comb(e,j)*shift**(e-j)
    return [int(out.get(i,0)) for i in range(max(poly.c)+1)]


def run():
    identities=[]
    def eq(name,left,right=0):
        left,right=KPoly(left),KPoly(right)
        assert not (left-right).c,name
        identities.append({'name':name,'status':'PASS','total_degree_bound':max(left.degree,right.degree)})

    B,z,t,p=[V(i) for i in range(4)]
    b=B+1;F=B+z;m=F*F+F+1
    S=(F+1)*p-z-1;T=t+z+1-F*p;alpha=t*(z+1)+F
    original=-(1+t*b)*S+(alpha-t)*T-alpha*b
    Q=(z-1)*(t-1)-m*p+F*(z+2)
    C=F+2;R=t-B*(p+z+1);N=b*b+b*z+z*z;K=(z+1)*F+1
    eq('axis_original_pair_residual',original,(t+1)*Q+t*R-B*C)
    eq('axis_difference_elimination',B*Q,m*R+B*C*K-N*t)
    eq('axis_mod_C',m,C*(F-1)+3)

    s,k,L,y=[V(i) for i in range(4)]
    K0=s*s-s+1;w=L+1-k*K0;D=s*(w+k)+1
    B=s*k;b=B+1;F=s*L;u=k*(s*L+1);t=u-s+1;z=L-k
    T=k*(s*k+2);ell=u+z
    S=F*T-B*(t-y)-ell;alpha=u*(y+z)+B+z
    original=-(s+t*b)*S+(s*alpha-t)*T-alpha*b
    Q=s*L*w-s*k*k+s-2*k
    eq('degenerate_scale',S,(s*k-1)*L+s*k*(s-k-1+y))
    eq('degenerate_original_residual',original,k*(t*(s*w-1)-D*y))
    A=s*s*K0*k*k+s*(s-1)**2*k-(s*s+s+1)
    G=s*s*(s-1)*k*k-s*k-s+1;H=(s*k+2)*G
    eq('degenerate_divisor_A',s*Q+A,D*(k*s*s*(s-1)+s*w-s-1))
    eq('degenerate_divisor_H',t*(s*w-1)+H,D*(k*k*s*s*(s-1)+k*s*w-k*s-k-s+1))
    r=k-K0*w
    eq('degenerate_small_cofactor',k*(s*r+2)-s*(w*w-w+1),-Q)

    s=V(0);K0=s*s-s+1;Cs=K0*((s-1)**4+3)
    f=[s*s*K0,s*(s-1)**2,-(s*s+s+1)]
    g=[s*s*(s-1),-s,-s+1]
    lin=f[0]*4-f[1]*(2*s)+f[2]*s*s
    quad=quadratic_resultant(f,g)
    eq('resultant_A_linear',lin,s*s*K0)
    eq('resultant_A_G',quad,-s**6*((s-1)**4+3))
    eq('resultant_product',lin*quad,-s**8*Cs)
    eq('cofactor_bound_gap',s*s*(K0+1)**2-Cs,
       3*s**4*(s-2)+10*s*s*(s-1)+8*s-4)

    # Cs-4 is divisible by the polynomial variable s; no numeric division.
    numer=Cs-4
    assert 0 not in numer.c and all(e<RADIX for e in numer.c)
    M=KPoly({e-1:c/Fraction(4) for e,c in numer.c.items()},numer.degree-1)
    qa=s*K0;qb=2-s*(M*(K0-2)+1);qc=-s*(M*(M-1)+1)
    disc=qb*qb-4*qa*qc
    P=s**8-6*s**7+17*s**6-30*s**5+41*s**4-44*s**3+34*s*s-20*s-2
    W=2*s**7-13*s**6+34*s**5-73*s**4+100*s**3-106*s*s+68*s-15
    eq('square_interval_identity',16*disc,P*P-4*W)
    G=2*P-1-4*W
    wc=shifted_coefficients(W,4);gc=shifted_coefficients(G,4)
    assert wc==[609,6324,8934,5652,1967,394,43,2]
    assert gc==[26135,42152,34636,19704,8134,2316,422,44,2]
    assert min(wc)>0 and min(gc)>0
    assert 3*((3*3-3+2)**2+1)+1==196
    assert (3*3-3+1)*((3-1)**4+3)==133

    here=Path(__file__).resolve().parent
    if (here.parent/'highd_axis').is_dir():
        producer=here.parent/'highd_axis'
        proof=producer/'high_d_axis_and_degenerate_obstruction_v24.tex'
        source=producer/'verify_high_d_axis_degenerate_v24.py'
        result=producer/'high_d_axis_degenerate_verification_v24.json'
    else:
        root=here.parent.parent
        proof=root/'paper/high_d_axis_and_degenerate_obstruction_v24.tex'
        source=root/'verification/verify_high_d_axis_degenerate_v24.py'
        result=root/'verification/high_d_axis_degenerate_verification_v24.json'
    paths=[proof,source,result,Path(__file__).resolve()]
    data={
        'version':'v24','status':'PASS','reviewer':'root',
        'independence':'No producer import/execution. Separate sparse univariate Kronecker encoding with proved injective degree bound, original residual reconstruction, division-free quadratic resultant formula, binomial shifted coefficients.',
        'radix':RADIX,'maximum_total_degree_bound':max(r['total_degree_bound'] for r in identities),
        'exact_identity_count':len(identities),'identities':identities,
        'square_gap_coefficients':{'W(s+4)':wc,'2P(s+4)-1-4W(s+4)':gc},
        'unbounded_argument_review':[
            'Axis z=1 separately excluded; positive p and tR=BC retained from original residual.',
            'R<=B, k=R^2/B positive integer, C>=5k and C divides 3k form the contradiction.',
            'Degenerate s divides B from two consecutive product divisibilities.',
            'Integral resultant argument does not divide a leading coefficient; gcd(D,s)=1 cancels s^8.',
            'r=0 and r>=1 branches, s=3 and s=4 endpoints, cofactor4 and consecutive-square gap covered.',
            'Fixed-s bound uses the old valid R0 bound, original-residual divisibility, and the new exclusion of x=0,R0=1.',
        ],
        'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        'arbitrary_parameter_scan_used':False,
        'external_peer_review':False,'proof_assistant_formalization':False,
    }
    out=here/'high_d_axis_independent_review_v24.json'
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:data[k] for k in ['status','exact_identity_count','maximum_total_degree_bound']}))


if __name__=='__main__':run()
