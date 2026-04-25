# Installation & Testing Guide

## Quick Start (Linux/macOS)

```bash
cd "Drone RL Environment"

# Make setup script executable
chmod +x setup.sh

# Run setup (installs everything)
./setup.sh

# Run all tests
python3 run_all_tests.py
```

## Manual Installation

### 1. Create Conda Environment (Recommended)

```bash
conda create -n drones python=3.10
conda activate drones
```

**Important:** Python 3.10 is required. Newer versions may have pybullet build issues.

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install gym-pybullet-drones

```bash
# Clone the repository
git clone https://github.com/utiasDSL/gym-pybullet-drones.git
cd gym-pybullet-drones

# CRITICAL: Use main branch, not master
git checkout main

# Install in editable mode
pip install -e .

cd ..
```

**Why main branch?** The `master` branch is the old 2021 codebase using `gym` (deprecated). The `main` branch uses `gymnasium` and `stable-baselines3 2.0`.

### 4. Verify Installation

```bash
python3 test_01_imports.py
```

If this passes, you're ready to run the full test suite.

## Running Tests

### Run All Tests (Recommended)

```bash
python3 run_all_tests.py
```

This runs tests in order and stops at first critical failure.

**Options:**
- `--continue`: Continue even if a test fails
- `--verbose`: Show full test output

### Run Individual Tests

```bash
# Phase 1: Core Library
python3 test_01_imports.py
python3 test_02_headless_basic.py
python3 test_03_headless_env.py

# Phase 2: Camera Test (CRITICAL DECISION GATE)
python3 test_04_camera_headless.py

# Phase 3: Core Mechanics (if camera passes)
python3 test_05_spawn_control.py
python3 test_06_collision.py
python3 test_07_opencv_pipeline.py
```

## Critical Test: Camera in Headless Mode

**Test 04 is the decision gate for the entire project.**

### If test_04_camera_headless.py PASSES:
- ✓ TinyRenderer produces usable images
- ✓ Proceed with vision-based `scan_area` tool
- ✓ Run test_07_opencv_pipeline.py to verify color detection
- ✓ Implement OpenCV color masking for object detection

### If test_04_camera_headless.py FAILS:
- ✗ TinyRenderer not producing valid output
- ✓ Use raycast-based `scan_area` instead
- ✓ Skip test_07_opencv_pipeline.py
- ✓ Implement `p.rayTestBatch()` for obstacle detection
- ✓ **This is NOT a project failure** - raycast is a valid approach

After test 04, check the generated image:
```bash
# View the test image
open test_camera_output.png  # macOS
xdg-open test_camera_output.png  # Linux
```

Verify:
- Image is not all black
- Objects are visible
- Colors are distinguishable

## Troubleshooting

### ImportError: No module named 'gym_pybullet_drones'

**Solution:**
```bash
cd gym-pybullet-drones
git checkout main  # Make sure you're on main branch
pip install -e .
```

### ImportError: No module named 'gymnasium'

**Solution:**
```bash
pip install gymnasium
```

**Note:** Do NOT install `gym` (deprecated). Use `gymnasium`.

### pybullet build fails on Ubuntu

**Solution:**
```bash
sudo apt install build-essential
pip install --upgrade pybullet
```

### Camera test produces all-black image

**Possible causes:**
1. TinyRenderer not initializing correctly
2. Scene not loaded properly
3. Camera position/orientation wrong

**Solution:**
- Check test output for errors
- Verify test_02_headless_basic.py passed
- If persistent, use raycast-based scan_area instead

### Wrong Python version

**Solution:**
```bash
# Install Python 3.10 via conda
conda create -n drones python=3.10
conda activate drones

# Or use pyenv
pyenv install 3.10.13
pyenv local 3.10.13
```

## Next Steps After Tests Pass

1. **If camera works:**
   - Implement vision-based `scan_area` tool
   - Use OpenCV color masking (red=obstacle, green=target)
   - Test on actual drone environment

2. **If camera fails:**
   - Implement raycast-based `scan_area` tool
   - Use `p.rayTestBatch()` for 360° obstacle detection
   - Return structured distance data to LLM

3. **Start building environment:**
   - Create OpenEnv wrapper
   - Implement 8 tool functions
   - Build Task 1 (Navigate & Reach)
   - Test with random agent

## Test Results Interpretation

### All tests pass
✓ Ready to build the full environment  
✓ All core mechanics verified  
✓ Proceed with implementation

### Camera test fails, others pass
✓ Core mechanics work  
✓ Use raycast instead of vision  
✓ Still ready to build environment

### Early tests fail (01-03)
✗ Installation issue  
✗ Fix dependencies first  
✗ Do not proceed until fixed

## Support

If tests fail and troubleshooting doesn't help:
1. Check `Docs/Drone/GPD test.md` Section 15 (Common Pitfalls)
2. Verify Python version is exactly 3.10
3. Verify you're on `main` branch of gym-pybullet-drones
4. Check that `gui=False` in all environment creation calls
