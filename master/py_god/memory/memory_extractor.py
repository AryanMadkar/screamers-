import re


class MemoryExtractor:


    def extract(self, session):

        text = session.current_text.lower()

        memory = session.memory


        if memory.interested is None:

            if "yes" in text:

                memory.interested = True

            elif "no" in text:

                memory.interested = False


        if memory.purpose is None:

            if "buy" in text:

                memory.purpose = "buy"

            elif "rent" in text:

                memory.purpose = "rent"


        if memory.property_type is None:

            if "flat" in text:

                memory.property_type = "flat"

            elif "villa" in text:

                memory.property_type = "villa"

            elif "office" in text:

                memory.property_type = "office"

            elif "penthouse" in text:

                memory.property_type = "penthouse"

            elif "plot" in text:

                memory.property_type = "plot"


        if memory.bhk is None:

            match = re.search(r"(\d+)\s*bhk", text)

            if match:

                memory.bhk = int(match.group(1))


        if memory.location is None:

            if "in " in text:

                memory.location = text.split("in ")[-1]


        if memory.budget is None:

            lakh = re.search(r"(\d+)\s*lakh", text)

            crore = re.search(r"(\d+)\s*crore", text)

            if lakh:

                memory.budget = lakh.group()

            elif crore:

                memory.budget = crore.group()


        amenities = []

        if "parking" in text:

            amenities.append("parking")

        if "swimming pool" in text:

            amenities.append("swimming pool")

        if "gym" in text:

            amenities.append("gym")

        if "garden" in text:

            amenities.append("garden")

        if "club house" in text:

            amenities.append("club house")

        if "lift" in text:

            amenities.append("lift")

        for item in amenities:

            if item not in memory.amenities:

                memory.amenities.append(item)

        return session