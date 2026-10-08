# Project Screenshot Capture Checklist

Guide detailing the 12 screenshots to capture for project documentation, report submission, and viva presentation.

---

## 1. Main Professional Dashboard (`/`)
- **URL**: `http://127.0.0.1:5000/`
- **What should be visible**:
  - Hero banner title and subtitle.
  - 6 Top KPI cards (Total Classes, Conflict Edges, Hard Violations, Soft Violations, Quality Score, Slots Used).
  - Project Status verification list (`✓ Completed`).
  - Initial vs. Final Quality Score box (+18 points banner).
  - Chart.js Algorithm Performance bar chart and Constraint doughnut chart.
  - Compact Weekly Timetable Grid summary.
  - Conflict Graph summary card and Quick Actions grid.

## 2. Input Data Specifications (`/data`)
- **URL**: `http://127.0.0.1:5000/data`
- **What should be visible**:
  - Division name (`TY-C`) and student count (`60`).
  - Table of Subjects (Subject Name, Type, Lab Requirement).
  - Table of Teachers (Teacher Name, Assigned Subjects, Unavailable Slots).
  - Table of Rooms (Room Name, Type, Capacity, Unavailable Slots).
  - Raw JSON specification viewer.

## 3. Conflict Graph Page (`/graph`)
- **URL**: `http://127.0.0.1:5000/graph`
- **What should be visible**:
  - Graph statistics cards (Nodes: 8, Edges: 28, Max Degree: 7, Avg Degree: 7.0).
  - Generated Matplotlib PNG image (`static/generated/conflict_graph.png`).
  - Table of detected conflict pairs and detailed reasons (Same Teacher, Same Division, Same Room).

## 4. Greedy Graph Colouring Timetable (`/timetable`)
- **URL**: `http://127.0.0.1:5000/timetable`
- **What should be visible**:
  - Algorithm summary badge (Colors Used, Execution Time).
  - Full 5-Day × 6-Period timetable grid displaying scheduled subjects, teachers, and rooms.
  - Color-to-Slot mapping table.

## 5. Backtracking Solver Page (`/backtracking`)
- **URL**: `http://127.0.0.1:5000/backtracking`
- **What should be visible**:
  - Solver metrics cards (Success status, Execution time, Backtrack count: 0, Recursive calls: 9).
  - Full backtracking timetable schedule grid.
  - Step-by-step variable ordering execution log.

## 6. Constraint Analysis Engine (`/constraints`)
- **URL**: `http://127.0.0.1:5000/constraints`
- **What should be visible**:
  - Feasibility badge banner (`✓ Feasible` or `✗ Infeasible`).
  - Diagnostic metric summary cards (Hard Violations, Soft Violations, Total Violations).
  - Detailed diagnostic table of hard and soft rule violations with constraint names, subjects, days, periods, and messages.

## 7. Optimization Engine Page (`/optimize`)
- **URL**: `http://127.0.0.1:5000/optimize`
- **What should be visible**:
  - Initial Quality Score (62/100) vs Final Quality Score (80/100) highlight box.
  - Local Search metrics cards (Iterations: 3, Candidate Moves: 363, Accepted Moves: 5).
  - Optimized weekly timetable grid.
  - Accepted moves iteration log.

## 8. Algorithm Comparison Dashboard (`/comparison`)
- **URL**: `http://127.0.0.1:5000/comparison`
- **What should be visible**:
  - Best Algorithm badge (`Hill-Climbing Optimized Timetable`).
  - Side-by-side comparative table (Greedy vs Backtracking vs Optimized).
  - Chart.js Quality Score bar chart and Execution Time comparison chart.
  - Dynamic observations bulleted list.

## 9. Explainable Slot Decisions ("Why This Slot?") (`/explain`)
- **URL**: `http://127.0.0.1:5000/explain`
- **What should be visible**:
  - Subject selector dropdown (e.g. `Operating Systems`).
  - Currently assigned slot badge (`Tuesday P5`).
  - "Why This Slot?" green checkmark (`✓`) reasons box.
  - "Why Not Other Slots?" grid displaying red cross (`✗`) reasons for alternative candidate slots.

## 10. What-If Timetable Simulation (`/simulation`)
- **URL**: `http://127.0.0.1:5000/simulation`
- **What should be visible**:
  - Subject and target slot dropdown parameter controls (`Operating Systems` $\rightarrow$ `Monday P3`).
  - Recommendation banner (`✗ Not Recommended (Reduces overall timetable quality score)`).
  - Baseline vs Simulated metrics comparison grid (Quality Score: 80 $\rightarrow$ 74).
  - Newly Created Violations list (`Too Many Consecutive Lectures`, `Teacher Gap`).
  - Recent Simulation History table.

## 11. Automated Test Suite Execution Result
- **Command**: `.\venv\Scripts\python.exe -m pytest -v`
- **What should be visible**:
  - Terminal output showing all 37 test cases passed (`37 passed in 2.05s`).

## 12. RESTful JSON API Response
- **URL**: `http://127.0.0.1:5000/api/dashboard`
- **What should be visible**:
  - Pretty-printed JSON output showing `summary`, `quality`, `algorithms`, `constraints`, `graph`, `timetable`, and `key_results`.
