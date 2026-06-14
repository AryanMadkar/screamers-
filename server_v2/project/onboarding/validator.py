def validate_intent(val):
    return val in ("buy", "rent")

def validate_location(val):
    return val is not None and len(val.strip()) > 1

def validate_name(val):
    return val is not None and len(val.strip()) > 0

def validate_amenities(val):
    return val is not None

def validate_meeting(val):
    return val is not None
