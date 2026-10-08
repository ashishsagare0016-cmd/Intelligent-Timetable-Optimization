"""
Constraint Analysis Engine
Evaluates hard and soft constraint violations for generated timetables.
"""


def check_teacher_conflicts(timetable_entries):
    """Hard Constraint 1: A teacher cannot teach two different classes at the same day + period."""
    violations = []
    schedule_map = {}
    for entry in timetable_entries:
        key = (entry['teacher'], entry['day'], entry['period'])
        if key not in schedule_map:
            schedule_map[key] = []
        schedule_map[key].append(entry)

    for (teacher, day, period), entries in schedule_map.items():
        if len(entries) > 1 and teacher != 'Unassigned':
            subjects = [e['subject'] for e in entries]
            violations.append({
                "constraint_type": "Hard",
                "constraint_name": "Teacher Conflict",
                "subject": ", ".join(subjects),
                "day": day,
                "period": period,
                "message": f"{teacher} is assigned to multiple classes simultaneously ({', '.join(subjects)}).",
                "severity": "Critical"
            })
    return violations


def check_division_conflicts(timetable_entries):
    """Hard Constraint 2: A division cannot attend two different classes at the same day + period."""
    violations = []
    schedule_map = {}
    for entry in timetable_entries:
        key = (entry['division'], entry['day'], entry['period'])
        if key not in schedule_map:
            schedule_map[key] = []
        schedule_map[key].append(entry)

    for (division, day, period), entries in schedule_map.items():
        if len(entries) > 1:
            subjects = [e['subject'] for e in entries]
            violations.append({
                "constraint_type": "Hard",
                "constraint_name": "Division Conflict",
                "subject": ", ".join(subjects),
                "day": day,
                "period": period,
                "message": f"Division {division} is scheduled for multiple subjects ({', '.join(subjects)}) at the same time.",
                "severity": "Critical"
            })
    return violations


def check_room_conflicts(timetable_entries):
    """Hard Constraint 3: A room cannot contain two different classes at the same day + period."""
    violations = []
    schedule_map = {}
    for entry in timetable_entries:
        key = (entry['room'], entry['day'], entry['period'])
        if key not in schedule_map:
            schedule_map[key] = []
        schedule_map[key].append(entry)

    for (room, day, period), entries in schedule_map.items():
        if len(entries) > 1:
            subjects = [e['subject'] for e in entries]
            violations.append({
                "constraint_type": "Hard",
                "constraint_name": "Room Conflict",
                "subject": ", ".join(subjects),
                "day": day,
                "period": period,
                "message": f"{room} is occupied by multiple classes ({', '.join(subjects)}) simultaneously.",
                "severity": "Critical"
            })
    return violations


def check_teacher_availability(timetable_entries, raw_data):
    """Hard Constraint 4: Teacher is available during assigned day + period."""
    violations = []
    teachers_list = raw_data.get('teachers', [])

    for entry in timetable_entries:
        teacher = entry['teacher']
        day = entry['day']
        period = entry['period']
        slot_str = f"{day} {period}"

        t_info = next((t for t in teachers_list if t.get('name') == teacher), None)
        if t_info:
            unavail = t_info.get('unavailable_slots', [])
            avail_map = t_info.get('availability', {})

            if slot_str in unavail or period in unavail:
                violations.append({
                    "constraint_type": "Hard",
                    "constraint_name": "Teacher Availability",
                    "subject": entry['subject'],
                    "day": day,
                    "period": period,
                    "message": f"{teacher} is not available on {day} during {period}.",
                    "severity": "Critical"
                })
            elif avail_map and day in avail_map:
                if period not in avail_map[day]:
                    violations.append({
                        "constraint_type": "Hard",
                        "constraint_name": "Teacher Availability",
                        "subject": entry['subject'],
                        "day": day,
                        "period": period,
                        "message": f"{teacher} is not available on {day} during {period}.",
                        "severity": "Critical"
                    })
    return violations


def check_room_availability(timetable_entries, raw_data):
    """Hard Constraint 5: Room is available during assigned day + period."""
    violations = []
    rooms_list = raw_data.get('rooms', [])

    for entry in timetable_entries:
        room = entry['room']
        day = entry['day']
        period = entry['period']
        slot_str = f"{day} {period}"

        r_info = next((r for r in rooms_list if r.get('name') == room), None)
        if r_info:
            unavail = r_info.get('unavailable_slots', [])
            avail_map = r_info.get('availability', {})

            if slot_str in unavail or period in unavail:
                violations.append({
                    "constraint_type": "Hard",
                    "constraint_name": "Room Availability",
                    "subject": entry['subject'],
                    "day": day,
                    "period": period,
                    "message": f"{room} is unavailable on {day} during {period}.",
                    "severity": "Critical"
                })
            elif avail_map and day in avail_map:
                if period not in avail_map[day]:
                    violations.append({
                        "constraint_type": "Hard",
                        "constraint_name": "Room Availability",
                        "subject": entry['subject'],
                        "day": day,
                        "period": period,
                        "message": f"{room} is unavailable on {day} during {period}.",
                        "severity": "Critical"
                    })
    return violations


def check_room_capacity(timetable_entries, raw_data):
    """Hard Constraint 6: Room capacity >= student_count."""
    violations = []
    student_count = raw_data.get('student_count', 60)
    rooms_list = raw_data.get('rooms', [])
    room_cap_map = {r['name']: r.get('capacity', 60) for r in rooms_list}

    for entry in timetable_entries:
        room = entry['room']
        capacity = room_cap_map.get(room, 60)
        if capacity < student_count:
            violations.append({
                "constraint_type": "Hard",
                "constraint_name": "Room Capacity",
                "subject": entry['subject'],
                "day": entry['day'],
                "period": entry['period'],
                "message": f"Room '{room}' capacity ({capacity}) is smaller than required student count ({student_count}).",
                "severity": "Critical"
            })
    return violations


def check_lab_requirements(timetable_entries, raw_data):
    """Hard Constraint 7: Practical / Lab classes must be assigned to laboratory rooms."""
    violations = []
    rooms_list = raw_data.get('rooms', [])
    subjects_list = raw_data.get('subjects', [])
    lab_room_names = {r['name'] for r in rooms_list if r.get('is_lab', False) or r.get('type') == 'Laboratory'}

    for entry in timetable_entries:
        sub_info = next((s for s in subjects_list if s.get('name') == entry.get('subject')), {})
        is_lab_class = (entry.get('class_type') == 'Practical') or sub_info.get('requires_lab', False) or sub_info.get('type') == 'Practical'
        room_assigned = entry['room']

        if is_lab_class and (room_assigned not in lab_room_names and not room_assigned.startswith("Lab")):
            violations.append({
                "constraint_type": "Hard",
                "constraint_name": "Lab Requirement",
                "subject": entry['subject'],
                "day": entry['day'],
                "period": entry['period'],
                "message": f"Practical subject '{entry['subject']}' is assigned to non-lab classroom '{room_assigned}'.",
                "severity": "Critical"
            })
    return violations



def check_consecutive_lectures(timetable_entries, periods_order):
    """Soft Constraint 1: 3 or more consecutive lectures for division or teacher."""
    violations = []
    period_idx_map = {p: i for i, p in enumerate(periods_order)}
    division_day_map = {}

    for entry in timetable_entries:
        key = (entry['division'], entry['day'])
        if key not in division_day_map:
            division_day_map[key] = []
        p_idx = period_idx_map.get(entry['period'], -1)
        if p_idx != -1:
            division_day_map[key].append((p_idx, entry))

    for (division, day), items in division_day_map.items():
        indices = sorted([p for p, _ in items])
        consecutive_count = 1
        for k in range(1, len(indices)):
            if indices[k] == indices[k - 1] + 1:
                consecutive_count += 1
                if consecutive_count >= 3:
                    sub = items[k][1]['subject']
                    violations.append({
                        "constraint_type": "Soft",
                        "constraint_name": "Too Many Consecutive Lectures",
                        "subject": sub,
                        "day": day,
                        "period": items[k][1]['period'],
                        "message": f"Division {division} has 3 or more consecutive lectures on {day}.",
                        "severity": "Warning"
                    })
            else:
                consecutive_count = 1
    return violations


def check_repeated_subject_same_day(timetable_entries):
    """Soft Constraint 2: Same subject assigned more than once on the same day."""
    violations = []
    subject_day_map = {}
    for entry in timetable_entries:
        key = (entry['subject'], entry['day'])
        if key not in subject_day_map:
            subject_day_map[key] = []
        subject_day_map[key].append(entry)

    for (subject, day), entries in subject_day_map.items():
        if len(entries) > 1:
            for e in entries[1:]:
                violations.append({
                    "constraint_type": "Soft",
                    "constraint_name": "Repeated Subject Same Day",
                    "subject": subject,
                    "day": day,
                    "period": e['period'],
                    "message": f"Subject '{subject}' is scheduled multiple times on {day}.",
                    "severity": "Warning"
                })
    return violations


def check_teacher_gaps(timetable_entries, periods_order):
    """Soft Constraint 4: Free period between scheduled classes for a teacher."""
    violations = []
    period_idx_map = {p: i for i, p in enumerate(periods_order)}
    teacher_day_map = {}

    for entry in timetable_entries:
        key = (entry['teacher'], entry['day'])
        if key not in teacher_day_map:
            teacher_day_map[key] = []
        p_idx = period_idx_map.get(entry['period'], -1)
        if p_idx != -1:
            teacher_day_map[key].append((p_idx, entry))

    for (teacher, day), items in teacher_day_map.items():
        if len(items) < 2:
            continue
        indices = sorted([p for p, _ in items])
        first_p = indices[0]
        last_p = indices[-1]

        scheduled_set = set(indices)
        for gap_p in range(first_p + 1, last_p):
            if gap_p not in scheduled_set:
                gap_period_name = periods_order[gap_p]
                violations.append({
                    "constraint_type": "Soft",
                    "constraint_name": "Teacher Gap",
                    "subject": f"Schedule of {teacher}",
                    "day": day,
                    "period": gap_period_name,
                    "message": f"Unnecessary 1-period idle gap for {teacher} on {day} during {gap_period_name}.",
                    "severity": "Warning"
                })
    return violations


def analyze_timetable(timetable_entries, raw_data):
    """
    Main entry point for constraint analysis.
    Evaluates hard and soft constraint rules and returns complete diagnostic report.
    """
    periods_order = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    # Hard constraints
    hard_violations = []
    hard_violations.extend(check_teacher_conflicts(timetable_entries))
    hard_violations.extend(check_division_conflicts(timetable_entries))
    hard_violations.extend(check_room_conflicts(timetable_entries))
    hard_violations.extend(check_teacher_availability(timetable_entries, raw_data))
    hard_violations.extend(check_room_availability(timetable_entries, raw_data))
    hard_violations.extend(check_room_capacity(timetable_entries, raw_data))
    hard_violations.extend(check_lab_requirements(timetable_entries, raw_data))

    # Soft constraints
    soft_violations = []
    soft_violations.extend(check_consecutive_lectures(timetable_entries, periods_order))
    soft_violations.extend(check_repeated_subject_same_day(timetable_entries))
    soft_violations.extend(check_teacher_gaps(timetable_entries, periods_order))

    # Summary counts
    all_constraint_names = [
        "Teacher Conflict", "Division Conflict", "Room Conflict",
        "Teacher Availability", "Room Availability", "Room Capacity",
        "Lab Requirement", "Too Many Consecutive Lectures",
        "Repeated Subject Same Day", "Teacher Gap"
    ]

    summary_counts = {name: 0 for name in all_constraint_names}
    for v in hard_violations + soft_violations:
        c_name = v['constraint_name']
        summary_counts[c_name] = summary_counts.get(c_name, 0) + 1

    summary_list = [
        {
            "name": name,
            "type": "Hard" if name in [
                "Teacher Conflict", "Division Conflict", "Room Conflict",
                "Teacher Availability", "Room Availability", "Room Capacity", "Lab Requirement"
            ] else "Soft",
            "count": count
        }
        for name, count in summary_counts.items()
    ]

    return {
        "hard_violations": hard_violations,
        "soft_violations": soft_violations,
        "hard_violation_count": len(hard_violations),
        "soft_violation_count": len(soft_violations),
        "total_violations": len(hard_violations) + len(soft_violations),
        "is_feasible": (len(hard_violations) == 0),
        "summary_counts": summary_counts,
        "summary_list": summary_list
    }
