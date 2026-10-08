"""
Graph Colouring Algorithm for Timetable Generation
Uses a Greedy Degree-Based Ordering (Largest Degree First / Welch-Powell heuristic).
"""
import time


def color_to_slot(color_id, days, periods):
    """
    Maps a 1-based color ID to a (Day, Period) tuple.
    Color 1  -> Monday P1
    Color 2  -> Monday P2
    ...
    Color 30 -> Friday P6
    """
    if color_id < 1:
        color_id = 1

    total_periods = len(periods)
    day_idx = (color_id - 1) // total_periods
    period_idx = (color_id - 1) % total_periods

    # Wrap around safely if colors exceed available slots
    if day_idx >= len(days):
        day_idx = day_idx % len(days)

    return days[day_idx], periods[period_idx]


def greedy_graph_coloring(G, days=None, periods=None):
    """
    Executes Greedy Graph Colouring with Degree-Based Ordering.

    Algorithm Steps:
    1. Calculate degree of every vertex in G.
    2. Sort vertices in descending order of degree (most constrained vertices first).
    3. For each vertex, assign the smallest positive integer color not used by its neighbours.
    4. Map assigned colors to timetable time slots (Day + Period).
    """
    if days is None:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    if periods is None:
        periods = ["P1", "P2", "P3", "P4", "P5", "P6"]

    start_time = time.perf_counter()

    # Step 1 & 2: Sort vertices by degree in descending order (Largest Degree First)
    # Classes with higher conflict degree are processed earlier so that highly constrained
    # classes receive valid slots before fewer options remain.
    sorted_nodes = sorted(G.nodes(), key=lambda n: G.degree(n), reverse=True)

    color_assignments = {}  # node_id -> color_id (1, 2, 3...)

    # Step 3: Greedy colouring loop
    for node in sorted_nodes:
        # Find colors already used by neighbouring classes
        neighbor_colors = {
            color_assignments[neighbor]
            for neighbor in G.neighbors(node)
            if neighbor in color_assignments
        }

        # Find the smallest positive color integer (starting from 1) not used by any neighbor
        assigned_color = 1
        while assigned_color in neighbor_colors:
            assigned_color += 1

        color_assignments[node] = assigned_color

    end_time = time.perf_counter()
    execution_time = round(end_time - start_time, 6)

    # Step 4: Validate colouring correctness (No two connected nodes share the same color)
    is_valid = True
    invalid_conflicts = []
    conflicts_checked = 0

    for u, v in G.edges():
        conflicts_checked += 1
        if color_assignments.get(u) == color_assignments.get(v):
            is_valid = False
            invalid_conflicts.append({
                "class1": G.nodes[u]['subject'],
                "class2": G.nodes[v]['subject'],
                "color": color_assignments.get(u)
            })

    # Step 5: Build final timetable entry objects & color mappings
    timetable_entries = []
    color_mappings = []
    used_colors = set(color_assignments.values())

    # Build color-to-slot dictionary map
    color_slot_map = {}
    for c in sorted(used_colors):
        day, period = color_to_slot(c, days, periods)
        color_slot_map[c] = {"day": day, "period": period}
        color_mappings.append({
            "color": c,
            "day": day,
            "period": period
        })

    # Build timetable entries per node
    for node_id, data in G.nodes(data=True):
        c = color_assignments[node_id]
        slot = color_slot_map[c]
        timetable_entries.append({
            "node_id": node_id,
            "subject": data['subject'],
            "teacher": data['teacher'],
            "division": data['division'],
            "room": data.get('room', 'Unassigned'),
            "class_type": data.get('class_type', 'Theory'),
            "colour": c,

            "day": slot['day'],
            "period": slot['period']
        })

    # Organize timetable into a 2D grid structure [day][period] -> list of entries
    grid = {d: {p: [] for p in periods} for d in days}
    for entry in timetable_entries:
        grid[entry['day']][entry['period']].append(entry)

    return {
        "color_assignments": color_assignments,
        "total_classes": len(G.nodes()),
        "colors_used": len(used_colors),
        "available_slots": len(days) * len(periods),
        "is_valid": is_valid,
        "invalid_conflicts": invalid_conflicts,
        "execution_time": execution_time,
        "conflicts_checked": conflicts_checked,
        "color_mappings": color_mappings,
        "timetable_entries": timetable_entries,
        "grid": grid,
        "days": days,
        "periods": periods,
        "sorted_node_degrees": [
            {"id": n, "subject": G.nodes[n]['subject'], "degree": G.degree(n), "color": color_assignments[n]}
            for n in sorted_nodes
        ]
    }
