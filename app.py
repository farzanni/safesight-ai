"""SafeSight AI - Streamlit Control Center & Agentic Dashboard.

OpenCV AI Competition 2026 (powered by AWS) - Agentic Vision Track.
"""

import streamlit as st
import cv2
import numpy as np
import time
import json
import os
from PIL import Image

from src.config import CONFIG, ZoneConfig
from src.cv_engine import OpenCVSafetyPipeline
from src.agent_engine import AgenticVisionEngine

# Page configuration
st.set_page_config(
    page_title="SafeSight AI | Autonomous Physical Safety Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for industrial HUD styling
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1a1c24; padding: 12px; border-radius: 8px; border: 1px solid #2d3139; }
    .agent-box { background-color: #161b22; border-left: 4px solid #f0883e; padding: 15px; border-radius: 4px; font-family: monospace; }
    .danger-box { background-color: #2b1212; border-left: 4px solid #f85149; padding: 15px; border-radius: 4px; }
    .tool-badge { background-color: #1f242c; color: #58a6ff; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_engines():
    cv_pipe = OpenCVSafetyPipeline()
    agent_engine = AgenticVisionEngine()
    return cv_pipe, agent_engine

cv_pipeline, agent_engine = get_engines()

# Sidebar: Controls & AWS Status
st.sidebar.image("https://opencv.org/wp-content/uploads/2022/05/logo.png", width=160)
st.sidebar.title("🛡️ SafeSight AI")
st.sidebar.caption("OpenCV 5 + AWS Bedrock Agentic Vision")

st.sidebar.markdown("---")
st.sidebar.subheader("📡 Input Stream Source")
input_mode = st.sidebar.radio(
    "Select video feed:",
    ["Synthetic Factory Floor (Built-in Demo)", "Upload Video / Image", "Live Camera"],
    index=0
)

show_mog2_mask = st.sidebar.checkbox("Show OpenCV MOG2 Motion Mask", value=False)

st.sidebar.markdown("---")
st.sidebar.subheader("☁️ AWS Architecture Status")
st.sidebar.markdown("**Agent Core:** AWS Bedrock (`Claude 3.5 Sonnet`)")
st.sidebar.markdown("**Region:** `us-east-1`")
st.sidebar.markdown("**Audit Sink:** `s3://safesight-safety-audits`")
st.sidebar.info("💡 Running in dual-mode: Auto-detects active AWS credentials; falls back to deterministic agent simulator for zero-friction judging.")

# Main Header
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("Autonomous Physical Safety Inspector")
    st.caption("Real-Time Spatial Perimeter Enforcement & OSHA Regulatory Compliance Agent")

# Metrics bar
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
metric_col1.metric("Perception Engine", "OpenCV 5.0-dev", "60 FPS Target")
metric_col2.metric("Decision Engine", "AWS Bedrock", "Agentic Vision")
status_placeholder = metric_col3.empty()
actions_placeholder = metric_col4.empty()

status_placeholder.metric("Site Status", "NORMAL", "All Clear")
actions_placeholder.metric("Tools Dispatched", "0", "Standing By")

st.markdown("---")

col_video, col_agent = st.columns([3, 2])

# Session state initialization for incident log
if "incidents" not in st.session_state:
    st.session_state.incidents = []

if "tool_history" not in st.session_state:
    st.session_state.tool_history = []

# Video processing handler
frame_placeholder = col_video.empty()
agent_container = col_agent.container()

def handle_frame_analysis(frame_bgr):
    result = cv_pipeline.process_frame(frame_bgr)
    
    # Update video frame in Streamlit
    display_frame = result.motion_mask if show_mog2_mask else result.annotated_frame
    display_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(display_rgb, use_container_width=True)

    # Process violations through Agentic Vision
    if result.violation_detected:
        status_placeholder.metric("Site Status", "CRITICAL BREACH", "-Hazard Active", delta_color="inverse")
        
        # Take the most severe active violation
        primary_violation = result.active_violations[0]
        
        # Invoke agent
        eval_result = agent_engine.evaluate_hazard(primary_violation, result.violation_roi_b64)
        
        # Update metrics
        tools_called = len(eval_result.get("tool_calls", []))
        actions_placeholder.metric("Tools Dispatched", str(tools_called), "Active Containment", delta_color="normal")
        
        # Display Agent Reasoning in sidebar container
        with agent_container:
            st.markdown(f"### 🤖 Agentic Autonomous Supervisor")
            st.markdown(f"**Target Model:** `{eval_result.get('model', 'Claude 3.5 Sonnet')}`")
            
            st.markdown("#### 🧠 Real-Time Cognitive Trace")
            st.info(eval_result.get("thought_trace", ""))
            
            st.markdown("#### ⚡ Autonomous Tool Invocations")
            for tool in eval_result.get("tool_calls", []):
                t_name = tool.get("tool", "Action")
                t_stat = tool.get("status", "COMPLETE")
                st.markdown(f"- `<span class='tool-badge'>{t_name}</span>` → **{t_stat}**", unsafe_allow_html=True)
                if "standard" in tool:
                    st.caption(f"OSHA Ref: {tool['standard']} - {tool['title']}")
                if "action" in tool:
                    st.caption(f"Hardware Relay: {tool['action']}")
            
            st.markdown(f"**Decision:** :red[{eval_result.get('decision')}]")
        
        # Record incident history
        st.session_state.incidents.append({
            "timestamp": time.strftime("%H:%M:%S"),
            "zone": primary_violation.get("zone_name"),
            "severity": primary_violation.get("severity"),
            "speed": f"{primary_violation.get('speed_px', 0):.1f} px/s",
            "decision": eval_result.get("decision")
        })

    else:
        status_placeholder.metric("Site Status", "SECURE", "No Violations")
        with agent_container:
            st.markdown("### 🤖 Agentic Autonomous Supervisor")
            st.success("Perimeter Secure. OpenCV 5 spatial tracking active. Zero safety infractions detected.")
            st.caption("Agent is monitoring all zones via continuous spatial geometric polygon intersection tests.")

# Execution based on input mode
if input_mode == "Synthetic Factory Floor (Built-in Demo)":
    demo_video_path = "assets/sample_factory_floor.mp4"
    if not os.path.exists(demo_video_path):
        from scripts.generate_sample_assets import create_synthetic_demo_video
        create_synthetic_demo_video()
    
    cap = cv2.VideoCapture(demo_video_path)
    run_btn = col_video.button("▶️ Start Simulation Loop", key="run_sim")
    
    if run_btn:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            handle_frame_analysis(frame)
            time.sleep(0.04) # ~25 fps
        cap.release()
    else:
        # Show first frame
        ret, frame = cap.read()
        if ret:
            handle_frame_analysis(frame)
        cap.release()

elif input_mode == "Upload Video / Image":
    uploaded = col_video.file_uploader("Upload video (mp4, avi) or still image (jpg, png):", type=["mp4", "avi", "jpg", "png"])
    if uploaded is not None:
        if uploaded.type.startswith("image"):
            file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, 1)
            handle_frame_analysis(frame)
        else:
            temp_path = f"/tmp/{uploaded.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded.read())
            cap = cv2.VideoCapture(temp_path)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                handle_frame_analysis(frame)
                time.sleep(0.03)
            cap.release()

elif input_mode == "Live Camera":
    start_cam = col_video.checkbox("Activate Webcam Feed")
    if start_cam:
        cap = cv2.VideoCapture(0)
        while start_cam:
            ret, frame = cap.read()
            if not ret:
                col_video.error("Failed to read from camera.")
                break
            handle_frame_analysis(frame)
        cap.release()

# Bottom Section: Audit Log
st.markdown("---")
st.subheader("📋 Autonomous Safety Audit Log (Exportable to AWS S3 / SIEM)")
if st.session_state.incidents:
    st.table(st.session_state.incidents[-5:])
    st.download_button(
        label="📥 Download Full Incident Audit Log (JSON)",
        data=json.dumps(st.session_state.incidents, indent=2),
        file_name="safesight_safety_audit.json",
        mime="application/json"
    )
else:
    st.caption("No hazard violations recorded in this session.")
