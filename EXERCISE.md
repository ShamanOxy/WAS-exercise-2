# Exercise 2: Automated Planning (10pt)

**Web-based Autonomous Systems, FS2026**
University of St.Gallen — Institute of Computer Science
Jan Grau, Alessandro Giugno, Andrei Ciortea

**Deadline: March 3, 2026; 23:59 CET**

---

In this exercise, you will gain experience with how agents can reason about action through classical planning. You will:

1. use the Planning Domain Definition Language (PDDL) 1.2 to model a planning domain of interest;
2. implement parts of a STRIPS-like automated planner;
3. apply your planner to your PDDL model to reason about action in the domain of interest;
4. explore how your planner addresses some of the limitations of a classical STRIPS planner.

---

## Task 1 (5 points): PDDL-based Scheduling and Planning

Consider this problem:

Many *inhabitants* move into a newly constructed building that has 10 *rooms*. The inhabitants are starting to arrive today and it is known in advance which *room* each inhabitant will occupy (e.g. `room1`), and at which *time* an inhabitant can arrive. An inhabitant may arrive at one or more specific times within the day (e.g. at 9 a.m. and 10 a.m.). When an inhabitant arrives, a *maintenance worker* needs to *set up* the inhabitant to their room by showing them to the room.

### Task 1.1 (2 points): Define the PDDL Domain and Problem

Your first task is to model the presented planning domain in PDDL and to create an instance of a planning problem in the domain. Before you start, consider the following questions: What aspects are part of the *planning domain*? What aspects are part of a *planning problem* in that domain?

In this task, you can consider that for setting up an inhabitant only the action `showRoom` is required, e.g.: `<showRoom am9 inhabitant1 room1>`, where `showRoom` would be the ground action applied to the instances `am9`, `inhabitant1`, and `room1`. The maintenance worker should schedule the appointments such that (i) they do not overlap with each other, and (ii) all inhabitants are set up by the end of the day. For example, if `inhabitant1` can arrive at 9 a.m. and at 9:15 a.m. to be set up in `room1`, and `inhabitant2` can arrive at 9 a.m. to be set up in `room2`, the maintenance worker should schedule the appointment with `inhabitant1` at 9:15 a.m. and the appointment with `inhabitant2` at 9 a.m. If both inhabitants can only arrive only at 9 a.m., the problem cannot be solved.

Define the PDDL domain and problem, so that the maintenance worker schedules the appointments with all the inhabitants. Consult the [documentation of PDDL 1.2](https://planning.wiki/ref/pddl) to define the domain and problem, and then solve the problem in the domain.

The [task1-1 folder](task-1/task-1-1/) is pre-filled with the example domain and problem files discussed at the beginning of the lecture. Those files are not relevant, but allow you to test whether your current setup works for running PDDL code. You can edit those files or create new ones in the same folder.

**To test your PDDL domain and problem**, you can use one of the following options:

- **VS Code** (Codespaces / Dev Containers): The included [PDDL extension](https://marketplace.visualstudio.com/items?itemName=jan-dolejsi.pddl) provides syntax highlighting, validation, and a built-in online planner. To run the planner:
  1. Open your **problem** file (e.g. `problem.pddl`).
  2. If the extension asks you to select the corresponding domain file, select your `domain.pddl` in the same folder. The extension should auto-detect it in subsequent runs.
  3. Press `Alt+P` (Windows/Linux) or `Option+P` (Mac), or open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run `PDDL: Run the planner and display the plan`.
  4. If prompted to select a planner, you will see a list of available online planners. These all run locally via the installed PDDL built-in planner.  Recommended choices for this exercise:

     | Planner | Description |
     |---|---|
     | **BFWS -- FF-parser version** | Best First Width Search with FF parser. Good default choice for PDDL 1.2 domains. |
     | **LAMA-first** | Finds solutions quickly without optimizing for plan cost. Fast and reliable. |
     | **BFWS: Best-First Width Search** | Alternative BFWS variant combining goal-oriented and width-based search. |
     | **ENHSP** | Supports classical and numeric planning (PDDL 2.1). Use if your domain has numeric fluents. |
     | **FI -- diverse agile planner** | Produces diverse sets of plans — useful for exploring different solutions. |
     | **Metric Fast-Forward 2.0** | Extension of FF planner for numeric state variables and axioms. |
     | **OPTIC** | For problems with preferences and time-dependent costs. |
     | **Temporal Fast Downward** | For temporal planning with durative actions. |
     | **VAL** | Not a planner — validates and analyzes plans. Use for checking plan correctness. |

     For Task 1 (PDDL 1.2 without numeric/temporal features), **BFWS -- FF-parser version** or **LAMA-first** are recommended.

  5. The plan output will appear in the editor.
- **Online**: Use the [Planning.Domains](http://editor.planning.domains/) online editor — paste your domain and problem PDDL, then click **Solve** (select the BFWS — FF-parser version planner). Also use this editor if the built-in planner does not work (do not spend time troubleshooting the built-in planner, as it is not the focus of this exercise).

> **Note on VAL tools**: The PDDL extension may show a warning about missing VAL tools (PDDL parser/validator). VAL provides detailed syntax checking and is automatically installed in **GitHub Codespaces** (x86_64). On **Apple Silicon Macs** (ARM64), VAL is not available — you can safely dismiss this warning and just test your code directly or use the online planner.

### Task 1.2 (3 points): Extend the PDDL Domain

Apart from resolving the scheduling presented in Task 1.1, now the maintenance worker needs also to plan their series of actions for setting up an inhabitant to a room: For setting up the inhabitant, the maintenance worker needs to `be at` the correct room at the time of the appointment. Additionally, for entering the room, the maintenance worker needs to first `unlock` the room. As a result, it is expected that for setting up an inhabitant, three sequential actions are required (e.g., `<unlock am9 room1>`, `<join am9 room1>`, `<showRoom am9 inhabitant1 room1>`).

Extend the PDDL domain so that the maintenance worker schedules all the appointments and plans the actions needed for each appointment.

---

## Task 2 (4 points): Working with a State-space Planner

In this task, you will complete a STRIPS-like planner and apply it to solve planning problems in the domain defined in Task 1. To help you focus on the central aspects of the planner, we provide you with an almost complete implementation of the planner in the [`task-2/`](task-2/) folder of this repository. The implementation is based on the [pyperplan](https://github.com/aibasel/pyperplan/) planner.

To complete this implementation, we want you to focus on two aspects of the planner: (1) the internal representation of planning tasks and operators (these are the abstractions that adopt the STRIPS representation), and (2) the A* search algorithm used by the planner for solving tasks.

### Project Structure

```
task-2/
├── plan.py              # main script for solving a planning problem
├── planner.py           # a STRIPS-like planner
├── task.py              # (TODO) Operator and Task classes — STRIPS representation
├── grounding.py         # grounding a schematic PDDL task to a STRIPS planning task
├── tools.py             # utility functions
├── pddl/                # a PDDL parser
├── search/
│   ├── a_star.py        # (TODO) A* search algorithm
│   ├── searchspace.py   # SearchNode class for nodes visited during search
│   ├── breadth_first_search.py
│   └── ...              # other search algorithms (wastar, gbf, bfs, ehs, ids, sat)
├── heuristics/          # heuristic methods (blind, landmark, lmcut, hadd, hff, hmax, hsa)
├── examples/            # "Blocks World" domain and problem for testing
└── benchmarks/          # IPC benchmark problems for further testing
```

### How to Run the Planner

The project requires [Python](https://www.python.org/) >= 3.7. You can run the planner either from the **terminal** or using the **pre-configured launch configurations** (if you are using GitHub Codespaces or VS Code Dev Containers — see [Development Environment](#development-environment-optional)).

**From the terminal**, run the script `plan.py` from the `task-2/` directory:

```
python3 plan.py [-s {astar,wastar,gbf,bfs,ehs,ids,sat}] [domain] problem
```

For example, to run with the breadth-first algorithm:
```
python3 plan.py -s bfs examples/blocks-world-domain.pddl examples/blocks-world-problem.pddl
```

Or to run with the A* algorithm that you implemented:
```
python3 plan.py -s astar ../task-1/task-1-1/domain.pddl ../task-1/task-1-1/problem.pddl
```

**From VS Code** (Codespaces / Dev Containers), open the **Run & Debug** panel (`Ctrl+Shift+D` / `Cmd+Shift+D`) and select one of the pre-configured launch configurations. These let you run and debug the planner with a single click, with breakpoints and step-through support.

### Task 2.1: Complete `task.py`

Complete the implementation of [`task.py`](task-2/task.py), which includes classes for creating Operators and STRIPS-like instances ⟨Propositional arguments, Operators, Initial state, Goals⟩:

- Implement the methods `applicable()` and `apply()` of the `Operator` class
- Implement the methods `goal_reached()` and `get_successor_states()` of the `Task` class

**Tips:**
- Study the class `Operator` in [`task.py`](task-2/task.py) to see how the planner should handle the removal and addition of predicates
- Use [Python Frozenset](https://www.programiz.com/python-programming/methods/built-in/frozenset)
- Run your planner implementation with a search algorithm other than A\* (e.g. `bfs`) until you implement Task 2.2
- If you didn't manage to complete Task 1, run your planner implementation with the provided [Blocks World domain and problem](task-2/examples/)

### Task 2.2: Complete `a_star.py`

Complete the implementation of [`a_star.py`](task-2/search/a_star.py), which includes the A\* search algorithm:

- Implement the method `astar_search()`

**Tips:**
- Study the class `Task` in [`task.py`](task-2/task.py) to see how the search algorithm should handle STRIPS-like planning tasks
- Study the class `SearchNode` in [`searchspace.py`](task-2/search/searchspace.py) to see how the search algorithm should handle the nodes of the search space
- Use the [heapq module](https://pythontic.com/algorithms/heapq/introduction) for handling heaps in Python
- For an easy-to-follow introduction to the A\* algorithm, we recommend this [online article](https://www.redblobgames.com/pathfinding/a-star/introduction.html)

> **Attention**: The planner does not support the negation of conditions in PDDL. Therefore, you cannot use it to test your PDDL domain and problem from Task 1. Instead, you can test it on the provided [Blocks World example](task-2/examples/).

**Note**: This exercise template is based on an open-source implementation of a STRIPS-like planner and we made no efforts to obfuscate the connection to this implementation. It is therefore not surprising that you *could* simply copy the code from that implementation. However, we ask you to implement the omitted aspects of the planner yourselves instead.

---

## Task 3 (1 point): Exploring the Sussman Anomaly

In this task, you will study a planning domain and problem susceptible to Sussman Anomaly. The problem requires for a maintenance worker to plan their actions towards cleaning a room.

Examine the following files and the behavior of the planner when solving the problem in the domain:

- [`t3-domain.pddl`](task-3/t3-domain.pddl) — the domain
- [`t3-problem.pddl`](task-3/t3-problem.pddl) — the problem
- [`t3-solution.soln`](task-3/t3-solution.soln) — a solution generated with a classical STRIPS planner

Then reply to the following questions in a [short report](task-3/REPORT.md) (max. 2 pages of text, the more concise the better):

1. What is the anomaly that occurs when solving the problem in the domain?
2. Under what circumstances does generally the anomaly occur in classical STRIPS planning?
3. What specifically in the problem and the domain make it susceptible?
4. Why is the behavior not observable with your planner implementation from Task 2?

**Note**: We strongly encourage you not to use LLMs to answer these questions. The purpose of the reflection questions is to help you engage with the concepts.

---

## Development Environment (Optional)

This repository includes a [Dev Container](https://containers.dev/) configuration, which you can use with **GitHub Codespaces** or **VS Code Dev Containers** to get a ready-to-use development environment. The setup includes:

- Python 3.12 with all required dependencies
- Pre-configured **Run & Debug** launch configurations (accessible via the Run & Debug panel or `Ctrl+Shift+D` / `Cmd+Shift+D`):

| Config | Description |
|---|---|
| **Task 2.1: BFS — Blocks World Example** | Test your `task.py` implementation with BFS on the provided example |
| **Task 2.1: BFS — Task 1.1 Domain** | Test your `task.py` implementation with BFS on your Task 1.1 PDDL |
| **Task 2.1: BFS — Task 1.2 Domain** | Test your `task.py` implementation with BFS on your Task 1.2 PDDL |
| **Task 2.2: A\* — Blocks World Example** | Test your `a_star.py` implementation on the provided example |
| **Task 2.2: A\* — Task 1.1 Domain** | Test your `a_star.py` implementation on your Task 1.1 PDDL |
| **Task 2.2: A\* — Task 1.2 Domain** | Test your `a_star.py` implementation on your Task 1.2 PDDL |
| **Task 3: BFS — Sussman Anomaly** | Run the Sussman Anomaly problem with BFS |
| **Task 3: A\* — Sussman Anomaly** | Run the Sussman Anomaly problem with A* |
| **Custom: Pick Search + Files** | Choose your own search algorithm and PDDL files |

To get started with Codespaces: click the green **Code** button on the repository page, select the **Codespaces** tab, and click **Create codespace on main**.

---

## Hand-in Instructions

By the deadline, hand in your work by uploading a **PDF** (recommended) or **ZIP** of your submission to **Canvas**. Place your files in the corresponding folders:

1. your **PDDL documents for Task 1** in `task-1/task-1-1/` and `task-1/task-1-2/`;
2. your **code for Task 2** in `task-2/`;
3. your **report for Task 3** in `task-3/`.

To generate the submission file, you can use one of the provided helper scripts:

**From VS Code** (Codespaces / Dev Containers): Open the **Run & Debug** panel and select:
- **Submit: PDF for Canvas** (recommended) — generates an HTML file and opens it in your browser for printing to PDF
- **Submit: ZIP for Canvas** — generates `submission-exercise-2.zip`

**From the terminal**:
```
python3 scripts/submit_pdf.py
```
or:
```
python3 scripts/submit_zip.py
```

The scripts will automatically commit and push your changes to GitHub before generating the submission file.

You can also create the submission file manually. A ZIP file should contain the entire repository folder. A PDF should contain at least the link to your GitHub repository.

---

Across all tasks, in this and the other assignments in this course, you are required to declare any support that you received from others and, within reasonable bounds, any support tools that you were using while solving the assignment. It is not required that you declare that you were using a text-editing software with orthographic correction; it is however required to declare if you were using any non-standard tools such as generative machine learning models (e.g., GPT, Claude).