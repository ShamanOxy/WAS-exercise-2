# Task 3: Sussman Anomaly Analysis

## 1. What is the anomaly that occurs when solving the problem in the domain?

The Sussman Anomaly occurs when the planner first moves to `room1` (appearing to make progress toward the goal of cleaning it), but then must leave `room1` to go to `storage1` to get the hoover, and then return to `room1` to actually clean it. This creates an inefficient plan where progress toward one goal (being at room1) is temporarily undone to achieve a prerequisite (getting the hoover), then re-achieved.

The solution shows this pattern: `(move reception1 room1)` → `(move room1 storage1)` → `(gethoover storage1)` → `(move storage1 room1)` → `(cleanroom room1)`. The worker visits room1 twice, demonstrating the backtracking behavior characteristic of the anomaly.

## 2. Under what circumstances does generally the anomaly occur in classical STRIPS planning?

The Sussman Anomaly occurs when:
- Multiple goals or subgoals are interdependent
- Achieving one goal requires temporarily undoing progress made toward another goal
- The planner uses a goal-stacking approach that doesn't recognize these dependencies upfront
- The planner processes goals sequentially without considering that achieving one goal's prerequisites might conflict with another goal's prerequisites

In classical STRIPS planning, this often happens with goal-stacking algorithms that select goals arbitrarily and work on them one at a time, without analyzing the full dependency structure between goals.

## 3. What specifically in the problem and the domain make it susceptible?

The domain makes the problem susceptible because:
- **Action dependencies**: The `cleanRoom` action requires both `(at room1)` AND `(haveHoover)` as preconditions
- **Resource location**: The hoover is located at `storage1`, which is different from `room1`
- **Mutual exclusivity**: The `at` predicate can only hold for one location at a time (moving sets `(at ?y)` and removes `(at ?x)`)
- **Sequential prerequisites**: To clean room1, you must first be at storage1 (to get hoover), then be at room1 (to clean)

The problem instance is susceptible because:
- The worker starts at `reception1`, far from both `room1` (goal location) and `storage1` (hoover location)
- The goal only requires cleaning `room1`, creating a single focused objective that masks the underlying dependency structure
- The planner might initially think "I need to be at room1" and move there, only to discover later that it also needs the hoover from storage1

## 4. Why is the behavior not observable with your planner implementation from Task 2?

The behavior may not be observable with our planner implementation from Task 2 because:

1. **A* search with heuristics**: Our planner uses A* search with heuristic functions that estimate the cost to reach the goal. These heuristics likely consider all goal requirements simultaneously, guiding the search toward states that satisfy multiple prerequisites efficiently.

2. **State-space search**: Unlike goal-stacking planners, our planner explores the entire state space systematically. It evaluates states based on their total estimated cost (g + h), which naturally considers all goal requirements together rather than focusing on one goal at a time.

3. **Heuristic guidance**: The heuristic functions (like `hadd`, `hff`, `hmax`) used in our planner compute estimates based on relaxed planning problems that consider all goal predicates simultaneously. This helps the planner recognize dependencies early and avoid inefficient backtracking.

4. **Optimal search**: A* with an admissible heuristic guarantees finding optimal solutions, which means it will naturally avoid the inefficient backtracking that characterizes the Sussman Anomaly, even if it explores more states initially.

In contrast, goal-stacking planners that process goals sequentially are more prone to the anomaly because they commit to achieving goals one at a time without considering the full dependency structure.
