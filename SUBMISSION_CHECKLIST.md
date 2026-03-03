# Submission Checklist for Exercise 2

## What to Submit

According to EXERCISE.md, you need to submit:

### ✅ Task 1: PDDL Domain and Problem Files
- **Location**: `task-1/task-1-1/` and `task-1/task-1-2/`
- **Files needed**:
  - `task-1/task-1-1/domain.pddl` ✅
  - `task-1/task-1-1/problem.pddl` ✅
  - `task-1/task-1-2/domain.pddl` ✅
  - `task-1/task-1-2/problem.pddl` ✅

### ✅ Task 2: Planner Implementation
- **Location**: `task-2/`
- **Files modified**:
  - `task-2/task.py` ✅ (4 methods implemented)
  - `task-2/search/a_star.py` ✅ (A* algorithm implemented)
- **Note**: The entire `task-2/` folder will be included (excluding benchmarks)

### ✅ Task 3: Sussman Anomaly Report
- **Location**: `task-3/`
- **File needed**:
  - `task-3/REPORT.md` ✅

---

## How to Submit

### Option 1: Use Submission Script (Recommended)

**For ZIP file:**
```bash
cd /Users/eva03/Documents/WebAutonomous/WAS-exercise-2
python3 scripts/submit_zip.py
```

**For PDF file:**
```bash
python3 scripts/submit_pdf.py
```

The scripts will:
1. Commit all your changes to git
2. Push to GitHub (if remote is configured)
3. Create a ZIP or PDF file ready for Canvas upload

### Option 2: Manual Submission

Create a ZIP file containing:
- `task-1/` folder (with all PDDL files)
- `task-2/` folder (with your code)
- `task-3/` folder (with REPORT.md)
- `EXERCISE.md` and `README.md`

---

## Verification Before Submission

### ✅ Task 1 Files Check
- [x] `task-1/task-1-1/domain.pddl` exists
- [x] `task-1/task-1-1/problem.pddl` exists
- [x] `task-1/task-1-2/domain.pddl` exists
- [x] `task-1/task-1-2/problem.pddl` exists

### ✅ Task 2 Code Check
- [x] `task-2/task.py` - all 4 methods implemented:
  - [x] `applicable()` - uses `issubset()`
  - [x] `apply()` - removes del_effects, adds add_effects
  - [x] `goal_reached()` - uses `issubset()`
  - [x] `get_successor_states()` - returns list of (op, state) pairs
- [x] `task-2/search/a_star.py` - A* algorithm implemented:
  - [x] Pops from heap correctly
  - [x] Checks goal reached
  - [x] Expands neighbors
  - [x] Handles duplicate detection

### ✅ Task 3 Report Check
- [x] `task-3/REPORT.md` exists
- [x] Answers all 4 questions:
  - [x] What is the anomaly?
  - [x] When does it occur?
  - [x] What makes it susceptible?
  - [x] Why not observable with your planner?

### ✅ Testing Check
- [x] Task 2 works with Blocks World example
- [x] Task 1.1 PDDL files work with planner
- [x] Task 1.2 PDDL files work with planner

---

## Important Notes

1. **AI Assistance Declaration**: According to EXERCISE.md, you must declare if you used generative AI tools (like GPT, Claude). Since you used AI assistance, you should include a note about this in your submission.

2. **Deadline**: March 3, 2026; 23:59 CET

3. **Format**: PDF (recommended) or ZIP file

4. **What NOT to include**: 
   - `__pycache__/` folders
   - `.pyc` files
   - `benchmarks/` folder (excluded automatically)

---

## Quick Test Before Submission

Run these commands to verify everything works:

```bash
# Test Task 2
cd task-2
python3 plan.py -s astar examples/blocks-world-domain.pddl examples/blocks-world-problem.pddl

# Test Task 1.1
python3 plan.py -s astar ../task-1/task-1-1/domain.pddl ../task-1/task-1-1/problem.pddl

# Test Task 1.2
python3 plan.py -s astar ../task-1/task-1-2/domain.pddl ../task-1/task-1-2/problem.pddl
```

All should produce valid plans!

---

## Final Steps

1. ✅ Review all files one more time
2. ✅ Run the submission script: `python3 scripts/submit_zip.py`
3. ✅ Upload the generated ZIP/PDF to Canvas
4. ✅ Include AI assistance declaration if required

Good luck! 🎉
