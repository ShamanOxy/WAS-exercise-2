# Complete Walkthrough: Understanding the Exercise Solutions

This document explains **what** was implemented, **why** it works, and **how** to think about each concept.

---

## Part 1: Understanding STRIPS Planning

### What is STRIPS?

**STRIPS** (Stanford Research Institute Problem Solver) is a planning formalism where:
- **State** = Set of true facts/predicates (e.g., `{on(A, B), clear(C)}`)
- **Action** = Operator that changes state (has preconditions, add effects, delete effects)
- **Goal** = Set of facts that must be true
- **Plan** = Sequence of actions to get from initial state to goal state

### Key Concept: State Transitions

```
Initial State → [Action 1] → State 2 → [Action 2] → State 3 → ... → Goal State
```

Each action:
1. Checks if preconditions are met (all must be true)
2. Removes delete effects (makes them false)
3. Adds add effects (makes them true)

---

## Part 2: Task 2.1 - Implementing STRIPS Operations (`task.py`)

### Method 1: `applicable(state)` - Can we use this action?

```python
def applicable(self, state):
    return self.preconditions.issubset(state)
```

**What it does:**
- Checks if ALL preconditions are present in the current state
- Returns `True` if we can apply this operator, `False` otherwise

**Example:**
```python
# Operator: pick-up block A
# Preconditions: {clear(A), ontable(A), handempty}
# Current state: {clear(A), ontable(A), handempty, on(B, C)}
# → Returns True (all preconditions present)

# Current state: {clear(A), ontable(A)}  # missing handempty
# → Returns False (can't pick up without free hand)
```

**Why `issubset()`?**
- We need ALL preconditions to be true
- `{a, b}.issubset({a, b, c})` = True (all of {a,b} are in {a,b,c})
- This is exactly what we need!

---

### Method 2: `apply(state)` - Execute the action

```python
def apply(self, state):
    new_state = state - self.del_effects  # Remove what becomes false
    new_state = new_state | self.add_effects  # Add what becomes true
    return new_state
```

**What it does:**
1. Start with current state
2. Remove delete effects (things that become false)
3. Add add effects (things that become true)
4. Return the new state

**Example:**
```python
# Operator: pick-up block A
# Preconditions: {clear(A), ontable(A), handempty}
# Add effects: {holding(A)}
# Delete effects: {ontable(A), clear(A), handempty}

# Current state: {clear(A), ontable(A), handempty, on(B, C)}
# Step 1: Remove delete effects → {on(B, C)}  # removed clear(A), ontable(A), handempty
# Step 2: Add add effects → {on(B, C), holding(A)}
# Result: {on(B, C), holding(A)}
```

**Why this order?**
- If something is both deleted and added, adding comes last, so it ends up true
- This handles edge cases correctly

---

### Method 3: `goal_reached(state)` - Are we done?

```python
def goal_reached(self, state):
    return self.goals.issubset(state)
```

**What it does:**
- Checks if ALL goal predicates are true in the current state
- Returns `True` if we've reached the goal

**Example:**
```python
# Goals: {on(A, B), on(B, C)}
# Current state: {on(A, B), on(B, C), clear(A)}
# → Returns True (all goals present)

# Current state: {on(A, B)}  # missing on(B, C)
# → Returns False (not all goals achieved)
```

---

### Method 4: `get_successor_states(state)` - What can we do next?

```python
def get_successor_states(self, state):
    successors = []
    for op in self.operators:
        if op.applicable(state):
            new_state = op.apply(state)
            successors.append((op, new_state))
    return successors
```

**What it does:**
1. Loop through all possible operators
2. For each operator that's applicable:
   - Apply it to get the new state
   - Add (operator, new_state) pair to results
3. Return all possible next states

**Example:**
```python
# Current state: {clear(A), ontable(A), handempty}
# Operators:
#   - pick-up(A): applicable → new_state = {holding(A)}
#   - pick-up(B): NOT applicable (B not clear or not on table)
#   - stack(A, B): NOT applicable (not holding A)
# Result: [(pick-up(A), {holding(A)})]
```

**Why return pairs?**
- We need both the operator (for the plan) and the new state (for search)
- The planner uses operators to build the final plan

---

## Part 3: Task 2.2 - A* Search Algorithm (`a_star.py`)

### What is A* Search?

**A*** is a graph search algorithm that finds optimal paths by:
- Using **g(n)** = actual cost from start to node n
- Using **h(n)** = estimated cost from node n to goal (heuristic)
- Evaluating nodes by **f(n) = g(n) + h(n)**
- Always expanding the node with lowest f(n) first

**Key insight:** If h(n) never overestimates (admissible), A* finds optimal solutions!

### The A* Algorithm Step-by-Step

#### Step 1: Initialize

```python
root = searchspace.make_root_node(task.initial_state)
state_cost = {task.initial_state: 0}  # Track best cost to reach each state
open = []  # Priority queue (heap) of nodes to explore
heuristic(root)  # Calculate h for initial state
heapq.heappush(open, make_open_entry(root, init_h, node_tiebreaker))
```

**What's happening:**
- Create root node (initial state, g=0, no parent)
- Track that we can reach initial state with cost 0
- Add root to priority queue

---

#### Step 2: Main Loop - Pop Best Node

```python
while open:
    (f, h, _tie, pop_node) = heapq.heappop(open)
    pop_state = pop_node.state
    pop_g = pop_node.g
```

**What's happening:**
- `heappop` gets the node with lowest f-value (most promising)
- Extract the state and actual cost g from the node

**Why a heap?**
- Heap keeps nodes sorted by f-value
- Always get the best node in O(log n) time

---

#### Step 3: Check if Worth Expanding

```python
if pop_g == state_cost.get(pop_state, float('inf')):
    # Only expand if this is still the cheapest path to this state
```

**Why this check?**
- We might have added a node to the queue
- Then found a cheaper path to the same state later
- If so, skip this node (it's outdated)

**Example:**
```
State S reached via path A with cost 5 → added to queue
State S reached via path B with cost 3 → cheaper! Update state_cost[S] = 3
When we pop the old node (cost 5), skip it because 5 != 3
```

---

#### Step 4: Check for Goal

```python
if task.goal_reached(pop_state):
    return pop_node.extract_solution()
```

**What's happening:**
- If current state satisfies all goals, we're done!
- Extract the plan by following parent pointers back to root

---

#### Step 5: Expand Neighbors

```python
for operator, successor_state in task.get_successor_states(pop_state):
    neighbor_node = searchspace.make_child_node(pop_node, operator, successor_state)
    neighbor_h = heuristic(neighbor_node)
    
    if neighbor_h == float('inf'):
        continue  # Can't reach goal from here
    
    neighbor_g = neighbor_node.g
    best_cost = state_cost.get(successor_state, float('inf'))
    
    if neighbor_g < best_cost:  # Found cheaper path!
        state_cost[successor_state] = neighbor_g
        heapq.heappush(open, make_open_entry(neighbor_node, neighbor_h, node_tiebreaker))
```

**What's happening:**
1. Get all possible next states (using `get_successor_states`)
2. For each successor:
   - Create a node (with parent pointer, g = parent.g + 1)
   - Calculate heuristic h
   - If h = infinity, skip (dead end)
   - Check if this is a cheaper path to this state
   - If yes, update best cost and add to queue

**Why check `neighbor_g < best_cost`?**
- We only want to explore states if we found a better path
- Avoids re-exploring states unnecessarily

---

### Visual Example of A* Search

```
Initial State (g=0, h=6, f=6)
    ↓
Expand → Get neighbors:
  - State A (g=1, h=5, f=6)
  - State B (g=1, h=4, f=5) ← Best! Expand this next
  
State B (g=1, h=4, f=5)
    ↓
Expand → Get neighbors:
  - State C (g=2, h=3, f=5)
  - State D (g=2, h=2, f=4) ← Best! Expand this next
  
State D (g=2, h=2, f=4)
    ↓
Expand → Get neighbors:
  - Goal State (g=3, h=0, f=3) ← Found it!
```

---

## Part 4: Task 1 - PDDL Domain Modeling

### What is PDDL?

**PDDL** (Planning Domain Definition Language) is a language for describing:
- **Domain**: Actions, predicates, types (the "rules of the game")
- **Problem**: Objects, initial state, goals (a specific instance)

### Task 1.1: Basic Scheduling Domain

#### Domain Structure

```pddl
(define (domain maintenance-scheduling)
  (:requirements :strips :typing)
  
  (:types inhabitant room time)
  
  (:predicates
    (can-arrive ?i - inhabitant ?t - time)
    (assigned-room ?i - inhabitant ?r - room)
    (scheduled ?i - inhabitant)
    (worker-available ?t - time)
  )
```

**What each part means:**
- **Types**: Categories of objects (inhabitant, room, time)
- **Predicates**: Facts that can be true/false
  - `can-arrive(i, t)`: Inhabitant i can arrive at time t
  - `assigned-room(i, r)`: Inhabitant i is assigned to room r
  - `scheduled(i)`: Inhabitant i has been scheduled
  - `worker-available(t)`: Worker is free at time t

#### Action Definition

```pddl
(:action showRoom
  :parameters (?i - inhabitant ?r - room ?t - time)
  :precondition (and
    (can-arrive ?i ?t)
    (assigned-room ?i ?r)
    (worker-available ?t)
  )
  :effect (and
    (scheduled ?i)
    (not (worker-available ?t))
  )
)
```

**Breaking it down:**
- **Parameters**: Variables that get instantiated (grounded) with specific objects
- **Precondition**: ALL must be true to execute:
  - Inhabitant can arrive at this time
  - Inhabitant is assigned to this room
  - Worker is available at this time
- **Effect**: What changes:
  - Inhabitant becomes scheduled
  - Worker becomes unavailable at this time (prevents double-booking!)

#### Problem Instance

```pddl
(define (problem scheduling-problem)
  (:domain maintenance-scheduling)
  
  (:objects
    inhabitant1 inhabitant2 inhabitant3 - inhabitant
    room1 room2 room3 - room
    am9 am915 am10 am1015 am11 - time
  )
  
  (:init
    (assigned-room inhabitant1 room1)
    (can-arrive inhabitant1 am9)
    (can-arrive inhabitant1 am915)
    (worker-available am9)
    ; ... more facts
  )
  
  (:goal (and
    (scheduled inhabitant1)
    (scheduled inhabitant2)
    (scheduled inhabitant3)
  ))
)
```

**What happens:**
1. **Grounding**: PDDL parser creates all possible action instances:
   - `showRoom(inhabitant1, room1, am9)`
   - `showRoom(inhabitant1, room1, am915)`
   - `showRoom(inhabitant2, room2, am9)`
   - etc.

2. **Planning**: Planner finds sequence that:
   - Schedules all inhabitants
   - Doesn't double-book worker (can't use same time twice)

---

### Task 1.2: Extended Domain with Sequential Actions

```pddl
(:action unlock
  :parameters (?r - room ?t - time)
  :precondition (worker-available ?t)
  :effect (unlocked ?r ?t)
)

(:action join
  :parameters (?r - room ?t - time)
  :precondition (and
    (unlocked ?r ?t)
    (worker-available ?t)
  )
  :effect (at-room ?r ?t)
)

(:action showRoom
  :parameters (?i - inhabitant ?r - room ?t - time)
  :precondition (and
    (can-arrive ?i ?t)
    (assigned-room ?i ?r)
    (at-room ?r ?t)  ← Now requires being at room!
    (worker-available ?t)
  )
  :effect (and
    (scheduled ?i)
    (not (worker-available ?t))
  )
)
```

**Key insight:** Actions create dependencies!
- To `showRoom`, you need `at-room`
- To `join`, you need `unlocked`
- Planner automatically finds the sequence: `unlock → join → showRoom`

---

## Part 5: Key Concepts Summary

### 1. State Space Search

Planning is searching through a graph:
- **Nodes** = States (sets of facts)
- **Edges** = Actions (operators)
- **Start** = Initial state
- **Goal** = Any state satisfying goal conditions

### 2. Why A* Works Well

- **Informed search**: Uses heuristics to guide exploration
- **Optimal**: Finds shortest plan (if heuristic is admissible)
- **Efficient**: Expands fewer nodes than blind search

### 3. Why PDDL is Powerful

- **Declarative**: Describe WHAT you want, not HOW to get it
- **Reusable**: Same domain can solve many problems
- **Automatic**: Planner handles search, you just model the problem

### 4. Common Patterns

**Mutual exclusion** (can't do two things at once):
```pddl
:effect (and
  (not (worker-available ?t))  ; Worker becomes busy
)
```

**Sequential dependencies** (must do A before B):
```pddl
:precondition (unlocked ?r ?t)  ; Must unlock first
```

**Resource constraints** (limited availability):
```pddl
:precondition (worker-available ?t)  ; Check availability
:effect (not (worker-available ?t))  ; Consume resource
```

---

## Part 6: How to Think About Planning Problems

### Step 1: Identify Components
- What are the **objects**? (inhabitants, rooms, times)
- What are the **states**? (scheduled, available, at location)
- What are the **actions**? (schedule, move, unlock)

### Step 2: Model Preconditions
- What must be true BEFORE an action?
- Think: "What do I need to have/be/do?"

### Step 3: Model Effects
- What CHANGES after the action?
- What becomes true? What becomes false?

### Step 4: Define Goals
- What must be true at the end?
- Keep it simple and declarative

### Step 5: Test and Refine
- Run planner, see if it works
- If not, check: Are preconditions too strict? Too loose?
- Are effects correct? Missing constraints?

---

## Part 7: Debugging Tips

### If planner finds no solution:
1. Check preconditions - might be too strict
2. Check initial state - are all needed facts present?
3. Check goals - are they achievable?

### If planner finds suboptimal solution:
1. Check heuristic - might not be admissible
2. Check action costs - might need to add costs

### If planner is slow:
1. Check domain size - too many objects = many grounded actions
2. Check heuristic quality - bad heuristic = more exploration

---

## Conclusion

You've learned:
1. **STRIPS representation**: States as sets, actions as state transformers
2. **A* search**: Optimal pathfinding with heuristics
3. **PDDL modeling**: Declarative problem description
4. **Planning concepts**: State space, actions, goals, search

The key insight: **Planning is search through possible futures**, and good modeling + good search = efficient solutions!
