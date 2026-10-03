from typing import Any

from backend.orchestrator.graph.state import AnalysisState


def historical_node(state: AnalysisState) -> dict[str, Any]:
    return {
        "historical_data": {
            "matches": 7,
            "median_impact": -0.058,
            "mean_impact": -0.061,
            "best_case": -0.021,
            "worst_case": -0.104,
        },
        "agent_trace": [
            {
                "agent": "historical",
                "status": "completed",
                "source": "mock",
            }
        ],
    }