"""
Conflict Graph Generator
Uses NetworkX to build a graph where nodes represent classes/subjects
and edges represent resource conflicts (Same Teacher, Same Division, Same Room).
"""
import os
import networkx as nx

# Configure Matplotlib backend for headless web server rendering
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def find_teacher_for_subject(subject_name, teachers):
    """Finds assigned teacher name for a subject."""
    for t in teachers:
        if subject_name in t.get('subjects', []):
            return t.get('name', 'Unassigned')
    return 'Unassigned'


def get_default_room_for_subject(subject_obj):
    """Assigns room based on subject type and requirements."""
    sub_name = subject_obj.get('name', '')
    is_lab = subject_obj.get('requires_lab', False) or subject_obj.get('type') == 'Practical'

    if is_lab:
        return 'Lab 1'

    # Room assignments for theory subjects
    room_map = {
        "Design and Analysis of Algorithms": "Room 101",
        "Database Management Systems": "Room 102",
        "Operating Systems": "Room 103",
        "Computer Networks": "Room 101",
        "Artificial Intelligence": "Room 102",
        "Machine Learning": "Lab 1",
        "Software Engineering": "Room 103",
        "Mathematics": "Room 101"
    }
    return room_map.get(sub_name, "Room 101")


def build_conflict_graph(timetable_data):
    """
    Builds a NetworkX conflict graph from timetable JSON dataset.

    Nodes: Classes / Subjects
    Edges: Conflicts between classes that cannot occur at the same time.
    """
    G = nx.Graph()

    division = timetable_data.get('division', 'TY-C')
    subjects = timetable_data.get('subjects', [])
    teachers = timetable_data.get('teachers', [])

    # Step 1: Add nodes (prefer timetable_entries if present)
    entries = timetable_data.get('timetable_entries', [])
    if entries:
        for entry in entries:
            node_id = entry.get('id', entry.get('subject'))
            sub_name = entry.get('subject')
            teacher_name = entry.get('teacher', 'Unassigned')
            room_name = entry.get('room', 'Room 101')
            div_name = entry.get('division', division)
            c_type = entry.get('class_type', 'Theory')
            req_lab = (c_type == 'Practical') or entry.get('requires_lab', False)

            G.add_node(
                node_id,
                subject=sub_name,
                teacher=teacher_name,
                division=div_name,
                room=room_name,
                class_type=c_type,
                requires_lab=req_lab
            )
    else:
        for sub in subjects:
            node_id = sub.get('id', sub.get('name'))
            teacher_name = find_teacher_for_subject(sub.get('name'), teachers)
            room_name = get_default_room_for_subject(sub)

            G.add_node(
                node_id,
                subject=sub.get('name'),
                teacher=teacher_name,
                division=division,
                room=room_name,
                class_type=sub.get('type', 'Theory'),
                requires_lab=sub.get('requires_lab', False)
            )


    # Step 2: Add edges for conflicts
    node_ids = list(G.nodes())
    num_nodes = len(node_ids)

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            u = node_ids[i]
            v = node_ids[j]

            u_attr = G.nodes[u]
            v_attr = G.nodes[v]

            reasons = []

            # Conflict Rule A: Same Teacher
            if u_attr['teacher'] == v_attr['teacher'] and u_attr['teacher'] != 'Unassigned':
                reasons.append("Same Teacher")

            # Conflict Rule B: Same Division
            if u_attr['division'] == v_attr['division']:
                reasons.append("Same Division")

            # Conflict Rule C: Same Room
            if u_attr['room'] == v_attr['room']:
                reasons.append("Same Room")

            # Add edge if any conflict exists
            if reasons:
                G.add_edge(u, v, reasons=reasons)

    return G


def get_graph_statistics(G):
    """Calculates graph metrics and lists of nodes and conflicts."""
    total_nodes = G.number_of_nodes()
    total_edges = G.number_of_edges()

    degrees = [deg for _, deg in G.degree()]
    max_degree = max(degrees) if degrees else 0
    avg_degree = round(sum(degrees) / total_nodes, 2) if total_nodes > 0 else 0.0

    # Node summary list
    node_list = []
    for node_id, data in G.nodes(data=True):
        node_list.append({
            "id": node_id,
            "subject": data['subject'],
            "teacher": data['teacher'],
            "division": data['division'],
            "room": data['room'],
            "class_type": data['class_type'],
            "degree": G.degree(node_id)
        })

    # Conflicts summary list
    conflicts_list = []
    for u, v, data in G.edges(data=True):
        u_data = G.nodes[u]
        v_data = G.nodes[v]
        reasons = data.get('reasons', [])
        conflicts_list.append({
            "class1": u_data['subject'],
            "class2": v_data['subject'],
            "class1_id": u,
            "class2_id": v,
            "reasons": reasons,
            "reasons_str": ", ".join(reasons)
        })

    return {
        "total_nodes": total_nodes,
        "total_edges": total_edges,
        "max_degree": max_degree,
        "avg_degree": avg_degree,
        "nodes": node_list,
        "conflicts": conflicts_list
    }


def generate_graph_image(G, output_path):
    """Generates and saves a visual PNG image of the NetworkX conflict graph."""
    plt.figure(figsize=(10, 7), dpi=150)

    # Layout for nodes
    pos = nx.spring_layout(G, seed=42, k=1.2)

    # Node colors based on Class Type
    node_colors = []
    for node in G.nodes():
        if G.nodes[node].get('class_type') == 'Practical':
            node_colors.append('#f59e0b')  # Amber for practical/lab
        else:
            node_colors.append('#6366f1')  # Indigo for theory

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        node_size=2200,
        alpha=0.9
    )

    # Draw edges
    nx.draw_networkx_edges(
        G, pos,
        edge_color='#94a3b8',
        width=1.8,
        alpha=0.7
    )

    # Short label generator for node titles
    labels = {n: G.nodes[n]['subject'] for n in G.nodes()}
    nx.draw_networkx_labels(
        G, pos,
        labels=labels,
        font_size=8,
        font_weight='bold',
        font_color='white',
        font_family='sans-serif'
    )

    plt.title("Timetable Conflict Graph (NetworkX)", fontsize=14, fontweight='bold', pad=15)
    plt.axis('off')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save figure
    plt.savefig(output_path, bbox_inches='tight', facecolor='white')
    plt.close()
