#!/usr/bin/env python3
"""
Test 07: Verify OpenCV color masking works on TinyRenderer output
Only run this if test_04_camera_headless.py PASSED.
"""

import sys
import numpy as np
import cv2
import pybullet as p
import pybullet_data

def get_camera_frame(client, width=224, height=224):
    """Capture camera frame from fixed position."""
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
        renderer=p.ER_TINY_RENDERER,
        physicsClientId=client
    )
    
    rgb_array = np.array(rgb, dtype=np.uint8).reshape(height, width, 4)
    return rgb_array[:, :, :3]  # Drop alpha

def detect_colored_objects(frame):
    """Detect red and green objects using color masking."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    
    detections = []
    
    # Detect red objects (obstacles)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours_red:
        area = cv2.contourArea(cnt)
        if area > 200:  # Filter noise
            detections.append({"color": "red", "area": area, "type": "obstacle"})
    
    # Detect green objects (targets)
    lower_green = np.array([40, 80, 80])
    upper_green = np.array([80, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours_green:
        area = cv2.contourArea(cnt)
        if area > 200:
            detections.append({"color": "green", "area": area, "type": "target"})
    
    return detections, mask_red, mask_green

def test_opencv_pipeline():
    """Test OpenCV color detection on TinyRenderer output."""
    print("=" * 60)
    print("TEST 07: OpenCV Color Masking Pipeline")
    print("=" * 60)
    print("\nNOTE: Only run this if test_04_camera_headless.py PASSED\n")
    
    client = None
    
    try:
        # Test 1: Setup scene with colored objects
        print("[1/4] Setting up scene with colored objects...")
        client = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        
        plane_id = p.loadURDF("plane.urdf", physicsClientId=client)
        
        # Create red obstacle (using visual shape)
        red_col = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.3, 0.3, 0.3], physicsClientId=client)
        red_vis = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[0.3, 0.3, 0.3],
            rgbaColor=[1.0, 0.0, 0.0, 1.0],  # Pure red
            physicsClientId=client
        )
        red_id = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=red_col,
            baseVisualShapeIndex=red_vis,
            basePosition=[3.0, 0.0, 0.5],
            physicsClientId=client
        )
        
        # Create green target
        green_col = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.2, 0.2, 0.2], physicsClientId=client)
        green_vis = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[0.2, 0.2, 0.2],
            rgbaColor=[0.0, 1.0, 0.0, 1.0],  # Pure green
            physicsClientId=client
        )
        green_id = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=green_col,
            baseVisualShapeIndex=green_vis,
            basePosition=[4.0, 1.0, 0.3],
            physicsClientId=client
        )
        
        print(f"✓ Scene created (red obstacle: {red_id}, green target: {green_id})")
        
        # Test 2: Capture frame
        print("\n[2/4] Capturing camera frame...")
        for _ in range(100):
            p.stepSimulation(physicsClientId=client)
        
        frame = get_camera_frame(client)
        print(f"✓ Frame captured: shape {frame.shape}, dtype {frame.dtype}")
        
        # Test 3: Run color detection
        print("\n[3/4] Running color detection...")
        detections, mask_red, mask_green = detect_colored_objects(frame)
        
        print(f"  Total detections: {len(detections)}")
        for det in detections:
            print(f"    - {det['type']} ({det['color']}): area {det['area']:.0f} pixels")
        
        # Test 4: Verify detections
        print("\n[4/4] Verifying detection results...")
        
        red_detected = any(d['color'] == 'red' for d in detections)
        green_detected = any(d['color'] == 'green' for d in detections)
        
        print(f"  Red obstacle detected: {red_detected}")
        print(f"  Green target detected: {green_detected}")
        
        # Save debug images
        try:
            cv2.imwrite("test_opencv_frame.png", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            cv2.imwrite("test_opencv_mask_red.png", mask_red)
            cv2.imwrite("test_opencv_mask_green.png", mask_green)
            print("\n  Debug images saved:")
            print("    - test_opencv_frame.png (original)")
            print("    - test_opencv_mask_red.png (red mask)")
            print("    - test_opencv_mask_green.png (green mask)")
        except Exception as e:
            print(f"  ⚠ Could not save debug images: {e}")
        
        # Summary
        print("\n" + "=" * 60)
        if red_detected or green_detected:
            print("✓ TEST PASSED - Color detection works")
            print(f"  Red detected: {red_detected}")
            print(f"  Green detected: {green_detected}")
            print("\nDECISION: Vision-based scan_area is viable")
            print("  Proceed with OpenCV color masking implementation")
        else:
            print("✗ TEST FAILED - No colored objects detected")
            print("\nPossible causes:")
            print("  1. TinyRenderer lighting model doesn't preserve colors well")
            print("  2. HSV thresholds need tuning for TinyRenderer output")
            print("  3. Objects not in camera view")
            print("\nDECISION: Fall back to raycast-based scan_area")
            print("  Use p.rayTestBatch() instead of vision")
        print("=" * 60)
        
        return red_detected or green_detected
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 60)
        print("DECISION: Fall back to raycast-based scan_area")
        print("=" * 60)
        return False
        
    finally:
        if client is not None:
            p.disconnect(client)

if __name__ == "__main__":
    success = test_opencv_pipeline()
    sys.exit(0 if success else 1)
