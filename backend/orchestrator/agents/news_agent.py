from typing import Any

from backend.orchestrator.graph.state import AnalysisState


def news_node(state: AnalysisState) -> dict[str, Any]:
    return {
        "news_data": {
            "article_count": 18,
            "overall_sentiment": -0.72,
            "key_signals": [
                "Refinery disruption risk",
                "Offshore production risk",
                "Supply chain disruption"
            ],
        },
        "agent_trace": [
            {
                "agent": "news",
                "status": "completed",
                "source": "mock",
            }
        ],
    }