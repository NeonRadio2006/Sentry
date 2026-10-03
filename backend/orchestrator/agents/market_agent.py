from typing import Any

from backend.orchestrator.graph.state import AnalysisState


def market_node(state: AnalysisState) -> dict[str, Any]:
    return {
        "market_data": {
            "XOM": {
                "price": 120.0,
                "change_1d": -0.032,
            },
            "CVX": {
                "price": 160.0,
                "change_1d": -0.027,
            },
        },
        "agent_trace": [
            {
                "agent": "market",
                "status": "completed",
                "source": "mock",
            }
        ],
    }