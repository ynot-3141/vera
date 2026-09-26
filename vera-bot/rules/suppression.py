def make_suppression_key(trigger: dict, merchant: dict) -> str:


    trigger_type = trigger["type"].lower()
    merchant_id = merchant["merchant_id"]
    trigger_id = trigger["trigger_id"]

    return f"{trigger_type}_{merchant_id}_{trigger_id}"


def is_duplicate(key: str, sent_keys: set[str]) -> bool:


    return key in sent_keys


def remember_key(key: str, sent_keys: set[str]) -> None:


    sent_keys.add(key)