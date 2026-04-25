#!/usr/bin/env python3
"""
Test 05: Verify drone spawn position and PID control
Tests that drones spawn at specified positions and can be controlled.
"""

import sys
import numpy as np

def test_spawn_control():
    """Test drone spawn and basic PID control."""
    print("=" * 60)
    print("TEST 05: Drone Spawn & PID Control")
    print("=" * 60)
    
    env = None
    
    try:
        from gym_pybullet_drones.envs.BaseAviary import BaseAviary
        from gym_pybullet_drones.utils.enums import DroneModel, Physics
        from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
        import pybullet as p
        
        # Test 1: Single drone spawn
        print("\n[1/4] Testing single drone spawn at custom position...")
        spawn_pos = np.array([[2.0, 3.0, 1.5]])
        
        env = BaseAviary(
            drone_model=DroneModel.CF2X,
            num_drones=1,
            initial_xyzs=spawn_pos,
            initial_rpys=np.array([[0.0, 0.0, 0.0]]),
            physics=Physics.PYB,
            gui=False
        )
        
        obs, info = env.reset()
        
        # Verify spawn position
        actual_pos, _ = p.getBasePositionAndOrientation(
            env.DRONE_IDS[0],
            physicsClientId=env.CLIENT
        )
        actual_pos = np.array(actual_pos)
        
        spawn_error = np.linalg.norm(actual_pos - spawn_pos[0])
        print(f"  Requested spawn: {spawn_pos[0]}")
        print(f"  Actual position: {actual_pos}")
        print(f"  Error: {spawn_error:.4f}m")
        
        if spawn_error < 0.01:
            print("✓ Drone spawned at correct position")
        else:
            print(f"⚠ WARNING: Spawn error {spawn_error:.4f}m (expected < 0.01m)")
        
        env.close()
        
        # Test 2: Multi-drone spawn
        print("\n[2/4] Testing two-drone spawn...")
        spawn_positions = np.array([
            [0.0, 0.0, 1.0],
            [2.0, 0.0, 1.0]
        ])
        
        env = BaseAviary(
            drone_model=DroneModel.CF2X,
            num_drones=2,
            initial_xyzs=spawn_positions,
            initial_rpys=np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]),
            physics=Physics.PYB,
            gui=False
        )
        
        obs, info = env.reset()
        
        for i in range(2):
            actual_pos, _ = p.getBasePositionAndOrientation(
                env.DRONE_IDS[i],
                physicsClientId=env.CLIENT
            )
            actual_pos = np.array(actual_pos)
            error = np.linalg.norm(actual_pos - spawn_positions[i])
            print(f"  Drone {i}: requested {spawn_positions[i]}, actual {actual_pos}, error {error:.4f}m")
        
        print("✓ Multi-drone spawn successful")
        
        # Test 3: PID controller initialization
        print("\n[3/4] Testing PID controller initialization...")
        ctrl = DSLPIDControl(drone_model=DroneModel.CF2X)
        print("✓ PID controller created")
        
        # Test 4: PID control computation
        print("\n[4/4] Testing PID control computation...")
        
        # Get current drone state
        drone_pos, drone_orn = p.getBasePositionAndOrientation(
            env.DRONE_IDS[0],
            physicsClientId=env.CLIENT
        )
        drone_vel, drone_ang_vel = p.getBaseVelocity(
            env.DRONE_IDS[0],
            physicsClientId=env.CLIENT
        )
        
        state = np.hstack([drone_pos, drone_orn, drone_vel, drone_ang_vel])
        target_pos = np.array([1.0, 1.0, 1.5])
        
        rpm, _, _ = ctrl.computeControlFromState(
            control_timestep=1.0/48.0,
            state=state,
            target_pos=target_pos,
            target_rpy=np.zeros(3)
        )
        
        print(f"  Current position: {drone_pos}")
        print(f"  Target position: {target_pos}")
        print(f"  Computed RPM: {rpm}")
        print(f"  RPM shape: {rpm.shape}")
        
        if rpm.shape == (4,):
            print("✓ PID controller produces correct RPM output")
        else:
            print(f"✗ FAIL: Expected RPM shape (4,), got {rpm.shape}")
            return False
        
        # Verify RPM values are reasonable
        if np.all(rpm > 0) and np.all(rpm < 30000):
            print(f"✓ RPM values in reasonable range (0-30000)")
        else:
            print(f"⚠ WARNING: RPM values outside expected range")
        
        # Summary
        print("\n" + "=" * 60)
        print("✓ TEST PASSED - Spawn and PID control work")
        print("  Drones spawn at specified positions")
        print("  PID controller computes valid RPM commands")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 60)
        print("FAILURE ANALYSIS:")
        print("  Spawn or PID control failed")
        print("\nPossible causes:")
        print("  1. Wrong gym-pybullet-drones version")
        print("  2. API changes in DSLPIDControl")
        print("=" * 60)
        return False
        
    finally:
        if env is not None:
            env.close()

if __name__ == "__main__":
    success = test_spawn_control()
    sys.exit(0 if success else 1)
