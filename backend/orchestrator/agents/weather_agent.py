from typing import Any

from backend.orchestrator.graph.state import AnalysisState


def weather_node(state: AnalysisState) -> dict[str, Any]:
    event = state["event"]

    return {
        "weather_data": {
            "event_type": event.get("type"),
            "location": event.get("location"),
            "severity": event.get("severity"),
            "severity_score": 0.91,
            "affected_regions": ["Texas", "Louisiana"],
            "affected_sectors": ["Energy"],
        },
        "agent_trace": [
            {
                "agent": "weather",
                "status": "completed",
                "source": "mock",
            }
        ],
    }