"""SafeSight AI Configuration & System Parameters."""

from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class ZoneConfig:
    name: str
    polygon: List[Tuple[float, float]]  # Normalized (x, y) coordinates [0.0 - 1.0]
    severity: str  # "HIGH", "CRITICAL", "WARNING"
    description: str

@dataclass
class AppConfig:
    app_title: str = "SafeSight AI | Autonomous Physical Site Safety Agent"
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    min_detection_confidence: float = 0.50
    motion_history_length: int = 500
    motion_var_threshold: float = 16.0
    hazard_cooldown_seconds: int = 4
    
    # Default industrial zones (normalized coordinates: 0.0 to 1.0)
    default_zones: List[ZoneConfig] = field(default_factory=lambda: [
        ZoneConfig(
            name="Zone Alpha: Heavy Machinery Exclusion",
            polygon=[(0.55, 0.25), (0.95, 0.25), (0.95, 0.85), (0.55, 0.85)],
            severity="CRITICAL",
            description="Active robot arm operational radius. Unauthorized personnel prohibited."
        ),
        ZoneConfig(
            name="Zone Beta: High Voltage Arc Corridor",
            polygon=[(0.05, 0.60), (0.45, 0.60), (0.45, 0.95), (0.05, 0.95)],
            severity="HIGH",
            description="Transformer bay. Requires insulated PPE and authorized clearance."
        )
    ])

CONFIG = AppConfig()
