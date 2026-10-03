from typing import Any

from backend.orchestrator.graph.state import AnalysisState


def synthesis_node(state: AnalysisState) -> dict[str, Any]:
    event = state["event"]
    risk_report = state["risk_report"]
    strategy = state["strategy"]
    evidence = state["evidence"][0]

    final_analysis = {
        "summary": (
            f"{event.get('type', 'Unknown').title()} event detected in "
            f"{event.get('location', 'unknown location')} with severity "
            f"{event.get('severity', 'unknown')}."
        ),
        "event": event,
        "risk": {
            "level": risk_report["risk_level"],
            "score": risk_report["risk_score"],
            "confidence": risk_report["confidence"],
            "base_portfolio_impact": (
                risk_report["scenarios"]["base"]["portfolio_impact"]
            ),
        },
        "key_risk_drivers": risk_report["key_risk_drivers"],
        "historical_context": {
            "events": risk_report["historical_statistics"]["events"],
            "mean_impact": (
                risk_report["historical_statistics"]["mean_impact"]
            ),
            "median_impact": (
                risk_report["historical_statistics"]["median_impact"]
            ),
        },
        "market_signals": evidence["market"],
        "news_signals": evidence["news"],
        "weather_signals": evidence["weather"],
        "strategy": strategy,
        "evidence": [
            {
                "source": "weather_agent",
                "data": evidence["weather"],
            },
            {
                "source": "news_agent",
                "data": evidence["news"],
            },
            {
                "source": "market_agent",
                "data": evidence["market"],
            },
            {
                "source": "historical_agent",
                "data": evidence["historical"],
            },
        ],
        "audit": {
            "agents_used": [
                "supervisor",
                "weather",
                "news",
                "market",
                "historical",
                "evidence_merger",
                "risk_engine",
                "strategy",
                "synthesis",
            ],
            "quantitative_source": "risk_engine",
            "strategy_source": "strategy_agent",
        },
    }

    return {
        "final_analysis": final_analysis,
        "agent_trace": [
            {
                "agent": "synthesis",
                "status": "completed",
                "source": "risk_report + strategy + evidence",
            }
        ],
    }