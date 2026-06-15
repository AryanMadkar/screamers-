import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from services.search import search_real_estate

llm = None

def get_llm():
    global llm

    if llm is None:
        # Get config from env/dotenv
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        # Strip optional wrapping quotes from .env value
        if api_key:
            api_key = api_key.strip('"\'')

        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY is not configured! Please open your '.env' file and "
                "set your real Groq API key in the GROQ_API_KEY field."
            )

        llm = ChatGroq(
            model=model,
            temperature=0.7,
            api_key=api_key
        )

    return llm


@tool
def search_web(query: str) -> str:
    """
    Search the web for Indian real estate listings, current property rates, market trends, or project availability.
    Input should be a search query (e.g. '2BHK rent in Malad West' or 'property rates in Pune').
    """
    return search_real_estate(query)


def generate_response(user_message, lead: dict = None):
    llm = get_llm()

    # Build system prompt with lead profile context
    lead_info = ""
    location = None
    if lead:
        parts = []
        name = lead.get("name")
        intent = lead.get("intent")
        location = lead.get("location")
        bhk = lead.get("bhk")
        budget = lead.get("budget")
        if name: parts.append(f"Name: {name}")
        if intent: parts.append(f"Intent: {intent}")
        if location: parts.append(f"Location: {location}")
        if bhk: parts.append(f"BHK: {bhk}")
        if budget: parts.append(f"Budget: {budget}")
        
        # Add optional ones if present
        for key in ["property_type", "furnished", "area_sqft", "facing", "floor_preference", "possession", "amenities"]:
            val = lead.get(key)
            if val:
                parts.append(f"{key.replace('_', ' ').capitalize()}: {val}")
        if parts:
            lead_info = "User Profile Context:\n" + "\n".join(f"- {p}" for p in parts) + "\n\n"

    system_prompt = (
        "You are Priya — a warm, professional, and knowledgeable real estate consultant in India.\n\n"
        f"{lead_info}"
        "Rules:\n"
        "- Acknowledge the user warmly. Use casual Indian English expressions naturally.\n"
        "- Never hallucinate. Never invent properties that don't exist.\n"
        "- If the user asks about listings, options, or market rates, use the search_web tool to fetch actual information.\n"
        "- Use the search results to answer. Show 2-3 listings with their name, price, location, and source/link if available.\n"
        "- If search returns no results, tell the user you couldn't find web listings and will consult your offline brokers.\n"
        "- Keep your response concise (usually 2-4 sentences or a brief list) and ask a single helpful follow-up question.\n"
        "- Do not mention tool calling or technical details to the user.\n"
        "- CRITICAL: If the user indicates they want to end the conversation, say goodbye, thank you, or wrap up, reply politely and append the tag '[END_CONVERSATION]' (include the square brackets) at the very end of your response."
    )

    # Bind tools
    tools = [search_web]
    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]

    try:
        response = llm_with_tools.invoke(messages)

        # If the model wants to call a tool
        if response.tool_calls:
            tool_call = response.tool_calls[0]
            if tool_call["name"] == "search_web":
                query = tool_call["args"].get("query")
                # If lead has location, inject it if not already in query
                if location and location.lower() not in query.lower():
                    search_res = search_real_estate(query, location)
                else:
                    search_res = search_real_estate(query)

                # Add AI response and Tool response to message chain
                messages.append(response)
                messages.append(ToolMessage(content=search_res, tool_call_id=tool_call["id"]))
                
                # Call LLM again
                final_response = llm.invoke(messages)
                return final_response.content

        return response.content
    except Exception as e:
        # fallback behavior if tool-calling or api fails
        try:
            fallback_response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ])
            return fallback_response.content
        except Exception as err:
            return f"I'm having trouble retrieving details right now. Let me check with our support team and get back to you! (Error: {str(err)})"