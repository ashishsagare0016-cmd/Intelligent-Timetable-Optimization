"""
Backtracking Algorithm for Timetable Slot Assignment
Uses Recursive Backtracking with Degree-Based Variable Ordering.
"""
import time


def generate_available_slots(days, periods):
    """Generates all 30 time slots (5 days x 6 periods)."""
    slots = []
    slot_id = 1
    for day in days:
        for period in periods:
            slots.append({
                "id": slot_id,
                "day": day,
                "period": period,
                "name": f"{day} {period}"
            })
            slot_id += 1
    return slots


def is_valid_assignment(node, candidate_slot_id, assignments, G):
    """
    Checks if candidate_slot_id can be assigned to node without graph conflict.
    Returns (is_valid, conflict_neighbour_subject).
    """
    for neighbor in G.neighbors(node):
        if neighbor in assignments and assignments[neighbor] == candidate_slot_id:
            neighbor_subject = G.nodes[neighbor]['subject']
            return False, neighbor_subject
    return True, None


class BacktrackingTimetableSolver:
    def __init__(self, G, days=None, periods=None):
        if days is None:
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        if periods is None:
            periods = ["P1", "P2", "P3", "P4", "P5", "P6"]

        self.G = G
        self.days = days
        self.periods = periods
        self.slots = generate_available_slots(days, periods)

        # Metrics counters
        self.recursive_calls = 0
        self.assignments_attempted = 0
        self.successful_assignments = 0
        self.rejected_assignments = 0
        self.backtrack_count = 0
        self.decision_log = []

    def solve(self):
        """Executes the recursive backtracking algorithm."""
        start_time = time.perf_counter()

        # Variable Ordering: Sort classes by vertex degree descending (Most constrained first)
        # Highly constrained classes have fewer available slots, so placing them early
        # reduces the search space and avoids deep backtracking trees.
        sorted_nodes = sorted(self.G.nodes(), key=lambda n: self.G.degree(n), reverse=True)

        assignments = {}  # node_id -> slot_id

        success = self._backtrack(0, sorted_nodes, assignments)

        end_time = time.perf_counter()
        execution_time = round(end_time - start_time, 6)

        # Verification step: Ensure no graph edges share the same slot
        is_valid = success
        if success:
            for u, v in self.G.edges():
                if assignments.get(u) == assignments.get(v):
                    is_valid = False
                    break

        status = "Success" if (success and is_valid) else "Failure"

        # Build timetable entries & grid layout
        timetable_entries = []
        grid = {d: {p: [] for p in self.periods} for d in self.days}
        slot_lookup = {s['id']: s for s in self.slots}

        if success:
            for node_id, slot_id in assignments.items():
                slot_info = slot_lookup[slot_id]
                data = self.G.nodes[node_id]
                entry = {
                    "node_id": node_id,
                    "subject": data['subject'],
                    "teacher": data['teacher'],
                    "division": data['division'],
                    "room": data.get('room', 'Unassigned'),
                    "class_type": data.get('class_type', 'Theory'),
                    "colour": slot_id,

                    "slot_id": slot_id,
                    "day": slot_info['day'],
                    "period": slot_info['period']
                }
                timetable_entries.append(entry)
                grid[slot_info['day']][slot_info['period']].append(entry)

        return {
            "status": status,
            "success": success,
            "is_valid": is_valid,
            "total_classes": len(self.G.nodes()),
            "classes_assigned": len(assignments) if success else 0,
            "backtrack_count": self.backtrack_count,
            "recursive_calls": self.recursive_calls,
            "assignments_attempted": self.assignments_attempted,
            "successful_assignments": self.successful_assignments,
            "rejected_assignments": self.rejected_assignments,
            "execution_time": execution_time,
            "decision_log": self.decision_log,
            "timetable_entries": timetable_entries,
            "grid": grid,
            "days": self.days,
            "periods": self.periods,
            "assignments": assignments
        }

    def _backtrack(self, index, nodes, assignments):
        """Recursive core solver."""
        self.recursive_calls += 1

        # Base case: All classes assigned successfully
        if index == len(nodes):
            return True

        current_node = nodes[index]
        subject_name = self.G.nodes[current_node]['subject']

        # Try available time slots one by one
        for slot in self.slots:
            slot_id = slot['id']
            slot_name = slot['name']
            self.assignments_attempted += 1

            # Check whether candidate slot violates any graph conflict
            is_valid, conflict_neighbour = is_valid_assignment(current_node, slot_id, assignments, self.G)

            if is_valid:
                # Action: Assign candidate slot
                assignments[current_node] = slot_id
                self.successful_assignments += 1

                self.decision_log.append({
                    "class_id": current_node,
                    "subject": subject_name,
                    "slot_name": slot_name,
                    "day": slot['day'],
                    "period": slot['period'],
                    "decision": "Accepted",
                    "reason": "No neighbour conflict",
                    "action": f"Assigned to {slot_name}"
                })

                # Recursively continue to next class
                if self._backtrack(index + 1, nodes, assignments):
                    return True

                # If subsequent assignments failed downstream: BACKTRACK!
                del assignments[current_node]
                self.backtrack_count += 1

                self.decision_log.append({
                    "class_id": current_node,
                    "subject": subject_name,
                    "slot_name": slot_name,
                    "day": slot['day'],
                    "period": slot['period'],
                    "decision": "Backtracked",
                    "reason": "Subsequent class assignment failed downstream",
                    "action": f"Removed assignment from {slot_name} and backtracked"
                })
            else:
                self.rejected_assignments += 1
                self.decision_log.append({
                    "class_id": current_node,
                    "subject": subject_name,
                    "slot_name": slot_name,
                    "day": slot['day'],
                    "period": slot['period'],
                    "decision": "Rejected",
                    "reason": f"Conflicts with '{conflict_neighbour}' in slot {slot_name}",
                    "action": "Skipped slot"
                })

        return False


def solve_timetable_backtracking(G, days=None, periods=None):
    """Helper wrapper function to run backtracking solver."""
    solver = BacktrackingTimetableSolver(G, days, periods)
    return solver.solve()
