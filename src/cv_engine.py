"""SafeSight AI - OpenCV Vision & Perception Engine.

Handles video ingestion, background modeling, motion segmentation,
spatial exclusion zone violation detection, and ROI extraction for the agent.
"""

import cv2
import numpy as np
import base64
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from src.config import ZoneConfig, CONFIG

@dataclass
class TrackedTarget:
    target_id: int
    bbox: Tuple[int, int, int, int]  # (x, y, w, h)
    centroid: Tuple[int, int]
    in_hazard_zone: Optional[str] = None
    violation_frames: int = 0
    speed_px: float = 0.0

@dataclass
class FrameAnalysisResult:
    annotated_frame: np.ndarray
    violation_detected: bool
    active_violations: List[Dict[str, Any]]
    motion_mask: np.ndarray
    tracked_targets: List[TrackedTarget]
    violation_roi_b64: Optional[str] = None

class OpenCVSafetyPipeline:
    def __init__(self, zones: Optional[List[ZoneConfig]] = None):
        self.zones = zones if zones is not None else CONFIG.default_zones
        # OpenCV 5 MOG2 background subtractor for motion segmentation
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=CONFIG.motion_history_length,
            varThreshold=CONFIG.motion_var_threshold,
            detectShadows=True
        )
        self.morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        self.target_history: Dict[int, Tuple[int, int]] = {}
        self.next_target_id: int = 1

    def process_frame(self, frame: np.ndarray) -> FrameAnalysisResult:
        """Processes a single BGR frame through the OpenCV perception pipeline."""
        height, width = frame.shape[:2]
        annotated = frame.copy()
        
        # 1. Spatial Zone Normalization to Pixel Coordinates
        pixel_zones = []
        for zone in self.zones:
            pts = np.array([
                [int(p[0] * width), int(p[1] * height)] for p in zone.polygon
            ], np.int32)
            pixel_zones.append((zone, pts))

        # 2. Motion Detection & Background Subtraction
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        fg_mask = self.bg_subtractor.apply(blurred)

        # Remove shadows (value 127 in MOG2) & filter noise via morphological ops
        _, thresh_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        cleaned_mask = cv2.morphologyEx(thresh_mask, cv2.MORPH_OPEN, self.morph_kernel)
        cleaned_mask = cv2.dilate(cleaned_mask, self.morph_kernel, iterations=2)

        # 3. Contour Detection for Moving Entities (Personnel / Equipment)
        contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        current_targets: List[TrackedTarget] = []
        active_violations: List[Dict[str, Any]] = []
        violation_detected = False
        roi_base64: Optional[str] = None

        # Draw Zone Overlays (Transparent HUD)
        zone_overlay = annotated.copy()
        for zone, pts in pixel_zones:
            color = (0, 0, 220) if zone.severity == "CRITICAL" else (0, 140, 255)
            cv2.fillPoly(zone_overlay, [pts], color)
            cv2.polylines(annotated, [pts], isClosed=True, color=color, thickness=2)
            # Label
            label_pos = (pts[0][0], max(25, pts[0][1] - 8))
            cv2.putText(annotated, f"[{zone.severity}] {zone.name}", label_pos,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Blend hazard zones onto frame (30% alpha for HUD effect)
        cv2.addWeighted(zone_overlay, 0.25, annotated, 0.75, 0, annotated)

        # 4. Target Extraction & Geometric Hazard Boundary Collision Test
        min_area = (width * height) * 0.003  # Filter trivial contours
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_area:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            centroid = (x + w // 2, y + h // 2)

            # Assign simple tracking ID
            target_id = self._match_or_assign_id(centroid)
            speed = self._calculate_speed(target_id, centroid)

            in_zone_name = None
            for zone, pts in pixel_zones:
                # cv2.pointPolygonTest returns positive if inside, 0 on edge, negative if outside
                dist = cv2.pointPolygonTest(pts, centroid, measureDist=False)
                if dist >= 0:
                    in_zone_name = zone.name
                    violation_detected = True
                    
                    # Capture violation details
                    violation_record = {
                        "target_id": target_id,
                        "zone_name": zone.name,
                        "severity": zone.severity,
                        "location_bbox": (x, y, w, h),
                        "speed_px": speed,
                        "description": zone.description
                    }
                    active_violations.append(violation_record)

                    # Extract ROI crop for Multimodal AI inspection
                    if roi_base64 is None:
                        margin = 20
                        roi_x1 = max(0, x - margin)
                        roi_y1 = max(0, y - margin)
                        roi_x2 = min(width, x + w + margin)
                        roi_y2 = min(height, y + h + margin)
                        crop = frame[roi_y1:roi_y2, roi_x1:roi_x2]
                        if crop.size > 0:
                            _, buffer = cv2.imencode('.jpg', crop)
                            roi_base64 = base64.b64encode(buffer).decode('utf-8')

            # Render Bounding Box and telemetry
            box_color = (0, 0, 255) if in_zone_name else (0, 255, 120)
            cv2.rectangle(annotated, (x, y), (x + w, y + h), box_color, 2)
            cv2.circle(annotated, centroid, 4, box_color, -1)
            
            tag = f"Entity #{target_id} | Spd: {speed:.1f}px/s"
            if in_zone_name:
                tag = f"VIOLATION: ID #{target_id}"
                
            cv2.putText(annotated, tag, (x, max(20, y - 6)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, box_color, 1, cv2.LINE_AA)

            current_targets.append(TrackedTarget(
                target_id=target_id,
                bbox=(x, y, w, h),
                centroid=centroid,
                in_hazard_zone=in_zone_name,
                speed_px=speed
            ))

        return FrameAnalysisResult(
            annotated_frame=annotated,
            violation_detected=violation_detected,
            active_violations=active_violations,
            motion_mask=cleaned_mask,
            tracked_targets=current_targets,
            violation_roi_b64=roi_base64
        )

    def _match_or_assign_id(self, centroid: Tuple[int, int]) -> int:
        best_id = None
        min_dist = 60.0  # Max pixel jump between frames
        for tid, prev_pt in self.target_history.items():
            dist = np.hypot(centroid[0] - prev_pt[0], centroid[1] - prev_pt[1])
            if dist < min_dist:
                min_dist = dist
                best_id = tid
        if best_id is None:
            best_id = self.next_target_id
            self.next_target_id += 1
        self.target_history[best_id] = centroid
        return best_id

    def _calculate_speed(self, target_id: int, centroid: Tuple[int, int]) -> float:
        if target_id in self.target_history:
            prev = self.target_history[target_id]
            dist = np.hypot(centroid[0] - prev[0], centroid[1] - prev[1])
            return float(dist * 15.0)  # Simulated frame-rate scalar
        return 0.0
