#!/usr/bin/env python3
"""
Master test runner - executes all tests in order and provides summary.
Stops at first failure unless --continue flag is used.
"""

import sys
import subprocess
import argparse
from pathlib import Path

TESTS = [
    {
        "name": "01_imports",
        "file": "test_01_imports.py",
        "description": "Verify all imports work",
        "critical": True,
        "phase": "Phase 1: Core Library"
    },
    {
        "name": "02_headless_basic",
        "file": "test_02_headless_basic.py",
        "description": "Verify PyBullet DIRECT mode",
        "critical": True,
        "phase": "Phase 1: Core Library"
    },
    {
        "name": "03_headless_env",
        "file": "test_03_headless_env.py",
        "description": "Verify HoverAviary headless",
        "critical": True,
        "phase": "Phase 1: Core Library"
    },
    {
        "name": "04_camera_headless",
        "file": "test_04_camera_headless.py",
        "description": "CRITICAL: Test TinyRenderer camera",
        "critical": True,
        "phase": "Phase 2: Camera Test (DECISION GATE)",
        "decision_gate": True
    },
    {
        "name": "05_spawn_control",
        "file": "test_05_spawn_control.py",
        "description": "Drone spawn and PID control",
        "critical": False,
        "phase": "Phase 3: Core Mechanics"
    },
    {
        "name": "06_collision",
        "file": "test_06_collision.py",
        "description": "Collision detection",
        "critical": False,
        "phase": "Phase 3: Core Mechanics"
    },
    {
        "name": "07_opencv_pipeline",
        "file": "test_07_opencv_pipeline.py",
        "description": "OpenCV color masking (if camera works)",
        "critical": False,
        "phase": "Phase 3: Core Mechanics",
        "skip_if_camera_failed": True
    },
]

def run_test(test_file):
    """Run a single test file and return success status."""
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Test timed out after 60 seconds"
    except Exception as e:
        return False, "", str(e)

def main():
    parser = argparse.ArgumentParser(description="Run all GPD verification tests")
    parser.add_argument("--continue", dest="continue_on_failure", action="store_true",
                        help="Continue running tests even if one fails")
    parser.add_argument("--verbose", action="store_true",
                        help="Show full test output")
    args = parser.parse_args()
    
    print("=" * 70)
    print("EDITH DRONE ENVIRONMENT - VERIFICATION TEST SUITE")
    print("=" * 70)
    print()
    
    results = []
    camera_test_passed = None
    current_phase = None
    
    for i, test in enumerate(TESTS, 1):
        # Print phase header if changed
        if test["phase"] != current_phase:
            current_phase = test["phase"]
            print("\n" + "=" * 70)
            print(f"{current_phase}")
            print("=" * 70)
        
        # Skip test if camera failed and this test depends on it
        if test.get("skip_if_camera_failed") and camera_test_passed is False:
            print(f"\n[{i}/{len(TESTS)}] SKIPPED: {test['name']}")
            print(f"    {test['description']}")
            print("    Reason: Camera test failed, vision pipeline not viable")
            results.append({"test": test["name"], "status": "SKIPPED", "reason": "camera_failed"})
            continue
        
        print(f"\n[{i}/{len(TESTS)}] Running: {test['name']}")
        print(f"    {test['description']}")
        
        test_file = Path(__file__).parent / test["file"]
        
        if not test_file.exists():
            print(f"    ✗ FAILED: Test file not found: {test_file}")
            results.append({"test": test["name"], "status": "MISSING"})
            if test["critical"] and not args.continue_on_failure:
                break
            continue
        
        success, stdout, stderr = run_test(test_file)
        
        if success:
            print(f"    ✓ PASSED")
            results.append({"test": test["name"], "status": "PASSED"})
            
            # Track camera test result
            if test["name"] == "04_camera_headless":
                camera_test_passed = True
        else:
            print(f"    ✗ FAILED")
            results.append({"test": test["name"], "status": "FAILED"})
            
            # Track camera test result
            if test["name"] == "04_camera_headless":
                camera_test_passed = False
            
            if args.verbose:
                print("\n--- STDOUT ---")
                print(stdout)
                if stderr:
                    print("\n--- STDERR ---")
                    print(stderr)
            
            if test["critical"] and not args.continue_on_failure:
                print(f"\n    Critical test failed. Stopping.")
                break
        
        # Print decision gate message
        if test.get("decision_gate"):
            print("\n" + "-" * 70)
            if camera_test_passed:
                print("DECISION: Camera test PASSED")
                print("  → Proceed with vision-based scan_area tool")
                print("  → Continue to test_07_opencv_pipeline.py")
            else:
                print("DECISION: Camera test FAILED")
                print("  → Use raycast-based scan_area tool instead")
                print("  → Skip test_07_opencv_pipeline.py")
                print("  → This is NOT a project failure - raycast is valid")
            print("-" * 70)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in results if r["status"] == "PASSED")
    failed = sum(1 for r in results if r["status"] == "FAILED")
    skipped = sum(1 for r in results if r["status"] == "SKIPPED")
    missing = sum(1 for r in results if r["status"] == "MISSING")
    
    print(f"\nTotal tests: {len(results)}")
    print(f"  ✓ Passed:  {passed}")
    print(f"  ✗ Failed:  {failed}")
    print(f"  ⊘ Skipped: {skipped}")
    print(f"  ? Missing: {missing}")
    
    print("\nDetailed results:")
    for r in results:
        status_symbol = {
            "PASSED": "✓",
            "FAILED": "✗",
            "SKIPPED": "⊘",
            "MISSING": "?"
        }[r["status"]]
        print(f"  {status_symbol} {r['test']}: {r['status']}")
    
    # Print next steps
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    
    if failed == 0 and missing == 0:
        print("\n✓ All tests passed!")
        if camera_test_passed:
            print("\nRecommendation:")
            print("  1. Proceed with vision-based scan_area implementation")
            print("  2. Use OpenCV color masking for object detection")
            print("  3. Start building the environment tools")
        else:
            print("\nRecommendation:")
            print("  1. Implement raycast-based scan_area using p.rayTestBatch()")
            print("  2. Skip vision pipeline - not needed")
            print("  3. Start building the environment tools")
    else:
        print("\n✗ Some tests failed")
        print("\nRecommendation:")
        print("  1. Fix failing tests before proceeding")
        print("  2. Check error messages above")
        print("  3. Consult GPD test.md for troubleshooting")
    
    print("=" * 70)
    
    # Exit code
    sys.exit(0 if failed == 0 and missing == 0 else 1)

if __name__ == "__main__":
    main()
