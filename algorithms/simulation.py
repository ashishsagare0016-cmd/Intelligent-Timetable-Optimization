"""
What-If Timetable Simulation Module (Stage 11)
Performs temporary timetable slot mutation on a deep copy of the schedule.
Evaluates before vs after quality scores, hard & soft constraint violations,
new vs resolved violations, and dynamic recommendations.
"""
import copy
from .constraints import analyze_timetable
from .optimizer import calculate_quality_score

# In-memory history of recent simulations (max 10 items)
SIMULATION_HISTORY = []


def get_simulation_history():
    """Returns recent simulation history list."""
    return list(reversed(SIMULATION_HISTORY))


def simulate_move(subject_name, target_slot_str, timetable_entries, raw_data):
    """
    Simulates moving a subject to target_slot_str on a COPY of the timetable.
    Returns simulation results dictionary. Original timetable is NEVER modified.
    """
    if not timetable_entries:
        return {"error": "Empty timetable dataset"}, 400

    # 1. Parse target slot (e.g. "Monday P3" -> Day="Monday", Period="P3")
    parts = target_slot_str.strip().split()
    if len(parts) < 2:
        return {"error": "Invalid target slot format. Expected format: 'Monday P1'"}, 400

    target_day = parts[0].capitalize()
    target_period = parts[1].upper()

    valid_days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    valid_periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    if target_day not in valid_days or target_period not in valid_periods:
        return {"error": f"Invalid day or period: {target_slot_str}"}, 400

    # 2. DEEP COPY timetable entries to guarantee isolation
    simulated_entries = copy.deepcopy(timetable_entries)

    # 3. Find subject in copied entries
    target_entry = None
    for entry in simulated_entries:
        if entry.get('subject', '').strip().lower() == subject_name.strip().lower():
            target_entry = entry
            break

    if not target_entry:
        return {"error": f"Subject '{subject_name}' not found in timetable"}, 404

    actual_subject_name = target_entry['subject']
    original_day = target_entry.get('day', 'Unassigned')
    original_period = target_entry.get('period', 'Unassigned')
    original_slot = f"{original_day} {original_period}"

    # 4. Mutate copy with target slot
    target_entry['day'] = target_day
    target_entry['period'] = target_period
    target_entry['slot'] = f"{target_day} {target_period}"

    # 5. Analyze BEFORE & AFTER
    before_analysis = analyze_timetable(timetable_entries, raw_data)
    before_score_info = calculate_quality_score(before_analysis)
    before_score = before_score_info['score']

    after_analysis = analyze_timetable(simulated_entries, raw_data)
    after_score_info = calculate_quality_score(after_analysis)
    after_score = after_score_info['score']

    score_change = round(after_score - before_score, 2)

    before_hv = before_analysis['hard_violation_count']
    after_hv = after_analysis['hard_violation_count']
    hv_change = after_hv - before_hv

    before_sv = before_analysis['soft_violation_count']
    after_sv = after_analysis['soft_violation_count']
    sv_change = after_sv - before_sv

    # 6. Compare BEFORE & AFTER violations to find new & resolved
    def build_violation_signature(v):
        return (
            v.get('constraint_name', 'Unknown'),
            v.get('day', ''),
            v.get('period', ''),
            v.get('message', '')
        )

    before_all = before_analysis['hard_violations'] + before_analysis['soft_violations']
    after_all = after_analysis['hard_violations'] + after_analysis['soft_violations']

    before_sig_map = {build_violation_signature(v): v for v in before_all}
    after_sig_map = {build_violation_signature(v): v for v in after_all}

    new_sigs = set(after_sig_map.keys()) - set(before_sig_map.keys())
    resolved_sigs = set(before_sig_map.keys()) - set(after_sig_map.keys())

    new_violations = [
        {
            "constraint_name": after_sig_map[s]['constraint_name'],
            "type": after_sig_map[s].get('constraint_type', 'Constraint'),
            "message": after_sig_map[s]['message']
        }
        for s in new_sigs
    ]

    resolved_violations = [
        {
            "constraint_name": before_sig_map[s]['constraint_name'],
            "type": before_sig_map[s].get('constraint_type', 'Constraint'),
            "message": before_sig_map[s]['message']
        }
        for s in resolved_sigs
    ]

    # 7. Dynamic Recommendation logic
    if after_hv > before_hv:
        recommendation = "Not Recommended (Introduces hard constraint violations)"
        recommendation_type = "not_recommended"
        recommendation_icon = "✗"
        is_valid = False
    elif score_change > 0:
        recommendation = "Recommended (Improves timetable quality score)"
        recommendation_type = "recommended"
        recommendation_icon = "✓"
        is_valid = True
    elif score_change == 0:
        recommendation = "No Significant Change (Quality score remains identical)"
        recommendation_type = "neutral"
        recommendation_icon = "⚠"
        is_valid = True
    else:
        recommendation = "Not Recommended (Reduces overall timetable quality score)"
        recommendation_type = "not_recommended"
        recommendation_icon = "✗"
        is_valid = True

    result = {
        "subject": actual_subject_name,
        "original_slot": original_slot,
        "target_slot": f"{target_day} {target_period}",
        "is_valid": is_valid,
        "before": {
            "quality_score": before_score,
            "hard_violations": before_hv,
            "soft_violations": before_sv,
            "total_violations": before_analysis['total_violations']
        },
        "after": {
            "quality_score": after_score,
            "hard_violations": after_hv,
            "soft_violations": after_sv,
            "total_violations": after_analysis['total_violations']
        },
        "score_change": score_change,
        "hard_violation_change": hv_change,
        "soft_violation_change": sv_change,
        "new_violations": new_violations,
        "resolved_violations": resolved_violations,
        "recommendation": recommendation,
        "recommendation_type": recommendation_type,
        "recommendation_icon": recommendation_icon
    }

    # 8. Record simulation in in-memory session history
    history_entry = {
        "subject": actual_subject_name,
        "original_slot": original_slot,
        "target_slot": f"{target_day} {target_period}",
        "score_change": f"{'+' if score_change > 0 else ''}{score_change}",
        "recommendation": recommendation,
        "recommendation_type": recommendation_type,
        "recommendation_icon": recommendation_icon
    }
    SIMULATION_HISTORY.append(history_entry)

    # Maintain history cap at 10 items
    if len(SIMULATION_HISTORY) > 10:
        SIMULATION_HISTORY.pop(0)

    return result, 200
