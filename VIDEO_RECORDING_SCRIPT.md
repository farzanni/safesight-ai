# SafeSight AI: 2-Minute Demo Video Script 🎬

> **Goal:** High-energy, crisp 120-second screen recording with voiceover. This video alone drives 40%+ of your judging score.

---

### [0:00 - 0:20] The Problem & The Hook
- **Visual:** Open with full-screen slide or live webcam/screen showing title: **SafeSight AI | Autonomous Physical Safety Supervisor**.
- **Voiceover:**
  > *"Every year, over 2.8 million industrial workplace injuries occur, costing industry $170 billion. Traditional CCTV cameras are completely passive—they record disasters after they happen, or sound false alarms that workers tune out. We built SafeSight AI: an Agentic Vision system that doesn't just watch, but autonomously reasons and acts to prevent injuries before they happen."*

---

### [0:20 - 0:55] OpenCV 5 Spatial Perception Demo
- **Visual:** Switch to the SafeSight AI dashboard (`http://localhost:8501`). Click **▶️ Start Simulation Loop**. Show the worker moving towards the robot arm hazard zone.
- **Voiceover:**
  > *"At the edge, we use OpenCV 5 for millisecond spatial perception. Our pipeline deploys OpenCV 5's MOG2 background subtraction to isolate moving personnel and equipment, filtering environmental noise with morphological transformations. Using OpenCV's pointPolygonTest, we compute exact geometric containment against complex hazard zones without the latency of cloud inference."*

---

### [0:55 - 1:30] Agentic Vision & AWS Bedrock Decision Engine
- **Visual:** The worker breaches the red hazard zone. Zoom in on the right sidebar showing the **Agentic Autonomous Supervisor** cognitive trace, the active OSHA citations, and tool calls.
- **Voiceover:**
  > *"The moment a perimeter breach occurs, OpenCV extracts the target ROI and feeds the telemetry to our AWS Bedrock Agent, powered by Claude 3.5 Sonnet. Instead of a dumb alert, the agent initiates an autonomous reasoning loop: it evaluates threat severity, references OSHA 29 CFR 1910.212 machine guarding regulations, and autonomously fires a sequence of tools—triggering an emergency hardware interlock relay, dispatching safety responders, and streaming an audit log to AWS S3."*

---

### [1:30 - 1:50] AWS Architecture & Audit Log
- **Visual:** Scroll down to the **Autonomous Safety Audit Log** and show the downloaded JSON / AWS S3 sink.
- **Voiceover:**
  > *"Under the hood, our AWS architecture integrates Bedrock runtime with S3 for immutable compliance records. SafeSight AI runs in dual-mode, supporting live AWS cloud execution as well as a zero-dependency local emulator for instant, frictionless evaluation."*

---

### [1:50 - 2:00] Conclusion & Submission Wrap-Up
- **Visual:** Show the repository README with OpenCV 5 + AWS badges and the team slide.
- **Voiceover:**
  > *"SafeSight AI transforms cameras from passive recorders into proactive, autonomous physical guardians. Built for the OpenCV AI Competition 2026. Thank you!"*
