from dataclasses import dataclass
from enum import Enum

class DebatePhase(Enum):
    OPENING = "opening"
    DISCUSSION = "discussion"
    REBUTTAL = "rebuttal"
    CLOSING = "closing"
    SUMMARY = "summary"

@dataclass
class DebateConfig:
    """Configuration settings for a debate session."""
    topic: str
    pro_position: str
    con_position: str
    max_turns: int = 10
    style: str = "structured"
    time_per_turn: int = 300  # seconds 