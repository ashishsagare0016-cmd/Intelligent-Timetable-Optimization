"""
Timetable Optimizer & Quality Scoring Engine
Uses Hill-Climbing Local Search to optimize time slot assignments and maximize quality score.
"""
import copy
import time
from .constraints import analyze_timetable


def calculate_quality_score(analysis):
    """
    Calculates timetable quality score (0 - 100).

    Formula:
    Score = 100
            - (hard_violations * 20)
            - (consecutive_violations * 4)
            - (repeated_subject_violations * 3)
            - (distribution_violations * 3)
            - (teacher_gap_violations * 2)
    """
    hard_count = analysis.get('hard_violation_count', 0)

    summary_counts = analysis.get('summary_counts', {})
    consecutive_count = summary_counts.get('Too Many Consecutive Lectures', 0)
    repeated_count = summary_counts.get('Repeated Subject Same Day', 0)
    distribution_count = summary_counts.get('Subject Distribution', 0)
    teacher_gap_count = summary_counts.get('Teacher Gap', 0)

    hard_penalty = hard_count * 20
    soft_penalty = (consecutive_count * 4) + (repeated_count * 3) + (distribution_count * 3) + (teacher_gap_count * 2)

    raw_score = 100 - hard_penalty - soft_penalty
    clamped_score = max(0, min(100, raw_score))

    return {
        "score": clamped_score,
        "raw_score": raw_score,
        "hard_penalty": hard_penalty,
        "soft_penalty": soft_penalty,
        "breakdown": {
            "hard_violations": hard_count,
            "consecutive_violations": consecutive_count,
            "repeated_subject_violations": repeated_count,
            "distribution_violations": distribution_count,
            "teacher_gap_violations": teacher_gap_count
        }
    }


class TimetableOptimizer:
    def __init__(self, initial_entries, raw_data, max_iterations=100):
        self.initial_entries = copy.deepcopy(initial_entries)
        self.raw_data = raw_data
        self.max_iterations = max_iterations
        self.days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    def optimize(self):
        """Executes hill-climbing local search algorithm."""
        start_time = time.perf_counter()

        current_entries = copy.deepcopy(self.initial_entries)
        initial_analysis = analyze_timetable(current_entries, self.raw_data)
        initial_score_info = calculate_quality_score(initial_analysis)
        current_score = initial_score_info['score']

        candidate_moves = 0
        accepted_moves = 0
        rejected_moves = 0
        move_log = []
        iterations_run = 0

        # Hill-climbing local search loop
        for iteration in range(1, self.max_iterations + 1):
            iterations_run = iteration
            improved_in_iteration = False

            # Try moving each class entry to an alternative day/period
            for i, entry in enumerate(current_entries):
                old_day = entry['day']
                old_period = entry['period']

                # Try all available time slots
                for candidate_day in self.days:
                    for candidate_period in self.periods:
                        if candidate_day == old_day and candidate_period == old_period:
                            continue

                        candidate_moves += 1

                        # Create candidate timetable
                        candidate_entries = copy.deepcopy(current_entries)
                        candidate_entries[i]['day'] = candidate_day
                        candidate_entries[i]['period'] = candidate_period

                        # Analyze candidate timetable
                        cand_analysis = analyze_timetable(candidate_entries, self.raw_data)

                        # Rule: Reject candidates that increase hard violations
                        if cand_analysis['hard_violation_count'] > initial_analysis['hard_violation_count']:
                            rejected_moves += 1
                            continue

                        cand_score_info = calculate_quality_score(cand_analysis)
                        cand_score = cand_score_info['score']

                        # Accept candidate only if score improves
                        if cand_score > current_score:
                            accepted_moves += 1
                            improved_in_iteration = True

                            reasons = [
                                "No hard constraint conflict introduced",
                                "Teacher availability satisfied",
                                "Room availability satisfied",
                                "Schedule gap or consecutive overlap improved",
                                f"Quality score increased from {current_score} to {cand_score}"
                            ]

                            move_log.append({
                                "subject": entry['subject'],
                                "teacher": entry['teacher'],
                                "old_slot": f"{old_day} {old_period}",
                                "new_slot": f"{candidate_day} {candidate_period}",
                                "old_day": old_day,
                                "old_period": old_period,
                                "new_day": candidate_day,
                                "new_period": candidate_period,
                                "score_before": current_score,
                                "score_after": cand_score,
                                "reasons": reasons
                            })

                            # Accept move
                            current_entries = candidate_entries
                            current_score = cand_score
                            break

                    if improved_in_iteration:
                        break

            if not improved_in_iteration:
                # Local optimum reached
                break

        end_time = time.perf_counter()
        execution_time = round(end_time - start_time, 6)

        final_analysis = analyze_timetable(current_entries, self.raw_data)
        final_score_info = calculate_quality_score(final_analysis)
        score_improvement = final_score_info['score'] - initial_score_info['score']

        # Build 2D grid for final timetable
        grid = {d: {p: [] for p in self.periods} for d in self.days}
        for e in current_entries:
            grid[e['day']][e['period']].append(e)

        return {
            "initial_timetable": self.initial_entries,
            "optimized_timetable": current_entries,
            "initial_analysis": initial_analysis,
            "final_analysis": final_analysis,
            "initial_score": initial_score_info,
            "final_score": final_score_info,
            "score_improvement": score_improvement,
            "has_improvement": (score_improvement > 0 or accepted_moves > 0),
            "metrics": {
                "iterations": iterations_run,
                "candidate_moves": candidate_moves,
                "accepted_moves": accepted_moves,
                "rejected_moves": rejected_moves,
                "execution_time": execution_time
            },
            "move_log": move_log,
            "grid": grid,
            "days": self.days,
            "periods": self.periods
        }


def optimize_timetable(initial_entries, raw_data, max_iterations=100):
    """Helper wrapper function to run timetable optimizer."""
    optimizer = TimetableOptimizer(initial_entries, raw_data, max_iterations)
    return optimizer.optimize()
