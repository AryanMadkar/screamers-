from database.db import db
from datetime import datetime

lead_collection = db['leads']
extraction_logs_collection = db['extraction_logs']

def create_lead(conversation_id, user_id):
    lead = {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "name": None,
        "intent": None,
        "location": None,
        "amenities": None,
        "meeting_time": None,
        "onboarding_step": "intent",  # FIX: changed from "welcome" to "intent" to prevent KeyError
        "created_at": datetime.utcnow(),
    }
    lead_collection.insert_one(lead)
    return lead

def get_lead(conversation_id):
    lead = lead_collection.find_one({"conversation_id": conversation_id})
    return lead

def update_lead(conversation_id, updates: dict):
    lead_collection.update_one({"conversation_id": conversation_id}, {"$set": updates})

def log_extraction(conversation_id, user_message, extracted: dict):
    """Logs extraction attempt for debugging and analytics."""
    extraction_logs_collection.insert_one({
        "conversation_id": conversation_id,
        "user_message": user_message,
        "extracted_value": extracted.get("value"),
        "confidence": extracted.get("confidence"),
        "raw_understood": extracted.get("raw_understood"),
        "timestamp": datetime.utcnow()
    })