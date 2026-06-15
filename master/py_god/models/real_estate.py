class RealEstateMemory:

    def __init__(self):

        self.interested = None

        self.property_type = None

        self.purpose = None

        self.location = None

        self.budget = None

        self.bhk = None

        self.amenities = []

        self.completed = False
        
    def complete(self) -> bool:
        return (
            self.interested is True and
            self.property_type is not None and
            self.purpose is not None and
            self.location is not None and
            self.budget is not None and
            self.bhk is not None and
            len(self.amenities) > 0
        )
        
    def to_dict(self):
        return {
            "interested": self.interested,
            "property_type": self.property_type,
            "purpose": self.purpose,
            "location": self.location,
            "budget": self.budget,
            "bhk": self.bhk,
            "amenities": self.amenities,
            "completed": self.completed,
        }