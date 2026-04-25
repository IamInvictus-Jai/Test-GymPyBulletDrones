# EDITH Drone Environment - Hackathon Checklist

Use this checklist to track progress during the hackathon.

## Phase 0: Setup & Verification (Target: 1 hour)

- [ ] **Install dependencies**
  - [ ] Python 3.10 installed
  - [ ] Conda environment created (optional but recommended)
  - [ ] Run `setup.sh` or `setup.bat`
  - [ ] All packages installed without errors

- [ ] **Run verification tests**
  - [ ] `python3 run_all_tests.py` executed
  - [ ] Test 01 (imports) passed
  - [ ] Test 02 (headless basic) passed
  - [ ] Test 03 (headless env) passed
  - [ ] Test 04 (camera) completed - **DECISION MADE**

- [ ] **Decision: scan_area implementation**
  - [ ] Vision-based (if camera works) OR
  - [ ] Raycast-based (if camera fails)
  - [ ] Decision documented

**STOP:** Do not proceed until all Phase 0 tests pass.

---

## Phase 1: Core Environment (Target: 4-6 hours)

### Scene Setup
- [ ] **Scene assets sourced**
  - [ ] Test scene loaded (pybullet_data builtins)
  - [ ] Obstacles load correctly
  - [ ] Target markers load correctly
  - [ ] Scene randomizer implemented

### Tool Functions (8 total)
- [ ] `get_drone_status(drone_id)` - position, velocity, battery
- [ ] `get_obstacle_distances(drone_id)` - raycast in 6 directions
- [ ] `get_camera_frame(drone_id)` - camera capture (if vision-based)
- [ ] `move_drone_to(drone_id, x, y, z)` - waypoint command
- [ ] `get_mission_status()` - targets, time, drone states
- [ ] `assign_drone_to_target(drone_id, target_id)` - assignment
- [ ] `return_drone_home(drone_id)` - return to spawn
- [ ] `scan_area(drone_id)` - vision OR raycast detection

### Core Mechanics
- [ ] **Battery simulation**
  - [ ] Battery drains based on velocity/acceleration
  - [ ] Battery state accessible via tool
  - [ ] Battery death handled correctly

- [ ] **Collision detection**
  - [ ] Ground collision detected
  - [ ] Obstacle collision detected
  - [ ] Proximity warning (< 0.3m) implemented

- [ ] **Episode loop**
  - [ ] LLM decision → execution → physics timing correct
  - [ ] Moving obstacles update each physics step (if used)
  - [ ] Execution interrupts on proximity warning

---

## Phase 2: Task 1 - Navigate & Reach (Target: 4-6 hours)

- [ ] **Environment wrapper**
  - [ ] OpenEnv MCPEnvironment base class used
  - [ ] `reset()` implemented
  - [ ] `step()` implemented
  - [ ] `state()` implemented
  - [ ] Tool calls registered as MCP tools

- [ ] **Task 1 implementation**
  - [ ] Single drone spawns correctly
  - [ ] Static obstacles randomize each episode
  - [ ] Target position randomizes (3 zones)
  - [ ] Mission brief provided to agent

- [ ] **Reward function**
  - [ ] Mission completion (35%)
  - [ ] Safety (25%)
  - [ ] Efficiency (15%)
  - [ ] Battery management (10%)
  - [ ] Milestone bonuses (10%)
  - [ ] Penalties (format, timeout)
  - [ ] Returns dictionary, not single float
  - [ ] All rewards in [0.0, 1.0]

- [ ] **Testing**
  - [ ] Random agent completes episodes without crash
  - [ ] Reward computed correctly
  - [ ] Episode terminates correctly
  - [ ] Info dict contains failure reasons

---

## Phase 3: Task 2 - Constrained Delivery (Target: 3-4 hours)

- [ ] **Task 2 features**
  - [ ] Battery starts at 70-100% (randomized)
  - [ ] Moving obstacle added (if time permits)
  - [ ] Mid-mission event (battery drain OR new obstacle)
  - [ ] Landing zone marker added

- [ ] **Testing**
  - [ ] Battery pressure forces tradeoffs
  - [ ] Mid-mission event detected by agent
  - [ ] Random agent handles task variants

---

## Phase 4: Task 3 - Two-Drone Coordination (Target: 3-4 hours)

**NOTE:** This is optional. Only implement if Tasks 1 & 2 are solid.

- [ ] **Task 3 features**
  - [ ] Two drones spawn
  - [ ] Battery levels differ (randomized)
  - [ ] One drone degrades mid-mission (speed reduction)
  - [ ] Multiple targets to allocate

- [ ] **Swarm mechanics**
  - [ ] Drone-drone collision detection
  - [ ] Redundancy detection (both assigned to same target)
  - [ ] Both drones must return home

- [ ] **Testing**
  - [ ] Random agent handles two drones
  - [ ] Reward computed correctly for swarm

---

## Phase 5: Integration & Deployment (Target: 2-3 hours)

- [ ] **OpenEnv compliance**
  - [ ] `openenv.yaml` manifest created
  - [ ] Environment name and description
  - [ ] Tool list documented
  - [ ] Reward structure documented

- [ ] **Docker deployment**
  - [ ] Dockerfile created
  - [ ] Environment runs in Docker (headless)
  - [ ] No display server required
  - [ ] Pushed to HuggingFace Space

- [ ] **Training script**
  - [ ] Unsloth or TRL GRPO script created
  - [ ] Curriculum learning implemented
  - [ ] Mastery gates (0.70, 0.65, 0.60)
  - [ ] Failure ceiling (200 attempts)
  - [ ] Script runs in Colab

---

## Phase 6: Evaluation & Demo (Target: 2-3 hours)

- [ ] **Held-out scene**
  - [ ] Fourth scene created (never seen in training)
  - [ ] Same task structure, different layout
  - [ ] Agent tested on held-out scene

- [ ] **Demo materials**
  - [ ] Before/after behavior recorded
  - [ ] Reward curves plotted (per task)
  - [ ] README with results
  - [ ] Mini-blog or video (<2 min)

- [ ] **Submission**
  - [ ] Environment on HuggingFace Space
  - [ ] Training script in Colab
  - [ ] README with all links
  - [ ] Video/blog linked from README

---

## Minimum Viable Submission

If time runs short, ensure you have:

- [x] **Task 1 fully working** (Navigate & Reach)
- [x] **Reward function complete** (all components)
- [x] **OpenEnv compliant** (MCPEnvironment, tools, manifest)
- [x] **Deployed to HuggingFace Space**
- [x] **Training script exists** (even if not fully trained)
- [x] **README with explanation**

This is enough for a strong submission. Tasks 2 and 3 are bonuses.

---

## Time Allocation (24 hours total)

| Phase | Time | Critical? |
|-------|------|-----------|
| 0. Setup & Verification | 1h | YES |
| 1. Core Environment | 6h | YES |
| 2. Task 1 | 6h | YES |
| 3. Task 2 | 4h | NO |
| 4. Task 3 | 4h | NO |
| 5. Integration | 3h | YES |
| 6. Evaluation & Demo | 3h | YES |
| **Buffer** | **-3h** | - |

**Critical path:** Phases 0, 1, 2, 5, 6 = 19 hours  
**Optional:** Phases 3, 4 = 8 hours (cut if needed)

---

## Decision Points

### Hour 1: Camera Test Result
- **Camera works** → Vision-based scan_area
- **Camera fails** → Raycast-based scan_area

### Hour 7: Task 1 Status
- **Task 1 working** → Proceed to Task 2
- **Task 1 broken** → Fix before proceeding

### Hour 13: Task 2 Status
- **Task 2 working** → Proceed to Task 3
- **Task 2 broken** → Skip Task 3, focus on polish

### Hour 17: Training Status
- **Training converging** → Continue to held-out test
- **Training not converging** → Use scripted baseline demo

### Hour 21: Submission Status
- **All done** → Polish and test
- **Not done** → Cut scope, ensure minimum viable

---

## Red Flags (Stop and Fix)

- ❌ Tests 01-03 fail → Fix installation immediately
- ❌ Task 1 doesn't run → Fix before adding features
- ❌ Reward always 0.0 → Debug reward function
- ❌ Episodes crash → Fix termination logic
- ❌ Docker doesn't run → Check headless mode

---

## Success Metrics

### Environment Innovation (40%)
- [ ] Novel task (multi-drone coordination)
- [ ] Proactive sensing design
- [ ] Dynamic resource allocation
- [ ] Genuine reasoning required (not automation)

### Storytelling (30%)
- [ ] Clear problem statement
- [ ] Compelling demo (before/after)
- [ ] README explains everything
- [ ] Video/blog is engaging

### Showing Improvement (20%)
- [ ] Reward curves show learning
- [ ] Before/after behavior comparison
- [ ] Held-out scene generalization

### Pipeline Setup (10%)
- [ ] Reward logic coherent
- [ ] Training script works
- [ ] Environment deployed

---

## Final Checklist (Before Submission)

- [ ] Environment runs in Docker (headless)
- [ ] All 8 tools work correctly
- [ ] Reward function returns dictionary
- [ ] Training script exists (Colab)
- [ ] README has all links
- [ ] Video/blog created (<2 min)
- [ ] Submitted to HuggingFace Space
- [ ] URL submitted to hackathon

**Good luck!** 🚁
