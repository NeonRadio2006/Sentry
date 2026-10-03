from backend.orchestrator.graph.workflow import build_workflow


def test_supervisor_workflow():
    workflow = build_workflow()

    initial_state = {
        "user_query": (
            "A Category 4 hurricane is approaching the Gulf of Mexico. "
            "Analyze its impact on my energy portfolio."
        ),
        "portfolio_id": "demo-energy",
    }

    result = workflow.invoke(initial_state)

    # -------------------------
    # Supervisor
    # -------------------------

    assert result["event"]["type"] == "hurricane"
    assert result["event"]["location"] == "Gulf of Mexico"
    assert result["event"]["severity"] == 4

    # -------------------------
    # All agents executed
    # -------------------------

    agents = {
        trace["agent"]
        for trace in result["agent_trace"]
    }

    assert agents == {
        "supervisor",
        "weather",
        "news",
        "market",
        "historical",
        "evidence_merger",
        "risk_engine",
        "strategy",
        "synthesis",
    }

    # -------------------------
    # Individual evidence
    # -------------------------

    assert result["weather_data"]["severity"] == 4

    assert result["news_data"]["article_count"] == 18

    assert result["market_data"]["XOM"]["price"] == 120.0

    assert result["historical_data"]["matches"] == 7

    # -------------------------
    # Evidence package
    # -------------------------

    assert len(result["evidence"]) == 1

    evidence = result["evidence"][0]

    assert evidence["event"]["type"] == "hurricane"

    assert evidence["weather"]["severity"] == 4

    assert evidence["news"]["article_count"] == 18

    assert evidence["market"]["XOM"]["price"] == 120.0

    assert evidence["historical"]["matches"] == 7

    # -------------------------
    # Risk Engine
    # -------------------------

    assert result["risk_report"]["risk_score"] == 0.82

    assert result["risk_report"]["risk_level"] == "HIGH"

    assert result["risk_report"]["confidence"] == 0.87

    assert (
        result["risk_report"]["scenarios"]["base"]["portfolio_impact"]
        == -0.0284
    )

    # -------------------------
    # Strategy Agent
    # -------------------------

    assert result["strategy"]["action"] == "HEDGE_AND_REALLOCATE"

    assert result["strategy"]["confidence"] == 0.87

    assert len(result["strategy"]["proposed_actions"]) == 3

    assert (
        result["strategy"]["proposed_actions"][0]["target"]
        == "XOM"
    )

    assert (
        result["strategy"]["proposed_actions"][1]["target"]
        == "CVX"
    )

    assert (
        result["strategy"]["scenario"]["base_portfolio_impact"]
        == -0.0284
    )

    # -------------------------
    # Final Synthesis
    # -------------------------

    assert "final_analysis" in result

    final_analysis = result["final_analysis"]

    assert final_analysis["event"]["type"] == "hurricane"

    assert final_analysis["event"]["location"] == "Gulf of Mexico"

    assert final_analysis["event"]["severity"] == 4

    # Risk summary
    assert final_analysis["risk"]["level"] == "HIGH"

    assert final_analysis["risk"]["score"] == 0.82

    assert final_analysis["risk"]["confidence"] == 0.87

    assert (
        final_analysis["risk"]["base_portfolio_impact"]
        == -0.0284
    )

    # Risk drivers
    assert len(final_analysis["key_risk_drivers"]) == 3

    # Historical context
    assert (
        final_analysis["historical_context"]["events"]
        == 7
    )

    # Strategy
    assert (
        final_analysis["strategy"]["action"]
        == "HEDGE_AND_REALLOCATE"
    )

    # Evidence
    assert len(final_analysis["evidence"]) == 4

    # Audit
    assert (
        final_analysis["audit"]["quantitative_source"]
        == "risk_engine"
    )

    assert (
        final_analysis["audit"]["strategy_source"]
        == "strategy_agent"
    )