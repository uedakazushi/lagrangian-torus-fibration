#!/usr/bin/env python3
"""Independent v25 endpoint audit: no producer/verifier is imported.
Rebuilds cleared original-pair residuals and checks full coefficient signs.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse,json

N=4
class P:
    def __init__(self,a=0):
        self.a=dict(a.a) if isinstance(a,P) else ({k:v for k,v in a.items() if v} if isinstance(a,dict) else ({(0,)*N:Fraction(a)} if a else {}))
    def __add__(self,b):
        c=defaultdict(Fraction,self.a)
        for k,v in P(b).a.items():c[k]+=v
        return P(c)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.a.items()})
    def __sub__(self,b):return self+-P(b)
    def __rsub__(self,b):return P(b)+-self
    def __mul__(self,b):
        c=defaultdict(Fraction)
        for i,v in self.a.items():
            for j,w in P(b).a.items():c[tuple(i[k]+j[k] for k in range(N))]+=v*w
        return P(c)
    __rmul__=__mul__
    def __pow__(self,n):
        c=P(1)
        for _ in range(n):c=c*self
        return c
    def sub(self,*values):
        c=P()
        for k,v in self.a.items():
            t=P(v)
            for i,p in enumerate(k):t=t*P(values[i])**p
            c=c+t
        return c

def vars4():return [P({tuple(int(i==j) for i in range(N)):Fraction(1)}) for j in range(N)]

def audit():
    s,b,z,e=vars4();checks=[];pos=[]
    def eq(name,l,r):
        assert not (l-r).a,name
        checks.append({'name':name,'passed':True})
    def positive(name,p):
        assert p.a and all(v>0 for v in p.a.values()) and p.a.get((0,)*N,0)>0,name
        pos.append({'name':name,'terms':len(p.a),'minimum_coefficient':str(min(p.a.values())),
                    'constant':str(p.a[(0,)*N]),'passed':True})
    den=b+1;F=b-1+s*z;K=s*(F-1)-z+1
    # Directly clear the original residual with S=t=K/den, T=s.
    anum=(s*den+K)*z+(b-1)*den
    direct=-(s*den+b*K)*K+(s*anum-K)*s*den-anum*b*den
    c2=(s*s-1)*(s*s-b*b)
    c1=(b-1)*(-2*b*b*s-b*s-b+3*s**3-s*s-2*s)
    c0=-b**4-b**3+3*b*b*s*s-2*b*b*s+b*b-3*b*s*s+2*b*s+3*s*s-2*s
    P0=c2*z*z+c1*z+c0
    eq('n0_original_pair_to_quadratic',direct,P0)
    eq('s2_b2_exception',P0.sub(2,2,z,0),-2*(3*z-2))
    eq('s2_b3_exception',P0.sub(2,3,z,0),-(z+1)*(15*z+43))
    positive('all_s_greater_b',P0.sub(s+b+3,b+2,z+1,0))
    positive('s_equals_b_at_least_3',P0.sub(s+3,s+3,z+1,0))
    positive('b_ge_three_s_over_two',(-16*P0).sub(s+3,Fraction(3,2)*(s+3)+b,z+1,0))
    positive('z_ge_s_over_two',(-4*P0).sub(s+3,s+b+4,Fraction(1,2)*(s+3)+z,0))
    # n=z: C=(b+1)e; use all numerator expressions before division.
    C=s*s*z*(z*z+1)-3*s*(z*z+1)+2*z+1
    bn=C-e; fn=C+(s*z-2)*e
    tn=s*e+z*C+(2*s*z-3)*z*e+e*e
    SS=s+z*(s*z-2)+e; TT=s*e+z*fn
    an=(s*e+tn)*z+C-2*e
    raw=-(s*e*e+tn*bn)*SS+(s*an-tn)*TT-an*bn
    A=3*s*(z*z+1)-4*z-1
    B=3*s*s*(z*z+1)**2-2*s*(z*z+1)*(4*z+1)+5*z*z+4*z-2
    H=s*z*(z*z+1)-z*z-z+3
    R=e**4+A*e**3+B*e*e+C*H*e-C*C
    eq('nz_original_pair_cleared_without_quotient_import',raw,R)
    for name,poly in [('A',A),('B',B),('H',H)]:positive('nz_s_ge_2_'+name,poly.sub(s+2,0,z+1,0))
    positive('nz_root_below_s',R.sub(s+2,0,z+1,s+2))
    positive('nz_root_above_s_minus_one_when_z_ge_s_plus_one',(-R).sub(s+2,0,s+3+z,s+1))
    eq('s1_C',C.sub(1,0,z,0),(z-1)**3-1)
    for name,poly in [('A',A),('B',B),('H',H)]:positive('nz_s_one_'+name,poly.sub(1,0,z+2,0))
    positive('nz_s1_root_below_one',R.sub(1,0,z+2,1))
    # Verify the manuscript's nontrivial printed coefficient tables independently.
    Qs=[16*z**5+8*z**4+28*z**3+38*z*z+6*z+25,
        24*z**5+52*z**4+18*z**3+171*z*z-31*z+117,
        12*z**5+58*z**4+2*z**3+177*z*z-30*z+130,
        2*z**5+23*z**4+69*z*z-6*z+53,3*z**4+9*z*z+7]
    eq('printed_R_s_table',R.sub(s,0,z,s),sum((p*(s-2)**i for i,p in enumerate(Qs)),P()))
    Es=[(s-1)**2*(s**3+2*s*s+s-1)*(s**4+s**3-4*s+1),
        (s-1)*(6*s**7+14*s**6+14*s**5+4*s**4+4*s**3-4*s*s-24*s+13),
        15*s**7+22*s**6+8*s**5-15*s**4-34*s**3-15*s*s+38*s-10,
        2*(10*s**6+14*s**5+2*s**4-14*s**3-13*s*s+11*s-1),
        s*(15*s**4+17*s**3-6*s*s-16*s+5),2*s*s*(3*s*s+2*s-2),s**3]
    eq('printed_root_gap_table',(-R).sub(s,0,s+1+z,s-1),sum((p*z**i for i,p in enumerate(Es)),P()))
    # A concrete rejected point preserves the original equation.
    ss,bb,zz,nn,tt=3,2,1,1,10
    ff=bb-1+ss*zz;S0=tt-(ff+1)*nn;T0=ss+ff*nn;al=(ss+tt)*zz+bb-1
    rr=-(ss+tt*bb)*S0+(ss*al-tt)*T0-al*bb
    assert rr==81
    return {'identities':checks,'positive_certificates':pos,'rejected_original_residual':rr}

if __name__=='__main__':
    p=argparse.ArgumentParser();here=Path(__file__).resolve().parent
    p.add_argument('--root',type=Path,default=Path('/workspace/scratch/d5d942d05d31/deliverables/general_type_surface_fibration_v25'))
    p.add_argument('--output',type=Path,default=here/'axis_endpoints_independent_review_v25.json')
    a=p.parse_args();data=audit()
    files=['papers/sections/paper/high_d_axis_endpoints_v25.tex','verification/verify_high_d_axis_endpoints_v25.py']
    out={'version':'v25','status':'PASS','passed':True,'issues':[],**data,
         'source_sha256':{n:sha256((a.root/n).read_bytes()).hexdigest() for n in files},
         'review_script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'independence':'No producer or verifier imported; original residual rebuilt with a separate sparse rational polynomial implementation. Full nonnegative-domain coefficient signs checked. Published finite scans not repeated.',
         'quantifier_review':'Unbounded endpoint exclusions are symbolic; only fixed-s endpoints are finite. General s and interior 0<n<z remain open.',
         'external_peer_review':False,'proof_assistant_formalization':False}
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','identities':len(data['identities']),'positive_certificates':len(data['positive_certificates'])}))
