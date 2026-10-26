"""Generates high-resolution architecture diagram and Devpost gallery media assets."""

import os
from PIL import Image, ImageDraw, ImageFont

def create_architecture_diagram(output_path="assets/architecture_diagram.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    width, height = 1600, 900
    img = Image.new("RGBA", (width, height), (15, 18, 24, 255))
    draw = ImageDraw.Draw(img)

    # Header Banner
    draw.rectangle([(0, 0), (width, 90)], fill=(22, 27, 34, 255))
    draw.rectangle([(0, 0), (width, 6)], fill=(232, 62, 92, 255))
    
    # Title
    draw.text((50, 25), "SafeSight AI | System Architecture & Agentic Data Flow", fill=(255, 255, 255))
    draw.text((width - 450, 32), "OpenCV AI Competition 2026 (Powered by AWS)", fill=(88, 166, 255))

    # Boxes: 4 Pillars
    pillars = [
        {
            "title": "1. Edge Perception (OpenCV 5)",
            "color": (92, 62, 232),
            "rect": (50, 130, 400, 780),
            "items": [
                "• Ingestion: IP RTSP / CCTV Streams",
                "• cv2.createBackgroundSubtractorMOG2",
                "• Morphological Noise Filtering",
                "• Dynamic Entity Contour Tracking",
                "• pointPolygonTest (Millisecond Collision)",
                "• Translucent Hazard HUD (cv2.addWeighted)",
                "• Target ROI Crop & Base64 Encoder"
            ]
        },
        {
            "title": "2. Cognitive Engine (AWS Bedrock)",
            "color": (255, 153, 0),
            "rect": (430, 130, 780, 780),
            "items": [
                "• Target: Claude 3.5 Sonnet / Multi-modal",
                "• Real-time Hazard Threat Assessment",
                "• OSHA Regulatory Knowledge Base",
                "  - 29 CFR 1910.212 (Machine Guarding)",
                "  - 29 CFR 1910.303 (Electrical Bays)",
                "• Autonomous Tool Planning & Sequencing",
                "• Chain-of-Thought Cognitive Audit Trace",
                "• Resilient Local Fallback Simulator"
            ]
        },
        {
            "title": "3. Autonomous Actions",
            "color": (0, 180, 216),
            "rect": (810, 130, 1160, 780),
            "items": [
                "• tool_trigger_emergency_interlock",
                "  -> Direct PLC Relay Stop Protocol",
                "• tool_dispatch_safety_supervisor",
                "  -> Geo-targeted Mobile Response Team",
                "• tool_cite_osha_regulation",
                "  -> Auto-formatted Legal Citation",
                "• tool_log_incident_s3",
                "  -> Immutable Audit Sink in AWS S3"
            ]
        },
        {
            "title": "4. Enterprise Console",
            "color": (0, 200, 116),
            "rect": (1190, 130, 1550, 780),
            "items": [
                "• Streamlit Mission Control HUD",
                "• Real-time FPS & Threat Telemetry",
                "• Multi-zone Polygon Configuration",
                "• One-click Simulation Loop Mode",
                "• Compliance Audit JSON Exporter",
                "• Live Cognitive Stream Inspection"
            ]
        }
    ]

    for p in pillars:
        x1, y1, x2, y2 = p["rect"]
        # Card Background
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=12, fill=(22, 27, 34, 255), outline=p["color"], width=2)
        # Header Box
        draw.rounded_rectangle([(x1, y1), (x2, y1 + 55)], radius=12, fill=p["color"])
        draw.text((x1 + 15, y1 + 18), p["title"], fill=(255, 255, 255))
        
        # Items
        curr_y = y1 + 80
        for item in p["items"]:
            draw.text((x1 + 20, curr_y), item, fill=(220, 225, 235))
            curr_y += 38

    # Connecting arrows between pillars
    arrow_y = 450
    for ax in [407, 787, 1167]:
        draw.line([(ax, arrow_y), (ax + 16, arrow_y)], fill=(255, 255, 255), width=3)
        draw.polygon([(ax + 16, arrow_y - 6), (ax + 24, arrow_y), (ax + 16, arrow_y + 6)], fill=(255, 255, 255))

    img.save(output_path, "PNG")
    print(f"Architecture diagram saved: {output_path}")

if __name__ == "__main__":
    create_architecture_diagram()
