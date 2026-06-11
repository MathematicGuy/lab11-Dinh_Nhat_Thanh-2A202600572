from hitl.hitl import ConfidenceRouter, hitl_decision_points


def test_confidence_router_escalates_high_risk_actions():
    router = ConfidenceRouter()

    decision = router.route(
        response="Transfer request drafted.",
        confidence=0.99,
        action_type="transfer_money",
    )

    assert decision.action == "escalate"
    assert decision.priority == "high"
    assert decision.requires_human is True


def test_confidence_router_uses_thresholds_for_general_queries():
    router = ConfidenceRouter()

    high = router.route("Balance answer", 0.95)
    medium = router.route("Loan answer", 0.8)
    low = router.route("Ambiguous answer", 0.5)

    assert high.action == "auto_send"
    assert medium.action == "queue_review"
    assert low.action == "escalate"


def test_hitl_decision_points_cover_three_review_scenarios():
    assert len(hitl_decision_points) == 3
    assert {point["hitl_model"] for point in hitl_decision_points} == {
        "human-in-the-loop",
        "human-on-the-loop",
        "human-as-tiebreaker",
    }
