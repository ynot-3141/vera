def build_prompt(
    category: dict,
    merchant: dict,
    trigger: dict,
    customer: dict | None = None,
    tone: str = "professional",
    focus: str = "merchant growth",
):


    identity = merchant.get("identity", {})
    performance = merchant.get("performance", {})
    signals = merchant.get("signals", [])
    offers = merchant.get("offers", [])

    # Find the merchant's active offer
    active_offer = next(
        (offer for offer in offers if offer.get("status") == "active"),
        None,
    )

    offer_text = "No active offer"

    if active_offer:
        offer_text = (
            f"{active_offer['title']} "
            f"(₹{active_offer['price']})"
        )

    customer_text = "No customer context"

    if customer:
        customer_text = (
            f"Last visit: {customer.get('last_visit_days', 'Unknown')} days\n"
            f"Consent: {customer.get('consent', False)}"
        )

    return f"""
You are Vera, Magicpin's AI merchant growth assistant.

Write ONE WhatsApp-style message.

RULES
- Maximum 45 words
- Friendly but professional
- Tone: {tone}
- Focus: {focus}
- Use ONLY the facts provided
- Never invent numbers, discounts or offers
- End with one clear CTA

BUSINESS
Name: {identity.get('name')}
Category: {category.get('name')}
Locality: {identity.get('locality')}
City: {identity.get('city')}

PERFORMANCE
Views: {performance.get('views')}
Calls: {performance.get('calls')}
7-day change: {performance.get('delta_7d')}

ACTIVE OFFER
{offer_text}

TRIGGER
Type: {trigger.get('type')}
Keyword: {trigger.get('keyword')}
Searches: {trigger.get('searches')}
Festival: {trigger.get('festival')}

SIGNALS
{signals}

CUSTOMER
{customer_text}

Generate only the merchant message.
""".strip()