# Devpost Submission Text: SafeSight AI

> **Tip for Submission:** Copy and paste the sections below directly into your Devpost project form at [opencv26.devpost.com](https://opencv26.devpost.com/).

---

### Project Title
SafeSight AI: Autonomous Physical Site Safety Supervisor Agent

### Elevator Pitch (One-liner)
An Agentic Vision safety supervisor bridging OpenCV 5 spatial tracking with AWS Bedrock to autonomously detect, reason about, and mitigate industrial hazards in real time.

---

### Inspiration
Industrial worksites—from manufacturing floors to high-voltage substations—are fraught with hazards. Despite billions spent on passive CCTV, workplace accidents claim thousands of lives and cost over $170 billion annually worldwide. 

Traditional computer vision simply raises noisy false alarms that operators quickly learn to ignore. We asked: *What if the vision system didn't just 'see' pixels, but acted as an autonomous safety supervisor with deep regulatory understanding and the power to trigger physical mitigations?* 

That question gave birth to **SafeSight AI**—built specifically for the OpenCV AI Competition 2026 Agentic Vision Track.

---

### What It Does
SafeSight AI provides 24/7 autonomous oversight for high-risk physical spaces:
1. **Perception**: Uses **OpenCV 5** to segment moving personnel, calculate trajectory velocities, and perform millisecond geometric collision checks against complex polygonal exclusion zones.
2. **Cognitive Reasoning**: When a breach occurs, the frame ROI and telemetry are piped to **AWS Bedrock** (Claude 3.5 Sonnet / Multi-modal). The agent evaluates the threat level, formulates a mitigation strategy, and retrieves relevant regulatory standards (such as OSHA 29 CFR 1910.212 for Machine Guarding).
3. **Autonomous Action**: Rather than passively pinging an operator, SafeSight AI sequences real-time tools:
   - Triggers emergency PLC interlock relays to power down machinery before impact.
   - Dispatches geo-targeted physical safety teams with situational briefs.
   - Compiles immutable compliance audit logs streamed directly into **AWS S3**.

---

### How We Built It
- **OpenCV 5 Perception Pipeline**:
  - `cv2.createBackgroundSubtractorMOG2` with dynamic shadow filtering and morphological noise reduction (`cv2.morphologyEx`).
  - Spatial containment verification via `cv2.pointPolygonTest` on arbitrary multi-vertex exclusion perimeters.
  - Custom alpha-blended Heads-Up Display (HUD) using `cv2.addWeighted`, bounding box tracking, and centroid velocity calculations.
  - Substantive ROI cropping and base64 serialization for multimodal consumption.
- **AWS Bedrock & Cloud Infrastructure**:
  - `boto3` client orchestrating AWS Bedrock (`anthropic.claude-3-5-sonnet-20241022-v2:0`).
  - Dynamic tool-use loop providing the LLM with structured APIs (`trigger_emergency_interlock`, `cite_osha_regulation`, `dispatch_safety_supervisor`, `log_incident_s3`).
  - S3 bucket integration for continuous safety compliance telemetry.
  - Built-in zero-friction fallback engine guaranteeing seamless offline evaluation for judges.
- **Frontend & Deployment**:
  - Streamlit dashboard providing real-time video telemetry, live cognitive thought traces, interactive simulation loops, and exportable audit records.

---

### Challenges We Ran Into
- **Latency in Real-Time Safety**: Machine guarding requires sub-second reaction. We solved this by splitting perception from reasoning: OpenCV 5 handles continuous high-frame-rate spatial collision tracking at the edge, while AWS Bedrock is selectively triggered with contextual metadata and target ROIs only when an anomaly is confirmed.
- **Judge Reproducibility**: Cloud credentials can be tricky for hackathon judges to set up. We engineered a dual-mode fallback architecture that automatically uses active AWS credentials if present, but seamlessly executes deterministic high-fidelity agent reasoning traces offline if credentials are not configured.

---

### Accomplishments That We're Proud Of
- Delivering a true **Agentic Vision** loop: The system doesn't stop at bounding boxes; it perceives, reasons through legal compliance, and autonomously executes hardware containment tools.
- A 100% reproducible, 1-command startup that judges can run locally or test via synthetic simulation.
- Clean architectural synergy between OpenCV 5's mathematical speed and AWS Bedrock's reasoning capability.

---

### What We Learned
- Combining geometric algorithms (`cv2.pointPolygonTest`) with multimodal LLMs provides the best of both worlds: deterministic sub-millisecond boundary checks backed by nuanced human-level reasoning.
- Structuring LLM agent tools with standardized regulatory knowledge bases (OSHA mandates) dramatically increases the practical utility of AI in physical industry.

---

### What's Next for SafeSight AI
- Deploying OpenCV 5 COOL (Cloud-Optimized OpenCV Library) pipelines to stream directly from multi-camera IP feeds via AWS Kinesis Video Streams.
- Integrating edge microcontrollers (ESP32/Raspberry Pi) for physical relay interlock testing in physical pilot facilities.

---

### Built With
- `opencv-5`
- `aws-bedrock`
- `aws-s3`
- `python`
- `streamlit`
- `computer-vision`
- `agentic-ai`
- `multimodal-ai`
