def validate_intent(val):
    return isinstance(val, str) and val.lower() in ("buy", "rent")

def validate_location(val):
    return isinstance(val, str) and len(val.strip()) > 1

def validate_name(val):
    return isinstance(val, str) and len(val.strip()) > 0

def validate_bhk(val):
    """Accept any non-empty string like '2BHK', 'studio', '3 BHK', 'rk'."""
    return isinstance(val, str) and len(val.strip()) > 0

def validate_budget(val):
    """Accept any non-empty string like '50-80 lakhs', '20k/month', 'flexible'."""
    return isinstance(val, str) and len(val.strip()) > 0

def validate_amenities(val):
    return isinstance(val, str) and val is not None

def validate_meeting(val):
    return isinstance(val, str) and val is not None

def validate_contact_number(val):
    """Accepts any string that looks like a phone number."""
    if not isinstance(val, str):
        return False
    digits = ''.join(filter(str.isdigit, val))
    return len(digits) >= 10

# Optional fields — collected greedily but not blocking
def validate_property_type(val):
    return isinstance(val, str) and len(val.strip()) > 0

def validate_furnished(val):
    return isinstance(val, str) and val.lower() in ("fully", "semi", "unfurnished", "any", "no preference")

def validate_area_sqft(val):
    return isinstance(val, str) and len(val.strip()) > 0

def validate_facing(val):
    return isinstance(val, str) and len(val.strip()) > 0

def validate_floor_preference(val):
    return isinstance(val, str) and len(val.strip()) > 0

def validate_possession(val):
    return isinstance(val, str) and len(val.strip()) > 0
