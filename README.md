# Slitherlink Puzzle Solver (Artificial Intelligence)

> An automated solver and interactive GUI for the **Slitherlink** logic puzzle, implemented in Python using search algorithms, heuristics, and automated test benchmarks.

---

## 📌 Suggested Repository Names
If you are deciding on a clean name for your GitHub repository, here are a few good options:
* `slitherlink-ai-solver` *(Recommended)*
* `slitherlink-search-solver`
* `slitherlink-solver-python`
* `ia-slitherlink`

---

## 📖 Overview

This project was developed for the **Artificial Intelligence** course. It provides an engine to represent, search, and solve **Slitherlink** (also known as *Loop the Loop*) boards of various sizes and difficulty levels.

The project features:
* **Search Algorithms:** State-space exploration and search strategies (`search.py`) tailored for board state constraints.
* **Heuristics & Optimization:** Custom heuristics and rule-based edge reductions (`utils.py`, `slitherlink.py`) to prune search trees efficiently.
* **Graphical Interface (GUI):** A visual board viewer built with Tkinter (`slitherlink_gui.py`).
* **Automated Benchmarks:** Shell scripts (`benchmark.sh`, `run_tests.sh`) to evaluate solver performance across public test boards.

---

## 🗂️ Project Structure

```text
.
├── slitherlink.py            # Core puzzle logic, board state representation, & solver
├── search.py                 # General search framework & algorithms
├── slitherlink_gui.py        # GUI interface for visual interaction
├── utils.py                  # Auxiliary helper functions & utilities
├── benchmark.sh              # Performance benchmark script
├── run_tests.sh              # Test runner script
├── slitherlink-boards-public/ # Directory containing test instances
└── Projeto-2526.pdf          # Project specification document
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.x
* Tkinter (usually included with standard Python installations for GUI support)

### Running the Solver & Tests
To run automated test suites against the public boards:
```bash
bash run_tests.sh
```

To run performance benchmarks:
```bash
bash benchmark.sh
```

### Launching the GUI
To visually inspect and solve boards using the graphical user interface:
```bash
python3 slitherlink_gui.py
```