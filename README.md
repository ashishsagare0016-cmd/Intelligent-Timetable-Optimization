# Intelligent Timetable Optimization Using Graph Colouring, Backtracking and Constraint Analysis

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.0+-blue?style=flat)](https://networkx.org/)
[![Tests](https://img.shields.io/badge/Pytest-37%20Passed-brightgreen?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Status](https://img.shields.io/badge/Project%20Status-Implementation%20Complete-success?style=flat)]()

An intelligent, web-based college timetable generation, constraint analysis, optimization, and decision-explanation system built using Python, Flask, NetworkX, Graph Colouring, Backtracking, and Hill-Climbing Local Search.

---

## 1. Project Overview

The **Intelligent Timetable Optimization System** automates the complex task of college timetable scheduling. Scheduling classes manually often causes resource conflicts (e.g., a teacher assigned to two places at once, room overlaps, or division double-booking). 

This project models classes as vertices and resource conflicts as edges in a NetworkX Graph. It applies **Greedy Graph Colouring (Welch-Powell heuristic)** and **Recursive Backtracking (Depth-First Search)** to generate feasible conflict-free timetables. It then applies a **Hill-Climbing Local Search Optimizer** to maximize schedule quality based on hard and soft constraints, provides **Explainable Slot Decisions** ("Why This Slot?" / "Why Not This Slot?"), enables **What-If Timetable Simulations**, and visualizes comparative metrics across algorithms.

---

## 2. Problem Statement

Timetable scheduling is a known NP-hard combinatorial optimization problem. A valid timetable must assign classes to discrete time slots while obeying multi-dimensional constraints:

- **Teacher Conflicts**: A teacher cannot teach two different classes in the same time slot.
- **Division Conflicts**: A student division cannot attend two different classes simultaneously.
- **Room Conflicts**: A classroom cannot host multiple classes in the same time slot.
- **Availability Constraints**: Teachers and rooms have specific unavailable time slots.
- **Room Capacity Constraints**: Classroom capacity must accommodate the student count.
- **Laboratory Requirements**: Practical classes require dedicated laboratory space.
- **Timetable Quality**: Minimizing teacher idle gaps, excessive consecutive lectures, and unbalanced daily workloads.

---

## 3. Objectives

1. Generate conflict-free timetable assignments automatically.
2. Represent resource conflicts dynamically using NetworkX graph structures.
3. Apply Greedy Graph Colouring for rapid timetable initialization.
4. Implement Recursive Backtracking to guarantee feasibility under tight constraints.
5. Evaluate 7 Hard and 3 Soft constraint rules via a dedicated Constraint Engine.
6. Compute an empirical Quality Score (0–100 scale) for timetable schedules.
7. Optimize timetable quality using Hill-Climbing Local Search.
8. Compare execution speed, quality scores, and backtracks across algorithms.
9. Provide human-explainable slot decision rationales ("Why This Slot?").
10. Allow interactive "What-If" timetable move simulations without mutating baseline schedules.

---

## 4. Technologies Used

- **Python 3.11**: Primary programming language for backend algorithms.
- **Flask**: Web application framework and RESTful API endpoints.
- **NetworkX**: Graph theory data structure for conflict representation and node degree calculations.
- **Matplotlib**: Server-side headless visualization for conflict graph rendering (`Agg` backend).
- **HTML5 & CSS3**: Responsive web layout with CSS grid, variables, and modern cards.
- **Vanilla JavaScript (ES6)**: Dynamic DOM updates and asynchronous API fetches.
- **Chart.js**: Client-side interactive bar and doughnut charts.
- **pytest**: Automated unit testing and edge-case verification framework.

---

## 5. System Architecture

```
                       [ Input Dataset (JSON) ]
                                  │
                                  ▼
                     [ Conflict Graph (NetworkX) ]
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
       [ Greedy Graph Colouring ]      [ Backtracking Solver ]
                  │                               │
                  └───────────────┬───────────────┘
                                  ▼
                    [ Constraint Analysis Engine ]
                        (7 Hard + 3 Soft Rules)
                                  │
                                  ▼
                     [ Quality Score (0 - 100) ]
                                  │
                                  ▼
                   [ Hill-Climbing Local Search ]
                                  │
                  ┌───────────────┼───────────────┐
                  ▼               ▼               ▼
           [ Comparison ]   [ Explainability ] [ What-If Sim ]
                  │               │               │
                  └───────────────┼───────────────┘
                                  ▼
                 [ Professional Dashboard & APIs ]
```

---

## 6. Project Structure

```
Intelligent-Timetable-Optimization/
├── app.py                      # Flask application entry point & web/API routes
├── requirements.txt            # Project dependencies (Flask, NetworkX, Matplotlib, pytest)
├── models/
│   ├── __init__.py
│   └── timetable_model.py     # Dataclasses for Subject, Teacher, Room, TimetableEntry
├── data/
│   └── sample_data.json       # Computer Engineering dataset (TY-C division, 8 subjects)
├── algorithms/
│   ├── __init__.py
│   ├── conflict_graph.py      # NetworkX conflict graph builder & PNG visualizer
│   ├── graph_coloring.py      # Greedy Graph Colouring (Welch-Powell degree heuristic)
│   ├── backtracking.py        # Recursive Backtracking DFS Solver
│   ├── constraints.py         # Constraint Engine (7 Hard + 3 Soft rules)
│   ├── optimizer.py           # Hill-Climbing Local Search & Quality Scoring (0-100)
│   ├── comparison.py          # Dynamic Algorithm Comparison Engine
│   ├── explanation.py         # Explainable Slot Decision Engine ("Why This Slot?")
│   ├── simulation.py          # What-If Simulation Engine & Session History
│   └── dashboard.py           # Dashboard Analytics & Metric Aggregator
├── static/
│   ├── css/
│   │   └── style.css          # Responsive CSS stylesheet
│   ├── js/
│   │   └── main.js           # Client-side JavaScript helpers
│   └── generated/
│       └── conflict_graph.png # Server-rendered conflict graph visualization
├── templates/
│   ├── base.html              # Shared layout template with top navigation
│   ├── index.html             # Stage 10 Main Dashboard UI
│   ├── data.html              # Input Data Specs page
│   ├── graph.html             # Conflict Graph page
│   ├── timetable.html         # Greedy Timetable page
│   ├── backtracking.html      # Backtracking Solver page
│   ├── constraints.html       # Constraint Analysis page
│   ├── optimization.html      # Optimization Engine page
│   ├── comparison.html       # Algorithm Comparison page
│   ├── explain.html          # Why This Slot? page
│   └── simulation.html       # What-If Simulation page
├── tests/
│   ├── __init__.py
│   ├── test_coloring.py       # Graph Colouring unit tests
│   ├── test_backtracking.py   # Backtracking Solver unit tests
│   ├── test_constraints.py    # Constraint Engine unit tests
│   ├── test_optimizer.py      # Local Search Optimizer unit tests
│   ├── test_simulation.py     # What-If Simulation & Immutability unit tests
│   ├── test_comparison.py     # Algorithm Comparison unit tests
│   ├── test_api_and_edge_cases.py # Flask API error handling & data edge cases
│   └── TEST_REPORT.md         # Full test suite execution report
└── docs/                      # Comprehensive college project documentation
    ├── PROJECT_REPORT.md      # Formal Project Report Document (24 Sections)
    ├── VIVA_NOTES.md          # 34 Q&A Viva Exam Preparation Guide
    ├── ALGORITHM_NOTES.md     # Deep-dive Algorithm & Complexity Notes
    ├── PRESENTATION_OUTLINE.md # 15-Slide Presentation Deck Outline
    ├── SCREENSHOT_CHECKLIST.md # Screenshot Capture Guide
    └── FINAL_CHECKLIST.md     # Pre-submission Verification Checklist
```

---

## 7. Algorithms

### A. Greedy Graph Colouring
- **Concept**: Represents classes as graph nodes and conflicts as edges. Colors represent time slots (Day + Period).
- **Ordering**: Sorts nodes by vertex degree descending (Welch-Powell Largest Degree First heuristic).
- **Slot Assignment**: Iteratively assigns the lowest color integer not used by any neighbor.

### B. Backtracking (Depth-First Search)
- **Concept**: Explores the assignment search space recursively.
- **Variable Ordering**: Degree-based node ordering.
- **Backtrack Step**: If a partial assignment leads to a dead end (no valid slot available), the solver backtracks to the previous decision point.

### C. Constraint Analysis Engine
- **Hard Constraints (7 Rules)**: Teacher Conflict, Division Conflict, Room Conflict, Teacher Availability, Room Availability, Room Capacity, Lab Requirement.
- **Soft Constraints (3 Rules)**: Consecutive Lectures (≥3), Repeated Subject Same Day, Teacher Idle Gap.

### D. Quality Scoring & Hill-Climbing Optimization
- **Quality Score**: Computed on a 0–100 scale:
  $$\text{Quality Score} = \max(0, 100 - (\text{Hard Violations} \times 25) - (\text{Soft Violations} \times 5))$$
- **Hill-Climbing Local Search**: Starts from a feasible timetable, generates candidate single-slot moves, evaluates neighbor quality, and adopts moves that strictly improve the Quality Score.

---

## 8. Complexity Analysis

| Algorithm / Module | Time Complexity | Space Complexity | Explanation |
| :--- | :--- | :--- | :--- |
| **Conflict Graph Construction** | $O(V^2)$ | $O(V + E)$ | Pairwise check across $V$ subjects for teacher, division, and room overlap. |
| **Greedy Graph Colouring** | $O(V^2 + E)$ | $O(V + E)$ | Degree sorting $O(V \log V)$ plus checking neighbor colors $O(V + E)$. |
| **Backtracking Solver** | $O(K^V)$ worst-case | $O(V)$ recursion depth | $K$ available time slots, $V$ subjects. Pruned efficiently by degree ordering. |
| **Constraint Analysis Engine** | $O(N + R)$ | $O(N)$ | Single-pass schedule mapping across $N$ timetable entries and $R$ constraint rules. |
| **Hill-Climbing Optimizer** | $O(I \cdot N \cdot K)$ | $O(N)$ | $I$ iterations × $N$ subjects × $K$ candidate slot moves per iteration. |

---

## 9. Application Routes

| Path | Type | HTTP Method | Description |
| :--- | :--- | :---: | :--- |
| `/` | Web Page | `GET` | Stage 10 Main Professional Dashboard |
| `/data` | Web Page | `GET` | Input Data Specs & JSON view |
| `/graph` | Web Page | `GET` | NetworkX Conflict Graph & visual image |
| `/timetable` | Web Page | `GET` | Greedy Graph Colouring Timetable Grid |
| `/backtracking` | Web Page | `GET` | Backtracking Solver Timetable Grid |
| `/constraints` | Web Page | `GET` | Hard & Soft Constraint Analysis Engine |
| `/optimize` | Web Page | `GET` | Hill-Climbing Optimization Results |
| `/comparison` | Web Page | `GET` | Algorithm Comparison Dashboard |
| `/explain` | Web Page | `GET` | Explainable Slot Decisions ("Why This Slot?") |
| `/simulation` | Web Page | `GET` | What-If Timetable Simulation |
| `/api/dashboard` | REST API | `GET` | Real-time Dashboard Analytics JSON |
| `/api/constraints` | REST API | `GET` | Constraint Violations & Diagnostics JSON |
| `/api/optimization` | REST API | `GET` | Optimization Metrics & Move Log JSON |
| `/api/comparison` | REST API | `GET` | Algorithm Comparison Results JSON |
| `/api/explain/<subject>`| REST API | `GET` | Subject Slot Explanation JSON |
| `/api/simulate` | REST API | `POST` | Execute What-If Simulation JSON |

---

## 10. How to Install

```bash
# 1. Clone repository
git clone https://github.com/your-username/Intelligent-Timetable-Optimization.git
cd Intelligent-Timetable-Optimization

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 11. How to Run

```bash
# Start Flask server
python app.py
```

Open your browser and navigate to:  
**`http://127.0.0.1:5000/`**

---

## 12. Testing

The project includes an automated test suite using `pytest`.

```bash
# Run complete test suite
python -m pytest -v
```

### Test Results Summary:
- **Total Tests**: 37 passed
- **Pass Rate**: 100%
- **Execution Speed**: 2.05 seconds
- **Covered Modules**: Graph Colouring, Backtracking, Constraints, Optimizer, What-If Simulation (Immutability), Algorithm Comparison, and API Edge Cases (404/400).

---

## 13. Features

- **Automated Conflict Graph Generation**: Dynamic NetworkX graph construction and server-rendered Matplotlib PNG.
- **Dual Solver Engines**: Greedy Graph Colouring (Welch-Powell) and Depth-First Search Backtracking.
- **Diagnostic Constraint Engine**: Automatic evaluation of 7 Hard and 3 Soft constraint rules.
- **Empirical Quality Score**: 0–100 quality scoring formula.
- **Hill-Climbing Local Search**: Automated score improvement engine (+18 points on sample dataset).
- **Dynamic Algorithm Comparison**: Side-by-side performance benchmarks and Chart.js charts.
- **Explainable Slot Decision Engine**: Human-understandable rationales ("Why This Slot?" & "Why Not This Slot?").
- **Interactive What-If Simulation**: Test hypothetical schedule moves on an isolated deep copy without modifying the baseline timetable.
- **Professional Dashboard**: Top KPI cards, project status, timetable grid summary, and live analytics API.

---

## 14. Future Scope

- **Database Integration**: Migrate from JSON files to PostgreSQL / MySQL with SQLAlchemy ORM.
- **Multi-Department Support**: Concurrent scheduling across multiple departments and semesters.
- **Faculty & Student Preference Learning**: Weighting soft constraints using machine learning.
- **Advanced Heuristic Solvers**: Genetic Algorithms, Simulated Annealing, and Tabu Search comparisons.
- **Cloud Deployment**: Containerization with Docker and deployment on Google Cloud Run or AWS.

---

## 15. Conclusion

The **Intelligent Timetable Optimization System** successfully demonstrates how graph theory (Graph Colouring), recursive search (Backtracking), constraint satisfaction, and local search optimization (Hill-Climbing) can be combined to solve real-world scheduling problems. The system produces verifiable, optimal timetables, provides human-explainable decisions, and offers an intuitive web interface for interactive simulation and monitoring.

---

**Project Status**: `Implementation Complete`
