TRIGGER_PRIORITY = {
    "FESTIVAL": 5,
    "SPIKE": 4,
    "DIP": 3,
    "RECALL": 2,
    "RESEARCH": 1,
}


def get_priority(trigger_type: str) -> int:


    return TRIGGER_PRIORITY.get(trigger_type.upper(), 0)


def choose_best_trigger(triggers: list[dict]) -> dict | None:


    if not triggers:
        return None

    return max(
        triggers,
        key=lambda trigger: get_priority(trigger["type"])
    )