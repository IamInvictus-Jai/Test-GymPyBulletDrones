# 🚁 EDITH Drone Environment - START HERE

## What You Have

A complete test suite to verify **gym-pybullet-drones** works in headless mode and determine the best implementation approach for your hackathon project.

## Quick Start (3 Steps)

### 1. Install (5 minutes)
```bash
cd "Drone RL Environment"
chmod +x setup.sh
./setup.sh
```

### 2. Run Tests (10 minutes)
```bash
python3 run_all_tests.py
```

### 3. Check Results
- Look at the terminal output
- Check `test_camera_output.png` (if test 04 ran)
- Follow the decision tree below

## The Critical Decision

**Test 04 determines your implementation path:**

```
test_04_camera_headless.py
    │
    ├─ ✓ PASS → Use vision-based scan_area (OpenCV)
    │
    └─ ✗ FAIL → Use raycast-based scan_area (p.rayTestBatch)
                 THIS IS NOT A FAILURE
```

## Files You Need

### To Get Started
1. **[QUICKSTART.md](QUICKSTART.md)** ← Read this first (5 min)
2. **[INSTALL.md](INSTALL.md)** ← If setup fails, read this

### During Testing
3. **[TEST_FLOW.txt](TEST_FLOW.txt)** ← Visual test flow diagram
4. **[TEST_PLAN.md](TEST_PLAN.md)** ← Detailed test plan

### During Hackathon
5. **[HACKATHON_CHECKLIST.md](HACKATHON_CHECKLIST.md)** ← Full 24-hour checklist
6. **[README_SUMMARY.md](README_SUMMARY.md)** ← Complete overview

## What Happens Next

### If All Tests Pass ✓
```
You're ready to build!

Next steps:
1. Implement vision-based scan_area (OpenCV color masking)
2. Build remaining 7 tool functions
3. Create Task 1 environment (Navigate & Reach)
4. Test with random agent
5. Proceed to Tasks 2 and 3

Time to completion: ~18 hours remaining
```

### If Camera Fails, Others Pass ✓
```
You're still ready to build!

Next steps:
1. Implement raycast-based scan_area (p.rayTestBatch)
2. Build remaining 7 tool functions
3. Create Task 1 environment (Navigate & Reach)
4. Test with random agent
5. Proceed to Tasks 2 and 3

Time to completion: ~18 hours remaining
Note: Raycast is actually FASTER than vision
```

### If Early Tests Fail ✗
```
Fix installation first!

Actions:
1. Read INSTALL.md troubleshooting section
2. Verify Python 3.10 installed
3. Verify gym-pybullet-drones on 'main' branch
4. Re-run tests

Do not proceed until tests 01-03 pass
```

## Time Budget

| Phase | Time | Status |
|-------|------|--------|
| Setup & Tests | 1 hour | ← YOU ARE HERE |
| Core Environment | 6 hours | Next |
| Task 1 | 6 hours | Next |
| Task 2 (optional) | 4 hours | Later |
| Task 3 (optional) | 4 hours | Later |
| Integration & Demo | 6 hours | Final |

## Key Insight

**Both vision and raycast approaches are valid for the hackathon.**

The camera test doesn't determine project success—it determines implementation approach. Judges care about the LLM's reasoning capability, not the sensing modality.

- **Vision-based:** More realistic, slower, requires tuning
- **Raycast-based:** Faster, more reliable, simpler

Both lead to a strong submission.

## Commands Reference

```bash
# Setup
./setup.sh                          # Linux/macOS
setup.bat                           # Windows

# Run all tests
python3 run_all_tests.py

# Run individual tests
python3 test_01_imports.py
python3 test_02_headless_basic.py
python3 test_03_headless_env.py
python3 test_04_camera_headless.py  # CRITICAL

# Check camera output
open test_camera_output.png         # macOS
xdg-open test_camera_output.png     # Linux
```

## Help & Support

- **Quick questions:** [QUICKSTART.md](QUICKSTART.md)
- **Installation issues:** [INSTALL.md](INSTALL.md)
- **Test details:** [TEST_PLAN.md](TEST_PLAN.md)
- **Hackathon planning:** [HACKATHON_CHECKLIST.md](HACKATHON_CHECKLIST.md)
- **Troubleshooting:** `Docs/Drone/GPD test.md` Section 15

## What's in This Directory

```
Drone RL Environment/
├── START_HERE.md              ← You are here
├── QUICKSTART.md              ← Read this next
├── INSTALL.md                 ← Installation guide
├── TEST_PLAN.md               ← Detailed test plan
├── TEST_FLOW.txt              ← Visual diagram
├── HACKATHON_CHECKLIST.md     ← 24-hour checklist
├── README_SUMMARY.md          ← Complete overview
│
├── setup.sh                   ← Linux/macOS setup
├── setup.bat                  ← Windows setup
├── requirements.txt           ← Python dependencies
├── run_all_tests.py           ← Master test runner
│
├── test_01_imports.py         ← Test: Imports
├── test_02_headless_basic.py  ← Test: PyBullet DIRECT
├── test_03_headless_env.py    ← Test: HoverAviary
├── test_04_camera_headless.py ← Test: Camera (CRITICAL)
├── test_05_spawn_control.py   ← Test: Spawn & PID
├── test_06_collision.py       ← Test: Collision
└── test_07_opencv_pipeline.py ← Test: OpenCV
```

## Ready?

1. Read [QUICKSTART.md](QUICKSTART.md) (5 min)
2. Run `./setup.sh` (5 min)
3. Run `python3 run_all_tests.py` (10 min)
4. Follow the decision tree above
5. Start building!

**Good luck with your hackathon!** 🚁

---

*For the full problem statement, see: `Docs/Drone/drone_problem_statement.md`*  
*For GPD documentation, see: `Docs/Drone/GPD test.md`*
