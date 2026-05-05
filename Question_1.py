# CCS3600 – Assignment 2 | Question 1

import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import os

# ============================================================
# GRAPH
# ============================================================
EDGES = [
    ('A','B',30), ('A','C',24),
    ('B','D',20), ('B','E',27),
    ('C','I',25), ('C','F',19),
    ('D','H',40),
    ('E','F',18), ('E','H',22),
    ('F','J',24),
    ('H','G',17),
    ('I','K',18),
    ('J','L',16),
    ('K','L',18),
    ('G','L',43),
]

GRAPH = {}
for u, v, w in EDGES:
    GRAPH.setdefault(u, []).append((v, w))
    GRAPH.setdefault(v, []).append((u, w))
if 'L' not in GRAPH:
    GRAPH['L'] = []

HEURISTIC = {
    'A':95,'B':105,'C':65,'D':100,
    'E':72,'F':45, 'G':42,'H':70,
    'I':38,'J':15, 'K':17,'L':0
}

START, GOAL = 'A', 'L'

# True shortest path = 83 km (Dijkstra verified)
TRUE_PATH = ['A','C','F','J','L']
TRUE_COST = 83


def path_cost(path):
    total = 0
    for i in range(len(path)-1):
        for n,d in GRAPH[path[i]]:
            if n == path[i+1]:
                total += d; break
    return total


# ============================================================
# ALGORITHM 1 - HILL CLIMBING
# ============================================================
def hill_climbing():
    print("="*62)
    print("  ALGORITHM 1: HILL CLIMBING")
    print("="*62)
    print(f"  Strategy : Pick neighbour with smallest h(n). No backtrack.")
    print(f"  Start={START}  h={HEURISTIC[START]}   Goal={GOAL}\n")
    current = START
    path, visited, order = [START], {START}, [START]
    step = 1
    while current != GOAL:
        successors = sorted([(HEURISTIC[n],n,d) for n,d in GRAPH[current] if n not in visited])
        print(f"  Step {step:2d} | Current: {current}  h={HEURISTIC[current]}")
        if not successors:
            print("  DEAD END\n"); return None, [], float('inf')
        print(f"           Successors (by h): {[(h,n) for h,n,d in successors]}")
        bh,best,_ = successors[0]
        print(f"           Pick: {best}  h={bh}\n")
        current = best
        visited.add(current); path.append(current); order.append(current); step += 1
    cost = path_cost(path)
    print(f"  GOAL REACHED")
    print(f"  Search order : {' -> '.join(order)}")
    print(f"  Path found   : {' -> '.join(path)}")
    print(f"  Total cost   : {cost} km\n")
    return path, order, cost


# ============================================================
# ALGORITHM 2 - BEST FIRST SEARCH
# ============================================================
def best_first_search():
    print("="*62)
    print("  ALGORITHM 2: BEST FIRST SEARCH")
    print("="*62)
    print(f"  Strategy : Expand node with smallest h(n) from open list.")
    print(f"  Start={START}  h={HEURISTIC[START]}   Goal={GOAL}\n")
    open_list = [(HEURISTIC[START], START, [START], 0)]
    visited, order, step = set(), [], 1
    while open_list:
        h, node, path, g = heapq.heappop(open_list)
        if node in visited: continue
        visited.add(node); order.append(node)
        print(f"  Step {step:2d} | Expand: {node}  h={h}  g(actual)={g}")
        if node == GOAL:
            cost = path_cost(path)
            print(f"\n  GOAL REACHED")
            print(f"  Search order : {' -> '.join(order)}")
            print(f"  Path found   : {' -> '.join(path)}")
            print(f"  Total cost   : {cost} km\n")
            return path, order, cost
        added = []
        for n,d in GRAPH[node]:
            if n not in visited:
                heapq.heappush(open_list,(HEURISTIC[n],n,path+[n],g+d))
                added.append(f"{n}(h={HEURISTIC[n]})")
        print(f"           Added: {added}"); step += 1
    return None, [], float('inf')


# ============================================================
# ALGORITHM 3 - A* SEARCH
# ============================================================
def a_star():
    print("="*62)
    print("  ALGORITHM 3: A* SEARCH")
    print("="*62)
    print(f"  Strategy : Expand node with smallest f(n)=g(n)+h(n).")
    print(f"  Start={START}  f(A)=0+{HEURISTIC[START]}={HEURISTIC[START]}   Goal={GOAL}\n")
    open_list = [(HEURISTIC[START], 0, START, [START])]
    visited, order, step = {}, [], 1
    while open_list:
        f, g, node, path = heapq.heappop(open_list)
        if node in visited and visited[node] <= g: continue
        visited[node] = g; order.append(node)
        print(f"  Step {step:2d} | Expand: {node}  f={f}  g={g}  h={HEURISTIC[node]}")
        if node == GOAL:
            cost = path_cost(path)
            print(f"\n  GOAL REACHED")
            print(f"  Search order : {' -> '.join(order)}")
            print(f"  Path found   : {' -> '.join(path)}")
            print(f"  Total cost   : {cost} km\n")
            return path, order, cost
        added = []
        for n,d in GRAPH[node]:
            ng = g+d
            if n not in visited or visited[n] > ng:
                nf = ng+HEURISTIC[n]
                heapq.heappush(open_list,(nf,ng,n,path+[n]))
                added.append(f"{n}(f={nf},g={ng},h={HEURISTIC[n]})")
        print(f"           Added: {added}"); step += 1
    return None, [], float('inf')


# ============================================================
# COMPARISON + JUSTIFICATION
# ============================================================
def print_comparison(hc_r, bfs_r, astar_r):
    results = [("Hill Climbing",hc_r),("Best First Search",bfs_r),("A* Search",astar_r)]
    costs = [r[2] for _,r in results if r[0]]
    min_cost = min(costs) if costs else 0
    print("="*62)
    print("  COMPARISON SUMMARY  (b)")
    print("="*62)
    print(f"  {'Algorithm':<22}  {'Path':<28}  {'Cost':>6}  Optimal")
    print(f"  {'-'*22}  {'-'*28}  {'-'*6}  {'-'*7}")
    for name,(path,order,cost) in results:
        p = ' -> '.join(path) if path else 'FAILED'
        print(f"  {name:<22}  {p:<28}  {cost:>6} km  {'YES' if cost==min_cost else 'NO'}")
    print()
    print("  c) JUSTIFICATION")
    print("  "+"─"*58)
    as_path,_,as_cost = astar_r
    print(f"  A* found path: {' -> '.join(as_path)} = {as_cost} km")
    print(f"  True shortest: {' -> '.join(TRUE_PATH)} = {TRUE_COST} km  (shown in yellow on A* panel)")
    print()
    print("  Why algorithms picked A->C->I->K->L:")
    print("    At A: B(h=105) vs C(h=65)  -> all pick C (lower h)")
    print("    At C: F(h=45)  vs I(h=38)  -> all pick I (lower h)")
    print("    At I: only K(h=17)          -> pick K")
    print("    At K: only L(h=0)           -> GOAL")
    print()
    print("  Note: True shortest A->C->F->J->L=83km was missed because")
    print("  heuristic h(C)=65 > true remaining cost 59km (inadmissible).")
    print("  A* still finds optimal among explored paths.")
    print("="*62)


# ============================================================
# NODE POSITIONS
# ============================================================
NODE_POS = {
    'A': (5.0, 9.5),  'B': (2.0, 7.5),  'C': (7.5, 8.2),
    'D': (1.0, 5.0),  'E': (4.2, 6.5),  'F': (6.8, 6.2),
    'G': (5.5, 3.2),  'H': (3.5, 4.0),  'I': (9.8, 7.5),
    'J': (8.5, 4.8),  'K': (11.2, 6.2), 'L': (10.5, 3.0),
}

# ============================================================
# COLOURS BACKGROUND
# ============================================================
BG        = '#0D1B2A'
PANEL_BG  = '#1A2E42'
EDGE_GREY = '#4A7FAA'
NODE_GREY = '#2E5070'
NODE_VIS  = '#3A6898'


# ============================================================
# DRAW ONE PANEL
# ============================================================
def draw_panel(ax, path, order, cost, title, path_color, show_true=False):
    G = nx.Graph()
    for u, v, w in EDGES:
        G.add_edge(u, v, weight=w)

    # Build edge sets
    path_edges = set()
    for i in range(len(path)-1):
        path_edges.add((path[i], path[i+1]))
        path_edges.add((path[i+1], path[i]))

    true_edges = set()
    for i in range(len(TRUE_PATH)-1):
        true_edges.add((TRUE_PATH[i], TRUE_PATH[i+1]))
        true_edges.add((TRUE_PATH[i+1], TRUE_PATH[i]))

    if show_true:
        # A* panel: ALL edges grey, only yellow true path on top
        plain_edges  = [(u,v) for u,v in G.edges()]
        algo_edges   = []
        yellow_edges = [(u,v) for u,v in G.edges()
                        if (u,v) in true_edges or (v,u) in true_edges]
    else:
        # HC and BFS panels: grey + colored algorithm path
        plain_edges  = [(u,v) for u,v in G.edges()
                        if (u,v) not in path_edges and (v,u) not in path_edges]
        algo_edges   = [(u,v) for u,v in G.edges()
                        if (u,v) in path_edges or (v,u) in path_edges]
        yellow_edges = []

    # ── Node colours ──────────────────────────────────────
    node_colors, node_sizes = [], []
    for n in G.nodes():
        if n == START:
            node_colors.append('#F4A500'); node_sizes.append(1600)   # gold = start
        elif n == GOAL:
            node_colors.append('#E03040'); node_sizes.append(1600)   # red  = goal
        elif show_true and n in TRUE_PATH:
            node_colors.append('#F4A500'); node_sizes.append(1300)   # gold = yellow path nodes
        elif not show_true and n in path:
            node_colors.append(path_color); node_sizes.append(1300)  # algorithm color
        elif n in order:
            node_colors.append(NODE_VIS); node_sizes.append(1050)
        else:
            node_colors.append(NODE_GREY); node_sizes.append(900)

    # ── Draw layers ───────────────────────────────────────
    # 1. Plain grey edges (all background roads)
    nx.draw_networkx_edges(G, NODE_POS, ax=ax,
                           edgelist=plain_edges,
                           edge_color=EDGE_GREY, width=2.2)

    # 2. Yellow true shortest (A* panel only)
    if yellow_edges:
        nx.draw_networkx_edges(G, NODE_POS, ax=ax,
                               edgelist=yellow_edges,
                               edge_color='#E8A800', width=9.0)

    # 3. Algorithm colored path (HC and BFS)
    if algo_edges:
        nx.draw_networkx_edges(G, NODE_POS, ax=ax,
                               edgelist=algo_edges,
                               edge_color=path_color, width=6.0)

    # 4. Nodes
    nx.draw_networkx_nodes(G, NODE_POS, ax=ax,
                           node_color=node_colors,
                           node_size=node_sizes,
                           edgecolors='#1A2A3A', linewidths=2.0)

    # 5. Node letters - dark so readable on light background
    nx.draw_networkx_labels(G, NODE_POS, ax=ax,
                            font_size=13, font_weight='bold',
                            font_color='white')

    # 6. Edge distance numbers - dark red, bold, white box behind them
    nx.draw_networkx_edge_labels(G, NODE_POS, ax=ax,
                                 edge_labels={(u,v): w for u,v,w in EDGES},
                                 font_size=10, font_color='#FFE000',
                                 font_weight='bold',
                                 label_pos=0.5,
                                 bbox=dict(facecolor='#0D1B2A',
                                           edgecolor='none',
                                           boxstyle='round,pad=0.2',
                                           linewidth=0,
                                           alpha=0.85))

    # 7. h(n) labels under each node - dark blue text
    for n,(x,y) in NODE_POS.items():
        ax.text(x, y-0.68, f"h={HEURISTIC[n]}",
                ha='center', va='top', fontsize=8,
                color='#00DDFF', fontweight='bold',
                bbox=dict(facecolor='#0D1B2A', edgecolor='none',
                          alpha=0.7, boxstyle='round,pad=0.1'))

    ax.set_facecolor(PANEL_BG)
    ax.axis('off')

    # ── Info box at bottom ────────────────────────────────
    if show_true:

        box_text = (f"Shortest Path : {' -> '.join(TRUE_PATH)}\n"
                    f"Total Cost    : {TRUE_COST} km\n"
                    f"(True optimal path shown in yellow)")
        box_color = '#E8A800'
    else:
        order_str = ' -> '.join(order)
        path_str  = ' -> '.join(path)
        box_text  = (f"Order : {order_str}\n"
                     f"Path  : {path_str}\n"
                     f"Cost  : {cost} km")
        box_color = path_color

    ax.text(0.5, -0.02,
            box_text,
            transform=ax.transAxes, ha='center', va='top',
            fontsize=9, color='white', fontfamily='monospace',
            fontweight='bold',
            bbox=dict(facecolor='#060E18', edgecolor=box_color,
                      boxstyle='round,pad=0.6', linewidth=2.5))

    # ── Panel title ───────────────────────────────────────
    ax.text(0.5, 1.02, title,
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=15, fontweight='bold', color=path_color if not show_true else '#CC8800')

    # Yellow note above A* panel
    if show_true:
        ax.text(0.5, 1.09,
                f"★  Shortest Path: {' -> '.join(TRUE_PATH)} = {TRUE_COST} km",
                transform=ax.transAxes, ha='center', va='bottom',
                fontsize=10, color='#996600', fontweight='bold')


# ============================================================
# VISUALISE - 3 panels side by side
# ============================================================
def visualise(hc_r, bfs_r, astar_r):

    panels = [
        ("Hill Climbing",     hc_r,    '#D93050', False),
        ("Best First Search", bfs_r,   '#1A8840', False),
        ("A* Search",         astar_r, '#CC8800', True),
    ]

    fig = plt.figure(figsize=(32, 18))
    fig.patch.set_facecolor(BG)

    # ── Header ────────────────────────────────────────────
    ax_hdr = fig.add_axes([0.0, 0.92, 1.0, 0.08])
    ax_hdr.set_facecolor('#060E18'); ax_hdr.axis('off')
    ax_hdr.text(0.5, 0.65,
                "CCS3600  —  Artificial Intelligence  —  Assignment 2",
                ha='center', va='center', fontsize=17, fontweight='bold',
                color='white', transform=ax_hdr.transAxes)
    ax_hdr.text(0.5, 0.18,
                "Question 1:  Graph Search  —  Hill Climbing  |  Best First Search  |  A*",
                ha='center', va='center', fontsize=12,
                color='#FFFFFF', transform=ax_hdr.transAxes)

    # ── 3 panels ──────────────────────────────────────────
    for i, (title, (path, order, cost), color, show_true) in enumerate(panels):
        ax = fig.add_axes([0.015 + i*0.328, 0.19, 0.305, 0.70])
        ax.set_facecolor(PANEL_BG)
        for sp in ax.spines.values():
            sp.set_edgecolor(color if not show_true else '#FFB800')
            sp.set_linewidth(4.0)
        draw_panel(ax, path or [], order or [], cost,
                   title, color, show_true=show_true)

    # ── Legend ────────────────────────────────────────────
    ax_leg = fig.add_axes([0.0, 0.0, 1.0, 0.11])
    ax_leg.set_facecolor('#060E18'); ax_leg.axis('off')
    ax_leg.set_visible(True)
    handles = [
        mpatches.Patch(color='#F4A500', label='Start node (A)'),
        mpatches.Patch(color='#E03040', label='Goal node (L)'),
        mpatches.Patch(color='#D93050', label='Hill Climbing path'),
        mpatches.Patch(color='#1A8840', label='Best First Search path'),
        mpatches.Patch(color='#E8A800', label='True Shortest Path 83km (A* panel)'),
        mpatches.Patch(color=NODE_VIS,  label='Explored node'),
        mpatches.Patch(color=NODE_GREY, label='Not visited'),
    ]
    ax_leg.legend(handles=handles, loc='center', ncol=4,
                  fontsize=13, framealpha=0.15, labelcolor='white',
                  facecolor='#060E18', edgecolor='#5599DD',
                  handlelength=2.5, handleheight=1.6,
                  borderpad=1.2, columnspacing=2.5)

    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'q1_graph_search.png')
    plt.savefig(save_path, dpi=180, bbox_inches='tight', facecolor=BG)
    print(f"\n  [Saved: {save_path}]")
    plt.show()


# ============================================================
# RUN EVERYTHING
# ============================================================
if __name__ == "__main__":
    print()
    print("  CCS3600 – Assignment 2 | Question 1")
    print()
    hc_r    = hill_climbing()
    bfs_r   = best_first_search()
    astar_r = a_star()
    print_comparison(hc_r, bfs_r, astar_r)
    print()
    visualise(hc_r, bfs_r, astar_r)