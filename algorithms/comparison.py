"""
Algorithm Comparison Engine
Runs Greedy Graph Colouring, Backtracking, and Local Search Optimization
on the same dataset and generates dynamic comparative metrics, charts data, and observations.
"""
import time
from .conflict_graph import build_conflict_graph
from .graph_coloring import greedy_graph_coloring
from .backtracking import solve_timetable_backtracking
from .constraints import analyze_timetable
from .optimizer import optimize_timetable, calculate_quality_score


def run_algorithm_comparison(raw_data):
    """
    Executes all three timetable generation strategies on the same dataset
    and collects dynamic comparative metrics.
    """
    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    # Build shared conflict graph
    G = build_conflict_graph(raw_data)

    # 1. GREEDY GRAPH COLOURING
    greedy_start = time.perf_counter()
    greedy_res = greedy_graph_coloring(G, days=days, periods=periods)
    greedy_analysis = analyze_timetable(greedy_res['timetable_entries'], raw_data)
    greedy_score_info = calculate_quality_score(greedy_analysis)
    greedy_end = time.perf_counter()
    greedy_total_time = round(greedy_end - greedy_start, 6)

    greedy_data = {
        "key": "greedy",
        "name": "Greedy Graph Colouring",
        "execution_time": greedy_total_time,
        "algo_execution_time": greedy_res['execution_time'],
        "hard_violations": greedy_analysis['hard_violation_count'],
        "soft_violations": greedy_analysis['soft_violation_count'],
        "total_violations": greedy_analysis['total_violations'],
        "quality_score": greedy_score_info['score'],
        "slots_used": greedy_res['colors_used'],
        "classes_assigned": greedy_res['total_classes'],
        "backtracks": 0,
        "is_feasible": greedy_analysis['is_feasible']
    }

    # 2. BACKTRACKING SOLVER
    bt_start = time.perf_counter()
    bt_res = solve_timetable_backtracking(G, days=days, periods=periods)
    bt_analysis = analyze_timetable(bt_res['timetable_entries'], raw_data)
    bt_score_info = calculate_quality_score(bt_analysis)
    bt_end = time.perf_counter()
    bt_total_time = round(bt_end - bt_start, 6)

    bt_data = {
        "key": "backtracking",
        "name": "Backtracking Solver",
        "execution_time": bt_total_time,
        "algo_execution_time": bt_res['execution_time'],
        "hard_violations": bt_analysis['hard_violation_count'],
        "soft_violations": bt_analysis['soft_violation_count'],
        "total_violations": bt_analysis['total_violations'],
        "quality_score": bt_score_info['score'],
        "slots_used": len(set(bt_res['assignments'].values())) if bt_res['assignments'] else 0,
        "classes_assigned": bt_res['classes_assigned'],
        "backtracks": bt_res['backtrack_count'],
        "recursive_calls": bt_res['recursive_calls'],
        "assignments_attempted": bt_res['assignments_attempted'],
        "rejected_assignments": bt_res['rejected_assignments'],
        "is_feasible": bt_analysis['is_feasible']
    }

    # 3. OPTIMIZED TIMETABLE (Hill-Climbing)
    opt_start = time.perf_counter()
    opt_res = optimize_timetable(bt_res['timetable_entries'], raw_data)
    opt_analysis = analyze_timetable(opt_res['optimized_timetable'], raw_data)
    opt_score_info = calculate_quality_score(opt_analysis)
    opt_end = time.perf_counter()
    opt_total_time = round(opt_end - opt_start + bt_res['execution_time'], 6)

    opt_data = {
        "key": "optimized",
        "name": "Optimized Timetable",
        "execution_time": opt_total_time,
        "algo_execution_time": opt_res['metrics']['execution_time'],
        "hard_violations": opt_analysis['hard_violation_count'],
        "soft_violations": opt_analysis['soft_violation_count'],
        "total_violations": opt_analysis['total_violations'],
        "quality_score": opt_score_info['score'],
        "slots_used": len({(e['day'], e['period']) for e in opt_res['optimized_timetable']}),
        "classes_assigned": len(opt_res['optimized_timetable']),
        "backtracks": 0,
        "iterations": opt_res['metrics']['iterations'],
        "candidate_moves": opt_res['metrics']['candidate_moves'],
        "accepted_moves": opt_res['metrics']['accepted_moves'],
        "score_improvement": opt_res['score_improvement'],
        "is_feasible": opt_analysis['is_feasible']
    }

    all_algos = [greedy_data, bt_data, opt_data]

    # Determine Best Overall Result dynamically
    sorted_algos = sorted(
        all_algos,
        key=lambda a: (-a['quality_score'], a['hard_violations'], a['soft_violations'], a['execution_time'])
    )
    best_algo = sorted_algos[0]

    # Generate observations dynamically
    fastest_algo = min(all_algos, key=lambda a: a['execution_time'])
    highest_score_algo = max(all_algos, key=lambda a: a['quality_score'])
    fewest_violations_algo = min(all_algos, key=lambda a: a['total_violations'])

    observations = [
        f"Fastest Algorithm: {fastest_algo['name']} completed execution in {fastest_algo['execution_time']} seconds.",
        f"Highest Quality Score: {highest_score_algo['name']} achieved the highest Quality Score of {highest_score_algo['quality_score']} / 100.",
        f"Fewest Violations: {fewest_violations_algo['name']} produced the fewest total violations ({fewest_violations_algo['total_violations']} total violations).",
        f"Optimization Gain: Local search optimization improved the initial timetable Quality Score by +{opt_res['score_improvement']} points."
    ]

    return {
        "greedy": greedy_data,
        "backtracking": bt_data,
        "optimized": opt_data,
        "algorithms": all_algos,
        "best_algorithm": best_algo['name'],
        "best_algo_data": best_algo,
        "observations": observations
    }
