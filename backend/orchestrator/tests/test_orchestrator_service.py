from backend.orchestrator.services.orchestrator_service import (
    OrchestratorService,
)


def test_orchestrator_service():
    service = OrchestratorService()

    result = service.analyze(
        user_query=(
            "A Category 4 hurricane is approaching the Gulf of Mexico. "
            "Analyze its impact on my energy portfolio."
        ),
        portfolio_id="demo-energy",
    )

    assert result["analysis_id"]

    analysis = result["analysis"]

    assert analysis["event"]["type"] == "hurricane"
    assert analysis["event"]["location"] == "Gulf of Mexico"
    assert analysis["event"]["severity"] == 4

    assert analysis["risk"]["level"] == "HIGH"
    assert analysis["risk"]["score"] == 0.82

    assert analysis["strategy"]["action"] == "HEDGE_AND_REALLOCATE"