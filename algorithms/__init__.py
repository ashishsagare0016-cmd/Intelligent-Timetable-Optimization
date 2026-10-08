from .conflict_graph import build_conflict_graph, get_graph_statistics, generate_graph_image
from .graph_coloring import greedy_graph_coloring, color_to_slot
from .backtracking import solve_timetable_backtracking, BacktrackingTimetableSolver, is_valid_assignment
from .constraints import analyze_timetable
from .optimizer import calculate_quality_score, TimetableOptimizer, optimize_timetable
from .comparison import run_algorithm_comparison
from .explanation import evaluate_slot_for_subject, explain_subject_slot_decision
from .dashboard import get_dashboard_data
from .simulation import simulate_move, get_simulation_history

__all__ = [
    'build_conflict_graph',
    'get_graph_statistics',
    'generate_graph_image',
    'greedy_graph_coloring',
    'color_to_slot',
    'solve_timetable_backtracking',
    'BacktrackingTimetableSolver',
    'is_valid_assignment',
    'analyze_timetable',
    'calculate_quality_score',
    'TimetableOptimizer',
    'optimize_timetable',
    'run_algorithm_comparison',
    'evaluate_slot_for_subject',
    'explain_subject_slot_decision',
    'get_dashboard_data',
    'simulate_move',
    'get_simulation_history'
]


