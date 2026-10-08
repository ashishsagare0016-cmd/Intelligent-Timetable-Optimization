# Intelligent Timetable Optimization - Technical Algorithm Notes

Detailed technical reference for the 8 core algorithms and processing modules implemented in the project.

---

## 1. Conflict Graph Generator (`algorithms/conflict_graph.py`)

- **Purpose**: Models timetable classes as graph nodes and resource overlaps as conflict edges.
- **Input**: Raw JSON dataset containing subjects, teachers, rooms, and divisions.
- **Processing**:
  1. Iterates over all subjects to create graph nodes with attributes (`teacher`, `division`, `room`, `type`, `requires_lab`).
  2. Performs pairwise node comparison ($O(V^2)$). Adds an edge $(u, v)$ if $u$ and $v$ share the same teacher, division, or room.
  3. Generates graph metrics (total nodes, total edges, max degree, avg degree).
  4. Renders PNG visual image using Matplotlib with `Agg` headless backend.
- **Output**: NetworkX `nx.Graph` instance, statistics dictionary, and `static/generated/conflict_graph.png`.
- **Time Complexity**: $O(V^2)$ where $V$ is the number of subjects.
- **Space Complexity**: $O(V + E)$ where $E$ is the number of conflict edges.
- **Advantages**: Visualizes bottleneck subjects with high degree count.
- **Limitations**: Pairwise comparison scales quadratically for extremely large subject counts.

---

## 2. Greedy Graph Colouring (`algorithms/graph_coloring.py`)

- **Purpose**: Generates a fast initial timetable assignment using node degree heuristic.
- **Input**: NetworkX conflict graph $G$, days list, periods list.
- **Processing**:
  1. Sorts graph nodes by vertex degree descending (Welch-Powell Largest Degree First heuristic).
  2. Iterates through sorted nodes. For each node, inspects colors already assigned to its graph neighbors.
  3. Assigns the smallest positive integer color not used by any neighbor.
  4. Maps color integers to discrete time slots (Day + Period).
- **Output**: Dictionary mapping nodes to time slots, structured timetable entry objects, execution time.
- **Time Complexity**: $O(V \log V + V + E)$.
- **Space Complexity**: $O(V)$.
- **Advantages**: Extremely fast execution ($\approx 0.0002$s).
- **Limitations**: Heuristic approach; does not backtrack if a color mapping violates room availability or capacity.

---

## 3. Backtracking Timetable Solver (`algorithms/backtracking.py`)

- **Purpose**: Guarantees a feasible timetable assignment satisfying all hard conflict rules using Depth-First Search.
- **Input**: Conflict graph $G$, days list, periods list.
- **Processing**:
  1. Variable Ordering: Sorts nodes by vertex degree descending.
  2. Recursive DFS function `_backtrack(node_index, assignments)`:
     - If all nodes are assigned, returns `True` (solution found).
     - Tries assigning available slots to the current node.
     - Checks validity against assigned neighbors.
     - If valid, recursively calls `_backtrack(node_index + 1)`.
     - If recursive call returns `False`, undoes (backtracks) the assignment.
- **Output**: Feasible timetable entries, execution time, backtrack count, recursive call count.
- **Time Complexity**: Worst-case $O(K^V)$ where $K$ is slot count. Pruned efficiently by degree ordering.
- **Space Complexity**: $O(V)$ recursion stack.
- **Advantages**: Guarantees finding a valid solution if one exists.
- **Limitations**: Worst-case exponential time complexity if constraints are overly tight.

---

## 4. Constraint Analysis Engine (`algorithms/constraints.py`)

- **Purpose**: Evaluates timetable entries against 7 Hard and 3 Soft constraint rules.
- **Input**: List of scheduled timetable entries and raw dataset specifications.
- **Processing**:
  1. **Hard Rules**: Teacher Conflict, Division Conflict, Room Conflict, Teacher Availability, Room Availability, Room Capacity, Lab Requirement.
  2. **Soft Rules**: Consecutive Lectures ($\ge 3$), Repeated Subject Same Day, Teacher Gap.
  3. Aggregates violation counts and sets `is_feasible = (hard_violations == 0)`.
- **Output**: Diagnostic report containing violation lists, counts, feasibility flag, and summary breakdown.
- **Time Complexity**: $O(N)$ where $N$ is the number of scheduled entries.
- **Space Complexity**: $O(N)$.
- **Advantages**: Comprehensive diagnostic breakdown of hard vs soft violations.
- **Limitations**: Fixed rule definitions; custom constraints require code additions.

---

## 5. Quality Score Calculator (`algorithms/optimizer.py`)

- **Purpose**: Computes an empirical numeric quality score on a 0–100 scale.
- **Input**: Constraint analysis diagnostic dictionary.
- **Processing**:
  $$\text{Quality Score} = \max(0, 100 - (\text{Hard Violations} \times 25) - (\text{Soft Violations} \times 5))$$
- **Output**: Score integer (0–100), rating text (Optimal, Good, Acceptable, Poor), penalty details.
- **Time Complexity**: $O(1)$.
- **Space Complexity**: $O(1)$.
- **Advantages**: Standardized metric for comparing different timetables.
- **Limitations**: Linear penalty weights (25 and 5).

---

## 6. Hill-Climbing Local Search Optimizer (`algorithms/optimizer.py`)

- **Purpose**: Optimizes timetable quality by adjusting class slot assignments.
- **Input**: Initial feasible timetable entries and dataset specifications.
- **Processing**:
  1. Calculates initial score.
  2. Iterates up to `max_iterations` (default 50).
  3. For each scheduled class entry, generates candidate target slots.
  4. Temporarily mutates entry slot, evaluates neighbor Quality Score.
  5. If neighbor score is strictly higher AND introduces no hard violations, accepts move and updates baseline.
  6. Stops when no candidate move yields an improvement (local optimum).
- **Output**: Optimized timetable entries, final score, score improvement, candidate/accepted move counts.
- **Time Complexity**: $O(I \cdot N \cdot K)$ where $I$ is iterations, $N$ is entries, $K$ is slots.
- **Space Complexity**: $O(N)$.
- **Advantages**: Consistently improves soft constraint quality without breaking hard feasibility.
- **Limitations**: Local search can potentially get trapped in a local optimum.

---

## 7. Algorithm Comparison Engine (`algorithms/comparison.py`)

- **Purpose**: Executes Greedy, Backtracking, and Optimizer on the same dataset for comparative analysis.
- **Input**: Raw dataset specifications.
- **Processing**:
  1. Measures execution time, quality score, hard/soft violations, and slots used for all 3 strategies.
  2. Dynamically identifies the best algorithm based on `(-score, hard_violations, soft_violations, time)`.
  3. Generates dynamic text observations.
- **Output**: Unified dictionary containing metrics for all 3 algorithms and observations.
- **Time Complexity**: Sum of individual algorithm complexities.
- **Space Complexity**: $O(N)$.
- **Advantages**: Fair, dynamic side-by-side benchmarking.
- **Limitations**: Dependent on CPU performance variations during timing.

---

## 8. What-If Simulation Engine (`algorithms/simulation.py`)

- **Purpose**: Simulates moving a subject to a candidate target slot without modifying the baseline schedule.
- **Input**: Subject name, target slot string, baseline timetable entries, raw dataset.
- **Processing**:
  1. Deep copies timetable entries (`copy.deepcopy(entries)`).
  2. Mutates subject slot in the copied entries.
  3. Analyzes baseline (before) and simulated (after) timetables.
  4. Calculates score change, hard/soft violation deltas, new violations, and resolved violations.
  5. Generates dynamic recommendation (`✓ Recommended`, `⚠ No Significant Change`, `✗ Not Recommended`).
  6. Records run in in-memory session history (capped at 10 items).
- **Output**: Simulation result JSON dictionary and status code.
- **Time Complexity**: $O(N)$ constraint analysis.
- **Space Complexity**: $O(N)$ for deep copy.
- **Advantages**: 100% safe isolated testing environment.
- **Limitations**: In-memory session history resets on server restart.
