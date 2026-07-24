def determine_next_action(
    topic: str,
    urgency: str,
    needs_more_information: bool,
) -> str:
    if needs_more_information:
        return "Ask customer for more information"

    if urgency == "High":
        return "Escalate to human supervisor"

    topic_actions = {
        "Policy / Contract": "Route to policy service",
        "Claims / Damage": "Create or update a claim",
        "Billing / Payment": "Forward to billing team",
        "Technical / Online Access": "Forward to technical support",
        "Other": "Route to general customer service",
    }

    return topic_actions.get(
        topic,
        "Route to general customer service",
    )