# Intelligent Timetable Optimization - Presentation Outline (15 Slides)

Presentation deck structure for project demonstration, capstone evaluation, and viva defense.

---

### Slide 1: Title Slide
- **Title**: Intelligent Timetable Optimization Using Graph Colouring, Backtracking and Constraint Analysis
- **Subtitle**: Automated Scheduling, Local Search Quality Scoring & Explainable AI
- **Presenter**: [Your Name / Team Name]
- **Guide / Institution**: Computer Engineering Department

---

### Slide 2: Problem Statement
- **Context**: College timetable scheduling is a complex combinatorial optimization problem.
- **Challenges**:
  - Manual double-booking of teachers, rooms, and student divisions.
  - Ignoring room capacities and specialized lab requirements.
  - Unbalanced workloads and excessive teacher idle gaps.
- **Goal**: Develop an intelligent, automated, web-based optimization system.

---

### Slide 3: Objectives
- Represent resource conflicts using **NetworkX Conflict Graphs**.
- Implement **Greedy Graph Colouring (Welch-Powell heuristic)** for rapid initialization.
- Implement **Recursive Backtracking (DFS)** to guarantee valid assignments.
- Evaluate 7 Hard and 3 Soft constraint rules via a **Constraint Analysis Engine**.
- Optimize timetable quality using **Hill-Climbing Local Search**.
- Provide human-explainable decisions (**"Why This Slot?"**) and **What-If Simulations**.

---

### Slide 4: Existing System vs Proposed System
- **Existing System**:
  - Manual spreadsheet grid construction.
  - High risk of double-booking teachers/rooms.
  - No automated constraint verification or quality scoring.
- **Proposed System**:
  - 100% automated graph-based conflict detection.
  - Dual solver engines (Greedy & Backtracking).
  - Hill-Climbing score optimization (+18 pts gain).
  - Transparent decision rationales & safe what-if simulation.

---

### Slide 5: System Architecture
- Flow Diagram:
  $$\text{JSON Dataset} \rightarrow \text{Conflict Graph} \rightarrow \text{Solvers} \rightarrow \text{Constraint Engine} \rightarrow \text{Optimizer} \rightarrow \text{Dashboard}$$
- Tech Stack: Python 3.11, Flask, NetworkX, Matplotlib, HTML5/CSS3, JavaScript, Chart.js, pytest.

---

### Slide 6: Conflict Graph & Greedy Colouring (Stage 3 & 4)
- **Conflict Graph**:
  - Vertices = Classes / Subjects.
  - Edges = Overlapping Teacher, Division, or Room.
- **Greedy Graph Colouring**:
  - Nodes ordered by degree descending (Welch-Powell).
  - Assigns lowest available color integer $\rightarrow$ mapped to (Day + Period).
  - Execution speed: $\approx 0.0002$ seconds.

---

### Slide 7: Backtracking Solver (Stage 5)
- **Depth-First Search Strategy**:
  - Explores decision tree recursively.
  - Degree-based variable ordering prunes invalid search branches early.
  - Backtracks upon hitting a dead-end slot assignment.
- **Result**: Guarantees finding a 100% feasible schedule when one exists ($\approx 0.0002$s, 9 recursive steps).

---

### Slide 8: Constraint Analysis Engine (Stage 6)
- **7 Hard Constraints**:
  - Teacher Conflict, Division Conflict, Room Conflict.
  - Teacher Availability, Room Availability.
  - Room Capacity ($\ge 60$ students), Lab Requirement.
- **3 Soft Constraints**:
  - Consecutive Lectures ($\ge 3$), Repeated Subject Same Day, Teacher Idle Gap.
- **Feasibility Rule**: Feasible only when Hard Violations $= 0$.

---

### Slide 9: Timetable Optimization & Quality Score (Stage 7)
- **Quality Score Formula**:
  $$\text{Quality Score} = \max(0, 100 - (\text{Hard Violations} \times 25) - (\text{Soft Violations} \times 5))$$
- **Hill-Climbing Local Search**:
  - Iteratively tests candidate single-slot moves.
  - Accepts moves yielding positive score gains without introducing hard violations.
  - Baseline score: **62/100** $\rightarrow$ Optimized score: **80/100** (+18 pts improvement).

---

### Slide 10: Algorithm Comparison (Stage 8)
- Dynamic Side-by-Side Benchmarking:
  - **Greedy**: Fast ($\approx 0.0002$s), basic quality.
  - **Backtracking**: Exact feasibility guarantee ($\approx 0.0002$s, 0 hard violations).
  - **Optimized**: Highest quality score (**80/100**, 0 soft violations, $\approx 0.03$s).

---

### Slide 11: Explainable Slot Decisions (Stage 9)
- **"Why This Slot?"**:
  - Inspects conflict graph neighbors, availability, capacity, and lab flags.
  - Explains why the assigned slot passed all constraints (`✓`).
- **"Why Not This Slot?"**:
  - Highlights specific hard/soft failure reasons for candidate rejected slots (`✗`).

---

### Slide 12: What-If Timetable Simulation (Stage 11)
- **Interactive Move Testing**:
  - Admin selects subject and candidate target slot.
  - Executes simulation on `copy.deepcopy()` to guarantee baseline schedule immutability.
- **Dynamic Output**:
  - Before vs After score comparison & violation deltas.
  - Newly created vs resolved violations.
  - Dynamic recommendation (`✓ Recommended`, `⚠ Neutral`, `✗ Not Recommended`).

---

### Slide 13: Professional Dashboard & Analytics (Stage 10)
- **Web Interface Highlights**:
  - Top 6 KPI cards (Total Classes, Conflicts, Quality Score, Slots Used).
  - Live Chart.js algorithm performance bar chart & constraint doughnut chart.
  - Weekly 5×6 timetable grid summary & conflict graph stats card.
  - RESTful JSON APIs (`/api/dashboard`, `/api/constraints`, `/api/optimization`).

---

### Slide 14: Testing & Advantages (Stage 12)
- **Testing Verification**:
  - Automated `pytest` suite with **37 / 37 passed tests** (100% pass rate in 2.05s).
  - Edge cases verified: empty dataset, single class, impossible dataset, API 404/400 errors.
- **Key Advantages**:
  - 100% automated conflict prevention.
  - Transparent explainability and safe simulation.

---

### Slide 15: Conclusion & Future Scope
- **Conclusion**: Successfully combined graph coloring, recursive backtracking, constraint analysis, and local search to solve academic timetable optimization.
- **Future Scope**:
  - Relational database integration (PostgreSQL / SQLAlchemy).
  - Multi-department concurrent scheduling.
  - Machine learning for faculty preference learning.
  - Cloud deployment.
- **Q&A**: Thank you! Questions?
