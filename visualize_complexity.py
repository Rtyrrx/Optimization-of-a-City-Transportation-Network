import json
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_results(filename):
    """Load results from JSON file"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['results']

def extract_data(results):
    """Extract data for plotting"""
    graph_ids = []
    vertices = []
    edges = []

    prim_ops = []
    kruskal_ops = []
    prim_time = []
    kruskal_time = []
    total_costs = []

    for result in results:
        graph_ids.append(result['graph_id'])
        vertices.append(result['input_stats']['vertices'])
        edges.append(result['input_stats']['edges'])

        prim_ops.append(result['prim']['operations_count'])
        kruskal_ops.append(result['kruskal']['operations_count'])
        prim_time.append(result['prim']['execution_time_ms'])
        kruskal_time.append(result['kruskal']['execution_time_ms'])
        total_costs.append(result['prim']['total_cost'])

    return {
        'graph_ids': graph_ids,
        'vertices': vertices,
        'edges': edges,
        'prim_ops': prim_ops,
        'kruskal_ops': kruskal_ops,
        'prim_time': prim_time,
        'kruskal_time': kruskal_time,
        'total_costs': total_costs
    }

def plot_operations_vs_vertices(data, output_dir):
    """Plot operations count vs number of vertices"""
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(data['vertices'], data['prim_ops'], 'o-', label='Prim', linewidth=2, markersize=8)
    plt.plot(data['vertices'], data['kruskal_ops'], 's-', label='Kruskal', linewidth=2, markersize=8)
    plt.xlabel('Number of Vertices (V)', fontsize=12)
    plt.ylabel('Operations Count', fontsize=12)
    plt.title('Operations Count vs Vertices', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)

    # Theoretical complexity overlay
    plt.subplot(1, 2, 2)
    v = np.array(data['vertices'])
    e = np.array(data['edges'])

    # Normalize for comparison
    prim_norm = np.array(data['prim_ops']) / max(data['prim_ops'])
    kruskal_norm = np.array(data['kruskal_ops']) / max(data['kruskal_ops'])

    # Theoretical: Prim = O(E log V), Kruskal = O(E log E)
    prim_theoretical = (e * np.log2(v + 1)) / max(e * np.log2(v + 1))
    kruskal_theoretical = (e * np.log2(e + 1)) / max(e * np.log2(e + 1))

    plt.plot(data['vertices'], prim_norm, 'o-', label='Prim (Actual)', linewidth=2, markersize=8)
    plt.plot(data['vertices'], kruskal_norm, 's-', label='Kruskal (Actual)', linewidth=2, markersize=8)
    plt.plot(data['vertices'], prim_theoretical, '--', label='Prim O(E log V)', alpha=0.6, linewidth=2)
    plt.plot(data['vertices'], kruskal_theoretical, '--', label='Kruskal O(E log E)', alpha=0.6, linewidth=2)
    plt.xlabel('Number of Vertices (V)', fontsize=12)
    plt.ylabel('Normalized Operations', fontsize=12)
    plt.title('Actual vs Theoretical Complexity', fontsize=14, fontweight='bold')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/operations_vs_vertices.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/operations_vs_vertices.png")
    plt.close()

def plot_time_vs_vertices(data, output_dir):
    """Plot execution time vs number of vertices"""
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(data['vertices'], data['prim_time'], 'o-', label='Prim', linewidth=2, markersize=8, color='blue')
    plt.plot(data['vertices'], data['kruskal_time'], 's-', label='Kruskal', linewidth=2, markersize=8, color='red')
    plt.xlabel('Number of Vertices (V)', fontsize=12)
    plt.ylabel('Execution Time (ms)', fontsize=12)
    plt.title('Execution Time vs Vertices', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(data['edges'], data['prim_time'], 'o-', label='Prim', linewidth=2, markersize=8, color='blue')
    plt.plot(data['edges'], data['kruskal_time'], 's-', label='Kruskal', linewidth=2, markersize=8, color='red')
    plt.xlabel('Number of Edges (E)', fontsize=12)
    plt.ylabel('Execution Time (ms)', fontsize=12)
    plt.title('Execution Time vs Edges', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/time_vs_vertices.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/time_vs_vertices.png")
    plt.close()

def plot_operations_comparison(data, output_dir):
    """Plot operations comparison between algorithms"""
    plt.figure(figsize=(10, 6))

    x = np.arange(len(data['graph_ids']))
    width = 0.35

    plt.bar(x - width/2, data['prim_ops'], width, label='Prim', alpha=0.8, color='skyblue')
    plt.bar(x + width/2, data['kruskal_ops'], width, label='Kruskal', alpha=0.8, color='lightcoral')

    plt.xlabel('Graph ID', fontsize=12)
    plt.ylabel('Operations Count', fontsize=12)
    plt.title('Operations Count Comparison (Prim vs Kruskal)', fontsize=14, fontweight='bold')
    plt.xticks(x, data['graph_ids'])
    plt.legend(fontsize=11)
    plt.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/operations_comparison.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/operations_comparison.png")
    plt.close()

def plot_time_comparison(data, output_dir):
    """Plot execution time comparison"""
    plt.figure(figsize=(10, 6))

    x = np.arange(len(data['graph_ids']))
    width = 0.35

    plt.bar(x - width/2, data['prim_time'], width, label='Prim', alpha=0.8, color='green')
    plt.bar(x + width/2, data['kruskal_time'], width, label='Kruskal', alpha=0.8, color='orange')

    plt.xlabel('Graph ID', fontsize=12)
    plt.ylabel('Execution Time (ms)', fontsize=12)
    plt.title('Execution Time Comparison (Prim vs Kruskal)', fontsize=14, fontweight='bold')
    plt.xticks(x, data['graph_ids'])
    plt.legend(fontsize=11)
    plt.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/time_comparison.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/time_comparison.png")
    plt.close()

def plot_density_analysis(data, output_dir):
    """Plot performance vs graph density"""
    plt.figure(figsize=(12, 6))

    # Calculate density: E / (V * (V-1) / 2)
    v = np.array(data['vertices'])
    e = np.array(data['edges'])
    max_edges = v * (v - 1) / 2
    density = e / max_edges

    plt.subplot(1, 2, 1)
    plt.scatter(density, data['prim_ops'], s=100, alpha=0.6, label='Prim', c='blue')
    plt.scatter(density, data['kruskal_ops'], s=100, alpha=0.6, label='Kruskal', c='red', marker='s')
    plt.xlabel('Graph Density (E / Max_E)', fontsize=12)
    plt.ylabel('Operations Count', fontsize=12)
    plt.title('Operations vs Graph Density', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.scatter(density, data['prim_time'], s=100, alpha=0.6, label='Prim', c='blue')
    plt.scatter(density, data['kruskal_time'], s=100, alpha=0.6, label='Kruskal', c='red', marker='s')
    plt.xlabel('Graph Density (E / Max_E)', fontsize=12)
    plt.ylabel('Execution Time (ms)', fontsize=12)
    plt.title('Execution Time vs Graph Density', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/density_analysis.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/density_analysis.png")
    plt.close()

def plot_complexity_verification(data, output_dir):
    """Verify complexity with log-log plots"""
    plt.figure(figsize=(14, 6))

    v = np.array(data['vertices'])
    e = np.array(data['edges'])

    # Plot 1: Prim complexity verification
    plt.subplot(1, 3, 1)
    plt.loglog(v, data['prim_ops'], 'o-', label='Prim Operations', linewidth=2, markersize=8)

    # Theoretical lines
    v_range = np.linspace(min(v), max(v), 100)
    e_range = np.linspace(min(e), max(e), 100)
    scale_factor = data['prim_ops'][len(v)//2] / (e[len(e)//2] * np.log2(v[len(v)//2]))
    plt.loglog(v_range, scale_factor * e_range.mean() * np.log2(v_range), '--',
               label='O(E log V)', alpha=0.6, linewidth=2)

    plt.xlabel('Vertices (V) - log scale', fontsize=11)
    plt.ylabel('Operations - log scale', fontsize=11)
    plt.title("Prim's Complexity", fontsize=13, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, which="both")

    # Plot 2: Kruskal complexity verification
    plt.subplot(1, 3, 2)
    plt.loglog(e, data['kruskal_ops'], 's-', label='Kruskal Operations', linewidth=2, markersize=8, color='red')

    scale_factor = data['kruskal_ops'][len(e)//2] / (e[len(e)//2] * np.log2(e[len(e)//2]))
    plt.loglog(e_range, scale_factor * e_range * np.log2(e_range), '--',
               label='O(E log E)', alpha=0.6, linewidth=2, color='darkred')

    plt.xlabel('Edges (E) - log scale', fontsize=11)
    plt.ylabel('Operations - log scale', fontsize=11)
    plt.title("Kruskal's Complexity", fontsize=13, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, which="both")

    # Plot 3: Direct comparison
    plt.subplot(1, 3, 3)
    ratio = np.array(data['kruskal_ops']) / np.array(data['prim_ops'])
    plt.plot(data['vertices'], ratio, 'o-', linewidth=2, markersize=8, color='purple')
    plt.axhline(y=1, color='gray', linestyle='--', alpha=0.5, label='Equal performance')
    plt.xlabel('Number of Vertices (V)', fontsize=11)
    plt.ylabel('Kruskal Ops / Prim Ops', fontsize=11)
    plt.title('Relative Performance', fontsize=13, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/complexity_verification.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/complexity_verification.png")
    plt.close()

def create_summary_table(data, output_dir):
    """Create a summary table as an image"""
    fig, ax = plt.subplots(figsize=(14, len(data['graph_ids']) * 0.5 + 1))
    ax.axis('tight')
    ax.axis('off')

    headers = ['Graph\nID', 'Vertices\n(V)', 'Edges\n(E)', 'Density',
               'Prim\nOps', 'Kruskal\nOps', 'Prim\nTime (ms)',
               'Kruskal\nTime (ms)', 'MST\nCost', 'Winner\n(Time)']

    table_data = []
    for i in range(len(data['graph_ids'])):
        v = data['vertices'][i]
        e = data['edges'][i]
        density = e / (v * (v - 1) / 2) if v > 1 else 0
        winner = 'Prim' if data['prim_time'][i] <= data['kruskal_time'][i] else 'Kruskal'

        row = [
            data['graph_ids'][i],
            v,
            e,
            f'{density:.3f}',
            data['prim_ops'][i],
            data['kruskal_ops'][i],
            f"{data['prim_time'][i]:.2f}",
            f"{data['kruskal_time'][i]:.2f}",
            data['total_costs'][i],
            winner
        ]
        table_data.append(row)

    table = ax.table(cellText=table_data, colLabels=headers,
                     cellLoc='center', loc='center',
                     colWidths=[0.08, 0.09, 0.08, 0.09, 0.10, 0.10, 0.11, 0.11, 0.09, 0.10])

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # Color header
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # Alternate row colors
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')

    plt.title('MST Algorithm Performance Summary', fontsize=16, fontweight='bold', pad=20)
    plt.savefig(f'{output_dir}/summary_table.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir}/summary_table.png")
    plt.close()

def main():
    """Main function to generate all visualizations"""
    print("=" * 60)
    print("MST Algorithm Complexity Analysis - Visualization Generator")
    print("=" * 60)

    # Create output directory
    output_dir = 'analysis_plots'
    Path(output_dir).mkdir(exist_ok=True)
    print(f"\nOutput directory: {output_dir}/")

    # Load results
    print("\nLoading results from output.json...")
    results = load_results('output.json')
    data = extract_data(results)
    print(f"Loaded {len(results)} graph results")

    # Generate plots
    print("\nGenerating visualizations...")
    print("-" * 60)

    plot_operations_vs_vertices(data, output_dir)
    plot_time_vs_vertices(data, output_dir)
    plot_operations_comparison(data, output_dir)
    plot_time_comparison(data, output_dir)
    plot_density_analysis(data, output_dir)
    plot_complexity_verification(data, output_dir)
    create_summary_table(data, output_dir)

    print("-" * 60)
    print(f"\n✓ All visualizations generated successfully!")
    print(f"✓ Total plots created: 7")
    print(f"✓ Check the '{output_dir}/' directory for all images")
    print("=" * 60)

if __name__ == '__main__':
    main()
{
  "graphs": [
    {
      "id": 1,
      "name": "Small Graph 1 (Triangle)",
      "nodes": ["A", "B", "C"],
      "edges": [
        {"from": "A", "to": "B", "weight": 1},
        {"from": "B", "to": "C", "weight": 2},
        {"from": "A", "to": "C", "weight": 3}
      ]
    },
    {
      "id": 2,
      "name": "Small Graph 2 (Square)",
      "nodes": ["A", "B", "C", "D"],
      "edges": [
        {"from": "A", "to": "B", "weight": 1},
        {"from": "A", "to": "C", "weight": 4},
        {"from": "B", "to": "C", "weight": 2},
        {"from": "C", "to": "D", "weight": 3},
        {"from": "B", "to": "D", "weight": 5}
      ]
    },
    {
      "id": 3,
      "name": "Small Graph 3 (Pentagon)",
      "nodes": ["A", "B", "C", "D", "E"],
      "edges": [
        {"from": "A", "to": "B", "weight": 4},
        {"from": "A", "to": "C", "weight": 3},
        {"from": "B", "to": "C", "weight": 2},
        {"from": "B", "to": "D", "weight": 5},
        {"from": "C", "to": "D", "weight": 7},
        {"from": "C", "to": "E", "weight": 8},
        {"from": "D", "to": "E", "weight": 6}
      ]
    },
    {
      "id": 4,
      "name": "Small Graph 4 (Hexagon)",
      "nodes": ["A", "B", "C", "D", "E", "F"],
      "edges": [
        {"from": "A", "to": "B", "weight": 2},
        {"from": "A", "to": "F", "weight": 3},
        {"from": "B", "to": "C", "weight": 4},
        {"from": "B", "to": "F", "weight": 6},
        {"from": "C", "to": "D", "weight": 1},
        {"from": "C", "to": "E", "weight": 5},
        {"from": "D", "to": "E", "weight": 7},
        {"from": "E", "to": "F", "weight": 8}
      ]
    },
    {
      "id": 5,
      "name": "Medium Graph 1 (10 vertices)",
      "nodes": ["V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9"],
      "edges": [
        {"from": "V0", "to": "V1", "weight": 4},
        {"from": "V0", "to": "V7", "weight": 8},
        {"from": "V1", "to": "V2", "weight": 8},
        {"from": "V1", "to": "V7", "weight": 11},
        {"from": "V2", "to": "V3", "weight": 7},
        {"from": "V2", "to": "V5", "weight": 4},
        {"from": "V2", "to": "V8", "weight": 2},
        {"from": "V3", "to": "V4", "weight": 9},
        {"from": "V3", "to": "V5", "weight": 14},
        {"from": "V4", "to": "V5", "weight": 10},
        {"from": "V5", "to": "V6", "weight": 2},
        {"from": "V6", "to": "V7", "weight": 1},
        {"from": "V6", "to": "V8", "weight": 6},
        {"from": "V7", "to": "V8", "weight": 7},
        {"from": "V8", "to": "V9", "weight": 3},
        {"from": "V4", "to": "V9", "weight": 5}
      ]
    },
    {
      "id": 6,
      "name": "Medium Graph 2 (12 vertices)",
      "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
      "edges": [
        {"from": "A", "to": "B", "weight": 3},
        {"from": "A", "to": "C", "weight": 5},
        {"from": "B", "to": "C", "weight": 2},
        {"from": "B", "to": "D", "weight": 4},
        {"from": "C", "to": "E", "weight": 6},
        {"from": "D", "to": "E", "weight": 1},
        {"from": "D", "to": "F", "weight": 8},
        {"from": "E", "to": "F", "weight": 7},
        {"from": "E", "to": "G", "weight": 3},
        {"from": "F", "to": "H", "weight": 2},
        {"from": "G", "to": "H", "weight": 5},
        {"from": "G", "to": "I", "weight": 4},
        {"from": "H", "to": "I", "weight": 6},
        {"from": "H", "to": "J", "weight": 1},
        {"from": "I", "to": "K", "weight": 3},
        {"from": "J", "to": "K", "weight": 7},
        {"from": "J", "to": "L", "weight": 2},
        {"from": "K", "to": "L", "weight": 4}
      ]
    },
    {
      "id": 7,
      "name": "Medium Graph 3 (15 vertices)",
      "nodes": ["N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "N10", "N11", "N12", "N13", "N14", "N15"],
      "edges": [
        {"from": "N1", "to": "N2", "weight": 5},
        {"from": "N1", "to": "N3", "weight": 3},
        {"from": "N2", "to": "N4", "weight": 7},
        {"from": "N3", "to": "N4", "weight": 2},
        {"from": "N3", "to": "N5", "weight": 4},
        {"from": "N4", "to": "N6", "weight": 6},
        {"from": "N5", "to": "N6", "weight": 8},
        {"from": "N5", "to": "N7", "weight": 1},
        {"from": "N6", "to": "N8", "weight": 3},
        {"from": "N7", "to": "N8", "weight": 5},
        {"from": "N7", "to": "N9", "weight": 2},
        {"from": "N8", "to": "N10", "weight": 4},
        {"from": "N9", "to": "N10", "weight": 7},
        {"from": "N9", "to": "N11", "weight": 3},
        {"from": "N10", "to": "N12", "weight": 1},
        {"from": "N11", "to": "N12", "weight": 6},
        {"from": "N11", "to": "N13", "weight": 4},
        {"from": "N12", "to": "N14", "weight": 2},
        {"from": "N13", "to": "N14", "weight": 5},
        {"from": "N13", "to": "N15", "weight": 3},
        {"from": "N14", "to": "N15", "weight": 8}
      ]
    },
    {
      "id": 8,
      "name": "Large Dense Graph (20 vertices, high density)",
      "nodes": ["V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9",
                "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19"],
      "edges": [
        {"from": "V0", "to": "V1", "weight": 12},
        {"from": "V0", "to": "V2", "weight": 8},
        {"from": "V0", "to": "V3", "weight": 15},
        {"from": "V1", "to": "V2", "weight": 5},
        {"from": "V1", "to": "V4", "weight": 9},
        {"from": "V2", "to": "V3", "weight": 7},
        {"from": "V2", "to": "V5", "weight": 11},
        {"from": "V3", "to": "V6", "weight": 6},
        {"from": "V4", "to": "V5", "weight": 4},
        {"from": "V4", "to": "V7", "weight": 13},
        {"from": "V5", "to": "V6", "weight": 3},
        {"from": "V5", "to": "V8", "weight": 10},
        {"from": "V6", "to": "V9", "weight": 2},
        {"from": "V7", "to": "V8", "weight": 14},
        {"from": "V7", "to": "V10", "weight": 8},
        {"from": "V8", "to": "V9", "weight": 5},
        {"from": "V8", "to": "V11", "weight": 12},
        {"from": "V9", "to": "V12", "weight": 7},
        {"from": "V10", "to": "V11", "weight": 6},
        {"from": "V10", "to": "V13", "weight": 9},
        {"from": "V11", "to": "V12", "weight": 4},
        {"from": "V11", "to": "V14", "weight": 11},
        {"from": "V12", "to": "V15", "weight": 3},
        {"from": "V13", "to": "V14", "weight": 8},
        {"from": "V13", "to": "V16", "weight": 5},
        {"from": "V14", "to": "V15", "weight": 10},
        {"from": "V14", "to": "V17", "weight": 6},
        {"from": "V15", "to": "V18", "weight": 2},
        {"from": "V16", "to": "V17", "weight": 7},
        {"from": "V16", "to": "V19", "weight": 4},
        {"from": "V17", "to": "V18", "weight": 9},
        {"from": "V18", "to": "V19", "weight": 1},
        {"from": "V0", "to": "V5", "weight": 16},
        {"from": "V1", "to": "V6", "weight": 14},
        {"from": "V3", "to": "V8", "weight": 13},
        {"from": "V4", "to": "V9", "weight": 15},
        {"from": "V7", "to": "V12", "weight": 11},
        {"from": "V10", "to": "V15", "weight": 12}
      ]
    },
    {
      "id": 9,
      "name": "Large Sparse Graph (25 vertices, low density)",
      "nodes": ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5",
                "C1", "C2", "C3", "C4", "C5", "D1", "D2", "D3", "D4", "D5",
                "E1", "E2", "E3", "E4", "E5"],
      "edges": [
        {"from": "A1", "to": "A2", "weight": 3},
        {"from": "A2", "to": "A3", "weight": 5},
        {"from": "A3", "to": "A4", "weight": 2},
        {"from": "A4", "to": "A5", "weight": 7},
        {"from": "A5", "to": "B1", "weight": 4},
        {"from": "B1", "to": "B2", "weight": 6},
        {"from": "B2", "to": "B3", "weight": 1},
        {"from": "B3", "to": "B4", "weight": 8},
        {"from": "B4", "to": "B5", "weight": 3},
        {"from": "B5", "to": "C1", "weight": 5},
        {"from": "C1", "to": "C2", "weight": 2},
        {"from": "C2", "to": "C3", "weight": 6},
        {"from": "C3", "to": "C4", "weight": 4},
        {"from": "C4", "to": "C5", "weight": 7},
        {"from": "C5", "to": "D1", "weight": 1},
        {"from": "D1", "to": "D2", "weight": 9},
        {"from": "D2", "to": "D3", "weight": 3},
        {"from": "D3", "to": "D4", "weight": 5},
        {"from": "D4", "to": "D5", "weight": 2},
        {"from": "D5", "to": "E1", "weight": 8},
        {"from": "E1", "to": "E2", "weight": 4},
        {"from": "E2", "to": "E3", "weight": 6},
        {"from": "E3", "to": "E4", "weight": 1},
        {"from": "E4", "to": "E5", "weight": 7},
        {"from": "A1", "to": "B1", "weight": 10},
        {"from": "B1", "to": "C1", "weight": 11},
        {"from": "C1", "to": "D1", "weight": 9},
        {"from": "D1", "to": "E1", "weight": 12}
      ]
    },
    {
      "id": 10,
      "name": "Very Large Graph (30 vertices)",
      "nodes": ["V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9",
                "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19",
                "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "V29"],
      "edges": [
        {"from": "V0", "to": "V1", "weight": 7},
        {"from": "V1", "to": "V2", "weight": 4},
        {"from": "V2", "to": "V3", "weight": 9},
        {"from": "V3", "to": "V4", "weight": 2},
        {"from": "V4", "to": "V5", "weight": 11},
        {"from": "V5", "to": "V6", "weight": 5},
        {"from": "V6", "to": "V7", "weight": 8},
        {"from": "V7", "to": "V8", "weight": 3},
        {"from": "V8", "to": "V9", "weight": 6},
        {"from": "V9", "to": "V10", "weight": 12},
        {"from": "V10", "to": "V11", "weight": 1},
        {"from": "V11", "to": "V12", "weight": 10},
        {"from": "V12", "to": "V13", "weight": 4},
        {"from": "V13", "to": "V14", "weight": 7},
        {"from": "V14", "to": "V15", "weight": 2},
        {"from": "V15", "to": "V16", "weight": 9},
        {"from": "V16", "to": "V17", "weight": 5},
        {"from": "V17", "to": "V18", "weight": 3},
        {"from": "V18", "to": "V19", "weight": 8},
        {"from": "V19", "to": "V20", "weight": 6},
        {"from": "V20", "to": "V21", "weight": 1},
        {"from": "V21", "to": "V22", "weight": 11},
        {"from": "V22", "to": "V23", "weight": 4},
        {"from": "V23", "to": "V24", "weight": 7},
        {"from": "V24", "to": "V25", "weight": 2},
        {"from": "V25", "to": "V26", "weight": 9},
        {"from": "V26", "to": "V27", "weight": 5},
        {"from": "V27", "to": "V28", "weight": 3},
        {"from": "V28", "to": "V29", "weight": 8},
        {"from": "V0", "to": "V5", "weight": 15},
        {"from": "V5", "to": "V10", "weight": 13},
        {"from": "V10", "to": "V15", "weight": 14},
        {"from": "V15", "to": "V20", "weight": 12},
        {"from": "V20", "to": "V25", "weight": 16},
        {"from": "V1", "to": "V6", "weight": 10},
        {"from": "V6", "to": "V11", "weight": 11},
        {"from": "V11", "to": "V16", "weight": 9},
        {"from": "V16", "to": "V21", "weight": 13},
        {"from": "V21", "to": "V26", "weight": 8},
        {"from": "V2", "to": "V7", "weight": 14},
        {"from": "V7", "to": "V12", "weight": 12},
        {"from": "V12", "to": "V17", "weight": 15},
        {"from": "V17", "to": "V22", "weight": 10},
        {"from": "V22", "to": "V27", "weight": 11},
        {"from": "V3", "to": "V8", "weight": 9},
        {"from": "V8", "to": "V13", "weight": 13},
        {"from": "V13", "to": "V18", "weight": 8},
        {"from": "V18", "to": "V23", "weight": 14},
        {"from": "V23", "to": "V28", "weight": 7}
      ]
    }
  ]
}

