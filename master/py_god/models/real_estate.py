class RealEstateMemory:
    def __init__(self):
        self.interested = None
        self.purpose = None
        self.property_type = None
        self.furnishing = None
        self.location = None
        self.budget = None
        self.bhk = None
        self.amenities = []
        self.facing = None
        self.parking = None
        self.possession = None
        self.investment = None
        self.sentiment = None
        self.objections = None
        self.lead_score = None
        self.confidence = None
        self.completed = False
        
    def complete(self) -> bool:
        # Completeness is managed dynamically by the Agent Orchestrator.
        return self.completed
        
    def to_dict(self):
        return {
            "interested": self.interested,
            "purpose": self.purpose,
            "property_type": self.property_type,
            "furnishing": self.furnishing,
            "location": self.location,
            "budget": self.budget,
            "bhk": self.bhk,
            "amenities": self.amenities,
            "facing": self.facing,
            "parking": self.parking,
            "possession": self.possession,
            "investment": self.investment,
            "sentiment": self.sentiment,
            "objections": self.objections,
            "lead_score": self.lead_score,
            "confidence": self.confidence,
            "completed": self.completed,
        }