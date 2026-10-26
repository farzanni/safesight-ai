"""Generates synthetic industrial video and image assets for instant demo testing."""

import os
import cv2
import numpy as np

def create_synthetic_demo_video(output_path: str = "assets/sample_factory_floor.mp4", duration_sec: int = 10, fps: int = 24):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    width, height = 800, 500
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    total_frames = duration_sec * fps

    for i in range(total_frames):
        # Base factory floor (dark slate background)
        frame = np.full((height, width, 3), (35, 38, 42), dtype=np.uint8)

        # Floor grid lines
        for y in range(0, height, 50):
            cv2.line(frame, (0, y), (width, y), (45, 50, 55), 1)
        for x in range(0, width, 50):
            cv2.line(frame, (x, 0), (x, height), (45, 50, 55), 1)

        # Machinery / Equipment representation (Static)
        cv2.rectangle(frame, (500, 150), (750, 400), (60, 65, 75), -1)
        cv2.rectangle(frame, (500, 150), (750, 400), (120, 130, 140), 2)
        cv2.putText(frame, "HEAVY ROBOT ARM CELL", (520, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # High Voltage Panel
        cv2.rectangle(frame, (50, 320), (340, 470), (45, 45, 55), -1)
        cv2.putText(frame, "HIGH VOLTAGE BAY", (70, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 180, 255), 1)

        # Animated Worker: walks from left (safe area) across towards the robot cell (breaching zone)
        t = i / total_frames
        # Starts at (120, 200), walks across towards (620, 300)
        worker_x = int(100 + t * 540)
        worker_y = int(220 + np.sin(t * np.pi * 3) * 60)

        # Worker head & body
        cv2.circle(frame, (worker_x, worker_y - 25), 12, (255, 200, 50), -1) # Helmet
        cv2.rectangle(frame, (worker_x - 14, worker_y - 12), (worker_x + 14, worker_y + 35), (40, 120, 230), -1) # Vest
        cv2.line(frame, (worker_x - 8, worker_y + 35), (worker_x - 10, worker_y + 65), (20, 20, 20), 4) # Leg
        cv2.line(frame, (worker_x + 8, worker_y + 35), (worker_x + 10, worker_y + 65), (20, 20, 20), 4) # Leg

        out.write(frame)

    out.release()
    print(f"Demo video saved to {output_path}")

    # Also save one still frame for instant image testing
    cv2.imwrite("assets/test_violation_frame.jpg", frame)
    print("Demo still frame saved to assets/test_violation_frame.jpg")

if __name__ == "__main__":
    create_synthetic_demo_video()
