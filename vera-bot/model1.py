# models.py

from pydantic import BaseModel




class Identity(BaseModel):
    name: str
    city: str
    locality: str




class Delta7D(BaseModel):
    views_pct: float = 0.0
    calls_pct: float = 0.0
    ctr_pct: float = 0.0



# Overall business performance


class Performance(BaseModel):
    views: int = 0
    calls: int = 0
    delta_7d: Delta7D



# Merchant offers
# Only one may be active at a time


class Offer(BaseModel):
    title: str
    price: int
    status: str



# Merchant object (matches the dataset)


class Merchant(BaseModel):
    merchant_id: str
    category_slug: str

    identity: Identity
    performance: Performance

    offers: list[Offer] = []
    signals: list[str] = []
    conversation_history: list[dict] = []

# Category information


class Category(BaseModel):
    slug: str
    name: str




class Trigger(BaseModel):
    trigger_id: str
    merchant_id: str

    type: str

    keyword: str | None = None
    searches: int | None = None

    festival: str | None = None




class Customer(BaseModel):
    customer_id: str

    name: str | None = None
    consent: bool = False
    last_visit_days: int | None = None




class ContextRequest(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: dict
    delivered_at: str


class TickRequest(BaseModel):
    now: str
    available_triggers: list[str]


class ReplyRequest(BaseModel):
    conversation_id: str
    merchant_id: str
    customer_id: str | None = None
    from_role: str
    message: str
    received_at: str
    turn_number: int




class ComposeResponse(BaseModel):
    message: str
    cta: str
    send_as: str
    suppression_key: str
    rationale: str