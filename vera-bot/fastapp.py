from fastapi import FastAPI
from pydantic import BaseModel
from composer import compose
from model1 import ContextRequest, TickRequest, ReplyRequest
from rules.priority import choose_best_trigger
from memory import (
    merchant_store,
    category_store,
    trigger_store,
    customer_store,
    versions,
    save,
    load,
)
# making the api using fastapi 
app = FastAPI(title="vera-bot")




# now i am gonna make the first endpoint the simulator

@app.get("/v1/healthz")
def healthz():
    return{
        "status":"ok"
    }

@app.get("/v1/metadata")
def metadata():
    return {
        "my_name" : "BHARTI",
        "model" : "google/gemini-2.5-flash",
        "deterministic" : True,
        "versions" : "1.0.0",
    }
# now the thing is the incoming context need to be saved
@app.post("/v1/context")
def push_context(req: ContextRequest):

    # Create a unique key for this context object.
    key = f"{req.scope}:{req.context_id}"

    # Ignore older or duplicate versions.
    if req.version <= versions.get(key, -1):
        return {
            "accepted": True,
            "ack_id": key,
        }

    # Store the newest version number.
    versions[key] = req.version

    save(req.scope, req.context_id, req.payload)

    return {
        "accepted": True,
        "ack_id": key,
    }

# now we have to make the trigger words that the vera can identify
@app.post("/v1/tick")
def tick(req: TickRequest):

    all_triggers = []

    
    for trigger_id in req.available_triggers:
        trigger = trigger_store.get(trigger_id)
        if trigger:
            all_triggers.append(trigger)

    if not all_triggers:
        return {"actions": []}

    
    best_trigger = choose_best_trigger(all_triggers)

    
    merchant = merchant_store[best_trigger["merchant_id"]]
    category = category_store.get(merchant["category_slug"], {})

    
    result = compose(
        category=category,
        merchant=merchant,
        trigger=best_trigger,
        customer=None
    )

    actions = [{
        "merchant_id": merchant["merchant_id"],
        "trigger_id": best_trigger["trigger_id"],
        "customer_id": None,
        "send_as": result["send_as"],
        "body": result["message"],
        "cta": result["cta"],
        "suppression_key": result["suppression_key"],
    }]

    return {"actions": actions}





# handle the user's response after vera send a message.
@app.post("/v1/reply")
def reply(req: ReplyRequest):

    text = req.message.lower()

    # -----------------------------------------
    # 1. Detect repeated automated messages
    # -----------------------------------------
    auto_reply = "thank you for contacting us"

    if auto_reply in text:

        # End the conversation after the 4th repeat
        if req.turn_number >= 5:
            return {
                "action": "end",
                "body": "Looks like this is an automated response. I'll stop here."
            }

        # Otherwise wait before trying again
        return {
            "action": "wait",
            "wait_seconds": 100
        }

    # -----------------------------------------
    # 2. Handle hostile messages
    # -----------------------------------------
    if "stop" in text or "spam" in text:
        return {
            "action": "end",
            "body": "Understood. I won't send further messages."
        }

    # -----------------------------------------
    # 3. Merchant accepted the suggestion
    # -----------------------------------------
    if any(word in text for word in ["yes", "ok", "let's do it"]):
        return {
            "action": "send",
            "body": "Perfect! I'll prepare the campaign draft now."
        }

    # -----------------------------------------
    # 4. Default behaviour
    # -----------------------------------------
    return {
        "action": "wait",
        "wait_seconds": 300
    }