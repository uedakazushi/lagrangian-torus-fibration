#!/usr/bin/env python3
"""Independent integer-coefficient audit of the v23 negative exceptions.

No producer code is imported or executed.  The producer JSON is read only to
compare coefficients and certificates.  This implementation uses fixed-index
monomial tuples, constructs the local residual directly from original rows,
extracts coefficients without interpolation, and computes the resultant as a
4-by-4 determinant.  Every parameter range checked symbolically is unbounded.
"""
from itertools import product, permutations
from math import comb, gcd, isqrt
from hashlib import sha256
from pathlib import Path
from functools import reduce
import argparse
import json


class Ring:
    def __init__(self, *names):
        self.names = names
        self.n = len(names)

    def p(self, value=0):
        return Poly(self, value)

    def var(self, name):
        i = self.names.index(name)
        return self.p({tuple(int(i == k) for k in range(self.n)): 1})


class Poly:
    def __init__(self, ring, value=0):
        self.ring = ring
        if isinstance(value, Poly):
            assert value.ring is ring
            self.d = dict(value.d)
        elif isinstance(value, dict):
            assert all(len(k) == ring.n and isinstance(v, int)
                       for k, v in value.items())
            self.d = {k: v for k, v in value.items() if v}
        else:
            assert isinstance(value, int)
            self.d = {(0,) * ring.n: value} if value else {}

    def __add__(self, other):
        other = self.ring.p(other)
        d = dict(self.d)
        for k, v in other.d.items():
            d[k] = d.get(k, 0) + v
        return self.ring.p(d)

    __radd__ = __add__

    def __neg__(self):
        return self.ring.p({k: -v for k, v in self.d.items()})

    def __sub__(self, other):
        return self + -self.ring.p(other)

    def __rsub__(self, other):
        return self.ring.p(other) + -self

    def __mul__(self, other):
        other = self.ring.p(other)
        d = {}
        for m, a in self.d.items():
            for n, b in other.d.items():
                k = tuple(i + j for i, j in zip(m, n))
                d[k] = d.get(k, 0) + a * b
        return self.ring.p(d)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        out = self.ring.p(1)
        for _ in range(exponent):
            out *= self
        return out

    def const(self):
        return self.d.get((0,) * self.ring.n, 0)

    def value(self, *values):
        assert len(values) == self.ring.n
        return sum(c * reduce(lambda x, y: x * y,
                              (v ** e for v, e in zip(values, mon)), 1)
                   for mon, c in self.d.items())

    def strict_sign(self):
        if self.const() > 0 and all(c > 0 for c in self.d.values()):
            return 1
        if self.const() < 0 and all(c < 0 for c in self.d.values()):
            return -1
        return 0


BI = Ring("ell", "t")
L, T = BI.var("ell"), BI.var("t")
XI = Ring("ell", "t", "X")
IDENTITIES = []


def identical(name, left, right=0):
    residual = left - right
    assert not residual.d, name
    IDENTITIES.append(name)


def lift(poly):
    poly = BI.p(poly)
    return XI.p({k + (0,): c for k, c in poly.d.items()})


def coefficients_from_original_rows(j, m, U, A, B, shift=0):
    """Clear the exact external pair after solving the two shared pairs."""
    j, U, A, B = (lift(v) for v in (j, U, A, B))
    X = XI.var("X") - lift(shift)
    Q = m * U + 1
    W = X + Q - U
    qa, qb = j * A + 1, (j + m - 1) * B + 1
    # Shared pairs give K=(qa*Q-1)/X, N=(qb*Q-1)/W.
    # External row sums give Z=qa-A+K and V=qb+B-N.
    Znum = (qa - A) * X + qa * Q - 1
    Vnum = (qb + B) * W - qb * Q + 1
    cleared = Znum * Vnum - (qa * qb - 1) * X * W
    assert all(mon[2] <= 2 for mon in cleared.d)
    coeffs = []
    for power in (2, 1, 0):
        coeffs.append(BI.p({mon[:2]: c for mon, c in cleared.d.items()
                            if mon[2] == power}))
    return tuple(coeffs)


def determinant4(matrix):
    out = BI.p()
    for perm in permutations(range(4)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(4) for j in range(i + 1, 4))
        term = BI.p(sign)
        for i in range(4):
            term *= matrix[i][perm[i]]
        out += term
    return out


def resultant_from_determinant(f, g):
    a, b, c = f
    d, e, z = g
    matrix = [[a, b, c, 0], [0, a, b, c],
              [d, e, z, 0], [0, d, e, z]]
    result = determinant4(matrix)
    assert result.d == ((a * z - c * d) ** 2 - (a * e - b * d) * (b * z - c * e)).d
    return result


def universal_bezout():
    R = Ring("a", "b", "c", "d", "e", "z", "X")
    a, b, c, d, e, z, X = (R.var(n) for n in R.names)
    f, g = a * X ** 2 + b * X + c, d * X ** 2 + e * X + z
    P, Q, W = a * e - b * d, a * z - c * d, b * z - c * e
    identical("universal_no_division_Bezout",
              Q ** 2 - P * W, (Q - P * X) * (a * g - d * f) - P * (b * g - e * f))
    return dict(division_by_leading_coefficient=False,
                degree_drop_scope="Identity holds even if either or both quadratic leading coefficients vanish")


def center(family):
    w = L * (T + 1)
    if family == "N+":
        r, S, U = 2 * w, w, w
        s, z = 2 * (w + 1 - L), (2 * w + 1) * T
        x, y = L * T + 1, w * T
    elif family == "N-":
        r, S, U = 2 * w - 1, w, w
        s, z = (2 * w - 1) * T, 2 * (w - 1 - L)
        x, y = w * T, L * T - 1
    elif family == "P+":
        R = w - 2
        r, S, U = 2 * R, 3 * R, 3 * R + 2
        s, z = 2 * (R + 1 - L), (2 * R + 1) * T
        x, y = 3 * (R + 1 - L), (3 * R + 2) * T
    elif family == "P-":
        R = w + 2
        r, S, U = 2 * R - 1, 3 * R - 2, 3 * R
        s, z = (2 * R - 1) * T, 2 * (L * T + 1)
        x, y = (3 * R - 2) * T, 3 * (L * T + 1)
    else:
        raise ValueError(family)
    a, b = r * x + 1, (r + 1) * y + 1
    identical(family + "_center_pair_with_first_low", r * x, s * S)
    identical(family + "_center_pair_with_second_low", (r + 1) * y, z * U)
    identical(family + "_center_high_pair", (a + x - s) * (b - y + z), a * b - 1)
    return dict(r=r, S=S, T=U, x=x, y=y, s=s, z=z)


def affine_substitution(poly, ell_scale, ell_offset, t_scale, t_offset):
    """Binomial expansion, independent of producer composition routine."""
    out = {}
    for (i, j), c in poly.d.items():
        for a in range(i + 1):
            ca = comb(i, a) * ell_scale ** a * ell_offset ** (i - a)
            if not ca:
                continue
            for b in range(j + 1):
                cb = comb(j, b) * t_scale ** b * t_offset ** (j - b)
                if cb:
                    key = (a, b)
                    out[key] = out.get(key, 0) + c * ca * cb
    return BI.p(out)


def certify_ratio(C, N, expected=None, resonance_allowed=False):
    # Check the zero coefficient FIRST, including in any expected-scale case.
    if not C.d:
        if not N.d:
            assert resonance_allowed
            return "identical zero, all positive scales retained"
        assert N.strict_sign()
        return "nonzero constant with zero leading coefficient"
    sign = C.strict_sign()
    assert sign, (C.d, N.d)
    if expected is not None and (N - C * expected).d == {}:
        return "unique specified scale"
    numerator = sign * N
    denominator = sign * C
    if all(c <= 0 for c in numerator.d.values()):
        return "nonpositive ratio"
    # The only possible gap is determined by the ratio at the origin;
    # there is no arbitrary search over gap indices.
    k = numerator.const() // denominator.const()
    assert k >= 0
    assert (numerator - k * denominator).strict_sign() == 1
    assert ((k + 1) * denominator - numerator).strict_sign() == 1
    return "strict interval ({},{})".format(k, k + 1)


def transfer_certificates():
    positive_domains = [
        ("r>=5,x>=2", L + 5, T + 2),
        ("r=3,x>=3", BI.p(3), T + 3),
        ("r=4,x>=3", BI.p(4), T + 3),
        ("r=3,x=2", BI.p(3), BI.p(2)),
        ("r=4,x=2", BI.p(4), BI.p(2)),
    ]
    negative_domains = [
        ("r>=5,y>=2", L + 5, T + 2, (-1, 0, 1, 2)),
        ("r=4,y>=2", BI.p(4), T + 2, (-1, 0, 1, 2)),
        ("r>=5,y=1", L + 5, BI.p(1), (-1, 0, 1, 2)),
        ("r=2,y>=2", BI.p(2), T + 2, (0, 1, 2)),
        ("r=3,y>=2", BI.p(3), T + 2, (0, 1, 2)),
    ]
    out = []
    for name, r, x in positive_domains:
        a = r * x + 1
        for nu, u, v in product(range(4), range(-4, 2), range(-4, 2)):
            j, E = r + nu - 1, a * u - x
            C, N = E * (j * v + 1) - a * j, a - 1 - E * v
            expected = {(0, 1, 1): x - 1, (1, -1, -1): BI.p(1),
                        (2, -1, -1): x + 1}.get((nu, u, v))
            disposition = certify_ratio(C, N, expected)
            out.append(dict(kind="positive_entry", region=name, offset=nu,
                            u=u, v=v, certificate=disposition))
    for name, r, y, offsets in negative_domains:
        a = (r + 1) * y + 1
        for h, u, v in product(offsets, range(-4, 2), range(-4, 2)):
            j, E = r + h, a * u + y
            C, N = E * (j * v - 1) - a * j, a - 1 - E * v
            expected = {(0, -1, -1): y - 1, (1, 1, 1): BI.p(1),
                        (2, 1, 1): y + 1}.get((h, u, v))
            resonance = name == "r>=5,y=1" and (h, u, v) == (1, -1, -1)
            disposition = certify_ratio(C, N, expected, resonance)
            out.append(dict(kind="negative_entry", region=name, offset=h,
                            u=u, v=v, certificate=disposition))
    assert len(out) == 1368
    assert sum("all positive scales" in c["certificate"] for c in out) == 1
    return out


def direct_scales(a, p, j, epsilon):
    out = []
    for u, v in product(range(-4, 2), repeat=2):
        E = a * u - p
        C, N = E * (j * v - epsilon) - a * j, a - 1 - E * v
        if C == 0:
            assert N != 0
            continue
        if N % C:
            continue
        S = N // C
        if S <= 0:
            continue
        q = 1 + j * S
        assert E * (q * v - epsilon * S) == a * q - 1
        out.append((S, u, v, q))
    return sorted(out)


def finite_transfer_boundaries():
    r2 = []
    for x in (3, 5):
        for nu in range(4):
            j = nu + 1
            values = direct_scales(2 * x + 1, x, j, -1)
            expected = {0: [(x - 1, 1, 1), (x, 0, -3)],
                        1: [(1, -1, -1)], 2: [(x + 1, -1, -1)], 3: []}[nu]
            assert [a[:3] for a in values] == sorted(expected)
            if nu == 0:
                extra = next(a for a in values if a[0] == x)
                assert extra[3] % 2 == 0
            r2.append(dict(x=x, nu=nu, candidates=values))
    # For w=2, use only the proven negative-column transfer and low D;
    # do not apply the r>=2 positive-column lemma at r=w-1=1.
    w2 = []
    for b0 in range(3):
        k = 3 - b0
        for A, u, v, qA in direct_scales(11, 5, k, -1):
            B = A - 1  # A-B+1=-D_D=2.
            qB = 1 + k * B
            assert B <= 0 or qA % 2 == 0 or qB % 2 == 0
            w2.append(dict(b0=b0, k=k, A=A, B=B, qA=qA, qB=qB))
    assert len(w2) == 4
    # r=4,y=1 is excluded by the center's even high denominator, before
    # applying the symbolic r>=5,y=1 region.
    assert (4 + 1) * 1 + 1 == 6
    return dict(r2_all_nodes=r2, w2_all_necessary_candidates=w2,
                r4_y1_even_center_denominator=6)


def first_template_checks():
    cases = [("N+", 1, 2, 6, 1, 5), ("N+", 2, 1, 8, 1, 3),
             ("N-", 1, 2, 6, 7, 3), ("N-", 2, 1, 8, 5, 3)]
    out = []
    for family, ell, t, k, A, B in cases:
        data = center(family)
        x, y, r = (data[name].value(ell, t) for name in ("x", "y", "r"))
        if family == "N+":
            assert x == 3 and k == r and (A, B) == (1, y - 1)
        else:
            assert y == 1 and k == r + 1 and (A, B) == (x + 1, 3)
        assert A - B + 1 == x - y
        coeff = [p.value(0, 0) for p in coefficients_from_original_rows(k, 1, 2, A, B)]
        divisor = reduce(gcd, (abs(c) for c in coeff if c))
        coeff = [c // divisor for c in coeff]
        if next(c for c in coeff if c) < 0:
            coeff = [-c for c in coeff]
        a, b, c = coeff
        if a:
            discriminant = b * b - 4 * a * c
            assert discriminant >= 0 and isqrt(discriminant) ** 2 != discriminant
            obstruction = dict(discriminant=discriminant, nonsquare=True)
        else:
            assert b != 0 and (-c) % b != 0
            obstruction = dict(linear_numerator=-c, linear_denominator=b,
                               nonzero_remainder=(-c) % b)
        out.append(dict(family=family, ell=ell, t=t, k=k, A=A, B=B,
                        primitive_polynomial=coeff, obstruction=obstruction))
    assert [x["primitive_polynomial"] for x in out] == [
        [0, 3, -20], [0, 34, -299], [3, -97, 544], [4, -184, 1403]]
    return out


def parity_and_cases():
    parities, cases = [], []
    for family in ("N+", "N-", "P+", "P-"):
        data = center(family)
        r, S, x, y, s, z = (data[n] for n in ("r", "S", "x", "y", "s", "z"))
        labels = list(product((-1, 1), repeat=2)) if family[0] == "N" else [(None, None)]
        for epsilon, eta in labels:
            if family[0] == "N":
                J = (r + epsilon, 2, 1, x + epsilon, y + epsilon)
                K = (S + eta, 1, 2, z + eta, s + eta)
                Q = 3
                key = (family, epsilon, eta)
            else:
                J = (r - 1, 4, 1, x - 1, y + 1)
                K = (S + 1, 1, 4, z - 1, s + 1)
                Q = 5
                key = (family,)
            high_products = [J[0] * J[3], (J[0] + J[1] - 1) * J[4],
                             K[0] * K[3], K[0] * K[4]]
            residues = []
            allowed = []
            for a, b in product(range(2), repeat=2):
                row = [p.value(a, b) % 2 for p in high_products]
                if not any(row):
                    allowed.append((a, b))
                residues.append(dict(ell=a, t=b, residues=row))
            assert allowed == [(1, 0)]
            parities.append(dict(case=key, residue_table=residues, allowed=allowed))
            for node in range(4):
                f = coefficients_from_original_rows(*J)
                g = coefficients_from_original_rows(*K, shift=Q + 1 - Q * node)
                cases.append((key + (node,), resultant_from_determinant(f, g)))
        if family == "P-":
            qK = 1 + (S + 1) * (z - 1)
            identical("Pnegative_ell_zero_entire_free_t_family",
                      affine_substitution(qK, 0, 0, 1, 0), 6)
    assert len(cases) == 40
    return parities, cases


def encoded_producer_polynomial(records, first="ell", second="t"):
    out = {}
    for row in records:
        monomial = row["monomial"]
        assert set(monomial) <= {first, second}
        n, d = row["coefficient"]
        assert d == 1
        out[(monomial.get(first, 0), monomial.get(second, 0))] = n
    return {k: v for k, v in out.items() if v}


def polynomial_hash(p):
    text = json.dumps([[a, b, c] for (a, b), c in sorted(p.d.items())], separators=(",", ":"))
    return sha256(text.encode()).hexdigest()


def full_coefficient_audit(cases, producer):
    supplied = {tuple(r["case"]): r for r in producer["resultant_certificates"]}
    assert set(supplied) == {k for k, p in cases}
    domains = [("ell>=3,t>=4", (2, 3, 2, 4)),
               ("t=2,ell>=5", (2, 5, 0, 2)),
               ("ell=1,t>=8", (0, 1, 2, 8))]
    points = [(1, 2), (3, 2), (1, 4), (1, 6)]
    out, zeros = [], []
    for key, p in cases:
        original = supplied[key]
        assert p.d == encoded_producer_polynomial(original["raw_resultant_coefficients"]), key
        regions = []
        for (name, substitution), supplied_region in zip(domains, original["tails"]):
            transformed = affine_substitution(p, *substitution)
            sign = transformed.strict_sign()
            assert sign in (-1, 1), (key, name)
            normalized = sign * transformed
            assert sign == supplied_region["normalizing_sign"]
            assert normalized.d == encoded_producer_polynomial(
                supplied_region["all_coefficients"], "v", "u"), (key, name)
            assert normalized.const() == supplied_region["strict_positive_constant"] > 0
            regions.append(dict(region=name, normalizing_sign=sign,
                                coefficient_count=len(normalized.d),
                                strictly_positive_constant=normalized.const(),
                                coefficient_sha256=polynomial_hash(normalized)))
        values = []
        for (ell, t), supplied_point in zip(points, original["finite_boundary"]):
            value = p.value(ell, t)
            assert value == supplied_point["resultant"]
            assert (ell, t) == (supplied_point["ell"], supplied_point["t"])
            if value == 0:
                assert key == ("N-", -1, -1, 2) and (ell, t) == (1, 2)
                B = center("N-")["y"].value(ell, t) - 1
                assert B == 0
                zeros.append(dict(case=key, ell=ell, t=t, B_J=B,
                                  excluded_by="positive low column is required"))
            values.append(dict(ell=ell, t=t, resultant=value))
        out.append(dict(case=key, raw_coefficient_count=len(p.d),
                        raw_coefficient_sha256=polynomial_hash(p),
                        full_raw_coefficients_match_producer=True,
                        regions=regions, points=values))
    assert len(out) == 40 and len(zeros) == 1
    return out, zeros


def locate(name, subdirectories):
    here = Path(__file__).resolve().parent
    for root in (here, *here.parents):
        for sub in ("", *subdirectories):
            path = root / sub / name
            if path.is_file():
                return path
    raise FileNotFoundError(name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer-report", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report_path = args.producer_report or locate(
        "g5_15_negative_exception_verification_v23.json", ("exceptional", "verification"))
    producer = json.loads(report_path.read_text(encoding="utf-8"))
    assert producer["status"] == "PASS"
    bezout = universal_bezout()
    transfers = transfer_certificates()
    boundaries = finite_transfer_boundaries()
    first = first_template_checks()
    parity, cases = parity_and_cases()
    certificates, zeros = full_coefficient_audit(cases, producer)
    proof = locate("g5_15_negative_exception_obstruction_v23.tex", ("exceptional", "paper"))
    source = locate("verify_g5_15_negative_exception_v23.py", ("exceptional", "verification"))
    assert sha256(proof.read_bytes()).hexdigest() == producer["proof_sha256"]
    assert sha256(source.read_bytes()).hexdigest() == producer["source_sha256"]
    output = args.output or Path(__file__).with_name("g5_15_exception_independent_review_v23.json")
    files = (Path(__file__).resolve(), proof, source, report_path)
    result = dict(
        version="v23", status="PASS", reviewer="/root/dense_v22",
        independence="No producer imports or execution; distinct integer polynomial representation, direct row residuals, determinant resultant, binomial coefficient transforms",
        scope="Independent algebra and complete symbolic-domain audit; unbounded template reduction also reviewed by hand",
        arbitrary_parameter_scan_used=False,
        universal_identities=IDENTITIES,
        resultant_degree_drop_review=bezout,
        symbolic_transfer_cases=len(transfers), transfer_certificates=transfers,
        finite_transfer_boundaries=boundaries,
        first_template_complete_cases=first,
        parity_and_full_ell_zero_resonance=parity,
        domain_coverage_reason="For odd ell>=1 and even t>=2: ell>=3,t>=4 is region A; t=2,ell>=5 is B; ell=1,t>=8 is C; the only remaining points are (1,2),(3,2),(1,4),(1,6).",
        resultant_cases=40, independent_determinants=40,
        raw_polynomial_exact_matches=40, whole_shifted_coefficient_exact_matches=120,
        endpoint_exact_matches=160, zero_endpoint_exclusions=zeros,
        coefficient_certificates=certificates,
        source_sha256={p.name: sha256(p.read_bytes()).hexdigest() for p in files},
        external_peer_review=False, proof_assistant_formalization=False)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(status="PASS", transfer_cases=1368, raw_polynomials=40,
                          coefficient_regions=120, endpoints=160,
                          zero_endpoints_excluded=len(zeros), output=str(output)), ensure_ascii=False))


if __name__ == "__main__":
    main()
