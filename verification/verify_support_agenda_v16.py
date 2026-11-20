#!/usr/bin/env python3
"""All 1024 support graphs after the v16 two-leaf triangle obstruction.

This is a finite graph audit, not a bounded search of denominators or charts.
It preserves all established shape identifiers. The new K4 restrictions and
common-low-puncture bounds are necessary conditions, not existence assertions.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate(name, folder="verification", workfolder=None):
    choices = [HERE/name,HERE.parent/folder/name]
    if workfolder:
        choices.append(HERE.parent/workfolder/name)
    choices.append(HERE.parents[1]/"deliverables/general_type_surface_fibration_v15"/folder/name)
    for p in choices:
        if p.is_file():
            return p
    raise FileNotFoundError(name)


DEP = locate("verify_k23_obstruction_v15.py")
spec = importlib.util.spec_from_file_location("graph_base_v15",DEP)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def triangles(edges):
    es = {tuple(sorted(e)) for e in edges}
    return [list(t) for t in combinations(range(5),3)
            if all(tuple(e) in es for e in combinations(t,2))]


def is_diamond(edges):
    adj = base.adjacency(edges)
    return len(edges)==5 and sorted(map(len,adj.values()))==[0,2,2,3,3]


def is_two_leaf_triangle(edges):
    if len(edges)!=5:
        return False
    adj = base.adjacency(edges)
    ts = triangles(edges)
    if len(ts)!=1:
        return False
    cycle = set(ts[0])
    leaves = set(range(5))-cycle
    if len(leaves)!=2 or any(len(adj[v])!=1 for v in leaves):
        return False
    neighbors = [next(iter(adj[v])) for v in sorted(leaves)]
    return len(set(neighbors))==2 and set(neighbors)<=cycle


def active_connected(adj):
    active = {i for i in range(5) if adj[i]}
    if not active:
        return False
    reached,stack = {min(active)},[min(active)]
    while stack:
        i=stack.pop()
        for j in adj[i]-reached:
            reached.add(j)
            stack.append(j)
    return reached==active


def common_low_punctures(edges):
    adj=base.adjacency(edges)
    return [dict(high_edge=[i,j],common_low_core=k)
            for i,j in sorted(edges) for k in range(5)
            if k not in (i,j) and k not in adj[i] and k not in adj[j]]


def main():
    previous=locate("support_agenda_verification_v15.json")
    old=json.loads(previous.read_text())
    assert old["passed"] and old["version"]=="v15"
    assert old["unlabelled_shapes_remaining"]==13
    assert old["labelled_nonempty_supports_remaining"]==421
    old_shapes={base.canonical_edges(s["canonical_edges"]):s for s in old["shapes"]}
    assert len(old_shapes)==13

    edges_all=list(combinations(range(5),2))
    counts=Counter()
    old_counts=Counter()
    remaining_counts=Counter()
    remaining=[]
    removed=[]
    triangle_free_before=triangle_free_after=0
    for mask in range(1<<10):
        edges=[e for bit,e in enumerate(edges_all) if mask&(1<<bit)]
        reason=base.v14_filter(edges)
        if reason:
            counts[reason]+=1
            continue
        if is_diamond(edges):
            counts["diamond"]+=1
            continue
        if base.is_k23(edges):
            counts["K2_3"]+=1
            continue
        canonical=base.canonical_edges(edges)
        assert canonical in old_shapes
        old_counts[canonical]+=1
        triangle_free_before+=not bool(triangles(edges))
        if is_two_leaf_triangle(edges):
            assert old_shapes[canonical]["shape_id"]=="G5_3"
            counts["two_leaf_triangle"]+=1
            removed.append(dict(edges=edges,shape_id="G5_3"))
            continue
        adj=base.adjacency(edges)
        active=[v for v in range(5) if adj[v]]
        rank=len(edges)-len(active)+1
        assert active_connected(adj) and len(active) in (4,5)
        assert rank>=2 and len(edges)>=6 and max(map(len,adj.values()))>=3
        assert triangles(edges)
        if len(active)==4:
            assert len(edges)==6 and all(len(adj[v])==3 for v in active)
        triangle_free_after+=not bool(triangles(edges))
        counts["remaining"]+=1
        remaining_counts[canonical]+=1
        remaining.append(dict(edges=edges,shape_id=old_shapes[canonical]["shape_id"],
                              active_vertices=active,cycle_rank=rank))

    expected={
        "empty_support":1,"tree_component":300,"pure_cycle_component":37,
        "triangle_with_two_degree_two_vertices":165,"C4_with_pendant_edge":60,
        "diamond":30,"K2_3":10,"two_leaf_triangle":60,"remaining":361,
    }
    assert dict(counts)==expected and sum(counts.values())==1024
    assert len(old_counts)==13 and sum(old_counts.values())==421
    assert len(remaining_counts)==12 and sum(remaining_counts.values())==361
    assert triangle_free_before==triangle_free_after==0
    assert len(removed)==60

    shapes=[]
    excluded_shape=None
    for canonical,shape in old_shapes.items():
        assert old_counts[canonical]==shape["labelled_K5_count"]
        es=[tuple(e) for e in shape["canonical_edges"]]
        automorphisms=sum(
            {tuple(sorted((p[i],p[j]))) for i,j in es}==set(es)
            for p in base.ALL_PERMUTATIONS)
        assert automorphisms==shape["automorphism_order"]
        assert 120//automorphisms==shape["labelled_K5_count"]
        if canonical not in remaining_counts:
            assert shape["shape_id"]=="G5_3" and automorphisms==2
            excluded_shape={**shape,"v16_exclusion":"two_leaf_triangle",
                            "theorem":"tg16:no-two-leaf-triangle"}
            continue
        assert remaining_counts[canonical]==shape["labelled_K5_count"]
        adj=base.adjacency(es)
        forced=[]
        for i in range(5):
            if len(adj[i])==2:
                j,k=sorted(adj[i])
                if k not in adj[j]:
                    forced.append(i)
        shapes.append({**shape,"triangles":triangles(es),
                       "two_high_vertices_forced_positive_by_low_neighbor_edge":forced,
                       "common_low_puncture_triples":common_low_punctures(es)})
    assert len(shapes)==12 and excluded_shape is not None
    assert [s["shape_id"] for s in shapes if s["vertices"]==4]==["G4_3"]
    assert all(s["cycle_rank"]>=2 and s["edges_count"]>=6 for s in shapes)
    assert not any(s["shape_id"]=="G5_3" for s in shapes)
    assert [(s["shape_id"],s["two_high_vertices_forced_positive_by_low_neighbor_edge"])
            for s in shapes if s["two_high_vertices_forced_positive_by_low_neighbor_edge"]]==[
                ("G5_5",[3,4]),("G5_10",[4])]
    triples={s["shape_id"]:s["common_low_puncture_triples"] for s in shapes}
    assert triples["G5_5"]==[
        dict(high_edge=[0,2],common_low_core=4),
        dict(high_edge=[1,2],common_low_core=3),
        dict(high_edge=[3,4],common_low_core=2)]
    assert triples["G5_10"]==[dict(high_edge=[0,1],common_low_core=4)]

    sources={
        "quintic_support_frontier_v16.tex":locate("quintic_support_frontier_v16.tex","papers/sections/paper"),
        "notes_support_agenda_v16.tex":locate("notes_support_agenda_v16.tex","papers/sections/notes"),
        "two_leaf_global_obstruction_v16.tex":locate("two_leaf_global_obstruction_v16.tex","papers/sections/paper","root"),
        "common_low_node_bound_v16.tex":locate("common_low_node_bound_v16.tex","papers/sections/paper","small_r"),
        "k4_low_hub_reduction_v16.tex":locate("k4_low_hub_reduction_v16.tex","papers/sections/paper","k4"),
    }
    result={
        "version":"v16","passed":True,
        "scope":"Complete finite graph audit of necessary support conditions. Surviving graphs are not asserted to admit integer charts, atlases, or fibrations.",
        "graph_hypotheses":["positive integer local charts","integer marked clutching",
                            "opposing D cancellation","nonnegative nodes",
                            "standard quintic K5 branch graph"],
        "denominator_or_entry_cutoff":None,
        "labelled_K5_graphs_checked":1024,
        "labelled_nonempty_supports_remaining":361,
        "unlabelled_shapes_remaining":12,
        "four_vertex_shapes":1,"five_vertex_shapes":11,
        "canonical_rule":old["canonical_rule"],
        "shape_identifiers_preserved_from_v13_v14":True,
        "excluded_counts_in_filter_order":{k:v for k,v in expected.items() if k!="remaining"},
        "intermediate_candidate_counts":[686,521,461,431,421,361],
        "newly_excluded_shapes":[excluded_shape],
        "all_60_newly_excluded_labelled_supports":removed,
        "structural_corollaries":{
            "every_nonempty_support_contains_a_triangle":True,
            "triangle_free_support_forces_all_denominators_one":True,
            "minimum_first_betti_number":2,"minimum_high_edges":6,
            "only_four_active_vertex_candidate":"G4_3 = K4",
            "unicyclic_candidates_remaining":0,
            "triangle_free_nonempty_candidates_remaining":0,
        },
        "shapes":shapes,
        "all_361_remaining_labelled_supports":remaining,
        "research_priorities":[
            {"shape_id":"G4_3","status":"Open; exceptional edges number two or four.",
             "two_exceptional_edges":{"ordered_denominator_pairs":[[3,7],[5,9]],
                                      "ordinary_graphs":["C4","triangle with one pendant edge"],
                                      "remaining_cycle_flow_dimension_at_most":1},
             "four_exceptional_edges":{"ordinary_edge_denominators_at_most":25,
                                       "when_disjoint_at_most":7,
                                       "exceptional_denominators_bounded":False},
             "next":"Use the low-hub flow, fixed exceptional choices, three-high pair equations, and marked high-edge clutching without assuming a general matching theorem."},
            {"shape_id":"G5_5","status":"Open; degree-two vertices 3 and 4 are on the positive branch; vertex 2 may remain negative.",
             "next":"Apply the ordinary common-low reverse bound at (02;4),(12;3),(34;2), retaining maximal-divisor exceptions."},
            {"shape_id":"G5_10","status":"Open; degree-two vertex 4 is on the positive branch.",
             "next":"Apply the ordinary common-low reverse bound at (01;4), then the positive degree-two chart and marked adjacent edges."},
        ],
        "resolved_do_not_reopen":["G5_3 two-leaf triangle, including crossed positive z=1 branches and B-label exceptions",
                                  "G4_2 diamond","G5_6 K2,3"],
        "local_conditions":{
            "ordinary_common_low_reverse_absolute_value_at_most":4,
            "ordinary_bound_uses_D_opposition":False,
            "ordinary_bound_restricts_neighbor_high_degrees":False,
            "general_three_high_matching_classification":"open",
            "general_nonnegative_high_D_question":"open",
        },
        "limitations":[
            "The finite graph audit applies previously proved obstructions; it does not prove those analytic or integer obstructions by graph enumeration.",
            "K4 remains a candidate. Bounds on its ordinary edges do not bound every exceptional denominator.",
            "A local integer family or a surviving graph is not a simultaneous five-core chart or a geometric atlas.",
            "The agenda does not classify all general-type surfaces or all Lagrangian torus fibrations.",
        ],
        "previous_certificate":{"file":previous.name,"sha256":sha(previous)},
        "source_sha256":{name:sha(path) for name,path in sources.items()},
        "script_sha256":sha(Path(__file__)),
        "dependency":{"file":DEP.name,"sha256":sha(DEP)},
    }
    out=HERE/"support_agenda_verification_v16.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"passed":True,"graphs":1024,"newly_removed_labelled":60,
                      "remaining_shapes":12,"remaining_labelled":361,
                      "minimum_cycle_rank":2,"minimum_edges":6,
                      "certificate":str(out)}))


if __name__=="__main__":
    main()
