CATEGORY_RULES = {

    "dentists": {
        "name": "Dental Clinic",
        "tone": "clinical",
        "focus": "trust and preventive care",
        "default_cta": "Reply YES"
    },

    "restaurants": {
        "name": "Restaurant",
        "tone": "visual",
        "focus": "food offers and cravings",
        "default_cta": "Feature combo"
    },

    "salons": {
        "name": "Salon",
        "tone": "friendly",
        "focus": "appointments and grooming",
        "default_cta": "Boost bookings"
    },

    "pharmacies": {
        "name": "Pharmacy",
        "tone": "utility",
        "focus": "availability and convenience",
        "default_cta": "Promote now"
    },

    "default": {
        "name": "Business",
        "tone": "professional",
        "focus": "local growth",
        "default_cta": "Show suggestions"
    }
}


def get_category_rules(slug: str) -> dict:
    return CATEGORY_RULES.get(slug, CATEGORY_RULES["default"])