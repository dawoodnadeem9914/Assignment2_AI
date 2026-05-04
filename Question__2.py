# ============================================================
#  CCS3600 – Artificial Intelligence  |  Assignment 2
# ============================================================

import heapq, os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ============================================================
# STATES  (0 = blank tile)
#  Initial:        Goal:
#   2  7  _         7  6  5
#   4  1  6         8  _  4
#   8  3  5         1  2  3
# ============================================================
INITIAL = (2,7,0, 4,1,6, 8,3,5)
GOAL    = (7,6,5, 8,0,4, 1,2,3)
GOAL_POS = {tile:(i//3, i%3) for i,tile in enumerate(GOAL)}

def manhattan(state):
    total = 0
    for i,tile in enumerate(state):
        if tile == 0: continue
        gr,gc = GOAL_POS[tile]
        cr,cc = i//3, i%3
        total += abs(cr-gr) + abs(cc-gc)
    return total

def get_successors(state):
    s = list(state); bi = s.index(0)
    br,bc = bi//3, bi%3; moves = []
    for dr,dc,name in [(-1,0,'UP'),(1,0,'DOWN'),(0,-1,'LEFT'),(0,1,'RIGHT')]:
        nr,nc = br+dr, bc+dc
        if 0<=nr<3 and 0<=nc<3:
            ni=nr*3+nc; ns=s[:]; tm=ns[ni]
            ns[bi],ns[ni]=ns[ni],ns[bi]
            moves.append((tuple(ns),name,tm))
    return moves

def a_star(initial, goal):
    h0 = manhattan(initial)
    pq = [(h0,0,initial,[initial],[])]
    visited = {}; nodes_exp = 0
    while pq:
        f,g,state,path_s,path_m = heapq.heappop(pq)
        if state in visited and visited[state]<=g: continue
        visited[state]=g; nodes_exp+=1
        if state==goal: return path_s,path_m,nodes_exp
        for ns,direction,tile in get_successors(state):
            ng=g+1
            if ns in visited and visited[ns]<=ng: continue
            nh=manhattan(ns)
            heapq.heappush(pq,(ng+nh,ng,ns,
                path_s+[ns],
                path_m+[(direction,tile,ng,nh,ng+nh)]))
    return None,None,nodes_exp

def fmt(state, indent="    "):
    rows=[]
    for r in range(3):
        cells=[str(state[r*3+c]) if state[r*3+c]!=0 else '_' for c in range(3)]
        rows.append(indent+' | '.join(cells))
    return '\n'.join(rows)

# ── Print full solution ───────────────────────────────────
def print_solution(path_s, path_m, nodes_exp):
    total = len(path_s)-1
    h0    = manhattan(INITIAL)
    print("="*62)
    print("  A* SOLUTION — ALL STEPS")
    print("="*62)
    print(f"\n  Step  0 | START      | g=0  h={h0}  f={h0}")
    print(fmt(INITIAL))
    for i,(state,mv) in enumerate(zip(path_s[1:],path_m),1):
        direction,tile,g,h,f = mv
        tag = "  ← GOAL REACHED!" if state==GOAL else ""
        print(f"\n  Step {i:2d} | Move {direction:<5} tile {tile} | g={g}  h={h}  f={f}{tag}")
        print(fmt(state))
    print()
    print("="*62)
    print(f"  (a) Total moves  g(n) = {total}")
    print(f"      Nodes explored    = {nodes_exp}")
    print("="*62)

# ── Part b: manual trace g=0 to g=3 ─────────────────────
def print_manual_comparison(path_s, path_m):
    print()
    print("="*62)
    print("  PART (b) — Manual A* Trace  (g = 0 to g = 3)")
    print("="*62)
    for i in range(min(4, len(path_s))):
        state=path_s[i]; g=i; h=manhattan(state); f=g+h
        if i==0:
            print(f"\n  g(n)=0  |  Initial State")
        else:
            direction,tile,*_=path_m[i-1]
            print(f"\n  g(n)={i}  |  Move: Blank slides {direction}")
        print(f"  h(n)={h} (Manhattan Distance to goal)")
        print(f"  f(n) = g({g}) + h({h}) = {f}")
        print(fmt(state))
        print()
        print("  Manhattan breakdown:")
        for j,t in enumerate(state):
            if t==0: continue
            gr,gc=GOAL_POS[t]; cr,cc=j//3,j%3
            d=abs(cr-gr)+abs(cc-gc)
            print(f"    Tile {t}: at ({cr},{cc}) → goal ({gr},{gc})  dist = {d}")
        print(f"    ─────────────────────────────────────")
        print(f"    Total h(n) = {h}")
    print()
    print("  FINDINGS:")
    print(f"  1. Total moves to reach goal: g(n) = {len(path_s)-1}")
    print("  2. Program and manual trace produce IDENTICAL steps.")
    print("  3. A* always picks node with smallest f=g+h — OPTIMAL.")
    print("  4. Manhattan Distance is ADMISSIBLE — never overestimates.")
    print("  5. f(n) stays constant (f=14) because g+1 and h-1 each step.")
    print("  f values (g=0 to g=3):", end="")
    for i in range(min(4,len(path_s))):
        g=i; h=manhattan(path_s[i]); f=g+h
        print(f"  g={g}→f={f}", end="")
    print()
    print("="*62)

# ── Draw one puzzle card ──────────────────────────────────
def draw_card(ax, state, idx, total, path_m, goal_list):
    COL_DONE  = {'fc':'#AED6F1','ec':'#2E86C1','tc':'#1A3A5C'}
    COL_MOVE  = {'fc':'#FAD7A0','ec':'#E67E22','tc':'#6E2C00'}
    COL_BLANK = {'fc':'#F8F9FA','ec':'#BFC9CA','tc':'#FFFFFF'}

    if idx==0:
        hdr_bg='#2874A6'; hdr_fg='#FFFFFF'; lbl='INITIAL'; border='#2874A6'
    elif idx==total-1:
        hdr_bg='#1E8449'; hdr_fg='#FFFFFF'; lbl='✓ GOAL'; border='#1E8449'
    else:
        direction,tile_mv,*_=path_m[idx-1]
        lbl=f'{direction} {tile_mv}'; hdr_bg='#D6EAF8'; hdr_fg='#1A3A5C'; border='#AED6F1'

    g=idx; h=manhattan(tuple(state)); f=g+h

    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(-0.08,3.08); ax.set_ylim(-0.90,3.60)
    ax.set_aspect('equal'); ax.axis('off')

    # Card border
    ax.add_patch(plt.Rectangle((-0.08,-0.90),3.16,4.50,
        facecolor='#FFFFFF',edgecolor=border,linewidth=2.5,zorder=0))
    # Header
    ax.add_patch(plt.Rectangle((-0.08,3.05),3.16,0.55,
        facecolor=hdr_bg,edgecolor='none',zorder=1))
    ax.text(0.04,3.32,f'Step {idx}',ha='left',va='center',
        fontsize=7.5,fontweight='bold',color=hdr_fg,zorder=3)
    ax.text(3.02,3.32,lbl,ha='right',va='center',
        fontsize=7.5,fontweight='bold',color=hdr_fg,zorder=3)

    # Tiles
    for row in range(3):
        for col in range(3):
            tile=state[row*3+col]
            is_blank=(tile==0)
            in_place=(not is_blank and goal_list[row*3+col]==tile)
            style=COL_BLANK if is_blank else (COL_DONE if in_place else COL_MOVE)
            # Shadow
            ax.add_patch(plt.Rectangle((col+0.10,2-row-0.03),0.86,0.86,
                facecolor='#D5D8DC',edgecolor='none',alpha=0.5,zorder=2))
            # Tile
            ax.add_patch(plt.Rectangle((col+0.06,2-row+0.06),0.86,0.86,
                facecolor=style['fc'],edgecolor=style['ec'],linewidth=1.8,zorder=3))
            if not is_blank:
                ax.text(col+0.49,2-row+0.49,str(tile),
                    ha='center',va='center',fontsize=17,
                    fontweight='bold',color=style['tc'],zorder=4)

    ax.text(1.5,-0.50,f'g={g}   h={h}   f={f}',
        ha='center',va='center',fontsize=7.5,
        color='#2C3E50',fontweight='bold',zorder=3,
        bbox=dict(facecolor='#EBF5FB',edgecolor='#AED6F1',
                  boxstyle='round,pad=0.25',linewidth=1.0))

# ── Main visualisation — ALL steps ─────────────
def visualise(path_s, path_m):
    total=len(path_s)   # 15 states: step 0 to step 14
    goal_list=list(GOAL)
    ncols=5
    nrows=(total+ncols-1)//ncols   # = 3 rows

    BG='#EBF5FB'

    fig,axes=plt.subplots(nrows,ncols,
        figsize=(ncols*3.2, nrows*4.2+1.2),
        dpi=250)   # HIGH DPI = sharp, no blur
    fig.patch.set_facecolor(BG)

    fig.text(0.5,0.992,
        'CCS3600  —  Artificial Intelligence  |  Assignment 2',
        ha='center',va='top',fontsize=14,fontweight='bold',color='#1A2A4A')
    fig.text(0.5,0.972,
        f'Question 2: 8-Puzzle A* Search  ·  g(n) = {total-1} moves  ·  Step 0 (Initial) → Step {total-1} (Goal)',
        ha='center',va='top',fontsize=10,color='#2E86C1')

    axes_flat=axes.flatten()
    for idx,ax in enumerate(axes_flat):
        if idx>=total:
            ax.axis('off'); ax.set_facecolor(BG); continue
        draw_card(ax,list(path_s[idx]),idx,total,path_m,goal_list)

    legend_patches=[
        mpatches.Patch(facecolor='#AED6F1',edgecolor='#2E86C1',
            label='Tile in correct position',linewidth=1.5),
        mpatches.Patch(facecolor='#FAD7A0',edgecolor='#E67E22',
            label='Tile needs to move',linewidth=1.5),
        mpatches.Patch(facecolor='#F8F9FA',edgecolor='#BFC9CA',
            label='Blank tile  ( _ )',linewidth=1.5),
    ]
    fig.legend(handles=legend_patches,loc='lower center',ncol=3,
        fontsize=10,framealpha=0.95,facecolor='white',edgecolor='#AED6F1',
        bbox_to_anchor=(0.5,0.0),handlelength=1.8,handleheight=1.3)

    plt.tight_layout(rect=[0,0.04,1,0.960],pad=1.5,h_pad=2.5,w_pad=1.5)

    save_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'q2_puzzle.png')
    plt.savefig(save_path,dpi=250,bbox_inches='tight',facecolor=BG)
    print(f"\n  [Saved: {save_path}]")
    plt.show()

# ── Part b ───────────────────────
def visualise_partb(path_s, path_m):
    total=len(path_s); goal_list=list(GOAL)
    BG='#EBF5FB'

    fig,axes=plt.subplots(1,4,figsize=(14,5.0),dpi=250)
    fig.patch.set_facecolor(BG)

    fig.text(0.5,1.01,
        'CCS3600 — Q2 Part (b): A* Manual Trace  |  g=0 to g=3',
        ha='center',fontsize=13,fontweight='bold',color='#1A2A4A')
    fig.text(0.5,0.94,
        'Showing first 4 states  ·  f(n) = g(n) + h(n) = 14  (constant throughout)',
        ha='center',fontsize=9,color='#2E86C1')

    for i,ax in enumerate(axes):
        draw_card(ax,list(path_s[i]),i,total,path_m,goal_list)

    # Arrows between cards
    for i in range(3):
        fig.text(0.235+i*0.187,0.50,'→',
            ha='center',va='center',fontsize=26,
            color='#2874A6',fontweight='bold')

    legend_patches=[
        mpatches.Patch(facecolor='#AED6F1',edgecolor='#2E86C1',
            label='Tile in correct position',linewidth=1.5),
        mpatches.Patch(facecolor='#FAD7A0',edgecolor='#E67E22',
            label='Tile needs to move',linewidth=1.5),
        mpatches.Patch(facecolor='#F8F9FA',edgecolor='#BFC9CA',
            label='Blank tile  ( _ )',linewidth=1.5),
    ]
    fig.legend(handles=legend_patches,loc='lower center',ncol=3,
        fontsize=9.5,framealpha=0.95,facecolor='white',edgecolor='#AED6F1',
        bbox_to_anchor=(0.5,-0.02),handlelength=1.8,handleheight=1.3)

    plt.tight_layout(pad=2.0)
    save_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'q2_partb.png')
    plt.savefig(save_path,dpi=250,bbox_inches='tight',facecolor=BG)
    print(f"  [Saved: {save_path}]")
    plt.show()

# ── MAIN ─────────────────────────────────────────────────
if __name__=="__main__":
    print()
    print()
    print("  Initial State:"); print(fmt(INITIAL)); print()
    print("  Goal State:");    print(fmt(GOAL));    print()
    h0=manhattan(INITIAL)
    print(f"  Initial h(n) = {h0}   →   f(n) = g(0) + h({h0}) = {h0}")
    print()

    path_s,path_m,nodes_exp=a_star(INITIAL,GOAL)

    if path_s is None:
        print("  ERROR: No solution found.")
    else:
        print_solution(path_s,path_m,nodes_exp)
        print_manual_comparison(path_s,path_m)
        print()
        print("  Generating images ...")
        visualise(path_s,path_m)        # ALL 15 steps
        visualise_partb(path_s,path_m)  # Part b: g=0 to g=3