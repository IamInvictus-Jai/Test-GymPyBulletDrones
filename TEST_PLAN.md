# EDITH Drone Environment - Test Plan & Decision Tree

## Objective

Verify that gym-pybullet-drones can run in **headless mode** (no GUI, no display server) and determine whether **vision-based** or **raycast-based** obstacle detection should be used for the `scan_area` tool.

## Critical Decision Point

**Test 04 (Camera in Headless Mode) is the decision gate:**

```
test_04_camera_headless.py
         |
         ├─ PASS → Use vision-based scan_area
         |         - OpenCV color masking
         |         - Detect red (obstacles) and green (targets)
         |         - Continue to test_07_opencv_pipeline.py
         |
         └─ FAIL → Use raycast-based scan_area
                   - p.rayTestBatch() for 360° detection
                   - Return distance data in 6 directions
                   - Skip test_07_opencv_pipeline.py
                   - THIS IS NOT A PROJECT FAILURE
```

## Test Phases

### Phase 1: Core Library (Tests 01-03)
**Goal:** Verify PyBullet and gym-pybullet-drones work in headless mode

| Test | What It Checks | If It Fails |
|------|----------------|-------------|
| 01_imports | All packages installed correctly | Install missing packages, check Python version |
| 02_headless_basic | PyBullet DIRECT mode works | Critical failure - cannot run headless |
| 03_headless_env | HoverAviary runs without GUI | Check branch (must be `main`), verify gymnasium installed |

**Stop here if any test fails.** Fix installation before proceeding.

### Phase 2: Camera Test (Test 04) - DECISION GATE
**Goal:** Determine if TinyRenderer produces usable images

| Test | What It Checks | If It Fails |
|------|----------------|-------------|
| 04_camera_headless | TinyRenderer produces valid RGB output | Use raycast instead - NOT a failure |

**After this test:**
1. Check `test_camera_output.png` visually
2. Verify image is not all black
3. Verify objects are visible
4. Make decision: vision vs raycast

### Phase 3: Core Mechanics (Tests 05-07)
**Goal:** Verify drone control and detection systems

| Test | What It Checks | If It Fails |
|------|----------------|-------------|
| 05_spawn_control | Drones spawn at correct positions, PID works | Check API compatibility, verify main branch |
| 06_collision | Collision detection and raycasting work | Check env.PLANE_ID and env.CLIENT accessible |
| 07_opencv_pipeline | Color masking works on TinyRenderer output | Fall back to raycast (skip if camera failed) |

## Expected Outcomes

### Scenario A: All Tests Pass (Best Case)
```
✓ Phase 1: Core library works
✓ Phase 2: Camera works
✓ Phase 3: All mechanics work

DECISION: Use vision-based scan_area
NEXT STEP: Implement OpenCV color masking pipeline
```

### Scenario B: Camera Fails, Others Pass (Common)
```
✓ Phase 1: Core library works
✗ Phase 2: Camera produces black/invalid images
✓ Phase 3: Collision and raycast work

DECISION: Use raycast-based scan_area
NEXT STEP: Implement p.rayTestBatch() for obstacle detection
NOTE: This is a valid approach, not a failure
```

### Scenario C: Early Failure (Installation Issue)
```
✗ Phase 1: Import or headless test fails

DECISION: Fix installation before proceeding
NEXT STEP: Check INSTALL.md troubleshooting section
```

## Implementation Paths

### Path A: Vision-Based scan_area (if camera works)

```python
def scan_area(drone_id):
    """Detect obstacles using camera + OpenCV."""
    # 1. Capture frame from drone camera
    frame = get_drone_camera_frame(env, drone_id)
    
    # 2. Convert to HSV for color masking
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    
    # 3. Detect red obstacles
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    contours_red = cv2.findContours(mask_red, ...)
    
    # 4. Detect green targets
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    contours_green = cv2.findContours(mask_green, ...)
    
    # 5. Return structured detections
    return {
        "detections": [
            {"type": "obstacle", "color": "red", "direction": "left", "distance": 3.2},
            {"type": "target", "color": "green", "direction": "center", "distance": 5.1}
        ]
    }
```

**Pros:**
- More realistic (uses actual camera)
- Can detect object types by color
- Closer to real-world drone operation

**Cons:**
- TinyRenderer is slow (50-200ms per frame)
- Color detection may be unreliable
- Requires tuning HSV thresholds

### Path B: Raycast-Based scan_area (if camera fails)

```python
def scan_area(drone_id):
    """Detect obstacles using raycasting."""
    drone_pos, _ = p.getBasePositionAndOrientation(
        env.DRONE_IDS[drone_id],
        physicsClientId=env.CLIENT
    )
    
    # Cast rays in 8 directions + up + down
    directions = {
        "north": [0, 1, 0],
        "south": [0, -1, 0],
        "east": [1, 0, 0],
        "west": [-1, 0, 0],
        "northeast": [1, 1, 0],
        "northwest": [-1, 1, 0],
        "southeast": [1, -1, 0],
        "southwest": [-1, -1, 0],
        "up": [0, 0, 1],
        "down": [0, 0, -1]
    }
    
    results = p.rayTestBatch(
        rayFromPositions=[drone_pos] * len(directions),
        rayToPositions=[[
            drone_pos[0] + d[0] * check_radius,
            drone_pos[1] + d[1] * check_radius,
            drone_pos[2] + d[2] * check_radius
        ] for d in directions.values()],
        physicsClientId=env.CLIENT
    )
    
    # Return distance in each direction
    detections = []
    for (name, direction), result in zip(directions.items(), results):
        hit_fraction = result[2]
        if hit_fraction < 1.0:
            distance = hit_fraction * check_radius
            detections.append({
                "direction": name,
                "distance": round(distance, 2),
                "obstacle_detected": True
            })
    
    return {"detections": detections}
```

**Pros:**
- Fast (no rendering overhead)
- Reliable (direct physics query)
- 360° coverage
- Works in any environment

**Cons:**
- Cannot distinguish object types by appearance
- Less realistic than camera
- No color information

**Note:** Both approaches are valid for the hackathon. Judges care about the reasoning capability of the LLM agent, not the sensing modality.

## Time Budget

| Phase | Estimated Time | Critical? |
|-------|----------------|-----------|
| Setup & Installation | 30-60 min | Yes |
| Phase 1 Tests (01-03) | 5-10 min | Yes |
| Phase 2 Test (04) | 5-10 min | Yes |
| Phase 3 Tests (05-07) | 15-20 min | No |
| **Total** | **55-100 min** | - |

**Critical path:** Tests 01-04 must pass. Tests 05-07 are verification only.

## Success Criteria

### Minimum Viable (Must Have)
- ✓ Test 01: Imports work
- ✓ Test 02: Headless mode works
- ✓ Test 03: Environment runs without GUI
- ✓ Test 04: Decision made (vision OR raycast)

### Full Verification (Nice to Have)
- ✓ Test 05: Spawn and control work
- ✓ Test 06: Collision detection works
- ✓ Test 07: OpenCV pipeline works (if using vision)

## Next Steps After Testing

### If All Tests Pass
1. Implement chosen scan_area approach (vision or raycast)
2. Build remaining 7 tool functions
3. Create Task 1 environment (Navigate & Reach)
4. Test with random agent
5. Proceed to Tasks 2 and 3

### If Camera Fails
1. Implement raycast-based scan_area
2. Skip vision pipeline entirely
3. Build remaining 7 tool functions
4. Create Task 1 environment
5. Proceed normally (no impact on project)

### If Early Tests Fail
1. Fix installation issues
2. Verify Python 3.10
3. Verify main branch of gym-pybullet-drones
4. Re-run tests
5. Do not proceed until fixed

## Questions to Answer

After running tests, you should know:

- [ ] Does PyBullet work in headless mode? (Test 02)
- [ ] Does gym-pybullet-drones work without GUI? (Test 03)
- [ ] Does TinyRenderer produce usable images? (Test 04)
- [ ] Should we use vision or raycast for scan_area? (Test 04 decision)
- [ ] Do drones spawn correctly? (Test 05)
- [ ] Does collision detection work? (Test 06)
- [ ] Does color masking work? (Test 07, if applicable)

## Final Recommendation

**Run the tests now.** The camera test (04) is the only unknown. Everything else should pass if installation is correct. The test suite will tell you exactly what to do next.

```bash
python3 run_all_tests.py
```

Then check the output and follow the decision tree above.
