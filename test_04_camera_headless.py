#!/usr/bin/env python3
"""
Test 04: CRITICAL TEST - Verify TinyRenderer produces usable images in headless mode

This is the DECISION GATE for the entire project:
- If this PASSES → proceed with vision-based scan_area tool
- If this FAILS → redesign scan_area to use raycast API instead

TinyRenderer is PyBullet's CPU-based renderer that works without GPU/display.
It's slower than OpenGL but should work in Docker/headless environments.
"""

import sys
import numpy as np
import pybullet as p
import pybullet_data

def test_camera_headless():
    """Test camera image capture in DIRECT mode using TinyRenderer."""
    print("=" * 60)
    print("TEST 04: CAMERA IN HEADLESS MODE (CRITICAL)")
    print("=" * 60)
    print("\nThis test determines if vision-based scan_area is viable.")
    print("If this fails, we'll use raycast-based obstacle detection instead.\n")
    
    client = None
    
    try:
        # Test 1: Connect and load scene
        print("[1/6] Connecting to PyBullet DIRECT mode...")
        client = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        print("✓ Connected")
        
        print("\n[2/6] Loading test scene (plane + cube)...")
        plane_id = p.loadURDF("plane.urdf", physicsClientId=client)
        cube_id = p.loadURDF(
            "cube_small.urdf",
            basePosition=[3.0, 0.0, 0.5],
            physicsClientId=client
        )
        print(f"✓ Scene loaded (plane: {plane_id}, cube: {cube_id})")
        
        # Test 2: Step simulation to ensure objects are stable
        print("\n[3/6] Running physics to stabilize scene...")
        for _ in range(100):
            p.stepSimulation(physicsClientId=client)
        print("✓ Scene stabilized")
        
        # Test 3: Capture camera image using TinyRenderer
        print("\n[4/6] Capturing camera image with TinyRenderer...")
        print("  Camera position: [0, 0, 2] looking at [3, 0, 0.5]")
        print("  Renderer: ER_TINY_RENDERER (CPU-based, headless-compatible)")
        
        width, height = 224, 224
        
        view_matrix = p.computeViewMatrix(
            cameraEyePosition=[0, 0, 2],
            cameraTargetPosition=[3, 0, 0.5],
            cameraUpVector=[0, 0, 1],
            physicsClientId=client
        )
        
        proj_matrix = p.computeProjectionMatrixFOV(
            fov=60,
            aspect=float(width) / height,
            nearVal=0.1,
            farVal=50.0,
            physicsClientId=client
        )
        
        _, _, rgb, depth, seg = p.getCameraImage(
            width=width,
            height=height,
            viewMatrix=view_matrix,
            projectionMatrix=proj_matrix,
            renderer=p.ER_TINY_RENDERER,  # CRITICAL: CPU renderer for headless
            physicsClientId=client
        )
        
        print("✓ Camera image captured")
        
        # Test 4: Verify image data
        print("\n[5/6] Verifying image data...")
        rgb_array = np.array(rgb, dtype=np.uint8).reshape(height, width, 4)
        rgb_only = rgb_array[:, :, :3]  # Drop alpha channel
        
        print(f"  RGB shape: {rgb_only.shape}")
        print(f"  RGB dtype: {rgb_only.dtype}")
        print(f"  RGB min: {rgb_only.min()}, max: {rgb_only.max()}")
        print(f"  RGB mean: {rgb_only.mean():.2f}")
        
        # Critical checks
        checks_passed = True
        
        if rgb_only.shape != (height, width, 3):
            print(f"  ✗ FAIL: Unexpected shape {rgb_only.shape}")
            checks_passed = False
        else:
            print(f"  ✓ Shape correct: {rgb_only.shape}")
        
        if rgb_only.max() == 0:
            print(f"  ✗ FAIL: All pixels are black (max value is 0)")
            print(f"    TinyRenderer is not producing output")
            checks_passed = False
        else:
            print(f"  ✓ Image has content (max pixel value: {rgb_only.max()})")
        
        if rgb_only.min() == rgb_only.max():
            print(f"  ✗ FAIL: All pixels have same value (no variation)")
            checks_passed = False
        else:
            print(f"  ✓ Image has variation (min: {rgb_only.min()}, max: {rgb_only.max()})")
        
        # Test 5: Save image for visual inspection
        print("\n[6/6] Saving test image for visual inspection...")
        try:
            import cv2
            # Convert RGB to BGR for OpenCV
            bgr = cv2.cvtColor(rgb_only, cv2.COLOR_RGB2BGR)
            cv2.imwrite("test_camera_output.png", bgr)
            print("✓ Image saved to: test_camera_output.png")
            print("  ACTION: Manually inspect this image to verify quality")
        except Exception as e:
            print(f"  ⚠ Could not save image: {e}")
            print("  (This is not critical - the test can still pass)")
        
        # Final verdict
        print("\n" + "=" * 60)
        if checks_passed:
            print("✓ TEST PASSED - TinyRenderer works in headless mode")
            print("\nDECISION: Proceed with vision-based scan_area tool")
            print("  - Use OpenCV color masking on camera frames")
            print("  - Test color detection in test_07_opencv_pipeline.py")
            print("\nNEXT STEPS:")
            print("  1. Inspect test_camera_output.png visually")
            print("  2. If image quality is poor, consider raycast fallback")
            print("  3. Run test_05_spawn_control.py")
        else:
            print("✗ TEST FAILED - TinyRenderer not producing valid output")
            print("\nDECISION: Use raycast-based scan_area instead")
            print("  - Implement scan_area using p.rayTestBatch()")
            print("  - Skip test_07_opencv_pipeline.py")
            print("  - This is still a valid approach for the hackathon")
        print("=" * 60)
        
        return checks_passed
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 60)
        print("FAILURE ANALYSIS:")
        print("  Camera capture failed in headless mode.")
        print("\nDECISION: Use raycast-based scan_area")
        print("  - p.rayTestBatch() for obstacle detection")
        print("  - No vision pipeline needed")
        print("  - This is a valid alternative for the hackathon")
        print("=" * 60)
        return False
        
    finally:
        if client is not None:
            p.disconnect(client)
            print("\nDisconnected from PyBullet")

if __name__ == "__main__":
    success = test_camera_headless()
    
    print("\n" + "=" * 60)
    print("CRITICAL DECISION POINT")
    print("=" * 60)
    if success:
        print("✓ Vision-based scan_area is VIABLE")
        print("  Continue to test_05_spawn_control.py")
    else:
        print("✗ Vision-based scan_area is NOT VIABLE")
        print("  Redesign scan_area to use raycast API")
        print("  This is NOT a failure - raycast is a valid approach")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
