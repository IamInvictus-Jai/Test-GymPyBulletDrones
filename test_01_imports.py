#!/usr/bin/env python3
"""
Test 01: Verify all required imports work
This is the first gate - if this fails, nothing else will work.
"""

import sys

def test_imports():
    """Test all critical imports."""
    print("=" * 60)
    print("TEST 01: Import Verification")
    print("=" * 60)
    
    failures = []
    
    # Test 1: PyBullet
    print("\n[1/6] Testing PyBullet import...")
    try:
        import pybullet as p
        print(f"✓ PyBullet version: {p.getVersionInfo()}")
    except ImportError as e:
        print(f"✗ FAILED: {e}")
        failures.append("pybullet")
    
    # Test 2: Gymnasium
    print("\n[2/6] Testing Gymnasium import...")
    try:
        import gymnasium
        print(f"✓ Gymnasium version: {gymnasium.__version__}")
    except ImportError as e:
        print(f"✗ FAILED: {e}")
        failures.append("gymnasium")
    
    # Test 3: NumPy
    print("\n[3/6] Testing NumPy import...")
    try:
        import numpy as np
        print(f"✓ NumPy version: {np.__version__}")
    except ImportError as e:
        print(f"✗ FAILED: {e}")
        failures.append("numpy")
    
    # Test 4: OpenCV
    print("\n[4/6] Testing OpenCV import...")
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
    except ImportError as e:
        print(f"✗ FAILED: {e}")
        failures.append("opencv-python-headless")
    
    # Test 5: Stable-Baselines3 (optional)
    print("\n[5/6] Testing Stable-Baselines3 import (optional)...")
    try:
        import stable_baselines3
        print(f"✓ Stable-Baselines3 version: {stable_baselines3.__version__}")
    except ImportError as e:
        print(f"⚠ WARNING: {e}")
        print("  (This is optional - only needed for local RL training)")
    
    # Test 6: gym-pybullet-drones (will fail until installed)
    print("\n[6/6] Testing gym-pybullet-drones import...")
    try:
        from gym_pybullet_drones.envs.HoverAviary import HoverAviary
        from gym_pybullet_drones.utils.enums import DroneModel, Physics
        print("✓ gym-pybullet-drones imported successfully")
    except ImportError as e:
        print(f"✗ FAILED: {e}")
        print("\n  ACTION REQUIRED:")
        print("  1. Clone: git clone https://github.com/utiasDSL/gym-pybullet-drones.git")
        print("  2. Checkout main branch: cd gym-pybullet-drones && git checkout main")
        print("  3. Install: pip install -e .")
        failures.append("gym-pybullet-drones")
    
    # Summary
    print("\n" + "=" * 60)
    if failures:
        print(f"✗ TEST FAILED - Missing packages: {', '.join(failures)}")
        print("\nInstall missing packages:")
        print("  pip install -r requirements.txt")
        if "gym-pybullet-drones" in failures:
            print("\nFor gym-pybullet-drones:")
            print("  git clone https://github.com/utiasDSL/gym-pybullet-drones.git")
            print("  cd gym-pybullet-drones")
            print("  git checkout main  # IMPORTANT: use main, not master")
            print("  pip install -e .")
        print("=" * 60)
        return False
    else:
        print("✓ ALL IMPORTS SUCCESSFUL")
        print("=" * 60)
        return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
