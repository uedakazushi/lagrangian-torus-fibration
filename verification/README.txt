第25版の数学検算・独立監査

最初にbundle直下の00_CONTINUATION_POLICY_ja.txtを読み、主張の量化を確認する。
このディレクトリは主検算89本と数学的結果JSON89件を含む。
audits/には追加の実行可能監査24本を含む。
旧v24の84主検算・84数学的結果・19監査scriptおよび保持した旧TeXは内容不変。
新五主検算・新五独立監査は最終source/proofに対して実行済み。
古い有界scanは同じ理由だけでは再実行しない。build.shは全履歴を含む完全再現用である。

新しい主結果と検算：
  verify_four_ray_matching_v25.py
    四行・五pairから第六pair残余を再構成し、P4を正値恒等式で無上界排除。
    weights無しのmatching/triangle分類、正weights iff matching。全64符号graph。
  verify_g514_five_node_v25.py --proof paper/g514_five_node_exclusion_v25.tex
    G5_14の五node単位枝を全尺度で排除。七局所型・LM=8,20の全36正因子。
    恒等零二型も元pairの整除障害を確認。有限パラメータscanによる証明ではない。
  verify_g514_central_matching_v25.py --proof paper/g514_central_matching_v25.tex
    G5_14の中央matchingを{01,23}に固定。16標識配置→4正規形、全node0配置。
    G5_14全体の存在・不存在は主張しない。G5_16へ二単位枝の議論を移さない。
  verify_high_d_axis_endpoints_v25.py --s-cap 400
    比例零軸端点n=0,zの無上界符号・整数間隙証明。固定sだけで完全有限復元。
    16恒等式、13正係数証明。1<=s<=400で模型なしという有限結果を全域へ外挿しない。
  verify_degenerate_divisor_v25.py --fixed-b 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
    a=0の元残余r=M(t-y)-tT、正整数L,M、hM=(b-1)L。
    h>=bでgcd(h,b-1)=1を排除。x>=1に対する固定bの完全有限復元。
    a=0全体の不存在は主張しない。x=0,h<bは既存固定s手順を保持する。

新しい独立監査：
  audit_four_ray_matching_independent_v25.py
    主checker未import。原有理式、第六残余、全符号graph、正weight gapを別に検算。
  audit_g514_five_node_independent_v25.py
    原coreをQ[B]上に再構成。36全因子の216pair・108row恒等式と全例外を確認。
  audit_g514_central_matching_independent_v25.py
    全標識置換、one-positive正常形、原clutchingと最終行和障害を独立確認。
  audit_axis_endpoints_independent_v25.py
    別の疎多項式実装で元残余を分母払った式から再導出。全係数正値性を検査。
  audit_degenerate_divisor_v25.py
    別の多項式実装と、L/gcd枝刈りを使わないF二次式復元で独立照合。

各証明書にsource/proof SHA256、入力範囲、実際の結果を記録する。
新sourceの最終hashはaudits/new_verification_runs_v25.jsonにもまとめる。
無上界の手計算、全係数証明、全有限型・全因子、固定入力の有限復元、有界回帰、特定例を区別する。
全てPython標準ライブラリで実行できる。内部点検は外部査読やproof assistant形式化ではない。
有限検算はMoser法、解析的gluing、Lagrangian fibrationの存在証明の代用ではない。

現行高分母support証明書はsupport_agenda_verification_v23.json（3型26標識）。
旧4型56標識はG5_15排除前の中間段階。安定graph識別子を詰め直さない。
旧全q<=101の排除はその上限付き結果。旧144低行検算は1<=s,t<=12に限る。
異なる結果の重複した候補数を加算しない。

主検算script一覧：
  verify_book_all_negative_v20.py
  verify_book_complete_obstruction_v22.py
  verify_book_low_D_cycle_v20.py
  verify_book_low_triangle_v19.py
  verify_book_one_negative_sector_reduction_v21.py
  verify_book_two_negative_obstruction_v21.py
  verify_bounded_reverse_catalog_v13.py
  verify_c4_no_D_v13.py
  verify_c4_pendant_v14.py
  verify_c5_obstruction_v13.py
  verify_common_low_node_bound_v16.py
  verify_core_surgery_v8.py
  verify_cycle_completion_v12.py
  verify_cycle_node_conditions_v12.py
  verify_degenerate_divisor_v25.py
  verify_degree_two_triangle_v14.py
  verify_denominator_rigidity_v9.py
  verify_dense_prime_support_v11.py
  verify_diamond_independent_audit_v15.py
  verify_diamond_v15.py
  verify_equal_two_high_negativity_v11.py
  verify_fixed_denominator_partners_v12.py
  verify_forest_obstruction_v13.py
  verify_four_ray_matching_v25.py
  verify_four_ray_positive_graph_v24.py
  verify_g514_central_matching_v25.py
  verify_g514_five_node_v25.py
  verify_g5_10_obstruction_v18.py
  verify_g5_11_obstruction_v20.py
  verify_g5_15_negative_exception_v23.py
  verify_g5_15_ordinary_outer_pair_v23.py
  verify_g5_15_reduction_v21.py
  verify_g5_15_resonance_boundary_v22.py
  verify_g5_7_obstruction_v19.py
  verify_g5_9_obstruction_v19.py
  verify_global_action_atlas_v8.py
  verify_high_d_asymmetry_v23.py
  verify_high_d_axis_degenerate_v24.py
  verify_high_d_axis_endpoints_v25.py
  verify_high_d_boundary_v20.py
  verify_high_d_low_row_finiteness_v22.py
  verify_high_d_proportional_v24.py
  verify_high_d_reconstruction_v21.py
  verify_house_obstruction_v18.py
  verify_k23_node_reduction_v14.py
  verify_k23_obstruction_v15.py
  verify_k4_four_exceptions_v17.py
  verify_k4_leaf_obstruction_v18.py
  verify_k4_low_hub_v16.py
  verify_k4_two_exceptions_v17.py
  verify_leaf_transfer_v13.py
  verify_low_degree_support_v11.py
  verify_meridian_topology_v8.py
  verify_minimal_low_entry_v12.py
  verify_mixed_plane_periods_v8.py
  verify_outer_core_transfer_v23.py
  verify_partitions_v8.py
  verify_path_escalation_v12.py
  verify_petersen_affine_v8.py
  verify_petersen_periods_v8.py
  verify_polarization_v8.py
  verify_positive_small_L_sector_v21.py
  verify_quadric_periods_v8.py
  verify_quintic_denominators_v10.py
  verify_quintic_links_v8.py
  verify_r1_B_leaf_v16.py
  verify_singular_three_high_v14.py
  verify_small_denominator_propagation_v13.py
  verify_support_agenda_v15.py
  verify_support_agenda_v16.py
  verify_support_agenda_v17.py
  verify_support_agenda_v18.py
  verify_support_agenda_v19.py
  verify_support_agenda_v20.py
  verify_support_agenda_v22.py
  verify_support_agenda_v23.py
  verify_three_high_bounds_v13.py
  verify_three_high_completion_v17.py
  verify_three_high_matching_v18.py
  verify_three_high_schur_v12.py
  verify_three_high_sign_reduction_v14.py
  verify_two_high_defect_v12.py
  verify_two_leaf_centers_v16.py
  verify_two_leaf_unit_finiteness_v16.py
  verify_two_leaves_independent_v15.py
  verify_two_leaves_v15.py
  verify_uniform_two_high_classification_v11.py
  verify_unit_three_high_triangles_v24.py
  verify_v8.py

追加監査script一覧：
  audit_axis_endpoints_independent_v25.py
  audit_book_all_negative_v20.py
  audit_book_one_negative_sectors_v21.py
  audit_book_rigidity_v22.py
  audit_book_two_negative_v21.py
  audit_degenerate_divisor_v25.py
  audit_four_ray_matching_independent_v25.py
  audit_g514_central_matching_independent_v25.py
  audit_g514_five_node_independent_v25.py
  audit_g5_10_original_equations_v18.py
  audit_g5_11_certificates_v20.py
  audit_g5_15_exception_independent_v23.py
  audit_g5_7_certificate_check_v19.py
  audit_g5_7_coefficients_v19.py
  audit_g5_9_certificate_v19.py
  audit_high_d_axis_independent_v24.py
  audit_high_d_low_row_v22.py
  audit_high_d_proportional_independent_v24.py
  audit_k4_four_hub_v17.py
  audit_k4_four_tail_v17.py
  audit_k4_leaf_cells_v18.py
  audit_local_signs_and_unit_triangles_v24.py
  audit_two_leaf_global_v16.py
  audit_two_leaf_unit_finiteness_v16.py
