# since the fastapp.py will recieve the request from the judge_simulator 
# this is the decision engine i am making so that the bot can take the input and gice us suitable output

# firstly let's put some trigger priority which will choose which message should be sent 
from rules.priority import choose_best_trigger
from rules.suppression import make_suppression_key
from gemini import generate_message
from rules.categories import get_category_rules
_trigger = {
    "Festival" : 5,
    "Spike" : 4,
    "Dip" : 3,
    "Recall" : 2,
    "Research" : 1,
}

def active_offer(merchant):
    for offer in merchant.get("offers",[]):
        if offer.get("status") == "active":
            return offer
    return None

def views_drop(merchant):
    delta = merchant.get("performance",{}).get("delta_7d", {})
    return abs(int(delta.get("views_pct", 0 ) * 100))

def calls_drop(merchant):
    delta = merchant.get("performance", {}).get("delta_7d", {})
    return abs(int(delta.get("calls_pct", 0)*100))

# now there's a chance that the bot can give out same answer twice and we don't want that

def suppression_key(trigger, merchant):
    return f"{trigger['type'].lower()}_{merchant['merchant_id']}"

# every category should have the message specific to it hence function related to it is required

def spike_message(category, merchant, trigger):
    business = merchant["identity"]["name"]
    locality = merchant["identity"].get("locality","your area")
    offer = active_offer(merchant)
    keyword = trigger.get("keyword", "your service")
    searches = trigger.get("searches", 0)

    if offer:
        return(
            f"{searches} people in {locality} searched for '{keyword}'today.\n"
            f"should I promote {business}'s {offer['title']} for Rs{offer['price']}?"
        )
    return (
        f"{searches} people in {locality} searched for '{keyword}' today.\n"
        f"Should I help {business} appear first?"
    )

def dip_message(merchant, trigger):
    business = merchant["identity"]["name"]
    offer = active_offer(merchant)
    views = views_drop(merchant)
    
    if offer:
        return (
            f"{business}'s views are down {views}% this week.\n"
            f"I can promote your {offer['title']} today."
        )

    return (
        f"{business}'s views are down {views}% this week.\n"
        "Let's improve your visibility today."
    )


def festival_message(trigger, merchant):
    festival = trigger.get("festival", "the festival")
    offer = active_offer(merchant)

    if offer:
        return (
            f"{festival} is coming soon.\n"
            f"Want me to feature your {offer['title']} for nearby customers?"
        )

    return (
        f"{festival} is coming soon.\n"
        "Want me to create a festive promotion?"
    )

def recall_message(customer, merchant):
    offer = active_offer(merchant)

    if customer and customer.get("last_visit_days"):
        days = customer["last_visit_days"]

        if offer:
            return (
                f"It's been {days} days since this customer visited.\n"
                f"Should I send them your {offer['title']}?"
            )

    return "Want me to re-engage your previous customers?"


# the whole purpose of the function is that it will read the trigger points, then choose the hardcoded message template and then create a cta.
# the whole thing will be returned in a JSON file

def compose(category, merchant, trigger, customer=None):
    trigger_type = trigger["type"].upper()

    rules = get_category_rules(category.get("slug"))

    cta = rules["default_cta"]
    tone = rules["tone"]
    focus = rules["focus"]


    signals = merchant.get("signals", [])

    # spike
    if trigger_type == "Spike":
        return{
            "message" : spike_message(category, merchant, trigger),
            "cta" : "kindly reply yes",
            "send_as" : "vera",
            "suppression_key" : make_suppression_key("DIP",merchant),
            "rationale" : "Recover declining traffic"
        }

    if trigger_type == "Dip":
        message = dip_message(merchant)
        if "perf_dip_severe" in signals:
            message += "\nThis is a good time to boost visibility"
        return {
            "message": message,
            "cta": "Boost now",
            "send_as": "vera",
            "suppression_key": make_suppression_key(trigger, merchant),
            "rationale": "Performance declined over the last 7 days."
        }
    if trigger_type == "Festival":
        return {
            "message" : festival_message(trigger, merchant),
            "cta" : "Featuring offer",
            "send_as": "vera",
            "suppression_key" : make_suppression_key("Festival",merchant),
            "rationale" : "seasonal promotion."
        }

    if trigger_type == "RECALL":

        return {
            "message": recall_message(customer, merchant),
            "cta": "Send recall",
            "send_as": "vera",
            "suppression_key": make_suppression_key(trigger, merchant),
            "rationale": "Re-engage inactive customers."
        }
    if trigger_type == "RESEARCH":

        locality = merchant["identity"].get("locality", "your locality")

        return {
            "message": (
                f"People in {locality} are actively researching businesses like yours.\n"
                "Want personalized growth suggestions?"
            ),
            "cta": "Show suggestions",
            "send_as": "vera",
            "suppression_key": make_suppression_key(trigger, merchant),
            "rationale": "Research intent detected."
        }

# since the we haven't hardcoded all the trigger words we can make fallback option so that it will return us the safe recommendation

    return {
        "message" : "Want help improving your today's visibility?",
        "cta": "show ideas",
        "send_as" : "vera",
        "suppresion_key" : suppression_key("Default", merchant),
        "rationale" : "Fallback recommendation"
    }