#!/usr/bin/env python3
"""Exact finite checks for the explicit degeneration and the polarization slice.

All computations use integers or fractions.  These checks supplement the proofs;
they neither prove the general-degree statements nor verify symplectic gluing.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json
import random


def triple(i, j, k):
    return (-i*j*k, i*j+i*k+j*k, -(i+j+k), 1)


def evaluate(s, point):
    return sum(point[k] * s**k for k in range(4))


def degree_case(d):
    checked_points = 0
    for i, j in combinations(range(1, d+1), 2):
        points = set()
        for r in range(d+1, 2*d+1):
            p = triple(i, j, r)
            assert evaluate(i, p) == evaluate(j, p) == evaluate(r, p) == 0
            assert all(evaluate(s, p) != 0 for s in range(1, 2*d+1)
                       if s not in (i, j, r))
            points.add(p)
        assert len(points) == d
        checked_points += len(points)
    assert checked_points == d*comb(d, 2)

    rng = random.Random(20261027+d)
    a = F(d+2, 3)
    raw = [F(rng.randint(1, 17), rng.randint(1, 11)) for _ in range(d-1)]
    total = sum((k+1)*x for k, x in enumerate(raw))
    gaps = [a*x/(2*total) for x in raw]
    beta = [F(0)]
    for gap in gaps:
        beta.append(beta[-1]+gap)
    S = sum(beta)
    areas = [a+S-d*b for b in beta]
    A = areas[-1]
    assert A == a/2
    squares = []
    for i in range(d):
        exceptionals = [beta[j]-beta[i] for j in range(i+1, d)]
        assert all(x > 0 for x in exceptionals)
        for j in range(i+1, d):
            assert areas[i]-d*(beta[j]-beta[i]) == areas[j]
        curve_bound = areas[i]-sum(exceptionals)
        assert curve_bound == a-sum(beta[i]-beta[j] for j in range(i))
        assert curve_bound >= A > 0
        square = areas[i]**2-d*sum(x*x for x in exceptionals)
        u = beta[-1]-beta[i]
        lower = A*A+2*d*A*u+d*(i+1)*u*u
        assert square >= lower > 0
        squares.append(square)
    assert sum(squares) == d*a*a
    assert areas[0]-sum(beta[j]-beta[0] for j in range(1, d)) == a

    e_core = comb(d-3, 2)
    nodes = d*comb(d, 2)
    assert d*e_core+nodes == d*(d*d-4*d+6)
    uniform_pants = d*(d-4)**2
    target_nodes = 2*d*(2*d-5)
    assert uniform_pants+target_nodes == d*(d*d-4*d+6)
    assert nodes-target_nodes == d*comb(d-4, 2)
    return {
        "degree": d, "checked_ODPs": checked_points,
        "a": str(a), "smallest_double_curve_area": str(A),
        "volume_sum": str(sum(squares)),
        "all_exact_identities": True,
        "core_Euler": e_core, "nodes": nodes,
        "uniform_pants_target": uniform_pants,
        "corresponding_node_target": target_nodes,
    }


def hexagon_case():
    L, delta = F(1), F(1, 10)
    C = L-F(3, 2)*delta
    # Constraints are (a,b,c), meaning a*x+b*y <= c.
    cuts = [(F(1),F(1),L),(-F(2),F(1),L),(F(1),-F(2),L),
            (-F(1,2),F(1),C),(F(1),-F(1,2),C),(-F(1,2),-F(1,2),C)]
    vertices = set()
    for (a,b,c),(u,v,w) in combinations(cuts, 2):
        det = a*v-b*u
        if not det:
            continue
        x,y=(c*v-b*w)/det,(a*w-c*u)/det
        if all(A*x+B*y <= K for A,B,K in cuts):
            vertices.add((x,y))
    assert len(vertices) == 6

    tested = 0
    strict_points = 0
    for ix in range(-60,61):
        for iy in range(-60,61):
            x,y=F(ix,20),F(iy,20)
            weak = [
                x>=delta and y>=delta and x+y>=L,
                -x>=delta and y-x>=delta and y-2*x>=L,
                -y>=delta and x-y>=delta and x-2*y>=L,
                abs(x)<=delta and y-x/2>=C,
                abs(y)<=delta and x-y/2>=C,
                abs(x-y)<=delta and -(x+y)/2>=C,
                all(A*x+B*y<=K for A,B,K in cuts),
            ]
            strict = [
                x>delta and y>delta and x+y>L,
                -x>delta and y-x>delta and y-2*x>L,
                -y>delta and x-y>delta and x-2*y>L,
                abs(x)<delta and y-x/2>C,
                abs(y)<delta and x-y/2>C,
                abs(x-y)<delta and -(x+y)/2>C,
                all(A*x+B*y<K for A,B,K in cuts),
            ]
            assert sum(weak) >= 1, (x,y,"gap")
            assert sum(strict) <= 1, (x,y,"interior overlap")
            if any(strict):
                assert sum(weak) == 1
                strict_points += 1
            tested += 1
    assert C+delta/2 == L-delta
    assert C-delta/2 == L-2*delta
    return {
        "L":str(L), "delta":str(delta),
        "vertices":[[str(x),str(y)] for x,y in sorted(vertices)],
        "exact_grid_points":tested,"strict_interior_points":strict_points,
        "covered_without_interior_overlap":True,
    }


def main():
    results = {
        "scope":"Finite exact checks; no analytic or symplectic existence theorem is verified by this script.",
        "degrees":[degree_case(d) for d in range(5,21)],
        "triple_chart_hexagon":hexagon_case(),
    }
    output=Path(__file__).with_name("polarization_v8_results.json")
    output.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n", encoding="utf-8")
    print("All exact checks passed; results:",output.name)


if __name__=="__main__":
    main()
