<div align="center">

# 🧠 AI Algorithms in Python

### *Classical AI problem-solving algorithms implemented in Python*

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![AI](https://img.shields.io/badge/Artificial_Intelligence-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](#)
[![Algorithms](https://img.shields.io/badge/Search_Algorithms-00C853?style=for-the-badge)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> Exploring how intelligent agents search, reason, and make decisions — through clean Python implementations of classical AI algorithms.

</div>

---

## 📋 Overview

This repository contains Python implementations of fundamental **Artificial Intelligence algorithms**, developed as part of the AI coursework at **University Putra Malaysia (UPM)**.

The focus is on **state-space search** — the backbone of classical AI — covering uninformed and informed search strategies used by intelligent agents to solve problems.

---

## 🔍 Algorithms Implemented

### Uninformed (Blind) Search

| Algorithm | Description | Completeness | Time |
|---|---|---|---|
| **BFS** (Breadth-First Search) | Explores level by level; finds shortest path | ✅ Complete | O(b^d) |
| **DFS** (Depth-First Search) | Explores deep before wide; memory efficient | ✅ Complete* | O(b^m) |
| **UCS** (Uniform-Cost Search) | Expands lowest-cost node first | ✅ Complete | O(b^(C/ε)) |

### Informed (Heuristic) Search

| Algorithm | Description | Optimality |
|---|---|---|
| **Greedy Best-First** | Uses heuristic only; fast but suboptimal | ❌ |
| **A\* Search** | Combines path cost + heuristic; optimal & efficient | ✅ |

---

## 🔄 How State-Space Search Works

```
Problem Definition
     │
     ▼
  ┌──────────┐
  │  State   │ ◄── Current configuration of the world
  └────┬─────┘
       │ Apply operators (actions)
       ▼
  ┌──────────┐
  │ Frontier │ ◄── States yet to be explored (queue/stack/priority queue)
  └────┬─────┘
       │ Select next state (strategy determines order)
       ▼
  ┌──────────┐
  │  Explore │ ◄── Check if GOAL STATE reached
  └──────────┘
```

---

## 💡 Example: A\* Search

```python
import heapq

def a_star(graph, start, goal, heuristic):
    """
    A* Search Algorithm
    f(n) = g(n) + h(n)
    g(n) = cost from start to n
    h(n) = estimated cost from n to goal (heuristic)
    """
    open_set = []
    heapq.heappush(open_set, (0 + heuristic[start], 0, start, [start]))

    visited = set()

    while open_set:
        f, g, node, path = heapq.heappop(open_set)

        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            print(f"Path found: {' -> '.join(path)}")
            print(f"Total cost: {g}")
            return path

        for neighbour, cost in graph[node].items():
            if neighbour not in visited:
                new_g = g + cost
                new_f = new_g + heuristic[neighbour]
                heapq.heappush(open_set, (new_f, new_g, neighbour, path + [neighbour]))

    return None  # No path found
```

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/dawoodnadeem9914/Assignment2_AI.git
cd Assignment2_AI

# No external dependencies — uses Python standard library only
python3 main.py
```

---

## 🔮 Future Improvements

- [ ] Add visualisation of search paths using `matplotlib`
- [ ] Implement minimax and alpha-beta pruning (game AI)
- [ ] Add constraint satisfaction problems (CSP)
- [ ] Benchmark and compare algorithm performance
- [ ] Add Jupyter Notebook with step-by-step walkthroughs

---

## 👨‍💻 Author

**Dawood Nadeem**  
BSc Computer Science @ University Putra Malaysia (UPM)  
📧 [Captaindawood12@gmail.com](mailto:Captaindawood12@gmail.com)  
🔗 [GitHub](https://github.com/dawoodnadeem9914)

---

<div align="center">

*AI Coursework @ UPM*  
*⭐ Star this repo if it helped you understand AI search!*

</div>
