from onboarding.validator import (
    validate_intent, validate_location, validate_name,
    validate_bhk, validate_budget, validate_amenities,
    validate_meeting, validate_contact_number,
    validate_property_type, validate_furnished,
    validate_area_sqft, validate_facing,
    validate_floor_preference, validate_possession,
)

OFFICE_ADDRESS = "123 Prestige Tower, Bandra West, Mumbai - 400050"

# ─────────────────────────────────────────────
# REQUIRED STEPS  (agent will always ask these)
# ─────────────────────────────────────────────
STEPS = [
    "intent",        # buy / rent
    "location",      # city / area
    "bhk",           # 1BHK / 2BHK / 3BHK / studio
    "budget",        # price range
    "name",          # user's name
    "contact",       # phone number
    "meeting",       # when to meet
]

# DB field name for each step
STEP_FIELDS = {
    "intent":   "intent",
    "location": "location",
    "bhk":      "bhk",
    "budget":   "budget",
    "name":     "name",
    "contact":  "contact_number",
    "meeting":  "meeting_time",
}

VALIDATORS = {
    "intent":   validate_intent,
    "location": validate_location,
    "bhk":      validate_bhk,
    "budget":   validate_budget,
    "name":     validate_name,
    "contact":  validate_contact_number,
    "meeting":  validate_meeting,
}

CLARIFY_PROMPTS = {
    "intent":   "Are you looking to **buy** a property or **rent** one?",
    "location": "Which city or area are you looking in? For example — Andheri, Pune, Navi Mumbai?",
    "bhk":      "How many bedrooms are you looking for? Like 1BHK, 2BHK, 3BHK — or a studio?",
    "budget":   "What's your budget range? For example — ₹50–80 lakhs, or ₹20,000/month for rent?",
    "name":     "May I know your name so I can address you properly?",
    "contact":  "Could you share your contact number so our team can reach out to you?",
    "meeting":  f"Would you be open to a quick call or office visit? We're at {OFFICE_ADDRESS} — what time suits you?",
}

TRANSITION_PROMPTS = {
    "intent": "Are you looking to **buy** or **rent** a property?",
}

# ─────────────────────────────────────────────
# GREEDY EXTRACTION  (all fields in one shot)
# ─────────────────────────────────────────────
EXTRACTION_SYSTEM_PROMPT = """
You are an expert real estate lead data extractor for an Indian real estate agency.

Carefully read the full conversation history below and extract all available lead details.
Be smart — users often mention multiple details in one message (e.g. "I want a 2BHK flat in Malad under 40 lakhs").

Fields to extract:

1.  intent         — Must be exactly "buy" or "rent". Detect from: buy/purchase/kharidna → "buy", rent/lease/kiraye → "rent".
2.  location       — City, area, or neighbourhood (e.g. "Malad West, Mumbai", "Pune", "Navi Mumbai"). Clean up STT noise.
3.  bhk            — Bedroom config as a short string (e.g. "1BHK", "2BHK", "3BHK", "4BHK", "studio", "rk", "penthouse").
4.  budget         — Budget as a human-readable string (e.g. "40-60 lakhs", "30k/month", "1 crore", "flexible").
5.  name           — User's name, title-cased. Strip filler: "my name is", "I am", "call me".
6.  contact_number — 10-digit Indian phone number. Accept +91 prefix. Return digits only with +91 prefix if present.
7.  meeting_time   — When they can meet. Normalise to readable English (e.g. "Saturday evening", "weekdays after 6pm"). If not interested → "not available".
8.  property_type  — Property category if mentioned (e.g. "flat", "villa", "penthouse", "rk", "commercial", "plot").
9.  furnished      — Furnishing preference if mentioned (e.g. "fully", "semi", "unfurnished", "any").
10. area_sqft      — Carpet/super-built-up area preference if mentioned (e.g. "800-1000 sqft", "1200 sqft min").
11. facing         — Direction preference if mentioned (e.g. "east facing", "sea facing", "north").
12. floor_preference — Floor preference if mentioned (e.g. "high floor", "ground floor", "any").
13. possession     — Possession timeline if mentioned (e.g. "ready to move", "under construction", "within 6 months").
14. amenities      — Any other requirements (e.g. "gym, pool, parking", "gated society", "near school"). Set "none" if explicitly none.

Return ONLY a valid JSON object with these exact keys. Set null for anything not mentioned.
No markdown, no explanation, no extra text — just the JSON.

{
  "intent": null,
  "location": null,
  "bhk": null,
  "budget": null,
  "name": null,
  "contact_number": null,
  "meeting_time": null,
  "property_type": null,
  "furnished": null,
  "area_sqft": null,
  "facing": null,
  "floor_preference": null,
  "possession": null,
  "amenities": null
}
"""

# ─────────────────────────────────────────────
# OPTIONAL FIELD → DB KEY MAP  (greedy save)
# ─────────────────────────────────────────────
OPTIONAL_FIELD_MAP = {
    "property_type":   ("property_type",   validate_property_type),
    "furnished":       ("furnished",        validate_furnished),
    "area_sqft":       ("area_sqft",        validate_area_sqft),
    "facing":          ("facing",           validate_facing),
    "floor_preference":("floor_preference", validate_floor_preference),
    "possession":      ("possession",       validate_possession),
    "amenities":       ("amenities",        validate_amenities),
}
