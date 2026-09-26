merchant_store : dict[str, dict] = {}

category_store : dict[str, dict] = {}

trigger_store : dict[str, dict] = {}

customer_store : dict[str, dict] = {}

versions : dict[str, int] = {}

def save(scope: str, context_id : str, payload: dict):
    stores = {
        "merchant": merchant_store,
        "category": category_store,
        "trigger": trigger_store,
        "customer": customer_store       
    }

    if scope in stores:
        stores[scope][context_id] = payload

def load(scope:str, context_id: str) -> dict | None:

    stores = {
        "merchant": merchant_store,
        "category": category_store,
        "trigger": trigger_store,
        "customer": customer_store,        
    }

    return stores.get(scope, {}).get(context_id)
