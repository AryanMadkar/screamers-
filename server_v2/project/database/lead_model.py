from database.db import db
from datetime import datetime

lead_collection = db['leads']
extraction_logs_collection = db['extraction_logs']


def create_lead(conversation_id, user_id):
    lead = {
        "conversation_id": conversation_id,
        "user_id": user_id,

        # ── Core identity ──
        "name": None,
        "contact_number": None,        # Phone number for follow-up

        # ── Search intent ──
        "intent": None,                # "buy" | "rent"
        "location": None,              # City / area

        # ── Property preferences ──
        "bhk": None,                   # "1BHK" | "2BHK" | "3BHK" | "4BHK" | "studio" | "rk"
        "property_type": None,         # "flat" | "villa" | "penthouse" | "rk" | "commercial" | "plot"
        "budget": None,                # Budget range as plain string e.g. "50-80 lakhs" or "25k/month"
        "furnished": None,             # "fully" | "semi" | "unfurnished"
        "area_sqft": None,             # Preferred area e.g. "800-1000 sqft"
        "facing": None,                # "east" | "west" | "north" | "south" | "sea facing"
        "floor_preference": None,      # "ground" | "low" | "high" | "any"
        "possession": None,            # "ready to move" | "under construction" | "6 months"
        "amenities": None,             # Free-text summary of any extra requirements

        # ── Meeting ──
        "meeting_time": None,          # Normalised time e.g. "Saturday 3pm" | "not available"

        # ── Meta ──
        "onboarding_step": "intent",
        "clarification_retries": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    lead_collection.insert_one(lead)
    return lead


def get_lead(conversation_id):
    return lead_collection.find_one({"conversation_id": conversation_id})


def update_lead(conversation_id, updates: dict):
    updates["updated_at"] = datetime.utcnow()
    lead_collection.update_one({"conversation_id": conversation_id}, {"$set": updates})


def log_extraction(conversation_id, user_message, extracted: dict):
    """Logs every extraction attempt for debugging and analytics."""
    extraction_logs_collection.insert_one({
        "conversation_id": conversation_id,
        "user_message": user_message,
        "extracted": extracted,
        "timestamp": datetime.utcnow()
    })