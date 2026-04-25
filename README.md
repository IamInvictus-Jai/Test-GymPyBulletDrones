# EDITH Drone Environment - Verification Tests

## Overview

This test suite verifies that **gym-pybullet-drones** works correctly in headless mode (no GUI) for the EDITH hackathon project. The most critical test is **test_04_camera_headless.py**, which determines whether we use vision-based or raycast-based obstacle detection.

## Quick Start

```bash
# Linux/macOS
chmod +x setup.sh
./setup.sh
python3 run_all_tests.py

# Windows
setup.bat
python run_all_tests.py
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## Test Execution Order

Run tests in this exact order. Each test is a gate — **do not proceed past any failure**.

### Phase 1: Core Library (CRITICAL)
1. `test_01_imports.py` - Verify all imports work
2. `test_02_headless_basic.py` - Verify PyBullet DIRECT mode works
3. `test_03_headless_env.py` - Verify HoverAviary runs headless

### Phase 2: Camera Test (DECISION GATE)
4. `test_04_camera_headless.py` - **CRITICAL: Test TinyRenderer image output**
   - If this passes → proceed with vision-based scan_area
   - If this fails → redesign scan_area to use raycast API

### Phase 3: Core Mechanics (if camera passes)
5. `test_05_spawn_control.py` - Drone spawn and PID control
6. `test_06_collision.py` - Collision detection
7. `test_07_opencv_pipeline.py` - OpenCV color masking on TinyRenderer output

### Phase 4: Advanced Features (if time permits)
8. `test_08_moving_obstacles.py` - Moving obstacle collision
9. `test_09_battery.py` - Battery simulation

## Quick Start

```bash
# Create conda environment
conda create -n drones python=3.10
conda activate drones

# Install dependencies
pip install --upgrade pip
cd "Drone RL Environment"
pip install -r requirements.txt

# Run tests in order
python test_01_imports.py
python test_02_headless_basic.py
python test_03_headless_env.py
python test_04_camera_headless.py  # CRITICAL GATE
# ... continue if tests pass
```

## Decision Points

### If test_04_camera_headless.py FAILS:
- **Do NOT proceed with vision-based scan_area**
- Redesign scan_area to use `p.rayTestBatch()` for obstacle detection
- This is still valid — many RL environments use raycast instead of vision

### If test_04_camera_headless.py PASSES:
- Proceed to test_07_opencv_pipeline.py
- Verify color masking works on TinyRenderer output
- If color masking is unreliable, still fall back to raycast

## Current Status

- [ ] Phase 1 complete
- [ ] Phase 2 complete (camera decision made)
- [ ] Phase 3 complete
- [ ] Phase 4 complete
