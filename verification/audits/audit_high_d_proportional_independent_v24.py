#!/usr/bin/env python3
"""Independent v24 proportional-sector coefficient audit.

No producer imports or execution. Uses packed-exponent polynomials and starts
with the original pair residual, independently clears rational denominators,
and compares every stored positive-certificate coefficient. Standard library.
"""
from __future__ import annotations
from collections import defaultdict
from hashlib import sha256
from _legacy_provenance import matches_archived_source

import argparse
import json
from pathlib import Path

RADIX=128
NVAR=5
POWERS=[RADIX**i for i in range(NVAR)]


def decode(key):
    out=[]
    for _ in range(NVAR):
        out.append(key%RADIX);key//=RADIX
    assert key==0
    return tuple(out)


class Packed:
    def __init__(self,value=0):
        if isinstance(value,Packed):self.terms=dict(value.terms)
        elif isinstance(value,dict):self.terms={k:v for k,v in value.items() if v}
        else:self.terms={0:value} if value else {}
        self.degree=tuple(max((decode(k)[i] for k in self.terms),default=0) for i in range(NVAR))
    def __add__(self,other):
        out=defaultdict(int,self.terms)
        for k,v in Packed(other).terms.items():out[k]+=v
        return Packed(out)
    __radd__=__add__
    def __neg__(self):return Packed({k:-v for k,v in self.terms.items()})
    def __sub__(self,other):return self+-Packed(other)
    def __rsub__(self,other):return Packed(other)+-self
    def __mul__(self,other):
        other=Packed(other)
        # No radix carry is possible: verify a degree bound BEFORE convolution.
        assert all(a+b<RADIX for a,b in zip(self.degree,other.degree))
        out=defaultdict(int)
        for k,v in self.terms.items():
            for q,w in other.terms.items():out[k+q]+=v*w
        return Packed(out)
    __rmul__=__mul__
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=Packed(1)
        for _ in range(n):out=out*self
        return out
    def substitute(self,values):
        values=list(values)+list(VARIABLES[len(values):])
        assert len(values)==NVAR
        values=[Packed(v) for v in values]
        powers=[{0:Packed(1)} for _ in values]
        out=Packed()
        for k,c in self.terms.items():
            term=Packed(c)
            for i,e in enumerate(decode(k)):
                if e not in powers[i]:powers[i][e]=values[i]**e
                term*=powers[i][e]
            out+=term
        return out
    def coefficient(self,var,degree):
        return Packed({k-degree*POWERS[var]:v for k,v in self.terms.items()
                       if decode(k)[var]==degree})
    def constant(self):return self.terms.get(0,0)


VARIABLES=tuple(Packed({p:1}) for p in POWERS)


def build_audit(certificate):
    identities=[];comparisons=[]
    def check(name,left,right=0):
        left,right=Packed(left),Packed(right)
        assert not (left-right).terms,(name,(left-right).terms)
        identities.append({'name':name,'status':'PASS','difference_terms':0})
    def positive(name,p,record,nvars):
        actual={decode(k)[:nvars]:v for k,v in p.terms.items()}
        assert all(not any(decode(k)[nvars:]) for k in p.terms)
        expected={tuple(x['exponents']):x['coefficient'] for x in record['full_coefficients']}
        assert actual==expected,(name,len(actual),len(expected))
        assert all(c>0 for c in actual.values()) and p.constant()>0
        comparisons.append({'name':name,'coefficients':len(actual),'constant':p.constant(),
                            'all_coefficients_exactly_equal':True,'all_nonzero_coefficients_positive':True})

    # x>=2: derive the clearing directly from the three terms of r.
    h,x,w,z,_=VARIABLES
    s=h+x;j=h+w;dnum=x*(h+j)+h*(z-1)
    lambda_num=h*h+s*dnum
    bnum=dnum*(s*h-1)+h*h*(h-3)-h*w
    alpha_num=h*bnum-h*h*w+w*(h+j)*lambda_num
    term_one=-(s*h*h*w+s*j*bnum)*j*h*w
    term_two=(s*alpha_num-s*j*h*w)*h*h*w
    term_three=-alpha_num*bnum
    residual_clear=term_one+term_two+term_three
    N=-alpha_num*(s*h*h*w-bnum)+2*s*j*h**3*w*w+bnum*s*j*j*h*w
    check('off_axis_original_three_term_residual',residual_clear,-N)
    shifted=(-residual_clear).substitute([h+1,x+2,w+1,z])
    positive('x>=2 infinite domain',shifted,certificate['off_axis_positive_certificate'],4)
    assert len(shifted.terms)==281 and shifted.constant()==312

    # x=1: reconstruct alpha and the residual before extracting k coefficients.
    h,z,k,_,_=VARIABLES
    s=h+1;b=h+k;den=h*k+1
    vnum=(h*h+h-1)*z+2*h*h-2*h-1
    lamnum=h*den+s*(vnum+(z+1)*den)
    anum=(b-1)*den*den+lamnum*(vnum+2*den)
    R=anum*(s*h-b)-s*h*(vnum+den)*(2*den+b*(vnum+den))
    R0=h*h*(h+1)*(h*h+h-1)*z*z+h*(4*h**4+h**3-6*h*h+2)*z+h*h*(4*h**3-6*h*h+3)
    R_at_one=-h*(h+1)**2*((h*h+h-1)*z*z+h*(3*h+1)*z+2*h*h+1)
    check('x_one_k_zero_formula',R.substitute([h,z,0]),R0)
    check('x_one_k_one_formula',R.substitute([h,z,1]),R_at_one)
    record=certificate['x_one_sign_certificates']
    positive('x=1 h>=2 k=0',R0.substitute([h+2,z,k]),record[0],3)
    for i in range(1,5):
        positive('x=1 negative coefficient k^'+str(i),
                 (-R.coefficient(2,i)).substitute([h+2,z,k]),record[i],3)
    hp=k**4+13*k**3+37*k*k+38*k+12+(4*k**3+25*k*k+38*k+16)*z+(2*k*k+8*k+4)*z*z
    check('h_one_boundary_formula',-R.substitute([1,z,k+1]),hp)
    positive('x=1 h=1 k>=1',hp,record[5],3)

    # x=y=0: use the actual canonical residual, with t still free.
    s,b,z,n,t=VARIABLES
    F=b-1+s*z;m=F*F+F+1;K=s*(F-1)-z+1
    S=t-(F+1)*n;T=s+F*n;u=s+t-1;ell=u+z
    alpha=(s+t)*z+b-1
    original=-(s+t*b)*S+(s*alpha-t)*T-alpha*b
    expression=-b*t*t+(s*s*z-2*s-b*z)*t+F*(s*s-b)+n*(s*m+(F*F+b)*t)
    check('zero_axis_original_residual_formula',original,expression)
    W=(alpha+1)*s-ell
    check('zero_axis_scale_difference',(F+1)*S+T-W,(b+1)*t-m*n-K)
    den=b+1;tn=m*n+K
    Sn=tn-(F+1)*n*den
    an=(s*den+tn)*z+(b-1)*den
    direct=-(s*den+b*tn)*Sn+(s*an-tn)*T*den-an*b*den
    P=-b*tn*tn+den*(s*s*z-2*s-b*z)*tn+den*den*F*(s*s-b)
    P+=n*(s*m*den*den+(F*F+b)*tn*den)
    check('zero_axis_denominator_clearing',direct,P)
    check('quartic_leading_coefficient',P.coefficient(1,4),n*n-z*n-1)
    assert P.degree[1]==4
    width=direct.substitute([s+1,b+2,z+1,z+n+2,0])
    positive('n>=z+1 infinite domain',width,certificate['zero_axis_lattice_width_certificate'],4)
    assert len(width.terms)==209 and width.constant()==63

    # Added divisor remainder and all zero remainders.
    Cn=n*((s*z)**2-3*s*z+3)+(s*s-1)*z-3*s+1
    check('divisor_remainder',tn,den*(s+n*(b+2*s*z-2))+Cn)
    check('resonance_s3_z1_n0',tn.substitute([3,b,1,0,0]),3*(b+1))
    check('resonance_s1_z2_n2',tn.substitute([1,b,2,2,0]),(b+1)*(2*b+5))
    check('resonance_original_residual',original.substitute([1,b,2,2,2*b+5]),-b*b+5*b+17)
    C0=Cn.substitute([s,b,z,0,0])
    check('C0_s1',C0.substitute([1,b,z,0,0]),-2)
    check('C0_s2',C0.substitute([2,b,z,0,0]),3*z-5)
    check('C0_s3',C0.substitute([3,b,z,0,0]),8*(z-1))
    s4=C0.substitute([s+4,b,z+1,0,0])
    assert all(v>0 for v in s4.terms.values()) and s4.constant()==4
    assert 9*9<93<10*10

    # Exact quartic coefficients in all six supplied complete fixed-data fixtures.
    fixture_matches=[]
    for fixture in certificate['finite_axis_fixtures']:
        ss,zz=fixture['fixed_s'],fixture['fixed_z']
        for row in fixture['quartics']:
            nn=row['n'];coefs=[]
            fixed=P.substitute([ss,b,zz,nn,0])
            for j0 in range(5):
                term=fixed.coefficient(1,j0)
                assert all(k0==0 for k0 in term.terms)
                coefs.append(term.constant())
            assert coefs==row['quartic_coefficients_ascending']
            cvalue=Cn.substitute([ss,b,zz,nn,0])
            assert all(k0==0 for k0 in cvalue.terms)
            assert cvalue.constant()==row['divisor_remainder_Cn']
            fixture_matches.append({'s':ss,'z':zz,'n':nn,'quartic_coefficients_match':True,
                                    'divisor_remainder_match':True})
    return identities,comparisons,fixture_matches


def first_existing(paths):
    return next(p for p in paths if p.is_file())


def main():
    here=Path(__file__).resolve().parent
    work=here.parent/'highd_proportional'
    bundle=here.parent.parent
    parser=argparse.ArgumentParser()
    parser.add_argument('--proof',type=Path,default=None)
    parser.add_argument('--primary',type=Path,default=None)
    parser.add_argument('--certificate',type=Path,default=None)
    parser.add_argument('--output',type=Path,default=here/'high_d_proportional_independent_review_v24.json')
    args=parser.parse_args()
    proof=args.proof or first_existing([work/'high_d_proportional_reduction_v24.tex',bundle/'papers/sections/paper/high_d_proportional_reduction_v24.tex'])
    primary=args.primary or first_existing([work/'verify_high_d_proportional_v24.py',bundle/'verification/verify_high_d_proportional_v24.py'])
    cert=args.certificate or first_existing([work/'high_d_proportional_verification_v24.json',bundle/'verification/high_d_proportional_verification_v24.json'])
    data=json.loads(cert.read_text())
    assert data['status']=='PASS'
    assert matches_archived_source(primary, data['source_sha256'])
    assert data['proof_sha256']==sha256(proof.read_bytes()).hexdigest()
    identities,comparisons,fixtures=build_audit(data)
    result={'version':'v24','status':'PASS','reviewer':'highd_axis_v24',
            'independence':'No producer imports or execution. Packed-exponent integer convolution with checked radix bounds; original residuals independently cleared before full coefficient comparison.',
            'identity_count':len(identities),'identities':identities,
            'full_positive_coefficient_comparisons':comparisons,
            'fixed_fixture_quartics':fixtures,
            'mathematical_read_through':[
                'delta=0 implies j=th/s>0; F>=h+1 gives n>=0; x>=1 then forces n=0 without relabelling s,t.',
                'x>=2 clearing has positive factor h^3 w^2; all 281 coefficients and constant312 are exactly reproduced.',
                'x=1 uses the integrality of b to pass from hb-h^2+1>0 to b>=h. k=0 is positive, k>=1 strictly negative; h=1 covered separately.',
                'Zero-axis n>=z+1 clearing has 209 positive coefficients and constant63; no denominator cutoff used.',
                'The quartic has leading coefficient n^2-zn-1<0 on 0<=n<=z; integer-root enumeration is finite even when constant terms vanish.',
                'Divisor remainder Cn has precisely the two stated zero cases; the first has t=s, the second has nonsquare discriminant93. Other nonpositive cases are -1,-2.',
                'Fixed(s,z) reconstruction retains all original pair products and positive weights; no global proportional nonexistence is claimed.'
            ],
            'issues':[], 'source_sha256':{
                Path(__file__).name:sha256(Path(__file__).read_bytes()).hexdigest(),
                proof.name:sha256(proof.read_bytes()).hexdigest(),
                primary.name:sha256(primary.read_bytes()).hexdigest(),
                cert.name:sha256(cert.read_bytes()).hexdigest()},
            'external_peer_review':False,'proof_assistant_formalization':False,
            'bounded_parameter_scan_used':False}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','identities':len(identities),
                      'full_positive_certificates':len(comparisons),'fixture_quartics':len(fixtures)}))


if __name__=='__main__':main()
