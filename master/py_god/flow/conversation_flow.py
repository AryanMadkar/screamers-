class ConversationFlow:


    def next_question(self, session):

        memory = session.memory


        if memory.interested is None:

            return "Are you looking for a property?"


        if memory.interested is False:

            memory.completed = True

            return "Thank you for your time. Have a nice day."


        if memory.purpose is None:

            return "Are you looking to buy or rent?"


        if memory.location is None:

            return "Which location are you looking for?"


        if memory.budget is None:

            return "What is your budget?"


        if memory.bhk is None:

            return "How many BHK are you looking for?"


        if memory.property_type is None:

            return "Are you looking for a flat, villa, office, penthouse or plot?"


        if len(memory.amenities) == 0:

            return "Do you have any preferred amenities like parking, swimming pool or gym?"


        memory.completed = True

        return None