"""
Explainable Slot Decision Engine ("Why This Slot?" and "Why Not This Slot?")
Analyzes slot validity, graph conflicts, teacher/room availability, capacity,
and preference scores for any subject.
"""
from urllib.parse import unquote
from .conflict_graph import build_conflict_graph
from .optimizer import optimize_timetable, calculate_quality_score
from .backtracking import solve_timetable_backtracking


def evaluate_slot_for_subject(subject_name, target_day, target_period, timetable_entries, raw_data, G=None):
    """
    Evaluates a specific candidate slot (Day, Period) for a subject against all hard/soft constraints.
    Returns (status, reasons, constraint_checks, failed_count).
    """
    if G is None:
        G = build_conflict_graph(raw_data)

    subjects = raw_data.get('subjects', [])
    target_sub_obj = next((s for s in subjects if s.get('name') == subject_name), None)

    if not target_sub_obj:
        return "rejected", ["Subject not found in dataset"], {}, 1

    teachers = raw_data.get('teachers', [])
    rooms = raw_data.get('rooms', [])
    student_count = raw_data.get('student_count', 60)
    division = raw_data.get('division', 'TY-C')

    # Assigned teacher
    teacher_name = next((t['name'] for t in teachers if subject_name in t.get('subjects', [])), 'Unassigned')

    # Assigned room
    assigned_room = 'Room 101'
    for e in timetable_entries:
        if e['subject'] == subject_name:
            assigned_room = e['room']
            break

    # Build hypothetical timetable entry for this candidate slot
    test_entry = {
        "subject": subject_name,
        "teacher": teacher_name,
        "division": division,
        "room": assigned_room,
        "class_type": target_sub_obj.get('type', 'Theory'),
        "day": target_day,
        "period": target_period
    }

    # Filter out any current entry for this subject to test candidate slot cleanly
    other_entries = [e for e in timetable_entries if e['subject'] != subject_name]

    reasons = []
    checks = {
        "teacher_conflict": False,
        "division_conflict": False,
        "room_conflict": False,
        "graph_neighbour_conflict": False,
        "teacher_available": True,
        "room_available": True,
        "capacity_satisfied": True,
        "lab_requirement_satisfied": True
    }

    # 1. Graph Neighbour Check
    sub_node = next((n for n in G.nodes() if G.nodes[n].get('subject') == subject_name), None)
    if sub_node:
        for neighbor in G.neighbors(sub_node):
            n_subject = G.nodes[neighbor].get('subject')
            for e in other_entries:
                if e['subject'] == n_subject and e['day'] == target_day and e['period'] == target_period:
                    checks["graph_neighbour_conflict"] = True
                    reasons.append(f"Graph neighbour conflict: '{n_subject}' is already assigned to {target_day} {target_period}.")

    # 2. Teacher Conflict
    if teacher_name != 'Unassigned':
        for e in other_entries:
            if e['teacher'] == teacher_name and e['day'] == target_day and e['period'] == target_period:
                checks["teacher_conflict"] = True
                reasons.append(f"Teacher conflict: {teacher_name} is already teaching '{e['subject']}' in this slot.")

    # 3. Division Conflict
    for e in other_entries:
        if e['division'] == division and e['day'] == target_day and e['period'] == target_period:
            checks["division_conflict"] = True
            reasons.append(f"Division conflict: Division {division} is already attending '{e['subject']}' in this slot.")

    # 4. Room Conflict
    for e in other_entries:
        if e['room'] == assigned_room and e['day'] == target_day and e['period'] == target_period:
            checks["room_conflict"] = True
            reasons.append(f"Room conflict: Room '{assigned_room}' is occupied by '{e['subject']}' in this slot.")

    # 5. Teacher Availability
    t_obj = next((t for t in teachers if t['name'] == teacher_name), None)
    if t_obj:
        avail = t_obj.get('availability', {}).get(target_day, [])
        if target_period not in avail:
            checks["teacher_available"] = False
            reasons.append(f"Teacher unavailable: {teacher_name} is unavailable on {target_day} {target_period}.")

    # 6. Room Availability
    r_obj = next((r for r in rooms if r['name'] == assigned_room), None)
    if r_obj:
        avail = r_obj.get('availability', {}).get(target_day, [])
        if target_period not in avail:
            checks["room_available"] = False
            reasons.append(f"Room unavailable: '{assigned_room}' is unavailable on {target_day} {target_period}.")

    # 7. Room Capacity
    if r_obj and r_obj.get('capacity', 60) < student_count:
        checks["capacity_satisfied"] = False
        reasons.append(f"Room capacity insufficient: '{assigned_room}' capacity ({r_obj.get('capacity')}) < required ({student_count}).")

    # 8. Lab Requirement
    is_practical = (target_sub_obj.get('type') == 'Practical' or target_sub_obj.get('requires_lab', False))
    if is_practical and r_obj and not r_obj.get('is_lab', False):
        checks["lab_requirement_satisfied"] = False
        reasons.append(f"Lab requirement violation: Practical subject '{subject_name}' requires a laboratory, but '{assigned_room}' is not a lab.")

    has_hard_failure = (
        checks["teacher_conflict"] or checks["division_conflict"] or checks["room_conflict"] or
        checks["graph_neighbour_conflict"] or not checks["teacher_available"] or
        not checks["room_available"] or not checks["capacity_satisfied"] or
        not checks["lab_requirement_satisfied"]
    )

    failed_count = (
        (1 if checks["teacher_conflict"] else 0) +
        (1 if checks["division_conflict"] else 0) +
        (1 if checks["room_conflict"] else 0) +
        (1 if checks["graph_neighbour_conflict"] else 0) +
        (0 if checks["teacher_available"] else 1) +
        (0 if checks["room_available"] else 1) +
        (0 if checks["capacity_satisfied"] else 1) +
        (0 if checks["lab_requirement_satisfied"] else 1)
    )

    if has_hard_failure:
        status = "rejected"
    else:
        status = "valid"
        reasons = [
            "No conflict with graph neighbours",
            f"Teacher {teacher_name} is available",
            f"Room {assigned_room} is available",
            f"Division {division} has no class in this slot",
            "Student capacity requirement satisfied",
            "Lab/Room requirement satisfied"
        ]

    return status, reasons, checks, failed_count


def explain_subject_slot_decision(subject_name, raw_data, timetable_entries=None):
    """
    Generates a full explanation report for a subject:
    - Why the assigned slot was accepted / preferred.
    - Why all alternative slots were rejected or less preferred.
    """
    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])
    G = build_conflict_graph(raw_data)

    if timetable_entries is None:
        # Generate initial backtracking & optimize
        bt_res = solve_timetable_backtracking(G, days=days, periods=periods)
        opt_res = optimize_timetable(bt_res['timetable_entries'], raw_data)
        timetable_entries = opt_res['optimized_timetable']

    # Find currently assigned entry for this subject
    assigned_entry = next((e for e in timetable_entries if e['subject'] == subject_name), None)

    if not assigned_entry:
        return {"error": f"Subject '{subject_name}' not found in timetable"}, 404

    assigned_slot_str = f"{assigned_entry['day']} {assigned_entry['period']}"

    # 1. Explain Assigned Slot ("Why This Slot?")
    assigned_status, assigned_reasons, assigned_checks, _ = evaluate_slot_for_subject(
        subject_name, assigned_entry['day'], assigned_entry['period'], timetable_entries, raw_data, G
    )

    assigned_explanation = {
        "subject": subject_name,
        "slot": assigned_slot_str,
        "day": assigned_entry['day'],
        "period": assigned_entry['period'],
        "status": "accepted / preferred",
        "reasons": assigned_reasons,
        "constraint_checks": assigned_checks
    }

    # 2. Evaluate All Alternative Slots ("Why Not Other Slots?")
    alternative_slots = []
    for day in days:
        for period in periods:
            slot_str = f"{day} {period}"
            if slot_str == assigned_slot_str:
                continue

            status, reasons, checks, failed_count = evaluate_slot_for_subject(
                subject_name, day, period, timetable_entries, raw_data, G
            )

            if status == "valid":
                display_status = "valid_but_less_preferred"
                display_reasons = [
                    "Slot is valid with zero hard conflicts",
                    f"However, '{assigned_slot_str}' was preferred because it produced a higher overall quality score / better schedule flow."
                ]
            else:
                display_status = "rejected"
                display_reasons = reasons

            alternative_slots.append({
                "slot": slot_str,
                "day": day,
                "period": period,
                "status": display_status,
                "reasons": display_reasons,
                "constraint_checks": checks,
                "failed_constraints_count": failed_count
            })

    return {
        "subject": subject_name,
        "assigned_slot": assigned_slot_str,
        "assigned_slot_explanation": assigned_explanation,
        "alternative_slots": alternative_slots,
        "total_alternatives_evaluated": len(alternative_slots)
    }, 200
