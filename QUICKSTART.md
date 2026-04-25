# Quick Start Guide

## 1. Install (5 minutes)

```bash
# Linux/macOS
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

## 2. Run Tests (10 minutes)

```bash
python3 run_all_tests.py
```

## 3. Check Results

### ✓ All tests pass
→ Proceed with vision-based scan_area  
→ Check `test_camera_output.png` to verify image quality

### ✗ Camera test fails (test 04)
→ Use raycast-based scan_area instead  
→ This is NOT a failure - raycast is valid

### ✗ Early tests fail (01-03)
→ Fix installation first  
→ See [INSTALL.md](INSTALL.md) troubleshooting

## 4. Next Steps

### If camera works:
```python
# Implement vision-based scan_area
def scan_area(drone_id):
    frame = get_camera_frame(drone_id)
    detections = detect_colored_objects(frame)  # OpenCV
    return {"detections": detections}
```

### If camera fails:
```python
# Implement raycast-based scan_area
def scan_area(drone_id):
    distances = get_obstacle_distances_raycast(drone_id)
    return {"detections": distances}
```

## Key Files

- `run_all_tests.py` - Run all tests
- `TEST_PLAN.md` - Detailed test plan and decision tree
- `INSTALL.md` - Installation troubleshooting
- `test_04_camera_headless.py` - **CRITICAL TEST**

## Decision Tree

```
test_04_camera_headless.py
    |
    ├─ PASS → Vision-based scan_area
    |         (OpenCV color masking)
    |
    └─ FAIL → Raycast-based scan_area
              (p.rayTestBatch)
              (NOT A FAILURE)
```

## Common Issues

| Issue | Solution |
|-------|----------|
| ImportError: gym_pybullet_drones | `cd gym-pybullet-drones && git checkout main && pip install -e .` |
| ImportError: gymnasium | `pip install gymnasium` (NOT `gym`) |
| pybullet build fails | `sudo apt install build-essential` (Ubuntu) |
| Camera produces black image | Use raycast instead - this is expected |
| Wrong Python version | Use Python 3.10 exactly |

## Time Budget

- Setup: 30-60 min
- Tests: 10-20 min
- **Total: 40-80 min**

## Success Criteria

**Minimum (must have):**
- ✓ Tests 01-03 pass (headless mode works)
- ✓ Test 04 completes (decision made)

**Full verification (nice to have):**
- ✓ Tests 05-07 pass (all mechanics verified)

## Help

- Detailed installation: [INSTALL.md](INSTALL.md)
- Test plan: [TEST_PLAN.md](TEST_PLAN.md)
- Troubleshooting: `Docs/Drone/GPD test.md` Section 15
