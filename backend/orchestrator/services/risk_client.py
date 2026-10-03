from typing import Any


def analyze_risk(evidence_package: dict[str, Any]) -> dict[str, Any]:
    """
    Temporary Risk Engine client.

    This mock will later be replaced by an HTTP call to
    Person 3's Risk Engine.
    """

    return {
        "risk_score": 0.82,
        "risk_level": "HIGH",
        "confidence": 0.87,

        "portfolio": {
            "total_value": 1_000_000,
            "affected_sector_exposure": 0.49,
        },

        "asset_risk": [
            {
                "ticker": "XOM",
                "exposure": 0.245,
                "scenario_impact": -0.061,
                "portfolio_contribution": -0.015,
            },
            {
                "ticker": "CVX",
                "exposure": 0.245,
                "scenario_impact": -0.055,
                "portfolio_contribution": -0.013,
            },
        ],

        "scenarios": {
            "mild": {
                "sector_impact": -0.02,
                "portfolio_impact": -0.0098,
            },
            "base": {
                "sector_impact": -0.058,
                "portfolio_impact": -0.0284,
            },
            "severe": {
                "sector_impact": -0.095,
                "portfolio_impact": -0.0466,
            },
        },

        "historical_statistics": {
            "events": 7,
            "mean_impact": -0.061,
            "median_impact": -0.058,
            "best_case": -0.021,
            "worst_case": -0.104,
        },

        "key_risk_drivers": [
            "High energy-sector exposure",
            "Offshore production disruption",
            "Refinery disruption risk",
        ],

        "evidence": evidence_package,
    }