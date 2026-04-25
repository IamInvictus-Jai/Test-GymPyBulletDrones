#!/usr/bin/env python3
"""
Test 02: Verify PyBullet DIRECT mode works (headless, no GUI)
This is CRITICAL for Docker deployment - must work without display server.
"""

import sys
import pybullet as p
import pybullet_data
import numpy as np

def test_headless_basic():
    """Test PyBullet DIRECT connection mode."""
    print("=" * 60)
    print("TEST 02: PyBullet DIRECT Mode (Headless)")
    print("=" * 60)
    
    client = None
    
    try:
        # Test 1: Connect in DIRECT mode
        print("\n[1/3] Connecting to PyBullet in DIRECT mode...")
        client = p.connect(p.DIRECT)
        print(f"✓ Connected successfully (client ID: {client})")
        
        # Set data path for URDF files
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        
        # Test 2: Load ground plane
        print("\n[2/3] Loading ground plane URDF...")
        plane_id = p.loadURDF("plane.urdf", physicsClientId=client)
        print(f"✓ Ground plane loaded (body ID: {plane_id})")
        
        # Test 3: Run physics simulation
        print("\n[3/3] Running 1000 physics steps...")
        for i in range(1000):
            p.stepSimulation(physicsClientId=client)
        print("✓ 1000 physics steps completed without error")
        
        # Summary
        print("\n" + "=" * 60)
        print("✓ TEST PASSED - PyBullet DIRECT mode works")
        print("  This means headless operation is supported.")
        print("  Docker deployment will work.")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        print("\n" + "=" * 60)
        print("FAILURE ANALYSIS:")
        print("  PyBullet DIRECT mode is not working.")
        print("  This is a critical failure - environment cannot run headless.")
        print("\nPossible causes:")
        print("  1. PyBullet not installed correctly")
        print("  2. Missing system dependencies (build-essential on Ubuntu)")
        print("\nTry:")
        print("  sudo apt install build-essential  # Ubuntu/Debian")
        print("  pip install --upgrade pybullet")
        print("=" * 60)
        return False
        
    finally:
        if client is not None:
            p.disconnect(client)
            print("\nDisconnected from PyBullet")

if __name__ == "__main__":
    success = test_headless_basic()
    sys.exit(0 if success else 1)
