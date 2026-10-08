import os
import json
from urllib.parse import unquote
from flask import Flask, render_template, jsonify, request
from models import TimetableData
from algorithms import (
    build_conflict_graph,
    get_graph_statistics,
    generate_graph_image,
    greedy_graph_coloring,
    solve_timetable_backtracking,
    analyze_timetable,
    optimize_timetable,
    calculate_quality_score,
    run_algorithm_comparison,
    explain_subject_slot_decision,
    get_dashboard_data,
    simulate_move,
    get_simulation_history
)


from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def load_dataset():
    """Helper function to load sample data from JSON."""
    json_path = os.path.join(app.root_path, 'data', 'sample_data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    return raw_data, TimetableData.from_dict(raw_data)


@app.route('/')
def home():
    raw_data, _ = load_dataset()
    dashboard_data = get_dashboard_data(raw_data, app_root_path=app.root_path)
    return render_template('index.html', d=dashboard_data)


@app.route('/api/dashboard')
def api_dashboard():
    raw_data, _ = load_dataset()
    dashboard_data = get_dashboard_data(raw_data, app_root_path=app.root_path)
    return jsonify(dashboard_data)



@app.route('/data')
def show_data():
    raw_data, structured_data = load_dataset()
    return render_template('data.html', data=raw_data, timetable=structured_data)


@app.route('/graph')
def show_graph():
    raw_data, _ = load_dataset()

    # 1. Build conflict graph using NetworkX
    G = build_conflict_graph(raw_data)

    # 2. Get graph statistics & conflict lists
    stats = get_graph_statistics(G)

    # 3. Generate visual graph image in static/generated/
    image_rel_path = os.path.join('generated', 'conflict_graph.png')
    image_full_path = os.path.join(app.root_path, 'static', image_rel_path)
    generate_graph_image(G, image_full_path)

    return render_template('graph.html', stats=stats, image_file='generated/conflict_graph.png')


@app.route('/timetable')
def show_timetable():
    raw_data, _ = load_dataset()

    # 1. Build conflict graph using NetworkX
    G = build_conflict_graph(raw_data)

    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    # 2. Run greedy graph-colouring algorithm
    result = greedy_graph_coloring(G, days=days, periods=periods)

    return render_template('timetable.html', result=result, timetable=raw_data)


@app.route('/backtracking')
def show_backtracking():
    raw_data, _ = load_dataset()

    # 1. Build conflict graph using NetworkX
    G = build_conflict_graph(raw_data)

    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    # 2. Run backtracking solver
    result = solve_timetable_backtracking(G, days=days, periods=periods)

    return render_template('backtracking.html', result=result, timetable=raw_data)


@app.route('/constraints')
def show_constraints():
    raw_data, _ = load_dataset()
    G = build_conflict_graph(raw_data)

    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    # Generate timetable using greedy algorithm
    tt_result = greedy_graph_coloring(G, days=days, periods=periods)

    # Run constraint analysis engine
    analysis = analyze_timetable(tt_result['timetable_entries'], raw_data)

    return render_template('constraints.html', analysis=analysis, timetable=raw_data)


@app.route('/api/constraints')
def api_constraints():
    raw_data, _ = load_dataset()
    G = build_conflict_graph(raw_data)

    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    tt_result = greedy_graph_coloring(G, days=days, periods=periods)
    analysis = analyze_timetable(tt_result['timetable_entries'], raw_data)

    return jsonify(analysis)


@app.route('/optimize')
def show_optimize():
    raw_data, _ = load_dataset()
    G = build_conflict_graph(raw_data)

    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    # 1. Run backtracking algorithm to get initial timetable
    bt_result = solve_timetable_backtracking(G, days=days, periods=periods)

    # 2. Run local-search hill-climbing optimization engine
    opt_result = optimize_timetable(bt_result['timetable_entries'], raw_data)

    return render_template('optimization.html', opt=opt_result, timetable=raw_data)


@app.route('/api/optimization')
def api_optimization():
    raw_data, _ = load_dataset()
    G = build_conflict_graph(raw_data)

    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    bt_result = solve_timetable_backtracking(G, days=days, periods=periods)
    opt_result = optimize_timetable(bt_result['timetable_entries'], raw_data)

    return jsonify(opt_result)


@app.route('/comparison')
def show_comparison():
    raw_data, _ = load_dataset()
    comp_result = run_algorithm_comparison(raw_data)
    return render_template('comparison.html', comp=comp_result, timetable=raw_data)


@app.route('/api/comparison')
def api_comparison():
    raw_data, _ = load_dataset()
    comp_result = run_algorithm_comparison(raw_data)
    return jsonify(comp_result)


@app.route('/explain')
def show_explain():
    raw_data, _ = load_dataset()
    subjects = [s['name'] for s in raw_data.get('subjects', [])]
    default_subject = subjects[0] if subjects else ""

    explanation_data, status_code = explain_subject_slot_decision(default_subject, raw_data)
    return render_template('explain.html', subjects=subjects, default_subject=default_subject, explanation=explanation_data)


@app.route('/api/explain/<path:subject_name>')
def api_explain(subject_name):
    raw_data, _ = load_dataset()
    decoded_subject = unquote(subject_name)
    result, status_code = explain_subject_slot_decision(decoded_subject, raw_data)
    return jsonify(result), status_code


def get_best_timetable(raw_data):

    """Retrieves the best available baseline timetable using fallback hierarchy."""
    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])
    try:
        G = build_conflict_graph(raw_data)
        bt_res = solve_timetable_backtracking(G, days=days, periods=periods)
        opt_res = optimize_timetable(bt_res['timetable_entries'], raw_data)
        return opt_res['optimized_timetable']
    except Exception:
        try:
            G = build_conflict_graph(raw_data)
            bt_res = solve_timetable_backtracking(G, days=days, periods=periods)
            return bt_res['timetable_entries']
        except Exception:
            G = build_conflict_graph(raw_data)
            gr_res = greedy_graph_coloring(G, days=days, periods=periods)
            return gr_res['timetable_entries']


@app.route('/simulation')
def show_simulation():
    raw_data, _ = load_dataset()
    timetable_entries = get_best_timetable(raw_data)
    subjects = [s['name'] for s in raw_data.get('subjects', [])]
    days = raw_data.get('days', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    periods = raw_data.get('periods', ["P1", "P2", "P3", "P4", "P5", "P6"])

    subject_slots = {}
    for entry in timetable_entries:
        subject_slots[entry['subject']] = f"{entry.get('day')} {entry.get('period')}"

    history = get_simulation_history()

    return render_template(
        'simulation.html',
        subjects=subjects,
        days=days,
        periods=periods,
        subject_slots=subject_slots,
        history=history,
        timetable=raw_data
    )


@app.route('/api/simulate', methods=['POST'])
def api_simulate():
    data = request.get_json(silent=True) or {}
    subject = data.get('subject')
    target_slot = data.get('target_slot')

    if not subject:
        return jsonify({"error": "Subject name is required"}), 400
    if not target_slot:
        return jsonify({"error": "Target slot is required"}), 400

    raw_data, _ = load_dataset()
    timetable_entries = get_best_timetable(raw_data)

    result, status_code = simulate_move(subject, target_slot, timetable_entries, raw_data)
    
    if status_code == 200 and isinstance(result, dict):
        result['history'] = get_simulation_history()

    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(debug=True)

