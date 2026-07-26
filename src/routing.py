def determine_next_action(
    topic: str,
    urgency: str,
    needs_more_information: bool,
) -> str:
    """Determine the recommended next action for a triaged ticket."""

    # Request clarification before routing tickets that are not actionable yet
    if needs_more_information:
        return "Ask customer for more information"

    # Escalate clear tickets with high urgency to a human supervisor
    if urgency == "High":
        return "Escalate to human supervisor"

    # Map each supported topic to its default operational action
    topic_actions = {
        "Policy / Contract": "Route to policy service",
        "Claims / Damage": "Create or update a claim",
        "Billing / Payment": "Forward to billing team",
        "Technical / Online Access": "Forward to technical support",
        "Other": "Route to general customer service",
    }

    # Use general customer service as a safe fallback for unknown topics
    return topic_actions.get(
        topic,
        "Route to general customer service",
    )