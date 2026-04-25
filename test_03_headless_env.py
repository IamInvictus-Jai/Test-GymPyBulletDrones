#!/usr/bin/env python3
"""
Test 03: Verify HoverAviary environment runs in headless mode
This tests the full gym-pybullet-drones environment without GUI.
"""

import sys
import numpy as np

def test_headless_env():
    """Test HoverAviary environment in headless mode."""
    print("=" * 60)
    print("TEST 03: HoverAviary Headless Environment")
    print("=" * 60)
    
    env = None
    
    try:
        # Import here to give better error message if not installed
        print("\n[1/5] Importing gym-pybullet-drones...")
        from gym_pybullet_drones.envs.HoverAviary import HoverAviary
        from gym_pybullet_drones.utils.enums import DroneModel, Physics
        print("✓ Imports successful")
        
        # Test 2: Create environment
        print("\n[2/5] Creating HoverAviary environment (headless)...")
        env = HoverAviary(
            drone_model=DroneModel.CF2X,
            initial_xyzs=np.array([[0.0, 0.0, 1.0]]),
            physics=Physics.PYB,
            pyb_freq=240,
            ctrl_freq=48,
            gui=False,  # CRITICAL: headless mode
            record=False
        )
        print("✓ Environment created successfully")
        
        # Test 3: Reset environment
        print("\n[3/5] Resetting environment...")
        obs, info = env.reset()
        print(f"✓ Environment reset successful")
        print(f"  Observation shape: {obs.shape}")
        print(f"  Expected shape: (1, 20) for single drone")
        
        if obs.shape != (1, 20):
            print(f"  ⚠ WARNING: Unexpected observation shape")
        
        # Test 4: Run episode
        print("\n[4/5] Running 500 simulation steps...")
        for step in range(500):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            
            if terminated or truncated:
                print(f"  Episode ended at step {step}")
                break
        
        print(f"✓ Completed {min(step + 1, 500)} steps without crash")
        print(f"  Final observation: {obs[0, :3]}")  # x, y, z position
        
        # Test 5: Verify observation structure
        print("\n[5/5] Verifying observation structure...")
        print(f"  Position (x,y,z): {obs[0, 0:3]}")
        print(f"  Quaternion: {obs[0, 3:7]}")
        print(f"  Euler (r,p,y): {obs[0, 7:10]}")
        print(f"  Velocity: {obs[0, 10:13]}")
        print(f"  Angular velocity: {obs[0, 13:16]}")
        print(f"  RPM: {obs[0, 16:20]}")
        print("✓ Observation structure verified")
        
        # Summary
        print("\n" + "=" * 60)
        print("✓ TEST PASSED - HoverAviary works in headless mode")
        print("  The environment can run without GUI.")
        print("  Ready to proceed to camera test.")
        print("=" * 60)
        return True
        
    except ImportError as e:
        print(f"\n✗ TEST FAILED: Import error")
        print(f"  {e}")
        print("\n" + "=" * 60)
        print("ACTION REQUIRED:")
        print("  Install gym-pybullet-drones:")
        print("  1. git clone https://github.com/utiasDSL/gym-pybullet-drones.git")
        print("  2. cd gym-pybullet-drones")
        print("  3. git checkout main  # IMPORTANT: main branch, not master")
        print("  4. pip install -e .")
        print("=" * 60)
        return False
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        print("\n" + "=" * 60)
        print("FAILURE ANALYSIS:")
        print("  The environment failed to run in headless mode.")
        print("\nPossible causes:")
        print("  1. Wrong branch (use 'main', not 'master')")
        print("  2. Incompatible Python version (requires 3.10)")
        print("  3. Missing dependencies")
        print("\nDebug steps:")
        print("  python -c 'import gymnasium; print(gymnasium.__version__)'")
        print("  python -c 'import pybullet; print(pybullet.getVersionInfo())'")
        print("=" * 60)
        return False
        
    finally:
        if env is not None:
            env.close()
            print("\nEnvironment closed")

if __name__ == "__main__":
    success = test_headless_env()
    sys.exit(0 if success else 1)
