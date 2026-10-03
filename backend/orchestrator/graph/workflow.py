from langgraph.graph import END, START, StateGraph

from backend.orchestrator.agents.historical_agent import historical_node
from backend.orchestrator.agents.market_agent import market_node
from backend.orchestrator.agents.news_agent import news_node
from backend.orchestrator.agents.strategy_agent import strategy_node
from backend.orchestrator.agents.supervisor import analyze_query
from backend.orchestrator.agents.synthesis_agent import synthesis_node
from backend.orchestrator.agents.weather_agent import weather_node
from backend.orchestrator.graph.state import AnalysisState
from backend.orchestrator.services.evidence_service import merge_evidence
from backend.orchestrator.services.risk_client import analyze_risk


def supervisor_node(state: AnalysisState) -> dict:
    result = analyze_query(state["user_query"])

    return {
        "event": result["event"],
        "agent_trace": [
            {
                "agent": "supervisor",
                "status": "completed",
                "required_agents": result["required_agents"],
            }
        ],
    }


def risk_node(state: AnalysisState) -> dict:
    evidence_package = state["evidence"][0]

    risk_report = analyze_risk(evidence_package)

    return {
        "risk_report": risk_report,
        "agent_trace": [
            {
                "agent": "risk_engine",
                "status": "completed",
                "source": "mock",
            }
        ],
    }


def build_workflow():
    graph = StateGraph(AnalysisState)

    # -------------------------
    # Agent Nodes
    # -------------------------

    graph.add_node("supervisor", supervisor_node)

    graph.add_node("weather", weather_node)
    graph.add_node("news", news_node)
    graph.add_node("market", market_node)
    graph.add_node("historical", historical_node)

    graph.add_node("evidence_merger", merge_evidence)

    graph.add_node("risk_engine", risk_node)

    graph.add_node("strategy", strategy_node)

    graph.add_node("synthesis", synthesis_node)

    # -------------------------
    # Workflow
    # -------------------------

    graph.add_edge(START, "supervisor")

    # Parallel evidence collection
    graph.add_edge("supervisor", "weather")
    graph.add_edge("supervisor", "news")
    graph.add_edge("supervisor", "market")
    graph.add_edge("supervisor", "historical")

    # Merge all evidence
    graph.add_edge("weather", "evidence_merger")
    graph.add_edge("news", "evidence_merger")
    graph.add_edge("market", "evidence_merger")
    graph.add_edge("historical", "evidence_merger")

    # Risk analysis
    graph.add_edge("evidence_merger", "risk_engine")

    # Strategy generation
    graph.add_edge("risk_engine", "strategy")

    # Final synthesis
    graph.add_edge("strategy", "synthesis")

    # End
    graph.add_edge("synthesis", END)

    return graph.compile()