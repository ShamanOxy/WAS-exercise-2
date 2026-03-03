# Task 3: Sussman Anomaly Analysis

## 1. What is the anomaly that occurs when solving the problem in the domain?

The Sussman Anomaly happens when the planner moves to room1 first (thinking it's making progress), but then has to leave room1 to go get the hoover from storage1, and then come back to room1 to clean it. So basically it's backtracking - it makes progress toward one goal (being at room1) but then has to undo that progress to get something else it needs (the hoover), and then redo the progress.

Looking at the solution: `(move reception1 room1)` → `(move room1 storage1)` → `(gethoover storage1)` → `(move storage1 room1)` → `(cleanroom room1)`. The worker goes to room1, leaves it, then comes back. This is inefficient backtracking which is what the anomaly is about.

## 2. Under what circumstances does generally the anomaly occur in classical STRIPS planning?

The anomaly usually happens when:
- You have multiple goals that depend on each other
- To achieve one goal, you have to undo progress on another goal temporarily
- The planner uses goal-stacking and doesn't see the dependencies between goals ahead of time
- Goals are processed one at a time without thinking about how they might conflict

This is common with goal-stacking planners that just pick goals randomly and work on them one by one, without looking at how the goals relate to each other.

## 3. What specifically in the problem and the domain make it susceptible?

The domain is set up in a way that causes the problem:
- The `cleanRoom` action needs both `(at room1)` AND `(haveHoover)` - so you need two things
- The hoover is at `storage1`, not at `room1` where you need to clean
- The `at` predicate can only be true for one place at a time - you can't be in two places
- So to clean room1, you need to: go to storage1 to get hoover, then go to room1 to clean

The specific problem instance makes it worse:
- The worker starts at `reception1`, which is far from both `room1` (where you need to clean) and `storage1` (where the hoover is)
- The goal is just to clean room1, so the planner might think "I'll just go to room1" without realizing it also needs the hoover
- This makes the planner likely to go to room1 first, then realize it needs the hoover and backtrack

## 4. Why is the behavior not observable with your planner implementation from Task 2?

Our planner from Task 2 probably won't show this anomaly because:

1. **A* with heuristics**: We're using A* search which uses heuristics to estimate how far we are from the goal. These heuristics look at all the goal requirements at once, not just one at a time, so they guide the search better.

2. **State-space search**: Our planner explores the whole state space systematically. It looks at states based on g + h (actual cost + estimated cost), which means it considers everything together rather than focusing on one goal.

3. **Heuristic functions**: The heuristics we use (like hff, hadd, hmax) work by solving relaxed versions of the problem that consider all goals at the same time. This helps the planner see dependencies early and avoid backtracking.

4. **Optimal search**: A* with a good heuristic finds optimal solutions, so it naturally avoids the inefficient backtracking that causes the anomaly.

Goal-stacking planners are more likely to have this problem because they work on goals one at a time without seeing how they're connected.
