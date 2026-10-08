"""
Dashboard & Analytics Aggregator Module
Calculates real-time metrics, project status, charts data, weekly timetable grid,
and key results for the main Dashboard (Stage 10).
"""
import os
from .conflict_graph import build_conflict_graph, get_graph_statistics
from .graph_coloring import greedy_graph_coloring
from .backtracking import solve_timetable_backtracking
from .constraints import analyze_timetable
from .optimizer import optimize_timetable, calculate_quality_score
from .comparison import run_algorithm_comparison


def get_dashboard_data(raw_data, app_root_path=None):
    """
    Generates all dynamic metrics required for the Stage 10 Dashboard UI & API.
    Does not hardcode any statistics. Safe fallback handling included.
    """
    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    # Track project features status
    project_status = []

    def record_status(name, is_ok):
        project_status.append({
            "name": name,
            "status": "Completed" if is_ok else "Not Available",
            "icon": "✓" if is_ok else "⚠",
            "available": bool(is_ok)
        })

    record_status("Data Loaded", bool(raw_data and raw_data.get('subjects')))

    # 1. CONFLICT GRAPH
    graph_stats = {"num_nodes": 0, "num_edges": 0, "max_degree": 0, "avg_degree": 0.0}
    try:
        G = build_conflict_graph(raw_data)
        graph_stats = get_graph_statistics(G)
        record_status("Conflict Graph", True)
    except Exception:
        G = None
        record_status("Conflict Graph", False)

    # 2. ALGORITHM COMPARISON & RUNS
    comp_result = None
    try:
        comp_result = run_algorithm_comparison(raw_data)
        record_status("Greedy Colouring", True)
        record_status("Backtracking", True)
        record_status("Constraint Analysis", True)
        record_status("Optimization", True)
        record_status("Algorithm Comparison", True)
    except Exception:
        record_status("Greedy Colouring", False)
        record_status("Backtracking", False)
        record_status("Constraint Analysis", False)
        record_status("Optimization", False)
        record_status("Algorithm Comparison", False)

    # 3. TIMETABLE SELECTION & FALLBACK HIERARCHY
    # Hierarchy: Optimized -> Backtracking -> Greedy
    best_entries = []
    timetable_source = "Unavailable"
    
    if G is not None:
        try:
            bt_res = solve_timetable_backtracking(G, days=days, periods=periods)
            opt_res = optimize_timetable(bt_res['timetable_entries'], raw_data)
            best_entries = opt_res['optimized_timetable']
            timetable_source = "Optimized (Hill-Climbing)"
        except Exception:
            try:
                bt_res = solve_timetable_backtracking(G, days=days, periods=periods)
                best_entries = bt_res['timetable_entries']
                timetable_source = "Backtracking Solver"
            except Exception:
                try:
                    gr_res = greedy_graph_coloring(G, days=days, periods=periods)
                    best_entries = gr_res['timetable_entries']
                    timetable_source = "Greedy Graph Colouring"
                except Exception:
                    best_entries = []

    # 4. CONSTRAINT ANALYSIS & SCORING FOR BEST TIMETABLE
    if best_entries:
        best_analysis = analyze_timetable(best_entries, raw_data)
        best_score_info = calculate_quality_score(best_analysis)
        hard_violations = best_analysis['hard_violation_count']
        soft_violations = best_analysis['soft_violation_count']
        quality_score = best_score_info['score']
        slots_used = len({(e['day'], e['period']) for e in best_entries})
    else:
        best_analysis = {"soft_constraints": {}, "hard_constraints": {}}
        hard_violations = 0
        soft_violations = 0
        quality_score = 0
        slots_used = 0

    total_classes = len(raw_data.get('subjects', []))

    # 5. SUMMARY KPI CARD VALUES
    summary_kpi = {
        "total_classes": total_classes,
        "conflict_edges": graph_stats.get('total_edges', 0),
        "hard_violations": hard_violations,
        "soft_violations": soft_violations,
        "quality_score": quality_score,
        "slots_used": slots_used
    }


    # 6. QUALITY & IMPROVEMENT METRICS
    initial_score = comp_result['backtracking']['quality_score'] if comp_result else quality_score
    final_score = comp_result['optimized']['quality_score'] if comp_result else quality_score
    improvement = final_score - initial_score

    if improvement > 0:
        improvement_text = f"+{improvement} points improvement"
    elif improvement == 0:
        improvement_text = "No improvement found"
    else:
        improvement_text = f"{improvement} points"

    quality_metrics = {
        "initial_score": initial_score,
        "final_score": final_score,
        "improvement": improvement,
        "improvement_text": improvement_text
    }

    # 7. SOFT CONSTRAINTS BREAKDOWN
    soft_details = best_analysis.get('soft_constraints', {})
    soft_breakdown = {
        "Consecutive lectures": soft_details.get('consecutive_lectures_exceeded', {}).get('count', 0),
        "Repeated subject": soft_details.get('same_subject_same_day_multitimes', {}).get('count', 0),
        "Subject distribution": soft_details.get('unbalanced_daily_load', {}).get('count', 0),
        "Teacher gaps": soft_details.get('teacher_idle_gap', {}).get('count', 0)
    }

    # 8. WEEKLY TIMETABLE GRID FOR SUMMARY
    timetable_grid = {day: {period: None for period in periods} for day in days}
    for entry in best_entries:
        d = entry.get('day')
        p = entry.get('period')
        if d in timetable_grid and p in timetable_grid[d]:
            timetable_grid[d][p] = {
                "subject": entry.get('subject', 'N/A'),
                "teacher": entry.get('teacher', 'N/A'),
                "room": entry.get('room', 'N/A'),
                "division": entry.get('division', 'N/A')
            }

    # Format 2D array grid for easy rendering in UI & Chart/Table
    table_rows = []
    for p in periods:
        row_data = {"period": p, "slots": {}}
        for d in days:
            row_data["slots"][d] = timetable_grid[d][p]
        table_rows.append(row_data)

    timetable_summary = {
        "days": days,
        "periods": periods,
        "grid": timetable_grid,
        "table_rows": table_rows,
        "source": timetable_source,
        "entries_count": len(best_entries)
    }

    # 9. GRAPH SUMMARY & IMAGE CHECK
    image_rel_path = os.path.join('generated', 'conflict_graph.png')
    image_exists = False
    if app_root_path:
        image_full_path = os.path.join(app_root_path, 'static', 'generated', 'conflict_graph.png')
        image_exists = os.path.exists(image_full_path)

    graph_summary = {
        "nodes": graph_stats.get('total_nodes', 0),
        "edges": graph_stats.get('total_edges', 0),
        "max_degree": graph_stats.get('max_degree', 0),
        "avg_degree": graph_stats.get('avg_degree', 0.0),
        "image_file": 'generated/conflict_graph.png',
        "image_exists": image_exists
    }

    # 10. DYNAMIC KEY RESULTS / OBSERVATIONS
    key_results = []
    if comp_result:
        if improvement > 0:
            key_results.append(f"Local search optimization improved Quality Score by +{improvement} points (from {initial_score} to {final_score}).")
        else:
            key_results.append(f"Local search optimization achieved optimal Quality Score of {final_score}/100.")
        
        key_results.append(f"The best timetable has {hard_violations} hard violations and {soft_violations} soft violations across {total_classes} scheduled subjects.")
        
        bt_info = comp_result.get('backtracking', {})
        if 'recursive_calls' in bt_info:
            key_results.append(f"Backtracking solver evaluated {bt_info.get('recursive_calls', 0)} recursive steps and {bt_info.get('backtracks', 0)} backtracks to guarantee feasibility.")
        
        key_results.append(f"Conflict graph analysis identified {graph_stats.get('total_edges', 0)} constraint edges among {graph_stats.get('total_nodes', 0)} subjects (Max degree: {graph_stats.get('max_degree', 0)}).")
        
        gr_info = comp_result.get('greedy', {})
        key_results.append(f"Greedy Graph Colouring executed in {gr_info.get('execution_time', 0)}s, whereas Hill-Climbing Optimization finished in {comp_result['optimized'].get('execution_time', 0)}s.")


    return {
        "summary": summary_kpi,
        "project_status": project_status,
        "quality": quality_metrics,
        "algorithms": comp_result,
        "constraints": {
            "hard_violations": hard_violations,
            "soft_violations": soft_violations,
            "total_violations": hard_violations + soft_violations,
            "soft_breakdown": soft_breakdown
        },
        "timetable": timetable_summary,
        "graph": graph_summary,
        "key_results": key_results
    }
