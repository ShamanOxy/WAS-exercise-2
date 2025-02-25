# Exercise 2: Automated Planning

**Web-based Autonomous Systems, FS2026** — University of St.Gallen

See the [Exercise Sheet](EXERCISE.md) for the full task descriptions, instructions, and grading.

## Quick Start

**Option A — GitHub Codespaces** (recommended): Click the green **Code** button on the repository page, select the **Codespaces** tab, and click **Create codespace on main**. Everything is pre-configured.

**Option B — Local**: Requires [Python](https://www.python.org/) >= 3.7. Run the planner from the `task-2/` directory:

```
python3 plan.py -s bfs examples/blocks-world-domain.pddl examples/blocks-world-problem.pddl
```

## Repository Structure

```
├── EXERCISE.md                  # exercise sheet with all task descriptions
├── task-1/                      # Task 1: PDDL domain and problem definitions
│   ├── task-1-1/                #   Task 1.1: domain.pddl + problem.pddl
│   └── task-1-2/                #   Task 1.2: domain.pddl + problem.pddl
├── task-2/                      # Task 2: STRIPS-like planner implementation
│   ├── task.py                  #   (TODO) Operator and Task classes
│   ├── search/a_star.py         #   (TODO) A* search algorithm
│   ├── plan.py                  #   main script for running the planner
│   └── ...                      #   parser, heuristics, other search algorithms
├── task-3/                      # Task 3: Sussman Anomaly analysis
│   ├── t3-domain.pddl           #   domain
│   ├── t3-problem.pddl          #   problem
│   ├── t3-solution.soln         #   reference solution
│   └── REPORT.md                #   (TODO) your report
├── .devcontainer/               # Dev Container / Codespaces configuration
└── .vscode/                     # pre-configured launch configurations
```
